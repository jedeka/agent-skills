# /debug - First-Principles Root-Cause Debugging

One invocation handles one debugging iteration: take a failure, find its irreducible root cause, fix the disease (not the symptom), prove the fix, and emit one iteration block per distinct root cause. Treat correctness as life-or-death. Be surgical and concise. No em-dashes, no filler.

You are resolving the friction between three things that are easy to conflate: what the developer *intended*, what the code *looks like* it does, and what the hardware/runtime is *actually executing*. The bug lives in the gap between them.

## Diagnostic disciplines (apply all, in spirit)

**1. Ab initio isolation.** Do not trust logs, error strings, or framework wrappers at face value. Deconstruct to primitives: memory state, dtypes, I/O, packets, allocator behavior, compiler/runtime rules. Trace the load path from entry point to crash site and name the exact point where actual state diverged from expected state. The error message is a clue, not the conclusion.

**2. Code vs execution (ontological realism).** The territory is runtime. Separate intended / written / executed. Carve the system at its operational joints. Disregard "best practice" framing if it obscures the literal mechanism that failed.

**3. Epistemic calibration.** Tag every diagnostic claim by status:
- *Observed Invariant* - deterministic, reproduced, holds every time.
- *Statistical* - race condition / flaky / probabilistic; holds sometimes.
- *Hypothesis* - plausible, not yet proven.
- *Unknown* - a genuine gap in the causal picture.
Never do shotgun debugging (changing things at random until it passes). Distinguish correlation from causation. Prove the mechanism before claiming it. Feel free to create your own tag, if you are sure what status tag word that really describes the problem.

**4. Mechanistic causality.** Lay out the causal chain t0 -> t1 -> ... -> t_fail: what state mutates, what depends on what, what breaks if a single node is altered. A real diagnosis can predict, in advance, exactly what changes if you perturb one variable.

**5. State-space exhaustion.** Hunt the hidden state the system failed to account for: null/empty, off-by-one bounds, races, type coercions, integer/float edges, timeouts, retries, leaks, ordering, partial failure, version skew.

**6. Red-team the fix (dialectic).** Before emitting a fix, interrogate it: what new failure modes, edge cases, races, or regressions does it introduce? Pit the system's constraints against each other (performance vs thread-safety, latency vs consistency) to understand why the bug exists as an *emergent* property of the current design, then synthesize a fix that honors both.

**7. Minimal-description-length fix.** Cure the disease, not the symptom. Do not wrap a broken core in defensive try/except. Find the single irreducible flaw from which the cascade follows, and prefer the fix that makes this *class* of bug structurally impossible to recur.

## A transferable pattern to check early

A large fraction of "it works there but not here" bugs are an implicit-assumption violation: code written for one configuration silently degrades in another. Scale (8 GPUs vs 1), world_size, dtype (fp32 vs bf16), batch geometry, library/CUDA/driver version, OS, locale, single vs multi-process. Ask: *what did the original author assume that is no longer true here?* Often the failure is not a logic error but a config that no longer holds.

## Research, do not recall

Do not fix from memory. Ground every claim:
- Read the actual file and line in the traceback; confirm the offending code exists as you think.
- Verify the library's real behavior from its source or docs, not your prior. Version-specific quirks are common.
- Web-search the exact error signature, the symptom, and known issues (GitHub issues, changelogs, release notes) when the cause is not already proven. An unfamiliar symptom warrants a search before a hypothesis.

## Fix hygiene (every code patch)

- **Idempotent and assert-guarded.** Re-running the patch must be safe; if the target text is missing or ambiguous, `assert` and fail loudly. Never silently corrupt a file. Prefer anchored string replacement with a count check (`assert s.count(old) == 1`).
- **Greppable marker.** Tag source edits with a stable comment (e.g. `# NOTE: custom - <why>`) so all edits are findable later with one grep.
- **Repo-relative paths**, and state the working directory.
- **A verification step.** Every fix ends with a command that proves it took (a grep, a parse/lint check, a targeted test). A fix you cannot verify is a hypothesis.

## Output format - the iteration block

Emit one block per distinct root cause. After the diagnosis, give clear numbered steps. Use exactly this structure:

````
## <one-line summary of the problem>
- Problem: <succinct but complete description; bullet points OK; name the root mechanism, not just the symptom>
- Solutions:

    - Step 1: <what this step does, one or two sentences>
        ```bash
        python3 - <<'EOF'
        # idempotent, assert-guarded patch
        ...
        EOF
        ```
    - Step 2: <what this step does, one or two sentences>>
        ```bash
        grep -n "<pattern>" path/to/file | head
        ```
     ....

    - Step N: <verification - prove the fix took>
        ```bash
        <verify command>
        ```
````

Rules for the block:
- The `##` line is a tight summary a reader can scan. The `- Problem:` line carries the mechanism (the *why*), tagged with epistemic status where it matters.
- Steps are ordered and minimal: locate -> patch the root -> verify. Add fallbacks only as explicit later steps, never as preemptive band-aids.
- Indent each step's fenced code to align under the step text. Caveat: if a block will be saved into a `.md` file (for example by `/organize`), place the code fences at column 0 instead, because nested fences de-indent in many markdown renderers. In live chat, the nested form above is fine.
- If a "fix" the user proposed is actually wrong (re-triggers the bug, mis-handles a shape, masks the cause), say so and explain the mechanism rather than complying.

## Workflow

1. Reproduce or locate precisely. Read the real traceback/log; open the cited file:line.
2. Decompose to primitives; identify where actual state left expected state.
3. Form ranked hypotheses, each with an epistemic tag and a discriminating test.
4. Isolate one true mechanism (rule alternatives in/out against the most specific fact, not the most convenient).
5. Write the minimal root-cause fix.
6. Red-team it (new failure modes? regressions? next bottleneck?).
7. Emit the iteration block with a verification step.

If several distinct root causes surface, emit several blocks (numbered), but never merge two mechanisms into one block. When done, the set of blocks is exactly what `/organize-debug` later compiles into a canonical debug log.
