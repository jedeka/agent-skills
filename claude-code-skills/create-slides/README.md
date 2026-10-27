# create-slides

An agent skill that turns content into a slide deck in the technical-swiss design: a 12-column Swiss
grid that still carries the numbers, conditions and caveats a technical audience needs. A deck is
written as one HTML `<section>` per slide and exported to PDF, PPTX or a claude.ai Slides artifact.
Before a deck ships, every slide is rendered in headless Chrome and checked on screen and in the
printed PDF for overflow, text past its box and colliding objects. The workflow then has the agent
look at every slide.

It builds two kinds of deck:

- **standard decks** (results, methods, systems, arguments) from 16 slide templates: title,
  section, main content, text and visual, figure, pipeline, equation, chart, table, key number,
  comparison, summary and more;
- **paper explainers**, two slides per research paper, assembled from one JSON file per paper. Every
  result number must sit in a span quoted from the paper, found on the cited page or the page next
  to it.

`SKILL.md` is the agent's entry point. It covers the deck types, setup, the workflow and an index of
every file.

## What is inside

| folder | contents |
|---|---|
| `SKILL.md` | what an agent reads first |
| `references/` | the slide rules, the verification pipeline, the template catalog and authoring guide, the design system, chart rules, the paper-explainer guide |
| `references/templates/` | every template rendered clean and with its anatomy (grid, margins, labelled regions with capacities), a gallery sheet, the R7 and print-check cases, a worked new template |
| `references/example-scenarios/`, `references/example-explainer/` | two finished decks, with their slide files and outputs |
| `templates/technical-swiss/` | the stylesheet, 18 slide templates, fonts (with licences) and placeholder images |
| `scripts/` | `setup.sh`, the deck engine `deck.py`, the PDF checker, the number trace, the claude.ai Slides exporter, math typesetting, contact sheets, anatomy renders, charts, and the paper-explainer tools |

Start with `references/templates/gallery.png` to see all 18 templates on one sheet
(`templates/technical-swiss/gallery.png` shows the 16 general ones).

## Install

The scripts find their own files relative to themselves, so the folder works wherever it is put.

For Claude Code, for every project:

```
cp -r create-slides ~/.claude/skills/
```

For one project only, copy it to `<project>/.claude/skills/` instead. If you downloaded a zip,
unpack it so that the `create-slides/` folder, the one holding `SKILL.md`, sits there. Other agents
can use it from any folder: point them at `SKILL.md`.

Then build the Python environment once:

```
bash ~/.claude/skills/create-slides/scripts/setup.sh
```

This creates a venv in `~/.local/share/create-slides/venv` (under `$XDG_DATA_HOME` when that is
set) with playwright, pymupdf, matplotlib, pillow and python-pptx. If no Chrome or Chromium is
found, it also downloads Playwright's headless Chromium. `--venv <path>` and `--browsers <path>` put
them elsewhere. On Linux the venv took 551 MB and Chromium 278 MB. When the home disk is small, also
point `PIP_CACHE_DIR` and `TMPDIR` at a disk with room. The script ends by printing the lines to run
in later shells. matplotlib needs no setting: with a read-only home the scripts give it a cache
folder in the system temp dir.

Check that everything works:

```
source ~/.local/share/create-slides/venv/bin/activate
python ~/.claude/skills/create-slides/scripts/deck.py selftest /path/to/empty-dir
```

It ends with `selftest passed: 7 of 7 as expected`.

## Quick start

Ask the agent for slides ("turn these results into a deck"), or in Claude Code type
`/create-slides <file or topic>`. By hand:

```
S=~/.claude/skills/create-slides/scripts
python $S/deck.py new mydeck --title "What the run shows" --slides main-title,main-content,table,summary
# fill in mydeck/slides/*.html, replacing every [bracketed placeholder]
python $S/deck.py text mydeck --prose     # face text and notes, for the writing passes
python $S/deck.py check mydeck            # fit and collisions on screen
python $S/deck.py pdf mydeck              # PDF, then overlap checks on the printed PDF
python $S/deck.py png mydeck && python $S/contact_sheet.py mydeck    # look at every slide
python $S/numtrace.py mydeck results.csv  # every number on the slides found in its source
python $S/deck.py pptx mydeck
```

Outputs land in `mydeck/build/`.

## Licences

The skill is MIT, as declared in `SKILL.md`. The fonts Inter and JetBrains Mono are under the SIL
Open Font License; the texts are in `templates/technical-swiss/fonts/LICENSES/`. The example
explainer's `sources/` folder holds text extracted from the two arXiv papers it explains, kept for
offline quote checks and number traces; those papers' own licences apply to it.
