# Method

How to do each step of the procedure well, and why each step works.

## Contents

- [Four ways to simplify](#four-ways-to-simplify)
- [What must survive](#what-must-survive)
- [The ledger](#the-ledger)
- [The reader](#the-reader)
- [The route, stage by stage](#the-route-stage-by-stage)
- [Devices that build intuition](#devices-that-build-intuition)
- [Analogies](#analogies)
- [Depth and layers](#depth-and-layers)
- [When the topic resists](#when-the-topic-resists)
- [The rewrite flow](#the-rewrite-flow)
- [The check flow](#the-check-flow)
- [Failure modes](#failure-modes)

## Four ways to simplify

| Move | What it does | Rule |
|------|--------------|------|
| Omit | Leaves detail out. | Allowed. Name the omission when it would change a decision or a prediction. |
| Approximate | States something close to true. | Allowed with its range: "for small angles", "to within 1%". |
| Reorder and illustrate | Changes the order of ideas, adds a case or a figure. | Always allowed. Most of the gain comes from here. |
| Falsify | States something false because it is easier to say. | Never. |

The line between omitting and falsifying is whether the sentence can be extended. "A p-value measures how surprising the data are if there is no effect" omits the detail, and a later course builds on it. "A p-value is the chance that the result is a fluke" is false, and a later course has to remove it.

One tempting move is a quiet falsification: replacing a technical term with a softer everyday word. The everyday word has a wider meaning, so the claim changes, and the reader loses the word they need to search with. Keep the real term and define it.

## What must survive

Eight things carry the rigor of a claim. A simplification that drops one of them states a different claim.

1. **Definitions.** The exact boundary of each term.
2. **Quantifiers.** All, some, at least one, exactly one, on average.
3. **Conditions.** The assumptions under which the claim holds.
4. **Direction.** Cause versus correlation. A given B versus B given A. Necessary versus sufficient.
5. **Quantities.** Numbers, units, and orders of magnitude.
6. **Strength.** Proven, measured, estimated, conjectured, disputed.
7. **Scope.** Which cases the claim covers and which it does not.
8. **Names.** The standard term, so that the reader can look it up.

## The ledger

The ledger is a short list of the claims that an expert would insist on. Write it for an expert reader, before any thought about wording for the real reader.

A ledger for "what is a hash table?":

- It stores key-value pairs in an array of numbered slots.
- A hash function maps each key to a slot number. The same key always gives the same number.
- Lookup, insert, and delete take constant time on average, whatever the number of entries.
- Two keys can map to one slot. This event is a collision, and the table needs a rule to handle it.
- In the worst case, when many keys collide, an operation takes time proportional to the number of entries.
- The average-case claim assumes that the hash function spreads keys evenly and that the table grows as it fills.

The explanation may present these in any order and at any length. It may not turn "on average" into "always", and it may not leave out collisions, because the average-case claim rests on them.

Mark where each line comes from: checked now, known, or uncertain. Verify the uncertain lines or carry the uncertainty into the text. A ledger line that you cannot source is a line that the explanation should not assert.

## The reader

Three readers cover most requests.

| Reader | Has | Needs |
|--------|-----|-------|
| Newcomer | General knowledge only. "ELI5" means this reader; it removes prerequisites, and it does not license false statements. | Every term defined. A case from daily life. |
| Outsider (default) | Training in another field. Reads carefully. | The vocabulary, and the reason the idea exists. |
| Practitioner | The field's vocabulary and nearby ideas. | The precise statement early, then how it differs from what they already use. |

List what the explanation requires and mark each requirement as present or missing for this reader. A missing requirement that is one step away gets a one-sentence definition in place. A missing requirement that is many steps away gets named as a prerequisite, with a two-line version: "This rests on conditional probability. In two lines: ...".

Detail that helps a newcomer slows a practitioner. Do not re-explain what the reader has shown that they know.

## The route, stage by stage

**1. The problem.** Ideas were invented to fix something. Show the thing that was broken: the query that took an hour, the measurement that two observers disagreed on. The reader who has felt the problem can judge whether the idea solves it.

**2. One concrete case.** Choose the smallest case that still shows the behavior. A list of one item hides how a sort works, and a list of a hundred cannot be followed; a list of four works. Use real values and show each intermediate state. Keep the same case to the end, because each new case makes the reader rebuild the picture. A second case belongs in a `deep` explanation, and its job is to stress a condition: show the rule failing when a hypothesis is removed.

**3. The mechanism.** Walk the causal chain, one link per sentence, and join the links with "because" and "so". Test each link: could the reader, at that point in the text, say why it follows? If a link needs a fact the reader lacks, state the fact there.

**4. The precise statement.** State the general rule in words, then in symbols if the field uses them. Tie each symbol to the case: "here n is the 100 flips". Give the standard name and the conditions.

**5. The limits.** Give the boundary where the idea stops being true. Name the neighbor that it gets confused with and the difference between the two. If a wrong picture is common, state it, mark it as wrong, and give the reason it fails. A direct refutation changes a reader's mind more reliably than a correct account that never mentions the error.

## Devices that build intuition

An explanation feels intuitive when the reader could have predicted the result. These devices give the reader that ability and cost no rigor.

- **Extreme cases.** Set a quantity to zero, to one, or to something very large, and read off what the rule says. A formula that gives nonsense at the extremes is wrong, and a formula that behaves well there is easier to believe.
- **Change one input.** Hold everything else fixed, move one quantity, and say what else moves and in which direction.
- **Two forms of one fact.** Give a number with a picture, or a formula with a sentence. Each form covers what the other hides.
- **Units.** Carry the units through a calculation. They show what each quantity measures.
- **The naive attempt.** Show what a reasonable person would try first, and where it fails. The idea then arrives as the repair.
- **The invariant.** Say what stays the same while everything else changes.
- **By hand.** Do the smallest case with pencil-sized numbers before the general rule appears.

## Analogies

An analogy is a different thing with the same structure. Because it is a different thing, it has properties that the target lacks, and the reader will carry those over unless told otherwise.

Four conditions make an analogy safe:

1. Use one. A second analogy has a second set of false properties.
2. Say what maps to what.
3. Say where the mapping breaks.
4. Return to the real terms afterward.

Example: electric current as water in pipes. Pressure maps to voltage, flow rate maps to current, and a narrow section maps to a resistor. The mapping breaks at an open end: water pours out of a cut pipe, and charge does not pour out of a cut wire, so an open circuit carries no current.

## Depth and layers

Build the answer in layers: one sentence, then one paragraph with the case, then the full route. Each layer is complete and true without the next, so the reader can stop at any layer and keep a correct picture. `brief` is the first two layers.

When the true answer is "it depends", name the variable it depends on, and give the answer for each main value of that variable.

When the field does not know, say that it does not know. When experts disagree, give each position and the evidence it rests on. An explanation that hides an open question fails the unlearn test.

## When the topic resists

Some ideas sit at the end of a long chain of prerequisites. There are two honest options.

- Say what can be said truthfully at this level, and mark what is left out.
- Give the chain of prerequisites in order, each with its two-line version, and let the reader choose how far to go.

A third option is not honest: an analogy presented as if it were the idea. If an analogy is all that this level allows, label it as an analogy and state the one thing that it gets right.

## The rewrite flow

1. Extract the ledger from the supplied text: its claims, numbers, conditions, and strength. If the source is wrong or unclear on a point, report the point. Do not repair facts silently.
2. Diagnose the text with the checker and the four tests.
3. Rebuild along the route. Keep the source's terms, numbers, citations, and code verbatim.
4. Compare the result with the ledger. The rewrite adds no claim and loses none.

Return the rewritten text. Add one or two lines on what moved only when the user asked for the reasoning.

## The check flow

Run the checker, apply the four tests, and change nothing. Report in this shape:

```markdown
## Verdict

Followable: [yes / no, with the first place a reader at this level gets lost]
True: [yes / no, with the first sentence an expert would reject]

## Findings

- [quoted span] — [rule or test] — [what the reader loses] — [suggested fix]

## What works

- [what to keep]
```

Order the findings by harm to the reader: false statements first, missing steps second, wording last.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| A definition built from undefined terms. | The text started at stage 4. | Start from the case. |
| Three analogies in a row. | The mechanism was never found. | Find the mechanism. Keep one analogy, mapped. |
| `Simply`, `clearly`, `just`. | A link was skipped. | Write the link. |
| A softer word in place of the real term. | Fear of jargon. | Keep the term and define it. |
| Conditions dropped. | Compression. | Restore them from the ledger. |
| Caveats piled up before the point. | Rigor displayed instead of used. | Point first. Each caveat goes where it binds. |
| A history of the field. | History is easier to write than the idea. | Cut it, unless the history is the reason. |
| A survey of approaches when one answer was asked for. | Reluctance to commit. | Give the answer. Name the alternatives in one line. |
| Notation explained, idea missing. | Symbols came first. | Words first. |
| The example changes midway. | Convenience. | One case. |
| Every sentence short and the same length. | The limit was used as a target. | Vary the length. Join ideas with connectives. |
