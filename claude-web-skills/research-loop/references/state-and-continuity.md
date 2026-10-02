# State and continuity (schema and resume protocol)

## The schema

`research-state.yaml` is the single source of truth for *where the project is*; the log is
the trail of *how it got there*; `findings.md` is *what it currently believes*. Keep the three
separated: state is overwritten, the log is append-only, findings are rewritten at outer loops.

Field notes for `research-state.yaml`:
- `next_action` is the resume point. It must always be concrete and imperative
  ("run H2 ablation with seed sweep", never "continue work"). Update it as the last
  act of every pass, so a crash costs one pass, not the project.
- `status` gates the engine: bootstrap runs once; inner/outer alternate; finalize
  runs knowledge-synthesis and the write-up.
- A hypothesis whose `spent` reaches `per_hypothesis` budget with the crux unresolved
  is killed, not extended (sunk-cost guard). Killing fast is success; record the verdict.

## Resume protocol

1. Read `research-state.yaml`. If it exists, the project exists: do NOT restart bootstrap.
2. Read the last 3 log entries and the findings header for orientation.
3. Continue from `next_action`. Consult the log before the pass (drift guard: never
   re-try what an entry already ruled out).

## Snapshot protocol (ephemeral harnesses)

In environments where the filesystem does not persist across sessions (chat harnesses):
- At every outer-loop boundary and at session end, zip the project workspace and place
  the archive in the user-visible outputs directory. The snapshot IS the project.
- To resume in a new session: the user re-uploads the archive; unzip, then run the
  resume protocol above. Treat the uploaded state as authoritative over memory of
  prior sessions.
- In persistent environments (a real workspace), skip snapshots; disk is enough.
