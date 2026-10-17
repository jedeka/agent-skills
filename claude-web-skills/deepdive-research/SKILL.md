---
name: deepdive-research
description: >-
  Gather evidence on a question the way a strong researcher does, and hand back an evidence map rather than a report. Use for "research X thoroughly", "find everything on", "dig into", "deep dive", "investigate", "what does the literature say", "what is the state of the art", comparative or multi-part questions, and any question one search cannot settle. It splits the question into threads, runs parallel researcher subagents plus one adversary that hunts the counter-case, requires two independent sources before a claim counts, traces every figure to its origin, records the exact passage with URL and date, stops at saturation, and writes notes to disk for knowledge-synthesis. Runs in a single context when subagents are unavailable. Not for a single fact lookup or for producing a finished prose report.
---

# Deepdive research

The investigation is done when the picture stops changing and every claim that matters rests on independent evidence. Volume of searching is not the measure; saturation and corroboration are. Stop short and the answer is a guess wearing citations. Go past and you are rabbit-holing.

This skill gathers and triages evidence. It does not synthesize, judge or write prose. Those belong to knowledge-synthesis, red-teaming-research and the caller. Keeping the gatherer free of conclusions is what makes its output usable downstream.

## Three rules that hold in both modes

1. **Two independent sources make a fact; one makes a lead.** Ten outlets repeating one press release are one source. Each note records where a claim originated and whether this source is the origin or an echo.
2. **Hunt the counter-case.** For the answer that is forming, search for the strongest evidence against it and the most credible critics, and ask what else should exist if the claim were true. Missing expected evidence is itself a finding and goes in the map.
3. **Record the passage, not the page.** Every finding carries the exact quoted span, the URL, the date it was true, the source type, and the numbers with their conditions. Downstream skills check entailment against the span. A link alone cannot be checked.

## Choose the mode

- **Sharp question** (one or two threads, an afternoon's reading): work in the current context, following the rules in `references/researcher.md` yourself. Write notes to the same place the fan-out would.
- **Real question** (three or more threads, or a frontier that moves): fan out, as below. Fan-out costs several times the tokens of a single pass, so reserve it for questions that earn it.
- **No subagent tool in this session**: work in the current context for any size of question, thread by thread, and say so in the map.

## Where notes go

Inside a research-loop workspace (a `research-state.yaml` exists in the project root or a parent): `literature/<thread-slug>.md`, one file per thread, plus `literature/evidence-map.md`.

Standalone: `./deepdive/<title>/` with the same layout. The title is three to six words in sentence case, letters and spaces only. If a folder with that title exists from an earlier run on the same topic, append what is new and label it; never overwrite earlier notes.

## The fan-out

**1. Clarify, only when it changes the search.** Ambiguous terms, an unstated region or period, a name that fits several entities. One short question; otherwise state the assumption in the map and proceed.

**2. Decompose into threads.** Sub-questions, and the entities, quantities, dates and claims the answer depends on. Threads should be exclusive and together cover the question. For each thread write one line that says what observation would settle it. That line goes to the researcher and is their stop condition.

**3. Spawn researchers in parallel, one per thread, plus one adversary.** Use the Agent tool with `subagent_type="general-purpose"`, all in one turn. Each brief carries:

```
Research thread: <thread>
Settles when: <the observation that would settle this thread>
Constraints: <period, region, source types, anything inherited from the question>
Write notes to: <absolute path>/literature/<thread-slug>.md
First read <skill directory>/references/researcher.md and follow it exactly.
```

The adversary gets `references/adversary.md` instead and the full question with the emerging shape of the answer, if one is forming. Its job is the strongest case against, the alternative explanations, and the expected evidence that is missing.

Do not read the researcher brief yourself when fanning out. The coordinator's job is to hold the question and judge the returns; the brief is long by design and belongs in the subagents' context.

**4. Validate every note before accepting it.**

```bash
python3 <skill directory>/scripts/validate_notes.py <absolute path>/literature/
```

The validator lists each finding that lacks a quote, URL, date, source type, origin, claim type or settling status. Send a failing note back to its researcher with the validator's output. Accept nothing that fails.

**5. Check saturation, then allow at most one more round.** Read the summaries the researchers returned, not their notes. A thread is saturated when its settling observation was found or shown to be absent, its load-bearing claims have two independent sources, and the adversary's attack on it has been answered or recorded as open. Spawn a second round only for threads that fail that test, with briefs that name the gap. After the second round, stop regardless; a remaining gap is a finding.

**6. Write the evidence map** from the returned summaries and the validated notes, following `references/evidence-map.md`. The map carries findings per thread with their sources and independence, conflicts with the weight of evidence on each side, the adversary's surviving objections, gaps, what was sought and not found, and the date of the search. No conclusions, no prose synthesis.

**7. Hand back.** Return the map's path and a summary of a few lines: threads covered, what is established, what is contested, what is open. The caller (knowledge-synthesis, research-loop, or the user) takes it from there.

## Single-context mode

Follow `references/researcher.md` thread by thread, then `references/adversary.md` against your own emerging answer, writing the same notes to the same paths. Run the validator on your own notes. The temptation in this mode is to skip the adversary pass because the answer already feels settled; that feeling is the reason the pass exists.

## Bundled files

- `references/researcher.md`: the research craft and the note format. Read by researcher subagents, or by you in single-context mode.
- `references/adversary.md`: the counter-case brief.
- `references/evidence-map.md`: the output template.
- `scripts/validate_notes.py`: checks notes for required fields. Run it; do not read it.
- `scripts/citations.py`: optional lookup of references and citing works through the OpenAlex API. Fails quietly when the network is unavailable.
