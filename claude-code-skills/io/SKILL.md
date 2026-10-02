---
name: io
description: Read a task from an input file, do the work in full, and append the result as a timestamped Q-and-A entry to an output file (a continual log), printing only a one-line confirmation to the terminal. Defaults to PR_INPUT.md and PR_OUTPUT.md; infers custom input and output filenames from the arguments, whether positional, labeled (i:/o:), or described in natural language. User-invoked as /io.
disable-model-invocation: true
---

# io

Read the input file, do the requested work with your full normal reasoning and tools, and append the result as a timestamped entry to the output file. The output file is a continual, append-only log: existing entries are never overwritten. The terminal shows one line and nothing else.

## The contract (do not violate)

- Your only visible output for this command is a single final line: `done outputting to <OUTPUT>`. No preamble, no narration, no plan, no running commentary, no summary, no postamble. Do not think out loud in the visible response.
- The complete work product goes into the output file, never into the terminal.
- If the input file cannot be read, print exactly one line instead, then stop: `error: cannot read <INPUT>`.

## Step 1: resolve the filenames from `$ARGUMENTS`

Defaults: input `PR_INPUT.md`, output `PR_OUTPUT.md`. `$ARGUMENTS` is the text after `/io`.

- Empty `$ARGUMENTS` -> use both defaults.
- Find the filename-like tokens: those with an extension (`.md`, `.txt`, and so on) or a `/` path separator.
- If role labels are present, honor them regardless of order. Input labels: `i`, `in`, `input`, `src`, `from`, `read`. Output labels: `o`, `out`, `output`, `dst`, `to`, `write`, `result`. Labels may be written any way (`i:`, `i is`, `input =`, `output -`). Ignore filler tokens (`is`, `the`, `,`, `and`).
- If no labels, treat position as meaning: the first filename is the input, the second is the output.
- If exactly one filename and it is unlabeled, treat it as the input and keep the default output.
- Any role left unspecified keeps its default.

Resolve paths relative to the current working directory. Do not print the resolved names.

## Step 2: do the work

Read the input file and treat its contents as the task or prompt. Do it completely, applying your usual reasoning quality and whatever tools the task needs. The input defines what to produce; produce it in full, exactly as if the user had typed it directly.

## Step 3: append a timestamped entry to the output

Get the current timestamp by running `date +"%y%m%d - %H:%M:%S"`. Do not guess it.

Append one entry to the output path in this exact shape:

```
[<TIMESTAMP, YYMMDD - HH:mm:SS>]
Q: <one-line summary of the input's question or task>
A:
<the complete result>
```

Rules:

- Create the output file, and any parent directories, if they do not exist.
- Never overwrite existing content. Append only.
- If the file already has content, separate the previous entry from this one with a line containing only `---`, with three blank line above it and one blank line below it. If the file is empty or new, write the entry with no leading separator.
- Put only the entry in the file: the timestamp header, the one-line `Q:` summary, `A:`, and the full result. No meta-commentary about this command.

## Step 4: report

Print exactly one line, using the actual resolved output path, and nothing before or after it:

```
done outputting to <OUTPUT>
```

