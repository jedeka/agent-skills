---
name: knowledge-synthesis
description: >-
  Use this skill to turn gathered material into durable, trustworthy knowledge, rather than a summary. Triggers include "synthesize this", "what's the takeaway", "distill what we found", "turn this into knowledge", building a knowledge base or briefing from sources, or the finalize step of an investigation. It rebuilds understanding from first principles, strips everything superfluous (via negativa), and attaches to every claim its justification: a source span for grounded facts, an explicit reasoning chain for derived ones, or a calibrated probability with its supporting argument for interpolated ones. It reconciles conflicts rather than averaging and quarantines the unverified. Receives gathered evidence from deep-research, uses grounded-claims for provenance and red-teaming-research to stress the result, and hands conjectures to disciplined-invention. Do NOT use it to gather the material (use deep-research) or to merely reformat tidy notes (use organize).
---

# Knowledge synthesis (precious knowledge, not a summary)

A summary restates sources. Knowledge is what you can defend: a claim plus the reason it is true. The goal is a small set of claims, each carrying its justification, that explains the most with the least and survives attack. Knowledge without its justification is rumor with good posture.

## The invariant

**No claim survives into the synthesis without its warrant attached.** Every unit is one of: GROUNDED (a source span that entails it), DERIVED (a checkable argument from grounded premises), INTERPOLATED (an explicit probability plus the reasoning that warrants it), or UNKNOWN (a named gap, left open). A claim carrying none of these is deleted. This is grounded-claims' status discipline, made the organizing principle of the output rather than a footnote.

## Build ab initio

Do not paraphrase the sources into a heap. Rebuild the understanding from primitives: what is the irreducible mechanism, the load-bearing fact, the thing from which the rest follows? Compress each source to its core and find the few truly load-bearing pieces among the mass of detail (this is hypercognize's hyper-compression in service of a claim). The test of understanding is that you can derive the consequences, not just recite the inputs.

## Cut via negativa

The synthesis improves mostly by removal. Strip the superfluous, the unsupported, the decorative, the redundant, and the merely-interesting-but-not-load-bearing. What remains after every safe deletion is the knowledge. Prefer the smallest set of claims that accounts for the evidence; a synthesis you cannot cut further is finished. Subtraction is the main move, not addition.

## Attach the warrant, always

For each claim, supply the strongest warrant it has, and show it:

- **GROUNDED:** cite the specific source span that entails the claim, not merely a source that is on-topic. Confirm entailment: a real source that does not actually say this is still a fabrication. Include the source whenever one exists.
- **DERIVED:** give the reasoning chain, step by step, from grounded premises to conclusion, so a reader can check it independently. The chain is part of the output, never hidden. Each step is licensed by a grounded fact or a prior derived step.
- **INTERPOLATED:** when the claim goes beyond what any source states (a generalization, an estimate, a filled gap), say so, attach a calibrated probability, and show the reasoning that earns it: the prior, what moves it, what it rests on, and what would raise or lower it. Never round an interpolation up to a fact; an honest "~70%, because" beats a false certainty.
- **UNKNOWN:** state the gap as a gap. A named gap is recoverable; a gap silently filled is a landmine.

## Reconcile, do not average

When sources or sub-findings conflict, resolve the conflict explicitly: weight by source quality and evidence, explain which side wins and why, and if it cannot be resolved, report both with their support and mark the question open. Averaging two incompatible claims produces a third claim that no evidence supports.

## Test the synthesis before trusting it

A conclusion that hangs on one source or one assumption is fragile. Note the sensitivity: which claims would change if a single source were wrong, or one assumption were dropped. Hand the assembled story to red-teaming-research and apply its type-aware check: does the evidence's form match each claim's form (causal claim needs a cause that was isolated, "in general" needs heterogeneous support)? A synthesis that survives that is knowledge; one that does not is a draft.

## The durable store (the safe flywheel)

Only GROUNDED and verified-DERIVED claims enter a durable knowledge base; INTERPOLATED and CONJECTURED claims are labeled and quarantined until a verifier promotes them (disciplined-invention governs that promotion). This single rule keeps a growing knowledge base free of accumulated guesswork: nothing unverified is ever silently trusted later.

## Output: the knowledge artifact

- **The claims**, ordered by importance, each with its status, its warrant (source span / reasoning chain / probability-and-argument), and its residual risk.
- **Conflicts**, reconciled, with the reason for the call.
- **Confidence and gaps:** what is solid, what is provisional, what is still UNKNOWN.
- **One line of "what would change this"** for the load-bearing claims.

Optionally emit the artifact as structured `knowledge.json` (claim, status, source or chain, probability, residual risk) so it is reusable and auditable. Hand the prose write-up to **organize**, and keep **grounded-claims** in force so no number loses its provenance. Within a larger effort, this is the finalize node of **research-loop**, fed by **deep-research**.
