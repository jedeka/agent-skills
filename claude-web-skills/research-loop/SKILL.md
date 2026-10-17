---
name: research-loop
description: >-
  Use this skill to run or manage a multi-step research or build project end to end, rather than a single isolated task. Triggers include "start a research project", "investigate X thoroughly", "run experiments on", "drive this to a conclusion", "manage this investigation", "keep going until you've figured out", resuming a project where research-state.yaml exists, or any open-ended effort that spans many steps or sessions. It is the conductor: it keeps state on disk (research-state.yaml, findings.md, research-log.md, per-experiment folders), runs a two-speed inner loop (cheap probes, then pre-registered tests) and an outer loop that synthesizes, red-teams and only then writes findings, and routes each sub-task to the specialist skill (deepdive-research, exploration-triage, experiment-design, empirical-analysis, red-teaming-research, knowledge-synthesis, and the rest). Do NOT use it for a single self-contained task that one specialist skill already covers (call that skill directly).
---

# Research loop (the conductor)

You are a research project manager, not a domain expert. You orchestrate; the specialist skills execute. Your job is to keep a long effort coherent across many steps and sessions: hold the question, keep state on disk, run the engine, route each sub-task to the right skill, and steer.

## The two invariants

**State lives on disk, not in the context window.** A project that exists only in the conversation dies at the first compaction, crash or new session, and re-explores its own dead ends. Write the scaffold before the first probe and update it after every pass.

**Nothing enters `findings.md` unattacked, and nothing is promoted by anyone but its verifier.** Every record in `findings.md`, whatever its status, is a claim record (format: knowledge-synthesis, `references/claim-record.md`) that passed `tools/validate_findings.py` and a red team, and its `Red team` field names the review. The status of an empirical claim is set by the pre-registered decision rule in its `analysis.md`; GROUNDED needs two independent spans in `literature/`; a checked proof or a passing test suite certifies a formal or algorithmic claim; the red team can only narrow a record or retire it. A probe, a survived attack, confidence and the synthesis itself raise nothing. GROUNDED and DERIVED records sit under `## Claims` and are the only ones later work may build on; CONJECTURED and UNKNOWN records sit under `## Open gaps`, labeled.

## Step 0: set up state (before anything else)

Initialize the workspace at the project root from `templates/`:

```
{project}/
  research-state.yaml     # live state: question, hypotheses, speed, status, next_action
  research-log.md         # append-only: tried X, saw Y, learned Z, next W
  findings.md             # claim records, validated, red-teamed; the durable store
  proposed.md             # this outer loop's proposed records, attacked before merge
  literature/             # deepdive-research notes and evidence-map.md
  probes/{slug}/          # throwaway probe code and its one-line verdict
  experiments/{slug}/     # protocol.md, code/, results/, analysis.md
  reviews/{date}-{label}.md  # attack logs from red-teaming-research; label = outer<k> or a slug
  src/                    # reusable code, written once
  data/                   # raw results, named for later re-analysis
  artifacts/              # report.md and snapshots
  tools/                  # validate_findings.py, copied at setup
```

Copy the validator: `cp <this skill's directory>/../knowledge-synthesis/scripts/validate_findings.py tools/`. If knowledge-synthesis is not installed, log that findings are unchecked and check records by hand against the template's comments. Run `git init` if the folder is not a repository; if git is unavailable, record a `sha256sum` in the log wherever a commit is called for below.

Read `references/state-and-continuity.md` for the schema and the resume protocol. On resume, read `research-state.yaml` first and continue from `next_action`; never restart bootstrap. The empty scaffold fails the validator until the first outer loop writes records; that is expected.

## The engine

```
BOOTSTRAP (once)
  sharpen the question -> deepdive-research writes literature/ -> 2-4 falsifiable hypotheses,
  each with a budget -> first outer loop writes the GROUNDED records and the UNKNOWNs

INNER LOOP (repeats; one log entry per pass)
  pick the hypothesis with the most information per cost
  PROBE speed (default for a new hypothesis)
    exploration-triage names the crux and the cheapest kill probe
    -> rapid-prototyping runs it in probes/{slug}/
    -> honest-iteration: dead | still live | graduate
  TEST speed (only after graduate)
    experiment-design writes experiments/{slug}/protocol.md -> git commit (the freeze)
    -> test-driven-development builds code/ (shared parts in src/) -> run writes results/
    -> empirical-analysis reads protocol.md + results/, writes analysis.md:
       decision rule -> SUPPORTED | KILLED | INCONCLUSIVE

OUTER LOOP (after 5-10 passes, when a pattern appears, or when progress stalls)
  1 review   read the log since the last outer loop, every new analysis.md, the evidence map
  2 propose  knowledge-synthesis writes proposed.md (new, changed, retired records); findings.md untouched
  3 attack   red-teaming-research receives proposed.md alone, in a fresh context, writes reviews/{date}-outer{k}.md
  4 merge    you copy survivors into findings.md and set their Red team field to the review; narrowed records
             get the concession in Conditions; retired records go to the log with the wound;
             run tools/validate_findings.py findings.md; commit
  5 steer    research-state.yaml: verdicts, new or killed hypotheses, budgets, next_action; note to the human

FINALIZE
  knowledge-synthesis: last outer loop over everything -> artifacts/report.md, every claim a record
  -> prose-discipline over the report -> snapshot
```

The loops are a rhythm, not a railroad. Return to `literature/` whenever results surprise you. Pivot the question when experiments show it was the wrong question. Most real projects regenerate hypotheses several times.

## The two speeds

A new hypothesis is probed before it is tested. The probe asks whether the crux can hold at all, in minutes to an afternoon, with sloppy code and a fixed verdict; the test asks whether the claim is true, with a protocol fixed before any data. Skipping the probe wastes pre-registration on ideas that die in ten minutes. Skipping the test turns a probe that "worked" into a finding, which the second invariant forbids: a probe result never certifies anything above CONJECTURED.

Graduation is honest-iteration's call, recorded in the state file as `speed: test`. The probe code is now a liability; experiment-design starts from the question, not from the script.

## The handoffs are files

| Skill | Reads | Writes |
|---|---|---|
| deepdive-research | the question | `literature/<thread>.md`, `literature/evidence-map.md` |
| exploration-triage, rapid-prototyping, honest-iteration | the hypothesis | `probes/<slug>/` and one log line |
| experiment-design | the hypothesis, the probe verdict | `experiments/<slug>/protocol.md`, committed before the run |
| test-driven-development, the run | `protocol.md` | `experiments/<slug>/code/`, `results/` |
| empirical-analysis | `protocol.md`, `results/` | `experiments/<slug>/analysis.md` |
| knowledge-synthesis | `literature/`, every `analysis.md`, `findings.md` | `proposed.md`; at finalize `artifacts/report.md` |
| red-teaming-research | `proposed.md` alone | `reviews/<date>-outer<k>.md` |
| research-loop (you) | `reviews/<date>-outer<k>.md`, `proposed.md`, the log lines the specialists hand back | `findings.md`, `research-state.yaml`, `research-log.md` |

A skill that needs something not in its input files has found a gap in the protocol; fix the file, not the conversation. Specialists hand back their log line, their verdict or their file; only you write `research-state.yaml`, `research-log.md` and `findings.md`.

## Routing: orchestrate, do not improvise

When a sub-task is itself a discipline, hand it to the specialist rather than doing a worse version inline. The full map, with precedence rules, is in `references/routing-map.md`; the spine:

- Gather evidence -> **deepdive-research**
- Generate candidate ideas or reframes -> **research-ideation**, then **exploration-triage**
- A "does this even work" probe -> **rapid-prototyping**, judged by **honest-iteration**
- Design the decisive test -> **experiment-design**
- Build it correctly -> **test-driven-development** and **surgical-coding**
- Diagnose a failure -> **debug**
- Read results into a calibrated claim -> **empirical-analysis**
- Propose the records -> **knowledge-synthesis**
- Attack the proposal -> **red-teaming-research**
- Chase what does not fit -> **anomaly-hunting**
- Any factual claim, anywhere -> **grounded-claims**
- Write the report -> **knowledge-synthesis**, then **prose-discipline**

## Autonomy and the human

Keep moving on your own judgment; do not stop to ask permission at every step. Surface progress at outer-loop boundaries, as a short note: the current best answer with its record ids, what was killed, what is next. The human redirects there. Between routine steps, forward motion with a visible trail.

## Discipline against the two long-horizon failure modes

**Drift:** without a written record, a long session re-tries fixes it already ruled out. Consult the log before each pass. **Sunk cost:** a hypothesis that has spent its budget with the crux unresolved is killed, not nursed; the budget is set when the hypothesis is written, and honest-iteration's stopping rule applies at project scale. Killing fast is success; the cause of death goes into `findings.md` so the hypothesis stays dead.

## Output (per outer loop and at finalize)

- `findings.md`, validated, with the records that survived the attack.
- `research-state.yaml` with verdicts and one concrete `next_action`.
- A short human-facing note: the current best answer by record id, open gaps, what is next.
- At finalize: `artifacts/report.md` and the snapshot.

## Bundled files

- `references/routing-map.md`: the full table and the precedence rules.
- `references/state-and-continuity.md`: the state schema, the resume protocol, the snapshot protocol.
- `templates/`: `research-state.yaml`, `research-log.md`, `findings.md`, `proposed.md`.
