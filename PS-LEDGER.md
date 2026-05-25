# Problem-Solving Ledger

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

- **Engine choice on this corpus is a configuration parity question, not an engine quality question.** Lance under-performed in early tests entirely because of two missing config bits (stop-word-filtered FTS query, larger fusion pool). Once matched to sqlite's config, the engines are functionally equivalent on retrieval quality. *(Experiments 2–4.)*
- **A few "hub" docs over-rank on diffuse queries when keyword anchoring is weak.** Chunks from `1.AI Model Basics/3.Embodied intelligent robot system architecture` and the MoveIt2 intros sit semantically close to many query embeddings; without strong BM25 anchoring they win on cosine and crowd out concrete walkthroughs. The stop-word + pool fix keeps them out of top-3 reliably. Worth knowing so future tuning doesn't accidentally re-introduce the failure mode.
- **Rerankers help when retrieval is ambiguous; they hurt when RRF was already correct.** Verified by inverse: BGE-reranker fixed our 3 chronically-failing diffuse queries (map a room, Jetson vs Pi, install ROS2) and broke 5 previously-clean queries. Net wash. *(Experiments 6–8.)*
- **Labeled and subjective evaluations must be paired.** Hits@k alone misled us into thinking the engines were identical when subjective relevance disagreed; subjective alone is noisy on small samples. Either signal in isolation gives wrong conclusions. *(Experiments 1 vs 2.)*
- **Both engines are defensible primary choices for this corpus.** Decision is operational, not quality: sqlite-rag for install footprint / portability / latency / score transparency; lance-db-rag for growth headroom / polyglot reads / dataset versioning / reranker plumbing.
- **Latency budget is generous.** ~80 ms hybrid is invisible to interactive users. Rerankers triple-to-quintuple it (157–440 ms) without reliable quality payoff here.
- **The embedding pipeline is byte-identical between engines.** Same BGE-small-en-v1.5, same query-instruction prefix, same L2 normalization. Semantic vectors are the same; all hybrid divergence comes from the keyword channel and fusion arithmetic downstream.
- **The comparison ran on five dimensions.** Retrieval quality (labeled MRR + Hits@k + subjective relevance on noob questions), latency (median ms after model warmup), install footprint (deps + binary size), portability (single file vs directory tree), and score transparency (per-channel scores visible in output). The engines tie on retrieval quality after the parity fix; the other four are where the operational tradeoff lives.
- **The evaluation methodology survives changes (Goal 4).** Two case sets (`tests/cases.jsonl` labeled, `tests/noob_questions.txt` unlabeled), two harness tools (`evaluate.py` for MRR + Hits@k, `ask.py` for subjective eyeball), one `importlib`-based runner exposing both engines through a uniform `search()` API. Survived two engine implementations and three reranker variants without harness changes.

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

## Considered and deferred

Options we evaluated and decided against, with reasoning so future-us doesn't re-derive the same conclusion.

- **ChromaDB as a third engine.** Embedded mode (PersistentClient) uses SQLite + binary HNSW files in a directory; collection API; HNSW out of the box. Decided against because (a) no built-in BM25 / proper full-text search — `where_document={"$contains": ...}` is substring filter, not a ranker, so hybrid would mean bolting on `rank_bm25` and writing our own fusion (essentially porting sqlite-rag with Chroma underneath), and (b) it sits in an awkward middle: heavier deps than sqlite-vec, fewer advanced features than LanceDB. The right pick only if pure semantic + HNSW were the goal.
- **LanceDB's built-in `RRFReranker` and `query_type="hybrid"` path.** We started here; ended up bypassing it for manual orchestration to apply configuration parity with sqlite (stop-word-filtered FTS query, explicit candidate pool). Built-in path is still available — see git history for the original implementation — but we'd rebuild the bypass if we re-introduced it, so there's no advantage.

## Experiment log

Only entries that asked a question and produced new knowledge. Construction milestones (building each engine) and shipping decisions (set default, write docs) live in the READMEs and `git log`, not here. `NQ#` references below point to specific questions in `tests/noob_questions.txt`; they are unrelated to the `Q#` open questions above.

| # | Question being tested | Method | Result / new knowledge |
|---|---|---|---|
| 1 | Do the two engines retrieve the same chunks on the labeled cases? | 10 hand-curated cases × 3 modes × 2 engines via `tests/evaluate.py` | Identical Hits@k on every cell except keyword mode where Lance edges sqlite by 1–2 ranks. Conclusion at the time: engines indistinguishable. |
| 2 | Does the labeled verdict hold on open-ended user-style queries? | 30 noob questions × 2 engines via `tests/ask.py` | **No.** sqlite 13 clear/slight wins, lance 2 slight, 5 tied. Lance had dramatic failures on NQ4 (map a room), NQ6 (Jetson vs Pi), NQ9 (install ROS2). Labeled and subjective evals can disagree. |
| 3 | What in Lance's hybrid path is causing the failures? | Dumped the candidate pool composition for each failing query | Tantivy was tokenizing the raw "How do I X" including stop words; Lance's hybrid pool was ≈ `top_k`, much smaller than sqlite's `max(top_k*4, 30)`. Root cause: configuration parity, not engine quality. |
| 4 | Will configuration parity close the gap? | Applied `to_lance_fts_query` (stop-word filter + OR-join) + manual orchestration with larger pool + Python-side RRF, then re-ran experiments 1 and 2 | **Yes.** All 3 failing queries fixed; 30-question subjective eval shows engines at parity. Labeled metrics unchanged (already at ceiling). |
| 5 | Does MRR change the labeled verdict that the engines are identical? | Added MRR to `evaluate.py`, re-ran | No. File MRR 0.950 / 0.950, chunk MRR 0.531 / 0.529. Metric is sharper than Hits@8 but the answer is the same on this case set. |
| 6 | Does a cross-encoder reranker beat plain RRF on hybrid retrieval? | Added `--rerank` with `cross-encoder/ms-marco-MiniLM-L-6-v2`, input `(query, text)`, top-20 candidates re-scored | Labeled chunk MRR 0.529 → 0.558 (+5%). Open-noob queries regressed: NQ4 picks theory over walkthrough, NQ6 demotes right doc, NQ9 drops install doc. Latency 81 → 157 ms. Labeled-only win, real-world loss. |
| 7 | Does feeding heading_path + text fix the ms-marco regression? | Same model, input changed to `(query, heading_path + " — " + text)` | No. Labeled unchanged (0.558). Open-noob regressions are different but similar in magnitude (NQ6 now lexically matches an "Arm Calibration → Jetson Nano, Raspberry Pi" subsection — heading made it worse here). |
| 8 | Does a passage-trained reranker (BGE-reranker, matched to our embedding model) behave differently? | Swapped to `BAAI/bge-reranker-base`, same `(query, heading + text)` input | Labeled chunk MRR 0.533 (≈ plain RRF). Fixes NQ4 (slam_toolbox into top-3), NQ6 (right doc at #1), NQ9 (`ROS2 install Humble` at #1, beats sqlite). Breaks NQ7 (drive 1m → Color block transport), NQ21 (e-stop → multimodal visual), NQ25 (depth camera → Line patrol), NQ28 (examples → STM32 burning), NQ30 (API key → Wake-up response). Latency 440 ms. Net wash — real wins traded for real losses. Rerankers help when retrieval is ambiguous and hurt when it's already correct. |
