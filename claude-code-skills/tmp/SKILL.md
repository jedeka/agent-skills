---
name: tmp
description: Find a tmp.md / TMP.md scratch file (any case) in the working tree and paste content into it. Called bare (/tmp) it appends the previous context — your immediately preceding response this conversation; called with a prompt (/tmp <prompt>) it does the work and appends that response instead. Only the file is written; the terminal shows one confirmation line. User-invoked as /tmp.
disable-model-invocation: true
---

# tmp

Locate a scratch file named `tmp.md` or `TMP.md` (either case) and paste content into it. The content is either your response to an inline prompt, or — if no prompt is given — the previous context (your immediately preceding response in this conversation).

## Contract (do not violate)

- Your only visible terminal output is a single final line: `done -> <FILE>`. No preamble, plan, narration, or summary — the content goes into the file, not the terminal.
- Append, never overwrite: existing entries in the file are preserved.

## Step 1 — find the file

Search the current working directory tree for a file named `tmp.md` case-insensitively:

```
find . -maxdepth 4 -iname 'tmp.md' 2>/dev/null | head -1
```

- If one or more match, use the first.
- If none match, create `TMP.md` in the current working directory.
- Do not print the path except inside the final confirmation line.

## Step 2 — decide the content

`$ARGUMENTS` is the text after `/tmp`.

- **`$ARGUMENTS` non-empty** -> treat it as a prompt. Do the work in full with your normal reasoning and tools; the content to paste is *that response*.
- **`$ARGUMENTS` empty** -> the content to paste is the **previous context**: your immediately preceding substantive response in this conversation, verbatim (the message just before this `/tmp` call). If there is no prior response, paste `(no previous context)`.

## Step 3 — paste it

Get a timestamp with `date +"%y%m%d - %H:%M:%S"` (run it; do not guess). Append one block to the file:

```
=== [<timestamp>] <the prompt, or "previous context"> ===

<content>

```

Append; never overwrite. Then print exactly one line and nothing else: `done -> <FILE>`.
