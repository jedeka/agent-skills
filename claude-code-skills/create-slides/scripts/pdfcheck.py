"""pdfcheck.py: check a printed slide PDF for collisions, as Chromium actually laid it out.

    python3 pdfcheck.py <deck.pdf> [--pages N] [--band 80] [--tol 2] [--label TEXT] [--allow overlays.json]

Chromium's print layout can differ from its screen layout (an image that shrinks inside a flex or grid
box on screen can print at its natural size and spill under the next element), so the screen check
in deck.py does not cover the PDF. This script reads the PDF itself, in canvas pixels (the page
width maps to 1920 px), and reports per page:

  page      the page is not 16:9 (1920 x 1080 px), or the page count differs from --pages
  text      two text lines overlap (glyph boxes, so tightly set display type does not trip it)
  image     a text line overlaps an image, or two images overlap
  panel     a text line or an image runs across the edge of a filled panel (starts outside it and
            runs into it); content wholly inside a panel is fine
  footer    text, an image or a panel enters the footer band (the bottom --band px), other than
            the footer itself: the page number "NN / TOTAL" and the footer label given by --label

Vector drawings other than filled rectangles (hairline rules, connector arrows, SVG formulas drawn
as glyph paths) are not read here; deck.py check covers them on the screen layout, which the
freeze before printing keeps equal to the print layout for images and SVG.

--allow takes {"pages": {"<n>": [[x0, y0, x1, y1], ...]}} in canvas px: the boxes of elements marked
data-layer="overlay" in the slide HTML (deck.py pdf writes it). A text line or image inside such a
box may overlap content outside it; two overlay items still may not overlap each other.

Prints "PDF OK: ..." or one line per finding and "PDF FAIL: ..."; exits 0 when clean, 1 on
findings, 2 on an unreadable file. Needs PyMuPDF (pip install pymupdf).
"""
import argparse
import json
import re
import sys

import pymupdf

W, H = 1920, 1080
PAGE_NUM = re.compile(r"^\d+\s*/\s*\d+$")
# Tight glyph boxes where PyMuPDF offers them; otherwise font-ascender boxes, shrunk in text_lines().
ACCURATE = getattr(pymupdf, "TEXT_ACCURATE_BBOXES", 0)


class Item:
    """One text line or image on a page, in canvas px."""

    def __init__(self, kind, box, text, size=0.0):
        self.kind, self.box, self.text, self.size = kind, box, text, size
        self.label = text[:48] + ("..." if len(text) > 48 else "")
        self.overlay = False

    def __repr__(self):
        return f'"{self.label}"' if self.kind == "text" else f"image {self.label}"


def scaled(rect, s):
    return pymupdf.Rect(rect.x0 * s, rect.y0 * s, rect.x1 * s, rect.y1 * s)


def text_lines(page, s):
    items = []
    for b in page.get_text("dict", flags=ACCURATE)["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b["lines"]:
            spans = [sp for sp in ln["spans"] if sp["text"].strip()]
            if not spans:
                continue
            box = pymupdf.Rect()
            for sp in spans:
                box |= pymupdf.Rect(sp["bbox"])
            size = max(sp["size"] for sp in spans) * s
            box = scaled(box, s)
            if not ACCURATE:               # ascender boxes: keep the middle 80 % of the line
                cut = 0.1 * box.height
                box = pymupdf.Rect(box.x0, box.y0 + cut, box.x1, box.y1 - cut)
            text = re.sub(r"\s+", " ", "".join(sp["text"] for sp in spans)).strip()
            items.append(Item("text", box, text, size))
    return items


def images(page, s):
    out = []
    for i, info in enumerate(page.get_image_info()):
        box = scaled(pymupdf.Rect(info["bbox"]), s)
        if box.width > 1 and box.height > 1:
            out.append(Item("image", box, f"#{i + 1} ({box.width:.0f} x {box.height:.0f} px)"))
    return out


def panels(page, s):
    """Filled rectangles that are not the page background, white, or a hairline rule."""
    out = []
    for d in page.get_drawings():
        fill = d.get("fill")
        if not fill or d.get("fill_opacity", 1) == 0 or len(d["items"]) != 1 or d["items"][0][0] not in ("re", "qu"):
            continue
        box = scaled(pymupdf.Rect(d["rect"]), s)
        if min(fill[:3]) > 0.99 or box.width < 16 or box.height < 16 or box.width * box.height > 0.9 * W * H:
            continue
        out.append(box)
    return out


def overlap(a, b, tol, vtol=None):
    """(width, height) of the intersection when it exceeds the tolerances, else None."""
    w = min(a.x1, b.x1) - max(a.x0, b.x0)
    h = min(a.y1, b.y1) - max(a.y0, b.y0)
    return (w, h) if w > tol and h > (tol if vtol is None else vtol) else None


def inside(a, b, tol):
    return a.x0 >= b.x0 - tol and a.y0 >= b.y0 - tol and a.x1 <= b.x1 + tol and a.y1 <= b.y1 + tol


def is_footer(text, label):
    """The page number, the footer label, or the two read as one line."""
    t = re.sub(r"\s+", " ", text).strip()
    if label:
        t = t.replace(re.sub(r"\s+", " ", label).strip(), "", 1).strip() if t != label else ""
    return t == "" or bool(PAGE_NUM.match(t))


def check_page(page, pno, band, tol, allow, label=""):
    s = W / page.rect.width
    ph = page.rect.height * s
    finds = []
    if abs(page.rect.width / page.rect.height - W / H) > 0.002:
        finds.append(f"page {pno}: [page] {page.rect.width:.0f} x {page.rect.height:.0f} pt is not 16:9 "
                     f"(expected 1920 x 1080 px)")
    texts, imgs, fills = text_lines(page, s), images(page, s), panels(page, s)
    for it in texts + imgs:
        it.overlay = any(inside(it.box, a, tol) for a in allow)
    at = lambda wh, a, b: f"by {wh[0]:.0f} x {wh[1]:.0f} px at ({max(a.x0, b.x0):.0f}, {max(a.y0, b.y0):.0f})"

    def layered(a, b):
        """True when an overlay item meets base-layer content: allowed."""
        return a.overlay != b.overlay

    for i, a in enumerate(texts):
        for b in texts[i + 1:]:
            if layered(a, b):
                continue
            # lines of one paragraph may touch ascender to descender; the overlap must exceed 12 % of
            # the smaller type size before it counts, while text side by side overlaps its full height
            wh = overlap(a.box, b.box, tol, max(tol, 0.12 * min(a.size, b.size)))
            if wh:
                finds.append(f"page {pno}: [text] {a!r} overlaps {b!r} {at(wh, a.box, b.box)}")
        for im in imgs:
            wh = None if layered(a, im) else overlap(a.box, im.box, tol)
            if wh:
                finds.append(f"page {pno}: [image] text {a!r} overlaps {im!r} {at(wh, a.box, im.box)}")
    for i, a in enumerate(imgs):
        for b in imgs[i + 1:]:
            wh = None if layered(a, b) else overlap(a.box, b.box, tol)
            if wh:
                finds.append(f"page {pno}: [image] {a!r} overlaps {b!r} {at(wh, a.box, b.box)}")
    for p in fills:
        for it in texts + imgs:
            if it.overlay or inside(it.box, p, tol) or inside(p, it.box, tol):
                continue
            wh = overlap(it.box, p, tol)
            if wh:
                what = f"text {it!r}" if it.kind == "text" else repr(it)
                finds.append(f"page {pno}: [panel] {what} runs across the edge of the filled panel "
                             f"({p.x0:.0f}, {p.y0:.0f}) to ({p.x1:.0f}, {p.y1:.0f}) {at(wh, it.box, p)}")
    top = ph - band
    foot = {id(t) for t in texts if t.box.y0 >= top - tol and is_footer(t.text, label)}
    for it in texts + imgs:
        if id(it) not in foot and it.box.y1 > top + tol:
            finds.append(f"page {pno}: [footer] {it!r} reaches y {it.box.y1:.0f}; the footer band starts at "
                         f"y {top:.0f}")
    for p in fills:
        if p.y1 > top + tol:
            finds.append(f"page {pno}: [footer] a filled panel reaches y {p.y1:.0f}; the footer band starts "
                         f"at y {top:.0f}")
    return finds, (len(texts), len(imgs), len(fills))


def check(pdf, pages=None, band=80.0, tol=2.0, allow=None, label=""):
    """(findings as lines of text, empty when clean; page count; [text lines, images, panels] checked)."""
    doc = pymupdf.open(pdf)
    allow = allow or {}
    finds, seen = [], [0, 0, 0]
    if pages is not None and len(doc) != pages:
        finds.append(f"page count: [page] the PDF has {len(doc)} pages, expected {pages}")
    for i, page in enumerate(doc, 1):
        boxes = [pymupdf.Rect(*r) for r in allow.get(str(i), [])]
        f, counts = check_page(page, i, band, tol, boxes, label)
        finds += f
        seen = [x + y for x, y in zip(seen, counts)]
    return list(dict.fromkeys(finds)), len(doc), seen


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("pdf")
    p.add_argument("--pages", type=int, help="expected page count")
    p.add_argument("--band", type=float, default=80, help="footer band height in canvas px (default 80)")
    p.add_argument("--tol", type=float, default=2, help="overlap tolerance in canvas px (default 2)")
    p.add_argument("--label", default="", help="the deck's footer label, if it has one")
    p.add_argument("--allow", help='JSON {"pages": {"<n>": [[x0,y0,x1,y1], ...]}} of overlay boxes')
    a = p.parse_args(argv)
    try:
        allow = json.load(open(a.allow, encoding="utf-8"))["pages"] if a.allow else {}
        finds, n, seen = check(a.pdf, a.pages, a.band, a.tol, allow, a.label)
    except (RuntimeError, OSError, ValueError, KeyError) as e:
        print(f"error: cannot check {a.pdf}: {e}", file=sys.stderr)
        return 2
    for f in finds:
        print(f)
    if finds:
        pages = set(re.findall(r"^page (\d+):", "\n".join(finds), re.M))
        print(f"PDF FAIL: {len(finds)} finding(s) on {len(pages)} of {n} pages")
        return 1
    print(f"PDF OK: {n} pages, 16:9; {seen[0]} text lines, {seen[1]} images and {seen[2]} filled panels "
          "checked: no overlaps, nothing in the footer band")
    return 0


if __name__ == "__main__":
    sys.exit(main())
