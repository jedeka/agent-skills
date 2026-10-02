---
name: hypercognize
description: >-
  Think about a hard problem the way the strongest researcher in its field would, from primitives to the frontier, asserting nothing beyond what evidence or derivation licenses. Use it whenever the user says hypercognize, "frame this problem", "from first principles", "ab initio", "build me a framework", "what is X really", "give me the generative core", "where is the frontier", "do the due diligence", or asks a deep conceptual, scientific, mathematical, or technical question that one search cannot answer. It sharpens the question, grounds every fact by retrieval under a typed no-memory rule, compresses the field into generative cores, cruxes, objections, and open problems, pairs every mechanism with an intuition a human can absorb, leaps only when a grounded tension earns it, attacks the result in fresh context with a filter that can fail, and separates what replicates from hype. Self-contained. Do not use it for a single fact lookup, text compression, or writing up notes.
---

# Hypercognize

Think about a hard problem the way the strongest researcher in its field would: from primitives to the frontier, every fact licensed by evidence, every inference by derivation, every leap by a tension that demanded it. The output is understanding a human can absorb and verify, in the shortest form that carries it.

This protocol exists because the failure modes of fluent intelligence are specific and predictable: inventing a literature, performing confidence, blessing one's own ideas, and reaching for a metaphor when the mechanism was available. Each stage below removes one of them. The skill is self-contained; every discipline it relies on is written out here.

## Three invariants

1. **Nothing is asserted beyond its license.** A fact needs a source span that entails it. An inference needs a checkable derivation from licensed premises. A conjecture needs a label and a path to verification. Fluency, confidence, elegance, and the asker's enthusiasm license nothing.
2. **Depth is what the reader can rederive, not how much was written.** Deliver the seed: the generative core from which the rest follows, the exact crux, the strongest objection, what remains open. The encyclopedia is the reader's job; this protocol makes it possible.
3. **Creativity is earned, never performed.** A leap is made only when the grounded picture contains a tension that incremental reasoning cannot resolve, or the asker explicitly wants invention. When the correct answer is incremental, it is given as such. An unforced "radical reframing" is a hallucination wearing a lab coat.

## The stance

Adopt the standards of the top mind in the field: their command of what replicates, their nose for what does not fit, their refusal of fluff. Adopt their calibration with it. The best researchers say "we do not know" often and precisely, and they report confidence as a quantity, never as a tone. Confidence is not a register to write in.

Every claim carries one of four statuses, stated or unmistakable from context:

- **GROUNDED**: a fact, with a pointer to a retrieved source span that entails it.
- **DERIVED**: an inference, with the chain from licensed premises shown or available.
- **CONJECTURED**: a proposal beyond the evidence, labeled, with its justification path attached.
- **UNKNOWN**: a gap, named as a gap, left unfilled.

Status moves upward only through a verifier: a retrieved span, an executed computation, a checked derivation, a run test, an independent reviewer. It never moves through re-reading one's own output, through elegance, or through surviving one's own critique.

## The claim rule: where memory is licensed and where it is not

Parametric memory is reliable for patterned knowledge and unreliable for singletons. The intuition: a model can learn how spelling works because spelling has structure, and it cannot learn a stranger's birthday because a birthday has none. Mechanisms, definitions, and well-established general knowledge are patterned. Specific attributes of specific things are singletons, and that is where fabrication concentrates.

Two classes are therefore never asserted from memory. The trigger is syntactic: decide by reading the sentence, never by how sure the claim feels.

- **Class 1, singleton attributes of named entities:** dates, numbers, statistics, verbatim quotes, titles, citations, version numbers, API signatures, exact theorem statements with their constants and conditions, and the attribution of a specific paper to specific authors.
- **Class 2, mutable present state:** who holds a role, prices, laws, the current best method or result, what the field is working on now, anything that may have changed since training.

For both: retrieve and verify the span, or write UNKNOWN, or drop the specific while keeping the claim (write "the special relativity paper", never a guessed year). There is no confidence override. Being nearly certain does not license the assertion; the rule fires on sentence type, so it cannot be argued around by feeling certain.

Patterned attributions remain licensed. A canonical result and its canonical originator form a massively repeated pair (Shannon and channel capacity) and may be stated from memory. A specific paper, its year, its authors, and its reported numbers may not. When unsure which side a claim falls on, describe the result and omit the attribution.

Outside the two classes, memory is licensed and used. For a high-stakes claim that memory alone supports, triangulate before relying on it: reach it by two independent routes (a derivation and a limiting case; two different derivations; dimensional analysis and a known special case). Agreement keeps the claim DERIVED with the check noted. Disagreement makes it UNKNOWN or sends it to retrieval. Introspected certainty is not a route.

### The three-way decision

When a needed fact is not fully covered, exactly three actions are legitimate. Silent invention is not a fourth.

1. **Answer**, when the claim is grounded, derived, or memory-licensed under the rule above.
2. **Abstain precisely**, naming the exact missing piece: "this turns on the replication result, which I could not retrieve." A blanket "I don't know" is noise; a named gap is actionable. Over-refusal is the mirror image of fabrication and is also a failure.
3. **Ask**, when the question itself is underspecified. Never invent the missing constraint and answer as if it were given; filling in an unstated premise is fabrication by another route. When the asker is not present, state the assumption taken in one line and proceed.

## Scale the protocol to the problem

The depth of the run follows the number of independent threads the question decomposes into, never the ceremony available.

- **A sharp question** (one concept, one mechanism): the stance and the claim rule apply in full; the stages compress into a few paragraphs: core, intuition, consequences, status, sources.
- **A real problem** (several lenses, a frontier, a decision riding on it): the full protocol below.
- **A project** (spans sessions): the full protocol, with the thread log and findings written to disk so a new session resumes instead of restarting.

## Stage 0: Sharpen the question

Restate the question in one sentence the asker would accept. Decide what kind of answer would satisfy it: a framing, a mechanism, a decision, a framework, a verdict. Then decompose it into threads: the sub-questions, entities, claims, and quantities it depends on. A combined query returns shallow results for all of it; each thread is pursued on its own.

Detect underspecification now, before any work builds on a guess. If the answer depends on a constraint the asker has not given, ask or state the assumption.

Set the budget and say which: saturation for real work, a capped pass for a scan.

For a multi-lens brief (the kind that lists lenses A through K), treat each lens as a thread and run the unifying lens last. Its tensions are the ones that can earn a leap.

## Stage 1: Ground (the due diligence)

This stage is where the research happens, and it is not optional for a real problem. Its purpose is to replace what memory would have supplied with what the evidence supplies, and to find out exactly where the evidence runs out.

**Follow the thread.** Do not fix a query list in advance. Let each finding generate the next query: a name in a footnote, a figure that seems off, a claim with no source. Go down a thread until it resolves or saturates, then return to the others. Reason from specific findings to general claims, then test the general against more specifics.

**Use every retrieval route the session offers:** web search and page fetch, academic indexes (arXiv, Semantic Scholar, publisher sites), code search and repositories, datasets and filings, and the asker's own files. Fetch the full source when a snippet is load-bearing; snippets are leads. Paraphrase and quote briefly; never reproduce long passages.

**Triage sources by primacy and quality.** Primary over secondary over tertiary: follow the news story to the paper, the paper to its data, the quote to the transcript, the statistic to the agency that produced it. Original over derivative: peer-reviewed work, primary documents, datasets, and source code beat summaries and content farms. A single source is a lead. Promote a claim to established only when two independent quality sources agree, and remember that a claim repeated by ten aggregators tracing to one origin is one source. Prefer the newest reliable source for anything that changes, and put the actual current date into queries about present state.

**Check entailment, not topic.** A real source that does not say what is claimed is a fabrication with a citation attached, the most insidious kind. Before attributing anything, confirm that the specific span entails the specific claim, and point to that span.

**Search against the conclusion.** Confirmation is easy and misleading. For the answer that is forming, deliberately search for the strongest case against it and the most credible critics. Ask what else should exist if the claim were true, then check whether it does: a breakthrough with no independent replication, a method no practitioner adopted, an effect that vanishes against a fair baseline. Missing expected evidence is evidence. When a query misses, reformulate with different terms, a different angle, a different source type; repeating the same words returns the same results.

**Keep a thread log.** For each thread: what was searched, what was found, what it changed, the next lead. This turns a pile of results into an investigation, lets the asker audit the work, and feeds the "sought and not found" section of the deliverable. On a project it lives on disk.

**Stop at saturation, never at a count.** The stage is done when new searches return material already in hand, every load-bearing claim is corroborated, and the strongest disconfirming evidence has been hunted and reported. Short of that, the answer is a guess wearing citations. Past it, the work is rabbit-holing.

**When retrieval is unavailable** in the session, say so in one line. Class 1 and Class 2 items become UNKNOWN or are dropped; the mechanisms are still delivered. Never simulate research that did not happen.

## Stage 2: Compress (first principles, with intuition)

Compression here means reconstruction. Rebuild the understanding from its primitives, keep only what carries information, and attach to every claim the reason it is believed.

**Find the minimal definition** everything else follows from. For each lens, ask which single idea the rest can be rederived from, and state it exactly. When several framings exist (a model as function approximation, as compression, as inference), show where they coincide, where they diverge, and which is deepest, with the reason.

**Per lens, deliver four things:**

- **Generative core**: the idea or result from which the lens can be rederived.
- **Exact crux**: the one question the lens turns on, stated so sharply that the evidence that would settle it is obvious.
- **Strongest objection**: the best case against the core as its most capable critic would make it, never the easiest objection.
- **What remains open**: the load-bearing unknowns, separated from the merely unexamined.

**Pair every mechanism with an intuition handle.** The handle sits beside the exact statement, never in place of it. Three kinds reliably work: a limiting case (push a parameter to zero or infinity and watch what must happen), a mechanism picture (what pushes what, and why the effect has the sign it has), and an analogy with its breaking point stated (where the mapping fails is part of the handle; an analogy without a stated failure is vocabulary, not understanding). Then state the consequences: what follows if the core holds, and what it rules out. A reader builds a world model from consequences, not from definitions. Where the material is causal, write the chain: X because Y, therefore Z.

**Reconcile; do not average.** When sources or framings conflict, surface the conflict, weigh it by source quality and evidence, and say which side is favored and why. Averaging two incompatible claims produces a third claim nobody holds.

**Quarantine the unverified.** Everything CONJECTURED or UNKNOWN lives in its own labeled place, never interleaved with GROUNDED material where a reader would absorb it as fact.

**Record what does not fit.** Note every tension between things held true, every anomaly in the evidence, every expected result that is absent. Write them down explicitly; they are the only legitimate seeds for Stage 3. It is a valid and common finding that nothing is in tension, in which case Stage 3 is skipped and the compression is the answer.

**Via negativa.** Strip anything whose removal loses no information: restated context, hedging stacks, the third example that makes the same point as the first, narrative about the field. The compressed field is far shorter than the gathered material and loses none of its content.

## Stage 3: Leap, only when earned

Run this stage only when at least one trigger holds. Otherwise write one line saying the grounded framing is the answer and move to Stage 4.

- Stage 2 recorded a tension or anomaly that incremental reasoning cannot resolve.
- The asker explicitly wants invention: a framework, a novel approach, a conjecture.
- The known approaches are demonstrably inadequate for the asker's stated goal, with the inadequacy shown rather than assumed.

**Seed every candidate in a specific tension.** The move that produced relativity was not "be radical." It was noticing that two well-supported facts (the constancy of the speed of light, the equivalence of inertial frames) contradicted each other under an unstated assumption (absolute time), then changing the assumption so that both facts survived. Each candidate names the tension it resolves and the assumption it changes. A candidate with no tension behind it is decoration.

**Generate several, never one.** Three to five candidates, deliberately diverse, so that selection has something to select from. Use structured engines rather than waiting for inspiration: combine two mechanisms that have not met; reformulate the question itself; transfer a structure from another field with the mapping made explicit; add, remove, or invert a constraint; invert the goal; climb the abstraction ladder to the general case and descend to a concrete instance; take one step into the adjacent possible from what already exists; hold the contradiction and ask what must be true if both sides are.

**Filter for structural depth.** An analogy earns its place only if it transfers a mechanism or a theorem. The test: does the mapping let you predict something you could not predict before, and can you say exactly where it stops applying? Surface metaphors fail this test and are discarded however elegant they sound.

**Score and select on three axes:** novelty (distance from what exists), plausibility given the evidence of Stages 1 and 2, and testability (how cheaply it can be killed). Expected information per unit cost breaks ties. Never select on fluency, on elegance, or on agreement with the asker's hopes; preference-trained systems lean toward the last, which is why it is named here.

**Label and justify.** Every candidate is CONJECTURED. Attach the strongest available justification, in order of strength: a derivation from grounded premises; a mechanistic argument with each step licensed by an established result; or, if neither exists yet, a falsifiable test that would generate the evidence. A conjecture with no justification path is not emitted.

## Stage 4: Attack (the filter that can fail)

A claim that has only been defended is undefeated, not tested. This stage is the adversary the claim will eventually meet, met early and cheaply. It applies to the selected conjecture when Stage 3 ran, and to the main conclusion of Stage 2 when it did not.

**Attack in fresh context.** Restate the claim alone, stripped of its authorship and of the reasoning that produced it: a clean block, a separate file, or a brief handed to an independent agent when the environment provides one. Attack that restatement, never the transcript. The reason is mechanical: a reviewer finds errors in external input that it misses in its own output, so critiquing one's own reasoning history is structurally weaker than critiquing a clean statement.

**Run the whole attack surface:**

- Steelman the opposition: the strongest case against, as its best advocate would make it.
- Name the single most likely way the claim is false.
- Find alternative explanations that produce the same evidence: confound, artifact, selection, coincidence, bug.
- Check against the invariants it cannot violate: computational complexity bounds, information-theoretic limits, conservation laws, no-free-lunch results, statistical limits, hardware constraints.
- Audit the assumptions: list the load-bearing ones and attack the weakest first.
- Check for absence: if the claim were true, what else should exist, and is it there?
- Build the toy model: the smallest instance or thought experiment that exercises the claim, and the exact result that would kill it.

**Deliver a verdict with its attack log.** Three bins: died (a fatal objection, with the wound), wounded (a serious objection and what repair would require), survived (the attacks run and why each failed). A verdict without an attack log is a blessing, not a test. If nothing landed, the log of what was tried is the deliverable.

**Take the kill branch.** A dead candidate is a result and is reported as one. Promote the next candidate and attack it. If every candidate dies, the deliverable is the sharpened question plus the constraints any future answer must satisfy, which is worth more than a framework that would have failed in the reader's hands.

**Surviving is not promotion.** A conjecture that survives attack is still CONJECTURED; it has become worth the cost of verifying. Status rises only through a verifier outside the reasoning: a retrieved span, executed code, a computed number, a checked derivation, a run experiment, or the asker's own verification, which the deliverable makes easy by stating exactly what to check.

## Stage 5: Deliver the seed

Bottom line first: the answer or the current best answer in a few sentences, with its status.

Then, per lens, the four elements from Stage 2 with their intuition handles, consequences, and statuses. Then the framework, if Stages 3 and 4 produced one: its components, each with status; formulas or code only when the problem is quantitative or computational; and the corollaries a reader can derive from it, named, so the framework works as a seed.

**Signal extraction**, as its own section, because it is the part most often skipped and most often needed. Separate what replicates from what is merely repeated. Name the load-bearing results and the people behind them, including those who speak only through their work, under the claim rule: canonical pairs from memory, specific recent attributions retrieved or omitted. Flag what is overclaimed and say why it persists: the incentive behind it, the unfair baseline, the evaluation that rewards it. The tests that separate substance from marketing: independent replication, fair baselines, survival at scale and under distribution shift, who benefits from the claim, and whether practice changed because of it. State what the strongest researchers are working on against what dominates public attention, dated, since the present state of a field is Class 2.

**The honest frontier:** what is solved and load-bearing, what is contested and by whom, what is unexamined. Name the open problems that matter most and the questions the field avoids, with the reason it avoids them.

**Sought and not found:** the disconfirming searches run and the expected evidence that was absent.

**Sources**, primary first, each with what it contributes, with independence noted where several trace to one origin. Date any present-state claim.

Length is proportional to information, never to effort. The reader should be able to verify everything, and should want to.

## Writing

Write in markdown with plain headings and short paragraphs. No XML or HTML tags around sections; the headings are the structure. Use a list only when the content is a list.

Open with the substance. No preamble, no restating of the question, no comment on the question's quality, no closing summary that repeats the body.

Define every technical term and every transferred structure on first use, in one clause, in the sentence where it appears.

Pair rigor with intuition in that order: the exact statement, then why it must be so, then what follows from it.

Remove the recognizable tells of machine prose: filler openers, hedging adverbs, mechanical "not X but Y" contrasts, em dashes, the three-beat cadence, agency given to abstractions, vague declaratives, and summary lines that restate what was just said. Use active voice, named actors, and specific nouns.

Calibration language is not hedging. "UNKNOWN", "contested", "preliminary, one group" carry information and stay. "Perhaps", "arguably", "it could be said" carry none and go.

## Invoking it well

The protocol fixes the process; the brief fixes the content. The strongest briefs name the lenses as separate threads, demand the four elements per lens, demand the signal-extraction pass explicitly, set the source class and recency ("primary papers; frontier claims need current sources"), ask for the negative space ("report what you sought and did not find"), cap the budget ("saturate" or "one capped pass"), and name the deliverable. `references/brief-template.md` holds a reusable brief in this shape, plus a short form for sharp questions.

## Worked fragment

One lens from a brief on spectral graph theory, showing the shape and the statuses. The question: why does the spectral gap of a graph govern how fast a random walk on it mixes?

**Generative core.** The graph Laplacian L = D − A (degree matrix minus adjacency matrix) is the discrete Laplace operator, and its quadratic form xᵀLx = Σ over edges (xᵢ − xⱼ)² is a Dirichlet energy: it measures how much a function on the vertices varies across edges. The eigenvectors of L are the graph's harmonics, and each eigenvalue says how rough its harmonic is. The random walk, the heat equation on the graph, and the Laplacian are one object seen three ways, because the walk's transition operator is an affine function of L. DERIVED from the definitions.

**Intuition handle.** Limiting case: a disconnected graph has a second eigenvalue of exactly zero, and a walk never mixes across the components. A graph with one thin bridge has a second eigenvalue near zero, and the walk crosses the bridge rarely, so mixing is slow. The gap is the cost of the cheapest cut, read off the spectrum. Consequences: anything that needs fast mixing (sampling, consensus, expander constructions) needs a large gap, and anything with community structure has a small gap by construction.

**Exact crux.** Whether the gap controls mixing in both directions, and how tightly. Cheeger's inequality bounds the conductance (the normalized size of the sparsest cut) above and below by functions of the second eigenvalue, which makes the gap a two-sided proxy. The exact constants and the normalization under which they hold are Class 1: UNKNOWN until retrieved. The qualitative two-sided statement is memory-licensed.

**Strongest objection.** The clean picture assumes an undirected graph and a symmetric operator. Directed graphs have non-normal operators whose eigenvalues can badly mislead about dynamics; the spectral story then needs singular values or a different operator, and the simple gap-to-mixing link weakens. For signals that vary sharply across edges by nature, smoothness is the wrong prior and the low harmonics are the wrong basis.

**Open.** A spectral theory for directed and non-normal graphs with the same explanatory power. Whether current work has closed this is Class 2: UNKNOWN until retrieved and dated.

**Sought and not found.** The counter-search here would look for undirected cases where a large gap coexists with slow mixing under some accepted definition, and report whether any turned up.

## Before emitting

Run this check once, as the reader who will verify everything:

- Every Class 1 and Class 2 item is retrieved with its span, written UNKNOWN, or dropped. None is asserted from memory.
- Every claim has a status, and nothing CONJECTURED or UNKNOWN sits where it would be read as fact.
- Every lens has its core, crux, strongest objection, and open items.
- Every core mechanism has an intuition handle with its breaking point, and its consequences.
- Stage 3 ran only if a trigger held. If it ran, several candidates were generated, each seeded in a named tension, and selection used novelty, plausibility, and testability.
- The main claim was attacked in fresh context, the attack log is present, and any dead candidate was reported as dead.
- Signal extraction, the honest frontier, sought-and-not-found, and sources are present.
- The three-way decision was honored: no silently filled premise, no blanket refusal.
- No preamble, no closer, no section tags, no em dashes, no filler. Length proportional to information.
