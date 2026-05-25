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
- **Add metrics**: MRR and per-case rank diff are already included. Per-mode side-by-side (run all three modes in one invocation and widen the report) is the natural next addition.
- **Add a third engine**: add an entry to `ENGINE_PATHS` in `runner.py`. The engine's `rag_query.py` must expose a `search(query, mode, top_k, ...) -> list[dict]` with `file_path` and `heading_path` keys per result.

## The unlabeled side: `ask.py` + `noob_questions.txt`

The labeled evaluator scores against an expected file. That's a clean metric but misses the failure mode where the right file appears at rank 5 with off-topic noise above it — Hits@8 still gives full credit. To catch *that*, we eyeball results on unlabeled, real-world-style questions.

```powershell
# Side-by-side top-k from both engines, no scoring.
python tests/ask.py "How long does the battery last?"
python tests/ask.py --file tests/noob_questions.txt -k 3
python tests/ask.py "what is a launch file" --mode semantic
```

`noob_questions.txt` holds 30 questions sourced from common ROS Discourse / Reddit / Robotics-SE newcomer patterns. Three batches: capability/setup/troubleshooting → ROS2 first-day pains → safety/specs/programming/config/use-cases. These are *not* used by the labeled evaluator; they're for subjective relevance checks.

## Findings (corpus: 247 docs, 2198 chunks)

The evaluation runs in two complementary modes:

| Tool | Cases | Metric | What it measures |
|---|---|---|---|
| `evaluate.py` | 10 hand-labeled (`cases.jsonl`) | MRR + Hits@1/3/8 (file + chunk) | Whether the *known* answer doc appears, and at what rank |
| `ask.py` | 30 unlabeled (`noob_questions.txt`) | Eyeball — subjective relevance | Whether the top 3 are useful for a newcomer's actual question |

### Headline results (hybrid mode, post-tuning)

| | sqlite-rag | lance-db-rag |
|---|---|---|
| file MRR | 0.950 | 0.950 |
| chunk MRR | 0.531 | 0.529 |
| file-match @1 | 9/10 | 9/10 |
| chunk-match @3 | 7/10 | 7/10 |
| median latency | ~37 ms | ~80 ms |
| Open-question subjective quality (30 noob qs) | baseline | parity (~tied) |

**Engines are functionally equivalent on this corpus** in the modes that matter (hybrid + semantic). Same embedding model (`BAAI/bge-small-en-v1.5`), so semantic vectors are byte-identical; the small lance latency overhead comes from doing two separate `.search()` calls instead of one optimized hybrid path.

### Three findings worth knowing if you build on this

1. **Labeled and subjective evals can disagree.** Early labeled runs said sqlite and lance were identical at every Hits@k. The 30-question subjective eval revealed sqlite winning 13 of 20 questions (zero clear lance wins), because the labeled metric gave full credit for "right file at rank 5 with noise above". The disagreement was *engine-meaningful*: it surfaced that lance was promoting "hub" docs (`Embodied AI architecture`, MoveIt2 intros) above concrete walkthroughs. Lesson: **labeled file-match metrics oversell parity; always pair with subjective spot-checks**.

2. **The lance gap closed entirely with configuration parity, not better algorithms.** The original sqlite advantage on diffuse queries came from two things lance wasn't doing: (a) pre-tokenizing the FTS query with stop-word filter + OR-join, (b) using a larger candidate pool (`max(top_k*4, 30)`) per channel before RRF. Both are now applied in lance's `run_search`. After the fix, lance matches sqlite on every previously-failing query (map a room, Jetson vs Pi, install ROS2). **Net lesson: most "engine X is better than engine Y" comparisons are actually configuration comparisons.**

3. **Cross-encoder reranking didn't reliably help this corpus.** We tried `ms-marco-MiniLM-L-6-v2` (regression on noob queries — over-fits to keyword-density in markdown chunks) and `BAAI/bge-reranker-base` (mixed — fixes the diffuse queries but introduces new failures on already-clean queries where RRF was correctly anchoring the right doc). Latency went from 81 ms → 440 ms. Default is now `--no-rerank`; the reranker stays as an opt-in flag. Hypothesis: rerankers help when retrieval is ambiguous; on clean queries where RRF already nailed the answer doc, re-scoring just adds noise.

### What we didn't try that might still help

- **Multi-query expansion** (LLM-generated paraphrases of the user query, search each, fuse). Works for both engines; needs an LLM API.
- **Bigger embedding model** (`bge-large-en-v1.5`, 1024-dim). Both engines benefit equally; ~500 MB model; requires `--rebuild`.
- **Chunking changes** — finer-grained (per-paragraph) chunks might help the reranker discriminate; bigger chunks might give the cross-encoder more context. Both are pre-embed changes that affect both engines.
- **Closing corpus gaps.** ~10 of 30 noob questions surfaced topics the docs don't actually cover (charging procedure, physical e-stop, "drive N meters", distributed-ROS for laptop control, "demo index"). No engine can find what isn't there.

## File layout

```
tests/
├── README.md            # this file
├── cases.jsonl          # labeled query → expected_file/heading test cases
├── noob_questions.txt   # 30 unlabeled questions for subjective eyeballing
├── runner.py            # importlib loader; calls each engine's search()
├── evaluate.py          # labeled scoring + report (MRR, Hits@k, per-case diff)
└── ask.py               # ad-hoc side-by-side query tool (unlabeled, no scoring)
```
