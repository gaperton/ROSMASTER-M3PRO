"""Convert all PDFs in the repo to markdown, mirroring the folder tree.

For each `<src>/<rel_dir>/<name>.pdf` writes
`<src>/markdown/<rel_dir>/<name>/<name>.md` plus extracted images.
Resumable: skips PDFs whose target .md already exists and is non-empty.
"""
import sys
import time
import traceback
from pathlib import Path

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import save_output

SRC_ROOT = Path(__file__).resolve().parent.parent
DST_ROOT = SRC_ROOT / "markdown"
SKIP_TOP_DIRS = {"markdown", ".git", ".claude", "node_modules", "__pycache__"}


def collect_pdfs(src_root: Path):
    pdfs = []
    for p in src_root.rglob("*.pdf"):
        rel = p.relative_to(src_root)
        if rel.parts[0] in SKIP_TOP_DIRS:
            continue
        pdfs.append(p)
    return sorted(pdfs)


def target_dir_for(pdf: Path) -> Path:
    rel = pdf.relative_to(SRC_ROOT)
    return DST_ROOT / rel.parent / pdf.stem


def main():
    pdfs = collect_pdfs(SRC_ROOT)
    print(f"Found {len(pdfs)} PDFs under {SRC_ROOT}", flush=True)

    # Pre-filter to figure out how many actually need work
    todo = []
    for pdf in pdfs:
        out_md = target_dir_for(pdf) / f"{pdf.stem}.md"
        if out_md.exists() and out_md.stat().st_size > 0:
            continue
        todo.append(pdf)
    print(f"{len(todo)} PDFs to convert ({len(pdfs)-len(todo)} already done)", flush=True)
    if not todo:
        return

    print("Loading marker models...", flush=True)
    t0 = time.time()
    artifact_dict = create_model_dict()
    converter = PdfConverter(artifact_dict=artifact_dict)
    print(f"Models loaded in {time.time()-t0:.1f}s", flush=True)

    failures = []
    total_t = time.time()
    for i, pdf in enumerate(todo, 1):
        out_dir = target_dir_for(pdf)
        rel = pdf.relative_to(SRC_ROOT)
        print(f"[{i}/{len(todo)}] {rel}", flush=True)
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            t1 = time.time()
            rendered = converter(str(pdf))
            save_output(rendered, str(out_dir), pdf.stem)
            print(f"  -> {time.time()-t1:.1f}s", flush=True)
        except Exception as e:
            print(f"  !! FAILED: {e}", flush=True)
            traceback.print_exc()
            failures.append((str(rel), str(e)))

    elapsed = time.time() - total_t
    print(f"\nFinished {len(todo)} files in {elapsed/60:.1f} min", flush=True)
    if failures:
        print(f"Failures ({len(failures)}):", flush=True)
        for rel, err in failures:
            print(f"  {rel}: {err}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
