"""contact_sheet.py: tile a deck's rendered slides into one labelled sheet, to review a whole deck at once.

    python3 scripts/deck.py png <deck_dir>                     # render the slides first
    python3 scripts/contact_sheet.py <deck_dir> [out.png]      # default out: <deck_dir>/build/contact-sheet.png

Four thumbnails per row. Each is labelled with its deck.json slide id ("09-chart" -> "09  chart") and,
under it, the slide's first heading: the first h1, h2 or h3 holding a letter (a bare section number
such as "02" is passed over), else the statement (.stmt), else the first kicker; a formula shows as
its TeX, and a heading too long for the tile is cut with "...". So the sheet says which slide holds
which content. Needs Pillow. Looking at the sheet does not replace opening single slides when text
is small.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

COLS, TW, TH, GAP, PAD = 4, 640, 360, 32, 48
LABEL = 96                   # under each tile: id line (26 px) and heading line (24 px)
FONTS = Path(__file__).resolve().parents[1] / "templates" / "technical-swiss" / "fonts"
HEADING = re.compile(r"<(h[1-3])\b[^>]*>(.*?)</\1\s*>", re.S | re.I)
FALLBACK = [re.compile(r"""<(p|div)\b[^>]*class\s*=\s*["'][^"']*\b%s\b[^>]*>(.*?)</\1\s*>""" % c, re.S | re.I)
            for c in ("stmt", "kicker")]
MATH = re.compile(r"""<(span|div)\b[^>]*class\s*=\s*["'][^"']*\bmath(?:-display)?\b[^>]*>(.*?)</\1\s*>""",
                  re.S | re.I)


def plain(fragment: str) -> str:
    """Text of an HTML fragment: formulas as $TeX$, tags dropped, white space collapsed."""
    fragment = MATH.sub(lambda m: f"${m[2].strip()}$", fragment)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def first_heading(src: str) -> str:
    """The slide's first heading holding a letter, else its statement, else its first kicker."""
    face = re.sub(r"<!--.*?-->|<aside\b.*?</aside>", " ", src, flags=re.S | re.I)
    for m in HEADING.finditer(face):
        text = plain(m[2])
        if re.search(r"[^\W\d_]", text):
            return text
    for rx in FALLBACK:
        m = rx.search(face)
        if m and plain(m[2]):
            return plain(m[2])
    return ""


def fit(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> str:
    """Cut text with "..." so it fits width px in font."""
    if draw.textlength(text, font=font) <= width:
        return text
    while text and draw.textlength(text + "...", font=font) > width:
        text = text[:-1]
    return text.rstrip() + "..."


def font(name: str, size: int):
    path = FONTS / name
    return ImageFont.truetype(str(path), size) if path.is_file() else ImageFont.load_default()


def sheet(deck_dir, out=None) -> Path:
    """Write the contact sheet of deck_dir (its slides must be rendered); return its path."""
    deck_dir = Path(deck_dir)
    ids = json.loads((deck_dir / "deck.json").read_text(encoding="utf-8"))["slides"]
    out = Path(out) if out else deck_dir / "build" / "contact-sheet.png"
    rows = -(-len(ids) // COLS)
    w = PAD * 2 + COLS * TW + (COLS - 1) * GAP
    h = PAD * 2 + rows * (TH + LABEL) + (rows - 1) * GAP
    img = Image.new("RGB", (w, h), "#E9E9E7")
    draw = ImageDraw.Draw(img)
    f_id, f_head = font("Inter-500.ttf", 26), font("Inter-400.ttf", 24)
    for i, sid in enumerate(ids):
        png = deck_dir / "build" / "png" / f"slide-{i + 1:02d}.png"
        if not png.is_file():
            sys.exit(f"missing {png}: run `deck.py png {deck_dir}` first")
        thumb = Image.open(png).convert("RGB").resize((TW, TH), Image.LANCZOS)
        x = PAD + (i % COLS) * (TW + GAP)
        y = PAD + (i // COLS) * (TH + LABEL + GAP)
        img.paste(thumb, (x, y))
        draw.rectangle([x - 1, y - 1, x + TW, y + TH], outline="#D9D9D9")
        num, _, name = sid.partition("-")
        draw.text((x, y + TH + 14), f"{num}  {name.replace('-', ' ')}", fill="#111111", font=f_id)
        src = deck_dir / "slides" / f"{sid}.html"
        head = first_heading(src.read_text(encoding="utf-8")) if src.is_file() else ""
        if head:
            draw.text((x, y + TH + 52), fit(draw, head, f_head, TW), fill="#666666", font=f_head)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    print(f"wrote {out} ({w}x{h}, {len(ids)} slides)")
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("deck_dir", help="deck folder holding deck.json, slides/ and build/png/")
    p.add_argument("out", nargs="?", default=None,
                   help="output PNG (default <deck_dir>/build/contact-sheet.png)")
    a = p.parse_args(argv)
    if not (Path(a.deck_dir) / "deck.json").is_file():
        p.error(f"{a.deck_dir}/deck.json not found")
    sheet(a.deck_dir, a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
