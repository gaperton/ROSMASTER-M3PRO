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

- **Surfacing `heading_path` to first-stage retrieval is the single biggest lift the harness has measured.** Prepending the heading path to chunk text before embedding (so the dense vector carries section context) and adding `heading_path` as an FTS5 column (so BM25 also sees it) moved file MRR to ceiling (0.950 → 1.000), chunk MRR up to 0.613/0.562 (from 0.531/0.529 baseline; better than bge-large's 0.483/0.483), and gave +10 clear / +2 slight noob wins against 1 clear / 4 slight regressions after tuning the sqlite heading weight to 1.0. Sqlite latency stayed ~40–43 ms; lance ~105 ms. Same bge-small weights, no new dependency. Confirms Q6: bge-large in NX2 was reinventing the heading signal that the schema was silently withholding. *(Experiments 10–11.)*

## Working Hypotheses

> Plausible explanations or predictions not yet established by experiment.

- **H1. Cross-encoder rerankers help only when first-stage retrieval is genuinely ambiguous.** Most queries against a well-tuned hybrid retriever are not ambiguous enough to justify reranking. RRF over stop-word-filtered FTS plus a wide vector pool already handles them, so a reranker often adds noise.  
  *Falsified by:* finding a reranker that improves both clean and ambiguous queries on this corpus.

- **H2. Retrieval benchmarks often compare defaults more than engines.** In this project, the apparent LanceDB quality gap disappeared after configuration parity. The broader hypothesis is that many “engine X beats engine Y” comparisons are actually default-configuration comparisons.  
  *Falsified by:* finding two hybrid retrieval engines that still differ meaningfully after careful configuration parity on a fair task.

- **H3. For small-to-medium corpora, linear scan over normalized vectors is a reasonable default.** sqlite-vec brute-force search runs at ~37 ms median on 2,198 chunks. At this scale, HNSW may add setup cost, recall risk, and tuning complexity for little practical gain. This is not yet directly tested here.  
  *Falsified by:* HNSW producing substantially lower latency at this scale without quality loss.

- **H4. Corpus coverage is probably the next major quality lever.** About one third of noob questions hit gaps where the corpus does not contain a good answer. Retrieval tuning cannot recover answers that are not present. Supporting evidence: Experiment 9 showed that doubling embedding capacity yields only a handful of noob wins, several of which (e.g. NQ22 lidar specs) succeeded because the right doc *was* in the corpus and bge-large simply surfaced it.  
  *Test:* TBD. If adding missing docs improves win rate more than the ~3-clear-wins baseline NX2 produced, this hypothesis is supported.

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
  *Why:* it is lightweight, English-focused, adequate for the current corpus, and shared across both engines, which removes one comparison variable. Experiment 9 ran NX2 and found `bge-large-en-v1.5` is only a mild net-positive on diffuse noob queries while costing ~70% Lance latency, a labeled chunk-MRR regression, and a 1.3 GB weight footprint. Experiment 10 (NX8) then showed bge-small with heading_path surfaced to both retrieval channels beats bge-large outright.  
  *Revisit if:* the corpus becomes multilingual, gains a substantial body of long technical chunks where 1024-dim discrimination would matter more than it currently does, or a new embedding family meaningfully improves on bge-small at comparable cost.

- **Promote NX8 (heading_path in both retrieval channels) to the default index format.**  
  *Why:* Experiments 10–11 produced the best labeled and subjective numbers the harness has measured (file MRR 1.000, chunk MRR 0.613/0.562, +10/+2 vs. −1/−4 on noob) at no additional dependency or model cost. The variant lives at `*.h.*` paths; promoting means making it the path the default `small` variant points at. `rag_query.py` accepts both schemas via the FTS column-count probe in `_fts_bm25_expr`; sqlite uses heading weight 1.0 after NX10 tuning.  
  *Revisit if:* a later fix for NQ17 requires changing the schema or fusion logic rather than adding corpus coverage.

## Open Questions

> Important things we know we do not know. Each should point to an experiment that can resolve it.

- **Q3. Does multi-query expansion help imprecise beginner questions?**  
  This may improve recall, but it partially breaks the no-services-on-retrieval-path constraint.  
  *Test:* NX3.

- **Q4. Does boundary-aware chunking improve retrieval specificity?**  
  The current `chunk_section` slides a 1800-char window over raw body text with no respect for code fences, Markdown tables, list items, or paragraph breaks. A code-heavy technical corpus may be losing chunks that cut mid-fence. May help BM25 and cross-encoder discrimination but increases chunk count and changes RRF dynamics.  
  *Test:* NX9.

- **Q5. Would a domain-fine-tuned cross-encoder reliably beat the off-the-shelf rerankers?**  
  Plausible but expensive. Requires labeled query / relevant-passage training data we do not currently have.  
  *Test:* TBD; not actionable until a labeled training set exists.

## Next Experiments

> Planned actions expected to resolve open questions, refine hypotheses, or improve the toolchain. Ordered by expected impact.

1. **NX9 — Boundary-aware chunking.**  
   Rewrite `chunk_section` to prefer paragraph (`\n\n`), sentence, then character boundaries; never split inside a fenced code block (``` ```) or Markdown table. Also strip PDF-conversion litter (`<span id="page-…"></span>`, anchor-link wrappers) before embedding so the model and snippet renderer see clean text. Rebuild both indexes and rerun labeled + subjective evaluations.  
   *Resolves:* Q4. *Supersedes the earlier "paragraph-level chunking" framing — broadened after the post-NX2 review surfaced code-fence and table cases. Builds on top of `small_h` schema.*

2. **NX3 — Add multi-query expansion.**  
   Use Anthropic Haiku to produce 3–5 paraphrases per user query, search each, and fuse results with RRF. Decide whether the partial break of the offline-retrieval constraint is acceptable.  
   *Resolves:* Q3.

3. **NX5 — Add metadata and query routing.**  
   Tag chunks by module number, doc type, and difficulty. Route questions to likely module ranges: ROS to modules 15–16, AI to 1–4, and so on.  
   *Tool work.*

4. **NX6 — Generate labeled cases for the remaining docs.**  
   Use Claude Haiku to produce one plausible question per remaining doc and commit them to `tests/cases.jsonl`.  
   *Coverage work.*

5. **NX7 — Add per-mode side-by-side reporting.**  
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
| 10 | Does giving `heading_path` to first-stage retrieval recover NX2's noob wins without its costs? | Added `embed_source = "<heading_path> — <body>"` for embedding (sqlite: change `texts = …` in `index_file`; lance: new `SourceField`). Converted sqlite `fts_chunks(text)` → `fts_chunks(heading_path, text)` with `bm25(fts_chunks, 2.0, 1.0)`; lance FTS index moved to `embed_source`. Built side-by-side `*.h.*` indexes as variant `small_h`, ran labeled hybrid eval + 30-noob eyeball. | File MRR 0.950 → **1.000** (sqlite + lance), chunk MRR 0.531/0.529 → **0.600/0.562** — best numbers the harness has measured, beating bge-large's 0.483/0.483 with the same bge-small weights. Noob: +10 clear / +2 slight wins vs. small (NQ2 wifi-password, NQ8 wifi-losing, NQ11 ros2-topics, NQ13 camera-feed, NQ15 laptop-control, NQ16 launch-file, NQ19 install-ros2, NQ20 velocity, NQ24 follow-me, NQ30 api-key) against 2 clear regressions (NQ4 map-room, NQ17 drive-straight) and 4 slight (NQ5, NQ6, NQ9, NQ26). Sqlite latency dropped 81 → 38 ms; lance 80 → 105 ms. One labeled chunk regression: `ssh-putty` 6 → out-of-top-8 on sqlite. Resolves Q6 and validates H4's framing: the bottleneck NX2 hit wasn't model capacity, it was missing input signal. Two clear noob regressions trace to BM25-weighted heading words over-anchoring ("SLAM" in heading dominating actual SLAM tutorials; "Calibrate" matching "straight line"). |
| 11 | What heading BM25 weight minimises over-anchoring without giving up NX8's wins? | Parameterized `_fts_bm25_expr`, then swept sqlite `small_h` at weights 1.0, 1.25, 1.5, 1.75, and 2.0 with `tests/evaluate.py --engine sqlite --variant small_h --mode hybrid` and `tests/ask.py --variant small_h --mode hybrid --file tests/noob_questions.txt`. | Pareto frontier: **1.0**. Sqlite file MRR stayed 1.000; chunk MRR improved to **0.613** at 1.0/1.25 versus 0.600 at 1.5/1.75/2.0 because `ssh-putty` returns to top-8. On noob top-1, 1.0 is the only tested weight that recovers NQ4 (`Cartographer-SLAM mapping` rank 1); the other 29 sqlite top-1 results are unchanged from 2.0, so NX8's +10 wins are preserved. NQ17 remains a miss at every weight, still led by `Robotic Arm Calibration`; that failure is not solved by heading-weight tuning and likely needs corpus/query-routing work. Resolves Q7: use sqlite heading weight **1.0**. |
