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
import sys
from pathlib import Path

import lancedb
from lancedb.rerankers import RRFReranker

# Import for side effect: the @register decorator in bge.py must run so LanceDB
# can rehydrate the embedding function attached to the chunks table.
from bge import BGE  # noqa: F401

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DB = SCRIPT_DIR / "index.lance"


def snippet(text: str, max_chars: int = 400) -> str:
    text = " ".join(text.split())
    return text if len(text) <= max_chars else text[:max_chars].rstrip() + " ..."


def run_search(table, query: str, mode: str, top_k: int):
    if mode == "hybrid":
        return (
            table.search(query, query_type="hybrid")
            .rerank(RRFReranker())
            .limit(top_k)
            .to_list()
        )
    if mode == "semantic":
        return table.search(query, query_type="vector").limit(top_k).to_list()
    return table.search(query, query_type="fts").limit(top_k).to_list()


def format_score(row: dict, mode: str) -> str:
    """LanceDB's result columns vary by mode; surface whichever the engine returned."""
    if mode == "hybrid":
        primary = row.get("_relevance_score")
        cos = row.get("_distance")
        bm = row.get("_score")
        parts = [f"rrf={primary:.4f}" if primary is not None else "rrf=—"]
        if cos is not None:
            parts.append(f"dist={cos:.3f}")
        if bm is not None:
            parts.append(f"fts={bm:.3f}")
        return "  ".join(parts)
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
    ap.add_argument("--full", action="store_true", help="Print the full chunk text instead of a snippet")
    args = ap.parse_args()

    db_path = Path(args.db).resolve()
    if not db_path.exists():
        print(f"Index not found at {db_path}. Run rag_index.py first.", file=sys.stderr)
        return 2

    db = lancedb.connect(str(db_path))
    table = db.open_table("chunks")

    results = run_search(table, args.query, args.mode, args.top_k)
    if not results:
        print("No results.")
        return 1

    for i, row in enumerate(results, 1):
        loc = row.get("file_path", "?")
        heading = row.get("heading_path") or ""
        if heading:
            loc += f"  ::  {heading}"
        scores = format_score(row, args.mode)
        text = row.get("text", "")
        print(f"\n[{i}] {scores}  {loc}")
        print("    " + (text if args.full else snippet(text)).replace("\n", "\n    "))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
