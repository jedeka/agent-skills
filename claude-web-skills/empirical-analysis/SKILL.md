---
name: empirical-analysis
description: Read experimental or empirical results into a calibrated claim. Triggers include "analyze the results", "what do these numbers mean", "is the effect real", "did it work", the analyze step after any experimental run, and any results file, metrics table, or backtest needing interpretation. It executes the pre-registered analysis plan as a contract and labels any deviation exploratory, reports effect sizes with uncertainty rather than bare significance, applies the planned multiplicity correction, sweeps for leakage, lookahead, survivorship, and data bugs before believing anything, tests robustness to seeds and reasonable analysis variants, and outputs a calibrated claim (effect, uncertainty, validity conditions, and what observation would change the conclusion). Negative results are reported as results. Do NOT use it to design the test (use experiment-design) or to attack the finished claim (use red-teaming-research).
---

# Empirical analysis (results into a calibrated claim)

Numbers do not speak; readings of numbers do, and most readings flatter the reader. This skill turns raw results into the strongest claim the evidence actually licenses — no more, and no less.

## The invariant

**The pre-registration is a contract; analysis executes it.** Run exactly the planned tests with the planned corrections against the planned thresholds. Anything beyond the plan is *exploratory*: label it so, and let it generate hypotheses, never conclusions. Silent deviation from the plan is how a null result becomes a publication.

## Before belief: the artifact sweep

A result you have not tried to explain away is not yet a result. Before interpreting, hunt the boring explanations: data leakage between splits, lookahead into the future, survivorship in the sample, duplicated or degenerate data, a metric computed wrong, a broken control. Too-good-to-be-true is a diagnosis, not a celebration — route genuine weirdness to **anomaly-hunting** and outright failures to **debug**. Only what survives the sweep gets read.

## Reading the numbers

- **Effect size with uncertainty, not bare significance.** Report how big, with an interval; then judge *practical* significance against the smallest-effect-that-matters from the design. A tiny certain effect and a huge uncertain one are different claims.
- **Multiplicity honestly.** Apply the correction chosen at design time. Where selection occurred anyway (many variants tried, best reported), deflate: in quant, report the probability of backtest overfitting and deflated performance, never the raw best run.
- **Robustness.** Re-run across seeds and small perturbations; try the reasonable alternative analyses. A conclusion that moves when the analyst sneezes is not a conclusion.

## The calibrated claim (the output)

One block, statuses per grounded-claims: *Effect X of size Y ± Z, under conditions C, by the pre-registered test; confidence [level and why]; exploratory observations [labeled]; the observation that would change this conclusion is [W].* Tag it DERIVED — from data through the stated chain — never as bare fact. Null and negative results get the identical treatment: they close branches, which is progress; log them via **honest-iteration** so dead ideas stay dead.

## Routes

The claim goes to **red-teaming-research** before it enters findings — analysis produces the claim, it does not certify it. Survivors feed **knowledge-synthesis** and, for conjectures under test, the status promotion in **disciplined-invention**.
