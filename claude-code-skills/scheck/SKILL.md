---
name: scheck
description: Schedule a Sonnet subagent to check the status of the currently running job or workflow at a given time, optionally resuming halted work and running a follow-up action afterwards. Accepts relative offsets ("45 minutes after", "in 2h"), absolute times ("mon 2026/08/19 8.13 pm"), and an optional instruction to execute once the check completes. With no argument it schedules the check for 1 minute after the usage limit resets. User-invoked as /scheck.
disable-model-invocation: true
---

# /scheck - Scheduled Status Check

Schedule a one-shot Sonnet subagent that inspects whatever job or workflow this session currently has running and reports its status.

## 1. Identify the target

Before scheduling, determine what is being watched, from this session's context:

- Background Bash shells (`run_in_background`), their command lines and shell IDs.
- Running subagents / workflows (`ListAgents`, workflow task IDs).
- Log files, output paths, PIDs, run directories, or checkpoints those jobs write to.
- The success criterion: what "done" and what "failed" look like for this specific job.

Record these concretely. The scheduled prompt must be self-contained, because it fires into a fresh turn with no guarantee the details are still fresh in view. If nothing is running, say so and ask what to watch instead of scheduling a blind check.

## 2. Parse the time argument

Compute the fire time in the user's local timezone. Get the current wall-clock time with `date` before doing any arithmetic; never guess it.

| Argument form | Example | Meaning |
|---|---|---|
| relative offset | `45 minutes after`, `in 2h`, `90m` | now + offset |
| absolute datetime | `mon 2026/08/19 8.13 pm` | that exact local datetime (`8.13 pm` = 20:13) |
| time only | `8.13 pm` | next occurrence of that time |
| *(empty)* | `/scheck` | **default:** 1 minute after the usage window resets (step 3) |
| time + action | `/scheck 2h, then rerun the eval` | schedule at the time, run the action after the check (step 5) |

Ambiguous or unparseable input: state your interpretation in one line and proceed; only ask if two readings differ by more than an hour.

Use `date -d ...` to resolve the target into minute, hour, day-of-month, and month.

## 3. Default mode (no argument): 1 minute after the usage window resets

Bare `/scheck` means: **check at the start of the next session window**, i.e. one minute after the current usage limit resets. Resolve the reset time in this order:

1. **`/usage` output already in context.** If this session has any `/usage` output or a rate-limit message carrying a reset time or a "N minutes/hours until reset" figure, parse it and use it. Anchor relative figures with `date` at the moment you read them, not later.
2. **Ask the user to run it.** You cannot invoke `/usage` yourself — it is a built-in CLI command, not a skill, and the reset time is not stored anywhere readable on disk. Ask them to type `/usage` (or `! date` alongside it) and paste the session/reset line. One short request, then continue.
3. **Fall back.** If they decline or nothing is available, schedule for 1 minute after the session's current work reaches a resting point, and say that is what you did and why.

Arithmetic: reset offset + 1 minute. "40 minutes until reset" read at 14:22 → fire at 15:03 → `cron: "3 15 <dom> <month> *"`. An absolute reset time gets the same treatment: reset + 1 min, exact, no off-minute nudging.

If the reset lands beyond this session's likely lifetime, say so plainly - the cron job dies with the session (step 7).

## 4. Schedule it

Call `CronCreate` with `recurring: false` and all five fields pinned to the computed time:

```
cron: "<min> <hour> <dom> <month> *"
recurring: false
```

Off-minute rule: when the user's time is approximate, avoid minute `0` and `30`. Honor exact times the user names (including the `+1 min` default) verbatim.

The `prompt` must instruct the main session to deploy a Sonnet subagent, and must carry the full target description from step 1:

```
Deploy a Sonnet subagent (Agent tool, model: "sonnet", subagent_type: "general-purpose")
to check the status of: <job description>.

The subagent should:
- Inspect <log paths / shell IDs / PIDs / output dirs>.
- Determine state: RUNNING | COMPLETED | FAILED | STALLED | UNKNOWN.
- For RUNNING: report progress signal and latest activity timestamp.
- For FAILED: report the error and the last ~30 relevant log lines.
- For COMPLETED: confirm against the success criterion: <criterion>.
- Not modify, restart, or kill anything. Read-only.
- If not RUNNING, identify why it stopped (usage limit / killed / crash / stalled)
  and the last completed checkpoint or item, so work can be resumed rather than redone.
- Return a compact report: state, evidence, elapsed time, halt cause, resume point,
  recommended next step.

<action, if the user specified one, with its trigger condition>

Then follow step 6 of the /scheck skill: if the work is halted for a resumable reason,
resume it from the reported checkpoint. Relay the outcome to the user in a few lines.
```

Read-only is a hard constraint for the *status check itself*: it observes, it never intervenes. Resumption (step 6) is the one sanctioned exception, and only under the conditions listed there.

## 5. Act after checking

`/scheck` takes an optional instruction after the time: everything that is not a time expression is the action to run once the check completes.

```
/scheck 45 minutes after                          -> check only
/scheck 45 minutes after, then run the eval suite -> check, then run it
/scheck deploy to staging if the tests passed     -> default timing, conditional action
```

Split the argument into `<time>` and `<action>`. If the split is unclear, state your reading in one line and proceed.

Bake the action into the scheduled prompt, after the report step, with its trigger condition made explicit:

- **Unconditional** ("then run X"): run it once the check returns, whatever the state, unless the check reveals the action is now meaningless.
- **Conditional** ("if it passed", "if it failed", "once it finishes"): evaluate the condition against the reported state and say plainly when you skip and why.
- **Default when unstated:** run the action only if the job reached COMPLETED and met its success criterion. A job that failed rarely wants its follow-up run on top of the wreckage.

The action runs in the main session with full tools, not inside the read-only checker subagent - the subagent observes, the session acts. Ordering is fixed: check, report, resume if halted (step 6), then the action. Never run the action before the check it was conditioned on.

Confirmation still applies. If the action is destructive or outward-facing (deploy, push, send, delete), the `/scheck` invocation counts as authorization for that specific named action and nothing beyond it; anything wider gets confirmed at fire time.

## 6. Resume halted work

A check that finds the job dead and merely says so is half a skill. Whenever the subagent reports a state other than COMPLETED, the main session must decide whether to restart the work, and by default it should.

Classify why it stopped:

| Cause | Evidence | Action |
|---|---|---|
| Usage / rate limit | limit message in transcript or log, agent died mid-turn with no error of its own | Wait for the reset, then resume from the last checkpoint |
| Killed (OOM, SIGKILL, terminal closed) | non-zero or 137/143 exit, truncated log, missing PID | Resume from the last checkpoint |
| Crash | traceback or error in the log | Do **not** blindly restart. Report the error; restart only if it is transient (network, disk, flaky dep) |
| Stalled | process alive, no log growth past its normal cadence | Report; restart only if the user has authorized it or the job is known-idempotent |
| Still running | log advancing | Do nothing; optionally reschedule another `/scheck` |

Rules for any resumption:

- **Resume, do not restart from zero.** Find the last checkpoint, output file, or completed item and continue from there. State explicitly which item or step you are resuming at.
- **Never duplicate work already committed.** Re-read outputs before writing; skip finished units.
- **Do not resume destructive or outward-facing work** (deploys, sends, deletes, pushes) without fresh confirmation, no matter what the original job did.
- **Cap the retries.** Two automatic resumptions of the same unit; after that, stop and report rather than looping.
- **Say what happened.** Report the halt cause, where you resumed from, and what was skipped.

For a usage-limit halt specifically, schedule the resumption as another one-shot `CronCreate` at the reset time plus a couple of minutes, rather than blocking. If the reset time is unknown, see the note in step 7.

## 7. Session end and usage reset (what is and is not detectable)

There is no tool that reports the session's remaining lifetime or the usage-limit reset timestamp, and it is not written anywhere under `~/.claude`. Do not fabricate one. Best-effort signals, in order of reliability:

1. **The limit message itself.** When a rate limit is hit, the reset time appears in the error text. If it is in this session's context or in a captured log, parse it and use it directly.
2. **`/usage`.** The user can run it; you cannot. If the reset time matters and none of the above is available, ask them to run `/usage` and paste the reset time, or type `! date` to anchor the clock.
3. **Otherwise, back off.** Reschedule the check in a conservative window (start at ~30 minutes, then widen) rather than polling tightly. Repeated early wakeups spend the very budget being waited on.

Session end is likewise not observable in advance, and cron jobs die with the session. When the scheduled fire time is far out, say plainly that the check will not survive a session exit, and suggest an external scheduler (system `cron`, `at`, `systemd-run --on-calendar`) if the work genuinely must outlive this session.

## 8. Confirm

Report back in one or two lines: the resolved fire time (local, with weekday), what is being checked, and the returned job ID for `CronDelete`.

Note that cron jobs are session-only. If the session exits before the fire time, the check is lost; tell the user when the gap is long enough to matter.
