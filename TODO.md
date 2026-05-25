# Plan

## Goals

- Local RAG over the repo's markdown course material so a beginner can ask natural-language questions and get back the most relevant chunks with file paths and heading breadcrumbs.
- Side-by-side comparison of two embedded vector-store engines (sqlite-vec, LanceDB) on this specific corpus, with a repeatable scoring harness.
- Honest, documented verdict on which engine to use and why — not a benchmark for benchmark's sake.
- Establish an evaluation methodology that can survive engine swaps, model upgrades, and corpus growth.

## Constraints

- **No services** — embedded engines only, single-file or single-directory storage.
- **Local-only retrieval path** — no network calls after the first model download. Anthropic / OpenAI keys are fine for offline case generation, not for live retrieval.
- **Windows / Python 3.12 / CPU.** No GPU assumed; model loads must fit in seconds, not minutes.
- **Corpus is fixed input.** 247 markdown files, Marker-converted from PDFs. We don't rewrite the docs; we work with the noise (markdown markup, mixed code blocks, translated-from-Chinese English).
- **Reproducibility.** Every claim in the READMEs should be backed by a script someone can re-run.

## Known problems

1. **Labeled file-match metrics oversell engine parity.** Hits@8 gives full credit when the right doc appears at rank 5 with off-topic noise above it. Real-world retrieval failures hide behind a 10/10 hits@8.
2. **"Hub" docs over-rank on diffuse queries.** Chunks from `1.AI Model Basics/3.Embodied intelligent robot system architecture` and a few MoveIt2 intros sit semantically close to many query embeddings; without strong BM25 anchoring they win on cosine and crowd out concrete walkthroughs.
3. **Cross-encoder rerankers introduce as many failures as they fix on this corpus.** ms-marco-MiniLM-L-6-v2 over-fits to surface keyword density in markdown chunks; BGE-reranker-base helps on ambiguous queries but adds noise on queries where RRF was already correct.
4. **`expected_heading_substring` in labeled cases is fragile.** Sibling `##` headings collapse to siblings (not parent-child) in the chunker, so a chunk body's `heading_path` may be just `"1. Content Description"` instead of `"Inverse kinematics design > 1. Content Description"`.
5. **LanceDB's hidden retry loop on embedding errors** costs ~25 min of exponential backoff before failing. Cost us debugging time during the StringScalar coercion bug.
6. **Corpus gaps surfaced by the 30 noob questions.** ~10 of 30 questions have no canonical answer doc in the corpus (charging procedure, physical e-stop, "drive N meters", distributed-ROS for laptop control, "demo index", arm-vibration troubleshooting, "where do I add a new behavior"). Some docs *exist* but have generic titles that neither engine surfaces (`16.ROS2 common command tools` not found for "check topics"; `Static IP and hotspot mode` not found for "change IP").
7. **Configuration-parity bugs masquerade as engine-quality differences.** Lance's original under-performance was entirely (a) raw natural-language string passed to Tantivy without stop-word filter / OR-join, and (b) smaller candidate pool before RRF.

## Hypotheses

1. **Engine choice is a configuration parity question, not an engine quality question.** ✅ *Verified.* Lance closed the entire subjective-quality gap once `to_lance_fts_query` + larger pool were applied. The engines are functionally equivalent on this corpus.
2. **Rerankers help when retrieval is ambiguous; they hurt when RRF was already correct.** ✅ *Verified by inverse.* BGE-reranker fixed Q4 (map a room), Q6 (Jetson vs Pi), Q9 (install ROS2) — all queries where multiple docs sit semantically close. It *broke* Q7, Q21, Q25, Q28, Q30 — all queries where RRF already had the right top-1.
3. **Labeled and subjective evals should always be paired; either alone misleads.** ✅ *Verified.* Labeled said engines were identical → subjective showed sqlite winning 13 of 20. After the config fix labeled still says identical → subjective also says identical. Both signals were needed to detect both states.
4. **The biggest remaining quality lever is the corpus, not the engine or the reranker.** 🟡 *Plausible, untested.* ~33% of noob questions hit corpus gaps. A few targeted new docs (charging, e-stop, distributed-ROS, simple `cmd_vel` recipes) would unblock more user questions than any retrieval tweak.
5. **Bigger embedding model (`bge-large-en-v1.5`, 1024-dim) would help both engines equally.** 🟡 *Plausible, untested.* Quality cap of bge-small on this corpus isn't known. Would also require a rebuild and ~500 MB model.
6. **Multi-query expansion (LLM paraphrases the query, fuse results) would help noob queries with imprecise wording.** 🟡 *Plausible, untested.* Both engines benefit equally; needs LLM API on query path → breaks the "no services" constraint partially.
7. **A domain-fine-tuned cross-encoder (trained on ROS doc Q→passage pairs) would beat both off-the-shelf rerankers we tried.** 🟡 *Plausible, untested.* Would require labeled training data we don't have.
8. **Finer-grained chunking (per-paragraph instead of per-section) would help the cross-encoder discriminate.** 🟡 *Plausible, untested.* Increases chunk count, changes RRF dynamics.

## Experiment results and conclusions

| # | Experiment | Result | Verdict |
|---|---|---|---|
| 1 | Build sqlite-vec + FTS5 hybrid RAG | 247 files → 2198 chunks, 8 MB `.db`, ~37 ms median query | ✅ baseline |
| 2 | Build LanceDB + Tantivy hybrid RAG | Same corpus → 12 MB directory, ~57 ms median; required workarounds for `BGE.create()`, `StringScalar` coercion, no-pandas, hidden retry loop | ✅ working |
| 3 | Labeled eval, 10 hand-curated cases × 3 modes × 2 engines | Identical Hits@k on every cell except keyword mode where Lance edges sqlite by 1–2 ranks | Engines indistinguishable on labeled |
| 4 | Subjective eyeball, 30 noob questions × 2 engines, *before* config fix | sqlite 13 clear or slight wins, lance 2 slight, 5 tied; dramatic Lance failures on Q4 (map a room), Q6 (Jetson vs Pi), Q9 (install ROS2) | Subjective disagreed with labeled |
| 5 | Diagnose Lance gap: dump pool composition for failing queries | Tantivy was tokenizing raw "How do I X" including stop words; pool ≈ `top_k`, smaller than sqlite's `max(top_k*4, 30)` | Root cause: config parity, not engine quality |
| 6 | Apply cheap fixes: `to_lance_fts_query` (stop-word filter + OR-join) + manual orchestration with larger pool + Python-side RRF | All 3 failing queries fixed; full 30-question subjective eval shows engines at parity | ✅ Lance ≈ sqlite |
| 7 | Add MRR to labeled evaluator | Re-confirmed engines identical on file MRR (0.950 / 0.950); chunk MRR 0.531 / 0.529 | Labeled metric refined, conclusion unchanged |
| 8 | Try `cross-encoder/ms-marco-MiniLM-L-6-v2` reranker, input `(query, text)` | Labeled chunk MRR 0.529 → 0.558 (+5%); open-noob queries regressed (Q4 picks theory over walkthrough, Q6 demotes right doc, Q9 drops install doc); latency 81 → 157 ms | ❌ labeled-only win, real-world loss |
| 9 | Same model, input `(query, heading_path + text)` | Labeled unchanged (0.558); open-noob regressions different but similar in magnitude (Q6 picked Arm Calibration's "Jetson, Raspberry Pi" subsection — lexical match made it worse) | ❌ heading didn't fix the underlying mismatch |
| 10 | Try `BAAI/bge-reranker-base`, input `(query, heading + text)` | Labeled chunk MRR 0.533 (≈ no rerank); fixes Q4 (slam_toolbox into top-3), Q6 (right doc at #1), Q9 (`ROS2 install Humble` at #1, beats sqlite); breaks Q7 (drive 1m → Color block transport), Q21 (e-stop → multimodal visual), Q25 (depth camera → Line patrol), Q28 (examples → STM32 burning), Q30 (API key → Wake-up response); latency 440 ms | 🟡 net wash, real wins traded for real losses |
| 11 | Set default to `--no-rerank`, keep `--rerank` as opt-in | Defaults reproduce experiment #7 numbers | ✅ shipped |
| 12 | Document findings across `tests/README.md`, `lance-db-rag/README.md`, `sqlite-rag/README.md` | All three READMEs aligned: engines equivalent; choice is operational | ✅ shipped |

### Bottom-line conclusions

- **Both engines are defensible primaries** for this corpus. Pick on operational fit, not retrieval quality.
- **Most engine comparisons are configuration comparisons.** We almost shipped "sqlite is better than Lance" until we realized we'd given Lance an inferior config.
- **Latency budget is generous** (~200 ms is invisible to interactive users), but rerankers triple-to-quintuple it without reliable quality gains here.
- **Open queries are a sharper test than labeled cases.** The labeled eval is necessary regression coverage but should not be the sole verdict.

### Outstanding follow-ups (not yet attempted, ordered by expected impact)

1. Add metadata to chunks (module number, doc-type, difficulty) + a tiny rule-based query router. Lets "ROS" questions skip non-ROS modules.
2. Write the missing answer docs surfaced by the noob test (charging, e-stop, distributed-ROS, `cmd_vel` cookbook, "demo index").
3. Auto-generate cases for the remaining ~236 docs via LLM so the labeled eval has statistical power.
4. Per-mode side-by-side in `evaluate.py` (run hybrid/semantic/keyword in one invocation, widen the report).
5. Try `bge-large-en-v1.5` (1024-dim) embeddings; rebuild both indexes; re-run.
6. Multi-query expansion (LLM paraphrases at query time). Requires deciding whether to relax "no services on retrieval path" for the optional case.
