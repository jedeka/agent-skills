---
name: research-loop
description: >-
  Use this skill to run or manage a multi-step research or build project end to end, rather than a single isolated task. Triggers include "start a research project", "investigate X thoroughly", "run experiments on", "drive this to a conclusion", "manage this investigation", "keep going until you've figured out", resuming a project where research-state.yaml exists, or any open-ended effort that spans many steps or sessions. It is the conductor: it maintains state on disk (research-state.yaml, findings.md, research-log.md, per-hypothesis folders), runs an inner experiment loop and an outer synthesis loop, and routes each sub-task to the specialist skill (deep-research, experiment-design, test-driven-development, empirical-analysis, red-teaming-research, knowledge-synthesis, and the rest). Do NOT use it for a single self-contained task that one specialist skill already covers (call that skill directly).
---

# Research loop (the conductor)

You are a research project manager, not a domain expert. You orchestrate; the specialist skills execute. Your job is to keep a long effort coherent across many steps and sessions: hold the question, maintain state on disk, run the two-loop engine, route each sub-task to the right skill, and steer.

## The invariant

**State lives on disk, not in the context window.** A project that exists only in the conversation dies at the first compaction, crash, or new session, and re-explores its own dead ends. Before the first experiment, write the state scaffold to disk and update it as you go. Continuity is the difference between a search and a random walk. This is mandatory; everything else supports it.

## Step 0: set up state (before anything else)

Initialize a workspace at the project root from `templates/`:

```
{project}/
  research-state.yaml     # the live state: question, hypotheses, status, next action
  research-log.md         # append-only timeline: tried X, saw Y, learned Z, next W
  findings.md             # the evolving synthesis: what we now believe and why
  literature/             # sources, with provenance (see deep-research, grounded-claims)
  experiments/{slug}/     # per hypothesis: protocol.md, code/, results/, analysis.md
  src/                    # reusable code, written once, not duplicated per experiment
  data/                   # raw result data, named descriptively for later re-analysis
  artifacts/              # reports, the final write-up
```

Read `references/state-and-continuity.md` for the schema and the resume protocol. On resume, read `research-state.yaml` first and continue from `next_action`; do not restart.

## The two-loop engine

```
BOOTSTRAP (once, light)
  Sharpen the question -> survey the landscape (deep-research) -> form 2-4 hypotheses

INNER LOOP (fast, repeating)
  pick hypothesis -> design the test (experiment-design) -> build it (test-driven-development)
  -> run -> analyze (empirical-analysis) -> record result + log -> next
  Target: each pass produces one decisive, measurable outcome

OUTER LOOP (periodic, reflective)
  review accumulated results -> find the pattern -> update findings.md
  -> red-team the emerging story (red-teaming-research) -> new or killed hypotheses -> steer
  Target: synthesis and direction. This is where novelty comes from.

FINALIZE
  distill (knowledge-synthesis) -> write up (organize, grounded-claims) -> archive
```

The two loops are a rhythm, not a railroad. Step back to the outer loop when roughly 5 to 10 inner passes have accumulated, when a pattern appears, or when progress stalls. Return to literature whenever results surprise you. Pivot the question if experiments reveal it was the wrong question. Most real projects loop back to the literature and regenerate hypotheses several times.

## Routing: orchestrate, do not improvise

When a sub-task is itself a discipline, hand it to the specialist rather than doing a worse version inline. The full map is in `references/routing-map.md`; the spine:

- Gather evidence on a topic -> **deep-research**
- Generate candidate ideas / reframes -> **research-ideation**, then triage with **exploration-triage**
- A quick "does this even work" probe -> **rapid-prototyping**, kept honest by **honest-iteration**
- Design a rigorous test before collecting data -> **experiment-design**
- Build the real thing correctly -> **test-driven-development** and **surgical-coding**
- Diagnose a failure -> **debug**
- Read the results into a calibrated claim -> **empirical-analysis**
- Stress-test any claim or the emerging story -> **red-teaming-research**
- Notice and chase what does not fit -> **anomaly-hunting**
- Distill gathered material into durable knowledge -> **knowledge-synthesis**
- Any factual claim, anywhere -> provenance via **grounded-claims**
- Write it up -> **organize**

## Autonomy and the human

Keep moving on your own judgment; do not stop to ask permission at every step. Surface progress to the human at outer-loop boundaries (a short findings update or an artifact), so they can redirect, but do not block on them between routine steps. The default is forward motion with a visible trail, not a stream of questions.

## Discipline against the two long-horizon failure modes

A long loop fails in two ways, and the state scaffold guards both. **Drift:** without a written record, a 90-minute session re-tries fixes it already ruled out; the log and `research-state.yaml` prevent this, so consult them before each pass. **Sunk cost:** a hypothesis that has eaten its budget with the crux unresolved should be killed, not nursed; pre-commit a budget per hypothesis (this is honest-iteration's stopping rule, applied at project scale). Killing a hypothesis fast is success.

## Output (per outer-loop turn and at finalize)

- Updated `findings.md`: what we now believe, each claim with its support and status.
- Updated `research-state.yaml`: hypotheses with verdicts, and the single `next_action`.
- A short human-facing note: progress, the current best answer, open gaps, and what is next.
- At finalize: the distilled knowledge artifact (knowledge-synthesis) and the write-up.
