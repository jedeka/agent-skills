# Example: a two-paper explainer

A finished paper explainer, built end to end with `scripts/explainer.py` (guide:
`references/paper-explainer.md`). It explains two papers for a reader building a robot that must decide
whether to grasp or to ask first. Copy its patterns, not its content.

| file | what |
|---|---|
| `explainer.json` | the deck config: title, subtitle, two sections, a four-term glossary, the "For us" label |
| `papers/ren23knowno.json` | KnowNo: Robots That Ask For Help (CoRL 2023, arXiv 2307.01928v2) |
| `papers/angelopoulos22crc.json` | Conformal Risk Control (preprint 2022, arXiv 2208.02814v4) |
| `figs/` | each paper's figure panel, cropped with `figcrop.py` at `--dpi 600` from the page and box in its JSON |
| `sources/` | page-marked text of each paper, written by `quotecheck.py text` from the pinned arXiv PDF; the quote check and `numtrace.py` read them |
| `conformal-guarantees-for-robots-that-ask.pdf` | the built deck, 9 pages |
| `contact-sheet.png` | all 9 slides on one sheet |

The PDFs are not copied here; each JSON names its pinned arXiv URL. The texts in `sources/` are enough to
check the quotes and trace the numbers offline. A new crop downloads the PDF once into the cache.

## Rebuild

From the skill folder, with the output in a scratch folder outside the skill:

```
python3 scripts/explainer.py check references/example-explainer --out <scratch>/example-explainer
python3 scripts/explainer.py build references/example-explainer --sheet --out <scratch>/example-explainer
python3 scripts/numtrace.py <scratch>/example-explainer/deck references/example-explainer/sources/*.txt --allow 0-10
```

The build of the files here printed `layout OK: 9 slides fit; no collisions`, `PDF OK: 9 pages, 16:9;
186 text lines, 2 images and 6 filled panels checked: no overlaps, nothing in the footer band`, `links
OK: 4 contents rows land on their pages; every paper slide links back` and `explainer OK`. Of the 186
text lines, 27 are the en dashes that open list items, which the PDF holds as separate lines.

The number trace read 112 numbers: 59 found in the papers' text, 45 allowed (0 to 10: section and
slide numbers, small counts), 8 untraced, and exited 1. The 8 are the two figure boxes that
explainer.py writes into the notes ("box [72, 262, 304, 374] (PDF points)"): crop coordinates from the
JSON, not claims about the paper. With `--faces-only` all 60 numbers on the faces trace or are allowed,
exit 0.

## Slides

| page | slide | built from |
|---|---|---|
| 1 | cover | `explainer.json` title, subtitle; the context line is the default |
| 2 | how to read | the two slide layouts, the glossary, a key to blue links, amber rules and page tags |
| 3 | contents | one row per section and per paper, each a link |
| 4, 7 | section dividers | each section's name and note, the papers as links |
| 5–6 | KnowNo | templates 17 and 18 |
| 8–9 | Conformal risk control | templates 17 and 18 |

## What it demonstrates

- **Certifies states the theorem, Limits states the gap.** KnowNo's table bounds "the prediction set
  holds no correct option", with probability 1 − δ over calibration. Its own Table 2 (p.8) reports task
  success 0.76 against the 0.85 target, so that gap is a limit and the slide's title: "The guarantee
  covers the plan, not the outcome". The paper names low-level control as the cause (p.23); the notes
  carry that line.
- **The qualifier stays.** Conformal risk control's guarantee is "in expectation, not with high
  probability" (p.2), and the figure shows calibration splits above α = 0.1.
- **Every result number sits in its quote.** "plan success 0.87, help rate 0.67" quotes the table row
  "KNOWNO PaLM-2L 0.85 0.87 0.76 2.22 0.67" (p.8). The quotes are in slide 2's speaker notes.
- **Assumptions are a row.** KnowNo assumes i.i.d. scenarios and a human who answers correctly
  (pp.3, 5); conformal risk control assumes exchangeable data and a monotone, right-continuous loss (pp.2–3).
- **Venue only when stated.** KnowNo's arXiv listing says "Conference on Robot Learning (CoRL) 2023";
  the conformal-risk-control listing names no venue, so it reads "Preprint 2022", the year of its arXiv
  id.
- **Greek in Unicode, notation in math.** "α = 0.1" and "1 − ε" are typed, so digits in running text
  keep one font; the two formulas and KnowNo's `$1-\hat{q}$` (a hat needs math) are typeset.
- **One panel, when the whole figure is too small to read.** KnowNo's Fig. 2 has three panels; across
  the column's 860 px its 5 and 6.2 pt labels showed at 11 and 13 px. The slide crops the right
  panel's threshold and prediction set (page 3, box 372, 97 to 506, 182 pt), which the idea is about,
  and the caption names the full figure ("Fig. 2, right panel"). At 495 × 314 px the same labels show
  at 18 and 23 px (`paper-explainer.md`, step 5).
  Conformal risk control's Fig. 1 (the paper's page 6) holds a strip of polyp masks above two
  histograms, 472 pt wide; whole, at 598 px, its 6 pt axis labels showed at about 8 px. Slide 8 crops
  the bottom-left histogram, the false-negative rate over 1000 splits with α dashed (box 72, 262 to
  304, 374 pt), because it shows the guarantee holding in expectation with some splits above α. At
  793 × 383 px its 6 and 6.5 pt labels show at 21 and 22 px, and the caption names the panel
  ("Fig. 1, bottom left").
- **Figures sized by the title.** KnowNo's two-line title leaves its figure the 314 px box, which its
  1.58 : 1 crop fills by height. Conformal risk control's one-line title gives its 2.07 : 1 crop the
  taller box (383 px), which it also fills by height.
- **Short name dropped when it repeats the title** ("Conformal Risk Control"), kept when it differs
  ("KnowNo").
- **Cut to fit, not shrunk.** The first drafts ran up to 170 px over on slide 2. The check said how
  many lines to cut per column; the detail moved to `notes`.
