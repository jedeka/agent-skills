---
name: red-teaming-research
description: Adversarially attack any claim, conclusion, design, or emerging story to find how it fails before reality does. Triggers include "red-team this", "stress-test", "poke holes", "devil's advocate", "what am I missing", "is this actually right", any conjecture leaving disciplined-invention, any proposed update from knowledge-synthesis, any claim emerging from empirical-analysis, and any finished claim or published result to attack. It receives the claim as an anonymous external artifact in fresh context (never as "my own reasoning"), hunts the strongest counter-argument, alternative explanations, threatening known results, and the cheapest disconfirming test, then returns a severity-ranked verdict of what died, what is wounded, and what survived. Do NOT use it to keep a live iteration loop honest (use honest-iteration) or to verify a factual citation (use grounded-claims).
---

# Red-teaming research (attack it before reality does)

A claim that has only been defended is undefeated, not tested. The job here is to be the adversary the claim will eventually meet (a hostile reviewer, a competing lab, the market, reality) and meet it first, cheaply.

## The invariant

**The critic never trusts the author, including when the author is you, so the attack happens in fresh context.** The claim arrives as an anonymous external artifact: restated verbatim, stripped of its authorship and the reasoning history that produced it. This is mechanism, not ritual: reviewers reliably find errors in external input that they miss in their own output, so attacking your own transcript is structurally weaker than attacking a clean restatement. In practice, write the claim alone into a file or a clean block (or hand it to a sub-agent), then attack *that*, never the conversation.

## What arrives

One of three things, each restated alone:

- **A claim**, one sentence with its conditions, as the user or a skill states it.
- **A proposed update**, `proposed.md` from a research-loop outer loop: claim records written by knowledge-synthesis, each with status, warrant, conditions and certifier. Attack every record; start with the ones listed under Fragile. The verdict is per record.
- **A design** (a protocol, an architecture, a plan): attack what it would fail to detect.

## The attack surface (run all of it)

- **Steelman the opposition.** Construct the strongest case *against*, as its best advocate would, not the easiest objection.
- **Rank the failure modes.** What is the single most likely way this is false?
- **Alternative explanations.** What else produces the same evidence: confound, artifact, selection effect, coincidence, a bug?
- **Threatening known results.** What established findings, theorems, or prior failures does this collide with?
- **Assumption audit.** List the load-bearing assumptions explicitly; attack the weakest one.
- **Form mismatch.** Does the warrant have the form the claim has? A causal claim needs a cause that was isolated; "in general" needs support across the range claimed; a theorem needs a proof, not an experiment; a present-state claim needs a dated source; a claim whose conditions are narrower than its sentence is two claims wearing one label. For a record, check that the certifier named in `Certified by` is the one its status requires, and that the file it names says what the record says it says.
- **Absence check.** If this were true, what else should exist, and is it there? Missing expected evidence is evidence.
- **Cheapest kill.** Name the single cheapest observation or test that would disconfirm it.

## The verdict (output)

Severity-ranked, three bins: **died** (a fatal objection, with the wound), **wounded** (a serious objection, and the concession that repairs it: a narrower `Conditions` line, stated exactly), **survived** (attacks tried and why they failed). Always attach the cheapest disconfirming test and the residual risk.

**The red team only narrows or retires.** A died verdict retires the claim; a wounded verdict narrows its conditions; a survived verdict changes nothing, because surviving is not truth. A status is never rewritten here: when a claim cannot stand at its status even with narrower conditions, the verdict is died, with a note that it may be re-proposed lower, and knowledge-synthesis re-proposes it with that status's warrant. Promotion runs through a verifier outside this skill: two independent spans for GROUNDED, a checkable chain, a checker or the pre-registered decision rule in `analysis.md` for DERIVED (knowledge-synthesis, `references/claim-record.md`, lists them). A survived red team means "worth the cost of verifying", and a survived record keeps the status its certifier gave it, never a higher one.

Inside a research-loop project, write the verdict and the attack log to `reviews/<date>-<label>.md`, label `outer<k>` for the k-th outer loop of the day or the claim's slug for a single attack, one entry per record (`C7: survived | wounded, conceded: <the exact Conditions text> | died: <wound>`), followed by the attack log. research-loop reads this file at its merge and writes the record's `Red team` field from it; this skill writes no other project file. Standalone, return the same content inline.

## The rubber-stamp guard

The pass condition is having genuinely hunted, not having found nothing. A verdict with no attack log is a blessing, not a red-team. If nothing lands, report *which* attacks were run and why each failed; that log is the deliverable.

## Routes

Wounded conjecture -> back to **disciplined-invention** for repair or burial. A factual doubt -> **grounded-claims** (retrieve and check the span). A testable objection -> stated as a candidate hypothesis in the verdict; research-loop writes it into `research-state.yaml` and probes it first (exploration-triage), and only a graduated hypothesis reaches **experiment-design**. The verdict -> back to the caller (**knowledge-synthesis**, **research-loop**, the user) with the attack log attached; research-loop, not this skill, merges the survivors into `findings.md`.
