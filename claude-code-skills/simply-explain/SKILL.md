---
name: simply-explain
description: Explains a complex topic so that a newcomer can follow every step while every claim stays exactly true. Builds from one concrete case to the precise statement, defines each term once, keeps conditions, quantities and uncertainty intact, and marks each approximation. Use when the user asks to explain, clarify, break down, simplify, teach, or "ELI5" something; asks "how does X work", "why does X happen", "what does this mean", or says "I don't get it"; wants an intuitive or plain-English account of a concept, paper, proof, error, design, or piece of code; or when an answer must carry a hard idea to a reader outside the field. Also use to rewrite or audit an existing explanation for clarity without loss of rigor.
license: MIT
user-invocable: true
argument-hint: "[explain · rewrite · check] <topic or text> [--for <reader>] [--depth brief|standard|deep] [--as text|diagram|page]"
metadata:
  version: "1.0.0"
---

# Simply Explain

Make a hard idea easy to hold without making it less true.

## The contract

An explanation makes two promises. When they pull apart, the second wins.

1. **Followable.** A reader at the stated level can follow every step without looking anything up.
2. **True.** An expert in the field would sign every sentence.

Simplify by leaving detail out and by choosing the order. Never simplify by saying something false. The working test is **add, never unlearn**: a reader who later studies the full theory should have to add to what you said, and should never have to take any of it back. When an omission matters, name it ("this ignores air resistance"). When you approximate, give the range where the approximation holds.

## Commands

| Command | What it does |
|---------|--------------|
| `explain` (default) | Explains a topic, a question, a file, or a piece of code. |
| `rewrite` | Re-explains a text the user supplies. Keeps every claim; changes order and wording. |
| `check` | Audits an explanation and reports findings. Changes nothing. |

All flags are optional. `--for <reader>` names the reader; the default is a sharp reader from another field. `--depth brief|standard|deep` sets the length; the default scales to the question. `--as text|diagram|page` sets the form; the default is text, with a table or figure where shape matters.

With no command word, run `explain`. For `rewrite` and `check`, read the matching flow in [references/method.md](references/method.md) first.

## Procedure

### 1. Get it right

You cannot simplify what you do not understand. Before you write, list the load-bearing claims in exact terms: the definition, the mechanism, the conditions, the key quantities, the known limits. Three to seven lines are enough. This list is the **ledger**, and the finished text is checked against it. If you cannot write the ledger, read the source, run the code, or look the topic up, and say what you could not verify. For code, read the code. Do not explain a function from its name.

### 2. Fix the reader

Take the reader from `--for`, from the conversation, or from how the question was worded. With no signal, write for a sharp reader from another field: intelligent, willing to work, missing the vocabulary. Decide what the reader already has, and build on it. Decide what the explanation needs that the reader lacks; each item becomes a term to define or a step to show. Ask the user about their level only when two plausible readers need different explanations and nothing in the conversation settles the choice.

### 3. State the point

Write the answer in one or two sentences that the reader understands now and an expert would sign. Put it first. If the true answer is "it depends", say what it depends on.

### 4. Build the route

Five stages, in this order. Skip a stage only when the reader already has it.

1. **The problem.** Say what goes wrong without this idea. A concept is easier to hold as the answer to a question.
2. **One concrete case.** Make it small, with real numbers or a real input, and work it in full. Keep this one case through the whole explanation.
3. **The mechanism.** Give the causal chain from the case to the result, one link per sentence. When you want to write `simply` or `clearly`, a link is missing. Write the link.
4. **The precise statement.** Give the general rule, its real name, and its conditions. The reader can read it now, because each part appeared in the case.
5. **The limits.** Say where the idea stops being true, what it gets confused with, and why the common wrong picture fails.

Prefer an example to an analogy. An example is an instance of the thing, so it cannot mislead about the thing. Use one analogy at most, say what maps to what, and say where the mapping breaks.

### 5. Pick the form

Prose carries reasons. Other forms carry shape: a table for items compared on the same attributes, a numbered list for steps, a diagram for structure, flow, state, or geometry, a chart for quantities. When the reader must vary an input to understand and the host can publish HTML, build an interactive page. Read [references/media.md](references/media.md) before you draw.

### 6. Write

- **One idea per sentence.** Aim under 25 words and split anything past 35. The limit is a ceiling: vary the length, and join related ideas with their connective.
- **Actors act.** The subject is the thing that does something, and the verb says what it does. Write "the cache stores the result", not "storage of the result is performed".
- **One name per thing.** After "learning rate", do not rotate to "step size" and "the rate". If the field has two names, give both once and keep one.
- **Define at first use**, in words the reader already has. Give the real term too, because the reader needs it to search and to read further.
- **Old before new.** Start a sentence from something already on the page and end it on the new thing.
- **Say the link.** Use "because", "so", "but", "unless", "which means". The links are the reasoning.
- **No loose pointers.** Each "it" and "this" has one possible referent, or the noun is repeated.
- **Numbers over adjectives.** Write "3 times faster" or "about 20 ms", with units.
- **One hedge, at its real strength.** Words like "always", "usually", and "may" are content. Keep the strength that the evidence has.
- **Words before symbols.** Introduce each symbol in words, and read each formula aloud once.
- **Verbatim spans.** Code, commands, identifiers, quotations, and official names stay as they are.

Before and after pairs for each rule are in [references/language.md](references/language.md).

### 7. Check

When you can run scripts, save the draft and run the checker from this skill's folder:

```bash
python3 scripts/explain_check.py draft.md            # add --reader technical for technical readers
```

Fix every `fix` finding and judge every `review` finding. The checker reads the surface only, so four tests remain yours:

- **Ledger.** Each claim from step 1 is in the text, with its conditions, quantities, and strength unchanged.
- **Unlearn.** A deeper course would retract no sentence. A marked approximation passes; a silent one fails.
- **Gap.** Each step follows from the text above it plus what the reader was assumed to know.
- **Stop.** Cut the text after any paragraph. The part that remains is still true and still useful.

## Output

| Depth | Shape |
|-------|-------|
| `brief` | The point and the case. Three to six sentences, no headings. |
| `standard` | The full route in about one screen. Headings only if it runs longer. |
| `deep` | The full route, the formal statement, a second case that stresses a condition, and the limits. Headings, and a table or figure where shape matters. |

Scale the depth to the question: a one-line question gets `brief`. If the topic cannot be told truthfully at the requested depth, say what the short version leaves out.

Start with the point. Do not praise the question, announce what you are about to do, or close with a recap of the body. One closing line may name a specific next layer.

Write in the language the user writes in. The rules carry over, but the checker reads English only.

Another writing skill may run after this one, for example a skill that removes machine-writing patterns. It may change wording. It may not change a ledger claim. Text written under these rules has more even sentence lengths than an essay, so a cadence score can come out low. Vary the length where a link joins two ideas, and do not pad or fragment sentences to move a score.

## Reference files

| File | When to read |
|------|--------------|
| [references/method.md](references/method.md) | For `deep` explanations, for `rewrite` and `check`, or when a stage of the route is hard to build. |
| [references/language.md](references/language.md) | When a sentence rule is unclear, or the reader has limited English. |
| [references/domains.md](references/domains.md) | Before explaining mathematics, code, systems, science, statistics, a paper, or law, finance, and medicine. |
| [references/media.md](references/media.md) | Before making a table, diagram, chart, or page. |
| [references/examples.md](references/examples.md) | To calibrate: three topics, each with a weak version, a ledger, and a strong version. |
