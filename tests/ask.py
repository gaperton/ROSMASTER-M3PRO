"""Ad-hoc side-by-side query tool — no scoring, just shows what each engine surfaces.

Useful for eyeballing relevance on unlabeled questions before deciding which to
add to cases.jsonl.

Usage:
    python tests/ask.py "How do I turn the robot on?"
    python tests/ask.py -k 5 "question 1" "question 2" "question 3"
    python tests/ask.py --file questions.txt   # one query per line, blank lines + #-comments ignored
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Force UTF-8 on Windows consoles so non-ASCII chars in heading paths don't crash print().
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import runner  # noqa: E402


def load_questions(args) -> list[str]:
    if args.file:
        out = []
        for line in Path(args.file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                out.append(line)
        return out
    return list(args.queries)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("queries", nargs="*", help="Questions to run (or use --file)")
    ap.add_argument("-k", "--top-k", type=int, default=3)
    ap.add_argument("--mode", default="hybrid", choices=("hybrid", "semantic", "keyword"))
    ap.add_argument("--file", help="Read one query per line from this file")
    args = ap.parse_args()

    questions = load_questions(args)
    if not questions:
        print("No questions provided.", file=sys.stderr)
        return 2

    engines = runner.engines()
    print(f"Loading {len(engines)} engines ({', '.join(engines)}) ...", flush=True)
    for q in questions:
        print(f"\n{'=' * 80}\nQ: {q}")
        for e in engines:
            print(f"\n  [{e}]")
            results = runner.search(e, q, mode=args.mode, top_k=args.top_k)
            if not results:
                print("    (no results)")
                continue
            for i, r in enumerate(results, 1):
                fp = r.get("file_path", "?")
                hp = r.get("heading_path") or ""
                loc = fp + (f"  ::  {hp}" if hp else "")
                print(f"    {i}. {loc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
