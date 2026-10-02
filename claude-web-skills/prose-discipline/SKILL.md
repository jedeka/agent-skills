---
name: prose-discipline
description: Use this skill whenever prose is being written, edited, or reviewed and it must not read as generic AI output. Triggers include "write this up", "edit this", "make this tighter", "does this sound like AI", "clean up the prose", drafting any document, post, summary, or message, and the final pass on anything a human will read. It removes the recognizable AI tells (filler openers, hedging adverbs, mechanical "not X but Y" contrasts, false agency where things do human verbs, narrator-from-a-distance voice, three-item cadence, em dashes, vague declaratives, pull-quote padding), and enforces active voice, named actors, specificity, and varied rhythm. Pairs with organize (structure) and knowledge-synthesis (which supplies the claims this renders). Do NOT use it to restructure or architect a document (use organize) or to check factual accuracy (use grounded-claims).
---

# Prose discipline (cut the tells)

Capable models write fluent prose with a recognizable fingerprint: hedged, padded, symmetrical, and weightless. The fix is mostly subtraction and one rule, active voice with a named actor, applied relentlessly. Good prose states things; it does not announce, hedge, or perform.

## The invariant

**Every sentence has a subject doing something, and every word earns its place.** Passive voice hides the actor and drains energy; filler and hedging dilute the point; padding insults the reader. If a word can be cut without loss, cut it. If a sentence announces an insight instead of delivering it, delete the announcement and keep the insight.

## Core rules

- **Active voice, named actor.** Find who did the thing and put them first. "The team shipped it Friday," not "it was shipped" and not "the decision was reached." Inanimate things do not perform human verbs: data does not "tell us," a complaint does not "become a fix," a culture does not "shift." Name the person, or use "you" to put the reader in the seat.
- **Cut filler and hedges.** Remove throat-clearing openers ("here's the thing," "it's worth noting," "in today's world") and empty adverbs ("really," "very," "just," "simply," "genuinely," "honestly," "actually," "literally"). They add length and subtract force.
- **State Y directly.** Drop the mechanical contrast. "Not X, but Y" / "it isn't X, it's Y" / "the question isn't X, it's Y" telegraphs a reversal the reader does not need. Say Y.
- **Be specific.** Replace vague declaratives ("the implications are significant," "the reasons are structural") with the specific implication or reason. Replace lazy extremes ("every," "always," "never," "everyone") with the actual scope.
- **Put the reader in the room.** Prefer concrete scenes and "you" to the narrator-from-a-distance voice ("nobody designed this," "people tend to," "this is why"). Specifics beat abstractions.
- **Vary the rhythm.** Mix sentence lengths; do not stack short staccato fragments for drama. Two items often beat a reflexive three. End paragraphs differently, not always on a punchy one-liner.
- **No em dashes.** Use a comma, a period, a colon, or parentheses. None at all.
- **Trust the reader.** State facts without softening, over-justifying, or hand-holding. Cut sentences that exist only to reassure or to preview ("the rest of this section will...").
- **No pull-quotes.** If a line sounds engineered to be quotable, rewrite it plainer.

The catalogue of specific patterns to hunt, with fixes, is in `references/ai-tells.md`.

## The pre-delivery pass

Before handing over prose, scan for and fix:

- any passive voice (find the actor, move them to the front);
- any inanimate thing doing a human verb (name the actor);
- any empty adverb or filler opener (cut);
- any "not X, it's Y" contrast (state Y);
- any em dash (replace);
- any vague declarative (name the specific thing);
- three consecutive sentences of the same length (break one);
- any sentence that announces rather than states (delete the announcement).

## A light rubric (when a verdict helps)

Score 1 to 5, and revise anything low: **directness** (states or announces?), **specificity** (named things or vague gestures?), **rhythm** (varied or metronomic?), **density** (anything cuttable?), **voice** (sounds like a person or a template?). Density and directness are the two that matter most.

## Output

The revised prose. When asked, also a short list of what was cut and why, so the pattern is visible and repeatable. This skill governs *how* it reads; the claims themselves come from **knowledge-synthesis** and keep their provenance via **grounded-claims**, and the structure comes from **organize**.
