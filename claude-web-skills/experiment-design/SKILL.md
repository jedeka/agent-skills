---
name: experiment-design
description: Design a decisive, pre-registered test before any data is collected or any run happens. Triggers include "design an experiment", "how do I test this", "set up the eval", "is this design sound", "will this experiment answer the question", a surviving idea graduating from rapid-prototyping or honest-iteration, and the design-the-test step of research-loop. It fixes hypothesis, prediction, metric, decision rule, and analysis plan before results exist, forces falsifiability (name the outcome that kills the hypothesis), and plans controls, baselines, ablations, confounds, sample size or budget, multiplicity correction, and holdout discipline, all cost-aware. Output is a pre-registration block that empirical-analysis is bound to. Do NOT use it for a throwaway probe (use rapid-prototyping) or for reading finished results (use empirical-analysis).
---

# Experiment design (decide what results mean before they exist)

After the data arrives, any result can be argued into support — the garden of forking paths is walked backwards and called a plan. The only cure is to make every interpretive decision **before** the data exists. That is the entire skill; everything below is how.

## The invariant

**A test is only decisive if its meaning was fixed in advance.** Hypothesis, prediction, metric, thresholds, and analysis plan are written down before the first run. Anything decided after seeing results is exploratory — sometimes valuable, never confirmatory.

## The pre-registration block (the output)

Write this block; **empirical-analysis** is contractually bound to it:

- **Hypothesis** — one sentence, falsifiable.
- **Prediction** — direction and the *smallest effect size that matters* (not just "different").
- **Metric** — exactly what is measured, exactly how.
- **Decision rule** — thresholds fixed now: what outcome counts as support, what kills it, what is inconclusive.
- **Analysis plan** — the tests to run, the multiplicity correction chosen now.
- **Sample / budget** — how much data or compute, chosen so the design can detect the smallest effect that matters.
- **Holdout plan** — the split made before anyone looks; the test set is touched once.
- **Confounds and controls** — the list, and for each: designed out, measured, or accepted with eyes open.
- **Stop rule** — when the experiment ends, fixed now (no peeking-until-significant).

## Design forces

- **Falsifiability.** Name the concrete outcome that kills the hypothesis. A design that cannot kill it is a demo, not a test.
- **Controls and baselines.** What comparison isolates the effect? Change one thing at a time; always include the dumb baseline — many effects die against it.
- **Confounds.** Enumerate what else could produce the predicted result; design it out or measure it.
- **Multiplicity.** Count every look, variant, metric, and subgroup you might examine — including the implicit ones — and pick the correction now. Uncounted comparisons are how noise gets published.
- **Power per cost.** The cheapest run that still decides; rank designs by expected information per unit cost (exploration-triage's logic, applied inside one experiment).

## Handoffs

Build the apparatus properly → **test-driven-development** (the probe code from rapid-prototyping is a liability now). Run it. Read the results → **empirical-analysis**, holding this block as the contract. Any later deviation is labeled exploratory there, not silently absorbed.
