# Domain moves

Each field goes wrong in its own way when it is simplified. Read the section for the topic's field before you build the route. Each section gives the shape of a good concrete case, the moves that work, and the carriers of rigor most at risk.

## Contents

- [Mathematics and proofs](#mathematics-and-proofs)
- [Algorithms and code](#algorithms-and-code)
- [Systems and architecture](#systems-and-architecture)
- [Physical and life sciences](#physical-and-life-sciences)
- [Statistics and machine learning](#statistics-and-machine-learning)
- [Papers and research results](#papers-and-research-results)
- [Law, finance, and medicine](#law-finance-and-medicine)

## Mathematics and proofs

**The case.** The smallest example that is not degenerate. For a theorem about matrices, use a 2-by-2 matrix of whole numbers.

- State a theorem in words before symbols.
- Say what each hypothesis is for. Remove the hypothesis and show the case that breaks.
- For a proof, give the one-sentence reason the result must be true, then the steps. Say which of the two the text offers: an intuition is not a proof.
- Keep three kinds of statement apart: a definition is a choice, a theorem is a consequence, and a convention is a habit of notation.
- Read each formula aloud once. Say what the left side measures and what the right side is built from.

**At risk.** Quantifiers and their order: "for every x there is a y" differs from "there is a y for every x". Conditions. "If" versus "if and only if".

## Algorithms and code

**The case.** One concrete input, traced from entry to return, with the state shown after each step.

- Read the code before you explain it, and cite the file and line.
- Name the invariant: the fact that holds at every step and makes the result correct.
- Give the cost with its variable and its kind: "in the worst case, time grows in proportion to n log n, where n is the number of items".
- Separate what the code does from why someone wrote it that way. The code shows the first. The second needs a source, such as a commit message, or a label that marks it as an inference.
- For an error message, give four things: what the program was trying to do, what it expected, what it found, and where the two diverged.

**At risk.** Edge cases: empty input, one item, duplicates. "Average" versus "worst". Behavior under concurrency.

## Systems and architecture

**The case.** One request, followed from the user's action to the stored result and back.

- Name each component by its job. Give each one sentence: what it receives, what it returns, what it keeps.
- For each component, say what happens when it fails. Behavior under failure is what defines a guarantee.
- Use the exact name of each guarantee and define it: "at-least-once delivery: every message arrives, and some arrive twice".
- Draw the request path. A figure nearly always helps here.

**At risk.** "Always" written where "in normal operation" is true. Latency given as one number with no percentile. "Consistent" and "available" used loosely.

## Physical and life sciences

**The case.** One observable event with its magnitudes: a 70 kg person, a 3 m fall.

- Build the mechanism as a causal chain with a quantity at each link.
- Name the model. Every scientific explanation holds inside a model: "in the ideal-gas model". Say where the model stops matching measurement.
- Say how the claim is known: the experiment, the measurement, the observation.
- Replace purpose language with cause. "The cell wants to conserve energy" becomes "cells that used less energy survived more often".

**At risk.** A model stated as reality. Correlation presented as cause. Orders of magnitude.

## Statistics and machine learning

**The case.** A count of people or events, small enough to hold in the head.

- State what is random and what is fixed. Most misreadings start here.
- Keep the direction of every conditional. The probability of the data given the hypothesis is not the probability of the hypothesis given the data.
- Use counts in place of percentages. "Of 1,000 people, 10 have the disease, and the test finds 9 of them. Of the 990 others, 89 also test positive. So 98 people test positive, and 9 of them are ill: about 9%."
- Separate the population from the sample, and a parameter from its estimate.
- For a model, give four things: what goes in, what comes out, what training adjusted, and what quantity training minimized. Trace one input through.

**At risk.** "Significant", which has a statistical sense and an everyday sense. Accuracy quoted without the base rate. A confidence level, which describes the procedure and not one interval. Mental verbs: "the model knows", "the model understands".

## Papers and research results

**The case.** The paper's main experiment: who or what was measured, how, and what number came out.

- Write the ledger as five lines: the claim, the evidence, the size of the effect, the conditions, and what the authors did not test.
- Separate what the authors showed from what they suggest. An abstract often blends the two.
- Give an effect with its baseline: "from 12% to 9%". A relative figure alone, "25% lower", hides the size.
- Say what result would change the conclusion.

**At risk.** Strength: a preprint, one study, or a replicated result. Scope: mice or people, a benchmark or real use. Relative versus absolute numbers.

## Law, finance, and medicine

**The case.** One person in one situation, with the date and the place.

- Treat conditions and definitions as the content. A rule has four parts: whom it binds, when it applies, what it requires, and what follows otherwise.
- Keep the jurisdiction and the date. Rules differ by place and change over time.
- Give a risk as a count with a denominator and a time span: "2 in 1,000 people over ten years".
- Explain, and do not advise. Say what the term or rule means. Say once that a decision about the reader's own case needs a professional who knows the facts.

**At risk.** "May", "must", and "shall". Exceptions. Defined terms that look like everyday words: "consideration", "material", "positive".
