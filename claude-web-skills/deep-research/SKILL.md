---
name: deep-research
description: Use this skill to investigate a topic exhaustively and coherently, like a pinnacle researcher or detective, rather than running one quick search. Triggers include "research X thoroughly", "find everything on", "dig into", "deep dive", "investigate", "leave no stone unturned", comparative or multi-part questions, and any topic where a single search would miss most of what matters. It decomposes the question into sub-questions and entities, follows each thread iteratively (each finding generates the next query), triages sources by primacy and quality, actively seeks disconfirming evidence and the strongest opposing case, files every finding against a sub-question, surfaces conflicts rather than averaging them, and stops only at saturation with every load-bearing claim corroborated. Pairs with knowledge-synthesis to distill what it gathers, grounded-claims for provenance, and red-teaming-research for adversarial coverage. Do NOT use it for a single quick fact lookup (just search once).
---

# Deep research (the internet detective)

A pinnacle investigator does not search more; they search until the picture stops changing and every load-bearing claim is nailed down. The work is closing the gap between what you have found and what would change the answer, then closing it again, until nothing moves.

## The invariant

**Coverage is measured by saturation and corroboration, not by query count.** The investigation is done when three things hold together: new searches return material you already have (saturation), every claim the conclusion rests on is confirmed by at least two independent quality sources, and you have actively hunted the strongest evidence against the conclusion and reported what you found. Stop short of that and the answer is a guess wearing citations; go past it and you are rabbit-holing. Neither volume nor confidence substitutes for these three conditions.

## Decompose, then follow the thread

Two motions, interleaved.

**Decompose.** Break the question into its sub-questions and the specific entities, claims, dates, numbers, and people it depends on. Each becomes a thread to resolve. A combined query ("everything about X") returns shallow results for all of it; search each thread separately and deeply.

**Follow the thread (iterative deepening).** Do not fix a query list up front. Let each finding generate the next query, the way a detective lets one fact point to the next. A name in a footnote, a figure that seems off, a claim with no source: each is a lead. Reason from the specific to the general, then test the general against more specifics. Keep going down a thread until it resolves or saturates, then return to the others.

## Source triage (a lead is not a fact)

Weight by primacy and quality, and corroborate. Read `references/source-triage-and-search.md` for the full hierarchy and query craft. The spine:

- **Primary over secondary over tertiary.** Go upstream: follow a news story to the paper, the paper to its data, the quote to the transcript, the statistic to the agency that produced it. A claim repeated by ten aggregators is one source, not ten.
- **Original over derivative.** Company filings, peer-reviewed work, primary documents, court records, datasets, and source code beat blog summaries and SEO content farms. Skip forums and content mills unless they are themselves the subject.
- **A single source is a lead.** Promote a claim to "established" only on independent corroboration. When sources conflict, do not average them; surface the conflict, weight by source quality and evidence, and say which you trust and why (this is grounded-claims' discipline applied live).
- **Recency where it matters.** For anything that changes (roles, prices, laws, state of the art), prefer the newest reliable source and use the actual current date in queries.

## Search adversarially, not just confirmingly

Confirmation is easy and misleading. Three habits force real coverage:

- **Seek the disconfirmation.** For the answer you are forming, deliberately search the strongest case against it and the most credible critics. If you only find support, you have not finished searching (hand the emerging conclusion to red-teaming-research).
- **Seek the absence.** Ask: if this were true, what else should exist, and is it there? A claimed breakthrough with no independent replication, a company with no filings, an expert with no record. Missing expected evidence is itself evidence.
- **Reformulate, do not repeat.** A query that misses is rephrased with different terms, a different angle, a different source type, or a more specific anchor. Repeating the same words does not change the results.

## Stay contextually coherent

Hold a model of the question the whole time. Every retrieved item is filed against the sub-question it answers; the irrelevant is discarded, not hoarded. A finding that does not bear on any open thread either opens a new thread or is dropped. Keep a running trail as you go (the research-log discipline): for each thread, what you searched, what you found, what it changed, and the next lead. This is what turns a pile of tabs into an investigation, and it is what research-loop persists to disk.

## Tools

Tool-agnostic. Use internal connectors for internal or proprietary data first, web search and fetch for the open web, and domain sources where they exist (academic indexes such as Semantic Scholar and arXiv, code search, public datasets, filings databases). Fetch the full source when a snippet is load-bearing; snippets are leads. Respect copyright: paraphrase, quote only briefly, never reproduce large copyrighted passages.

## Output: an evidence map (not a pile of links)

- **Per sub-question:** the corroborated finding, in one or two lines.
- **Sources:** primary first, with what each contributes; note independence (or that several trace to one origin).
- **Conflicts:** where sources disagree, the disagreement and which side the evidence favors.
- **Confidence + gaps:** how well-established each finding is, and the load-bearing questions still open.
- **What was sought and not found:** the disconfirming searches run and the expected evidence that is absent.

Hand the map to **knowledge-synthesis** to distill it into durable knowledge, and to **grounded-claims** so every figure keeps its source. Within a larger effort, this is the evidence-gathering node of **research-loop**.
