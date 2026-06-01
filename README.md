# ROSMASTER M3 Pro — Documentation Corpus & Expert Skill

A cleaned-up, searchable offline mirror of Yahboom's [ROSMASTER M3 Pro](https://category.yahboom.net/products/rosmaster-m3-pro) course documentation, packaged as a skill that Claude (Hermes) and other AI agents can use to answer questions about the robot.

The project does three things:

1. **Converts** the vendor's PDF course material into clean, structured Markdown.
2. **Reorganizes** 18 loosely-numbered course modules into a coherent table of contents and copy-edits the machine-translated English into readable technical documentation.
3. **Makes it searchable** through a local hybrid-retrieval index and a packaged agent skill, so an AI agent can ground its answers in the source docs instead of guessing.

There is no network dependency at query time and no LLM answer synthesis in this repository — it produces ranked, citable source passages from the corpus.

## What's in this repository

| Path | Contents |
|---|---|
| [`skills/rosmaster-m3pro-expert/`](skills/rosmaster-m3pro-expert/) | The production deliverable: the cleaned Markdown corpus, a prebuilt retrieval index, query/build scripts, and the `SKILL.md` that lets an AI agent use them. |
| [`pdf-source/`](pdf-source/) | The original Yahboom course PDFs the corpus is derived from. Treated as read-only source material. |
| [`rag-experiments/`](rag-experiments/) | The controlled retrieval study that decided the skill's final search design (engine, embedding model, chunking, fusion, routing). |

## The documentation corpus

The corpus lives at [`skills/rosmaster-m3pro-expert/assets/corpus/`](skills/rosmaster-m3pro-expert/assets/corpus/) — **247 Markdown files** across **18 course modules**, mirrored from the PDFs in [`pdf-source/`](pdf-source/) and edited for clarity.

The full table of contents is in the [**course catalog**](skills/rosmaster-m3pro-expert/assets/corpus/README.md). It is organized into two parts:

- **Part A — Operate the Robot:** setup and first run, mobility and navigation, robotic-arm manipulation, perception and vision, and the embodied-AI stack — roughly the order you learn to use the kit.
- **Part B — Platform & Foundations** *(reference):* operating system / ROS 2 / Docker, the compute boards (Jetson, Raspberry Pi), STM32 + micro-ROS control-board firmware, and OpenCV image-processing basics.

**How the docs were produced:**

- PDFs were converted to Markdown with [Marker](https://github.com/datalab-to/marker), preserving figures, code blocks, tables, and command examples.
- Each module was then given a full editorial pass: awkward machine-translation phrasing was rewritten, headings and tables were tidied, and the structure was made consistent — while keeping every command, file path, topic name, IP address, and technical value accurate. The editing guidelines are recorded in [`assets/PROMPTS.md`](skills/rosmaster-m3pro-expert/assets/PROMPTS.md).

## The expert skill

[`skills/rosmaster-m3pro-expert/`](skills/rosmaster-m3pro-expert/) is a self-contained skill. Its [`SKILL.md`](skills/rosmaster-m3pro-expert/SKILL.md) instructs an agent to ground robot answers in the bundled docs: search first, read the top passages, and answer with concrete commands, launch files, and expected robot state, citing the source files and headings.

**How an AI agent uses it.** Run the query wrapper from the skill directory:

```bash
cd skills/rosmaster-m3pro-expert
python scripts/query_robot_docs.py "How do I make the robot map a room?"
python scripts/query_robot_docs.py "How do I calibrate the robotic arm servos?" --top-k 5
```

The script returns JSON: for each hit it gives the source `link`/`path`, a best-effort `line` number, the `heading_path` breadcrumb for section context, a `snippet`, and the full chunk `text` for grounding. The agent uses these to answer with citations rather than from general robotics knowledge.

**Retrieval design (summary).** Hybrid search over the corpus: `BAAI/bge-small-en-v1.5` semantic vectors plus SQLite FTS5/BM25 keyword search, with heading breadcrumbs exposed to both channels, fused with Reciprocal Rank Fusion, and a narrow deterministic route-boost layer for a few predictable beginner intents. The prebuilt index ships at [`assets/index/rosmaster_m3pro.sqlite`](skills/rosmaster-m3pro-expert/assets/index/); rebuild it with `python scripts/build_index.py --rebuild`. See [`references/retrieval-notes.md`](skills/rosmaster-m3pro-expert/references/retrieval-notes.md) for the exact configuration.

## Retrieval research

The search design was not arbitrary — it came out of a controlled study in [`rag-experiments/`](rag-experiments/) that compared two local engines (SQLite + sqlite-vec vs. LanceDB), embedding-model sizes, chunking strategies, reranking, and routing against a hand-labeled benchmark. See [`rag-experiments/README.md`](rag-experiments/README.md) for the research question, methods, results, and findings, and [`rag-experiments/PS-LEDGER.md`](rag-experiments/PS-LEDGER.md) for the chronological decision log.

Headline result: on the labeled benchmark both engines reach file MRR 1.000; the biggest quality lever was exposing heading breadcrumbs to first-stage retrieval. The skill ships the SQLite implementation because it is smaller, faster, and more transparent.

## Repository layout

```text
ROSMASTER-M3PRO/
├── skills/
│   └── rosmaster-m3pro-expert/   # Production skill
│       ├── SKILL.md              # Agent instructions
│       ├── assets/
│       │   ├── corpus/           # 247 cleaned Markdown files (18 modules)
│       │   ├── index/            # Prebuilt SQLite retrieval index
│       │   └── PROMPTS.md        # Documentation-editing guidelines
│       ├── scripts/              # query_robot_docs.py, build_index.py, ...
│       └── references/           # retrieval-notes.md
├── pdf-source/                   # Original Yahboom course PDFs (source material)
├── rag-experiments/              # Retrieval study: engines, benchmark, ledger
└── README.md                     # This file
```

## Robot context

The ROSMASTER M3 Pro is a ROS 2 Humble platform with a Mecanum-wheel chassis, pendulum suspension, a 6-DOF arm, a binocular depth camera, and dual TOF LiDAR. It runs on Jetson Nano B01, Jetson Orin Nano Super, Jetson Orin NX Super, or Raspberry Pi 5 main boards.

Product and hardware information: <https://category.yahboom.net/products/rosmaster-m3-pro>.

## Sources and credits

- **Course content:** copyright Yahboom. The PDFs in [`pdf-source/`](pdf-source/) are the as-shipped training material, redistributed here for offline reference and indexing.
- **Markdown conversion:** produced by [Marker](https://github.com/datalab-to/marker).
- **Upstream support, per Yahboom:** WhatsApp `+86 18682378128`, email `support@yahboom.com`.
