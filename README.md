# ROSMASTER M3 Pro Local RAG Retrieval Study

## Abstract

This repository is a searchable offline mirror of Yahboom's ROSMASTER M3 Pro course documentation and a controlled retrieval study over that corpus. The research question was practical: for a fixed set of Marker-converted Markdown manuals, which local retrieval design gives beginners the most relevant source chunks without using a network service at query time?

The final system uses hybrid retrieval over 247 Markdown files: BGE-small embeddings, BM25/FTS keyword search, heading breadcrumbs exposed to both retrieval channels, Reciprocal Rank Fusion, and a narrow deterministic route-boost layer for predictable beginner intents. On the labeled benchmark, both sqlite-vec and LanceDB reach file MRR 1.000. Chunk MRR is 0.613 for sqlite-rag and 0.562 for lance-db-rag. The remaining weak answers are primarily corpus-coverage limitations, not retriever failures.

## Research Question

Given a small technical corpus of robotics course material, can a fully local RAG retriever reliably surface answer-bearing chunks for natural-language beginner questions, and does the storage engine materially affect retrieval quality?

## Corpus

- Source: Yahboom ROSMASTER M3 Pro PDF course material.
- Converted form: Marker-generated Markdown under [`markdown/`](markdown/).
- Size: 247 Markdown files, about 2.2k retrieval chunks in the final legacy-chunking index.
- Domain: ROS2 Humble, chassis control, robotic arm operation, SLAM/navigation, camera/lidar perception, Linux setup, AI/LLM demos, Docker, and multi-vehicle workflows.
- Constraint: the source corpus is fixed. This project does not add or rewrite authoritative documentation.

## Methods

Two independent local retrieval engines are implemented:

| Engine | Storage | Keyword channel | Vector channel |
|---|---|---|---|
| [`sqlite-rag/`](sqlite-rag/) | SQLite + sqlite-vec | FTS5 / BM25 | BGE-small vectors |
| [`lance-db-rag/`](lance-db-rag/) | LanceDB | Tantivy FTS | BGE-small vectors |

The final retrieval pipeline is:

1. Split Markdown by heading path, using the legacy NX8/NX10 sliding-window chunker.
2. Embed `heading_path + body` with `BAAI/bge-small-en-v1.5`.
3. Index heading and body text for keyword retrieval.
4. At query time, run semantic and keyword retrieval with a widened candidate pool.
5. Fuse ranks with Reciprocal Rank Fusion.
6. Apply small, transparent post-fusion route boosts for a few observed beginner intents: room mapping, chassis velocity commands, and narrow ROS2 workflow questions.

The evaluation harness is in [`tests/`](tests/):

- [`tests/evaluate.py`](tests/evaluate.py): 10 hand-labeled cases with file-rank and chunk-rank MRR / Hits@k.
- [`tests/ask.py`](tests/ask.py): 30 unlabeled beginner questions for subjective top-3 relevance review.
- [`PS-LEDGER.md`](PS-LEDGER.md): chronological experiment ledger and decision record.

## Results

Final labeled results, hybrid mode, `small_h` heading-aware index:

| Metric | sqlite-rag | lance-db-rag |
|---|---:|---:|
| File MRR | 1.000 | 1.000 |
| Chunk MRR | 0.613 | 0.562 |
| File match @1 | 10/10 | 10/10 |
| Chunk match @1 | 5/10 | 4/10 |
| File match @3 | 10/10 | 10/10 |
| Chunk match @3 | 7/10 | 7/10 |
| File match @8 | 10/10 | 10/10 |
| Chunk match @8 | 8/10 | 8/10 |
| Median latency | about 40 ms | about 85-105 ms |

Targeted beginner-query outcomes after the final routing layer:

| Question | Final top result |
|---|---|
| "How do I make the robot map a room?" | `6.Lidar Course/7.Cartographer-SLAM mapping` |
| "How do I make the robot drive in a straight line for 1 meter?" | `5.Chassis Control Course/1.ROS control > Controlling the Car's Speed` |
| "How do I send a velocity command from the terminal to move the robot?" | `5.Chassis Control Course/1.ROS control > Controlling the Car's Speed` |

## Main Findings

### Engine Choice

sqlite-vec and LanceDB are equivalent on observed retrieval quality after configuration parity. The initial LanceDB gap came from raw natural-language FTS queries and a smaller hybrid candidate pool, not from an inferior retrieval engine. Once LanceDB used the same stop-word-filtered OR query and the same per-channel pool size, the quality gap closed.

The engine decision is therefore operational:

- sqlite-rag is smaller, simpler, faster, and more transparent.
- lance-db-rag has better growth headroom, dataset versioning, and built-in vector-index machinery.

### Best Quality Lever

The largest improvement came from exposing `heading_path` to first-stage retrieval. Prepending heading breadcrumbs before embedding and adding the heading path to the keyword index moved file MRR from 0.950 to 1.000 and improved chunk MRR from roughly 0.53 to 0.613/0.562.

### Model Size

`BAAI/bge-large-en-v1.5` helped a few diffuse beginner questions but regressed labeled chunk MRR from 0.531/0.529 to 0.483/0.483, increased Lance latency by about 70%, and increased model footprint from about 130 MB to about 1.3 GB. It is not the default.

### Reranking

Off-the-shelf cross-encoder rerankers were not reliable on this corpus. They fixed some ambiguous noob questions but broke clean queries where RRF had already found the correct result. The default is no reranker; Lance still keeps reranking as an opt-in experimental flag.

### Chunking

Boundary-aware chunking produced cleaner text and avoided splitting code fences and Markdown tables, but it reduced retrieval quality. Labeled chunk MRR fell from 0.613/0.562 to 0.548/0.546, and important noob queries regressed. The final default is the legacy heading-aware sliding-window chunker.

### Local Routing

Small deterministic route boosts solved the remaining predictable beginner-query failures without lowering the labeled benchmark. The rules are deliberately narrow and post-fusion; they should not become a broad synonym system.

## Limitations

- The labeled benchmark has only 10 cases. It is useful for regression detection, not broad statistical claims.
- The 30 noob questions are subjective review prompts, not scored labels.
- Some weak answers are caused by missing source coverage. Because this project cannot add new authoritative corpus material, those are recorded as corpus limitations.
- Multi-query LLM expansion and domain-fine-tuned reranking are closed as non-goals under the local/offline retrieval constraint.

## Reproducibility

Build the final heading-aware indexes:

```powershell
pip install -r sqlite-rag/rag_requirements.txt
pip install -r lance-db-rag/rag_requirements.txt

python sqlite-rag/rag_index.py --db sqlite-rag/rag_index.h.db --model BAAI/bge-small-en-v1.5 --chunking legacy --rebuild
python lance-db-rag/rag_index.py --db lance-db-rag/index.h.lance --variant small --chunking legacy --rebuild
```

Run the labeled evaluation:

```powershell
python tests/evaluate.py --variant small_h --mode hybrid
```

Run the subjective noob-question review:

```powershell
python tests/ask.py --variant small_h --mode hybrid --file tests/noob_questions.txt
```

Ask an individual question:

```powershell
python sqlite-rag/rag_query.py --db sqlite-rag/rag_index.h.db "How do I make the robot map a room?"
python lance-db-rag/rag_query.py --db lance-db-rag/index.h.lance "How do I send a velocity command from the terminal?"
```

Results are ranked source chunks with file paths and heading breadcrumbs. There is no LLM answer synthesis in this repository.

## Repository Layout

```text
ROSMASTER-M3PRO/
|-- pdf-source/      Original Yahboom course PDFs
|-- markdown/        Marker-converted Markdown and extracted figures
|-- sqlite-rag/      Local hybrid RAG backed by SQLite + sqlite-vec + FTS5
|-- lance-db-rag/    Local hybrid RAG backed by LanceDB
|-- tests/           Retrieval-quality harness and query sets
|-- PS-LEDGER.md     Research ledger: hypotheses, decisions, experiment log
`-- README.md        This summary
```

## Course Catalog

The 18 modules under [`markdown/`](markdown/) are mirrored from [`pdf-source/`](pdf-source/):

| Group | Module |
|---|---|
| Setup and operation | [`0. Configuration and Operation Guide`](markdown/0.Configuration%20and%20Operation%20Guide/) |
| Platform internals | [`12. Control Board Course`](markdown/12.Control%20Board%20Course/), [`13. Main Control Course`](markdown/13.Main%20Control%20Course/), [`14. Linux System Course`](markdown/14.Linux%20System%20Course/), [`15. ROS Basic Course`](markdown/15.ROS%20Basic%20Course/), [`16. Docker Course`](markdown/16.Docker%20Course/) |
| AI / LLM stack | [`1. AI Model Basics`](markdown/1.AI%20Model%20Basics/), [`2. AI Model Development`](markdown/2.AI%20Model%20Development/), [`3. AI Model - Text Version`](markdown/3.AI%20Model%20-%20Text%20Version/), [`4. AI Model - Voice Version`](markdown/4.AI%20Model%20-%20Voice%20Version/) |
| Motion and manipulation | [`5. Chassis Control Course`](markdown/5.Chassis%20Control%20Course/), [`9. Robotic Arm and 3D Space Gripping Course`](markdown/9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/), [`10. MoveIt2 Simulation Course`](markdown/10.MoveIt2%20Simulation%20Course/), [`11. Multi-vehicle Course`](markdown/11.Multi-vehicle%20Course/) |
| Perception | [`6. Lidar Course`](markdown/6.Lidar%20Course/), [`7. Depth Camera Course`](markdown/7.Depth%20Camera%20Course/), [`8. Mediapipe Visual Course`](markdown/8.Mediapipe%20Visual%20Course/), [`17. Image Processing Basics Course`](markdown/17.Image%20Processing%20Basics%20Course/) |

## Robot Context

The ROSMASTER M3 Pro is a ROS2 Humble platform with a Mecanum-wheel chassis, pendulum suspension, 6-DOF arm, binocular depth camera, and dual TOF LiDAR. It runs on Jetson Nano B01, Jetson Orin Nano Super, Jetson Orin NX Super, or Raspberry Pi 5 main boards.

Product description and hardware information: <https://category.yahboom.net/products/rosmaster-m3-pro>.

## Sources and Credits

- Course content: copyright Yahboom. PDFs in [`pdf-source/`](pdf-source/) are the as-shipped training material, redistributed here for offline reference and indexing.
- Markdown conversion: produced by [Marker](https://github.com/datalab-to/marker). See [`markdown/convert.log`](markdown/convert.log) for the conversion run.
- Upstream contact, per Yahboom: WhatsApp `+86 18682378128`, email `support@yahboom.com`.
