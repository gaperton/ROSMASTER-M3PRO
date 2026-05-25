"""Run every case in cases.jsonl against every engine, compute Hits@k and a per-case
diff, and print a comparison table.

Match rules (per case):
  - file_match  = expected_file appears anywhere in top-k results' file_path
  - chunk_match = file_match AND the matching result's heading_path contains
                  expected_heading_substring (case-insensitive). For each k we use
                  the *best* (lowest-rank) matching result.

Usage:
    python tests/evaluate.py
    python tests/evaluate.py --mode keyword
    python tests/evaluate.py --cases tests/cases.jsonl -k 1 3 8
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# Make tests/ importable as a sibling package regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import runner  # noqa: E402

KS = (1, 3, 8)


def load_cases(path: Path) -> list[dict]:
    cases = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            cases.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{path}:{i}: invalid JSON ({e})")
    return cases


def first_match_rank(results: list[dict], expected_file: str, heading_substr: str) -> tuple[int | None, int | None]:
    """Return (file_match_rank, chunk_match_rank). 1-indexed; None if no match."""
    file_rank = None
    chunk_rank = None
    for i, r in enumerate(results, 1):
        if expected_file in r.get("file_path", ""):
            if file_rank is None:
                file_rank = i
            if heading_substr and heading_substr.lower() in (r.get("heading_path", "") or "").lower():
                chunk_rank = i
                break
    return file_rank, chunk_rank


def score_engine(engine: str, cases: list[dict], mode: str, top_k: int) -> dict:
    file_hits = {k: 0 for k in KS if k <= top_k}
    chunk_hits = {k: 0 for k in KS if k <= top_k}
    file_rr_sum = 0.0
    chunk_rr_sum = 0.0
    per_case: list[dict] = []
    durations: list[float] = []

    for case in cases:
        start = time.perf_counter()
        results = runner.search(engine, case["query"], mode=mode, top_k=top_k)
        durations.append(time.perf_counter() - start)

        f_rank, c_rank = first_match_rank(
            results, case["expected_file"], case.get("expected_heading_substring", "")
        )
        for k in file_hits:
            if f_rank is not None and f_rank <= k:
                file_hits[k] += 1
            if c_rank is not None and c_rank <= k:
                chunk_hits[k] += 1
        if f_rank is not None:
            file_rr_sum += 1.0 / f_rank
        if c_rank is not None:
            chunk_rr_sum += 1.0 / c_rank
        per_case.append({
            "id": case["id"],
            "file_rank": f_rank,
            "chunk_rank": c_rank,
        })

    n = len(cases)
    return {
        "file_hits": file_hits,
        "chunk_hits": chunk_hits,
        "file_mrr": file_rr_sum / n if n else 0.0,
        "chunk_mrr": chunk_rr_sum / n if n else 0.0,
        "per_case": per_case,
        "median_ms": sorted(durations)[len(durations) // 2] * 1000 if durations else 0.0,
    }


def render_report(cases: list[dict], results_by_engine: dict[str, dict], mode: str, top_k: int) -> None:
    n = len(cases)
    engines = list(results_by_engine.keys())

    print(f"\n=== mode={mode}  top_k={top_k}  cases={n}  engines={','.join(engines)} ===\n")

    # Headline: MRR is the sharpest signal (weights rank-1 heavily); Hits@1/@3 next;
    # @8 is a coarse "did we find it at all" bound that usually saturates.
    print(f"{'metric':<22}" + "".join(f"{e:>14}" for e in engines))
    print(f"  file MRR             " + "".join(f"{results_by_engine[e]['file_mrr']:>14.3f}" for e in engines))
    print(f"  chunk MRR            " + "".join(f"{results_by_engine[e]['chunk_mrr']:>14.3f}" for e in engines))
    for k in KS:
        if k > top_k:
            continue
        row_file = [f"{results_by_engine[e]['file_hits'][k]}/{n}" for e in engines]
        row_chunk = [f"{results_by_engine[e]['chunk_hits'][k]}/{n}" for e in engines]
        print(f"  file-match @{k:<10}" + "".join(f"{v:>14}" for v in row_file))
        print(f"  chunk-match @{k:<9}" + "".join(f"{v:>14}" for v in row_chunk))
    print(f"  median latency (ms)  " + "".join(f"{results_by_engine[e]['median_ms']:>14.1f}" for e in engines))

    # Per-case diff: rank of first file-match and chunk-match per engine, side by side.
    print(f"\n--- per-case ranks (file / chunk, '-' = miss in top {top_k}) ---")
    print(f"{'case_id':<26}" + "".join(f"{e:>18}" for e in engines))
    by_id = {e: {c["id"]: c for c in results_by_engine[e]["per_case"]} for e in engines}
    for case in cases:
        cid = case["id"]
        cols = []
        for e in engines:
            row = by_id[e][cid]
            fr = row["file_rank"] if row["file_rank"] is not None else "-"
            cr = row["chunk_rank"] if row["chunk_rank"] is not None else "-"
            cols.append(f"{fr}/{cr}")
        print(f"{cid:<26}" + "".join(f"{v:>18}" for v in cols))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases", default=str(Path(__file__).resolve().parent / "cases.jsonl"))
    ap.add_argument("--mode", default="hybrid", choices=("hybrid", "semantic", "keyword"))
    ap.add_argument("-k", "--top-k", type=int, default=8)
    ap.add_argument("--engine", choices=("sqlite", "lance", "both"), default="both")
    args = ap.parse_args()

    cases = load_cases(Path(args.cases))
    if not cases:
        print(f"No cases loaded from {args.cases}", file=sys.stderr)
        return 2

    targets = runner.engines() if args.engine == "both" else [args.engine]
    print(f"Loading {len(targets)} engine(s): {', '.join(targets)} (first query per engine cold-starts the model) ...", flush=True)

    results = {}
    for e in targets:
        results[e] = score_engine(e, cases, args.mode, args.top_k)

    render_report(cases, results, args.mode, args.top_k)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
