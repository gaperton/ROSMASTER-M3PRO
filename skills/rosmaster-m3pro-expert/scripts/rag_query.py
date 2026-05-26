"""Query the bundled ROSMASTER M3 Pro docs and print JSON results."""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import struct
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = SKILL_ROOT / "assets" / "index" / "rosmaster_m3pro.sqlite"
DEFAULT_CORPUS = SKILL_ROOT / "assets" / "corpus"
CORPUS_PREFIX = "assets/corpus"
MODEL_NAME = "BAAI/bge-small-en-v1.5"
QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "
RRF_K = 60
BM25_HEADING_WEIGHT = 1.0
SNIPPET_CHARS = 700

STOP_WORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "by", "but", "can", "did", "do",
    "does", "for", "from", "had", "has", "have", "how", "i", "if", "in", "into",
    "is", "it", "its", "me", "my", "no", "not", "of", "on", "or", "so", "than",
    "that", "the", "their", "them", "then", "there", "these", "they", "this",
    "to", "was", "we", "were", "what", "when", "where", "which", "who", "why",
    "will", "with", "you", "your",
})

_MODEL: Any = None


def emit(payload: dict[str, Any], status: int = 0) -> int:
    print(json.dumps(payload, indent=2))
    return status


def open_db(db_path: Path) -> sqlite3.Connection:
    import sqlite_vec

    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn


def model() -> Any:
    from sentence_transformers import SentenceTransformer

    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(MODEL_NAME)
    return _MODEL


def serialize_f32(vec: Any) -> bytes:
    import numpy as np

    return struct.pack(f"{len(vec)}f", *vec.astype(np.float32).tolist())


def to_fts5_query(query: str) -> str:
    raw = re.findall(r"\w+", query, flags=re.UNICODE)
    kept = [token for token in raw if token.lower() not in STOP_WORDS]
    tokens = kept or raw
    return " OR ".join(f'"{token}"' for token in tokens)


def search_semantic(conn: sqlite3.Connection, query: str, pool: int) -> list[tuple[int, float]]:
    import numpy as np

    q_emb = model().encode(
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
    return [(rowid, 1.0 - (distance * distance) / 2.0) for rowid, distance in rows]


def search_keyword(conn: sqlite3.Connection, query: str, pool: int) -> list[tuple[int, float]]:
    fts_query = to_fts5_query(query)
    if not fts_query:
        return []
    rows = conn.execute(
        f"""
        SELECT rowid, bm25(fts_chunks, {BM25_HEADING_WEIGHT:g}, 1.0)
        FROM fts_chunks
        WHERE fts_chunks MATCH ?
        ORDER BY bm25(fts_chunks, {BM25_HEADING_WEIGHT:g}, 1.0)
        LIMIT ?
        """,
        (fts_query, pool),
    ).fetchall()
    return [(rowid, -score) for rowid, score in rows]


def rrf_fuse(rankings: list[list[int]]) -> dict[int, float]:
    scores: dict[int, float] = {}
    for ids in rankings:
        for rank, chunk_id in enumerate(ids, start=1):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (RRF_K + rank)
    return scores


def fetch_chunks(conn: sqlite3.Connection, chunk_ids: list[int]) -> dict[int, tuple[str, str, int, str]]:
    if not chunk_ids:
        return {}
    placeholders = ",".join("?" * len(chunk_ids))
    rows = conn.execute(
        f"""
        SELECT id, file_path, heading_path, ord, text
        FROM chunks
        WHERE id IN ({placeholders})
        """,
        chunk_ids,
    ).fetchall()
    return {chunk_id: (file_path, heading_path, ordinal, text) for chunk_id, file_path, heading_path, ordinal, text in rows}


def compact_text(text: str, max_chars: int = SNIPPET_CHARS) -> str:
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + " ..."


def strip_markdown_heading(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\\_", "_")
    text = re.sub(r"^\*\*(.*)\*\*$", r"\1", text.strip())
    text = re.sub(r"^__(.*)__$", r"\1", text.strip())
    return text.strip()


def find_line(abs_path: Path, heading_path: str, chunk_text: str) -> int | None:
    if not abs_path.exists():
        return None
    content = abs_path.read_text(encoding="utf-8", errors="replace")
    if heading_path:
        heading = strip_markdown_heading(heading_path.split(" > ")[-1])
        heading_match = re.search(rf"^#{{1,6}}\s+[*_]*{re.escape(heading)}[*_]*\s*$", content, re.MULTILINE)
        if heading_match:
            return content.count("\n", 0, heading_match.start()) + 1

    probe = chunk_text.strip()[:160]
    if probe:
        idx = content.find(probe)
        if idx >= 0:
            return content.count("\n", 0, idx) + 1
    return None


def corpus_path(relative_path: str) -> str:
    return f"{CORPUS_PREFIX}/" + relative_path.replace("\\", "/")


def source_fields(file_path: str, line: int | None) -> dict[str, Any]:
    label = Path(file_path).name
    path = corpus_path(file_path)
    target = f"{path}:{line}" if line is not None else path
    return {
        "label": label,
        "path": path,
        "line": line,
        "link": f"[{label}](<{target}>)",
    }


def search(
    query: str,
    top_k: int = 8,
    db_path: Path = DEFAULT_DB,
    corpus_root: Path = DEFAULT_CORPUS,
) -> dict[str, Any]:
    pool = max(top_k * 4, 30)
    conn = open_db(db_path)
    try:
        semantic = search_semantic(conn, query, pool)
        keyword = search_keyword(conn, query, pool)
        semantic_scores = {chunk_id: score for chunk_id, score in semantic}
        keyword_scores = {chunk_id: score for chunk_id, score in keyword}
        fused = rrf_fuse([
            [chunk_id for chunk_id, _ in semantic],
            [chunk_id for chunk_id, _ in keyword],
        ])
        ranked = sorted(fused.items(), key=lambda item: item[1], reverse=True)[:top_k]
        chunks = fetch_chunks(conn, [chunk_id for chunk_id, _ in ranked])
    finally:
        conn.close()

    results = []
    for rank, (chunk_id, rrf_score) in enumerate(ranked, start=1):
        file_path, heading_path, ordinal, text = chunks[chunk_id]
        line = find_line((corpus_root / file_path).resolve(), heading_path, text)
        results.append({
            "rank": rank,
            "chunk_id": chunk_id,
            "source": source_fields(file_path, line),
            "heading_path": heading_path,
            "chunk_ord": ordinal,
            "scores": {
                "rrf": rrf_score,
                "cos": semantic_scores.get(chunk_id),
                "bm25": keyword_scores.get(chunk_id),
            },
            "snippet": compact_text(text),
            "text": text,
        })

    return {
        "query": query,
        "top_k": top_k,
        "model": MODEL_NAME,
        "retrieval": "hybrid_rrf",
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Robot question or search query")
    parser.add_argument("-k", "--top-k", type=int, default=8, help="Number of JSON results")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite index path")
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS), help="Markdown corpus root")
    args = parser.parse_args()

    db_path = Path(args.db).resolve()
    corpus_root = Path(args.corpus).resolve()
    if not db_path.exists():
        return emit({"error": "index_not_found", "db_path": str(db_path)}, status=2)
    if not corpus_root.exists():
        return emit({"error": "corpus_not_found", "corpus_root": str(corpus_root)}, status=2)

    return emit(search(args.query, args.top_k, db_path, corpus_root))


if __name__ == "__main__":
    raise SystemExit(main())
