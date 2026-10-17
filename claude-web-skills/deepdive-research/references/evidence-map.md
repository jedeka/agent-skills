# Evidence map template

The map is the skill's output. It reports what the evidence shows, thread by thread, and what the search did not find. It draws no conclusion beyond the evidence, writes no narrative, and leaves synthesis to knowledge-synthesis. Write it to `literature/evidence-map.md` beside the thread notes.

```markdown
# Evidence map: <question in one sentence>

Searched: <date>
Mode: fan-out (<n> researchers + adversary) | single context
Assumptions taken: <any ambiguity resolved without asking, or none>
Notes: <list of thread note files>

## Threads

### <thread>

Status: SETTLED | ABSENT | OPEN
Finding: <one or two lines, as the evidence states it>
Established by: <source 1> and <source 2>, independent | single source, lead only
Numbers: <value, units, conditions, or none>
Open: <what remains unresolved on this thread, or none>

### <thread> ...

## Conflicts

- <claim A> (<sources>) versus <claim B> (<sources>). Weight of evidence: <which side and why, or unresolved>.

## Adversary

- Most likely way the emerging picture is wrong: <one line>
- Surviving objections: <each with its evidence>
- Attacks that found nothing: <list>

## Sought and not found

- <what was expected to exist if the answer held>: queries <list>, result <nothing | partial>

## Independence

- <origin> is echoed by <sources>; counted once.

## Leads not pursued

- <lead>, <why it matters>, <which thread it would open>
```

Rules:

- Every finding in the map must trace to a validated note. Do not add findings from memory.
- Established requires two independent sources in the notes. Otherwise write "lead only".
- Keep the map short. Its value is in the status fields, the conflicts and the gaps; the detail is in the notes.
- Date everything that could change.
