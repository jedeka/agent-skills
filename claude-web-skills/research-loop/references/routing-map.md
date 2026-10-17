# Routing map (the full table)

Hand a sub-task to the specialist the moment it becomes a discipline; a worse inline version is never cheaper. Situations, destinations, and what comes back, as a file where the engine needs one:

| Situation | Route to | Hands back |
|---|---|---|
| Ingest and frame a hard problem from scratch | hypercognize | a structured framing |
| Gather evidence on any topic | deepdive-research | `literature/<thread>.md`, `literature/evidence-map.md` |
| Generate candidate ideas or reframes | research-ideation | candidate ideas as structural mappings |
| Order candidates, name the crux and the cheapest kill probe | exploration-triage | an ordered probe queue |
| "Does this even work" probe | rapid-prototyping | `probes/<slug>/`, one signal, throwaway code |
| Judge a probe: dead, still live, graduate | honest-iteration | the verdict and one log line |
| Design the decisive test before data exists | experiment-design | `experiments/<slug>/protocol.md`, committed |
| Build correctly (test discipline) | test-driven-development | `experiments/<slug>/code/`, green suite |
| Write or modify the code itself (restraint) | surgical-coding | the minimal diff |
| Diagnose any failure | debug | root cause, fix, regression test hook |
| Read results into a calibrated claim | empirical-analysis | `experiments/<slug>/analysis.md` with the decision rule's output |
| Something does not fit expectations | anomaly-hunting | artifact-versus-real verdict |
| Propose records from the evidence | knowledge-synthesis | `proposed.md`, validated with `--proposed` |
| Attack the proposal or any claim | red-teaming-research | `reviews/<date>-<label>.md`: per record, survived, narrow or retire, with the attack log |
| Invent beyond sources (conjecture) | disciplined-invention | a labeled conjecture with its verification path |
| Any factual assertion, anywhere | grounded-claims | statused, provenanced claims |
| Write the report from the records | knowledge-synthesis | `artifacts/report.md`, every claim a record |
| De-AI and tighten the prose | prose-discipline | final-pass prose |
| Compress for the human | succinct, ultra-summary | MDL text, two-sentence digest |

## Precedence (where routes could collide)

- **Who changes a status.** The pre-registered decision rule in `analysis.md` promotes an empirical claim. Two independent spans in `literature/` make a GROUNDED claim. A checkable chain in the record, a checked proof or a passing test suite makes a DERIVED claim. red-teaming-research only narrows a record or retires it; a record that cannot stand at its status is retired, and knowledge-synthesis may re-propose it lower next time. knowledge-synthesis proposes and never promotes. A testable objection from the red team becomes a new hypothesis in `research-state.yaml`, written by research-loop and probed first like any other. Nothing else touches a status.
- **Probe versus test.** exploration-triage, rapid-prototyping and honest-iteration govern `probes/` and decide graduation. experiment-design and empirical-analysis govern `experiments/`. A probe result never becomes a record above CONJECTURED. If a `protocol.md` exists, empirical-analysis owns the verdict and honest-iteration has no say.
- **Fresh context for the attack.** red-teaming-research receives `proposed.md`, or the claim restated alone, never the transcript or the reasoning that produced it. It writes `reviews/<date>-<label>.md` and nothing else.
- **Proposal before merge.** knowledge-synthesis writes `proposed.md`; research-loop merges into `findings.md` after the attack and the validator. No skill writes `findings.md` except research-loop.
- **Probe code.** rapid-prototyping suspends surgical-coding's restraint by design; graduation re-imposes it, and experiment-design starts from the question, not from the probe script.
- **Report.** knowledge-synthesis writes the report from the records; prose-discipline edits wording and may not change a record.
