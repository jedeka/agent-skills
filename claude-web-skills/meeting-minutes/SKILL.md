---
name: meeting-minutes
description: Convert raw meeting notes, discussion points, or rough transcripts into concise, information-first meeting minutes that capture only decisions, findings, proposals, progress updates, and action items, compressed to at most three paragraphs. Use this whenever the user wants to write up or summarize a meeting, turn notes from a standup, sync, planning, or research meeting into clean minutes, or distill messy bullet points into a short durable record. Trigger even when the user does not say the word "minutes" — for example they paste rough meeting bullets and say "write this up," "clean this up," or "summarize what we discussed." Do not trigger for non-meeting summarization such as condensing an article, paper, or general document.
---

# Meeting Minutes Writer

Convert raw meeting notes, discussion points, or rough transcripts into concise meeting minutes written in an information-first, Occam's-razor style. The minutes are a durable record that someone reads weeks later to recover what was decided, found, proposed, and what happens next. They are not a replay of the conversation.

## The core principle

Keep every sentence that carries a decision, finding, proposal, progress update, or action item. Cut everything else. The test for any phrase: if removing it loses no factual information a reader would need later, remove it.

This is why the output is dramatically shorter than the input. Most raw notes are mostly texture (who said what, hedging, back-and-forth, restated context), and texture is not information.

Stay faithful. Preserve facts, names (including non-Latin names exactly as written), numbers, and technical terms. Do not interpret, speculate, editorialize, or invent connective tissue that was not in the notes.

## The shape: at most three paragraphs

The hard target is three paragraphs, sometimes fewer. The cap is not arbitrary. It forces the compression that is the entire point: a reader should absorb the whole meeting in a few sentences, not wade through an outline. Treat three as a ceiling, not a quota. A thin meeting may need only one or two paragraphs, and that is correct.

Map the meeting onto these three paragraphs:

1. **What was done and shown** — progress updates and presentations.
2. **What was discussed and proposed** — the main findings, observations, debates, and the changes or future work someone proposed. This is usually the densest paragraph.
3. **What happens next** — planned evaluations, action items, decisions, and next steps.

Drop a paragraph entirely if the meeting had no content for it. Merge ruthlessly within each paragraph: several related bullets become a few sentences, and a presentation plus its sub-results becomes one sentence or two. Do not print the paragraph labels themselves unless the user asks for headers; let the order carry the structure.

## Writing style

Write in complete, short, declarative sentences. Use plain professional language. Prefer one sentence per key point, then fold closely related points together so the paragraph reads as a record rather than an outline.

Flatten the hierarchy of the raw notes. Notes use nested bullets to capture stream-of-thought; minutes dissolve that nesting into prose. The structure lives in sentences and paragraph order, never in indentation.

Attribute findings and proposals to a person when the notes do, since who owns a decision or an action matters later. Attribute in passing ("Jason reported...", "Henry proposed...") rather than narrating speaker by speaker.

## What to avoid, and why

These add length without adding information:

- Nested bullet points. They reintroduce the outline you are supposed to be removing.
- Transcript-style or speaker-by-speaker narration. Minutes record what was concluded, not the dialogue that produced it.
- Restated context and repetition. State each fact once.
- Filler openers and closers such as "Overall," "In conclusion," or "In summary." They signal an essay rather than a record and carry no information.
- Speculation or interpretation beyond what the notes state.

## Worked example

**Input**

- Henry presents ideas on agentic memory systems.
- Jason presents WSJ dataset progress.
  - Migrated from llama.cpp to vLLM.
  - Batch processing is much faster.
- 致中 presents first A-mem run and ablations.
- Henry proposes news entity recognition before processing.
- Jason and 致中 find many LLM-generated keywords are not useful.
  - Consider deterministic extraction.
  - Consider prompt improvements later.
- Jason proposes replacing some linking steps with embedding similarity.
- Evaluate on QA and finance tasks.

**Output**

Henry presented ideas on building an agentic memory system that extends beyond standard memory-based approaches. Jason reported progress on A-mem with the WSJ dataset, including migration from llama.cpp to vLLM and faster processing through batching. 致中 shared the first A-mem run and ablation results.

Henry proposed adding news entity recognition before ingestion to enable structured analysis of entities and sentiment over time. Jason and 致中 observed that many LLM-generated keywords are not contextually useful and suggested deterministic extraction, with prompt-based filtering as a later improvement. Jason also proposed replacing some linking steps with embedding-based similarity to improve efficiency and consistency.

The system will be evaluated on downstream tasks, including QA and financial sentiment analysis.

Notice what the transformation does: it collapses an eight-bullet, two-level outline into exactly three paragraphs, merges each presentation with its sub-points, attributes in passing, drops nothing factual, and ends on the planned evaluation. The output is far shorter than the input while losing no decision, finding, proposal, or action. Each paragraph corresponds to one of the three slots: progress, then discussion and proposals, then next steps.

## Process

Given meeting notes:

1. Identify the load-bearing content (decisions, findings, proposals, progress, actions). Discard the rest.
2. Sort each surviving point into one of the three slots: done/shown, discussed/proposed, or next steps.
3. Within each slot, merge related points into a few clean sentences, removing all original bullet hierarchy.
4. Write the three paragraphs in order, dropping any slot that has no content. Stay at or under three.
5. Check that every important fact from the input survived and that the result is much shorter than the input.
6. Output only the minutes. No preamble, no headers (unless asked), no meta-commentary, no "here are your minutes."
