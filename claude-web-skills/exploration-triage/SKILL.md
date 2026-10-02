---
name: exploration-triage
description: Use this skill whenever the user has several candidate ideas, approaches, or directions and needs to decide which to try first and how to test feasibility fastest. Triggers include "which idea should I try", "is this feasible", "how do I test this quickly", "where do I start", "too many directions", "de-risk", "what's the fastest way to find out". Use this at the front of any exploration or hyper-iteration loop, before building anything, to turn vague ideas into an ordered queue of cheap kill-experiments. Do NOT use for executing a single probe (use rapid-prototyping) or for the careful pre-registered experiment that follows once an idea survives (use experiment-design).
---

# Exploration triage

Exploration optimizes **information per unit cost**, not correctness. Given several candidate ideas, the job is to find the fastest path to a feasibility verdict on each, and to spend probes in the order that buys the most certainty per minute. Most ideas are bad; the prior is NO; optimize for fast rejection, not confirmation.

## For each candidate, do three things

1. **Name the crux.** The single riskiest assumption — the thing most likely to kill the idea, not the parts you already know will work. If the crux holds, the idea is probably feasible; if it fails, the idea is dead. Ask: "what has to be true here that I'm least sure of?"
2. **Design the cheapest falsifying probe.** The ten-minutes-to-an-afternoon version that could show the crux *fails*. Tune the probe to produce a fast NO, not a careful YES. If even the cheapest probe takes days, the crux isn't sharp enough — decompose it, or find a proxy (smaller data, a toy version, a back-of-envelope estimate, a single hard example).
3. **Estimate information ÷ cost.** Roughly: how much does this probe move your belief about feasibility, divided by how long it takes to run?

## Order the queue

- Run the highest-information, cheapest, most-likely-to-kill probe **first**. Front-load the experiments that could end an idea quickly — a day spent killing three dead ideas beats a day spent half-building one.
- **Breadth before depth.** When several ideas are live, probe several of them shallowly before going deep on any one. A single probe is high-variance; committing to the first idea that looks good is a one-armed-bandit error. Parallelize independent probes.

## Output

A probe queue: for each idea, its crux, its cheapest kill-probe, the rough cost, and the run order — plus which probes can run in parallel. Hand each probe to rapid-prototyping.

Keep this to minutes. Triage is not a research plan; if it feels like one, you are over-thinking the front of the loop.
