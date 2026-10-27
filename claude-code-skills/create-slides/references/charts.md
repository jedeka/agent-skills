# Charts

Charts are static PNGs drawn with `scripts/charts.py` (matplotlib, Inter, theme colours) and placed as images. The functions and their arguments are listed in the script's docstring. Run it with the venv's python from `scripts/setup.sh`; `python3 scripts/charts.py <out_dir>` writes one sample chart per form, with made-up numbers. When the home folder is read-only, charts.py points matplotlib's cache at a per-user folder in the system temp dir by itself.

## Pick the form by the job

| job | form |
|---|---|
| the same measure before and after, or under two conditions | dumbbell: hollow marker = baseline, filled marker = new, a rule between them |
| several conditions measured against a target | dot plot with a dashed target line |
| magnitudes of a few categories | horizontal bars, sorted by value unless the order means something |
| one value that carries the slide | not a chart: use the `13-key-number` slide |
| many values to read exactly | not a chart: use a table |

## Rules

- **One message per chart.** The slide title states it, and the chart shows it.
- **Colour follows meaning.**
  - The baseline series is gray (#666666, or a hollow #929292 marker).
  - The focal series is blue (#315EF5) or ink (#111111).
  - A failing row or value is red (#D93838). Nothing else is red.
- **Identity never rides on colour alone.** Use marker shape (hollow or filled, circle or square), a legend for two or more series, and direct labels.
- **Label selectively.** Label the values the argument uses, not every point. A label never overlaps a tick label: if a row has no room on its left, put one label on the right ("0.011 → 0.000").
- **One axis.** Never a dual axis. Use recessive gridlines (#D9D9D9) and keep the axis, unit and population in the x label.
- **Size for the slide.** Draw at the size the image will occupy (for example 1155 × 714 px in 8 columns), at 2× resolution, so tick and label text reads at 24 px or more.
- **Check the result.** Open every chart image before it goes on a slide, looking for collisions, clipped labels and empty space.
- **Reproducible.** Charts read their numbers from the same data file the tables use, never from hand-typed values, so chart and table cannot disagree.
