"""Query the local markdown RAG index built by rag_index.py.

Usage:
    python rag_query.py "how do I unlock the controller buttons"
    python rag_query.py "moveit2 pick and place" -k 5
    python rag_query.py "lidar setup" --full        # print full chunk text, not snippet
"""
from __future__ import annotations

import argparse
import sqlite3
import struct
import sys
from pathlib import Path

import numpy as np
import sqlite_vec
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DB = SCRIPT_DIR / "rag_index.db"


def serialize_f32(vec: np.ndarray) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec.astype(np.float32).tolist())


def open_db(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn


def snippet(text: str, max_chars: int = 400) -> str:
    text = " ".join(text.split())
    return text if len(text) <= max_chars else text[:max_chars].rstrip() + " ..."


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", help="Natural-language question")
    ap.add_argument("-k", "--top-k", type=int, default=8, help="Number of results (default: 8)")
    ap.add_argument("--db", default=str(DEFAULT_DB), help=f"SQLite index path (default: {DEFAULT_DB})")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"Embedding model (default: {DEFAULT_MODEL})")
    ap.add_argument("--full", action="store_true", help="Print the full chunk text instead of a snippet")
    args = ap.parse_args()

    db_path = Path(args.db).resolve()
    if not db_path.exists():
        print(f"Index not found at {db_path}. Run rag_index.py first.", file=sys.stderr)
        return 2

    model = SentenceTransformer(args.model)
    q_emb = model.encode(
        [QUERY_INSTRUCTION + args.query],
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0]

    conn = open_db(db_path)
    rows = conn.execute(
        """
        SELECT c.file_path, c.heading_path, c.text, v.distance
        FROM vec_chunks v
        JOIN chunks c ON c.id = v.rowid
        WHERE v.embedding MATCH ?
          AND k = ?
        ORDER BY v.distance
        """,
        (serialize_f32(np.asarray(q_emb)), args.top_k),
    ).fetchall()
    conn.close()

    if not rows:
        print("No results.")
        return 1

    for i, (file_path, heading_path, text, distance) in enumerate(rows, 1):
        # sqlite-vec returns L2 distance; vectors are unit-normalized so
        # ||a-b||^2 = 2 - 2*cos(a,b), hence cos = 1 - distance^2 / 2.
        cosine = 1.0 - (distance * distance) / 2.0
        loc = f"{file_path}"
        if heading_path:
            loc += f"  ::  {heading_path}"
        print(f"\n[{i}] cos={cosine:.3f}  {loc}")
        print("    " + (text if args.full else snippet(text)).replace("\n", "\n    "))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
