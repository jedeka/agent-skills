---
name: rapid-prototyping
description: Use this skill whenever the user wants to test an idea, assumption, or approach as fast as possible with throwaway code or a quick experiment. Triggers include "quick prototype", "spike", "does this even work", "hack something together", "proof of concept", "try this fast", "just see if", "rough version". Use this to execute a single fast probe that attacks the riskiest assumption and produces one clear signal, deliberately cutting every corner that does not matter. Do NOT use this for production code, for code others will depend on, or once an idea has survived and needs to be built properly (switch to experiment-design and test-driven discipline then).
---

# Rapid prototyping (spike)

Goal: get a real signal on the riskiest assumption as fast as possible. This phase **inverts normal engineering discipline** — the code should be sloppy and the thinking rigorous. The model's defaults are backwards for this: it tends to write careful code and draw sloppy conclusions. Flip both.

## Cut every corner that does not matter — this is correct here

- Hardcode values. Skip error handling. No abstractions, no classes, no config files. One ugly script. Copy-paste freely. **No tests.** This is throwaway code; writing it cleanly is wasted time. Actively resist the urge to make it nice.
- **Build only the crux.** Stub, fake, or mock everything that is not the risky part. Use the smallest data, smallest model, fewest examples, and toy or synthetic inputs — whatever still shows the signal.

## Stay rigorous exactly where it counts — the signal

- **Decide the verdict before running.** State, in advance, what observation means "the crux holds" versus "it fails." If you cannot tell from the output which one happened, the probe is malformed — fix it before running, not after.
- **Make the result unambiguous and visible.** Print it, plot it, eyeball it. One number or one picture that settles the question.
- **Fix the random seed** so the result is signal, not noise — but build no infrastructure beyond that one line.
- **Time-box it.** Set a hard limit before you start. If the crux is not resolved when you hit the limit, that *is* the result: the thing is harder than it looked, and feasibility just dropped.

## When it works, do not believe it yet

A fast probe that "works" is the most dangerous output in exploration. Before celebrating, run one quick adversarial check: could this be a false positive — a leaked answer, a too-easy case, a bug that fakes success? (Full check: honest-iteration.) Then report the signal and a one-line verdict: **crux resolved — yes / no / unclear** — and what it implies for feasibility.
