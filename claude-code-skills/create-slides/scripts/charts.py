"""charts.py: matplotlib charts in the technical-swiss style, sized for the 1920x1080 slide canvas.

    python3 charts.py <out_dir>    # writes three sample charts, with made-up numbers, into out_dir

From a script (the deck's own chart script, kept beside the data it reads):

    import sys; sys.path.insert(0, "<skill>/scripts"); import charts
    fig = charts.dumbbell([("condition A", 0.42, 0.81), ...], "before", "after",
                          xlabel="accuracy", target=0.80, width_px=1155, height_px=640)
    charts.save(fig, "<deck_dir>/assets/chart_accuracy.png")

Sizing rule: a figure is drawn at 1 pt = 1 canvas px (figsize = px / 72 inches) and saved at 2x
pixel density, so a 24 pt label is 24 px on the slide when the <img> is shown at width_px. Show
the image at exactly that width (save() prints the <img> tag); save() warns about any text under
24 px. Build the figure at the size of the slot it fills: a c8 column is 1155 px wide.

Colours have one meaning each (references/technical-swiss.md): RED failure or below target,
BLUE the focal method, GREEN meets target, AMBER caveat; everything else is neutral ink and gray.
Identity also rides on marker shape and direct labels, never on hue alone.
matplotlib is imported on first use (with mathsvg.quiet_mpl_cache: no cache warning when the home
folder is read-only); everything else is the standard library.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mathsvg import quiet_mpl_cache  # noqa: E402

FONTS = Path(__file__).resolve().parents[1] / "templates" / "technical-swiss" / "fonts"
INK, SEC, TER, RULE, PANEL = "#111111", "#666666", "#929292", "#D9D9D9", "#F4F4F2"
RED, BLUE, GREEN, AMBER = "#D93838", "#315EF5", "#198754", "#C78A00"
MEANING = {RED: "failure / below target", BLUE: "focal method", GREEN: "meets target",
           AMBER: "caveat / provisional"}
MIN_PX = 24                  # smallest text on the canvas
LABEL = 28                   # tick labels, axis labels, legend, direct labels (caption size)
MARKER = 22 ** 2             # scatter marker area: 22 px across
_plt = None


def plt():
    """matplotlib.pyplot with the theme fonts and rcParams applied (imported once, lazily)."""
    global _plt
    if _plt is None:
        quiet_mpl_cache()
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib import font_manager, pyplot
        for f in sorted(FONTS.glob("*.ttf")):
            font_manager.fontManager.addfont(str(f))
        pyplot.rcParams.update({
            "font.family": "Inter", "font.size": LABEL, "axes.labelsize": LABEL,
            "xtick.labelsize": LABEL, "ytick.labelsize": LABEL, "legend.fontsize": LABEL,
            "axes.labelcolor": SEC, "xtick.color": SEC, "ytick.color": INK,
            "axes.edgecolor": RULE, "axes.linewidth": 1.5, "axes.spines.top": False,
            "axes.spines.right": False, "axes.spines.left": False, "axes.axisbelow": True,
            "axes.labelpad": 12, "xtick.major.size": 6, "xtick.major.width": 1.5,
            "xtick.major.pad": 8, "ytick.major.size": 0, "ytick.major.pad": 16,
            "grid.color": RULE, "grid.linewidth": 1.5, "lines.linewidth": 3,
            "legend.frameon": False, "legend.handletextpad": 0.4, "legend.columnspacing": 1.6,
            "figure.facecolor": "white", "savefig.facecolor": "white", "pdf.fonttype": 42})
        _plt = pyplot
    return _plt


def figure(width_px: int = 1155, height_px: int = 640):
    """A figure and axes at 1 pt = 1 canvas px."""
    return plt().subplots(figsize=(width_px / 72, height_px / 72), dpi=72)


def save(fig, path, width_px: int = None, height_px: int = None, scale: int = 2) -> Path:
    """Save at `scale`x density; optionally resize to the slot first. Warns about text < 24 px."""
    from matplotlib.text import Text
    if width_px:
        h = height_px or fig.get_figheight() * 72 * width_px / (fig.get_figwidth() * 72)
        fig.set_size_inches(width_px / 72, h / 72)
    fig.tight_layout(pad=0.6)
    w, h = round(fig.get_figwidth() * 72), round(fig.get_figheight() * 72)
    small = sorted({(round(t.get_fontsize(), 1), t.get_text()[:30]) for t in fig.findobj(Text)
                    if t.get_visible() and t.get_text().strip() and t.get_fontsize() < MIN_PX})
    for size, text in small:
        print(f"warning: chart text '{text}' is {size} px on the canvas (< {MIN_PX})", file=sys.stderr)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=72 * scale)
    plt().close(fig)
    print(f'wrote {path}: show as <img src="assets/{path.name}" style="width:{w}px;height:{h}px">')
    return path


# ---------------------------------------------------------------- shared pieces

def _rows(ax, labels, red=(), focus=()):
    """Category axis top-down; red rows get red semibold tick labels, focus rows blue."""
    ys = list(range(len(labels)))[::-1]
    ax.set_yticks(ys)
    ax.set_yticklabels(labels)
    for tick, lab in zip(ax.get_yticklabels(), labels):
        if lab in red or lab in focus:
            tick.set_color(RED if lab in red else BLUE)
            tick.set_fontweight(600)
    ax.set_ylim(-0.6, len(labels) - 0.4)
    ax.grid(axis="x")
    return ys


def _inside(ax, artists, placed, renderer) -> bool:
    box = ax.get_window_extent(renderer)
    for a in artists:
        e = a.get_window_extent(renderer)
        if e.x0 < box.x0 or e.x1 > box.x1 or e.y0 < box.y0 or e.y1 > box.y1:
            return False
        if any(e.overlaps(p) for p in placed):
            return False
    return True


def _place(ax, options, placed):
    """Try label layouts in order; keep the first whose labels stay inside the axes (so they never
    meet tick labels) and clear earlier labels. Each option is a list of annotate() kwargs."""
    renderer = ax.figure.canvas.get_renderer()
    made = []
    for opt in options:
        made = [ax.annotate(textcoords="offset points", fontsize=LABEL, **kw) for kw in opt]
        if _inside(ax, made, placed, renderer):
            break
        if opt is not options[-1]:
            for a in made:
                a.remove()
    placed.extend(a.get_window_extent(renderer) for a in made)


def _target(ax, x, label):
    """Dashed target line; returns its legend handle (the label lives in the legend, so it can
    never collide with the data or the legend)."""
    ax.axvline(x, color=INK, lw=2, ls=(0, (4, 3)), zorder=0)
    return plt().Line2D([], [], color=INK, lw=2, ls=(0, (4, 3)), label=label)


def _legend(ax, handles):
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.0, 1.02), ncol=len(handles),
              borderaxespad=0, handletextpad=0.4)


# ---------------------------------------------------------------- chart forms

def dumbbell(rows, a_label, b_label, xlabel="", xlim=None, fmt="{:.2f}", red=(), label_rows=(),
             target=None, target_label=None, width_px=1155, height_px=None):
    """Two values per row: hollow gray marker = a (before, baseline), filled marker = b (after).

    rows: [(label, a, b)]. red: labels drawn red (failure rows). label_rows: rows that get direct
    value labels, placed beside the markers, else as one "a → b" label, else above the row.
    """
    labels = [r[0] for r in rows]
    fig, ax = figure(width_px, height_px or 72 * len(rows) + 210)
    ys = _rows(ax, labels, red=red)
    vals = [v for r in rows for v in r[1:]] + ([target] if target is not None else [])
    pad = 0.06 * ((max(vals) - min(vals)) or 1)
    ax.set_xlim(*(xlim or (min(vals) - pad, max(vals) + pad)))
    for y, (lab, a, b) in zip(ys, rows):
        ink = RED if lab in red else INK
        ax.plot([a, b], [y, y], color=RULE, lw=3, zorder=1)
        ax.scatter(a, y, s=MARKER, facecolor="white", edgecolor=TER, lw=3, zorder=3)
        ax.scatter(b, y, s=MARKER, color=ink, zorder=3)
    handles = [plt().Line2D([], [], ls="", marker="o", ms=20, mfc="white", mec=TER, mew=3,
                            label=a_label),
               plt().Line2D([], [], ls="", marker="o", ms=20, color=INK, label=b_label)]
    if target is not None:
        handles.append(_target(ax, target, target_label or f"target {fmt.format(target)}"))
    _legend(ax, handles)
    ax.set_xlabel(xlabel)
    fig.tight_layout(pad=0.6)
    placed = []
    for y, (lab, a, b) in zip(ys, rows):
        if lab not in label_rows:
            continue
        ink = RED if lab in red else INK
        (lo, clo), (hi, chi) = sorted([(a, SEC), (b, ink)])
        both = f"{fmt.format(a)} → {fmt.format(b)}"
        _place(ax, [
            [dict(text=fmt.format(lo), xy=(lo, y), xytext=(-18, 0), ha="right", va="center", color=clo),
             dict(text=fmt.format(hi), xy=(hi, y), xytext=(18, 0), ha="left", va="center", color=chi)],
            [dict(text=both, xy=(hi, y), xytext=(18, 0), ha="left", va="center", color=ink)],
            [dict(text=both, xy=(lo, y), xytext=(-18, 0), ha="right", va="center", color=ink)],
            [dict(text=both, xy=((a + b) / 2, y), xytext=(0, 16), ha="center", va="bottom", color=ink)],
        ], placed)
    return fig


def dots(labels, series, xlabel="", xlim=None, fmt="{:.2f}", focus=None, target=None,
         target_label=None, below_red=False, label_rows=(), width_px=1155, height_px=None):
    """Cleveland dot plot: one row per label, one marker shape per series on the row's line.

    series: [(name, [value per label])]. focus: the series drawn blue (the deck's method); the
    others are neutral. below_red: points under `target` turn red (they miss it). label_rows:
    rows whose focus (or only) series value gets a direct label.
    """
    shapes, neutrals = "osD^v", [INK, SEC, TER]
    fig, ax = figure(width_px, height_px or 72 * len(labels) + 210)
    ys = _rows(ax, labels)
    ax.grid(axis="y", color=RULE, lw=1, ls=(0, (1, 3)))
    vals = [v for _, vs in series for v in vs] + ([target] if target is not None else [])
    pad = 0.06 * ((max(vals) - min(vals)) or 1)
    ax.set_xlim(*(xlim or (min(vals) - pad, max(vals) + pad)))
    s, handles, k = plt(), [], 0
    for i, (name, vs) in enumerate(series):
        col = BLUE if name == focus else neutrals[k % 3]
        k += name != focus
        cols = [RED if below_red and target is not None and v < target else col for v in vs]
        ax.scatter(vs, ys, s=MARKER, marker=shapes[i % 5], c=cols, zorder=3 + (name == focus))
        handles.append(s.Line2D([], [], ls="", marker=shapes[i % 5], ms=20, color=col, label=name))
    if target is not None:
        handles.append(_target(ax, target, target_label or f"target {fmt.format(target)}"))
    _legend(ax, handles)
    ax.set_xlabel(xlabel)
    fig.tight_layout(pad=0.6)
    main = dict(series).get(focus, series[0][1])
    placed = []
    for y, lab, v in zip(ys, labels, main):
        if lab in label_rows:
            col = RED if below_red and target is not None and v < target else INK
            _place(ax, [[dict(text=fmt.format(v), xy=(v, y), xytext=(x, 0), ha=ha, va="center",
                              color=col)] for x, ha in ((18, "left"), (-18, "right"))]
                   + [[dict(text=fmt.format(v), xy=(v, y), xytext=(0, 16), ha="center",
                            va="bottom", color=col)]], placed)
    return fig


def hbar(labels, values, xlabel="", xlim=None, fmt="{:.2f}", focus=(), red=(), target=None,
         target_label=None, width_px=1155, height_px=None):
    """Horizontal bars with direct value labels at the bar ends (inside the bar if no room).

    Bars are neutral gray; focus rows blue, red rows red (failure). Values may be negative.
    """
    fig, ax = figure(width_px, height_px or 72 * len(labels) + 170)
    ys = _rows(ax, labels, red=red, focus=focus)
    cols = [RED if lab in red else BLUE if lab in focus else TER for lab in labels]
    ax.barh(ys, values, height=0.62, color=cols, zorder=2)
    vals = list(values) + [0] + ([target] if target is not None else [])
    span = (max(vals) - min(vals)) or 1
    ax.set_xlim(*(xlim or (min(vals) - (0.12 * span if min(vals) < 0 else 0),
                           max(vals) + 0.2 * span)))
    ax.axvline(0, color=INK, lw=1.5, zorder=3)
    if target is not None:
        _legend(ax, [_target(ax, target, target_label or f"target {fmt.format(target)}")])
    ax.set_xlabel(xlabel)
    fig.tight_layout(pad=0.6)
    placed = []
    for y, v, c in zip(ys, values, cols):
        out, inside = (12, "left"), (-12, "right")
        if v < 0:
            out, inside = (-12, "right"), (12, "left")
        _place(ax, [[dict(text=fmt.format(v), xy=(v, y), xytext=(out[0], 0), ha=out[1],
                          va="center", color=INK)],
                    [dict(text=fmt.format(v), xy=(v, y), xytext=(inside[0], 0), ha=inside[1],
                          va="center", color="white", fontweight=600)]], placed)
    return fig


# ---------------------------------------------------------------- demo

def demo(out_dir):
    """Three sample charts with made-up numbers, one per form."""
    out = Path(out_dir)
    rows = [("full instruction", 0.91, 0.95), ("colour only", 0.62, 0.88),
            ("size only", 0.55, 0.84), ("relational", 0.31, 0.72), ("absent object", 0.48, 0.12)]
    save(dumbbell(rows, "before re-ranking", "after re-ranking", xlabel="top-1 accuracy",
                  xlim=(0, 1.04), red=("absent object",),
                  label_rows=("relational", "absent object", "full instruction")),
         out / "chart_dumbbell.png")
    labels = ["condition A", "condition B", "condition C", "condition D", "condition E"]
    save(dots(labels, [("baseline", [0.84, 0.79, 0.88, 0.71, 0.93]),
                       ("method", [0.91, 0.90, 0.92, 0.86, 0.95])],
              xlabel="coverage", focus="method", target=0.90, below_red=True,
              label_rows=("condition D",)), out / "chart_dots.png")
    save(hbar(["speech end to transcript", "decision", "speech synthesis", "first motion"],
              [0.15, 0.40, 0.95, 0.70], xlabel="median seconds", fmt="{:.2f} s",
              focus=("decision",), width_px=1155, height_px=430), out / "chart_hbar.png")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("out_dir", help="folder for the three sample charts (made-up numbers): chart_dumbbell.png, "
                                   "chart_dots.png, chart_hbar.png")
    demo(p.parse_args(argv).out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
