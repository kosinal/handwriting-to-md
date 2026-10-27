# /// script
# requires-python = ">=3.9"
# dependencies = ["pypdfium2", "pillow"]
# ///
import argparse
from pathlib import Path

from PIL import Image


def render(pdf, out_dir, scale):
    import pypdfium2 as pdfium

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(pdfium.PdfDocument(pdf), start=1):
        path = out / f"page-{i}.png"
        page.render(scale=scale).to_pil().save(path)
        print(path)


def crop(png, left, top, width, height, out):
    Image.open(png).crop((left, top, left + width, top + height)).save(out)
    print(out)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Render PDF pages to PNG and crop regions.")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render", help="render every page to <out_dir>/page-N.png")
    r.add_argument("pdf")
    r.add_argument("out_dir")
    r.add_argument("--scale", type=float, default=3)
    c = sub.add_parser("crop", help="cut a box (pixels) out of a PNG")
    c.add_argument("png")
    for name in ("left", "top", "width", "height"):
        c.add_argument(name, type=int)
    c.add_argument("out")
    a = p.parse_args()
    if a.cmd == "render":
        render(a.pdf, a.out_dir, a.scale)
    else:
        crop(a.png, a.left, a.top, a.width, a.height, a.out)
