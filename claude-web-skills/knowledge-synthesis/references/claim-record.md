# The claim record

One format for every claim that `knowledge-synthesis` writes, whether into a standalone knowledge artifact, into `proposed.md` during a research-loop outer loop, or (through research-loop's merge) into `findings.md`. The validator at `scripts/validate_findings.py` checks the fields below, so a record that breaks the format fails the file.

## Format

```markdown
### C7: <the claim in one sentence, with its conditions inside the sentence>
- Status: GROUNDED | DERIVED | CONJECTURED | UNKNOWN
- Warrant: <see the table; a chain or a long argument may continue on indented lines below>
- Certified by: <see the table>
- Conditions: <where it holds: data, scale, regime, definition in force>
- Red team: reviews/<date>-<label>.md: survived | reviews/<date>-<label>.md: wounded, conceded: <what moved into Conditions> | NOT YET
- Would change it: <the single observation that would retire or alter this record>
- Hypothesis: H2 | none
- Updated: YYYY-MM-DD
```

`Status` is the bare word; "DERIVED from data" and "DERIVED by argument" below name cases, and the field reads `DERIVED` in both. IDs are `C` plus a number, unique for the life of the project. A retired record keeps its ID in `research-log.md`; the number is never reused.

## What each status requires

| Status | Warrant | Certified by |
|---|---|---|
| GROUNDED | the quoted span or spans that entail the claim, each with its URL | the `literature/<thread>.md` note and finding number (or `deepdive/<title>/...` standalone), and the second independent source; one source is a lead, not a GROUNDED claim |
| DERIVED, from data | the effect, its interval and the decision rule's output, copied from the analysis | `experiments/<slug>/analysis.md, SUPPORTED` or `..., KILLED` |
| DERIVED, by argument | the chain, step by step, each step licensed by a GROUNDED record or a prior step | `derivation above` |
| DERIVED, by a checker | what was checked and the checker's output | `verified: <path>, <checker>`, for example `verified: src/proofs/bound.lean, Lean 4` or `verified: experiments/sort/code/test_sort.py, pytest 40 passed` |
| CONJECTURED | a prior as a percentage, then the argument that earns it: what it rests on, what would raise or lower it; after an INCONCLUSIVE run, name the `analysis.md` here | `NONE` |
| UNKNOWN | what is missing and what was searched for it | `NONE` |

Rules the validator enforces:

- Every field listed above is present and non-empty. `Conditions` may say `none stated by the source`, never nothing.
- In `findings.md`, GROUNDED and DERIVED records name their review in `Red team`; `NOT YET` fails for them. CONJECTURED and UNKNOWN records may carry `NOT YET` only in a standalone artifact that was never attacked; inside a research-loop project every merged record names its review.
- CONJECTURED records carry a percentage in `Warrant`.
- A DERIVED record names an `analysis.md` with its rule output, `derivation above`, or `verified: <path>, <checker>`; CONJECTURED and UNKNOWN name `NONE`.
- A wounded verdict names what was conceded.
- Every `literature/`, `experiments/`, `reviews/`, `probes/`, `deepdive/` or `src/` path named in `Certified by`, `Red team` or `Killed by` must exist on disk, relative to the file being checked. A record certified by a file that is not there is a fabrication with a filename.
- `Updated` is a date, `YYYY-MM-DD`.
- `## Current best answer` cites only record ids that exist in the file.

Rules the validator cannot enforce, which you hold:

- The warrant has the form the claim has. A causal claim needs a cause that was isolated, a general claim needs support across the range it claims, a theorem needs a proof and not an experiment, a present-state claim needs a dated source.
- The span entails the claim. A source that is on topic but does not say the claim does not ground it.
- Two sources are independent: different groups, and neither cites the other for this claim.
- Numbers keep their units, their uncertainty and their conditions.
- A probe result (from `probes/`) never certifies anything above CONJECTURED.

## Who may change a status

| Move | Only by |
|---|---|
| anything to GROUNDED | two independent spans in `literature/` |
| an empirical claim to DERIVED | the pre-registered decision rule, computed in `experiments/<slug>/analysis.md` |
| an argued claim to DERIVED | a chain whose every step is checkable, written in the record |
| a formal or algorithmic claim to DERIVED | a proof checker or a test suite, named in `Certified by` |
| a record narrower | a red-team wounded verdict: the concession goes into `Conditions`, the status stays |
| a record out of the store | a red-team died verdict, or evidence in a later `analysis.md`: the record is retired to the log with its reason |

The red team never rewrites a status. A record that cannot stand at its status is retired; knowledge-synthesis may re-propose the claim at a lower status, with that status's warrant, in the next `proposed.md`. A survived red team raises nothing. Confidence, fluency, a probe that "worked", an INCONCLUSIVE run and the synthesis itself raise nothing.

## The file around the records

`findings.md` has four sections, in this order, and the validator requires all four:

```markdown
# Findings: <question>

## Current best answer
<one paragraph; every claim in it names the record it rests on, as (C7)>

## Claims
<GROUNDED and DERIVED records, most load-bearing first; the only records later work may build on>

## Killed hypotheses
### H3: <statement>
- Killed by: experiments/<slug>/analysis.md, KILLED | probes/<slug>/, crux failed | reviews/<date>-outer<k>.md, retired | budget spent, crux unresolved
- Date: YYYY-MM-DD

## Open gaps
<CONJECTURED records awaiting a verifier, and UNKNOWN records>
```

`proposed.md` (template in research-loop) holds a header, the new records, the changed records, the records to retire and the fragile list. It is validated with `--proposed`, which allows `NOT YET` everywhere because the attack has not happened yet; research-loop replaces `NOT YET` with the review at the merge.

## Running the validator

```bash
python3 scripts/validate_findings.py findings.md
python3 scripts/validate_findings.py proposed.md --proposed
python3 scripts/validate_findings.py findings.md --no-paths   # outside a project folder
python3 scripts/validate_findings.py findings.md --json
```

Exit 0 when the file passes, 1 when any record fails, 2 on a usage error. The empty template fails until the first records are written; that is expected.
