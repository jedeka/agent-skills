---
name: succinct
description: Rewrite any text, article, draft, or prior conversation content into its most succinct, minimum-description-length form conveying the same information, preferably lossless, at most slightly lossy where core meaning fully survives. This is compression by rewriting, not summarization. The output keeps everything the input said, strips only redundancy and filler, and stays intuitive rather than cryptic. Use whenever the user says /succinct, "make this succinct", "tighten this", "compress without losing anything", "shorten but keep all the info", or points at text (pasted, attached, or earlier in the chat) and wants it shorter with content intact. Also applies in generation mode, when /succinct accompanies a fresh question, meaning the answer itself must be composed at minimum description length from the start. Do NOT use for digests that discard detail, since a two-sentence gist with action items is ultra-summary, and a meeting write-up is meeting-minutes.
---

# Succinct

Rewrite text into its minimum-description-length form: the shortest version that still conveys everything the original does. This is compression, not summarization. A summary selects what matters and discards the rest; succinct keeps all the information and discards only the words that were not carrying any.

Apply it in two modes:

- **Rewrite mode**: the user points at existing text, pasted, attached, or earlier in the conversation ("make your last answer succinct"). Compress that text.
- **Generation mode**: the user attaches /succinct to a fresh question or task. There is no input text to compress; instead, compose the answer itself at minimum description length. Decide what the complete answer must contain, then write only that. The same standard applies as if a verbose draft had been written and compressed, without ever writing the verbose draft.

## The objective

Think of the input as information wrapped in packaging. The job is to remove the packaging and hand over the information. Formally: find the shortest text from which a reader recovers the same content the original conveyed.

Lossless is the target. Every claim, fact, number, name, qualifier, and logical step in the input should be recoverable from the output. Slightly lossy is acceptable only when the loss is genuinely peripheral, such as collapsing a redundant example when one already makes the point, or dropping a decorative aside, and never when it touches a load-bearing fact, a caveat that changes the claim, or a step the argument needs.

Two failure modes bound the task, and both are failures:

- **Under-compression**: the output still contains filler, repetition, or throat-clearing. The job is not done.
- **Over-compression (absurdizing)**: the output is so terse it becomes cryptic, telegraphic, or ambiguous, and the reader must decompress it by guessing. Compression that shifts work from the writer to the reader has negative value. The output must remain natural, intuitive, and digestible prose that a cold reader understands in one pass.

The optimum sits exactly at the boundary: every word removable without information loss is removed, and every word needed for one-pass comprehension is kept.

## What compression removes

Most text is mostly packaging. The recurring forms:

- **Throat-clearing and meta-commentary**: "It is important to note that", "In this section we will discuss", "As mentioned earlier". These announce information instead of stating it. Delete the announcement, keep the information.
- **Redundancy**: the same point restated in different words, a claim followed by its paraphrase, a conclusion that repeats the body. State each fact once, in its best formulation.
- **Hedging stacks**: "could potentially perhaps" is "may". Keep one hedge when uncertainty is real information; delete the pile.
- **Inflated phrasing**: "due to the fact that" is "because"; "has the ability to" is "can"; "a large number of" is "many". Every inflated idiom has a short exact equivalent.
- **Empty intensifiers and qualifiers**: "very", "really", "quite", "basically", "essentially" almost never change the claim.
- **Redundant examples**: when three examples make the same point, one well-chosen example plus the general statement usually carries it. Keep examples that add distinct information.
- **Passive and nominalized constructions**: "a decision was made by the team to implement" is "the team decided to implement". Verbs beat noun-phrases built from verbs.

## What compression must preserve

- Every distinct fact, claim, number, name, and definition.
- Qualifiers that change meaning: scope ("in most cases"), conditions ("if X"), genuine uncertainty ("preliminary results suggest"). Cutting these is not compression, it is distortion.
- The logical skeleton: if the input argues A therefore B despite C, the output argues exactly that.
- Tone and register at the level that matters: a formal document stays formal, a technical document keeps its technical terms. Compression changes density, not voice.
- Wording that is already optimal. This is rewriting only where rewriting wins; when the original sentence is already at MDL, keep it verbatim. There is no obligation to paraphrase for its own sake.

## Calibration

Output length is whatever the information content dictates, so there is no target ratio and no fixed shape. Dense technical text might compress 15 percent; bloated corporate prose might compress 70 percent. The structure of the input (sections, paragraphs, lists) survives when it organizes information, and dissolves when it was itself packaging.

Unless the user asks otherwise, output only the compressed text. No preamble, no commentary on what was cut, no "here is the tightened version".

## Worked example

**Input**

> It is important to note that, in the vast majority of cases, the performance issues that users have been experiencing are, at the end of the day, fundamentally related to the fact that the database queries being executed are not making use of the indexes that exist. What this essentially means is that, whenever a query is run against the users table, the system is basically forced to perform what is known as a full table scan, which, as one might expect, has the potential to become extremely slow as the size of the table continues to grow over time. In order to address and resolve this particular issue, the recommendation that we are putting forward is that a composite index should be created on the email and created_at columns, which, based on our preliminary testing, could potentially reduce query times by approximately 90 percent, although it should of course be kept in mind that these results are still preliminary in nature.

**Output**

> Most of the performance issues trace to database queries not using existing indexes. Every query against the users table forces a full table scan, which grows slower as the table grows. We recommend a composite index on the email and created_at columns; preliminary testing suggests roughly 90 percent faster queries.

Every fact survives: the cause, the mechanism, the scaling behavior, the exact fix, the measured gain, and the "preliminary" caveat (kept once, because it changes how much to trust the number). What died was only packaging: 148 words became 55 with nothing lost, and the output reads as natural prose, not shorthand.

## Process

1. Determine the mode: existing text to compress (rewrite mode) or a fresh query to answer (generation mode).
2. Build the information inventory. Rewrite mode: every distinct fact, claim, qualifier, and logical link in the input. Generation mode: everything a complete and correct answer must contain, and nothing more. This is the checklist nothing may fall off.
3. Write at MDL: state each inventory item once, in its shortest natural formulation, preserving logical structure and the appropriate register. In rewrite mode, keep original sentences that are already optimal.
4. Verify completeness: check the output against the inventory. Anything missing goes back in, in compressed form.
5. Verify digestibility: read it cold. If any line needs a second pass or a guess to understand, it is over-compressed; add back the minimum words that make it self-evident.
6. Output the compressed text or the succinct answer alone.
