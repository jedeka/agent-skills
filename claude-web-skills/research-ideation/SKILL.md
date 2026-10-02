---
name: research-ideation
description: Use this skill to generate genuinely novel ideas, directions, hypotheses, or reframings, rather than incremental tweaks. Triggers include "brainstorm", "come up with ideas", "novel approaches to", "I'm stuck in a local optimum", "reframe this problem", "what angles am I missing", "is there a fundamentally different way", or the front of any research effort. It applies structured creativity engines from cognitive science (combination, reformulation, analogical transfer, constraint manipulation, inversion, abstraction laddering, the adjacent possible, holding contradictions) instead of waiting for inspiration, and it filters every idea for structural depth versus surface metaphor. It feeds exploration-triage (which idea to try first) and disciplined-invention (how to validate a chosen conjecture). Do NOT use it to validate or stress an idea (use disciplined-invention then red-teaming-research), to order candidates by feasibility (use exploration-triage), or to survey what already exists (use deep-research).
---

# Research ideation (generate, then judge)

Novelty is mostly recombination under structure, not lightning. The move is to run deliberate generative engines that force the mind out of its default frame, produce many candidates, and only then judge. Generation and judgment are separate phases: judging while generating kills the idea before it forms. Diverge first, converge after.

## The invariant

**A strong idea is a structural mapping, not a verbal one.** The mechanism transfers, not just the label. "The network is like a brain" is a surface metaphor and worth nothing; "attention implements selective gating analogous to a filter, so the same capacity limits should appear" is a structural mapping that makes a testable prediction. Every candidate is filtered on this: does a mechanism carry over and produce a consequence you could check? If not, discard it.

## The generative engines

Run several; different engines reach different parts of the space. Each is a deliberate operation, not a vibe.

- **Combination (bisociation).** Take two domains you know and cross them. List the core primitives of each, form the grid, and ask of each cell: what would it mean to apply A's mechanism to B's problem? Evolution x optimization gave genetic algorithms; statistical physics x learning gave energy-based models. The combination is the creative act.
- **Reformulation.** Stop solving the problem as stated and re-represent it. Change the objective ("make it faster" becomes "remove the need for this computation"), the formalism (graph becomes spectrum), the granularity (per-token becomes per-span), the agent ("how should the model learn" becomes "how should the data teach"), or the direction (forward simulation becomes inverse problem). Breakthroughs often live in the new representation, not the new answer.
- **Analogical transfer.** Find a field that solved the structural twin of your problem and import its solution, checking that the mechanism, not just the story, maps. Immune memory for caching; mechanism design for routing.
- **Constraint manipulation.** Add a brutal constraint (solve it with 1% of the compute, in one pass, with no labels) and see what new design the constraint forces. Or remove a constraint everyone assumes is fixed and ask what becomes possible.
- **Inversion.** Negate the goal: instead of "how do we achieve X", ask "how would we guarantee not-X", then invert the answers. The failure modes you list often name the real levers.
- **Abstraction laddering.** Move up ("what is this a special case of?") to find a more general solution, or down ("what is the smallest concrete instance?") to find a foothold. The right rung is often neither where you started.
- **The adjacent possible.** Survey what just became feasible (a new tool, result, dataset, or scale) and ask what it puts within one step's reach that was out of reach last year. Many real advances are simply the first to step into a newly-opened room.
- **Holding the contradiction.** When two requirements conflict, do not compromise to mush; hold both and look for the design that honors them at once. The tension is often where the non-obvious solution hides.

## Generate wide, then filter

Produce many candidates before judging any. Then filter, in order: keep only structural mappings (the invariant), drop the ones with no checkable consequence, and set aside the ones that merely restate prior work. Do not filter on feasibility or priority here; that is exploration-triage's job, and filtering too early kills the wild idea that would have survived.

## Output

- **A short list of candidate ideas**, each stated as a structural mapping with the consequence or prediction it implies, and the gap or pattern it exploits.
- For each, a one-line **why it is plausible** and **what it would take to test or refute it** (the seed disciplined-invention needs).

Hand the list to **exploration-triage** to order by information per unit cost, and a chosen candidate to **disciplined-invention** to turn into a labeled, justified, verifiable conjecture. Within a larger effort, this is the idea-generation node of **research-loop**.
