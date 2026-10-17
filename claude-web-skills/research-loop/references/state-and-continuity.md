# State and continuity (schema, resume, snapshots)

## The files and their write rules

`research-state.yaml` is the single source of truth for *where the project is*; `research-log.md` is the trail of *how it got there*; `findings.md` is *what it currently believes*; `proposed.md` is *what the current outer loop wants to believe, before the attack*. Each has its own write rule, and the rule is what makes the file useful:

| File | Write rule | Why |
|---|---|---|
| `research-state.yaml` | overwritten every pass | small and current, so a resume takes one read |
| `research-log.md` | append-only | a ruled-out fix stays on record, so it is not retried |
| `proposed.md` | rewritten at each outer loop, by knowledge-synthesis | the attack has a clean target |
| `findings.md` | merged at each outer loop, by research-loop only, after the attack and the validator | the store holds nothing unattacked |
| `experiments/<slug>/protocol.md` | written once, committed, then read-only | the meaning of the result was fixed before the data |

## Field notes for `research-state.yaml`

- `next_action` is the resume point. It is concrete and imperative ("run H2 ablation with the seed sweep in protocol.md", never "continue work"). Update it as the last act of every pass, so a crash costs one pass, not the project.
- `status` gates the engine: `bootstrap` runs once; `inner` and `outer` alternate; `finalize` runs the last synthesis and the report.
- Each hypothesis carries `speed: probe | test`. It starts at `probe` and moves to `test` only on honest-iteration's graduate verdict. A hypothesis at `probe` speed has no `experiment` and may have no claim above CONJECTURED.
- Each hypothesis carries `claims: [C3, C7]`, the records in `findings.md` that bear on it. `status: supported` requires at least one DERIVED record whose `Certified by` names this hypothesis's `analysis.md` with SUPPORTED. `status: killed` requires an entry under `## Killed hypotheses` in `findings.md`.
- A hypothesis whose `spent` reaches `budget` with the crux unresolved is killed, not extended. Record the verdict and the cause of death.
- `passes_since_outer` counts inner passes; at 5 to 10, or earlier when a pattern appears or progress stalls, run the outer loop and reset it.

## The outer-loop merge

research-loop, not knowledge-synthesis, performs step 4 of the outer loop:

1. Read `reviews/<date>-outer<k>.md`. For each record in `proposed.md`: survived, copy it into `findings.md` and set `Red team: reviews/<date>-outer<k>.md: survived`; narrow, copy it with the concession added to `Conditions` and `Red team: reviews/<date>-outer<k>.md: wounded, conceded: <the concession>`; retire, do not copy, and append the record id and the wound to the log. A status never changes at the merge: a record the red team says cannot stand at its status is retired, and knowledge-synthesis may re-propose it at a lower status, with that status's warrant, in the next `proposed.md`.
2. Retire the records `proposed.md` marked for retirement: move each to the log with its reason. Never reuse the id.
3. Move killed hypotheses into `## Killed hypotheses` with `Killed by` pointing at the file that killed them, or reading `budget spent, crux unresolved` for a budget kill.
4. Rewrite `## Current best answer` so that every claim in it names its record.
5. Run `python3 tools/validate_findings.py findings.md`. Fix until it passes. Commit.

## Resume protocol

1. Read `research-state.yaml`. If it exists, the project exists: do not restart bootstrap.
2. Read the last 3 log entries and `## Current best answer` for orientation.
3. If `proposed.md` is newer than the last merge noted in the log, the previous session died mid outer loop: resume at step 3 (attack) or step 4 (merge), whichever the log shows incomplete. Review files are named `reviews/<date>-outer<k>.md`, k counting the outer loops of that day, so a second loop never overwrites the first.
4. Continue from `next_action`. Consult the log before the pass; never retry what an entry ruled out.

## Snapshot protocol (ephemeral harnesses)

Where the filesystem does not persist across sessions:

- At every outer-loop boundary and at session end, zip the project workspace into the user-visible outputs directory. The snapshot is the project.
- To resume in a new session, the user re-uploads the archive; unzip, then run the resume protocol. The uploaded state is authoritative over any memory of prior sessions.
- In a persistent workspace, skip snapshots; disk and git are enough.
