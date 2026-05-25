# ROSMASTER M3 Pro ROS2 Robot for Jetson NANO B01/Orin NX SUPER/Orin NANO SUPER/RPi 5

A searchable mirror of [Yahboom](https://category.yahboom.net/products/rosmaster-m3-pro)'s course documentation for the **ROSMASTER M3 Pro** robotics platform, plus local command-line RAG (Retrieval-Augmented Generation) tooling for asking natural-language questions over the docs without a network call.

The original Yahboom material ships as PDFs. This repo keeps the PDFs alongside a git-friendly markdown conversion produced by [Marker](https://github.com/datalab-to/marker), so the content is both grep-able and embedding-friendly.

## Repository layout

```
ROSMASTER-M3PRO/
├── pdf-source/      Original Yahboom course PDFs (246 documents across 18 modules)
├── markdown/        Marker-converted markdown + extracted figures, one folder per PDF
├── sqlite-rag/      Local hybrid RAG over markdown/, backed by SQLite + sqlite-vec + FTS5
└── lance-db-rag/    Local hybrid RAG over markdown/, backed by LanceDB (parallel implementation)
```

Both RAG folders are independent — same chunking, same embedding model (BGE-small-en-v1.5), same hybrid retrieval (semantic + BM25 fused with Reciprocal Rank Fusion), different storage engines. See each folder's README for the design rationale and a head-to-head comparison.

## Searching the docs

Pick either RAG implementation; both expose the same CLI.

```powershell
# Lighter option: single .db file, ~3 small Python deps
pip install -r sqlite-rag/rag_requirements.txt
python sqlite-rag/rag_index.py
python sqlite-rag/rag_query.py "how do I unlock the controller buttons"
python sqlite-rag/rag_query.py "moveit2 pick and place" -k 5
python sqlite-rag/rag_query.py "lidar setup" --mode keyword
```

```powershell
# Heavier option: built-in HNSW + auto-embedding + dataset versioning
pip install -r lance-db-rag/rag_requirements.txt
python lance-db-rag/rag_index.py
python lance-db-rag/rag_query.py "how do I unlock the controller buttons"
```

Results are ranked chunks with file paths and heading breadcrumbs — no LLM synthesis. You read the chunks yourself or pipe them downstream. First run downloads the ~130 MB embedding model into your HuggingFace cache; subsequent runs are incremental (sha256 per file).

## Course catalog

The 18 modules under [`markdown/`](markdown/) (and mirrored in [`pdf-source/`](pdf-source/)):

| Group | Module |
|---|---|
| **Setup & operation** | [`0. Configuration and Operation Guide`](markdown/0.Configuration%20and%20Operation%20Guide/) |
| **Platform internals** | [`12. Control Board Course`](markdown/12.Control%20Board%20Course/) · [`13. Main Control Course`](markdown/13.Main%20Control%20Course/) · [`14. Linux System Course`](markdown/14.Linux%20System%20Course/) · [`15. ROS Basic Course`](markdown/15.ROS%20Basic%20Course/) · [`16. Docker Course`](markdown/16.Docker%20Course/) |
| **AI / LLM stack** | [`1. AI Model Basics`](markdown/1.AI%20Model%20Basics/) · [`2. AI Model Development`](markdown/2.AI%20Model%20Development/) · [`3. AI Model - Text Version`](markdown/3.AI%20Model%20-%20Text%20Version/) · [`4. AI Model - Voice Version`](markdown/4.AI%20Model%20-%20Voice%20Version/) |
| **Motion & manipulation** | [`5. Chassis Control Course`](markdown/5.Chassis%20Control%20Course/) · [`9. Robotic Arm and 3D Space Gripping Course`](markdown/9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/) · [`10. MoveIt2 Simulation Course`](markdown/10.MoveIt2%20Simulation%20Course/) · [`11. Multi-vehicle Course`](markdown/11.Multi-vehicle%20Course/) |
| **Perception** | [`6. Lidar Course`](markdown/6.Lidar%20Course/) · [`7. Depth Camera Course`](markdown/7.Depth%20Camera%20Course/) · [`8. Mediapipe Visual Course`](markdown/8.Mediapipe%20Visual%20Course/) · [`17. Image Processing Basics Course`](markdown/17.Image%20Processing%20Basics%20Course/) |

## About the robot

The ROSMASTER M3 Pro is a ROS2 Humble platform with a Mecanum-wheel chassis, pendulum suspension, 6-DOF arm, binocular depth camera, and dual TOF LiDAR. It runs on a choice of Jetson NANO B01, Jetson Orin NANO SUPER, Jetson Orin NX SUPER, or Raspberry Pi 5 main boards, and the courses cover everything from controller use through SLAM, MoveIt2, voice/text LLM interaction, and multi-vehicle coordination.

Full product description, hardware specs, and purchase info: <https://category.yahboom.net/products/rosmaster-m3-pro>.

## Sources & credits

- **Course content**: © Yahboom. PDFs in [`pdf-source/`](pdf-source/) are the as-shipped Yahboom training material; this repo redistributes them for convenient offline reference and indexing.
- **Markdown conversion**: produced by [Marker](https://github.com/datalab-to/marker) (see `markdown/convert.log` for the run log). The conversion preserves text, tables, and inline figures; some formatting may diverge from the original PDF.
- **Upstream contact** (per Yahboom): WhatsApp `+86 18682378128`, email `support@yahboom.com`.
