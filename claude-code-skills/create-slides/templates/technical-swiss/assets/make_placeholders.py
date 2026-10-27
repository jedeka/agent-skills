"""Generate the neutral placeholder images used by the technical-swiss slide templates.

Usage:
    python3 make_placeholders.py            # writes the PNGs next to this script
    python3 make_placeholders.py --out DIR  # writes them into DIR

Each placeholder is a flat #F4F4F2 panel with a thin #D9D9D9 border and a centred gray label
(Inter) naming the intended content and aspect ratio. Sizes are close to the size each image is
shown at on the 1920 x 1080 canvas, so the label stays legible and the files stay small.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "fonts"

FILL, BORDER, INK, SUB = "#F4F4F2", "#D9D9D9", "#929292", "#B4B4B4"

# file name, width, height, label, sub-label
PLACEHOLDERS = [
    ("placeholder-cover.png", 1426, 1200, "Cover visual", "diagram, photo or scene · fits 713 x 600"),
    ("placeholder-figure-16x9.png", 1600, 900, "Figure", "plot, diagram or screenshot · 16:9"),
    ("placeholder-chart-16x10.png", 1600, 1000, "Chart", "axes, units and labels inside · 16:10"),
    ("placeholder-photo-a.png", 1200, 900, "Image A", "photo or render · 4:3"),
    ("placeholder-photo-b.png", 1200, 900, "Image B", "photo or render · 4:3"),
    ("placeholder-photo-c.png", 1200, 900, "Image C", "photo or render · 4:3"),
]


def draw(width, height, label, sub):
    """Return one placeholder image: panel, 2 px border, two centred lines of text."""
    img = Image.new("RGB", (width, height), FILL)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width - 1, height - 1], outline=BORDER, width=2)
    big = ImageFont.truetype(str(FONTS / "Inter-600.ttf"), width // 18)
    small = ImageFont.truetype(str(FONTS / "Inter-400.ttf"), width // 34)
    cx, cy = width / 2, height / 2
    d.text((cx, cy - width // 60), label, font=big, fill=INK, anchor="ms")
    d.text((cx, cy + width // 30), sub, font=small, fill=SUB, anchor="mt")
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=HERE, help="output directory (default: here)")
    out = ap.parse_args().out
    out.mkdir(parents=True, exist_ok=True)
    for name, w, h, label, sub in PLACEHOLDERS:
        draw(w, h, label, sub).save(out / name, optimize=True)
        print(out / name)


if __name__ == "__main__":
    main()
