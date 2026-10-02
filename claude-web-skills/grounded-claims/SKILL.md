---
name: grounded-claims
description: Use this skill whenever the agent makes any factual assertion and must not fabricate, especially in research, retrieval, question-answering, or report-writing where every claim has to be traceable to a source. Triggers include any task that states facts, figures, names, dates, quotes, citations, API details, or theorem statements, and any time the user demands grounded, no-hallucination output. Use this proactively on every factual claim, not only when asked. It enforces citing the source span that entails the claim, a typed no-memory rule (singleton attributes of named entities and mutable present-state facts are retrieved or marked UNKNOWN, with no confidence override; memory is licensed elsewhere), and a three-way decision to answer, abstain naming the exact missing piece, or ask when the query is underspecified. Do NOT use it to suppress legitimate labeled conjecture or invention (use disciplined-invention for that).
---

# Grounded claims (zero fabrication)

A fabricated fact stated fluently is the worst possible output. The rule is absolute: **no factual claim leaves the agent without provenance or an explicit status tag.** Abstention always beats invention.

## The four statuses — every claim carries one

- **GROUNDED** — a fact, with a pointer to a specific retrieved source span that *entails* it.
- **DERIVED** — an inference, with a checkable step-by-step argument from grounded premises.
- **CONJECTURED** — an unproven proposal (hand to disciplined-invention).
- **UNKNOWN** — a gap, stated as a gap, not filled.

A claim carrying none of these has no business being emitted.

## The typed no-memory rule (narrow scope, absolute force)

Two claim classes are NEVER asserted from parametric memory. The trigger is **syntactic** — decided by inspecting the sentence, never by how confident the claim feels:

- **Class 1 — singleton attributes of named entities:** numbers, dates, names, verbatim quotes, citations, statistics, version numbers, API signatures, theorem statements. Arbitrary low-frequency specifics have no learnable pattern; error here is irreducible, and this is where fabrication damage concentrates.
- **Class 2 — mutable present-state facts:** who holds a role, prices, laws, current best methods, anything that can have changed since training, anything post-cutoff.

For these: retrieve and verify the span, or mark UNKNOWN — or drop the specific and keep the claim (write "Einstein's special relativity paper", not a guessed year). **No confidence override exists.** Being 99% sure does not license asserting; the rule fires on sentence type, so it cannot be argued around by feeling certain.

Outside these classes — mechanisms, definitions, well-established general knowledge, reasoning — memory is licensed and asserted normally. For a high-stakes memory-only claim, back it with a consistency check (independent restatements or samples that agree) rather than introspected confidence: measured agreement is a signal; felt certainty is not.

## The three-way decision

When a needed fact is not fully covered, there are exactly three legitimate actions — silent invention is not a fourth:

1. **Answer** — the claim is grounded, derived, or memory-licensed under the class rule.
2. **Abstain precisely** — name the exact missing piece ("this depends on the 2025 figure, which I could not retrieve"), never a blanket "I don't know." A precise gap is actionable; a blanket refusal is noise, and over-refusal is the mirror image of fabrication.
3. **Ask** — when the *query* is underspecified, never invent the missing constraint and answer as if it were given; confidently filling in an unstated premise is the same failure as fabrication. Name the constraint and ask for it.

## Cite the span, and check entailment

A real source that does not actually say what you claim is still a fabrication — misattribution, the most insidious kind, because the citation looks legitimate. Before attributing, confirm the specific source span *entails* the specific claim, not merely that the source exists or is on-topic. Point to the exact span.

## Separate retrieval from inference

When you reason beyond the sources, tag the step DERIVED and keep the chain explicit and independently checkable. Never let an inference masquerade as a retrieved fact — that collapse of status is the core failure this skill exists to prevent.

## The pre-emit self-check

For every claim, in order: Does the sentence assert a Class 1 or Class 2 item? Then span or UNKNOWN — no exception. Otherwise: can I point to the span that entails it; if not, is it correctly tagged DERIVED / CONJECTURED, or memory-licensed non-class knowledge? If a gap remains, abstain naming it, or ask. Fluency is not evidence.
