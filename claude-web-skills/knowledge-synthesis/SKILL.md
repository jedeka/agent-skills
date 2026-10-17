---
name: knowledge-synthesis
description: >-
  Use this skill to turn gathered material into durable, trustworthy knowledge, rather than a summary. Triggers include "synthesize this", "what's the takeaway", "distill what we found", "turn this into knowledge", building a knowledge base or briefing from sources, research-loop's outer-loop synthesis and finalize steps, and writing the report that ends an investigation. It rebuilds understanding from first principles, strips the superfluous (via negativa), and writes every claim as a claim record with its warrant: a source span for grounded facts, a checkable chain or a pre-registered decision rule for derived ones, a prior with its argument for conjectures, a named gap for unknowns. A validator checks the records. It reconciles conflicts instead of averaging, proposes before it writes, and lets only the red team narrow and only a verifier promote. Reads deepdive-research notes; its proposal goes to red-teaming-research before anything is stored. Not for gathering the material (deepdive-research).
---

# Knowledge synthesis (precious knowledge, not a summary)

A summary restates sources. Knowledge is what you can defend: a claim plus the reason it is true. The goal is the smallest set of claims, each carrying its justification, that explains the most and survives attack. Knowledge without its justification is rumor with good posture.

## The invariant

**No claim survives into the synthesis without its warrant attached.** Every claim is a record with one of four statuses, the statuses of grounded-claims: GROUNDED (a source span that entails it), DERIVED (a checkable chain from grounded premises, or a pre-registered decision rule computed on data), CONJECTURED (a prior as a percentage, plus the argument that earns it), or UNKNOWN (a named gap, left open). A claim carrying none of these is deleted. The record format is in `references/claim-record.md`, and `scripts/validate_findings.py` checks it; a record the validator rejects is not knowledge yet.

## Two modes

**Standalone.** The user hands you material, or deepdive-research ran first. You produce the knowledge artifact: a file of claim records with the four sections of `findings.md`, validated, plus a short note on what is solid, what is provisional and what is unknown.

**Inside research-loop.** You run at every outer loop and at finalize, and you never write `findings.md` directly. You write `proposed.md`: the records that are new, the records whose status or conditions should change, and the records to retire, each with its reason. red-teaming-research attacks `proposed.md` in a fresh context, and only what survives is merged, by research-loop, into `findings.md`. At finalize you also write the report (below).

## Where the evidence comes from

- deepdive-research notes: `literature/<thread>.md` and `literature/evidence-map.md` inside a research-loop workspace, or `deepdive/<title>/` standalone. Read the map for the shape, then the notes for the spans. Each finding carries the quoted passage, URL, date, source type, origin and corroboration state, which is what a GROUNDED warrant needs. A finding marked `Corroboration: NONE YET` is a lead; it cannot become GROUNDED on its own.
- Experiment results: `experiments/<slug>/analysis.md`, written by empirical-analysis. The decision rule's output there, SUPPORTED or KILLED, is the only thing that makes an empirical claim DERIVED. Copy the effect, its interval and the conditions into the warrant; do not restate them from memory.
- Probe results: `probes/<slug>/`. A probe shows feasibility and never certifies a claim above CONJECTURED.
- Material the user pasted, with no provenance: GROUNDED only where you can retrieve the span; otherwise CONJECTURED with a prior, or UNKNOWN.

## Build ab initio

Do not paraphrase the sources into a heap. Rebuild the understanding from primitives: what is the irreducible mechanism, the load-bearing fact, the thing from which the rest follows? Compress each source to its core and find the few load-bearing pieces among the mass of detail. The test of understanding is that you can derive the consequences, not that you can recite the inputs.

## Cut via negativa

The synthesis improves mostly by removal. Strip the superfluous, the unsupported, the decorative, the redundant, and the interesting but not load-bearing. What remains after every safe deletion is the knowledge. Prefer the smallest set of claims that accounts for the evidence; a synthesis you cannot cut further is finished.

## Write the warrant, always

For each claim, supply the strongest warrant it has, in the record's `Warrant` field:

- **GROUNDED:** the specific span that entails the claim, with its URL, and a second independent source. Confirm entailment: a real source that does not say this is still a fabrication. One source is a lead.
- **DERIVED by argument:** the chain, step by step, from GROUNDED records to the conclusion, so a reader can check it. Each step is licensed by a grounded fact or a prior step. The chain is in the record, never hidden.
- **DERIVED from data:** the effect with its uncertainty and the decision rule's output, copied from `analysis.md`. A run that came back INCONCLUSIVE promotes nothing: the claim stays CONJECTURED, with the `analysis.md` named in the warrant.
- **DERIVED by a checker:** what a proof assistant or a test suite checked, with `Certified by: verified: <path>, <checker>`.
- **CONJECTURED:** the claim goes beyond what any source or test states (a generalization, an estimate, a filled gap). Say so, give a prior as a percentage, and show what earns it: what it rests on, what moves it, what would raise or lower it. Never round a conjecture up to a fact; "~70%, because" beats a false certainty.
- **UNKNOWN:** state the gap as a gap, with what was searched. A named gap is recoverable; a gap silently filled is a landmine.

Write the claim's conditions into the sentence and into `Conditions`. Then check that the warrant has the form the claim has: a causal claim needs a cause that was isolated, a general claim needs support across the range it claims, a theorem needs a proof and not an experiment, a present-state claim needs a dated source. Where the forms differ, narrow the claim until they match.

## Reconcile, do not average

When sources or results conflict, resolve the conflict explicitly: weigh by source quality and evidence, say which side wins and why, and if it cannot be resolved, keep both records with their support and open an UNKNOWN. Averaging two incompatible claims produces a third claim that no evidence supports.

## Propose, then let the red team cut

Before anything is written as knowledge, mark the fragile records: which would change if one source were wrong or one assumption dropped. The records then go, alone and in a fresh context, to red-teaming-research: inside research-loop the loop dispatches them as its step 3; standalone you do. The verdict only narrows or retires: a wounded record gets the concession written into `Conditions`, a dead record is retired to the log with its wound, and a record that cannot stand at its status is retired, to be re-proposed lower with that status's warrant. A survived verdict raises nothing. Inside research-loop these edits are the loop's merge step, not yours; standalone you make them. Promotion comes only from the verifiers named in `references/claim-record.md`: two independent spans, a checkable chain, a checker, or the pre-registered decision rule.

## The durable store

`findings.md` (or the standalone artifact) holds records of all four statuses, but in two places that mean different things. `## Claims` holds GROUNDED and DERIVED records, the only ones later work may build on and the only ones the report may state as fact. `## Open gaps` holds CONJECTURED records awaiting a verifier and UNKNOWN records, labeled; disciplined-invention governs how a conjecture earns promotion. Nothing moves from the second place to the first without a verifier. This one rule keeps a growing store free of accumulated guesswork.

## The report

When a human-facing write-up is wanted (research-loop's finalize, or the user asks), write it from the records: `artifacts/report.md` in a project, or alongside the artifact standalone. The rule is that the report contains no claim that is not a record. Each paragraph names the records it rests on, as (C7). Conditions travel with the claim; a sentence that drops them states a different claim. Statuses appear in the prose as plain words: "shown by", "follows from", "we conjecture (~70%)", "unknown". Run prose-discipline over it last; it may change wording and may not change a record.

## Output

- Standalone: the knowledge artifact (claim records in the four sections), validated with `python3 <this skill's directory>/scripts/validate_findings.py <file>`, and a short note: what is solid, what is provisional, what is UNKNOWN, and one line of "what would change this" for the load-bearing records.
- In research-loop: `proposed.md`, validated with `--proposed`, and at finalize `artifacts/report.md`.

## Bundled files

- `references/claim-record.md`: the record format, what each status requires, who may change a status, the sections of `findings.md`.
- `scripts/validate_findings.py`: checks records, sections, killed-hypothesis entries and that every project path named in `Certified by`, `Red team` or `Killed by` exists. `--proposed` for `proposed.md`, `--no-paths` outside a project, `--json` for machine output. research-loop copies this script into `tools/` at project setup.
