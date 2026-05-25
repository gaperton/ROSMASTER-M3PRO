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

## What we know

Durable lessons earned through running the experiments below. Each one has a citation back to the experiment log.

- **Engine choice on this corpus is a configuration parity question, not an engine quality question.** Lance under-performed in early tests entirely because of two missing config bits (stop-word-filtered FTS query, larger fusion pool). Once matched to sqlite's config, the engines are functionally equivalent on retrieval quality. *(Experiments 4–6.)*
- **A few "hub" docs over-rank on diffuse queries when keyword anchoring is weak.** Chunks from `1.AI Model Basics/3.Embodied intelligent robot system architecture` and the MoveIt2 intros sit semantically close to many query embeddings; without strong BM25 anchoring they win on cosine and crowd out concrete walkthroughs. The stop-word + pool fix keeps them out of top-3 reliably. Worth knowing so future tuning doesn't accidentally re-introduce the failure mode.
- **Rerankers help when retrieval is ambiguous; they hurt when RRF was already correct.** Verified by inverse: BGE-reranker fixed our 3 chronically-failing diffuse queries (map a room, Jetson vs Pi, install ROS2) and broke 5 previously-clean queries. Net wash. *(Experiments 8–10.)*
- **Labeled and subjective evaluations must be paired.** Hits@k alone misled us into thinking the engines were identical when subjective relevance disagreed; subjective alone is noisy on small samples. Either signal in isolation gives wrong conclusions. *(Experiments 3 vs 4.)*
- **Both engines are defensible primary choices for this corpus.** Decision is operational, not quality: sqlite-rag for install footprint / portability / latency / score transparency; lance-db-rag for growth headroom / polyglot reads / dataset versioning / reranker plumbing.
- **Latency budget is generous.** ~80 ms hybrid is invisible to interactive users. Rerankers triple-to-quintuple it (157–440 ms) without reliable quality payoff here.
- **The embedding pipeline is byte-identical between engines.** Same BGE-small-en-v1.5, same query-instruction prefix, same L2 normalization. Semantic vectors are the same; all hybrid divergence comes from the keyword channel and fusion arithmetic downstream.

## Open questions

Unverified predictions and unknowns. Each one points to the experiment that would resolve it.

- **Q1. Is the corpus the biggest remaining quality lever?** ~33% of noob questions hit corpus gaps. *Test: NX1* (write the missing docs, re-run the 30-question eyeball — does the win rate visibly move?).
- **Q2. Does `bge-large-en-v1.5` (1024-dim) meaningfully beat `bge-small` on this corpus?** Both engines would benefit equally. We don't know the headroom. *Test: NX2.*
- **Q3. Does multi-query expansion (LLM paraphrases the query, fuse results) help imprecise noob queries?** Partial break of the "no services on retrieval path" constraint — needs a decision. *Test: NX3.*
- **Q4. Does finer-grained (per-paragraph) chunking help the cross-encoder discriminate?** Increases chunk count; changes RRF dynamics; might also help BM25 specificity. *Test: NX4.*
- **Q5. Would a domain-fine-tuned cross-encoder reliably beat both off-the-shelf rerankers we tried?** Plausible but expensive — requires labeled (query, relevant-passage) training data we don't have. *Test: TBD; not actionable without labeled training set.*

## Next experiments

Concrete actions, ordered by expected impact. Tool-work items (NX5, NX6, NX7) have no associated open question; they pay back as evaluator coverage or operational quality.

1. **NX1 — Write missing answer docs surfaced by the noob test.** Charging procedure, physical e-stop, simple `cmd_vel` cookbook ("drive N meters"), distributed-ROS for laptop control, "demo index", arm-vibration troubleshooting. Re-run `tests/ask.py` against the updated corpus and count how many previously-tied or previously-missed questions now have a clear top-1. *Resolves Q1.*
2. **NX2 — Try `bge-large-en-v1.5` (1024-dim) embeddings.** Rebuild both indexes (`--rebuild`); rerun `tests/evaluate.py --mode hybrid` and the 30-question eyeball. Compare MRR and subjective wins. ~500 MB model + slower encoding. *Resolves Q2.*
3. **NX3 — Multi-query expansion at query time.** Use Anthropic Haiku to produce 3–5 paraphrases per user query, search each, fuse with RRF on top of the existing pool. Decide whether this partial break of the offline-retrieval constraint is acceptable. *Resolves Q3.*
4. **NX4 — Per-paragraph chunking variant.** Change `chunk_section` to split sections into paragraph-level pieces; rebuild both indexes; re-run labeled + subjective evals. *Resolves Q4.*
5. **NX5 — Metadata + query router.** Tag chunks with module number, doc-type ("walkthrough" / "concept" / "config"), difficulty. A small classifier or rule routes "ROS" questions to modules 15–16, "AI" to 1–4, etc. Both engines support metadata filters cleanly. *Tool work; no hypothesis.*
6. **NX6 — Auto-generate cases for the remaining ~236 docs.** Use Claude Haiku to produce one plausible question per doc, commit to `tests/cases.jsonl`. Gives the labeled eval real statistical power. *Coverage; no hypothesis.*
7. **NX7 — Per-mode side-by-side in `evaluate.py`.** Run hybrid/semantic/keyword in one invocation; widen the report so you see all 3 columns per engine. *Tool work; no hypothesis.*

## Experiment log

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
