---
name: honest-iteration
description: Use this skill throughout any fast exploration or hyper-iteration loop to keep it honest and bounded. Triggers include "is this result real", "am I fooling myself", "should I keep going on this", "it works", "when do I stop", "I've been stuck on this", or any moment a quick experiment seems to succeed or an idea is eating too much time. Use this to catch false positives before building on them, to enforce a stopping rule against sunk cost, to keep a lightweight log of what was tried, and to decide when an idea has survived enough to graduate from sloppy exploration to rigorous development. Do NOT use this as the final rigorous analysis itself (use empirical-analysis) or to attack a finished published claim (use red-teaming-research).
---

# Honest iteration

Fast iteration has exactly two fatal failure modes. This skill guards against both and nothing else — adding more would make it the ceremony it exists to prevent.

## Failure mode 1: self-deception (the dangerous one)

Moving fast, with no test suite and emotionally invested in a hit, you are the easiest person to fool — and you fool yourself fastest at the exact moment a probe "succeeds." Before promoting any *it works*, run the cheapest **disconfirming** probe: change the seed, the data, or the case and see whether the result survives. A result that vanishes under a perturbation that should not matter was never real. Common ways a fast probe lies are catalogued in references/false-positives.md.

## Failure mode 2: rabbit-holing (sunk cost)

- **Pre-commit a budget** (time or attempts) per idea. When you hit it with the crux unresolved, **stop**. The effort already spent is irrelevant to whether to continue — only expected remaining information ÷ cost matters. Killing an idea fast is success, not failure; most ideas should die.
- **Breadth smell:** if you have gone several probes deep on one idea while others sit unprobed, that is sunk cost talking. Return to the triage queue.

## Capture (this is what makes it a search, not a random walk)

One line per probe: **tried X → saw Y → learned Z → next W.** A running log, not documentation. It stops you re-exploring dead ends and lets partial insights compound across attempts.

## The graduation (the most important call)

The moment an idea *survives* — crux resolved, false-positive check passed — exploration is **over** for it. Stop cutting corners. The sloppy probe code is now a liability: hand off to the rigorous phase (experiment-design, test-driven development, empirical-analysis), where correctness becomes load-bearing and the throwaway code is rebuilt properly. Naming this boundary is the whole point: sloppiness is correct *before* it and reckless *after* it.

## Output

Per idea: a verdict — **dead / still live / graduate** — plus the one-line log entry, and if graduating, the handoff to the rigorous phase.
