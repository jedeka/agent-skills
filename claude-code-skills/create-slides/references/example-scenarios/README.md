# Example deck: scenarios in an 80-scene run

A finished 15-slide technical-swiss deck, kept as the one-shot reference. It reports an evaluation:
a robot decides from camera images whether to grasp, ask or abstain, with conformal prediction
setting the threshold. Read it before writing a new deck. Copy the patterns, not the content.

Files:

- `deck.json`: title, theme and slide order. It has no footer label, so every footer is the page
  number only;
- `slides/<id>.html`: one `<section>` each, speaker notes in `<aside class="notes">`;
- `assets/`: one scene photo and three charts, all used;
- `build/`: the HTML viewer, PDF, PPTX and slide PNGs from `deck.py all` and `deck.py png`;
- `contact-sheet.png`: every slide on one sheet (`contact_sheet.py`), each tile labelled with its
  slide id and title.

## Slides and the template each uses

| # | slide id | template | what it shows |
|---|---|---|---|
| 1 | 01-cover | 01-main-title | title, subtitle, one line of scope; photo in the right half; no footer |
| 2 | 02-setup | 03-main-content | two ruled 6-column blocks: calibration vs test |
| 3 | 03-how-to-read | 10-table | column definitions (two columns, `table.lg`) |
| 4 | 04-instruction-types | 10-table | the ten kinds of instruction with an example each |
| 5 | 05-instruction-results | 10-table | numeric results, failure row in red, total row |
| 6 | 06-missing-box | 13-key-number | two red key numbers beside three ruled sentences |
| 7 | 07-vague-instructions | 04-text-visual | three sentences in 4 columns, chart in 8 |
| 8 | 08-look-by-instruction | 04-text-visual | same layout, before/after chart |
| 9 | 09-camera-sets | 10-table | definition table |
| 10 | 10-camera-results | 10-table | grouped header: two methods side by side |
| 11 | 11-look-by-camera | 04-text-visual | text plus chart |
| 12 | 12-before-after-look | 10-table | four rows; the focal method's rows in blue |
| 13 | 13-scene-pools | 10-table | definition table, caveat row in amber |
| 14 | 14-pool-results | 10-table | numeric results |
| 15 | 15-summary | 16-summary | four numbered findings in the order shown, next steps in the panel |

Not used here: 02-section-title, 05-text-images, 06-full-figure, 07-pipeline, 08-equation,
09-chart, 11-image-compare, 12-text-dominant, 14-comparison, 15-statement. The deck has four parts
and no section slides: numbered kickers (`01 · Instruction types` … `04 · Scene pools`) mark the
parts, which `slide-rules.md` §4 allows. Setup, how-to-read and summary carry unnumbered kickers.

## What it demonstrates

- **Titles state the finding** on every result slide: "A missing box is the most dangerous case",
  "The top camera alone is the weakest view", not "Results by camera". The summary's title is the
  deck's takeaway ("Act on full names; a missing box is the worst case"), not a label such as
  "What the scenarios show". Definition slides get a plain label ("Ten kinds of instruction"). The
  kicker above the title gives part and condition (`02 · Camera sets · ε = 0.10`), so the title
  does not have to.
- **Plain words, not codes.** The source report names the instruction kinds with level codes (L0
  to L4, such as "L4-fd robot side") and a policy column after its owner. The faces say "absent box", "left of, robot side" and "look first"; slide 4's notes
  keep the mapping to the source's codes for the presenter. All three charts were redrawn with
  `charts.py` at their 1155 × 704 px slot, from the run's results file, so the instruction charts'
  row labels match the tables.
- **One idea per slide.** Each table is followed by a finding slide that pulls out one number and
  its chart.
- **The summary follows template 16.** Four statements restate the findings of slides 5, 6, 7 and
  11, in that order, each with its number; the next-steps panel holds three actions taken from the
  deck itself (slides 6, 13 and 14), and the notes say where each came from.
- **Colour carries one meaning.** Red marks failure only: the absent-box row and the cells that
  fail (coverage 0.401, wrong grasp 25.6%), the weakest camera set, the key numbers on slide 6.
  Blue marks the focal method, the per-count threshold (group header on slide 10, rows on slide
  12). Amber marks the one caveat row, `tr.amber` with `td.lab` on slide 13 (dim / back-light: not
  a lighting result). Green is unused because no cell needed it. Everything else is ink and greys.
- **Tables are trimmed.** Results tables keep 8–11 columns and at most 11 rows. The source's n
  column moved to the speaker notes; its ε = 0.20 and after-the-look tables stayed in the source
  document, and their findings appear as charts (slides 7, 8, 11). Definition cells are shortened
  ("meant box (2 match)"). Numbers are right-aligned (`th.n`, `td.n`), with a ruled `tr.total`.
- **Numbers trace to a source file.** Every figure was computed by a script into a JSON file, and
  the original slides were filled from that file by placeholder, so they could not drift; each
  slide's notes name the section of the source report (`80-run-unique-scenario.md §1` …). The
  report is not shipped with the skill. `numtrace.py`, run against that report, its results JSON
  and the run's two other write-ups, traced 449 of the 450 numbers on the faces and in the notes.
  The one it could not trace is the threshold range "0.444 to 0.997" on slide 2: none of those
  files holds 0.444. It is kept as the deck had it, and flagged here.
- **Caveats live in the notes or a caption**, not in the title: the population of a table,
  the temperature used, why the lighting pools say nothing about lighting.
- **Inline style only for one-off sizes:** key numbers at 160 px (240 px overflows a 5-column
  block for "25.6%"), chart height 704 px, table column widths, the grouped header row.

## Left off on purpose

The source report contained a person's name (the owner of the decision policy, whose column is
"look first" here), the date of an earlier report, the id of an excluded scene, internal task,
decision and level codes, and a project codename in the cover kicker. None reach the slide faces;
the level codes appear only in the notes of slides 4, 6 and 7, mapped to the plain names. Scene
ids were also removed from asset file names (`scene-top.png`).

## Not in this deck

`slide-rules.md` §4 asks for a limits slide before the summary. This deck has none: its caveats
sit in captions and notes (slides 10, 13 and 14). A new deck should add one.

## Traps this deck hit

`.kicker` and table headers are set in capitals by the theme, which turns `ε` into `Ε` (it reads as
a Latin E). Slides 5, 10 and 14 wrap it as `<span class="nocase">ε</span>`.

A short expression such as `ε = 0.10` can break across lines at its spaces and leave `= 0.10`
alone at the start of a line. Bind it with non-breaking spaces: `ε&nbsp;=&nbsp;0.10`, and the same
for arrows and a label with its value (`<b>Full&nbsp;name</b>:&nbsp;0.851&nbsp;→&nbsp;0.931`,
slide 8).

Chrome also breaks after an en dash or a hyphen: a first build split `86–91%` and `21–31%` on
slide 7 and `per-count` on slide 11 across two lines. Each is now wrapped in
`<span style="white-space:nowrap">…</span>`. Looking at the slides found three more breaks, now
bound: "(18" alone at a line end on slide 2, and "left" / "of" in a quoted instruction on slides 13
and 14.

A title longer than the 50-character budget wraps. Slide 12's title first ran to 63 characters on
two lines; it was cut to 49 ("The look raises accuracy, grasps and wrong grasps") so it fits one.
The theme's `text-wrap: balance` would split a two-line title evenly, but one line is the rule.
