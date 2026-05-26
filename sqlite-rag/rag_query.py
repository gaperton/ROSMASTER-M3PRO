"""Query the local markdown RAG index built by rag_index.py.

Default mode is hybrid: runs semantic (sentence-transformer + sqlite-vec) and
keyword (SQLite FTS5 / BM25) retrieval in parallel and fuses them with
Reciprocal Rank Fusion. --mode lets you pick a single channel.

Usage:
    python rag_query.py "how do I unlock the controller buttons"
    python rag_query.py "moveit2 pick and place" -k 5
    python rag_query.py "lidar setup" --full              # full chunk text, not snippet
    python rag_query.py "ros2 topic list" --mode keyword  # FTS5/BM25 only
    python rag_query.py "what is a quaternion" --mode semantic
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import struct
import sys
from pathlib import Path

import numpy as np
import sqlite_vec
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "
RRF_K = 60
DEFAULT_BM25_HEADING_WEIGHT = 1.0
ROUTE_BOOST = 0.006

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DB = SCRIPT_DIR / "rag_index.db"


def serialize_f32(vec: np.ndarray) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec.astype(np.float32).tolist())


def open_db(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn


def snippet(text: str, max_chars: int = 400) -> str:
    text = " ".join(text.split())
    return text if len(text) <= max_chars else text[:max_chars].rstrip() + " ..."


STOP_WORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "by", "but", "can", "did", "do",
    "does", "for", "from", "had", "has", "have", "how", "i", "if", "in", "into",
    "is", "it", "its", "me", "my", "no", "not", "of", "on", "or", "so", "than",
    "that", "the", "their", "them", "then", "there", "these", "they", "this",
    "to", "was", "we", "were", "what", "when", "where", "which", "who", "why",
    "will", "with", "you", "your",
})


def to_fts5_query(q: str) -> str:
    """Convert a natural-language query into a safe FTS5 MATCH expression.

    Splits on word boundaries, drops common English stop words (they cost
    snippet noise — BM25's IDF already weights them near zero — but if the
    query is *only* stop words we keep them rather than return empty),
    double-quotes each remaining token to neutralize FTS5 operators, and
    joins with OR so results are ranked rather than required to contain
    every term.
    """
    raw = re.findall(r"\w+", q, flags=re.UNICODE)
    if not raw:
        return ""
    kept = [t for t in raw if t.lower() not in STOP_WORDS]
    tokens = kept or raw
    return " OR ".join(f'"{t}"' for t in tokens)


def query_profile(query: str) -> tuple[str, set[str]]:
    """Return (keyword_query, route_intents) for local beginner-query fixes."""
    q = query.lower()
    expansions: list[str] = []
    intents: set[str] = set()

    mapping_terms = ("map a room", "mapping", "slam", "make a map")
    if any(term in q for term in mapping_terms) or ("map" in q and "room" in q):
        intents.add("mapping")
        expansions.extend(["slam", "mapping", "cartographer", "gmapping", "slam_toolbox", "lidar"])
    for mapper in ("gmapping", "cartographer", "slam_toolbox"):
        if mapper in q:
            intents.add(f"{mapper}_exact")

    chassis_terms = (
        "cmd_vel",
        "velocity command",
        "terminal to move",
        "drive straight",
        "straight line",
        "1 meter",
        "one meter",
        "move the robot",
    )
    if any(term in q for term in chassis_terms):
        intents.add("chassis_velocity")
        expansions.extend(["cmd_vel", "linear", "velocity", "chassis", "ros2", "topic", "pub"])

    ros2_terms = ("install ros2", "ros2 install", "launch file", "package", "workspace")
    if any(term in q for term in ros2_terms):
        intents.add("ros2_workflow")
        expansions.extend(["ros2", "humble", "workspace", "package"])

    if not expansions:
        return query, intents
    return query + " " + " ".join(dict.fromkeys(expansions)), intents


def route_boost(file_path: str, heading_path: str, intents: set[str]) -> float:
    """Small post-fusion boost for predictable local-doc routing intents."""
    if not intents:
        return 0.0

    path = f"{file_path} {heading_path}".lower().replace("\\", "/")
    boost = 0.0

    if "mapping" in intents:
        if "gmapping_exact" in intents:
            if "6.lidar course/" in path and "gmapping" in path:
                boost += ROUTE_BOOST * 2.0
        elif "cartographer_exact" in intents:
            if "6.lidar course/" in path and "cartographer" in path:
                boost += ROUTE_BOOST * 2.0
        elif "slam_toolbox_exact" in intents:
            if "6.lidar course/" in path and "slam_toolbox" in path:
                boost += ROUTE_BOOST * 2.0
        elif "6.lidar course/" in path and "cartographer" in path:
            boost += ROUTE_BOOST * 2.0
        elif "6.lidar course/" in path and any(
            term in path for term in ("gmapping", "slam_toolbox", "rtab-map")
        ):
            boost += ROUTE_BOOST

    if "chassis_velocity" in intents:
        if "5.chassis control course/1.ros control" in path:
            boost += ROUTE_BOOST * 1.5
        elif "5.chassis control course/" in path:
            boost += ROUTE_BOOST

    if "ros2_workflow" in intents and "15.ros basic course/" in path:
        boost += ROUTE_BOOST

    return boost


def search_semantic(
    conn: sqlite3.Connection,
    model: SentenceTransformer,
    query: str,
    pool: int,
) -> list[tuple[int, float]]:
    """Return [(chunk_id, cosine_similarity)] best-first."""
    q_emb = model.encode(
        [QUERY_INSTRUCTION + query],
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0]
    rows = conn.execute(
        """
        SELECT rowid, distance
        FROM vec_chunks
        WHERE embedding MATCH ? AND k = ?
        ORDER BY distance
        """,
        (serialize_f32(np.asarray(q_emb)), pool),
    ).fetchall()
    # Unit vectors → ||a-b||^2 = 2 - 2*cos, so cos = 1 - distance^2 / 2.
    return [(rowid, 1.0 - (d * d) / 2.0) for rowid, d in rows]


def _fts_bm25_expr(conn: sqlite3.Connection, heading_weight: float = DEFAULT_BM25_HEADING_WEIGHT) -> str:
    """Pick the BM25 expression that matches whichever FTS5 schema this DB has.

    Pre-NX8 DBs: `fts_chunks(text)` — one column, default weights.
    NX8 DBs:     `fts_chunks(heading_path, text)` — weight heading vs. body.
    """
    col_count = len(conn.execute("SELECT * FROM fts_chunks LIMIT 0").description)
    heading_weight = float(heading_weight)
    return f"bm25(fts_chunks, {heading_weight:g}, 1.0)" if col_count == 2 else "bm25(fts_chunks)"


def search_keyword(
    conn: sqlite3.Connection,
    query: str,
    pool: int,
    heading_weight: float = DEFAULT_BM25_HEADING_WEIGHT,
) -> list[tuple[int, float]]:
    """Return [(chunk_id, bm25_score)] best-first. Higher score = better."""
    fts_query = to_fts5_query(query)
    if not fts_query:
        return []
    bm25_expr = _fts_bm25_expr(conn, heading_weight)
    rows = conn.execute(
        f"""
        SELECT rowid, {bm25_expr}
        FROM fts_chunks
        WHERE fts_chunks MATCH ?
        ORDER BY {bm25_expr}
        LIMIT ?
        """,
        (fts_query, pool),
    ).fetchall()
    # FTS5 bm25() is negated (lower = better); flip sign so higher = better.
    return [(rowid, -score) for rowid, score in rows]


def rrf_fuse(
    rankings: dict[str, list[int]],
    k: int = RRF_K,
) -> dict[int, float]:
    """Reciprocal Rank Fusion: score(doc) = sum_channels 1/(k + rank)."""
    scores: dict[int, float] = {}
    for ids in rankings.values():
        for rank, cid in enumerate(ids, start=1):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
    return scores


def fetch_chunks(
    conn: sqlite3.Connection,
    ids: list[int],
) -> dict[int, tuple[str, str, str]]:
    if not ids:
        return {}
    placeholders = ",".join("?" * len(ids))
    rows = conn.execute(
        f"SELECT id, file_path, heading_path, text FROM chunks WHERE id IN ({placeholders})",
        ids,
    ).fetchall()
    return {cid: (fp, hp, txt) for cid, fp, hp, txt in rows}


_MODEL_CACHE: dict[str, SentenceTransformer] = {}


def _get_model(name: str) -> SentenceTransformer:
    """Cached model loader so eval harnesses can reuse one model across many queries."""
    if name not in _MODEL_CACHE:
        _MODEL_CACHE[name] = SentenceTransformer(name)
    return _MODEL_CACHE[name]


def search(
    query: str,
    mode: str = "hybrid",
    top_k: int = 8,
    db_path: Path = DEFAULT_DB,
    model_name: str = DEFAULT_MODEL,
    pool: int = 0,
    bm25_heading_weight: float = DEFAULT_BM25_HEADING_WEIGHT,
) -> list[dict]:
    """Programmatic entry point — returns top-k chunks as plain dicts.

    Each dict carries: chunk_id, file_path, heading_path, text, primary (the
    score the caller would rank by in the chosen mode), and per-channel scores
    when available (cos for semantic, bm25 for keyword, rrf for hybrid).
    """
    pool = pool if pool > 0 else max(top_k * 4, 30)
    keyword_query, route_intents = query_profile(query)
    conn = open_db(Path(db_path))
    try:
        sem_results: list[tuple[int, float]] = []
        kw_results: list[tuple[int, float]] = []
        if mode in ("semantic", "hybrid"):
            sem_results = search_semantic(conn, _get_model(model_name), query, pool)
        if mode in ("keyword", "hybrid"):
            kw_results = search_keyword(conn, keyword_query, pool, bm25_heading_weight)

        sem_scores = {cid: s for cid, s in sem_results}
        kw_scores = {cid: s for cid, s in kw_results}

        if mode == "semantic":
            ranked = list(sem_results)[:top_k]
            primary_label = "cos"
        elif mode == "keyword":
            ranked = list(kw_results)[:top_k]
            primary_label = "bm25"
        else:
            fused = rrf_fuse(
                {
                    "semantic": [cid for cid, _ in sem_results],
                    "keyword": [cid for cid, _ in kw_results],
                }
            )
            meta = fetch_chunks(conn, list(fused.keys()))
            boosts = {}
            boosted = {}
            for cid, score in fused.items():
                file_path, heading_path, _ = meta.get(cid, ("?", "", ""))
                boost = route_boost(file_path, heading_path, route_intents)
                boosts[cid] = boost
                boosted[cid] = score + boost
            ranked = sorted(boosted.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
            primary_label = "rrf"

        if not ranked:
            return []

        ranked_ids = [cid for cid, _ in ranked]
        if mode != "hybrid":
            meta = fetch_chunks(conn, ranked_ids)
            boosts = {}

        out: list[dict] = []
        for cid, primary in ranked:
            file_path, heading_path, text = meta.get(cid, ("?", "", ""))
            out.append(
                {
                    "chunk_id": cid,
                    "file_path": file_path,
                    "heading_path": heading_path,
                    "text": text,
                    "primary_label": primary_label,
                    "primary": primary,
                    "cos": sem_scores.get(cid),
                    "bm25": kw_scores.get(cid),
                    "route_boost": boosts.get(cid, 0.0),
                }
            )
        return out
    finally:
        conn.close()


def fetch_fts_snippets(
    conn: sqlite3.Connection,
    query: str,
    ids: list[int],
) -> dict[int, str]:
    """Match-centered snippets for chunk ids the FTS query also hits.

    snippet() args: (table, col_index, start_mark, end_mark, ellipsis, max_tokens).
    Returns {} for chunks the query doesn't match — caller falls back to head-of-chunk.
    """
    fts_query = to_fts5_query(query)
    if not fts_query or not ids:
        return {}
    # Snippet should center on the body match, not the heading. Body is always
    # the last column: index 0 in pre-NX8 (text-only), index 1 in NX8 schema.
    col_count = len(conn.execute("SELECT * FROM fts_chunks LIMIT 0").description)
    text_col = col_count - 1
    placeholders = ",".join("?" * len(ids))
    rows = conn.execute(
        f"""
        SELECT rowid, snippet(fts_chunks, {text_col}, '[[', ']]', ' ... ', 32)
        FROM fts_chunks
        WHERE fts_chunks MATCH ? AND rowid IN ({placeholders})
        """,
        (fts_query, *ids),
    ).fetchall()
    return {rowid: snip for rowid, snip in rows}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", help="Natural-language question")
    ap.add_argument("-k", "--top-k", type=int, default=8, help="Number of results (default: 8)")
    ap.add_argument(
        "--mode",
        choices=("hybrid", "semantic", "keyword"),
        default="hybrid",
        help="Retrieval mode (default: hybrid = vec + BM25 fused with RRF)",
    )
    ap.add_argument(
        "--pool",
        type=int,
        default=0,
        help="Candidates per channel before fusion (default: max(top_k*4, 30))",
    )
    ap.add_argument("--db", default=str(DEFAULT_DB), help=f"SQLite index path (default: {DEFAULT_DB})")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"Embedding model (default: {DEFAULT_MODEL})")
    ap.add_argument(
        "--bm25-heading-weight",
        type=float,
        default=DEFAULT_BM25_HEADING_WEIGHT,
        help=(
            "BM25 weight for heading_path in two-column FTS indexes "
            f"(default: {DEFAULT_BM25_HEADING_WEIGHT:g})"
        ),
    )
    ap.add_argument("--full", action="store_true", help="Print the full chunk text instead of a snippet")
    args = ap.parse_args()

    db_path = Path(args.db).resolve()
    if not db_path.exists():
        print(f"Index not found at {db_path}. Run rag_index.py first.", file=sys.stderr)
        return 2

    pool = args.pool if args.pool > 0 else max(args.top_k * 4, 30)
    keyword_query, route_intents = query_profile(args.query)
    conn = open_db(db_path)

    sem_results: list[tuple[int, float]] = []
    kw_results: list[tuple[int, float]] = []

    if args.mode in ("semantic", "hybrid"):
        model = SentenceTransformer(args.model)
        sem_results = search_semantic(conn, model, args.query, pool)
    if args.mode in ("keyword", "hybrid"):
        kw_results = search_keyword(conn, keyword_query, pool, args.bm25_heading_weight)

    sem_scores = {cid: s for cid, s in sem_results}
    kw_scores = {cid: s for cid, s in kw_results}

    if args.mode == "semantic":
        ranked = [(cid, s) for cid, s in sem_results][: args.top_k]
        primary_label = "cos"
    elif args.mode == "keyword":
        ranked = [(cid, s) for cid, s in kw_results][: args.top_k]
        primary_label = "bm25"
    else:
        fused = rrf_fuse(
            {
                "semantic": [cid for cid, _ in sem_results],
                "keyword": [cid for cid, _ in kw_results],
            }
        )
        meta = fetch_chunks(conn, list(fused.keys()))
        boosts = {}
        boosted = {}
        for cid, score in fused.items():
            file_path, heading_path, _ = meta.get(cid, ("?", "", ""))
            boost = route_boost(file_path, heading_path, route_intents)
            boosts[cid] = boost
            boosted[cid] = score + boost
        ranked = sorted(boosted.items(), key=lambda kv: kv[1], reverse=True)[: args.top_k]
        primary_label = "rrf"

    if not ranked:
        print("No results.")
        conn.close()
        return 1

    ranked_ids = [cid for cid, _ in ranked]
    if args.mode != "hybrid":
        meta = fetch_chunks(conn, ranked_ids)
        boosts = {}
    fts_snips = (
        {} if args.full or args.mode == "semantic"
        else fetch_fts_snippets(conn, keyword_query, ranked_ids)
    )
    conn.close()

    for i, (cid, primary) in enumerate(ranked, 1):
        file_path, heading_path, text = meta.get(cid, ("?", "", ""))
        loc = file_path + (f"  ::  {heading_path}" if heading_path else "")
        extras = []
        if args.mode == "hybrid":
            cos = sem_scores.get(cid)
            bm = kw_scores.get(cid)
            extras.append(f"cos={cos:.3f}" if cos is not None else "cos=—")
            extras.append(f"bm25={bm:.2f}" if bm is not None else "bm25=—")
        extras_str = ("  " + "  ".join(extras)) if extras else ""
        primary_fmt = f"{primary:.4f}" if primary_label == "rrf" else f"{primary:.3f}"
        print(f"\n[{i}] {primary_label}={primary_fmt}{extras_str}  {loc}")
        if args.full:
            body = text
        elif cid in fts_snips:
            body = fts_snips[cid]
        else:
            body = snippet(text)
        print("    " + body.replace("\n", "\n    "))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
