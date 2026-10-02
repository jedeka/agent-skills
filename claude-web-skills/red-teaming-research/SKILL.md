---
name: red-teaming-research
description: Adversarially attack any claim, conclusion, design, or emerging story to find how it fails before reality does. Triggers include "red-team this", "stress-test", "poke holes", "devil's advocate", "what am I missing", "is this actually right", any conjecture leaving disciplined-invention, any conclusion emerging from deep-research or empirical-analysis, and any finished claim or published result to attack. It receives the claim as an anonymous external artifact in fresh context (never as "my own reasoning"), hunts the strongest counter-argument, alternative explanations, threatening known results, and the cheapest disconfirming test, then returns a severity-ranked verdict of what died, what is wounded, and what survived. Do NOT use it to keep a live iteration loop honest (use honest-iteration) or to verify a factual citation (use grounded-claims).
---

# Red-teaming research (attack it before reality does)

A claim that has only been defended is undefeated, not tested. The job here is to be the adversary the claim will eventually meet — a hostile reviewer, a competing lab, the market, reality — and meet it first, cheaply.

## The invariant

**The critic never trusts the author, including when the author is you — so the attack happens in fresh context.** The claim arrives as an anonymous external artifact: restated verbatim, stripped of its authorship and the reasoning history that produced it. This is mechanism, not ritual: reviewers reliably find errors in external input that they miss in their own output, so attacking your own transcript is structurally weaker than attacking a clean restatement. Practically — write the claim alone into a file or a clean block (or hand it to a sub-agent), then attack *that*, never the conversation.

## The attack surface (run all of it)

- **Steelman the opposition.** Construct the strongest case *against*, as its best advocate would — not the easiest objection.
- **Rank the failure modes.** What is the single most likely way this is false?
- **Alternative explanations.** What else produces the same evidence — confound, artifact, selection effect, coincidence, a bug?
- **Threatening known results.** What established findings, theorems, or prior failures does this collide with?
- **Assumption audit.** List the load-bearing assumptions explicitly; attack the weakest one.
- **Absence check.** If this were true, what else should exist — and is it there? Missing expected evidence is evidence.
- **Cheapest kill.** Name the single cheapest observation or test that would disconfirm it.

## The verdict (output)

Severity-ranked, three bins: **died** (a fatal objection, with the wound), **wounded** (a serious objection and what repair would require), **survived** (attacks tried and why they failed). Always attach the cheapest disconfirming test and the residual risk. Surviving is not truth — promotion of status still runs through a verifier (disciplined-invention's invariant), and a survived red-team only means "worth the cost of verifying."

## The rubber-stamp guard

The pass condition is having genuinely hunted, not having found nothing. A verdict with no attack log is a blessing, not a red-team. If nothing lands, report *which* attacks were run and why each failed; that log is the deliverable.

## Routes

Wounded conjecture → back to **disciplined-invention** for repair or burial. A factual doubt → **grounded-claims** (retrieve and check the span). A testable objection → **experiment-design** (turn the cheapest kill into a real test). A conclusion that survives → back to the caller (**deep-research**, **knowledge-synthesis**, **research-loop**) with the attack log attached.
