---
name: ultra-summary
description: Compress any dense or messy text (meeting notes, a long document, a chat thread, research updates) into a maximally short digest with two tagged sections, [SUMMARY] at most two information-dense sentences and an optional [TODO] of numbered imperative action items compressed to minimum description length. Use this whenever the user wants the tightest possible summary plus action items, asks to "ultra-summarize" or for an "ultra summary", wants a TL;DR with todos, says "compress this hard" or "give me the gist and next steps", or pastes messy notes and wants a short tagged digest rather than full prose. Prefer this over full meeting minutes when the user wants extreme brevity and an explicit action list rather than a readable multi-paragraph record.
---

# Ultra-Summary

Crush any dense or messy text into the shortest digest that still carries its meaning: a two-sentence summary and, when the text contains concrete next actions, a numbered TODO list. The reader wants the payload in seconds, not a record. This is the most aggressive compression in the toolkit, sharper and shorter than meeting minutes, and it strips everything a reader does not strictly need.

## Output skeleton

Produce exactly this, and nothing else. No preamble, no headers, no closing remarks.

```
**[SUMMARY]** <at most two information-dense sentences>
**[TODO]**
(1) <imperative action>
(2) <imperative action>
...
```

Keep the tags in bold exactly as written, `**[SUMMARY]**` and `**[TODO]**`, so they render as bold labels. The summary text sits on the same line as its tag. Omit the entire `**[TODO]**` block when the text has no concrete next actions; do not pad it with invented tasks.

## The governing principle: minimum description length

Every choice here answers one question: what is the shortest message that still lets the reader reconstruct the full meaning? MDL is not "short at the cost of meaning." It is "as short as possible given that no decision, action, or load-bearing fact is lost." The operational test for any word or phrase: delete it, and ask whether a reader loses information they would need. If not, it stays deleted. Apply this test to the summary as a whole and to each TODO item on its own.

## The summary: at most two sentences

Pack the whole text into one or two sentences. One is correct when that suffices.

Drop attribution. Names of who said or proposed what are almost always texture here, not information, so remove them by default (this is the key difference from meeting minutes, which keeps them). Keep a name only when the owner of an action is itself the essential fact and would be lost otherwise.

Use an impersonal, telegraphic register ("Reviewed updates on...", "the architecture will be ablated..."). When the text has a clear now-versus-next shape, use the natural arc: the first sentence states where things stand and the single most important issue, the second states what will be done, why, and how it will be judged. When there is no plan (a pure document or thread), simply make the two sentences answer "what is this about, and what matters most about it."

Generalize illustrative lists into their category when the category carries the meaning ("backtested Sharpe, Calmar ratio" becomes "quantitative trading metrics"). But keep specifics that are load-bearing: technical terms, tools, datasets, and numbers that a reader actually needs. Compression is lossless on facts and lossy only on texture.

## The TODO: MDL-compressed action items

Extract the concrete forward actions. Prefer an explicit "next steps" or "what I will do" section when one exists; otherwise gather the real actions scattered through the text. Consolidate: several nested sub-bullets about one task collapse into a single item.

Each item is:

- One imperative line beginning with a verb (Optimize, Test, Implement, Improve).
- Numbered as `(1)`, `(2)`, `(3)`.
- Flattened. No nesting, no sub-bullets. The original outline hierarchy dissolves into flat, ordered lines.
- Compressed to MDL. If an item still reads long, compress it again: cut connective tissue, hedges, and illustrative asides, but never the core action or its load-bearing qualifiers. Keep a specific like "cosine similarity" when the tool is the action; drop it when it is mere illustration.

## What to strip, and why

Remove everything that adds length without adding information: attribution and speaker narration, restated context, hedging and back-and-forth, filler openers or closers ("Overall", "In summary"), and any outline hierarchy from the source. Do not interpret, speculate, or invent connective tissue. The output is a dense signal, not a story about the meeting.

## Worked example

**Input**

```
<aside>
✍🏻
# Minute
## Context:
Each member presented their slides and progress.
Henry presented ideas on building an agentic memory system that goes beyond standard memory and dataset-based approaches. Jason reported progress on A-mem with the WSJ dataset, including migration from llama.cpp to vLLM and faster batch processing. 致中 shared initial A-mem runs and ablation results.
Henry proposed adding news entity recognition before ingestion to enable structured analysis like company sentiment tracking over time. Jason and 致中 noted that LLM-generated keywords are often not useful and suggested using more deterministic extraction methods first, with prompt-based filtering as a later improvement. Jason further plan to ablate A-mem by replacing some mechanism.
The system can be evaluated on multiple tasks in the future, including QA (LoCoMo) for the base and financial sentiment or trading metrics.
</aside>

# Discussion Points
- Presents each own presentation
    - Henry presents some ideas regarding how we can build use such agentic system, its advantages beyond the normal memory system and the data.
    - Jason presents the WSJ dataset, and the current progress of running A-mem.
        - The migration from llamacpp to vllm, and furthermore running the processing in batches speeds up a lot
    - 致中 presents his A-mem first run and ablations.
- Some ideas:
    - News entity recognition first by Henry. This makes the news more contextually useful instead of directly throwing the dataset to the model and sequentially processing one-by-one. e.g., if some news is tied to the company, we can use the memory to analyze the sentiment towards the company over time.
    - Jason and 致中 found several LLM-generated keywords are contextually not useful. Some ideas include deterministic processing (priority) and LLM prompt engineering to filter its generated words (later). 致中 will test this.
    - Jason plans to ablate the architecture and modify what A-mem does redundantly, to speed up.
        - Some modifications such as linking can be done with simple embedding distance, cosine similarity, and other deterministic math tools
        - Expected impact: more deterministic and consistent memory linking, a better graph, and massive inference speedup.
- We can set up the system to be tested on multiple downstream tasks.
    - e.g. LoCoMo for QA, finance for sentiment analysis and even market testing, quantitative finance and trading metrics (backtested Sharpe, Calmar ratio, etc.)

# Next Step
- What I will do in the incoming days
    - Architecture optimization: link generation and evolution stage modification
        - Simple embedding distance, cosine similarity, and other deterministic math tools to speed up note linking
        - Modify the A-mem evolution stage to reduce redundant note replication
        - Test the improvement of the notes and their respective neighbors
    - LLM prompt-based keyword filtering to filter out "mundane words"
    - Memory/note embedding graph visualization improvement
```

**Output**

```
**[SUMMARY]** Reviewed updates on agentic memory systems, including a shift to vLLM for faster batch processing and the need for deterministic entity recognition over poor LLM-generated keywords. To optimize performance, the architecture will be ablated by using deterministic math tools (like cosine similarity) for note linking to drastically improve inference speed and graph consistency, with downstream evaluation planned for QA, sentiment tracking, and quantitative trading metrics.
**[TODO]**
(1) Optimize A-mem architecture for faster note linking using deterministic math tools like embedding distance and cosine similarity
(2) Test the quality improvement of the optimized notes and their respective graph neighbors.
(3) Implement LLM prompt-based keyword filtering to strip away mundane, low-value filler words.
(4) Improve the memory/note embedding graph visualization.
```

What the transformation did: dropped every name, collapsed three input regions (context aside, nested discussion, next-step list) into two summary sentences plus four flat todos, generalized the trading-metric examples into a category while keeping "cosine similarity" where it is the action, and merged each cluster of nested sub-bullets into one MDL-compressed line.

## Process

Given the text:

1. Read for the payload: the current state, the key problem, the plan, and the concrete next actions. Ignore everything else.
2. Write the summary. Fuse state and key issue, then plan and evaluation, into at most two sentences. Strip names. Generalize illustrative lists; keep load-bearing specifics.
3. Extract the TODO. Gather concrete actions (favor an explicit next-steps section), flatten all nesting, merge related sub-points, and compress each to one imperative line. Omit the block if there are no real actions.
4. Run the MDL pass: on the summary and on every todo, delete any word whose removal loses no information, then check that no decision, action, or load-bearing fact was dropped.
5. Run the clarity pass: read the digest once, cold, as an outsider would. Every sentence and every todo must be understood on that first read, with no backtracking and no guessing at referents. This is the counterweight to the MDL pass: compression that turns a line cryptic has gone too far, so add back the few words needed to make it self-evident. The target is the shortest form a reader still grasps in one pass, not the shortest form.
6. Output only the `**[SUMMARY]**` and `**[TODO]**` blocks. No preamble, no meta-commentary.
