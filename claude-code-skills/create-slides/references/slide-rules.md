# Slide rules

The user's rules for every deck, in one place, each with the reason behind it. They apply to every
theme and every template. Order of precedence:

1. The user's explicit instructions for this deck.
2. These rules.
3. The design system (`technical-swiss.md`, and the source spec `swiss-design-spec.md` it adapts).
   Where the spec says otherwise, these rules win. For example, the spec's §21 suggests an author or
   lab in the footer, but the footer rule below allows only the page number.

How the rules turn into layout geometry is in `template-authoring.md`. How each one is checked is
in `verification.md`.

The reasons in §5, §6 and §7 are the incidents that produced those rules. The other reasons state
what each rule protects.

## 1. Defaults: leave these off the slide face unless the user asks

| leave off | instead | why |
|---|---|---|
| Person names: authors, collaborators, supervisors, reviewers, "X's rule" | Name the thing: "the decision policy" | Decks get forwarded beyond the room. A name ties a finding to a person, not to evidence. |
| Dates: deadlines, version dates, "as of" stamps | Nothing | A dated slide looks stale as soon as it is reused. |
| Internal identifiers: ticket and decision ids, scene or sample ids, module names, codenames | A gloss in plain words, if the argument needs the thing at all | The audience cannot decode them, and codenames leak project context. |
| File paths and commands | Speaker notes (`<aside class="notes">`) | They are provenance for the presenter, not content for the audience. |
| Logos, agenda slides, "thank you" and "questions?" slides, decoration | Nothing | They take time and space and carry no information. |

## 2. Fidelity: every claim traces to a source

- **Numbers come from the source, never from memory.** Read the file, table or output that holds
  the number. Copy it at the source's precision, or round once from the unrounded value.
  *Why:* rounding an already-rounded number causes off-by-0.01 errors that a reader cannot trace.
- **Conditions stay attached.** Every number carries its population, n, unit and threshold on the
  slide face: in the kicker, the caption or the setting line, not only in the notes. A rate over
  all cases and a rate over a subset say which they are. Two slides that use different
  populations say so. *Why:* a number without its condition is read as a different claim.
- **Label the epistemic status** of every claim:
  - **measured:** stated flat;
  - **inference:** phrased as one ("suggests");
  - **hypothesis:** labelled "hypothesis: …";
  - **illustrative:** an invented example or number is labelled "illustrative" on the face. An
    example drawn from data names its case in the notes.

  *Why:* an unmarked estimate in a table gets quoted later as a measurement.
- **No universal without the case walk.** Before "always", "never", "only" or "every", check each
  case; otherwise write the claim per case. *Why:* one counter-case voids the slide.
- **Cross-check after writing.** For more than a handful of numbers, script the comparison between
  the slides and the source data (`scripts/numtrace.py` does it for any text source), and fix every
  mismatch. A derived number (a sum, a ratio, `n + 1`) is checked the same way: its arithmetic,
  run and saved with its output, is its source. *Why:* errors made while copying are invisible on
  reread.
- **Corrections propagate.** If a later slide qualifies an earlier claim, update the earlier slide
  too. *Why:* the deck must not hold two versions of one fact.

## 3. Writing

- **Titles state the finding.** "The top camera alone is the weakest view", not "Camera results".
  A title fits one line, about 50 characters at 60 px. Definition slides may use a plain label.
  *Why:* many readers read only the titles.
- **One idea per slide.** A slide that needs two titles is two slides. *Why:* two ideas on one
  slide compete for the same 864 px and the same minute of attention.
- **Plain words.** Expand jargon on first use in the deck, in one clause. Write short sentences
  with the actor first. *Why:* a deck is read once, at the speaker's pace.
- **No filler, no hype, no bragging numbers.** Cut "It is important to note", "In this slide",
  "Let's", "Key takeaways:", "In conclusion", and adjectives such as "remarkable" or "dramatic". A
  number appears because the argument needs it, not to impress. *Why:* every filler word displaces
  a fact, and hype costs trust.
- **Numbers as numbers, with units:** "3.74 of 5 labels", not "most labels".
- **Statements, not fragments.** Bullets are full short sentences or label–value pairs, three to
  five per block.
- **One name per thing.** After "per-count threshold", do not switch to a synonym.
  *Why:* a new name reads as a new thing.

## 4. Structure of a deck

1. Cover: title, a one-line subtitle, and optionally 3–4 key counts.
2. How to read: definitions and defaults, when the deck has metrics.
3. Content in parts. Each part opens on its explainer or its strongest finding. Section slides
   (`02-section-title`) come one per part, all parts or none, numbered 01, 02, … in order, and the
   kickers carry the same numbers:
   - three or more parts: section slides are allowed but not required; numbered kickers alone
     ("02 · Camera sets") can mark the parts, as in `example-scenarios/` (four parts, no section
     slides);
   - two parts: numbered kickers only, unless the user asks for section slides; then both parts
     get one;
   - one part: no section slide (it would only repeat the cover) and no part number in the
     kickers.

   A request for section slides, in whatever words ("add a divider"), switches them on for every
   part, a single part included, since the user's instruction comes first. Only an instruction that
   names which parts get one overrides "all parts or none". The cover, a setup or how-to-read
   slide, limits and summary stand outside the parts: no section slide, no part number in their
   kickers (`example-scenarios/` labels them "Setup", "How to read the tables", "Summary").

   A paper explainer follows its own structure: `explainer.py` gives every section a divider, one
   section included, because the linked contents land on them.
4. Limits: what the evidence cannot support.
5. Summary: three to four statements that restate findings already shown, then next steps.

## 5. Footer

- The default footer is the **page number only** ("NN / TOTAL"). The build adds it to every slide
  except the cover and section slides (and any section marked `data-nofooter`).
- A short label left of the number only when the user asks for one.
- **Never a date.** `deck.py` refuses a footer label that looks like one.

*Why:* the user removed a footer that held the deck title and a date. The title is already on the
cover, the date goes stale, and both took space from every slide.

## 6. R7: nothing collides

Before a deck is handed over, check every slide for objects that collide:

- text boxes, images, formulas, shapes or connectors whose boxes overlap;
- text that runs past its box.

Render the slides and look at each one: a screenshot, a PDF export, or the editor's view. Where
rendering is not possible, compute every element's box, test each pair for overlap, and say plainly
which slides were not checked visually.

A height estimate against the margins is not this check. It catches overflow at the bottom, not two
boxes side by side. A large number beside text gets an explicit width with slack, or sits above its
text instead of beside it.

*Why:* in the incident behind this rule, a 72 px bold "35.3%" and its explanatory text sat side by
side in one row and collided. The deck had passed a structure lint, a number trace, a contrast check
and a height estimate. None of those looks at overlap, and the deck had not been rendered.
`verification.md` reproduces the case.

## 7. The printed PDF is checked as well as the screen

Chromium's printed PDF can lay out differently from the screen. An image that shrinks inside a flex
or grid box on screen can print at its natural size and spill under the next element. So:

- freeze image sizes from the checked screen layout before printing (`deck.py pdf` does this);
- check the PDF itself (`deck.py pdf` runs `pdfcheck.py`) for:
  - text overlapping text;
  - text overlapping images;
  - text or an image running into a filled panel's edge;
  - content in the footer band.

*Why:* it happened: images that fitted on screen printed at their natural size and spilled under the
next element, after the screen check had passed. `verification.md` reproduces the case with a
fixture.

## 8. Speaker notes

`<aside class="notes">`, the last child of the section, carries:

- the source of every number (file, section, table);
- the commands that produced the numbers;
- caveats too long for the face;
- the case behind any example drawn from data.

Notes may hold paths and ids; the face may not.

## 9. Writing passes on slide text

Run these on the slide text and the notes: they are step 1 of `verification.md`. Each is a skill
the user invokes for decks. Where one is not installed, do the pass by hand from its description.

| pass | what it does to a deck |
|---|---|
| **unslop** | removes AI writing patterns: filler openers, stock phrases, inflated adjectives, rule-of-three padding |
| **presend** | stamps every number, quote, done-claim, universal and example against evidence obtained now; restates the question; enumerates cases before *only / always / never*; reads the deck for two statements that cannot both be true |
| **simply-explain** | checks that a newcomer can follow each slide in one read: one concrete case before the general statement, each term defined once, conditions and approximations kept and marked |

`python3 <skill>/scripts/deck.py text <deck> --prose` prints every slide's face text and its notes,
the input for these passes: the text as written (a kicker is not in capitals there) and one block
per paragraph, so a sentence checker reads it as prose. Two kinds of line that the rules above
require can draw unslop flags (a restatement, a list of topics) and stay: the summary statements
that restate findings already shown (§4), and a section slide's contents line that lists the
part's slide topics.

## 10. Before delivering

Every step of `verification.md` is done, and the report to the user names anything not verified:
slides not checked visually, numbers not traced, exports not produced.
