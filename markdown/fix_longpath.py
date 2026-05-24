"""Convert the two PDFs that hit Windows MAX_PATH during the main batch.

Strategy: copy each PDF to a short temp path, run marker, then place the
output at markdown/<source-folder>/<stem>.md (no per-PDF subdir) so the
total path stays under 260 chars. Images land alongside.
"""
import shutil
import tempfile
import time
from pathlib import Path

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import save_output

SRC_ROOT = Path(__file__).resolve().parent.parent
DST_ROOT = SRC_ROOT / "markdown"

PROBLEMS = [
    "3.AI Model - Text Version/5.Robotic arm gripping+Multimodal visual understand+SLAM navigation/Robotic arm gripping+Multimodal visual understand+SLAM navigation.pdf",
    "4.AI Model - Voice Version/5.Robotic arm gripping+Multimodal visual understand+SLAM navigation/Robotic arm gripping+Multimodal visual understand+SLAM navigation.pdf",
]


def main():
    print("Loading models...", flush=True)
    t0 = time.time()
    converter = PdfConverter(artifact_dict=create_model_dict())
    print(f"Models loaded in {time.time()-t0:.1f}s", flush=True)

    for i, rel in enumerate(PROBLEMS, 1):
        src = SRC_ROOT / rel
        if not src.exists():
            print(f"[{i}] MISSING: {src}", flush=True)
            continue
        # Flatten: drop the per-PDF subfolder for these two outliers
        final_dir = DST_ROOT / Path(rel).parent
        final_md = final_dir / f"{src.stem}.md"
        if final_md.exists() and final_md.stat().st_size > 0:
            print(f"[{i}] SKIP (exists): {final_md.relative_to(SRC_ROOT)}", flush=True)
            continue
        print(f"[{i}] {rel}", flush=True)

        with tempfile.TemporaryDirectory(prefix="mk_", dir="C:\\") as tmp:
            tmp = Path(tmp)
            short_pdf = tmp / "a.pdf"
            shutil.copy2(src, short_pdf)
            out_dir = tmp / "out"
            out_dir.mkdir()

            t1 = time.time()
            rendered = converter(str(short_pdf))
            save_output(rendered, str(out_dir), "a")
            print(f"  converted in {time.time()-t1:.1f}s", flush=True)

            # save_output may or may not create a subfolder — find the .md
            md_candidates = list(out_dir.rglob("*.md"))
            print(f"  produced files: {[str(p.relative_to(out_dir)) for p in out_dir.rglob('*') if p.is_file()]}", flush=True)
            if not md_candidates:
                print("  !! no .md produced — aborting this file", flush=True)
                continue
            produced_md = md_candidates[0]
            produced_dir = produced_md.parent

            final_dir.mkdir(parents=True, exist_ok=True)
            md_text = produced_md.read_text(encoding="utf-8")
            final_md.write_text(md_text, encoding="utf-8")

            for f in produced_dir.iterdir():
                if f == produced_md:
                    continue
                if f.suffix == ".json" and f.stem.endswith("_meta"):
                    target = final_dir / f"{src.stem}_meta.json"
                else:
                    target = final_dir / f.name
                shutil.copy2(f, target)
            print(f"  wrote {final_md.relative_to(SRC_ROOT)}", flush=True)

    print("Done.", flush=True)


if __name__ == "__main__":
    main()
