# Frameworks - The Intellectual Toolkit for Organizing

Deep dives behind the quick-reference table in SKILL.md. Read the section for the tool you need; you rarely need all of them at once.

## Contents

1. Diataxis - the four modes of documentation
2. LATCH - the (only) ways to organize anything
3. The Pyramid Principle - lead with the answer
4. MECE - clean, gapless grouping
5. Cognitive load and progressive disclosure
6. Systems modeling - faithfully representing a complex domain
7. Atomic notes and linking (Zettelkasten) - networked knowledge
8. Information scent and findability

---

## 1. Diataxis - the four modes of documentation

Daniele Procida's insight: technical documentation serves four *different* needs, and the cardinal error is mixing them in one piece. The needs split on two axes - whether the reader is *acquiring* skill or *applying* it, and whether the content is *practical* (action) or *theoretical* (cognition).

| Mode | Reader need | Orientation | Answers | Form |
|------|-------------|-------------|---------|------|
| **Tutorial** | "teach me, I am new" | learning, practical | "take me by the hand" | a lesson; a guaranteed-to-work sequence; concrete, not comprehensive |
| **How-to guide** | "I have a goal, show me the steps" | task, practical | "how do I achieve X?" | a recipe; assumes competence; a series of steps to a result |
| **Reference** | "I need to look something up" | information, theoretical | "what exactly is X?" | a map; dry, accurate, exhaustive; structured for lookup, not reading-through |
| **Explanation** | "help me understand why" | understanding, theoretical | "why is it this way?" | a discussion; context, design rationale, alternatives, history |

**The cardinal sin:** a reference page that drifts into teaching, or a tutorial cluttered with edge-case reference detail. A reader looking up a function signature does not want a lesson; a beginner following a tutorial does not want every option enumerated. **Keep one section in one mode.** If material spans modes, split it into separate sections (or separate documents) and link them.

**How to tell which mode a piece of content wants:** ask what the reader is doing *while* they read it. Following along step by step at a keyboard -> tutorial or how-to (new -> tutorial, competent -> how-to). Scanning to find one fact -> reference. Reading in an armchair to understand -> explanation.

**Example.** Organizing scattered notes about a payments API:
- "Walkthrough: charge your first card in 5 minutes" -> Tutorial.
- "How to issue a refund" / "How to handle a declined card" -> How-to guides.
- "Endpoint reference: every field, type, and error code" -> Reference.
- "Why we use idempotency keys" -> Explanation.

Four sections, four modes, cleanly separated, cross-linked. That is a well-organized doc set; one giant blended page is not.

---

## 2. LATCH - the (only) ways to organize anything

Richard Saul Wurman's claim ("five hat racks"): every collection of information can be organized by one of essentially five axes, plus magnitude. Choosing the axis *deliberately* is most of the battle.

| Axis | Organize by | Best when | Failure mode |
|------|-------------|-----------|--------------|
| **Location** | physical or spatial position | geography, anatomy, a building, a diagram, a network topology | useless when items have no meaningful place |
| **Alphabet** | A-Z | large reference where the reader knows the item's name (glossary, index, directory) | hides relationships; arbitrary adjacency |
| **Time** | chronology / sequence | history, processes, timelines, changelogs, anything causal or procedural | obscures category when readers want "all of type X" |
| **Category** | kind / type / topic | grouping like with like; most topical documents | requires the categories to be MECE or it collapses |
| **Hierarchy** | magnitude, importance, rank, containment | priorities, taxonomies, org structure, "biggest to smallest" | forces a single dimension of ranking onto multi-dimensional items |

(Wurman folded magnitude into Hierarchy; treat "by importance / by size" as its own move when ranking is the point.)

**The discipline:** name the axis before you sort. Most confusing documents secretly switch axes mid-level - half the sections are by category and half by time, with no signal. Pick one axis per level of the hierarchy. You can nest a *different* axis at the next level down (Category at the top, Time within each category) - that is fine and often ideal - but never blend two at the same level.

**Example.** A list of 30 restaurants can be organized by Location (neighborhood map), Alphabet (a directory), Time (newest openings first), Category (cuisine), or Hierarchy (by rating). Each serves a different reader. "I am hungry near here" wants Location; "is that place I heard about any good" wants Alphabet; "what should I try" wants Hierarchy. The *purpose* picks the axis.

---

## 3. The Pyramid Principle - lead with the answer

Barbara Minto's method for structuring any document that makes a point. Two rules:

**Vertical: answer first, then support.** State the governing thought (the answer, the recommendation, the conclusion) at the top. Below it, the few groups of reasons that support it. Below each group, the detail. The reader meets the point immediately and descends only as far as their skepticism requires. This is the inverted pyramid: a reader who stops after the first paragraph still leaves with the thesis.

**Horizontal: each level is MECE and answers the question the level above raises.** If the top says "we should adopt X," the next level answers "why?" with a MECE set of reasons; each reason, if questioned, is itself supported below. The structure is a Q-and-A dialogue running top to bottom.

**SCQA for the introduction.** When the document needs a setup, frame it as:
- **Situation** - the stable context the reader agrees with.
- **Complication** - what changed / went wrong / raises the question.
- **Question** - the question the Complication provokes.
- **Answer** - your governing thought (which then becomes the top of the pyramid).

**The "so what?" test.** After every section, ask "so what?" If the answer is not obvious or not relevant to the governing thought, the section is detail in search of a point - cut it or subordinate it.

**Example.** Bad: a report that recounts the investigation chronologically and reveals the recommendation on page 9. Good: page 1 says "Recommendation: migrate to Postgres by Q3," followed by three MECE reasons (cost, reliability, team familiarity), each expanded below. The executive reads one page and decides; the engineer reads on for the detail.

---

## 4. MECE - clean, gapless grouping

Mutually Exclusive, Collectively Exhaustive. The quiet backbone of every good structure.

- **Mutually Exclusive** - no item belongs in two buckets. Overlap forces the reader to wonder "why is this here and not there?" and creates double-counting.
- **Collectively Exhaustive** - every item has a bucket; nothing falls through. Gaps are where readers lose trust ("but what about Y?").

**Tests.** For exclusivity: take a borderline item and check it has exactly one home. For exhaustiveness: imagine the most likely "but what about...?" and confirm it has a bucket (even if that bucket is "Other / edge cases," explicitly).

**Common MECE structures, in rough order of rigor:**
- **Algebraic / partition** - splits that are provably complete: `< 0 | = 0 | > 0`; `internal | external`; `before | during | after`. The gold standard when available.
- **Process steps** - the stages of a sequence, which are exclusive (you are in one stage) and exhaustive (the stages cover the whole process).
- **Conceptual** - categories that are *argued* to be complete (e.g. "people, process, technology"). Weaker; always pressure-test for a missing category.

When a grouping feels subtly wrong, it is almost always a MECE break - two buckets overlap, or a whole class of item has no home.

---

## 5. Cognitive load and progressive disclosure

The reader has a small working memory. Respect it or lose them.

- **Three loads (Sweller).** *Intrinsic* (the inherent difficulty of the material - fixed), *extraneous* (difficulty added by bad presentation - eliminate this), *germane* (effort that builds understanding - preserve this). Good organization drives extraneous load to zero so the reader spends their capacity on the material, not on decoding your layout.
- **Chunk.** Group into units of roughly four to seven; nest rather than listing twenty flat items. Humans hold few items at once (Miller's 7+-2; Cowan's tighter ~4).
- **Progressive disclosure.** Reveal in layers matched to need: a one-line summary, then the body, then deep specifics in appendices, footnotes, or collapsibles. The reader pulls detail as their need grows instead of being buried up front.
- **Inverted pyramid (journalism).** Most newsworthy fact first, supporting detail after, background last. A reader who leaves early still got the essential.
- **Signaling and parallelism.** Headings, consistent structure, and parallel grammar act as signposts that let the reader navigate without re-reading. Spatial contiguity: keep a label next to the thing it labels, an explanation next to the code it explains.

The practical upshot for a document: a scannable summary on top, MECE chunked sections below, depth tucked into clearly-labeled lower layers.

---

## 6. Systems modeling - faithfully representing a complex domain

When the source is a tangled system (an architecture, a process, a research area, an organization), model it as a system before you write. Borrowed from systems thinking.

- **Entities and relationships.** List the entities (components, actors, concepts). Then the edges: what *contains, precedes, causes, depends on, produces, consumes, or contradicts* what. This entity-relationship sketch is the true shape; the document narrates it.
- **Structure vs behavior.** Structure is the static set of relationships (the wiring). Behavior is what happens over time (the signals on the wires). Separate them: "here is how it is built" vs "here is how it runs." Conflating them is a top source of muddled technical writing.
- **Stocks, flows, feedback.** What accumulates (stocks), what moves between stocks (flows), and where outputs loop back to affect inputs (feedback loops, reinforcing or balancing). Naming a feedback loop often explains a behavior that a flat list never could.
- **Boundary.** What is inside the system you are documenting and what is environment? An explicit boundary prevents scope sprawl.
- **Hierarchy / holarchy.** Most systems are nested: each part is itself a system, each is part of a larger one. Document at one level, with explicit pointers up and down, rather than smearing three levels together.
- **Leverage points.** When the purpose is to *act* on the system, identify where a small change produces a large effect. This tells the reader where to focus.

The deliverable of modeling is a faithful map. A diagram (a flowchart, an entity-relationship sketch, a sequence) is often the clearest rendering; in Markdown, reach for a Mermaid block (see formats.md).

---

## 7. Atomic notes and linking (Zettelkasten) - networked knowledge

When the goal is an evergreen knowledge base (a wiki, a "second brain," a set of reusable notes) rather than a single linear read, organize as a *network* of atomic notes.

- **Atomicity.** One note = one idea, stated so it stands alone. Atomic notes recombine freely; a note that crams three ideas can only ever be filed in one place.
- **Autonomy.** Each note is self-contained - understandable without its neighbors - so it survives being linked from anywhere.
- **Linking over filing.** Instead of forcing every note into one folder (a single hierarchy), link related notes. Structure *emerges* from the link graph rather than being imposed up front. An index or map-of-content note serves as an entry point.
- **Emergence.** As links accumulate, clusters reveal themselves - these become the real, bottom-up categories, usually better than any taxonomy you would have guessed in advance.

Choose this over a linear document when the material is a body of knowledge the user will return to and extend, where any note may relate to many others, and where lookup-by-association matters more than read-once flow. In Markdown, render with relative links or wikilinks (Obsidian style) - see formats.md.

---

## 8. Information scent and findability

From Rosenfeld and Morville (information architecture). A document or corpus is *findable* when a reader can predict, from a label, what lies behind it - the "scent" leads them to the prey.

- **Labels must predict content.** A heading is a promise; the body must keep it. Broken scent ("this section is not what its title suggested") is a deep trust-killer. Test every heading against its content in the verify pass.
- **Navigation and search systems.** For anything large: a table of contents (navigation), consistent anchors and cross-links, and labels chosen from the *reader's* vocabulary, not the author's jargon.
- **The corpus as a findable system.** When organizing many documents, the meta-structure (how they relate and link) matters as much as each document's internals. An entry point / index, consistent labeling, and cross-references turn a pile into a navigable whole.

The single practical rule: **every heading is a promise the body must keep, written in words the reader already uses.**
