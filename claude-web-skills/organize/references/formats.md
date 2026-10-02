# Formats - The Rendering Playbook

How to render the architected outline into each target format. Default is Markdown. Pick the format from the source's purpose (see the selection guide at the end), then follow that format's section.

## Universal render-safe rules (apply to every text format)

These exist because formatting breaks *silently* in some viewers; the document must render identically everywhere.

- **Fenced code / pre-formatted blocks at column 0**, blank line directly above, never indented inside a list item, never nested inside another fence. If a step owns a code block, put a **bold label above it** (`**Step 1 - <what>:**`) so it reads as belonging to that step without depending on list nesting.
- **Tables for comparable or scannable data** (options, settings, before/after, attribute grids). Prose narrates; tables are for lookup.
- **Parallel, hierarchical headings**; add a table of contents once headings exceed about one screen.
- **Exact verbatim** for commands, code, quotes, identifiers, numbers, names. Never silently "clean up" in a way that changes meaning.
- **Links for a networked corpus** - cross-references and anchors over flattening.
- **No em-dashes.**

---

## Markdown (default)

The default for notes, READMEs, docs, specs, briefs, wikis, summaries.

- **Headings:** one `#` H1 (the title), then `##` / `###`. Keep them parallel in grammar and altitude. Do not skip levels.
- **Table of contents:** for longer docs, a bulleted list of anchor links under the title. Anchors are the lowercased heading with spaces as hyphens.
- **Tables:** GitHub-flavored pipe tables for any tabular or comparative data.
- **Code fences:** triple-backtick with a language tag (` ```bash `, ` ```python `, ` ```json `) for syntax highlighting. Column 0, blank line above.
- **Task lists:** `- [ ]` / `- [x]` for checklists and action items.
- **Callouts / admonitions:** GitHub supports `> [!NOTE]`, `> [!WARNING]`, `> [!TIP]` blockquote callouts; many other renderers do not. Use sparingly and never let meaning depend on them - a plain `> **Note:** ...` blockquote renders everywhere.
- **Footnotes:** `text[^1]` with `[^1]: ...` for asides that would break flow. Supported in many but not all renderers; keep load-bearing content in the body.
- **Front matter:** a leading `---` YAML block (title, date, tags) when the target is a static-site generator or note system; omit otherwise.
- **Diagrams:** a ` ```mermaid ` block for flowcharts, sequence diagrams, entity-relationship sketches, state machines, and Gantt timelines. Renders natively on GitHub and many tools - ideal for showing the *structure* a systems model surfaced. Keep a one-line text description nearby for viewers that do not render it.
- **Math:** `$inline$` and `$$display$$` where the renderer supports KaTeX/MathJax (GitHub now does).

**Obsidian / wiki variant:** use `[[wikilinks]]` for note-to-note links and `![[embeds]]` for transclusion when the user's target is Obsidian or a linked-note vault. Otherwise prefer standard relative-path links for portability.

---

## HTML

Choose when the deliverable should be self-contained, styled, or interactive (a single file the user opens in a browser, a small dashboard, a document with collapsible sections or a live filter).

- **Single file.** Inline the CSS and JS; pull any libraries from a CDN. No build step.
- **Semantic structure.** Real `<h1>`-`<h6>`, `<table>`, `<nav>` for the TOC, `<details>`/`<summary>` for progressive disclosure.
- **No fabricated interactivity.** Wire only what the content needs.
- For substantial UI or design work, consult the **frontend-design** skill for the visual system.

---

## Word, PDF, Slides, Spreadsheet - hand off to the format skill

Do **not** hand-roll these binaries. This skill owns the architecture (the outline, the MECE grouping, the answer-first order); the format skill owns the rendering. Read that skill's `SKILL.md` first, then pass it the structured outline.

| Target | Skill | Use for |
|--------|-------|---------|
| `.docx` (Word) | **docx** | formal documents, reports, letters, memos, anything with headings/TOC/letterhead the user wants as Word |
| `.pdf` | **pdf** | print-ready or portable final output, form filling, merging |
| `.pptx` (slides) | **pptx** | decks, presentations - the outline becomes the slide structure |
| `.xlsx` (spreadsheet) | **xlsx** | models, trackers, multi-column data with formulas/formatting |

The workflow is the same as always - ingest, model, architect - and only the **render** step changes: instead of writing Markdown, you invoke the format skill with the finished outline.

---

## Structured data - JSON / YAML / CSV / TSV

When the organized output is *data* for a machine or a spreadsheet, not prose for a human.

- **JSON / YAML:** choose when the material is hierarchical or record-shaped (config, an entity list with attributes, a structured export). Emit *valid*, consistently-keyed output. Decide the schema first (the keys and their types) and apply it uniformly across every record. Include a short legend or a `// comment` / `# comment` (YAML) explaining the schema when the consumer is human. YAML for human-edited config; JSON for interchange.
- **CSV / TSV:** choose for purely tabular data - one record per row, stable header row, one fact per cell. Quote fields containing commas or newlines. For anything that needs multiple sheets, formulas, types, or formatting, use the **xlsx** skill instead - CSV is the lowest common denominator, not the rich option.

The same modeling discipline applies: atomize, dedupe, and make the fields MECE (each column one attribute, no overlapping columns).

---

## Other text formats (on request)

- **reStructuredText (`.rst`):** Sphinx/Python-docs ecosystems. Directives (`.. note::`), explicit TOC trees.
- **AsciiDoc (`.adoc`):** richer than Markdown for books and manuals; admonition blocks, includes, attributes.
- **org-mode (`.org`):** Emacs users; outline-native with TODO states, drawers, and literate-programming blocks.

Match the format's native idioms (its heading syntax, its admonition style, its link form) rather than transliterating Markdown.

---

## Format-selection guide

Pick from the source's purpose and reader, not from habit:

| If the goal is... | Default to |
|-------------------|------------|
| read-once narrative, notes, a doc to share or commit | **Markdown** |
| a formal deliverable the user will send as a document | **docx** (via skill) |
| print-ready, portable, or final-form output | **pdf** (via skill) |
| something to present aloud | **pptx** (via skill) |
| a self-contained or interactive single-file artifact | **HTML** |
| look-up / scannable comparison (settings, options) | tables inside **Markdown**, or a **reference**-mode doc |
| tabular records with formulas or multiple sheets | **xlsx** (via skill) |
| flat tabular data for import elsewhere | **CSV / TSV** |
| structured/hierarchical data for a machine | **JSON / YAML** |
| an evergreen, networked knowledge base | linked **Markdown** / **Obsidian** wikilinks |

When the user names a format, use it. When they do not, infer from purpose and state the choice in one line; offer an alternative if a different format would clearly serve them better (for example, "saved as Markdown; say the word and I will render it as a Word doc").
