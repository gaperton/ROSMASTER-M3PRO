# Problem-Solving Ledger

## Goals

> 2–5 bullets describing what success looks like. Each should be testable as done / not done.

- Build local RAG over the repo's Markdown course material so a beginner can ask natural-language questions and receive relevant chunks with file paths and heading breadcrumbs.
- Compare two embedded vector-store engines, sqlite-vec and LanceDB, on this corpus using a repeatable scoring harness.
- Produce an honest verdict on which engine to use and why, without turning this into a generic benchmark.
- Establish an evaluation method that survives engine swaps, model upgrades, and corpus growth.

## Constraints

> Non-negotiable limits on the solution space.

- **No services** — embedded engines only; storage must be single-file or single-directory.
- **Local retrieval path** — no network calls after the first model download. Anthropic / OpenAI keys are acceptable for offline case generation, not for live retrieval.
- **Windows / Python 3.12 / CPU** — no GPU assumed; model startup must take seconds, not minutes.
- **Fixed corpus** — 247 Markdown files, Marker-converted from PDFs. We do not rewrite the source docs; we handle their noise: Markdown artifacts, mixed code blocks, and translated-from-Chinese English.
- **Reproducibility** — every README claim should be backed by a script someone can rerun.

## Established Findings

> Empirical findings, causal diagnoses, and methodological lessons supported by the experiment log. Each claim should state or imply its scope.

- **On this corpus, engine quality was not the cause of the early sqlite-vec / LanceDB gap.** LanceDB underperformed because two configuration details were not matched: stop-word-filtered FTS query generation and a larger fusion pool. Once those were matched, sqlite-vec and LanceDB were functionally equivalent on observed retrieval quality. *(Experiments 2–4.)*

- **Weak keyword anchoring lets broad “hub” docs over-rank on diffuse queries.** Chunks from `1.AI Model Basics/3.Embodied intelligent robot system architecture` and the MoveIt2 intros sit semantically close to many query embeddings. Without strong BM25 anchoring, they win on cosine similarity and crowd out concrete walkthroughs. The stop-word + pool fix keeps them out of top-3 reliably.

- **Off-the-shelf rerankers are a net wash on this corpus.** BGE-reranker fixed three chronically failing diffuse queries — map a room, Jetson vs Pi, install ROS2 — but broke five previously clean queries. Rerankers help when retrieval is genuinely ambiguous and hurt when RRF is already correct. *(Experiments 6–8.)*

- **Labeled and subjective evaluations must be paired.** Hits@k alone initially suggested the engines were equivalent. Open-ended noob questions exposed failures the labeled set missed. Subjective review alone is also noisy on a small sample. Either signal by itself is insufficient. *(Experiments 1–2.)*

- **Engine choice is now operational, not quality-based.** After the parity fix, the engines tie on observed retrieval quality. sqlite-rag is stronger on install footprint, portability, latency, and score transparency. lance-db-rag is stronger on growth headroom, polyglot reads, dataset versioning, and reranker plumbing.

- **Latency is not currently the limiting factor.** Hybrid retrieval at ~80 ms is acceptable for interactive use. Rerankers increase latency to 157–440 ms without reliable quality gain on this corpus.

- **The embedding pipeline is identical across engines.** Both use BGE-small-en-v1.5, the same query-instruction prefix, and L2 normalization. Semantic vectors are the same; hybrid differences come from the keyword channel and fusion logic.

- **The comparison used five dimensions.** Retrieval quality, latency, install footprint, portability, and score transparency. Retrieval quality ties after parity; the other four dimensions determine the operational tradeoff.

- **The evaluation harness has survived implementation changes.** Two case sets, `tests/cases.jsonl` and `tests/noob_questions.txt`, plus two tools, `evaluate.py` and `ask.py`, worked across two engine implementations and three reranker variants.

- **`bge-large-en-v1.5` is a mild net-positive that does not justify its cost.** The 1024-dim model improved a handful of diffuse noob queries where bge-small's vectors blurred a clearly-correct doc (lidar specs, IP-change, "Controlling the Car's Speed", install-ROS2) but regressed labeled chunk MRR from 0.531/0.529 to 0.483/0.483 — same right file, different chunk inside it — and demoted at least one exact-match chunk (Configuring API-Key). Lance latency rose ~70% (80 → 137 ms); sqlite was flat. The 2.7× weight footprint (~130 MB → ~1.3 GB) and slower re-embed are not paid back by ~3 clear noob wins minus 1 labeled regression. *(Experiment 9.)*

## Working Hypotheses

> Plausible explanations or predictions not yet established by experiment.

- **H1. Cross-encoder rerankers help only when first-stage retrieval is genuinely ambiguous.** Most queries against a well-tuned hybrid retriever are not ambiguous enough to justify reranking. RRF over stop-word-filtered FTS plus a wide vector pool already handles them, so a reranker often adds noise.  
  *Falsified by:* finding a reranker that improves both clean and ambiguous queries on this corpus.

- **H2. Retrieval benchmarks often compare defaults more than engines.** In this project, the apparent LanceDB quality gap disappeared after configuration parity. The broader hypothesis is that many “engine X beats engine Y” comparisons are actually default-configuration comparisons.  
  *Falsified by:* finding two hybrid retrieval engines that still differ meaningfully after careful configuration parity on a fair task.

- **H3. For small-to-medium corpora, linear scan over normalized vectors is a reasonable default.** sqlite-vec brute-force search runs at ~37 ms median on 2,198 chunks. At this scale, HNSW may add setup cost, recall risk, and tuning complexity for little practical gain. This is not yet directly tested here.  
  *Falsified by:* HNSW producing substantially lower latency at this scale without quality loss.

- **H4. Corpus coverage is probably the next major quality lever.** About one third of noob questions hit gaps where the corpus does not contain a good answer. Retrieval tuning cannot recover answers that are not present. Supporting evidence: Experiment 9 showed that doubling embedding capacity yields only a handful of noob wins, several of which (e.g. NQ22 lidar specs) succeeded because the right doc *was* in the corpus and bge-large simply surfaced it.  
  *Test:* NX1. If adding missing docs improves win rate more than the ~3-clear-wins baseline NX2 produced, this hypothesis is supported.

## Decisions Made

> Consequential choices to preserve or reconsider deliberately.

- **Default to `--no-rerank` for lance-db-rag.**  
  *Why:* EF §3, Experiments 6–8, and H1. Reranking remains available through the opt-in `--rerank` flag.  
  *Revisit if:* a domain-fine-tuned reranker becomes available, or Q5 produces usable labeled training data.

- **Keep both engines side by side for now.**  
  *Why:* after parity, retrieval quality is equivalent and the remaining choice is operational. Keeping both preserves the comparison harness and avoids premature lock-in.  
  *Revisit if:* maintaining two engines becomes more expensive than the side-by-side comparison is worth, or one engine pulls ahead on retrieval quality.

- **Bypass LanceDB's built-in `query_type="hybrid"` + `RRFReranker` path.**  
  *Why:* parity with sqlite required manual orchestration: stop-word-filtered Tantivy query, explicit `max(top_k * 4, 30)` pool per channel, and Python-side RRF. The built-in path remains in git history, but re-adopting it would recreate the same bypass.  
  *Revisit if:* LanceDB exposes enough controls to match the manual path directly.

- **Reject ChromaDB as a third engine for now.**  
  *Why:* embedded ChromaDB has HNSW, but no built-in BM25 / proper FTS ranking. `where_document={"$contains": ...}` is a substring filter, not a ranker. Hybrid retrieval would require bolting on `rank_bm25` and custom fusion, effectively recreating sqlite-rag under a heavier dependency stack.  
  *Revisit if:* the project shifts to pure semantic + HNSW retrieval, or ChromaDB gains a strong built-in hybrid path.

- **Accept duplicated chunking code for now.**  
  *Why:* `sqlite-rag/rag_index.py` and `lance-db-rag/rag_index.py` both carry `split_by_headings` / `chunk_section`. A shared-module refactor can wait until one engine becomes primary.  
  *Revisit if:* a third engine is added, or chunking behavior starts diverging unintentionally.

- **Keep `BAAI/bge-small-en-v1.5` as the default embedding model.**  
  *Why:* it is lightweight, English-focused, adequate for the current corpus, and shared across both engines, which removes one comparison variable. Experiment 9 ran NX2 and found `bge-large-en-v1.5` is only a mild net-positive on diffuse noob queries while costing ~70% Lance latency, a labeled chunk-MRR regression, and a 1.3 GB weight footprint.  
  *Revisit if:* the corpus becomes multilingual, gains a substantial body of long technical chunks where 1024-dim discrimination would matter more than it currently does, or a new embedding family meaningfully improves on bge-small at comparable cost.

## Open Questions

> Important things we know we do not know. Each should point to an experiment that can resolve it.

- **Q1. Is corpus coverage the biggest remaining quality lever?**  
  About one third of noob questions hit corpus gaps.  
  *Test:* NX1.

- **Q3. Does multi-query expansion help imprecise beginner questions?**  
  This may improve recall, but it partially breaks the no-services-on-retrieval-path constraint.  
  *Test:* NX3.

- **Q4. Does paragraph-level chunking improve retrieval specificity?**  
  It may help BM25 and cross-encoder discrimination, but it also increases chunk count and changes RRF dynamics.  
  *Test:* NX4.

- **Q5. Would a domain-fine-tuned cross-encoder reliably beat the off-the-shelf rerankers?**  
  Plausible but expensive. Requires labeled query / relevant-passage training data we do not currently have.  
  *Test:* TBD; not actionable until a labeled training set exists.

## Next Experiments

> Planned actions expected to resolve open questions, refine hypotheses, or improve the toolchain. Ordered by expected impact.

1. **NX1 — Write missing beginner-answer docs.**  
   Add docs for charging, physical e-stop, simple `cmd_vel` usage, distributed ROS for laptop control, demo index, and arm-vibration troubleshooting. Rebuild indexes and rerun `tests/ask.py`.  
   *Resolves:* Q1.

2. **NX3 — Add multi-query expansion.**  
   Use Anthropic Haiku to produce 3–5 paraphrases per user query, search each, and fuse results with RRF. Decide whether the partial break of the offline-retrieval constraint is acceptable.  
   *Resolves:* Q3.

3. **NX4 — Test paragraph-level chunking.**  
   Change `chunk_section` to split sections into paragraph-level pieces. Rebuild both indexes and rerun labeled + subjective evaluations.  
   *Resolves:* Q4.

4. **NX5 — Add metadata and query routing.**  
   Tag chunks by module number, doc type, and difficulty. Route questions to likely module ranges: ROS to modules 15–16, AI to 1–4, and so on.  
   *Tool work.*

5. **NX6 — Generate labeled cases for the remaining docs.**  
   Use Claude Haiku to produce one plausible question per remaining doc and commit them to `tests/cases.jsonl`.  
   *Coverage work.*

6. **NX7 — Add per-mode side-by-side reporting.**  
   Update `evaluate.py` so one invocation reports hybrid, semantic, and keyword results for both engines.  
   *Tool work.*

## Experiment Log

> Chronological record of experiments that produced new knowledge.

Excludes construction milestones and shipping decisions; those belong in the READMEs and `git log`. `NQ#` references below point to questions in `tests/noob_questions.txt`; they are unrelated to the `Q#` open questions above.

| # | Question tested | Method | Result / new knowledge |
|---|---|---|---|
| 1 | Do the two engines retrieve the same chunks on labeled cases? | 10 hand-curated cases × 3 modes × 2 engines via `tests/evaluate.py` | Identical Hits@k except keyword mode, where Lance edged sqlite by 1–2 ranks. Initial conclusion: engines were indistinguishable. |
| 2 | Does the labeled verdict hold on open-ended user-style queries? | 30 noob questions × 2 engines via `tests/ask.py` | No. sqlite had 13 clear/slight wins, Lance had 2 slight wins, and 5 were tied. Lance failed badly on NQ4, NQ6, and NQ9. Labeled and subjective evaluations can disagree. |
| 3 | What caused LanceDB's hybrid failures? | Dumped candidate-pool composition for each failing query | Tantivy tokenized raw “How do I X” queries including stop words, and Lance's hybrid pool was about `top_k`, much smaller than sqlite's `max(top_k * 4, 30)`. Root cause: configuration mismatch. |
| 4 | Does configuration parity close the gap? | Applied `to_lance_fts_query`, stop-word filtering, OR-join, larger pool, and Python-side RRF; reran Experiments 1 and 2 | Yes. All three failing queries were fixed. The 30-question subjective eval showed parity. Labeled metrics stayed unchanged because they were already near ceiling. |
| 5 | Does MRR change the labeled verdict? | Added MRR to `evaluate.py` and reran | No. File MRR was 0.950 / 0.950; chunk MRR was 0.531 / 0.529. MRR is sharper than Hits@8, but the answer stayed the same. |
| 6 | Does a cross-encoder reranker beat plain RRF? | Added `cross-encoder/ms-marco-MiniLM-L-6-v2`, scoring top-20 `(query, text)` pairs | Labeled chunk MRR improved from 0.529 to 0.558, but open-noob queries regressed: NQ4, NQ6, and NQ9 got worse. Latency rose from 81 ms to 157 ms. Labeled-only win; real-world loss. |
| 7 | Does adding heading path fix the ms-marco regression? | Same model, input changed to `(query, heading_path + " — " + text)` | No. Labeled MRR stayed 0.558. Open-noob regressions changed but did not disappear; NQ6 got worse because the heading created a misleading lexical match. |
| 8 | Does BGE-reranker behave differently? | Swapped to `BAAI/bge-reranker-base`, same `(query, heading + text)` input | Labeled chunk MRR was 0.533, about the same as plain RRF. It fixed NQ4, NQ6, and NQ9, but broke NQ7, NQ21, NQ25, NQ28, and NQ30. Latency rose to 440 ms. Net wash. |
| 9 | Does `bge-large-en-v1.5` (1024-dim) meaningfully beat `bge-small-en-v1.5` (384-dim)? | Parameterized both engines for variable embed dim, built side-by-side `*.large.*` indexes, reran `evaluate.py --mode hybrid` and `ask.py --file noob_questions.txt` for both variants. | File MRR unchanged (0.950 / 0.950). Chunk MRR regressed 0.531/0.529 → 0.483/0.483: same right file, different chunk inside it. On the 30 noob queries: 5 clear large wins (NQ4 map-room, NQ19 install-ROS2, NQ20 velocity-from-terminal, NQ22 lidar-specs, NQ26 IP-change), 3 slight large wins, 1 clear small win (NQ30 API-key), 4 slight small wins, 17 ties. Sqlite latency flat (~78 ms); Lance latency rose ~70% (80 → 137 ms). Engines stayed equivalent. Resolves Q2: bge-large is a mild net-positive, not worth the 1.3 GB model and slower re-embed. |