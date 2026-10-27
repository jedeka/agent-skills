# technical-swiss: the default theme

The source spec is `swiss-design-spec.md`. technical-swiss keeps its grid, hierarchy, restraint and colour discipline. It drops the minimalism: a technical deck carries the whole argument, including the numbers, conditions, populations, units and caveats a reviewer needs. Whitespace separates and groups content; it never stands in for it.

The stylesheet is `templates/technical-swiss/theme.css`. The values below are what it implements; change them there, not per slide.

## Canvas and grid

| item | value | why |
|---|---|---|
| canvas | 1920 × 1080 px (16:9) | 1 pt = 2 px on a 13.33 in slide |
| margins | 88 px left/right (≈ 0.6 in), 80 px top, 136 px bottom | the spec's 0.55–0.65 in; the bottom holds the footer |
| content area | 1744 × 864 px | everything in flow must fit here |
| grid | 12 columns of 123.33 px, 24 px gutters (≈ 0.17 in) | the spec's 0.15–0.20 in |
| column classes | `.c1`–`.c12` = 123, 271, 418, 565, 713, 860, 1007, 1155, 1302, 1449, 1597, 1744 px | two-column splits are 4 + 8, 5 + 7 or 6 + 6 |
| footer | the page number `NN / TOTAL` at the right, bottom 48 px, inside an 80 px footer band (`--foot-band`); a short label left of it only when the user asks; never a date | inserted by `scripts/deck.py build` |

## Type

One family, Inter; JetBrains Mono for equations, code and identifiers. Sentence case; uppercase only for small labels.

| role | px | pt | class |
|---|---|---|---|
| main title | 80 | 40 | `h1` |
| section title | 104 | 52 | `h1.section-title` |
| slide title | 60 | 30 | `h2` |
| key statement / quote | 72 | 36 | `.stmt` |
| key number | 240 | 120 | `.big` |
| body | 38 | 19 | `p`, `li` |
| secondary | 32 | 16 | `.s` |
| caption, table text | 28 | 14 | `.cap`, `table` |
| labels, footer | 24 | 12 | `.kicker`, `.meta` |
| equations | 48 | 24 | `.eq` |

Nothing is smaller than 24 px except table header labels (22 px, uppercase). Body text at 38 px holds about 0.55 × 38 ≈ 21 px per character: 34 characters per line in 5 columns, 41 in 6, 83 across all 12.

## Colour: one meaning per colour, fixed for the whole deck

| colour | hex | meaning |
|---|---|---|
| ink | #111111 | text, primary marks |
| secondary | #666666 | captions, labels, the baseline series |
| tertiary | #929292 | de-emphasised marks only (fails 4.5:1 for small text) |
| rule | #D9D9D9 | dividers, gridlines |
| panel | #F4F4F2 | grouping background, used sparingly |
| red | #D93838 | failure, below target, the dangerous case |
| blue | #315EF5 | the focal method or condition of the deck |
| green | #198754 | meets target (rare: most passing values stay ink) |
| amber | #C78A00 | caveat, limitation, provisional |

A colour never carries a meaning alone: a red value is also stated as below target in the text or caption, and a blue series is named in a legend or heading. Do not use red for emphasis.

## What makes it technical

- **Density.** A slide may fill its 864 px area. Split a slide when it overflows; never shrink text below the scale.
- **Conditions travel with numbers.** Every number on a slide is readable with its condition: threshold, population, n, unit, split count. Put these in the kicker ("05 · Results · ε = 0.10", with `ε` in a `.nocase` span) or the caption, not only in speaker notes.
- **Tables are typography.** Hairline rules, a 2 px rule under the header, right-aligned tabular numerals, one emphasised row or column, a `total` row when it helps. Trim columns the slide's claim does not need.
- **Captions name the population and the source.** One line under the visual: who, how many, what was measured.
- **Speaker notes hold provenance.** `<aside class="notes">`: source files, the command that produced the numbers, caveats too long for the slide.

## Layout rules

- Title top-left; the heading block (kicker + title) sits in the same place on every content slide.
- One dominant object per slide: a table, a chart, an image group or an equation set.
- Asymmetric columns: the larger region holds the technically important visual.
- Align everything to the grid or to another element's edge. Related items close, unrelated items visibly apart; use 12 / 20 / 28 / 40 px steps.
- No cards, shadows, gradients, rounded boxes or decorative shapes. Use a `.rule` hairline or a `.panel` background when grouping helps comprehension.

## Fit budget

Estimate before building, then confirm with `deck.py check`.

| element | height |
|---|---|
| heading block (kicker + one-line title) | ≈ 110 px, plus 69 px per extra title line |
| body line at 38 px | ≈ 49 px |
| table row at 28 px | ≈ 47 px; header ≈ 43 px, or more if labels wrap |
| gap between blocks | 28–40 px |
| chart image | width ÷ aspect ratio; at most ≈ 714 px tall under a heading |

If the estimate exceeds 864 px, cut words or split the slide. Never lower the type scale.

## Typesetting traps

`deck.py check` catches none of these except the one-word last line, so look for them when you
look at the rendered slides.

- **Capitals change symbols and units.** Kickers (`.kicker`) and table headers (`th`) are set in
  capitals by `text-transform`, which also capitalises every case-sensitive symbol or unit inside
  them: `n = 18` shows as `N = 18`, `k` as `K`, `ms` as `MS`, `kB` as `KB`, and a Greek `ε` turns
  into a Latin-looking `Ε`. Wrap such text in `<span class="nocase">…</span>`, which keeps it as
  written (`<p class="kicker">Results · <span class="nocase">n = 18, ε = 0.10</span></p>`), or keep
  it out of the kicker and put it in the caption.
- **Arrows and `=` need non-breaking spaces.** Chrome breaks at any space, so a line can start with
  `= 0.10` or end on `→`. Bind the expression: `ε&nbsp;=&nbsp;0.10`, `n&nbsp;=&nbsp;323`,
  `0.476&nbsp;→&nbsp;0.719`.
- **A separator binds to the item before it.** A line of items joined by ` · ` (a setting line,
  a context line) can break before a dot, and the next line then starts with `·`. Write
  `18 scenes&nbsp;· 20 splits`: the line can break only after the dot.
- **Ranges and hyphenated terms need a nowrap span.** Chrome also breaks after an en dash or a
  hyphen, where `&nbsp;` cannot help because there is no space: a range splits as `86–` / `91%`, a
  term as `per-` / `count` or `top-` / `1`. Wrap them: `<span style="white-space:nowrap">86–91%</span>`.
  A word joiner after the dash (`86–&#8288;91%`) also prevents the break, but `numtrace.py` then
  reads `86` as a plain number instead of a percentage, so prefer the span.
- **`.mono` shrinks.** `.mono` and `code` are `0.9em` of their parent: `<p class="meta mono">`
  renders at 14 px because `.mono` overrides `.meta`'s size. Put the mono text in an inner span:
  `<p class="cap"><span class="mono">in&nbsp;→ out</span></p>`. A `.math` formula inside `.mono`
  shrinks the same way, to 0.9 of the text beside it: give a TeX symbol its own `.math` span
  instead.
- **A formula does not follow bold.** A typeset formula is glyph paths in the fontset's regular
  weight, so inside a bold title or a `<b>` it stays regular beside bold words. In a title, write a
  plain Greek letter in Unicode (`λ` is set bold with the title) and keep TeX for notation the
  title cannot do without.
- **Tabular figures** are on only for `td.n` cells, `.num` and `.big`. Inter's tabular setting
  also widens hyphens (`top-1` reads `top - 1`), so do not add it to text.
- **Line breaking:** the theme sets `text-wrap: pretty` on every slide, which avoids most one-word
  last lines, and `text-wrap: balance` on `h1` and `h2`, so a title that must wrap splits evenly.
  `deck.py check` reports a one-word last line that remains (kind `widow`): cut or reword, or bind
  the last two words with `&nbsp;`.

## Lists and table status

- `ul.dash`: each item starts with an en dash on the column's left edge, and the text hangs 1 em
  in, so wrapped lines align under the first word. The dash sits inside the column, not in the
  margin, so the checks see it as part of the item. `ul.plain` has no markers. The theme styles
  only these two: a bare `<ul>` gets the browser's round bullets and indent.
- Table cells: `td.n` (right-aligned tabular numbers; `th.n` for its header), `tr.focus` (the focal
  method's row, tinted), `tr.total` (a ruled total row). A text column right after a `.n` column
  starts 40 px after the numbers instead of 24 (the theme pads it 28 px on the left), so a count
  and the word after it ("1", "act") read as two columns, not as "1 act".
- Table status, by the fixed colour meanings: `td.bad` (red, below target), `td.good` (green, meets
  target), `td.amber` (amber, a caveat: provisional, small n, not comparable). To mark a whole row,
  put `tr.bad` or `tr.amber` on it and `class="lab"` on its label cell: only that label cell turns
  red or amber and semibold, so the numbers stay readable.

## Math

- `<span class="math">TeX</span>` (inline) and `<div class="math-display">TeX</div>` (its own line,
  at 48 px) are typeset at build time into SVG by `scripts/mathsvg.py`, with matplotlib's mathtext:
  no LaTeX install, a subset of LaTeX (no `\begin{align}`; one formula per element).
- `deck.json` `"math_fontset"` picks the formula font for the whole deck:
  - `cm`: Computer Modern, the default; the explainer decks this theme grew from used it;
  - `stix`: a Times-like serif;
  - `stixsans`: STIX sans-serif;
  - `dejavusans`, `dejavuserif`: DejaVu.

  Any other value stops the build and lists these five. matplotlib's sixth value, `custom`, is not
  offered: it takes its fonts from settings a deck cannot pass.
- **An inline symbol next to Inter.** A `.math` span is set at the font size of the text around
  it, but the fontsets' lower-case letters are not as tall as Inter's. Measured as the height of
  `x` in em (matplotlib's glyph paths; Inter from its font file):

  | font | `x` height |
  |---|---|
  | Inter (the theme's text) | 0.55 |
  | `dejavusans` | 0.55 |
  | `dejavuserif` | 0.52 |
  | `stixsans` | 0.46 |
  | `cm`, `stix` | 0.45 |

  So with `cm` an inline `k` or `x` reads about 18% smaller than the words beside it. A deck whose
  formulas sit mostly inside sentences (symbol lists, definitions) reads evenly with `dejavusans`;
  a deck of display equations can keep `cm`. The fontset applies to the whole deck.
- matplotlib needs a writable config and cache folder. When `MPLCONFIGDIR` is unset and the home
  folder is read-only, `mathsvg.py` (and so the build) and `charts.py` point matplotlib at a
  per-user folder in the system temp dir, so nothing needs setting by hand. An `MPLCONFIGDIR` that
  is set is used as it is.
