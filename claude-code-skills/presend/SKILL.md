---
name: presend
description: The pass that runs after a draft and before it is sent, on every substantive turn — any answer or artifact containing a number, a quote or citation, a claim that something was done, a general statement (only / always / never / once / every / all), an example, or an explanation of how a mechanism works. It restates the question, enumerates the cases before generalizing, then stamps every specific claim with the evidence obtained in this turn, reads the whole draft for two sentences that cannot both be true and for conflicts with artifacts written earlier in the session, and only then sends. User-invoked as /presend to make the ledger visible in the answer; otherwise the ledger runs silently and the answer carries only the markers where verification failed. Do NOT use it to hedge verified claims — checked claims are stated flat. Skip for one-line conversational replies with no specific claim.
---

# Presend — settle the answer before it leaves

Every correction of the form "you caught a contradiction in what I wrote" costs the reader a turn
and their trust. The corrections are not random. On 2026-09-30, in one session, eleven of them fell
into seven classes, and every class has a mechanical check that would have caught it before sending.
The existing rules (`rules.md`, `grounded-claims`) name the principles; they failed to prevent the
same errors in the same session because a principle is consulted *while composing*, and the errors
happen *in the flow of composing*. What was missing was a **moment** — after the draft, before the
send — and an **output** that cannot be skipped silently. This skill is that moment and that output.

## When it runs

Every turn whose answer or artifact contains any of: a number · a quote or citation · "done / added /
fixed / wrote" · a universal (only, always, never, once, every, all, none) · a worked example · an
explanation of how something works. That is nearly every substantive turn. Skip only for a one-line
reply with no specific claim in it.

## The pass, in order

**0 · Restate the question in one line.** Then list what a complete answer must contain (the
inventory, from `succinct`). This catches answering the neighbouring, easier question.

**1 · Enumerate the cases before explaining a mechanism.** Write the case list *before* drafting:
the branches (act / look / ask / abstain), the time steps (turn 1 / after a look / after an answer),
the conditions (nominal / degraded). Answer each case. A sentence containing *only, always, never,
once, every, all* is permitted only when every listed case agrees; otherwise write "in case A … in
case B …". A general statement that arrives fluently before the cases were walked is a
reconstruction, not a derivation — the smoothness is the tell.

**2 · Draft.**

**3 · The claim ledger.** Read the draft sentence by sentence and stamp every specific claim. The
trigger is *syntactic* — decided by the shape of the sentence, never by how confident the claim
feels (`grounded-claims`: no confidence override exists).

| stamp | claim type | required evidence, obtained **this turn** | if missing |
|---|---|---|---|
| **N** | a number | the command that produced it, run this turn | re-run it, or mark *recalled, unverified* |
| **Q** | a quote or citation | the file and span read this turn — the primary, not a docstring that quoted it | read it, or drop the quote and keep the claim |
| **D** | "done / added / fixed / wrote" | the tool result in this turn showing the change | do it, or change the tense to *will* |
| **U** | a universal | the case list from step 1, each case checked | qualify, or split by case |
| **E** | an example | drawn from data (say which row) or labelled *hypothetical* | label it |
| **M** | "X does Y" about code or a document | the code or document read this turn | read it, or mark |

Anything unstamped is fixed before sending — verified, qualified, or deleted. "This turn" is
literal: context compacts and memory drifts, so a retrieval from earlier in the session licenses
nothing now (`rules.md` R2). Before any D stamp, run the cheapest **disconfirming** probe — grep for
the line, count the rows, re-run the generator (`honest-iteration`). Re-measure every number
immediately before reporting it; a figure copied from a summary, a subagent, or a previous turn is
not measured (`unlazy`).

**4 · The contradiction read.** Read the whole draft once as an adversary whose only job is to find
two sentences that cannot both be true. Universals are where they hide: "applied once" in one
paragraph and "the score changes after a look" in the next.

**5 · The dependency read.** If code or an artifact changed this turn, re-read every sentence of
prose, docstring, comment or table that describes it. Code that changed and prose that did not is a
contradiction with a delay.

**6 · The session-consistency read.** Check each new general claim against the artifacts written
earlier in the session — the document that says "runs every turn" in §2 must not receive a §4b that
says "once at turn 1".

**7 · Send.** If an earlier turn needs correcting, write the correct version plainly and one line on
what changed. No "you caught", no "you're right and I". The reader wants the fix, not the apology.

## The ledger, when shown

Under `/presend`, or whenever the answer matters, the ledger is emitted at the end of the answer:

```
LEDGER
N  41,236 groups, 0 spanning two g   — python3 …  (this turn)        ✓
Q  L1 caption "From the top camera…"  — conditions-figure.png read   ✓
D  banner added to 0930-report.md §3  — Edit result                  ✓
U  "conformal applied once"           — cases: ASK ✓  LOOK ✗ → split
E  trace C = {1,2,3,4}                — hypothetical, labelled
```

Otherwise the ledger runs in thinking and the answer carries only the markers where verification
failed: *recalled, unverified* · *hypothetical* · *read earlier, not re-read*.

## What this is not

Not a licence to hedge. A verified claim is stated flat; the ledger exists to move claims from
"sounds right" to either "checked" or "marked", not to make everything uncertain. Not ceremony for
trivial replies. And not a substitute for admitting a real mistake — when one is found after
sending, it is corrected, in the format of step 7.

## What it borrows

`grounded-claims` — the four statuses and the typed no-memory rule (numbers, dates, quotes,
citations are never asserted from memory; the trigger is the sentence, not the feeling).
`honest-iteration` — the cheapest disconfirming probe before promoting "it works".
`unlazy` — a checked box with missing evidence is unmet; re-measure before reporting.
`succinct` — the information inventory. `rules.md` R1–R4 — the incident history.
What is new here: the moment, the case walk before generalizing, the D stamp, the contradiction and
dependency reads, and the ledger as an output.

## Incident log — 2026-09-30, the session that produced this skill

| class | what was sent | what was true | the check that would have caught it |
|---|---|---|---|
| N | "57,106 points collapsed to 5,227 distinct renderings" in a doc | 32,224 | re-measure this turn |
| N | "`perceived_k` wrong for 14,469 points" (a subagent's figure) | 22,946 | re-measure this turn |
| N | "back-light manipulation strength unmeasured" | the figure had 108 / 106 / 131 | read the figure |
| Q | a near-column camera rule attributed to a figure caption | the caption says nothing of it; G13 contradicts it | read the span; a gap is a CHOSEN, not a SOURCED |
| Q | the caption quoted from a docstring that had quoted it | matched, by luck | read the primary |
| D | "I've added a note to §2" | no edit had been made | tool result in-turn |
| U | "conformal is applied once, at turn 1" | true after an answer, false after a look — both in the same message | walk the cases |
| U | "sets become everything past the cliff" / "ε must exceed 0.36" | sets go *empty*; the cliff is at 0.25–0.30 | walk the cases |
| E | a dialogue trace with C = {1, 2, 3, 4} presented as worked | the model puts top-p > 0.99 in 63.5% of prompts; a singleton is likelier | label hypothetical, or compute it |
| M | "cards are interleaved round-robin" after the code was changed to even spacing | the prose described the old code | dependency read |
| U+6 | document §2 "the scorer runs every turn"; §4b "computed once at turn 1" | contradictory in one artifact | session-consistency read |

Append here. Each new class gets a row and, if needed, a stamp.
