---
name: jargon
description: Expand every unexplained piece of jargon. User-invoked as /jargon — with no argument it takes the previous assistant message; with pasted text, a file path, or "last N" it takes that. It finds every project-internal identifier, acronym, method name, metric, field name or shorthand that the text uses without a gloss in the same message, and returns a glossary table — one row per term, one plain clause each, with the file and line where the meaning is defined when the term is project-specific. Also invoke it yourself before sending any reply that would contain three or more unglossed identifiers (G-numbers, L-levels, field names, method names). Never guess a meaning: a term whose definition cannot be found at source is listed as unresolved with where you looked. This is the on-demand half of rules.md R3 (expand jargon on first use, every turn); R3 remains the standing rule.
---

# Jargon — say what the words mean

A reader who has to ask "what is G13?" has stopped reading. Every project-internal term in a message
is either glossed in that message or it is a defect. This skill finds the defects and fixes them.

## What counts as jargon

Anything a person joining at this message could not follow without asking:

| kind | examples |
|---|---|
| numbered decisions and gates | G13, V10, LC7, E3-H3, B7 |
| levels and codes | L0 … L4, L4-fd, g = 2, k3, P16 |
| method and theory names | Mondrian, Gibbs conditional calibration, split CP, CRC, KnowNo, RSA, DiT, ACT, DDIM |
| metrics and symbols | q̂, ε, α, coverage, set size, singleton rate, AUROC, NLL, Wilson interval, McNemar |
| field and file names used as words | `cal_eligible`, `perceived_k`, `c_star`, `scripted_answer`, `prompt_group`, `points.jsonl` |
| rig and speech terms | VAD, ASR, TTS, barge-in, half-duplex, logprob, prefill, tunnel, :8123 |
| project shorthand | the escape class, the lighting hole, the draw protocol, the fit pool, the holdout, the smoke bank |

A term counts as glossed only if the gloss is in the *same message* — a definition three turns ago
does not count, and neither does one in a file the reader has not opened.

## Where meanings live (look here before writing one)

| for | source |
|---|---|
| Eduardo's G-numbers, V-items, E-items | `docs/project-notion/guide-or-act_recordings_and_plan_2026-09-29/recording_script/docs/DECISIONS.md` (the table row for the id); plain-sentence decoder in `INTUITIVE-EXPLANATION.md` §0 |
| L0–L4, g, the pools, lighting levels | `…/recording_script/docs/CONDITIONS.md`; `docs/project-notion/conditions-figure.png` |
| card and trial fields | `…/recording_script/docs/DATA_SCHEMA.md`; `…/tools/README.md` |
| local-cp fields, arms, gates | `local-cp/README.md`, `local-cp/cp.py` docstrings, `local-cp/GATES.md` |
| conformal terms (q̂, ε, coverage, Mondrian, Gibbs, CRC) | `docs/ed.md`, `docs/project-notion/task1.md`, `docs/0909-understanding_uncertainty.md` |
| rig and speech terms | `CLAUDE.md` "Rig" and "Measured" sections; `perceptionplay/BUILD.md` |
| our own rule ids (R1–R6) | `rules.md` |

Read the defining line before writing the gloss. If it is not there, the row says *unresolved — looked
in X, Y* (rules.md R1: a gap is named, not filled).

## Output

One table, terms in order of first appearance, nothing else unless asked:

| term | plain meaning | defined in |
|---|---|---|
| G14 | the routing rule: expected set size k comes from the sentence; LOOK when the set exceeds k and a camera is blocked, ASK when it exceeds 1 but not k, at most one LOOK | DECISIONS.md line 170 |
| `perceived_k` | how many spots still match the description given what the working cameras resolve | local-cp/adapt.py |
| Gibbs | conditional calibration by Gibbs, Cherian and Candès: one threshold *function* fitted over overlapping group indicators using all the data, instead of one threshold per disjoint group | docs/ed.md §3; arXiv:2305.12616 |
| the lighting hole | the case G14 does not cover: a set larger than the sentence asked for, caused by dim or back-light rather than by a blocked camera | INTUITIVE-EXPLANATION.md, Cases 9–10 |

One clause per row. The test: could someone joining at this message follow it now without asking?

## When you invoke it yourself

Before sending a reply, count the unglossed identifiers in the draft. Three or more → either gloss
them inline (preferred, one clause each at first use) or append this table. Zero exceptions for
G-numbers: they are never readable bare.
