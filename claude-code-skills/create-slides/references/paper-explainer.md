# Paper explainer

A deck type that explains research papers two slides each, so a reader can learn a body of literature
quickly and trust every number on it.

- **Slide 1, the idea** (template `17-paper-idea`): the paper's title, problem, idea, its own figure
  with the page it came from, and a one-sentence takeaway.
- **Slide 2, how it works** (template `18-paper-method`): method, formula, what it measures, what it
  certifies, results with pages, limits, and what it means for the reader ("For us").

`scripts/explainer.py` builds the whole deck from one JSON file per paper. The deck runs: cover, how to
read, linked contents, then per section a divider (one even for a single section, since the contents
rows link to it) and each paper's two slides. Every number on a result line is checked against a
quoted span of the paper, on the cited page. The example in `references/example-explainer/` (two
papers, 9 slides) was built this way; copy its patterns.

Use it when the user asks to explain, survey or compare papers, to make a reading deck or a literature
explainer, or to turn a reading list into slides. For one paper inside an ordinary deck, the two
templates can also be used by hand with `deck.py new --slides paper-idea,paper-method`.

## Workflow

1. **Start the project** and fill in the deck config (fields below):
   ```
   python3 <skill>/scripts/explainer.py new <project> --title "Conformal guarantees for robots that ask"
   ```
2. **Add each paper.** This downloads the PDF (or reads a local one), writes its text with page marks to
   `sources/<key>.txt`, and writes a skeleton `papers/<key>.json`:
   ```
   python3 <skill>/scripts/explainer.py add <project> ren23knowno --pdf https://arxiv.org/pdf/2307.01928v2
   ```
   Pin the arXiv version (`v2`), so page numbers stay valid. The key names the file and the slide
   anchors; it never shows on a slide.
3. **Read the paper.** Read the whole text file, and look at the PDF pages that carry the key figure,
   the main theorem and the result tables. Write down each number you will use, with its page and the
   verbatim span that holds it.
4. **Write the JSON**, field by field (schema below). Write only what the paper states, or what follows
   from it in one visible step. Mark readings as readings ("suggests", "For us").
5. **Crop the figure** and look at the crop:
   ```
   python3 <skill>/scripts/figcrop.py find papers/<key>.json            # caption lines: Fig. N, Table N
   python3 <skill>/scripts/figcrop.py page papers/<key>.json 3          # page 3 on a 50 pt grid -> PNG
   python3 <skill>/scripts/figcrop.py crop papers/<key>.json 3 372 97 506 182 --dpi 600   # -> figs/<key>.jpg
   ```
   A caption usually sits under its figure, so `find` gives the figure's bottom edge. Read the box off
   the grid (red numbers are x, blue are y, in PDF points), crop, open the JPEG and adjust until nothing
   is cut and no body text is included. `crop` prints the `"figure"` entry to paste. Write the caption
   yourself.

   **Keep the figure's own text readable.** The figure is fitted into an 860 × 314 px box (860 × 383
   under a one-line title), so a figure of W × H points shows text of `size` points at about
   `size × 860 / W` px, or `size × 314 / H` when the box's height limits it. When that falls under
   about 20 px, crop the single panel the idea needs, and name the full figure in the caption
   ("Fig. 2, right panel: …"). Raise `--dpi` so the crop has about twice the pixels it is shown at:
   a 134 pt panel shown 495 px wide needs about 1000 px, so `--dpi 600`. PyMuPDF lists the text
   sizes on a page:
   ```
   python3 -c "import pymupdf,sys; [print(round(s['size'],1), s['text']) for b in pymupdf.open(sys.argv[1])[int(sys.argv[2])-1].get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]" paper.pdf 3
   ```
   In the example, KnowNo's Fig. 2 spans three panels across 402 pt, with labels of 5 and 6.2 pt: at
   the column's 860 px they showed at 11 and 13 px. The right panel's threshold and prediction set
   alone, 134 × 85 pt, fill the box's height at 495 × 314 px and show the same labels at 18 and
   23 px. A figure drawn as one raster image has no text to list: measure a letter on the `page`
   render instead.
6. **Check** one paper or all of them, fix what it reports, and look at both previews:
   ```
   python3 <skill>/scripts/explainer.py check <project> <key>
   ```
7. **Build** the deck and look at every page, rendered from the PDF itself. Then trace every
   number on the faces and in the notes to the papers' text:
   ```
   python3 <skill>/scripts/explainer.py build <project> --sheet
   python3 <skill>/scripts/numtrace.py <project>/build/deck <project>/sources/*.txt --allow 0-10
   ```
   The figure boxes that explainer.py writes into the notes ("box [72, 262, 304, 374] (PDF
   points)") are crop coordinates from the JSON, not claims, and stay untraced. Any other untraced
   number is copied wrong, not in the paper, or derived (save its arithmetic as a source:
   `verification.md`, step 6). On the example, the 8 untraced
   numbers of 112 are the two boxes' coordinates; `--faces-only` checks the faces alone and exits 0.
8. **Run the writing passes** on the slide text, which
   `python3 <skill>/scripts/deck.py text <project>/build/deck --prose`
   prints: `unslop` (no AI patterns), `presend` (stamp every number and claim against its source
   before sending), `simply-explain` (followable in one read). Fix the JSON, then rebuild.

Requirements: Chrome or Chromium (found as in `deck.py`); matplotlib for formulas; PyMuPDF for PDFs,
figure crops and the PDF checks; Pillow for figures. `scripts/setup.sh` installs them. Source URLs are
downloaded once into `$CREATE_SLIDES_CACHE`; when that is unset, into `~/.cache/create-slides`, or the
system temp folder when that is not writable.

## Project layout

```
<project>/
  explainer.json        the deck config
  papers/<key>.json     one paper each; files starting with "_" are skipped
  figs/<key>.jpg        figure crops (figcrop.py crop)
  sources/<key>.txt     page-marked text ("===== PAGE n =====" lines), written by add
  build/                written by check and build (or --out DIR):
    check/<key>-1.png, <key>-2.png      previews from check
    deck/                               the assembled deck: deck.json, slides/, assets/
    <title-slug>.pdf, contact-sheet.png the PDF (also in deck/build/) and, with --sheet, all slides
```

Paths inside a paper JSON are relative to the project folder. `build/deck/` is an ordinary deck folder:
`deck.py pptx` or `deck.py inline` work on it. It is regenerated on every build, so change the JSON
or the templates, not those slide files.

## The deck config: `explainer.json`

| field | limit | shows on | purpose |
|---|---|---|---|
| `title` | 60 | cover | the deck's subject, as a statement or a name |
| `label` | 30 | cover and divider kicker | default `Paper explainer` |
| `subtitle` | 90 | cover | who the papers are read for, in one sentence |
| `context` | 110 | cover, bottom line | default: "N papers in M sections, two slides each. Every result is quoted from its paper, with the page." |
| `sections` | name 40, note 130 | dividers, contents, eyebrows | `[{"name": ..., "note": ...}]`, in deck order; the note is the question the section answers |
| `glossary` | ≤ 6; term 24, meaning 90 | how-to-read slide | `[["term", "meaning"], ...]`: every term the slides use unexplained |
| `callout_label` | 16 | slide 2 bar | default `For us`; name the reader's side ("For the gate", "For our robot") |
| `show_authors` | — | slide 1 meta line | default `false`: author names go to the notes only |
| `papers` | — | — | optional list of keys: only these, in this order within each section |
| `footer` | — | footer | optional short label left of the page number; never a date (deck.py refuses one) |
| `math_fontset` | — | formulas | optional: `cm` (default), `stix`, `stixsans`, `dejavusans` or `dejavuserif` (`technical-swiss.md`, Math) |

Without `papers`, the order is: sections as listed, then within a section by the year in each venue,
then by short name. A paper whose section is not listed is left out, and build says so.

## The paper JSON: `papers/<key>.json`

Limits count characters as they will show; a `$math$` span counts its visible symbols. Each limit lets
one field fit on its own. Fields share a column, so the rendered check is what decides; see Budgets below.

| field | required | limit | shows on | rules |
|---|---|---|---|---|
| `key` | yes | 40 | nowhere | equals the file name; letters, digits, `-`, `_` |
| `short` | yes | 24 | slide 1 meta, slide 2 kicker, contents | the name people use for the method or paper |
| `title` | yes | 110, 2 lines | slide 1 title | verbatim; if longer, keep the main title and put the whole one in `full_title` |
| `full_title` | no | — | notes | the complete title when `title` is cut |
| `authors` | no | 60 on the face | notes (face only with `show_authors`) | as cited: "A. Ren, A. Dixit, …, et al." |
| `venue` | yes | 40 | slide 1 meta, contents | venue and year as the paper or its listing states them ("CoRL 2023"); "Preprint 2022" when none is stated |
| `arxiv` | no | 20 | slide 1 meta | the arXiv id without version |
| `url` | no | — | notes | landing page |
| `source` | yes | — | notes | `{"pdf": path or URL, "text": path or URL}`, at least one; the quote check reads `text` first |
| `section` | yes | — | eyebrow, contents | one of the config's section names |
| `tags` | no | ≤ 2, 28 each; eyebrow ≤ 80 | slide 1 eyebrow | short labels after the section: setting, family ("Hardware and simulation") |
| `problem` | yes | 180, ≈ 3 lines | slide 1 | what goes wrong without the paper, with a concrete case from the paper |
| `idea` | yes | 2–3 items, 110 each | slide 1 | the mechanism in plain words, one step per item |
| `figure` | no | caption 120, 2 lines | slide 1 | `{"file", "page", "box", "caption"}`: the paper's own figure; the caption says what to look at |
| `takeaway` | yes | 190, 2 lines | slide 1 bar | the one sentence to remember about the paper |
| `finding` | yes | 55, 1 line | slide 2 title | what the paper shows, stated as a finding |
| `method` | yes | 2–3 items, 110 each | slide 2 | what is computed from what |
| `formula` | no | fits 812 px at 48 px; `reads` 110 | slide 2 panel | `{"tex", "reads"}`: the central equation in mathtext, and what it says in words |
| `measures` | yes | 1–2 items, 70 each | slide 2 | each measure the results use: "Name: definition" |
| `certifies` | yes, or `null` | event 90, guarantee 60, level 60, assumes 70 | slide 2 table | see below; `null` drops the block |
| `results` | yes | 2–3 items, text 110 | slide 2 | `{"text", "quote", "page"}`: setting, number, comparison; the quote is verbatim from that page |
| `limits` | yes | 1–2 items, 110 each | slide 2, amber rule | what the results do not show, or what the guarantee does not cover |
| `for_us` | yes | 170 with the label | slide 2 bar | what the paper means for the reader's work: an inference, worded as one |
| `notes` | no | — | speaker notes of slide 2 | longer caveats, pages of side facts, what was left off the slide |

Writing rules for every field, from `slide-rules.md`:
- **No person names, dates, internal ids or file paths on the face.** The venue year is part of the
  citation. Authors, paths and URLs go to the notes, which explainer.py fills from `authors`, `source`,
  `url` and `figure`.
- **Numbers keep their conditions:** setting, population, n, level, unit ("Kitchen, PaLM-2L, target
  0.85: plan success 0.87"). A rate and its target never travel apart.
- **One name per thing,** expanded on first use or in the glossary ("conformal prediction", not "CP").
- **Greek letters and simple expressions in Unicode** (α = 0.1, 1 − ε, N = 400), so the digits match
  the text. Use `$…$` only for real notation: hats, subscripts, fractions (`$\hat{R}_n$`). Spaces
  around `=`, `≤`, `≥`, `<`, `>`, `±`, `×`, `≈`, `−` and after "Fig.", "Table", "Prop." and similar
  words are made non-breaking automatically.
- **Epistemic status shows in the wording.** Results are what the paper measured, stated flat. Limits
  and `for_us` are readings: write "suggests" or "for us" when a sentence goes beyond the paper.

## What "What it certifies" must and must not say

The table states the paper's formal guarantee, in the paper's own terms, as four rows. Optionally,
`quote` and `page` cite the theorem or the equation; the quote check verifies them.

| row | must say | example |
|---|---|---|
| Bounds (`event`) | the exact event or quantity the theorem bounds | "the prediction set holds no correct option" |
| Guarantee (`guarantee`) | the type: marginal coverage, coverage with probability 1 − δ over calibration (PAC), a bound in expectation, conditional coverage | "in expectation, not with high probability" |
| Level, n (`level`) | the nominal level and the calibration size used in the results shown, with δ when there is one | "1 − ε = 0.85 (kitchen); N = 400, δ = 0.01" |
| Assumes (`assumes`) | what the guarantee needs: exchangeable or i.i.d. data, monotone loss, accurate human answers, known shift weights | "exchangeable data; loss monotone and right-continuous in λ" |

It must not:
- **state a measured rate as the guarantee.** "Plan success 0.87" is a result; the guarantee is
  "coverage ≥ 0.85". Measured numbers go to Results.
- **widen the event.** A bound on the plan is not a bound on the physical outcome, nor on safety. When
  the paper's own numbers show the gap, put it in Limits (KnowNo: task success 0.76 at a 0.85 target).
- **drop the qualifier.** "Marginal", "in expectation" and "with probability 1 − δ" change what a reader
  may conclude about a single deployment.
- **borrow a guarantee from related work** or from the reader's project. A paper with no formal
  guarantee gets `"certifies": null`; its block is dropped, and Results and Limits carry the evidence.

## Budgets

Measured on the built example (the template comments hold the same numbers):

| slide | region | height | a line | holds |
|---|---|---|---|---|
| 1 | text column (problem, idea) | 426 px; 495 px under a one-line title | 36 px, ~58 characters | ≈ 7 lines; ≈ 9 under a one-line title |
| 1 | figure column | same | caption 38 px | figure ≤ 860 × 314 px (860 × 383 under a one-line title), caption ≤ 2 lines |
| 2 | left (method, formula, measures) | 539 px | 31 px, ~70 characters | ≈ 7 lines with a formula, ≈ 11 without |
| 2 | right (certifies, results, limits) | 539 px | 31 px | ≈ 3 lines of results and limits under four one-line certifies rows |

Fixed costs: a block label 65 px, the gap between blocks 24 px, the formula panel ≈ 122 px plus its
reading, a certifies row 43 px a line. Slide 2 sets its running text at 24 px, the theme's floor, one
step under slide 1's 28 px. It is the detail slide and holds six blocks and a formula. When a column
overflows, cut words or move a detail to `notes`; never shrink type or add a third slide.

## What the checks catch, and what they do not

`explainer.py check` and `build` report, per paper (messages copied from real runs):

| check | message, e.g. |
|---|---|
| fields, counts, limits, placeholders | `problem is 227 characters (max 180)`, `idea[1] is still a placeholder` |
| math | `formula is 1088 px wide at 48 px; its panel holds 812: shorten it (move a consequence into the reading)` |
| quote not on the cited page ±1 | `results[1].quote not on p.5 or its neighbours; it is on p.8` |
| quote on a neighbour page (passes) | `note: results[1].quote found on p.8, cited p.7: cite p.8` |
| number not in its quote | `results[0].text states 0.88, which its quote does not hold` |
| a region overflows | `slide 2: left column (method, formula, measures): 73 px too tall, about 3 lines (~216 characters)` |
| line limits | `slide 1: title takes 3 lines (at most 2)` |
| deck.py's checks | R7 collisions, text past its box, the footer band, type under 24 px, one-word last lines (`widow`) |

`build` adds deck.py's PDF export. Images are frozen at their screen size, then `pdfcheck.py` reads the
printed PDF. Last comes a link check: every contents row lands on its planned page, every paper slide
links back to the contents, and each planned page shows its paper's short name. Exit codes: 0 all
passed, 1 a check failed, 2 the run stopped (missing file, bad JSON, Chrome error).

They do not check that a paraphrase is faithful, that the right theorem was quoted, or that a "For us"
line is sound. A quote proves only that the span exists on that page. Read the paper, then run
`presend` on the slide text.

`quotecheck.py` also runs alone: `quotecheck.py papers/*.json`, or
`quotecheck.py --source <pdf|txt|URL> --page 8 "quoted span"`. `quotecheck.py text <pdf|URL> --out f.txt`
writes page-marked text from any PDF.

## Changing the layout

The two templates are the layout's source. explainer.py fills them through attributes, so they can
be edited like any other template, as long as these stay:

- `data-slot="name"`: an element explainer.py fills: `title`, `problem`, `idea` (a list whose first
  `<li>` is repeated per item), `figure`, `figure-img`, `caption`, `figure-page`, `takeaway`, `notes`
  on 17; `short`, `finding`, `method`, `formula`, `tex`, `reads`, `measures`, `certifies`, `event`,
  `guarantee`, `level`, `assumes`, `results` (its `<li>` holds the sub-slots `text` and `page`),
  `limits`, `callout`, `for_us`, `notes` on 18; `section` on both (gets the `id`); `eyebrow`, `cite`,
  `short-sep`, `text-col` on 17.
- `data-fit="name"`: a region whose children must fit inside it; the check reports the overflow in
  px, lines and characters. Give the row `flex:1;min-height:0` so the region's height is fixed.
- `data-lines="N"`: the most lines an element may take.
- `data-box="WxH"` (and `data-box-1` for one-line titles) on the figure `<img>`: the largest figure
  size. Measure the region after a change and set it from the measurement.

After an edit, rebuild the example (`explainer.py build references/example-explainer --sheet --out
<scratch>`), look at every page, and update the capacity numbers in the template comment and in the
Budgets table above from a measurement, not an estimate.
