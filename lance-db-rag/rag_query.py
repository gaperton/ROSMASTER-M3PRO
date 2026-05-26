"""Query the local LanceDB RAG index built by rag_index.py.

Default mode is hybrid: LanceDB runs vector search (auto-embedded via the BGE
function attached to the schema) and FTS in parallel, then fuses them with
Reciprocal Rank Fusion via the built-in RRFReranker. --mode lets you pick a
single channel.

Usage:
    python rag_query.py "how do I unlock the controller buttons"
    python rag_query.py "moveit2 pick and place" -k 5
    python rag_query.py "lidar setup" --full
    python rag_query.py "ros2 topic list"   --mode keyword
    python rag_query.py "what is a quaternion" --mode semantic
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import lancedb

# Import for side effect: the @register decorators in bge.py must run so LanceDB
# can rehydrate whichever embedding function is attached to the opened table.
from bge import BGE, BGELarge  # noqa: F401

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DB = SCRIPT_DIR / "index.lance"

# Cross-encoder reranker. BAAI/bge-reranker-base (~280 MB) is trained on passage
# retrieval data by the same team that trains our BGE embedding model. Tried
# cross-encoder/ms-marco-MiniLM-L-6-v2 first; it over-fit to surface keyword
# similarity in markdown chunks and hurt diffuse-query quality even when it
# nudged labeled MRR up. BGE-reranker is matched to passages, not web QA.
DEFAULT_RERANKER = "BAAI/bge-reranker-base"
RERANK_POOL = 20  # how many RRF-fused candidates the cross-encoder re-scores

_CROSS_ENCODER_CACHE: dict = {}


def _get_cross_encoder(name: str):
    """Lazy import + cache so the module loads even if the user only does --no-rerank.

    Returns a sentence_transformers.CrossEncoder; left untyped to keep the
    import lazy.
    """
    if name not in _CROSS_ENCODER_CACHE:
        from sentence_transformers import CrossEncoder
        _CROSS_ENCODER_CACHE[name] = CrossEncoder(name)
    return _CROSS_ENCODER_CACHE[name]

# Kept in sync with sqlite-rag/rag_query.py so the two CLIs highlight identically.
STOP_WORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "by", "but", "can", "did", "do",
    "does", "for", "from", "had", "has", "have", "how", "i", "if", "in", "into",
    "is", "it", "its", "me", "my", "no", "not", "of", "on", "or", "so", "than",
    "that", "the", "their", "them", "then", "there", "these", "they", "this",
    "to", "was", "we", "were", "what", "when", "where", "which", "who", "why",
    "will", "with", "you", "your",
})
RRF_K = 60
ROUTE_BOOST = 0.006


def query_content_tokens(q: str) -> list[str]:
    raw = re.findall(r"\w+", q, flags=re.UNICODE)
    kept = [t for t in raw if t.lower() not in STOP_WORDS]
    return kept or raw


def to_lance_fts_query(q: str) -> str:
    """Stop-word-filtered OR-joined Tantivy query (parity with sqlite's to_fts5_query).

    Without this, Tantivy receives the raw natural-language string and lets
    common words anchor the BM25 ranking toward generic 'hub' docs.
    """
    tokens = query_content_tokens(q)
    return " OR ".join(tokens) if tokens else ""


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


def rrf_fuse(rankings: dict[str, list[str]], k_param: int = RRF_K) -> dict[str, float]:
    scores: dict[str, float] = {}
    for ids in rankings.values():
        for rank, cid in enumerate(ids, start=1):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k_param + rank)
    return scores


def snippet(text: str, max_chars: int = 400) -> str:
    text = " ".join(text.split())
    return text if len(text) <= max_chars else text[:max_chars].rstrip() + " ..."


def centered_snippet(text: str, tokens: list[str], radius: int = 150) -> str:
    """Slice the chunk around the first content-token match and bracket every match.

    Falls back to the head-of-chunk snippet when no token matches (typical for
    purely-semantic hits where the query and chunk share meaning but no words).
    """
    if not tokens:
        return snippet(text)
    # Boundaries on letters/digits only — `\b` would treat `_` as a word char and
    # miss matches inside compound identifiers like `quaternion_from_euler`.
    pattern = re.compile(
        r"(?<![A-Za-z0-9])(?:" + "|".join(re.escape(t) for t in tokens) + r")(?![A-Za-z0-9])",
        re.IGNORECASE,
    )
    first = pattern.search(text)
    if first is None:
        return snippet(text)
    start = max(0, first.start() - radius)
    end = min(len(text), first.end() + radius)
    excerpt = pattern.sub(lambda m: f"[[{m.group(0)}]]", text[start:end])
    excerpt = " ".join(excerpt.split())
    prefix = " ... " if start > 0 else ""
    suffix = " ... " if end < len(text) else ""
    return prefix + excerpt + suffix


def run_search(
    table,
    query: str,
    mode: str,
    top_k: int,
    pool: int = 0,
    rerank: bool = True,
    reranker_name: str = DEFAULT_RERANKER,
):
    """Orchestrate retrieval manually instead of using LanceDB's hybrid path.

    Pipeline for hybrid mode:
      1. Run vector + FTS independently with `pool` candidates each.
      2. RRF-fuse and keep top RERANK_POOL candidates.
      3. If rerank=True, score each (query, chunk_text) pair with a cross-encoder
         and re-sort. Otherwise return RRF order.

    Rationale for (1) and (2): three things diverged between Lance's built-in
    hybrid and sqlite-rag's hybrid — Tantivy received the raw natural-language
    string (sqlite pre-tokenizes), Lance's hybrid pool was small (sqlite uses
    max(top_k*4, 30)), and RRF inputs differed accordingly. This function fixes
    all three.

    Rationale for (3): RRF is rank-based and engine-agnostic. A cross-encoder
    re-scores the survivors with a real ML model that understands query-document
    semantics directly, sharper on diffuse queries where token overlap and
    vector centroids both mislead. Cost: ~50 ms / query for RERANK_POOL pairs.
    """
    pool = pool if pool > 0 else max(top_k * 4, 30)
    keyword_query, route_intents = query_profile(query)

    if mode == "semantic":
        return table.search(query, query_type="vector").limit(top_k).to_list()

    if mode == "keyword":
        fts_q = to_lance_fts_query(keyword_query)
        if not fts_q:
            return []
        return table.search(fts_q, query_type="fts").limit(top_k).to_list()

    # Hybrid: pool per channel, manual RRF.
    vector_rows = table.search(query, query_type="vector").limit(pool).to_list()
    fts_q = to_lance_fts_query(keyword_query)
    fts_rows = (
        table.search(fts_q, query_type="fts").limit(pool).to_list() if fts_q else []
    )

    # Merge rows by chunk_id, preserving both channels' raw scores.
    by_id: dict[str, dict] = {}
    for r in vector_rows:
        by_id[r["chunk_id"]] = dict(r)
    for r in fts_rows:
        cid = r["chunk_id"]
        if cid in by_id:
            by_id[cid]["_score"] = r.get("_score")
        else:
            row = dict(r)
            row.setdefault("_distance", None)
            by_id[cid] = row

    scores = rrf_fuse({
        "semantic": [r["chunk_id"] for r in vector_rows],
        "keyword": [r["chunk_id"] for r in fts_rows],
    })
    boosts = {}
    for cid, row in by_id.items():
        boost = route_boost(row.get("file_path", "?"), row.get("heading_path") or "", route_intents)
        boosts[cid] = boost
        if cid in scores:
            scores[cid] += boost

    # Narrow to a rerank pool first; cross-encoder only sees the top RERANK_POOL.
    fused_top = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    rerank_pool = fused_top[: max(RERANK_POOL, top_k)] if rerank else fused_top[:top_k]

    if rerank and rerank_pool:
        ce = _get_cross_encoder(reranker_name)
        # Prepend heading_path so the cross-encoder sees *what* the chunk is
        # about (e.g. "Mapping Tutorial > Step 3"), not just its words. Plain
        # `(query, text)` pairs lose this context and let the model over-rank
        # keyword-dense theory chunks above task-matching how-to chunks.
        pairs = []
        for cid, _ in rerank_pool:
            row = by_id[cid]
            heading = row.get("heading_path") or ""
            text = row.get("text", "")
            doc_text = f"{heading} — {text}" if heading else text
            pairs.append((query, doc_text))
        ce_scores = ce.predict(pairs)
        reranked = sorted(
            ((cid, float(s)) for (cid, _), s in zip(rerank_pool, ce_scores)),
            key=lambda kv: kv[1],
            reverse=True,
        )
        ranked = reranked[:top_k]
        score_label = "_ce_score"
    else:
        ranked = rerank_pool[:top_k]
        score_label = "_relevance_score"

    out = []
    for cid, score in ranked:
        row = by_id[cid]
        row[score_label] = score
        # Always carry the RRF score too so callers can see both.
        row["_relevance_score"] = scores.get(cid, row.get("_relevance_score"))
        row["_route_boost"] = boosts.get(cid, 0.0)
        out.append(row)
    return out


_TABLE_CACHE: dict[str, object] = {}


def _get_table(db_path: Path):
    """Cached table handle so eval harnesses don't reopen the DB on every query."""
    key = str(db_path)
    if key not in _TABLE_CACHE:
        db = lancedb.connect(key)
        _TABLE_CACHE[key] = db.open_table("chunks")
    return _TABLE_CACHE[key]


def search(
    query: str,
    mode: str = "hybrid",
    top_k: int = 8,
    db_path: Path = DEFAULT_DB,
    pool: int = 0,
    rerank: bool = False,
) -> list[dict]:
    """Programmatic entry point — returns top-k chunks as plain dicts.

    Each dict carries file_path, heading_path, text, primary (the engine's
    headline score: ce when rerank=True in hybrid, otherwise rrf / cos / fts),
    and per-channel scores when available.
    """
    table = _get_table(Path(db_path))
    rows = run_search(table, query, mode, top_k, pool, rerank=rerank)
    out: list[dict] = []
    for row in rows:
        d = row.get("_distance")
        cos = 1.0 - (d * d) / 2.0 if d is not None else None
        fts = row.get("_score")
        rrf = row.get("_relevance_score")
        ce = row.get("_ce_score")
        if mode == "hybrid":
            if ce is not None:
                primary_label, primary = "ce", ce
            else:
                primary_label, primary = "rrf", rrf
        elif mode == "semantic":
            primary_label, primary = "cos", cos
        else:
            primary_label, primary = "fts", fts
        out.append(
            {
                "file_path": row.get("file_path", "?"),
                "heading_path": row.get("heading_path") or "",
                "text": row.get("text", ""),
                "primary_label": primary_label,
                "primary": primary,
                "cos": cos,
                "bm25": fts,
                "rrf": rrf,
                "route_boost": row.get("_route_boost", 0.0),
            }
        )
    return out


def format_score(row: dict, mode: str) -> str:
    """LanceDB's result columns vary by mode; surface whichever the engine returned."""
    if mode == "hybrid":
        ce = row.get("_ce_score")
        rrf = row.get("_relevance_score")
        d = row.get("_distance")
        cos = 1.0 - (d * d) / 2.0 if d is not None else None
        bm = row.get("_score")
        boost = row.get("_route_boost") or 0.0
        parts = []
        if ce is not None:
            parts.append(f"ce={ce:+.3f}")
        if rrf is not None:
            parts.append(f"rrf={rrf:.4f}")
        if cos is not None:
            parts.append(f"cos={cos:.3f}")
        if bm is not None:
            parts.append(f"fts={bm:.3f}")
        if boost:
            parts.append(f"boost={boost:.3f}")
        return "  ".join(parts) if parts else "?=—"
    if mode == "semantic":
        d = row.get("_distance")
        # vectors are unit-normalized: cos = 1 - d^2 / 2
        cos = 1.0 - (d * d) / 2.0 if d is not None else None
        return f"cos={cos:.3f}" if cos is not None else "cos=—"
    bm = row.get("_score")
    return f"fts={bm:.3f}" if bm is not None else "fts=—"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", help="Natural-language question")
    ap.add_argument("-k", "--top-k", type=int, default=8, help="Number of results (default: 8)")
    ap.add_argument(
        "--mode",
        choices=("hybrid", "semantic", "keyword"),
        default="hybrid",
        help="Retrieval mode (default: hybrid)",
    )
    ap.add_argument("--db", default=str(DEFAULT_DB), help=f"LanceDB directory (default: {DEFAULT_DB})")
    ap.add_argument(
        "--pool",
        type=int,
        default=0,
        help="Candidates per channel before fusion (default: max(top_k*4, 30))",
    )
    ap.add_argument(
        "--rerank",
        action="store_true",
        help=(
            f"Enable cross-encoder reranking with {DEFAULT_RERANKER} (~280 MB, ~5x slower). "
            "Off by default: testing showed it trades wins on diffuse queries for losses "
            "on already-clean queries. Only affects hybrid mode."
        ),
    )
    ap.add_argument("--full", action="store_true", help="Print the full chunk text instead of a snippet")
    args = ap.parse_args()

    db_path = Path(args.db).resolve()
    if not db_path.exists():
        print(f"Index not found at {db_path}. Run rag_index.py first.", file=sys.stderr)
        return 2

    db = lancedb.connect(str(db_path))
    table = db.open_table("chunks")

    results = run_search(table, args.query, args.mode, args.top_k, args.pool, rerank=args.rerank)
    if not results:
        print("No results.")
        return 1

    tokens = query_content_tokens(args.query)
    for i, row in enumerate(results, 1):
        loc = row.get("file_path", "?")
        heading = row.get("heading_path") or ""
        if heading:
            loc += f"  ::  {heading}"
        scores = format_score(row, args.mode)
        text = row.get("text", "")
        if args.full:
            body = text
        else:
            body = centered_snippet(text, tokens)
        print(f"\n[{i}] {scores}  {loc}")
        print("    " + body.replace("\n", "\n    "))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
