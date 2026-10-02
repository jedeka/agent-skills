---
name: surgical-coding
description: Write and modify code with surgical restraint, changing exactly what the task requires and nothing else. Triggers include "minimal change", "small diff", "don't break anything", "touch only", "fix this without refactoring", editing or extending an existing codebase, working inside legacy or unfamiliar code, and the write-the-code step of test-driven-development or research-loop. It enforces defining done before writing, reading the mechanism before cutting into it, the smallest correct diff, no drive-by refactors or reformatting, no speculative generality built ahead of a real need, matching local conventions, checking the blast radius of every change, and keeping changes reversible. Do NOT use it for throwaway probes where corner-cutting is licensed (use rapid-prototyping), for test discipline itself (use test-driven-development), or for diagnosing why something is broken (use debug).
---

# Surgical coding (restraint while writing)

Code is a liability that occasionally pays rent. Every line written must be maintained, understood, and trusted by whoever comes next — so the discipline is not writing more correctly, it is writing *less*, correctly. The diff is the argument: every changed line justified by the task, no line changed for any other reason.

## The invariant

**Define done first; then make the smallest correct change that reaches it.** Before touching anything, state what "done" is — the behavior that must hold, the behavior that must not change (test-driven-development makes this executable; here it is at minimum written down). Then the target is the minimum diff that achieves it. Bigger is not safer; every extra changed line is extra blast radius.

## Read before cutting

Never edit a mechanism you have not read. Understand what the code does and *why it is the way it is* before changing it — the odd-looking guard is usually load-bearing (Chesterton's fence). If you cannot explain the current behavior, you are not ready to change it; that gap routes to **debug** (diagnose) or plain reading, not to bolder edits.

## The restraint rules

- **No drive-by changes.** Renames, reformatting, "cleanups", and refactors of code the task did not require are separate tasks. Smuggling them into a fix widens the blast radius and hides the real change inside noise. If a real refactor is needed, name it as its own task and do it alone, under green tests.
- **No building ahead.** Solve the case that exists, not the general case that might (the simplicity rule test-driven-development leans on). Speculative abstraction is a bet on requirements you have not seen; it usually loses, and it always costs now.
- **Match the local conventions.** The codebase's existing style beats personal taste; consistency is worth more than any individual preference. Surgery adapts to the patient.
- **Check the blast radius.** Before committing to a change: what calls this, what depends on the behavior being altered, what breaks at the edges? Run the surrounding tests; where behavior matters and no test pins it, pin it first (hand to **test-driven-development**).
- **Stay reversible.** Small, self-contained, incremental changes that can be backed out cleanly. A change you cannot revert is a change you cannot safely make.

## Scope discipline

"While I'm here" is the failure mode. When mid-task you discover something else worth fixing, write it down as a new task and finish the incision you opened. One change, one purpose, one diff.

## Routes

Correctness worth locking in → **test-driven-development** (red-green-refactor around this discipline). Something already broken → **debug** first; the fix returns here for minimal implementation and there for the regression test. A throwaway probe → **rapid-prototyping**, where these rules are deliberately suspended. Within a project, this is the build node of **research-loop** alongside test-driven-development.
