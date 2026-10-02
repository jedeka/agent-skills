---
name: organize-debug
description: Compile a debugging or troubleshooting session into one clean, canonical, replayable debug-log document (a DEBUG_LOG.md). Use this whenever the user says /organize-debug, asks to "organize / summarize / write up the fixes", wants a record of what was changed during debugging, asks for a DEBUG_LOG.md, or has finished a multi-bug session and needs the crucial solutions distilled into a single markdown file. Traces the entire conversation, separates the fixes that are genuinely load-bearing in the final working state from failed attempts, superseded patches, and stale reruns, and emits each as a flattened, render-safe iteration block, plus Verify, success-signature, and Cleanup sections. This is the compilation counterpart to /debug. For organizing any NON-debugging content (chats, research, notes, web pages, files) into a document, use /organize instead.
---

# /organize-debug - Compile a Debugging Session into a Canonical Debug Log

Turn a long, messy debugging chat - full of dead ends, reruns, and patches that were later superseded - into ONE authoritative `DEBUG_LOG.md` that a teammate could replay from a clean checkout to reach the exact working state. Be surgical and concise. No em-dashes.

This is the inverse of `/debug`: `/debug` produces many iteration blocks during the session; `/organize-debug` distills them into the minimal, ordered, load-bearing set. (For organizing non-debugging material into a document, use `/organize`.)

## The core judgment: what is load-bearing

Include a fix only if the final working state *depends on it*. The test for each candidate:

> If I revert this one change on a clean checkout, does the green state break?

- **Keep** the minimal set that reproduces the working state.
- **Discard** failed attempts, superseded patches, debugging scaffolding that was removed, and stale reruns. They are noise; they make the log un-replayable.
- **Demote to a conditional note** any fix that a *later* change neutralized. Example: if a code path was disabled, a patch that only mattered inside that path is no longer load-bearing; record it as "only needed if you re-enable X", not as a live step.

When two fixes were really attempts at the same root cause, keep only the one that survived. When the final fix supersedes three earlier ones, document the final fix and drop the three.

## Tracing procedure

1. Read the whole conversation. If a transcript tool or the full history is available, scan it incrementally rather than trusting a summary - the load-bearing/superseded distinction lives in the details.
2. Build the list of distinct root causes (not distinct messages). For each, find the *final* fix that is in force in the working state.
3. Run the revert test above on each candidate. Drop or demote accordingly.
4. Order them. Prefer the order in which a fresh checkout would need to apply them (dependencies first), or the order encountered if there is no dependency.
5. Classify each with a tag: `[script]`, `[source]`, `[config]`, `[decision]`, `[env]`.

## Document structure

Produce a single `.md` with these sections, in order:

1. **Title + context** - one short paragraph: what system, what hardware/setup, what the log covers, and (if there is one) the meta-pattern that recurs across the bugs.
2. **Conventions** - where to run commands from, the greppable marker used on source edits, and the fact that patches are idempotent and assert-guarded.
3. **One section per fix**, headed `## N - <one-line summary>  [tag]`, each containing:
   - `**Problem.**` the mechanism (the *why*), not just the symptom.
   - numbered `**Step k -**` entries, each with its command. This is the `/debug` block, flattened (see formatting).
   - a short `**Note.**` for tradeoffs, fallbacks, or "only if you re-enable X" conditions.
4. **Verify all fixes are present** - one command block: a grep for every marker, plus a parse/lint/import check that the edited files are still valid.
5. **What "green" looks like** - the success signature (the lines that prove it worked), and explicitly list benign warnings to ignore so they are not re-debugged later.
6. **Cleanup stale artifacts** - prune run-by-run accumulation (old logs, backups, generated files). Every destructive command is preceded by an `ls`/`du` inspect-first command, and any irreversible action carries a one-line caveat.
7. **Quick-reference table** (optional) - the final settings and a one-line reason for each, so the working configuration is scannable.

## Formatting rules (render-safe - this is the whole point)

These exist because nested fenced code blocks de-indent or break in many markdown viewers. The compiled document must render identically everywhere.

- **Every fenced code block sits at column 0**, never indented inside a list item, with a blank line directly above it.
- **Label each step in bold immediately above its block** (`**Step 1 - <desc>:**`) so it still reads as belonging to that step without relying on list nesting.
- **No nested fences. No em-dashes.** Use bold labels and column-0 blocks instead of deep bullet nesting.
- Keep prose tight: Problem states the mechanism; steps carry the commands; notes carry tradeoffs.
- Preserve patches verbatim (idempotent, assert-guarded). Do not silently "clean up" a command in a way that changes its behavior.

## Workflow

1. Trace the conversation and assemble the load-bearing set (apply the revert test; drop/demote the rest).
2. Draft the document with the structure and formatting rules above.
3. Write it to a file (default name `DEBUG_LOG.md`) in the outputs directory.
4. If a `present_files` tool is available, present the file. Give a one-paragraph summary of what it contains and how to replay it; do not restate the whole document in chat.

The finished log is the single source of truth: applying its steps to a clean checkout reproduces the working state, its Verify block confirms the edits are in place, and its Cleanup block removes the debris the session left behind.
