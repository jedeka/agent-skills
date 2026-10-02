---
name: disciplined-invention
description: Use this skill whenever the agent must be genuinely creative or original, proposing a new conjecture, proof strategy, mechanism, hypothesis, algorithm, or alpha signal that goes beyond established sources. Triggers include "discover", "conjecture", "novel approach", "invent", "find an edge", "new proof", "fill the gap", "is there a better method", or any request to create rather than retrieve. It lets the agent invent freely while forbidding unverified assertion. It makes the agent label the claim as conjecture, justify it by derivation or mechanism or a falsifiable experiment plan, red-team it, route it to a verifier that does not trust the model, and report with epistemic status intact. Do NOT use it for ordinary factual claims (use grounded-claims) or for triaging which idea to try first (use exploration-triage).
---

# Disciplined invention (creativity without hallucination)

Invention is not hallucination — *if* it is labeled and gated. Hallucination is an unwarranted assertion presented as fact. A legitimate conjecture is a warranted proposal presented *as* a conjecture, carrying a path to verification. The entire difference is the label and the path. Invent freely; assert nothing unverified.

## The invariant

**Epistemic status moves up only through a verifier — never through confidence, fluency, or elegance.** A beautiful conjecture that survives hard scrutiny is still a conjecture until a checker certifies it.

## The protocol

1. **State it as a conjecture.** Name it, state it precisely, and give the pattern or gap it exploits and *why it is plausible* — the mechanistic, architectural, or mathematical reason it should hold. Attach a rough prior and what it rests on.
2. **Justify with the strongest available support, in order of strength:**
   - a rigorous derivation from grounded premises (machine-checkable if formal); else
   - a mechanistic argument, each step licensed by an established result; else
   - if neither yet exists, a *falsifiable experiment or proof plan* that would generate the evidence.
   Never present a conjecture with no justification path attached.
3. **Red-team it** (hand to red-teaming-research): the strongest counter-argument, the most likely way it is false, the cheapest disconfirming test, the known results that threaten it.
4. **Route to a verifier that does not trust the model:**
   - formal claim → proof assistant (Lean / Coq / Isabelle); only a checked proof is PROVEN;
   - algorithm → execute it against tests (property-based, adversarial, edge cases);
   - empirical or quant claim → a pre-registered, multiple-testing-corrected, out-of-sample, cost-aware gauntlet (hand to experiment-design + empirical-analysis).
   Only the verifier's verdict promotes status.
5. **Report with status intact:** "Conjecture (prior ~X), justified by [derivation / mechanism / plan], survives [checks passed], fails [checks failed], residual risk [Y]; status now [conjectured / partially-verified / proven]." Never round a surviving conjecture up to "fact."

## Self-improvement (the safe flywheel)

A conjecture the verifier certifies graduates into the trusted knowledge base and becomes grounded context for future work. One that dies is logged *with the reason*, so it is not re-proposed. Only verified outputs ever enter the trusted store — that single rule is what keeps the self-improving loop free of accumulated hallucination.

## Domain notes

- **Math:** autoformalize the statement, search for the proof, let the checker certify. The checker guarantees the proof — *of the formalized statement*. Back-translate the formal statement to confirm it matches the intended claim, or you may prove the wrong theorem. The residual risk lives in the formalization, not the proof.
- **Quant:** the backtest is a weak, easily fooled verifier. The gauntlet must be brutal — guard against lookahead and survivorship bias, transaction costs, and capacity, and above all multiple testing; report deflated performance and the probability of backtest overfitting. "Verified alpha" means "survived the gauntlet with quantified false-discovery risk," never "guaranteed edge."
- **Facts:** cross-source confirmation; a single source is a lead, not a fact.
