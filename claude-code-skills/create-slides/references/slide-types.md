# Slide types

Eighteen templates live in `templates/technical-swiss/slides/`, one per type: 01–16 for any deck,
17 and 18 for the paper explainer (`paper-explainer.md`), which `scripts/explainer.py` fills. This
page helps you pick one. `template-catalog.md` has a page per template: its anatomy image, capacity, binding rules
and a do/don't pair. The comment at the top of each template file gives its capacity limits and is
authoritative.

To see them:

- `references/templates/gallery.png`: all 18 clean renders on one sheet, the two paper-explainer
  templates included (the theme's own `templates/technical-swiss/gallery.png` shows the 16 general
  templates);
- `references/templates/<id>.png`: one template, clean, 1920 × 1080;
- `references/templates/<id>-anatomy.png`: the same with the grid, margins, footer band and
  labelled regions drawn on it.

`python3 scripts/anatomy.py`, run from the skill folder, regenerates all three from the templates.

| template | use it for | layout | anatomy |
|---|---|---|---|
| `01-main-title` | the cover | title block 7 columns, one visual 5 columns, context line under a rule | [01](templates/01-main-title-anatomy.png) |
| `02-section-title` | opening each part of a deck with three or more parts, one per part, or none (`slide-rules.md` §4) | section number, large title, one-line subtitle, contents line | [02](templates/02-section-title-anatomy.png) |
| `03-main-content` | one finding carried by 2–4 points | points 8 columns, side note 4 | [03](templates/03-main-content-anatomy.png) |
| `04-text-visual` | a diagram or plot explained in a few statements | text 5 columns, visual 7 (or 4 + 8) | [04](templates/04-text-visual-anatomy.png) |
| `05-text-images` | a pair of photos or screenshots with commentary | text 4 columns, two images of 4 | [05](templates/05-text-images-anatomy.png) |
| `06-full-figure` | a figure that must be read in detail | compact heading and reading 3 columns, figure 9 | [06](templates/06-full-figure-anatomy.png) |
| `07-pipeline` | an architecture, process or data flow | 4–5 equal nodes joined by thin arrows; optional panel opening the focal stage | [07](templates/07-pipeline-anatomy.png) |
| `08-equation` | a method defined by equations | equation panel, reading and condition 8 columns, symbols 4 | [08](templates/08-equation-anatomy.png) |
| `09-chart` | one result chart | chart 7 columns, finding and two called-out values 5 (or 8 + 4) | [09](templates/09-chart-anatomy.png) |
| `10-table` | numbers compared across conditions | table 9 columns, reading 3 (or table across 12) | [10](templates/10-table-anatomy.png) |
| `11-image-compare` | the same view under two or three conditions | three images of 4 columns (or two of 6), label above, caption below | [11](templates/11-image-compare-anatomy.png) |
| `12-text-dominant` | an argument in words | three units of 4 columns on 2 px rules (or two of 6) | [12](templates/12-text-dominant-anatomy.png) |
| `13-key-number` | one result that carries the deck | the number at 240 px in 7 columns, comparison and meaning in 5 | [13](templates/13-key-number-anatomy.png) |
| `14-comparison` | two or three alternatives on the same attributes | attribute column and alternatives of 3 columns each; focal last, in blue | [14](templates/14-comparison-anatomy.png) |
| `15-statement` | one conclusion or quotation | a 72 px statement in 9 columns, attribution in 3; use rarely | [15](templates/15-statement-anatomy.png) |
| `16-summary` | closing | numbered statements 8 columns, next steps 4 | [16](templates/16-summary-anatomy.png) |
| `17-paper-idea` | paper explainer, slide 1: problem, idea, the paper's figure | text 6 columns, figure 6, takeaway bar across 12 | [17](templates/17-paper-idea-anatomy.png) |
| `18-paper-method` | paper explainer, slide 2: method, certificate, results, limits | two columns of 6, "For us." bar across 12 | [18](templates/18-paper-method-anatomy.png) |

## Choosing

- **Numbers across conditions:** `10-table`. When the shape matters more than the values, use
  `09-chart`, with the table in the notes or on the next slide.
- **One number that carries the deck:** `13-key-number`, once or twice per deck, not on every
  slide.
- **Two numbers that make one claim:** no template yet. `template-authoring.md` builds one, the
  two-metric template, as its worked example, ready to adopt.
- **A method:** `08-equation` for its definition, `07-pipeline` for its flow.
- **Explaining other people's papers:** `17-paper-idea` and `18-paper-method`, two slides per paper,
  built with `scripts/explainer.py` (`paper-explainer.md`), not by hand.
- **Parts of a deck:** `02-section-title` once per part, all parts or none, and only with three or
  more parts unless the user asks. Without them, numbered kickers ("02 · Camera sets") mark the
  parts. A one-part deck has neither (`slide-rules.md` §4).
- **Pictures of the data:** `05-text-images` for one scene, `11-image-compare` for conditions side
  by side.
- **Before and after, or method A against method B:** `14-comparison`, or a dumbbell chart in
  `09-chart` (see `charts.md`).
- **Nothing fits:** do not stretch a template past its comment's variants. Build a new one with
  `template-authoring.md`.

## Rules shared by all types

- **Heading.** The kicker and the title open every slide except the cover and section slides. The
  kicker is a short uppercase label with the part number and the condition, for example
  "05 · Results · ε = 0.10". It is set in capitals, so a symbol or unit whose case matters (`n`,
  `ms`, `ε`) goes in `<span class="nocase">` (`technical-swiss.md`, typesetting traps). The title
  states the finding.
- **Footer.** The build adds it: the page number only, unless the user asks for a label, and never
  a date. Don't write it into the slide.
- **Images.** Images live in `assets/`, use `object-fit: contain`, and are sized to their slot. A
  label set on an image carries `data-layer="overlay"`.
- **Regions.** In templates 01–16 each slot carries `data-role` and `data-cap`, which `anatomy.py`
  reads. Keep them when filling a template; they do not change the render. Templates 17 and 18 mark
  their slots with `data-slot` for `explainer.py` instead.
- **Lists and table status.** Lists are `ul.dash` (an en dash on the column edge, text hanging
  1 em) or `ul.plain`. Table cells take `td.bad`, `td.good` or `td.amber`; a whole row takes
  `tr.bad` or `tr.amber` with `td.lab` on its label cell (`technical-swiss.md`).
- **Speaker notes.** Sources, commands and long caveats go in `<aside class="notes">`, as the last
  child of the section.
- **Large numbers.** A number set at 64 px or more (`.num`, `.big`) sits above its text, or in a column measured to fit
  its widest value with slack (`slide-rules.md` §6).
