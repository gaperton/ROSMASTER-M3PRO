"""Build or refresh the bundled ROSMASTER M3 Pro index. Output is always JSON."""
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
    parser.add_argument("--docs", default=str(DEFAULT_CORPUS), help="Markdown corpus root")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite index path")
    parser.add_argument("--rebuild", action="store_true", help="Delete and rebuild the index")
    args = parser.parse_args()

    corpus_root = Path(args.docs).resolve()
    db_path = Path(args.db).resolve()
    if not corpus_root.exists():
        payload: dict[str, Any] = {"error": "corpus_not_found", "corpus_root": str(corpus_root)}
        print(json.dumps(payload, indent=2))
        return 2

    from rag_index import build_index

    print(json.dumps(build_index(corpus_root, db_path, args.rebuild), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
