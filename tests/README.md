# tests — RAG retrieval quality harness

Apples-to-apples comparison of the two RAG implementations ([`../sqlite-rag/`](../sqlite-rag/) and [`../lance-db-rag/`](../lance-db-rag/)) on a labeled set of natural-language queries. Loads both engines in-process via `importlib`, runs every case through every engine, scores Hits@k against expected-file and expected-chunk targets, and prints a side-by-side table.

## How to use

```powershell
# Default: hybrid mode, top_k=8, both engines, all cases in cases.jsonl
python tests/evaluate.py

# Single mode / single engine / different k
python tests/evaluate.py --mode keyword
python tests/evaluate.py --engine sqlite -k 5
python tests/evaluate.py --cases tests/my_cases.jsonl
```

Both engine indexes must already be built (`python sqlite-rag/rag_index.py`, `python lance-db-rag/rag_index.py`). The first query against each engine cold-starts the embedding model; subsequent queries reuse it via a module-level cache, so a 10-case run finishes in a few seconds.

## Case format

[cases.jsonl](cases.jsonl) is line-delimited JSON, one object per case:

```json
{
  "id": "arm-median-calibration",
  "query": "How do I calibrate the median of the robotic arm servos?",
  "expected_file": "0.Configuration and Operation Guide/3. Robotic Arm Calibration/3. Robotic Arm Calibration.md",
  "expected_heading_substring": "Calibrate the median"
}
```

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Stable kebab-case identifier; used as the row label in the per-case diff. |
| `query` | yes | Natural-language question, exactly as a user would type it. |
| `expected_file` | yes | Path under `markdown/` (POSIX slashes). Substring match — any result whose `file_path` contains this string counts as a file-match. |
| `expected_heading_substring` | optional | Case-insensitive substring that must appear in a matching chunk's `heading_path` for it to count as a chunk-match. Omit to skip chunk-match scoring. |

Comments (`#`) and blank lines in the file are skipped.

## Scoring rules

For each case the harness asks each engine for the top `top_k` results, then computes:

- **`file_rank`** — 1-indexed rank of the *first* result whose `file_path` contains `expected_file`. `None` if missed.
- **`chunk_rank`** — 1-indexed rank of the *first* result that is both a file-match **and** whose `heading_path` contains `expected_heading_substring`. `None` if missed.

From those per-case ranks the report aggregates:

- **Hits@k (file-match)** — did the right *document* appear in the top k?
- **Hits@k (chunk-match)** — did the right *section* (file + heading) appear in the top k?
- **Median latency** — wall-clock per query (model load excluded; only counts the second-query-onwards timing).

The per-case diff at the bottom prints `file_rank / chunk_rank` per engine so you can see precisely which queries flipped between engines and where the chunk match went off.

## Reading the report

Sample output for 10 cases × hybrid mode × top_k=8:

```
metric                  sqlite    lance
file-match @1            9/10     9/10
chunk-match @1           4/10     4/10
file-match @3           10/10    10/10
chunk-match @3           7/10     7/10
file-match @8           10/10    10/10
chunk-match @8           8/10     8/10
median latency (ms)      36.1     56.6

case_id                       sqlite             lance
arm-median-calibration           1/1               1/1
rag-hallucination                1/1               1/1
ros2-publisher                   2/3               2/2
ssh-putty                        1/7               1/5
moveit2-ik-rviz                  1/-               1/-
...
```

How to interpret:

- **File-match @k climbing fast** (9/10 → 10/10 between k=1 and k=3) means the *right document* is almost always in the top 3, but sometimes pushed off rank 1 by a similar doc. That's a ranking-quality signal.
- **Chunk-match consistently below file-match** means the right document is found but the answer-bearing *section* often isn't the top chunk inside it. That's expected: a 5-section file produces 5+ chunks and the highest-ranking one is usually the title/intro chunk, not the deep how-to chunk.
- **Per-case `1/-`** is the diagnostic case: right document found at rank 1, but no chunk inside matched the expected heading substring. Could mean the heading was named differently than you expected, or the chunker put the body in a chunk whose `heading_path` doesn't contain your substring (see Gotchas below).
- **Engines disagreeing by 1–2 ranks** is noise on a 10-case set — small absolute differences aren't statistically meaningful until you have 50+ cases.

## Gotchas

- **`expected_heading_substring` is fragile.** The chunker treats sibling `##` headings as siblings, *not* as parent-child. So a doc that starts with `## Inverse kinematics design` followed by `## 1. Content Description` produces chunks whose `heading_path` is just `1. Content Description` for the body content — not `Inverse kinematics design > 1. Content Description`. If you author cases by inspecting the source `.md` file, look at how `split_by_headings` in `rag_index.py` would actually produce the `heading_path`, or pick a substring that appears in the leaf-level heading.
- **`expected_file` is a substring match, not exact.** Be specific enough to disambiguate (the full course-folder path is usually enough). Two unrelated docs sharing a filename would both match a too-short string.
- **Cold-start latency is excluded from the median.** The first query per engine includes the ~1–2 s `SentenceTransformer` load. The harness times every query and reports the median, so the cold start barely shifts the number — but if you only had 1 case it would dominate. The eval is meant for ≥5 cases.
- **The case set authoring step is the bottleneck.** With 10 hand-curated cases you get clean signal but limited statistical power. ~30 cases is the floor for engine comparisons being meaningful; 246 (one per doc) covers the corpus but takes an LLM to write at scale. There is no `generate_cases.py` yet — see Extending below.

## Extending

- **Add cases**: append to `cases.jsonl` by hand. Useful when a real question fails in production and you want regression coverage.
- **Auto-generate cases**: write a `generate_cases.py` that walks `markdown/` and asks an LLM (Anthropic / OpenAI / local Ollama) for one plausible question per doc. Commit the output once — these are stable test data, not regenerated each run.
- **Add metrics**: MRR (`1 / file_rank` averaged) is a 3-line addition to `score_engine`. Per-mode (`hybrid`/`semantic`/`keyword`) side-by-side requires looping over modes and widening the report; the `score_engine` function is mode-agnostic so this is purely a presentation change.
- **Add a third engine**: add an entry to `ENGINE_PATHS` in `runner.py`. The engine's `rag_query.py` must expose a `search(query, mode, top_k, ...) -> list[dict]` with `file_path` and `heading_path` keys per result.

## File layout

```
tests/
├── README.md      # this file
├── cases.jsonl    # labeled query → expected_file/heading test cases
├── runner.py      # importlib loader; calls each engine's search()
└── evaluate.py    # scoring + report
```
