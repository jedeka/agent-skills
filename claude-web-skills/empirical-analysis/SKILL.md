---
name: empirical-analysis
description: Read experimental or empirical results into a calibrated claim. Triggers include "analyze the results", "what do these numbers mean", "is the effect real", "did it work", the analyze step after any experimental run, and any results file, metrics table, or backtest needing interpretation. It executes the pre-registered analysis plan as a contract and labels any deviation exploratory, reports effect sizes with uncertainty rather than bare significance, applies the planned multiplicity correction, sweeps for leakage, lookahead, survivorship, and data bugs before believing anything, tests robustness to seeds and reasonable analysis variants, and outputs a calibrated claim (effect, uncertainty, validity conditions, and what observation would change the conclusion). Negative results are reported as results. Do NOT use it to design the test (use experiment-design) or to attack the finished claim (use red-teaming-research).
---

# Empirical analysis (results into a calibrated claim)

Numbers do not speak; readings of numbers do, and most readings flatter the reader. This skill turns raw results into the strongest claim the evidence actually licenses, no more and no less.

## The invariant

**The pre-registration is a contract; analysis executes it.** Run exactly the planned tests with the planned corrections against the planned thresholds. Anything beyond the plan is *exploratory*: label it so, and let it generate hypotheses, never conclusions. Silent deviation from the plan is how a null result becomes a publication.

## Inputs and output

Inside a research-loop project, read `experiments/<slug>/protocol.md` (the frozen pre-registration) and `experiments/<slug>/results/` (what the run wrote), and write `experiments/<slug>/analysis.md`. Standalone, the pre-registration block and the results the user supplies play the same roles. Compute from the results files with code, and keep the code or the command in `analysis.md`; a number typed from memory of the run is not a result. `analysis.md` has these sections, in order: **Artifact sweep**, **Pre-registered result** (the decision rule's output, SUPPORTED, KILLED or INCONCLUSIVE, with the effect and its interval), **Robustness** (the runs the protocol's robustness plan named), **Exploratory** (everything outside the plan, labeled), **Calibrated claim**, **Would change it**.

## Before belief: the artifact sweep

A result you have not tried to explain away is not yet a result. Before interpreting, hunt the boring explanations: data leakage between splits, lookahead into the future, survivorship in the sample, duplicated or degenerate data, a metric computed wrong, a broken control. Too-good-to-be-true is a diagnosis, not a celebration: route genuine weirdness to **anomaly-hunting** and outright failures to **debug**. Only what survives the sweep gets read.

## Reading the numbers

- **Effect size with uncertainty, not bare significance.** Report how big, with an interval; then judge *practical* significance against the smallest-effect-that-matters from the design. A tiny certain effect and a huge uncertain one are different claims.
- **Multiplicity honestly.** Apply the correction chosen at design time. Where selection occurred anyway (many variants tried, best reported), deflate: in quant, report the probability of backtest overfitting and deflated performance, never the raw best run.
- **Robustness.** Run the seeds, perturbations and alternative analyses the protocol's robustness plan named; they are part of the contract, not deviations. A conclusion that moves when the analyst sneezes is not a conclusion. A robustness check the plan did not name is exploratory, and says so.

## The calibrated claim (the output)

One block, statuses per grounded-claims: *Effect X of size Y ± Z, under conditions C, by the pre-registered test, decision rule: SUPPORTED | KILLED | INCONCLUSIVE; exploratory observations [labeled]; the observation that would change this conclusion is [W].* Write it so that knowledge-synthesis can copy it into a claim record: the claim sentence with its conditions inside, the effect with its interval, the decision rule's output, and the path of this `analysis.md`. Null and negative results get the identical treatment: a KILLED rule closes a branch, which is progress, and research-loop records the death under `## Killed hypotheses` so the idea stays dead; standalone, say plainly that the hypothesis is dead and why.

## Who certifies

The decision rule certifies; this skill computes it. Because the rule was fixed before the data, its output on the planned test is the one promotion an empirical claim can receive: SUPPORTED makes the claim DERIVED, with `Certified by: experiments/<slug>/analysis.md, SUPPORTED`; KILLED makes the negation DERIVED and kills the hypothesis; INCONCLUSIVE promotes nothing: the claim stays CONJECTURED with `Certified by: NONE`, and the `analysis.md` is named in its warrant as the run that did not decide. No later step can raise this status: not a red team that finds nothing, not the synthesis, not a convincing story. The red team can lower it, by narrowing the conditions or retiring the claim, and that is its only power over it. An exploratory finding, however striking, enters the record as CONJECTURED with a prior, and earns its own protocol if it matters.

## Routes

Inside research-loop, `analysis.md` waits for the outer loop: **knowledge-synthesis** folds the claim into `proposed.md`, **red-teaming-research** attacks the proposal, and research-loop merges the survivors into `findings.md`. Standalone, hand the claim to **knowledge-synthesis**, which writes the record and sends it to **red-teaming-research**. A conjecture under test (from **disciplined-invention**) is promoted or buried by the same rule.
