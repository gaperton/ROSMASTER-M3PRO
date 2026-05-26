"""Query the bundled ROSMASTER M3 Pro docs. Output is always JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = SKILL_ROOT / "assets" / "index" / "rosmaster_m3pro.sqlite"
DEFAULT_CORPUS = SKILL_ROOT / "assets" / "corpus"


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
        payload: dict[str, Any] = {"error": "index_not_found", "db_path": str(db_path)}
        print(json.dumps(payload, indent=2))
        return 2
    if not corpus_root.exists():
        payload = {"error": "corpus_not_found", "corpus_root": str(corpus_root)}
        print(json.dumps(payload, indent=2))
        return 2

    from rag_query import search

    print(json.dumps(search(args.query, args.top_k, db_path, corpus_root), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
