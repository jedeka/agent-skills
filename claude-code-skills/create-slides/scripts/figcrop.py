"""figcrop.py: find a figure in a paper's PDF, look at its page on a coordinate grid, and crop it.

    python3 figcrop.py find <src> ["Fig. 2"]           pages and boxes where the text occurs; without text,
                                                        every caption start (Fig. N, Figure N, Table N)
    python3 figcrop.py page <src> <page> [--out F.png]  render the page with a 50 pt grid, list its images
    python3 figcrop.py crop <src> <page> x0 y0 x1 y1 [--out F] [--dpi 200]   crop that box to JPEG or PNG

<src> is a PDF (path or http(s) URL, downloaded once into the quotecheck.py cache) or a paper JSON,
whose "source.pdf" is used; then the default outputs follow the explainer project layout:
<project>/build/check/<key>-page<N>.png for page and <project>/figs/<key>.jpg for crop. Without a
paper JSON, page writes ./page<N>.png and crop needs --out.

Coordinates are PDF points from the page's top-left corner (1 pt = 1/72 in), the same in all three
commands. The grid draws a thin line every 50 pt and a labelled line every 100 pt (red for x, blue
for y); read the box off it, crop, and look at the crop. A caption usually sits under its figure and
a table's above it: `find` gives the caption's top, which bounds the figure's bottom. After a crop it
prints the "figure" entry for the paper JSON (write the caption yourself). Needs PyMuPDF and Pillow.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import quotecheck

CAPTION = re.compile(r"^\s*(Fig\.|Figure|FIGURE|Table|TABLE)\s*[A-Z]?\d+")
GRID_ZOOM = 1.5


def open_pdf(src: str):
    """(document, paper key or '', project folder or None) for a PDF path/URL or a paper JSON."""
    try:
        import pymupdf
    except ImportError:
        sys.exit("error: figcrop.py needs PyMuPDF (pip install pymupdf, or run scripts/setup.sh)")
    key, project, ref, base = "", None, src, Path(".")
    if src.endswith(".json") and Path(src).is_file():
        paper = json.loads(Path(src).read_text(encoding="utf-8"))
        ref = (paper.get("source") or {}).get("pdf")
        if not ref:
            sys.exit(f'error: {src} has no "source": {{"pdf": ...}}')
        key = paper.get("key", Path(src).stem)
        project = base = quotecheck.project_of(Path(src))
    try:
        path = quotecheck.fetch(ref, base)
    except quotecheck.SourceError as e:
        sys.exit(f"error: {e}")
    if not quotecheck.is_pdf(path):
        sys.exit(f"error: {ref} is not a PDF")
    return pymupdf.open(path), key, project


def get_page(doc, n: int):
    if not 1 <= n <= len(doc):
        sys.exit(f"error: page {n} outside 1-{len(doc)}")
    return doc[n - 1]


def cmd_find(a) -> int:
    doc, _, _ = open_pdf(a.src)
    hits = 0
    for i, pg in enumerate(doc, 1):
        if a.text:
            boxes = [(r, a.text) for r in pg.search_for(a.text)]
        else:
            boxes = []
            for b in pg.get_text("dict")["blocks"]:
                for ln in b.get("lines", []):
                    t = "".join(s["text"] for s in ln["spans"])
                    if CAPTION.match(t):
                        boxes.append((ln["bbox"], t.strip()[:70]))
        for r, t in boxes:
            x0, y0, x1, y1 = r
            print(f"page {i}: x0={x0:.0f} y0={y0:.0f} x1={x1:.0f} y1={y1:.0f}  {t!r}")
            hits += 1
    if not hits:
        print("no match" if a.text else "no caption lines found (search for a word of the caption instead)")
    return 0 if hits else 1


def cmd_page(a) -> int:
    from PIL import Image, ImageDraw
    import pymupdf
    doc, key, project = open_pdf(a.src)
    pg = get_page(doc, a.page)
    z = GRID_ZOOM
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(z, z))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im)
    w, h = pg.rect.width, pg.rect.height
    for x in range(0, int(w) + 1, 50):
        major = x % 100 == 0
        dr.line([(x * z, 0), (x * z, im.height)], fill=(220, 0, 0) if major else (255, 175, 175), width=1)
        if major:
            dr.text((x * z + 3, 3), str(x), fill=(200, 0, 0))
    for y in range(0, int(h) + 1, 50):
        major = y % 100 == 0
        dr.line([(0, y * z), (im.width, y * z)], fill=(0, 0, 220) if major else (175, 175, 255), width=1)
        if major:
            dr.text((3, y * z + 3), str(y), fill=(0, 0, 200))
    if a.out:
        out = Path(a.out)
    elif project:
        out = project / "build" / "check" / f"{key}-page{a.page}.png"
    else:
        out = Path(f"page{a.page}.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    print(f"wrote {out}: page {a.page} is {w:.0f} x {h:.0f} pt; red lines = x, blue = y, every 50 pt, "
          "labelled every 100")
    for r, n in image_groups(pg):
        print(f"  raster image{'s' if n > 1 else ''} ({n}) at x0={r.x0:.0f} y0={r.y0:.0f} x1={r.x1:.0f} y1={r.y1:.0f}")
    return 0


def image_groups(pg) -> list:
    """Raster images on the page, clipped to it, with touching ones merged: [(box, count)].
    Vector figures (plots drawn as paths) do not appear here; read them off the grid."""
    import pymupdf
    boxes = []
    for info in pg.get_image_info():
        r = pymupdf.Rect(info["bbox"]) & pg.rect
        if not r.is_empty and r.width * r.height > 100:
            boxes.append([r, 1])
    merged = True
    while merged:
        merged = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i][0], boxes[j][0]
                if not (pymupdf.Rect(a.x0 - 4, a.y0 - 4, a.x1 + 4, a.y1 + 4) & b).is_empty:
                    boxes[i] = [a | b, boxes[i][1] + boxes[j][1]]
                    del boxes[j]
                    merged = True
                    break
            if merged:
                break
    return [(r, n) for r, n in boxes]


def cmd_crop(a) -> int:
    from PIL import Image
    import pymupdf
    doc, key, project = open_pdf(a.src)
    pg = get_page(doc, a.page)
    box = pymupdf.Rect(a.x0, a.y0, a.x1, a.y1)
    if box.is_empty or not pg.rect.contains(box):
        sys.exit(f"error: box {a.x0:g} {a.y0:g} {a.x1:g} {a.y1:g} is empty or outside the page "
                 f"(0 0 {pg.rect.width:g} {pg.rect.height:g})")
    if a.out:
        out = Path(a.out)
    elif project:
        out = project / "figs" / f"{key}.jpg"
    else:
        sys.exit("error: give --out FILE (.jpg or .png) when the source is not a paper JSON")
    if out.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        sys.exit("error: --out must end in .jpg or .png")
    s = a.dpi / 72
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(s, s), clip=box)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() == ".png":
        im.save(out, optimize=True)
    else:
        im.save(out, quality=90)
    print(f"wrote {out} ({im.width} x {im.height} px at {a.dpi} dpi)")
    rel = out.relative_to(project).as_posix() if project and out.resolve().is_relative_to(project.resolve()) \
        else str(out)
    entry = {"file": rel, "page": a.page, "box": [round(v) for v in (a.x0, a.y0, a.x1, a.y1)],
             "caption": "[What to look at in the figure, <= 120 characters]"}
    print('"figure": ' + json.dumps(entry, ensure_ascii=False))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find", help="where a text occurs; without text, every caption start")
    f.add_argument("src")
    f.add_argument("text", nargs="?", default="")
    g = sub.add_parser("page", help="render a page with a coordinate grid")
    g.add_argument("src")
    g.add_argument("page", type=int)
    g.add_argument("--out", default="")
    c = sub.add_parser("crop", help="crop a box (PDF points) from a page")
    c.add_argument("src")
    c.add_argument("page", type=int)
    for k in ("x0", "y0", "x1", "y1"):
        c.add_argument(k, type=float)
    c.add_argument("--out", default="")
    c.add_argument("--dpi", type=int, default=200)
    a = p.parse_args(argv)
    return {"find": cmd_find, "page": cmd_page, "crop": cmd_crop}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
