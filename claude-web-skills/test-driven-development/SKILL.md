---
name: test-driven-development
description: Use this skill when building code that has to be correct and is worth building properly, especially after a fast probe has graduated out of exploration. Triggers include "write tests", "TDD", "build this properly", "make this production-ready", "I keep breaking this, lock it down", "what tests should this have", or graduating a prototype into real code. It enforces red-green-refactor (a failing test first, the minimum code to pass, then refactor under green), tests that assert real behavior rather than presence, tests pinned to the spec and to the bug, and a fast trustworthy suite. It is the rigorous-build phase that honest-iteration graduates into and that experiment-design hands execution to. Pairs with surgical-coding (restraint while writing) and debug (which adds a regression test for each fix). Do NOT use it for a throwaway exploratory probe where correctness is not yet load-bearing (use rapid-prototyping).
---

# Test-driven development (the test is the spec)

A test is an executable definition of what "correct" means. Writing it first forces you to say what you are building before you build it, and leaves behind a tripwire that catches the next person (often you) who breaks it. This is the discipline that takes an idea which survived cheap exploration and makes it load-bearing.

## The invariant

**No behavior is trusted until a test that would fail without it passes.** A feature with no failing-then-passing test is a hope, not a capability. The order matters: the test fails first (proving it can fail), then the code makes it pass (proving the code is why). A test written after the code, never seen to fail, may be asserting nothing.

## Red, green, refactor

The loop, in strict order:

1. **Red.** Write one small test for the next slice of behavior. Run it. Watch it fail, for the expected reason. A test that passes before you have written the code is testing the wrong thing, or nothing.
2. **Green.** Write the minimum code to make it pass. Not the elegant version, not the general version: the least code that turns the test green. Resist building ahead of the test (surgical-coding's simplicity rule).
3. **Refactor.** With the test green, improve the structure: remove duplication, clarify names, simplify. The green test is your safety net; if it goes red, you broke something, so fix it before moving on.

Small slices. Each loop adds one behavior and stays green at the end. A long red period means the slice was too big; shrink it.

## Tests must test (the central failure mode)

A passing test that asserts nothing is worse than no test: it is a silent false assurance. Guard against it:

- **Assert behavior, not presence.** Check what the code produces and does, not merely that a function exists or returns without error. "It ran" is not "it is correct."
- **Watch it fail first.** The red step is what proves the test has teeth. Skipping it is how assertion-free tests slip in.
- **Mutation check the doubtful ones.** If you are unsure a test bites, break the code on purpose and confirm the test goes red. If it stays green, the test is decorative.
- **Test the contract, not the implementation.** Pin the behavior callers depend on, so a refactor that preserves behavior keeps the test green. Tests welded to internals break on every refactor and get deleted, taking their coverage with them.

## Cover the space, not just the happy path

The bug lives in the state you did not consider (debug's state-space discipline, applied before the bug exists). For each unit, test the edges: empty and null, boundaries and off-by-one, the maximum and the degenerate, error and failure paths, concurrency and ordering where they apply, and the awkward real inputs. One happy-path test is a demo; the edges are where correctness is won.

## Pin the spec and pin the bug

- **Spec to test.** Each requirement becomes a test that fails until the requirement is met (this is experiment-design's "define the falsification first" and surgical-coding's "define done", made executable). The suite is the spec, kept honest by running.
- **Bug to test (regression).** Every fixed bug gets a test that reproduces it first and then passes, so it can never silently return. A fix without a regression test is a fix on probation. This is the standing handoff from debug.

## Keep the suite fast and trustworthy

A slow or flaky suite stops being run, and an unrun suite protects nothing. Keep unit tests fast and deterministic; isolate slow or external-dependent tests so the core loop stays quick. A flaky test is a defect in its own right: fix it or quarantine it, because a test that fails at random trains everyone to ignore red, which defeats the entire point.

## Output

- The tests, written before or alongside the code, each having been seen to fail first.
- Code that is the minimum to pass, then refactored under green.
- Edge and error cases covered, not just the happy path.
- A regression test for every bug fixed along the way.
- A green, fast, deterministic suite that encodes the spec.

Write the code itself under **surgical-coding**; when something breaks, **debug** finds the cause and returns here for the regression test. Within a larger effort, this is the build node of **research-loop**, entered when **honest-iteration** graduates an idea.
