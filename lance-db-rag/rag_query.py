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
from lancedb.rerankers import RRFReranker

# Import for side effect: the @register decorator in bge.py must run so LanceDB
# can rehydrate the embedding function attached to the chunks table.
from bge import BGE  # noqa: F401

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DB = SCRIPT_DIR / "index.lance"

# Kept in sync with sqlite-rag/rag_query.py so the two CLIs highlight identically.
STOP_WORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "by", "but", "can", "did", "do",
    "does", "for", "from", "had", "has", "have", "how", "i", "if", "in", "into",
    "is", "it", "its", "me", "my", "no", "not", "of", "on", "or", "so", "than",
    "that", "the", "their", "them", "then", "there", "these", "they", "this",
    "to", "was", "we", "were", "what", "when", "where", "which", "who", "why",
    "will", "with", "you", "your",
})


def query_content_tokens(q: str) -> list[str]:
    raw = re.findall(r"\w+", q, flags=re.UNICODE)
    kept = [t for t in raw if t.lower() not in STOP_WORDS]
    return kept or raw


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
) -> list[dict]:
    """Programmatic entry point — returns top-k chunks as plain dicts.

    Each dict carries file_path, heading_path, text, primary (the engine's
    headline score: rrf for hybrid, cos for semantic, fts for keyword), and
    per-channel scores when LanceDB exposes them.
    """
    table = _get_table(Path(db_path))
    rows = run_search(table, query, mode, top_k)
    out: list[dict] = []
    for row in rows:
        d = row.get("_distance")
        cos = 1.0 - (d * d) / 2.0 if d is not None else None
        fts = row.get("_score")
        rrf = row.get("_relevance_score")
        if mode == "hybrid":
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
            }
        )
    return out


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
