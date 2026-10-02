---
name: organize
description: Transform any unstructured or sprawling source - a long chat, a research thread, web pages and browser tabs, pasted notes, uploaded files, or a directory of material - into one clean, canonical, well-architected document (default Markdown, any format on request). Use this whenever the user says /organize, or asks to "organize this", "document this", "write this up", "clean this up", "consolidate", "make sense of this", "turn this into notes / a doc / a wiki / a spec / a brief / a reference / a summary", or otherwise wants scattered information distilled into a structured, scannable, single-source-of-truth artifact. Applies systems thinking, information architecture (LATCH, MECE), Diataxis, and the Pyramid Principle to model the material, structure it for the reader and purpose, and render it render-safe. For compiling a DEBUGGING/troubleshooting session into a replayable debug log, defer to /organize-debug; use this skill for everything else.
---

# /organize - The Universal Technical Documenter and Organizer

Take any pile of raw material - a sprawling chat, a research dump, a set of web pages, a folder of files, a stream of pasted notes - and turn it into ONE document that is the single source of truth: faithful to the source, architected for a specific reader and purpose, render-safe in its target format, and so well-organized that the reader can find any fact and act on it from cold. Treat correctness as life-or-death. Be surgical. No fabrication, no fluff, no em-dashes.

Organizing is not decoration and it is not summarizing-and-hoping. It is two acts performed together: **modeling reality faithfully** (what is actually here, how it relates, what is true) and **shaping it for use** (so a particular reader achieves a particular purpose with minimum friction). A pretty document that drops a load-bearing fact, buries the answer, or invents a detail has failed.

(For one specific job - distilling a debugging session into a replayable debug log - use `/organize-debug`. This skill handles all other organization.)

## The cardinal rule: audience x purpose determines everything

Before choosing a single heading, answer four questions. They cascade into every downstream decision (which structure, which depth, which order, which format):

1. **Who reads this?** Their expertise, their vocabulary, what they already know.
2. **Why - what do they do after reading?** Decide, build, look something up, learn a concept, onboard, hand off, remember.
3. **What single question must this document answer?** The governing thought. If you cannot name it, you do not yet understand the material.
4. **What is the failure mode?** What would make this document useless to them (missing the answer, too long to scan, wrong altitude, untrustworthy).

If the source or the user makes these answerable, proceed. If genuinely ambiguous and the choice materially changes the artifact, ask exactly one sharp question; otherwise infer the most likely reader/purpose and state the assumption in one line at the top. Never stall on a question you can answer yourself.

## The pipeline

```
INGEST  ->  MODEL  ->  ARCHITECT  ->  RENDER  ->  VERIFY
(get it    (see the   (choose the   (write it   (prove it is
 all,       structure   structure)    render-     the single
 faithfully) before                   safe)       source of
            writing)                               truth)
```

### 1. Ingest - get the full source, faithfully

Capture at full fidelity *before* compressing. You cannot organize what you have not fully read. Pull from whichever sources apply:

- **The current chat.** Read the whole thing. Do not trust your own running summary; the load-bearing detail lives in the specifics.
- **Past chats.** `conversation_search` for a topic, `recent_chats` for a time window. Use when the user references "what we discussed", "my project", "the thread from last week".
- **Uploaded files and transcripts.** Look in `/mnt/user-data/uploads` and `/mnt/transcripts`. Use the **file-reading** skill to route by type (pdf, docx, xlsx, csv, json, images, archives) instead of blindly `cat`-ing a binary. If a file is already shown in context, use it directly.
- **Web pages and browser content.** A URL the user gives -> `web_fetch` (or fetch each tab/link). A live browsing tool, if one is connected, for an active session.
- **Pasted content.** Use it as-is; it is already the source.

Then fix the **scope boundary** explicitly: what is in, what is out. State it if non-obvious. Fidelity first, compression second - never the reverse.

### 2. Model - see the structure before you write (systems thinking)

Do not start typing prose. First build a model of what is actually here. This is the step amateurs skip and is where most of the value is created.

- **Atomize.** Break the source into atomic units: one idea, fact, claim, decision, step, definition, or entity each. Atomic units can be re-grouped freely; paragraph-blobs cannot.
- **Map relationships (entities and edges).** What relates to what? What contains, precedes, causes, depends on, or contradicts what? Sketch the entity-relationship graph mentally or on scratch. Distinguish **structure** (the static relationships) from **behavior** (what changes over time, the flows and feedback loops).
- **Find the hierarchy and the timeline.** Which units are parents, which children? Is there a temporal sequence? A dependency order?
- **Surface the recurring patterns.** The themes, the repeated motifs, the meta-structure that the raw material does not announce but that organizes it. Naming the pattern is often the single most useful move.
- **Separate signal from noise.** Drop digressions, dead ends, pleasantries, and chatter. Keep what bears weight.
- **Deduplicate (DRY: one fact, one place).** If the same fact appears five times, it lives once in the document, in the right place, referenced elsewhere if needed.
- **Resolve contradictions.** When sources conflict, later usually supersedes earlier - but a *genuine* unresolved conflict is flagged explicitly (`Note: sources disagree on X`), never silently resolved by picking the convenient one.
- **Calibrate epistemically.** Tag, at least in your own head, what is *stated* in the source vs *inferred* by you vs *uncertain/unknown*. **Never fabricate to fill a gap.** A labeled gap ("the source does not specify Y") is more valuable than a confident fiction, and infinitely safer.

The output of this stage is a model: a set of atomic units, their relationships, the themes, and the known gaps. The document is just this model, rendered.

### 3. Architect - choose the structure (most documents are won or lost here)

A document is its skeleton. Get the skeleton right before any prose. Use the toolkit (deep dives in `references/frameworks.md`):

- **Pick the organizing axis (LATCH).** There are essentially only six ways to organize anything: **L**ocation, **A**lphabet, **T**ime, **C**ategory, **H**ierarchy, and Magnitude. Choose deliberately and name which one you are using. Mixing axes within one level is a common cause of confusing documents.
- **Make the groups MECE.** Mutually Exclusive (no item fits two buckets - no overlap) and Collectively Exhaustive (every item has a bucket - no gap). MECE failures are the deep cause of "this document feels off."
- **Apply the Pyramid Principle.** Lead with the answer / governing thought, then the MECE groups that support it, then the detail under each. Inverted pyramid: the most important thing first, so a reader who stops early still gets the point. Use SCQA (Situation, Complication, Question, Answer) to frame an introduction when one is needed.
- **Pick the Diataxis mode if this is documentation.** Tutorial (learning-oriented), How-to (task-oriented), Reference (information-oriented), Explanation (understanding-oriented). These serve different needs; **do not mix two modes in one section** - it is the most common documentation error. A reader looking something up does not want a lesson; a learner does not want a dry table.
- **Layer for cognitive load (progressive disclosure).** A short summary / TL;DR up top, the body below, deep specifics in appendices or collapsibles. Chunk into groups of roughly four to seven. Keep headings parallel in grammar and altitude so the structure is legible at a glance.
- **Draft the skeleton first.** Write the outline - headings and one-line intents - and sanity-check it (MECE? right axis? answer-first? right mode?) *before* writing prose. Fixing a bad outline costs a minute; fixing a bad 2000-word draft costs an hour.

### 4. Render - in the target format, render-safe

Default is **Markdown**. For any other format, follow `references/formats.md`. Whatever the format, obey the universal render-safe rules - they exist because sloppy formatting breaks silently in some viewers and the document must render *identically everywhere*:

- **Code/pre-formatted fences sit at column 0**, with a blank line directly above, never indented inside a list item and never nested. If a step owns a code block, put a **bold label above the block** (`**Step 1 - <what>:**`) so it reads as belonging to that step without relying on list nesting.
- **Use tables for anything comparable or scannable** (settings, options, before/after, attribute grids). Prose is for narrative; tables are for lookup.
- **Headings: parallel, scannable, hierarchical.** Add a table of contents once the document exceeds roughly one screen of headings.
- **Link a networked corpus** rather than flattening it - cross-references and anchors turn a pile into a navigable web.
- **Preserve verbatim what must be exact:** commands, code, quotes, identifiers, numbers, names. Never silently "clean up" something in a way that changes its meaning.
- **No em-dashes.**

For rich formats, do not hand-roll the binary: hand the architected outline to the corresponding skill - **docx** (Word), **pdf** (PDF), **pptx** (slides), **xlsx** (spreadsheets). This skill owns the architecture; that skill owns the rendering. For structured data (JSON, YAML, CSV) emit valid, schema-consistent output with a legend. See `references/formats.md` for the per-format playbook and a format-selection guide.

### 5. Verify - the document is the single source of truth

Before finishing, run the checklist. Each item has a failure mode that ruins the artifact:

- **Completeness** - every load-bearing unit from the model is present; nothing important was dropped in compression.
- **Fidelity** - zero fabrication; every claim is traceable to the source; numbers, quotes, and identifiers are exact.
- **MECE** - no overlap, no gap; contradictions are resolved or explicitly flagged.
- **Navigability** - a reader can locate any fact fast via headings, TOC, or links; the answer is near the top, not buried.
- **Mode integrity** - no section silently mixes Diataxis modes; altitude is consistent.
- **Render** - it opens and renders identically in a plain viewer; no broken fences, tables, or links.
- **The acid test** - *could the target reader accomplish their purpose using only this document, starting cold?* If not, find the gap and close it.

### 6. Adversarial pass (dialectic) - red-team your own document

The best organization survives a hostile reader. Before you ship, attack it yourself: Where is the lead buried? Where do two sections overlap or leave a gap (MECE break)? Where does a heading promise something the body does not deliver (broken information scent)? Where does the structure fight the content (a process forced into a category scheme, or vice versa)? Where did I assert something the source did not say? Fix what the attack finds. A document that cannot be broken by its own author is ready.

## The intellectual toolkit (quick reference)

Pull the right tool for the situation. Depth and worked examples live in `references/frameworks.md`.

| Tool | Use it to | Reach for it when |
|------|-----------|-------------------|
| **Audience x Purpose** | decide everything downstream | always, first |
| **LATCH** | choose the organizing axis | structuring any set of items |
| **MECE** | get clean, gapless grouping | any time you create buckets |
| **Pyramid Principle / SCQA** | lead with the answer, frame intros | reports, briefs, recommendations |
| **Diataxis (4 modes)** | match doc shape to reader need | any technical documentation |
| **Progressive disclosure / cognitive load** | layer depth, control overwhelm | long or dense material |
| **Systems modeling (entities, flows, feedback)** | model a complex domain faithfully | architectures, processes, tangled topics |
| **Atomic notes / linking (Zettelkasten)** | build a networked knowledge base | wikis, evergreen notes, second brains |

## Output format menu (default: Markdown)

- **Markdown** (default) - notes, docs, READMEs, specs, briefs, wikis. Render-safe rules above; details in `references/formats.md`.
- **HTML** - self-contained or interactive single-file documents.
- **Word / PDF / Slides / Spreadsheet** - hand the outline to the **docx** / **pdf** / **pptx** / **xlsx** skill.
- **JSON / YAML / CSV / TSV** - structured or tabular data; valid and schema-consistent.
- **Other** (Obsidian, org-mode, reStructuredText, AsciiDoc) - see `references/formats.md`.

## Workflow

1. **Ingest** the full source faithfully (chat, past chats, files, web, paste). Fix the scope boundary.
2. **Model** it: atomize, map relationships, find hierarchy/timeline/themes, dedupe, resolve or flag contradictions, mark gaps. Never invent.
3. **Architect**: name the governing question; pick the LATCH axis and the Diataxis mode; make groups MECE; order answer-first (Pyramid); draft and sanity-check the outline before prose.
4. **Render** in the target format (default Markdown) following the render-safe rules; hand rich formats to their skill.
5. **Verify** against the checklist; run the **adversarial pass**.
6. **Write** the file (default name `<topic>.md`) to the outputs directory.
7. If a `present_files` tool is available, **present** it with a one-paragraph summary of what it contains and how it is organized. Do not restate the document in chat.

The finished artifact is the single source of truth: faithful to the source, architected for its reader, render-safe, and complete enough that the reader can act from it cold.
