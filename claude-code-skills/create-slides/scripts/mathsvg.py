r"""mathsvg.py: typeset TeX math as SVG glyph paths with matplotlib's mathtext; no LaTeX install needed.

    python3 mathsvg.py '\hat{y} = \frac{1}{n}\sum_i x_i' [--fontset cm] [--size 48] [--out f.svg]

deck.py calls it at build time: in a slide,
    <span class="math">TeX</span>          inline, at the surrounding text size, on its baseline
    <div class="math-display">TeX</div>    on its own line, at the theme's equation size (--t-eq)
are filled with an <svg> sized in em (so it scales with the element's font size), lowered by its
depth so its baseline sits on the text baseline, and painted in currentColor (the text colour).
Markup inside an HTML comment is left alone.
Write TeX without dollar signs; escape < > & as &lt; &gt; &amp;. The TeX stays in the SVG's
aria-label. A parse error raises MathError with the TeX and matplotlib's message, and the build
stops naming the slide. Glyphs are paths, so the formula looks the same in every viewer and
export, and its text cannot be selected.

mathtext is a subset of LaTeX: sub/superscripts, \frac, \sqrt, accents (\hat, \bar, \tilde),
Greek, \sum and other big operators, \mathbb, \mathcal, \mathrm, \text, \left( \right), spaces
(\, \; \quad). No environments (\begin{align}); write one formula per element instead. Accepted
aliases mathtext lacks: \le \ge \ne \lvert \rvert (to \leq \geq \neq | |).
Fontsets, all five that mathtext ships: cm (Computer Modern, the default), stix (STIX, Times-like
serif), stixsans (STIX sans), dejavusans and dejavuserif (DejaVu). A deck picks one with
"math_fontset" in deck.json. matplotlib's sixth value, custom, is not offered: it takes its fonts from
mathtext.* settings that a deck cannot pass. Needs matplotlib. When MPLCONFIGDIR is unset and
matplotlib's own config or cache folder cannot be written (a read-only home), matplotlib is pointed at
a per-user folder in the temp dir, so it neither warns nor rebuilds its font cache on every run.
"""
import argparse
import functools
import html
import os
import re
import sys
import tempfile
from pathlib import Path

FONTSETS = ("cm", "stix", "stixsans", "dejavusans", "dejavuserif")
FONTSET_HELP = ("cm (Computer Modern, the default), stix (Times-like serif), stixsans, dejavusans, "
                "dejavuserif")
REF = 100.0          # path units per em
ALIASES = {r"\le": r"\leq", r"\ge": r"\geq", r"\ne": r"\neq", r"\lvert": "|", r"\rvert": "|"}
MARKUP = re.compile(r"""<(span|div)(\s[^>]*?\bclass\s*=\s*["'][^"']*\bmath(-display)?\b[^"']*["'][^>]*)>(.*?)</\1\s*>""",
                    re.S | re.I)
COMMENT = re.compile(r"(<!--.*?-->)", re.S)


class MathError(ValueError):
    """TeX that mathtext cannot typeset."""


def _writable(d: Path) -> bool:
    try:
        d.mkdir(parents=True, exist_ok=True)
    except OSError:
        return False
    return d.is_dir() and os.access(d, os.W_OK)


def quiet_mpl_cache() -> None:
    """Call before importing matplotlib. If MPLCONFIGDIR is unset and matplotlib's default config or
    cache folder cannot be written, set MPLCONFIGDIR to <tempdir>/matplotlib-<uid>, a folder this
    user owns: matplotlib would otherwise warn and rebuild its font cache in a new folder every run."""
    if os.environ.get("MPLCONFIGDIR") or "matplotlib" in sys.modules:
        return
    home = Path.home()
    if sys.platform.startswith(("linux", "freebsd")):      # matplotlib's own choice of folders
        dirs = [Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config") / "matplotlib",
                Path(os.environ.get("XDG_CACHE_HOME") or home / ".cache") / "matplotlib"]
    else:
        dirs = [home / ".matplotlib"]
    if all(_writable(d) for d in dirs):
        return
    uid = os.getuid() if hasattr(os, "getuid") else None
    cache = Path(tempfile.gettempdir()) / f"matplotlib-{uid if uid is not None else 'user'}"
    try:
        cache.mkdir(mode=0o700, exist_ok=True)
        if uid is not None and cache.stat().st_uid != uid:
            return                                          # someone else's folder: leave matplotlib to it
    except OSError:
        return
    if _writable(cache):
        os.environ["MPLCONFIGDIR"] = str(cache)


def _num(v: float) -> str:
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


@functools.lru_cache(maxsize=512)
def tex_to_svg(tex: str, fontset: str = "cm", size: float = 0) -> str:
    """One formula as an <svg>: em-sized and baseline-aligned, or size px tall glyphs when size > 0."""
    if fontset not in FONTSETS:
        raise MathError(f"unknown math fontset '{fontset}'; choose one of: {FONTSET_HELP}")
    src = tex.strip()
    for a, b in ALIASES.items():
        src = re.sub(re.escape(a) + r"(?![A-Za-z])", lambda _: b, src)
    if not src:
        raise MathError("empty math element")
    quiet_mpl_cache()
    import matplotlib
    from matplotlib.font_manager import FontProperties
    from matplotlib.path import Path as MPath
    from matplotlib.textpath import TextPath, TextToPath
    with matplotlib.rc_context({"mathtext.fontset": fontset}):
        prop = FontProperties(size=REF)
        try:
            w, h, d = TextToPath().get_text_width_height_descent(f"${src}$", prop, ismath=True)
            path = TextPath((0, 0), f"${src}$", size=REF, prop=prop)
        except ValueError as e:
            msg = [ln.strip() for ln in str(e).strip().splitlines() if ln.strip()]
            raise MathError(f"cannot typeset '{tex.strip()}': {msg[-1] if msg else e}") from None
    ink = path.get_extents() if len(path.vertices) else None
    x0 = min(0.0, ink.x0) if ink else 0.0
    x1 = max(float(w), ink.x1) if ink else float(w)
    top = max(float(h - d), ink.y1) if ink else float(h - d)     # above the baseline
    bot = max(float(d), -ink.y0) if ink else float(d)            # below the baseline
    parts = []
    for verts, code in path.iter_segments(curves=True, simplify=False):
        pts = " ".join(f"{_num(x)} {_num(-y)}" for x, y in verts.reshape(-1, 2))
        parts.append({MPath.MOVETO: "M", MPath.LINETO: "L", MPath.CURVE3: "Q", MPath.CURVE4: "C"}
                     .get(code, "Z") + ("" if code == MPath.CLOSEPOLY else pts))
    box = f"{_num(x0)} {_num(-top)} {_num(x1 - x0)} {_num(top + bot)}"
    if size:
        dims = f'width="{_num((x1 - x0) * size / REF)}" height="{_num((top + bot) * size / REF)}"'
    else:
        dims = (f'style="width:{(x1 - x0) / REF:.3f}em;height:{(top + bot) / REF:.3f}em;'
                f'vertical-align:{-bot / REF:.3f}em"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" {dims} role="img" '
            f'aria-label="{html.escape(tex.strip(), quote=True)}"><path fill="currentColor" d="{"".join(parts)}"/></svg>')


def replace_math(src: str, fontset: str = "cm") -> str:
    """Fill every math element of an HTML fragment with its SVG; raise MathError on bad TeX.
    HTML comments are left as written (a template's comment shows math markup as an example)."""
    def one(m):
        tag, attrs, body = m[1], m[2], m[4]
        if "<svg" in body:
            return m[0]
        if "<" in body:
            raise MathError(f"math element holds HTML ({body.strip()[:60]!r}); write TeX only, "
                            "with < > & escaped as &lt; &gt; &amp;")
        return f"<{tag}{attrs}>{tex_to_svg(html.unescape(body), fontset)}</{tag}>"
    parts = COMMENT.split(src)
    return "".join(p if p.startswith("<!--") else MARKUP.sub(one, p) for p in parts)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("tex", help="TeX without dollar signs")
    p.add_argument("--fontset", default="cm", choices=FONTSETS, metavar="NAME",
                   help=f"math font: {FONTSET_HELP}")
    p.add_argument("--size", type=float, default=48, help="font size in px for the standalone file (default 48)")
    p.add_argument("--out", help="write the SVG here (default: print it)")
    a = p.parse_args(argv)
    try:
        svg = tex_to_svg(a.tex, a.fontset, a.size)
    except MathError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(svg + "\n")
        print(f"wrote {a.out} ({len(svg)} bytes)")
    else:
        print(svg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
