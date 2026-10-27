---
name: create-slides
description: Builds slide decks from content the user points at (chat, documents, result tables, notes, research papers) as HTML in the technical-swiss design, a 12-column Swiss grid that keeps full technical detail, and exports them to PDF, PPTX or a claude.ai Slides artifact. Use when the user asks for slides, a deck, a presentation, a PPT or PPTX, PDF slides, "turn this into slides", a paper explainer or reading deck that explains research papers, or a deck restyled to this design. Standard decks are built from 16 slide templates, paper explainers from two more. Every slide is rendered in headless Chrome and checked for overflow and colliding objects, on screen and again in the printed PDF. Every number traces to its source. Names, dates, internal ids and file paths stay off the slide faces, and the footer is the page number only.
license: MIT
user-invocable: true
argument-hint: "<what to turn into slides: a file, a folder, papers, 'the last answer'> [--out <deck_dir>] [--formats pdf,pptx,slides]"
metadata:
  version: "2.0.0"
---

# create-slides

Turns the content the user names into a deck that is technically complete, clean on the grid, and
true to its sources. Every content slide starts from a template. Every number traces to a source.
Every slide is rendered, machine-checked and looked at before the deck ships.

`<skill>` below is this folder (the one holding this file). `<deck>` is a deck folder. All scripts
find their own files relative to themselves, so run them from any directory.

## 1. Pick the deck type

| type | pick it when | built with | guide |
|---|---|---|---|
| standard deck | results, a method, a system, an argument: anything except explaining other people's papers | `scripts/deck.py` and templates 01–16 | §3 below |
| paper explainer | the user wants papers explained, surveyed or compared: a reading deck, two slides per paper | `scripts/explainer.py` and templates 17–18 | `references/paper-explainer.md` |
| claude.ai Slides export | the finished deck should live as a claude.ai Slides artifact (a link to present, page through, comment on) | either deck above, then `deck.py inline` | §5 below |

Defaults, unless the user says otherwise:

| setting | default |
|---|---|
| deck folder | a new folder named after the deck in the user's working directory (`--out` overrides), never inside `<skill>` |
| design | `technical-swiss` (`templates/technical-swiss/`) |
| exports | HTML viewer, PDF and PPTX (`--formats` picks; `slides` adds the claude.ai Slides export) |
| footer | the page number only. A short label only when the user asks for one, never a date |
| slide faces | no person names, dates, internal ids, file paths, codenames, logos or decoration |
| language | the user's |

## 2. Setup

```
bash <skill>/scripts/setup.sh                                   # venv in ${XDG_DATA_HOME:-~/.local/share}/create-slides/venv
bash <skill>/scripts/setup.sh --venv <path> --browsers <path>   # both somewhere with room
```

It installs playwright, pymupdf, matplotlib, pillow and python-pptx in a venv. It also downloads
Playwright's headless Chromium unless a Chrome or Chromium is found already. A second run installs
nothing new. It ends by printing the lines to run in later shells:

- `source <venv>/bin/activate`;
- `export PLAYWRIGHT_BROWSERS_PATH=...` when `--browsers` was given.

matplotlib needs nothing set by hand: when the home folder is read-only and `MPLCONFIGDIR` is
unset, the scripts point matplotlib at a per-user folder in the system temp dir.

`python3` below means the venv's python. Confirm the checks work once:
`python3 <skill>/scripts/deck.py selftest <empty dir>` ends with `selftest passed: 7 of 7 as expected`.

Chrome is found by `--chrome PATH`, else `$CHROME_PATH`, else Chrome, Chromium, Edge or
chrome-headless-shell on `PATH`, else a Playwright browser cache. Without the venv, `deck.py new`,
`build`, `check` and `png` still run on the standard library plus Chrome; math needs matplotlib.

## 3. Workflow: standard deck

Read `references/slide-rules.md` before the first slide. It holds the user's rules and the reason for
each. Then follow these steps in order.

1. **Read the content.** Read every source the deck draws on in full: the conversation, documents,
   tables, result files. If the scope, the audience or what to leave out is unclear, ask once. An
   agent that cannot ask (a subagent) proceeds on the most likely reading, marks every inference as
   one in the ledger and the notes, and lists those inferences in its report.
2. **Content ledger.** Before any slide exists, write `<deck>/ledger.md`, a Markdown table with one
   row per claim, number or caveat and these columns:
   - `item`: the claim, number or caveat;
   - `source`: the file and location (section, table, line) that holds it;
   - `conditions`: population, n, unit, threshold;
   - `status`: measured, inference, hypothesis or illustrative (`slide-rules.md` §2);
   - `slide`: where it appears, filled in at step 3.

   Every number needs a source. A number computed from source numbers (a sum, a ratio, `n + 1`) is
   derived: run the arithmetic, save the command with its printed output as
   `<deck>/derivations.txt`, and name that file as its source; it keeps the status of its inputs. A
   claim no source states either goes, or stays as an inference or a hypothesis and is labelled as
   one on the slide or in the notes, such as a standard definition the input does not give.
3. **Outline.** Write the slide titles first. One idea per slide; each title states a finding, in
   one line of about 50 characters, the summary's title included. Follow the deck structure in
   `slide-rules.md` §4: cover, how to read, the parts, limits, summary with next steps. Section
   slides come one per part or not at all, only with three or more parts unless the user asks; a
   request for section slides gives every part one. Without a request, a one-part deck has none
   and no part numbers in its kickers. The cover, how to read, limits and summary stand outside
   the parts. The finished examples show the patterns: `references/example-scenarios/` is a
   15-slide standard deck, `references/example-explainer/` a 9-slide paper explainer.
4. **Templates.** For each slide, pick a type with `references/slide-types.md`. Read its page in
   `references/template-catalog.md` and look at `references/templates/<id>-anatomy.png`, which shows
   the grid columns and every region with its capacity. Then scaffold the deck:
   ```
   python3 <skill>/scripts/deck.py new <deck> --title "<title>" --slides main-title,main-content,table,summary
   ```
   Types are named without their numbers; an unknown name prints the list. A type may repeat. You
   can rename the slide files afterwards, as long as `deck.json` "slides" lists the same ids.
   `new` also copies every placeholder image the chosen templates show into `<deck>/assets/`
   (`placeholder-cover.png` for the cover, and so on). Replace each with the real image, or delete
   it with its slot: `check` warns about an image in `assets/` that no slide uses.
5. **Write.**
   - Replace every `[bracketed placeholder]` within the capacity in the template's leading comment.
     That comment is copied into the slide and is authoritative.
     `grep -n '\[[^]]*\]' <deck>/slides/*.html` lists the brackets left; each one must be real
     content, such as an interval, or gone.
   - Use the theme's classes for type, colour and spacing; never an inline colour. An inline style
     is for a one-off size or position, as the templates and examples use it: an image's measured
     width and height, a table column's width, `margin-top:auto` to pin a line to its box's bottom,
     `white-space:nowrap`, a key number set smaller to fit a narrower column. Never shrink body
     text that way. Keep the `data-role` and `data-cap` attributes.
   - Put images in `<deck>/assets/`. Draw charts with `scripts/charts.py` at their slot's pixel size,
     from the same data as the tables (`references/charts.md`).
   - Write math as `<span class="math">TeX</span>` or `<div class="math-display">TeX</div>`. The build
     typesets it (`scripts/mathsvg.py`) and warns about TeX left outside them (`s_i`, `\alpha`). Do
     not nest a formula in `.mono`: it renders at 0.9 em, smaller than the text beside it. A formula
     stays regular weight inside bold text, so write a plain Greek letter in a title as Unicode.
     `deck.json` `"math_fontset"` picks the formula font: `cm` (default), `stix`, `stixsans`,
     `dejavusans` or `dejavuserif`. The lower-case letters of `cm`, `stix` and `stixsans` stand
     0.45–0.47 em tall against Inter's 0.55, so an inline symbol reads about 18% smaller than the
     text beside it; `dejavusans` matches Inter (`technical-swiss.md`, Math).
   - Bind what must not break: `ε&nbsp;=&nbsp;0.10` and `0.476&nbsp;→&nbsp;0.719` with
     non-breaking spaces, and `<span style="white-space:nowrap">86–91%</span>` for ranges and
     hyphenated terms, because Chrome breaks lines after a dash or hyphen. In a line of items joined
     by `·`, bind each dot to the item before it (`18 scenes&nbsp;· 20 splits`), so a wrapped line
     never starts with a dot.
   - Kickers and table headers are set in capitals, which turns `n` into `N`, `ms` into `MS` and
     `ε` into `Ε`: wrap such symbols and units in `<span class="nocase">` (`technical-swiss.md`,
     typesetting traps).
   - Lists are `ul.dash` (an en dash on the column edge, the text hanging 1 em in) or `ul.plain`.
     Mark table status with `td.bad`, `td.good` or `td.amber`, or a whole row with `tr.bad` or
     `tr.amber` plus `td.lab` on its label cell.
   - Set a number of 64 px or more above its text, or in a column measured to fit its widest value
     with slack (`slide-rules.md` §6).
   - Mark a label placed on an image with `data-layer="overlay"`.
   - Put sources, commands, paths and long caveats in `<aside class="notes">`, the section's last
     child.
6. **Writing passes** on the slide text and the notes, which
   `python3 <skill>/scripts/deck.py text <deck> --prose` prints slide by slide (face, then notes),
   in the case written and with a blank line after every block, so a checker reads a kicker as
   words, not acronyms, and never joins a title and a caption into one sentence:
   **unslop** (removes AI patterns), **presend** (stamps every number and claim against evidence
   obtained now), **simply-explain** (each slide followable in one read). Use the skills where
   installed; otherwise do the passes by hand from `slide-rules.md` §9. Unslop flags on the summary
   statements (they restate findings, as §4 requires) and on a section slide's contents line are
   expected: keep those lines. Then read the faces as the audience sees them, capitals included
   (`deck.py text <deck>`, without `--prose`), and run the face scan in `references/verification.md`
   (step 2) for years and paths left on slide faces.
7. **Build and check:**
   ```
   python3 <skill>/scripts/deck.py check <deck>
   ```
   It builds `<deck>/build/<slug>.html` and renders every slide at 1920 × 1080. It reports boxes
   leaving the content area, text past its box, every pair of colliding objects, content in the
   footer band, missing images, type under 24 px and one-word last lines, and exits 1 on any of them
   (`verification.md` explains each kind). It also warns, without failing, about an image in
   `assets/` that no slide uses: delete it or use it, since `build/` ships it. Fix problems by
   cutting words, re-laying out on the grid or splitting the slide. Never shrink type to fit.
8. **PDF and pdfcheck:**
   ```
   python3 <skill>/scripts/deck.py pdf <deck>
   ```
   It freezes every image and SVG at its checked screen size and prints with Chrome. Then
   `pdfcheck.py` reads the PDF itself for text over text or images, text or images running into a
   filled panel's edge, and content in the footer band. It must print `PDF OK`. Never print from a
   browser's print dialog.
9. **Look at every slide.** Render the slides and tile them on one sheet:
   ```
   python3 <skill>/scripts/deck.py png <deck>
   python3 <skill>/scripts/contact_sheet.py <deck>
   ```
   Look at `<deck>/build/contact-sheet.png` (each tile labelled with its slide id and first heading),
   then open every `<deck>/build/png/slide-NN.png`, not a sample. Look for edges off the grid,
   uneven spacing, an expression broken across lines (`86–` / `91%`) or a line starting with `·`,
   a symbol capitalised by a kicker (`N` for `n`), raw TeX or a formula smaller than the text
   beside it, a cramped or empty column, and labels colliding inside a chart image (the check sees
   a chart as one image).
   `python3 <skill>/scripts/anatomy.py --deck <deck>` draws the grid over each slide when alignment is
   in doubt. Also look at the PDF pages. An agent that cannot open a PDF can render its pages to PNG:
   ```
   python3 -c "import pymupdf,sys; [p.get_pixmap(dpi=96).save(f'{sys.argv[2]}/page-{p.number+1:02d}.png') for p in pymupdf.open(sys.argv[1])]" <deck>/build/<slug>.pdf <existing dir>
   ```
10. **Number trace.** Compare every number on the slides with the ledger's sources:
    ```
    python3 <skill>/scripts/numtrace.py <deck> <source files> --allow 0-10
    ```
    The sources are the files the ledger names, `derivations.txt` included, never the ledger
    itself. It lists every number on the faces and in the notes that no source holds, as the same
    value, rounded once from a longer one, or as a percentage of a fraction, and exits 1 while any
    is left (`verification.md` step 6). `--allow` names numbers that need no source, such as
    ordinals: single values and integer ranges, so `0-10` allows the integers 0 to 10, not 0.859.
    A trace shows the value exists in a source, not that it is the right one: check each table
    against its source. Re-read every face for names, dates, internal ids and codenames, which no
    pattern catches.
11. **Export:**
    ```
    python3 <skill>/scripts/deck.py pptx <deck>
    ```
    It writes one full-bleed picture per slide plus the speaker notes. The PPTX is faithful but not
    editable: edit the HTML and rebuild. `deck.py all <deck>` runs check, pdf (with pdfcheck) and pptx
    in one command and exits 1 on any finding. It does not replace steps 1–6, 9, 10 and 12. For
    claude.ai Slides, see §5.
12. **Report.** Give the paths of the HTML, PDF and PPTX in `<deck>/build/`. Name anything not
    verified: slides not looked at, numbers not traced, exports not produced.

If no Chrome or Chromium can run, follow "When rendering is not possible" in `verification.md`, and
tell the user which slides were not checked visually.

## 4. Workflow: paper explainer

Two slides per paper: 17 paper-idea (problem, idea, the paper's own figure, a takeaway) and
18 paper-method (method, formula, what it certifies, results with pages, limits, "For us"). The deck
also gets a cover, a how-to-read slide, linked contents and section dividers. Follow
`references/paper-explainer.md`; in short:

```
python3 <skill>/scripts/explainer.py new   <project> --title "<title>"
python3 <skill>/scripts/explainer.py add   <project> <key> --pdf <path, or an arXiv URL with its version>
#   read the paper; write <project>/papers/<key>.json (schema in paper-explainer.md)
python3 <skill>/scripts/figcrop.py   page  <project>/papers/<key>.json <page>       # page on a 50 pt grid
python3 <skill>/scripts/figcrop.py   crop  <project>/papers/<key>.json <page> x0 y0 x1 y1
python3 <skill>/scripts/explainer.py check <project> <key>                          # fields, math, quotes, layout
python3 <skill>/scripts/explainer.py build <project> --sheet                        # deck, PDF, pdfcheck, links
python3 <skill>/scripts/numtrace.py  <project>/build/deck <project>/sources/*.txt --allow 0-10
```

Every number on a result line must sit in a span quoted from the paper, found on the cited page
or the page next to it (`scripts/quotecheck.py`). When a paper figure's own text would show under
about 20 px in the figure box, crop the single panel the idea needs and name the full figure in the
caption (`paper-explainer.md`, step 5). The figure boxes that explainer.py writes into the notes
are crop coordinates, not claims, and stay untraced (`paper-explainer.md`, step 7). Look at both
previews per paper
(`<project>/build/check/<key>-1.png`, `-2.png`) and at `<project>/build/contact-sheet.png`. The
writing passes of step 6 apply. The assembled deck in `<project>/build/deck/` is an ordinary deck
folder: `deck.py pptx` and `deck.py inline` work on it. Change the JSON and rebuild; never edit that
folder.

## 5. Export to claude.ai Slides

This needs an agent with claude.ai's Artifact tool. The deck keeps its technical-swiss look, so no
design system is installed unless the user asks for one.

1. Inline the deck:
   ```
   python3 <skill>/scripts/deck.py inline <deck>
   ```
   It writes `<deck>/build/inline/project/`: `deck.json` plus one `slides/<id>.html` per slide,
   every style inline. It also writes `blobs.json`, the images to upload. It renders each inlined
   slide against the build and must print `all N slides match`. For an explainer, `<deck>` is
   `<project>/build/deck`.
2. Create the artifact. Publish with the Slides type's `type_url` (from Artifact `action: "list"`,
   `scope: "types"`), a `title`, no files and `auto_open: "after_first_write"`. Keep the returned
   `url`.
3. Upload each image named in `blobs.json`. Its keys are paths in the deck such as `assets/x.png`, so
   publish `{url, file_path: <deck>/assets/x.png, asset: true}`. Write each returned url, verbatim,
   as that key's value in `blobs.json`.
4. Inline again with the urls: `python3 <skill>/scripts/deck.py inline <deck> --blobs <deck>/build/inline/blobs.json`.
5. Publish to that `url` with `root: <deck>/build/inline`,
   `file_path: <deck>/build/inline/project/deck.json` and `files` mapping each
   `project/slides/<id>.html` to itself.

The create result carries the Slides type's own instructions; follow them for the calls. The pixel
comparison in step 1 is this export's check. `scripts/inline.py` lists the format rules it writes
to: inline styles only, no classes or margins, at most 200 elements per slide, notes up to 4,000
characters. It reports any slide it cannot bring within them.

## 6. The rules in brief

Full statements, with the reason for each, are in `references/slide-rules.md`; this list is only an
index.

- Slide faces carry no person names, dates, internal ids, file paths, codenames, logos or decoration
  unless the user asks (§1).
- Every number comes from its source, with its population, n, unit and threshold on the face. An
  inference, hypothesis or illustrative number is labelled as such (§2).
- Titles state findings. One idea per slide. Plain words, with jargon expanded on first use. No
  filler, hype or bragging numbers (§3).
- Structure: cover, how to read, the parts, limits, summary with next steps. Section slides one per
  part or none; without a request, only with three or more parts (§4).
- The footer is the page number only. Add a label only when the user asks (`deck.py new --footer`,
  or `"footer"` in `deck.json`); `deck.py` refuses one that looks like a date (§5).
- R7: nothing collides. Render every slide and look at it. A large number beside text gets a
  measured width with slack, or sits above its text (§6).
- The printed PDF is checked as printed, with image sizes frozen first (§7).
- Speaker notes carry sources, commands and long caveats (§8).
- Type never shrinks to fit: cut words, re-layout on the grid, or split the slide.

## 7. Deck format

```
<deck>/
  deck.json          {"title": "...", "theme": "technical-swiss", "slides": ["01-main-title", ...]}
                     optional: "footer" (a short label, only when asked), "math_fontset" ("cm" by
                     default; or "stix", "stixsans", "dejavusans", "dejavuserif")
  slides/<id>.html   exactly one <section>; class "cover" or "section", or data-nofooter, means no footer;
                     optional <aside class="notes"> as its last child
  assets/            images and charts, referenced as assets/<file>
  ledger.md          the content ledger (§3 step 2); derivations.txt, the saved arithmetic of derived numbers
  build/             written by the scripts: <slug>.html, .pdf, .pptx, png/, contact-sheet.png, inline/,
                     anatomy/ (anatomy.py --deck: working renders with the grid, not part of the deck)
```

## 8. New templates and themes

- **A slide that no template fits:** build a new template with `references/template-authoring.md`.
  It shows how each written rule becomes a grid measure, works a two-metric template from a failing
  first draft to an accepted one, and ends with an acceptance checklist. Never stretch a template
  past the variants its comment names.
- **Another theme:** copy `templates/technical-swiss/` to `templates/<name>/` and change the tokens
  in `theme.css`. Keep its class names and the `--foot-band` token: the checks and `anatomy.py` read
  them. Then:
  - pass `deck.py new --theme <name>` (it writes `"theme": "<name>"` into `deck.json`);
  - render its templates with `python3 <skill>/scripts/anatomy.py --theme <name> --out <dir>`;
  - describe the theme in `references/<name>.md`.

  `explainer.py` always builds in technical-swiss.

## 9. Files

| path | what it holds |
|---|---|
| `README.md` | overview, install and copy instructions |
| `references/slide-rules.md` | the user's slide rules in one place: faces, fidelity, writing, structure, footer, R7, print, notes, writing passes |
| `references/verification.md` | the check pipeline step by step, each check's report, the R7 incident and the print lesson as reproduced cases, the face scan |
| `references/slide-types.md` | the 18 templates in one table, and how to choose |
| `references/template-catalog.md` | one page per template: anatomy image, grid, capacity, binding rules, do and don't |
| `references/template-authoring.md` | rules to geometry, tailoring a template, the worked two-metric template, the acceptance checklist |
| `references/technical-swiss.md` | the design system: canvas, grid, type scale, colour meanings, fit budget, typesetting traps |
| `references/swiss-design-spec.md` | the source Swiss spec that technical-swiss adapts (`slide-rules.md` wins where they differ) |
| `references/charts.md` | chart forms and rules |
| `references/paper-explainer.md` | the paper-explainer workflow, JSON schema, budgets and checks |
| `references/templates/` | `<id>.png` (clean render) and `<id>-anatomy.png` (grid and labelled regions) for all 18 templates; `gallery.png` (all 18, the two paper-explainer templates included); `cases/` (the R7 and print cases); `authoring-example/` (the worked template deck and its renders) |
| `references/example-scenarios/` | a finished 15-slide standard deck: `slides/` and `assets/`, `build/` outputs, contact sheet, a README on what it shows |
| `references/example-explainer/` | a finished 9-slide paper explainer: project files, figure crops, page-marked sources, PDF, contact sheet, README |
| `templates/technical-swiss/` | `theme.css`, `deck.json` and `gallery.png` (the 16 general templates as one deck; `references/templates/gallery.png` adds the two paper-explainer ones), `slides/` (18 templates), `fonts/` (Inter, JetBrains Mono, with `LICENSES/`), `assets/` (placeholder images and `make_placeholders.py`) |
| `scripts/setup.sh` | creates the venv and installs headless Chromium when no Chrome is found |
| `scripts/deck.py` | `new`, `build`, `check`, `text`, `png`, `pdf`, `pptx`, `inline`, `all`, `selftest` (`--help` on each); `text` prints each slide's face text and notes, `text --prose` the input for the writing passes |
| `scripts/numtrace.py` | traces every number on the faces and in the notes to source text files; exit 1 while any is untraced |
| `scripts/pdfcheck.py` | checks a printed PDF for overlaps, panel edges and the footer band (run by `deck.py pdf`) |
| `scripts/inline.py` | claude.ai Slides export with pixel verification (run by `deck.py inline`) |
| `scripts/mathsvg.py` | TeX to SVG with matplotlib mathtext (run by the build for `.math` elements) |
| `scripts/contact_sheet.py` | all rendered slides on one sheet, each tile labelled with its slide id and first heading |
| `scripts/anatomy.py` | clean and anatomy renders of templates (`references/templates/`) or of a deck (`--deck`) |
| `scripts/charts.py` | matplotlib charts in the theme: dumbbell, dot plot, horizontal bars, sized saving |
| `scripts/explainer.py` | paper explainer: `new`, `add`, `check`, `build` |
| `scripts/figcrop.py` | finds, shows on a grid, and crops a figure from a paper's PDF |
| `scripts/quotecheck.py` | checks quoted spans against a paper's page-marked text; writes that text from a PDF |

Each script's header docstring gives its full usage and what it needs: the standard library,
Chrome, matplotlib, PyMuPDF, Pillow or python-pptx.
