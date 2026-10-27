# Language rules

Sentence-level rules for step 6. They descend from ASD-STE100 (Simplified Technical English), a controlled language written for aircraft maintenance manuals. The rules here keep what serves explanation and leave the rest.

## Contents

- [The rules, with examples](#the-rules-with-examples)
- [Words of strength](#words-of-strength)
- [What came from STE, and what was left](#what-came-from-ste-and-what-was-left)
- [Readers with limited English](#readers-with-limited-english)

## The rules, with examples

### One idea per sentence

Aim under 25 words. Split a sentence that passes 35. At least four sentences in five should meet the 25-word aim.

> Before: The optimizer, which uses the gradient that backpropagation computed in the previous step, updates each weight in proportion to the learning rate, a number that is set before training begins and controls the step size.
>
> After: Backpropagation computes the gradient. The optimizer then moves each weight against its gradient. The learning rate, a number fixed before training begins, sets the size of that move.

The limit is a ceiling. A run of short sentences of equal length reads as a drumbeat and hides how the ideas connect.

> Before: The pump moves fuel. The fuel goes to the engine. The engine burns the fuel. A unit watches the pressure.
>
> After: The pump moves fuel to the engine, which burns it. A control unit watches the fuel pressure and slows the pump when the pressure rises.

### Actors act

Make the subject the thing that does something. Use a verb for the action; an action packed into a noun hides who acts.

> Before: Validation of the input is performed by the server prior to the execution of the query.
>
> After: The server validates the input before it runs the query.

Passive voice is correct when the actor is unknown or does not matter: "the bridge was built in 1932".

### One name per thing

A reader assumes that a new word means a new thing. Choose one name and repeat it.

> Before: The learning rate controls each update. A large step size overshoots the minimum, so tune the rate with care.
>
> After: The learning rate controls the size of each update. A large learning rate overshoots the minimum, so set the learning rate with care.

When the field has two names for one thing, give both once ("the learning rate, also called the step size") and keep the first.

### Define at first use

Define a term in the sentence that first uses it, or in the next one. A definition names the category and then the property that sets the thing apart: "A mutex is a lock that one thread at a time can hold." Follow it with an instance when the term is abstract.

> Before: Use a mutex to avoid the race.
>
> After: Two threads that write the same variable can interleave, and one update is lost. This bug is called a race condition. A mutex, a lock that one thread at a time can hold, prevents the race condition.

### Old before new

Start each sentence from something the reader already has. Put the new item at the end, where the stress falls.

> Before: A hash function is needed to find the slot. Keys are the input to the hash function.
>
> After: Each key goes through a hash function. The hash function returns a slot number, and the slot holds the value.

### Say the link

Two facts side by side leave the reader to guess the relation. State the relation.

> Before: The table is full. Lookups slow down.
>
> After: As the table fills, more keys share each slot, so each lookup compares more keys.

### No loose pointers

> Before: The server sends the token to the client, and it stores it.
>
> After: The server sends the token to the client, and the client stores the token.

A sentence that opens with "This" needs a noun after it: "This delay", "This rule".

### Numbers over adjectives

> Before: The index makes the query much faster.
>
> After: With the index, the query reads 20 rows instead of 2 million.

`Exponentially` has an exact meaning: the quantity is multiplied by a fixed factor at each step. Do not use it to mean "a lot".

### One hedge, at its real strength

> Before: This could potentially lead to some slowdown in certain cases.
>
> After: This slows writes when the log is on a spinning disk.

If the evidence supports only a weak claim, make the weak claim once, and say what the uncertainty is about.

### Words before symbols

> Before: ∇L(w) gives the update direction.
>
> After: The gradient of the loss, written ∇L(w), lists how much the loss changes when each weight changes by a small amount.

### Verbatim spans

Code, commands, identifiers, file paths, error messages, quotations, and official names stay exactly as they are. Format them as code or as quotations.

### Smaller rules

- One topic per paragraph, and at most about 150 words.
- Keep articles and `that`. "Make sure that the valve is open" reads faster than "ensure valve open".
- At most three nouns in a row. Write "the timeout of the connection pool", not "connection pool timeout value setting".
- Use a vertical list for parallel items and a numbered list for steps in order.
- State a rule in the positive form when one exists: "keep the lock for under 1 ms", not "do not hold the lock too long".

## Words of strength

Choose the word that matches the evidence, and use it once.

| Word | Claim it makes |
|------|----------------|
| always, never, every | No exception exists. True by definition or by proof. |
| in every tested case | No exception was found. None is ruled out. |
| usually, typically | Most cases. Give the share if it is known. |
| can | It is possible and has been observed. |
| may, might | It is not known whether it happens. |
| is thought to | The leading hypothesis, not yet confirmed. |
| is unknown | Nobody knows. Say so plainly. |

## What came from STE, and what was left

| STE rule | Here | Reason |
|----------|------|--------|
| Descriptive sentences of at most 25 words. | Aim of 25 for four sentences in five, ceiling of 35. | A claim with its conditions can need 30 words. A split can separate the claim from its conditions. |
| One topic per sentence. Six sentences per paragraph. | One topic per sentence. One topic per paragraph, at most about 150 words. | A count of sentences punishes short sentences. The word limit is the same budget: six sentences of 25 words. |
| Active voice. | Kept as the default. | |
| One name for one item. | Kept. It is the rule that pays most. | |
| Keep articles and `that`. | Kept. | |
| Vertical lists for complex text. | Kept. | |
| Noun clusters of at most three words. | Kept. | |
| Imperative for procedures; fixed form for warnings. | Kept for procedures. | |
| A dictionary of about 900 approved words. | Dropped. | It was built for aircraft maintenance. In other fields it forces a paraphrase of standard terms, and precision is lost. |
| Only `can`, `must`, `will`. No `may`, `might`, `should`. | Dropped. | In an explanation, these words carry the strength of a claim. "May cause" and "causes" are different claims. |
| No `-ing` forms. No perfect tenses. | Dropped. | For a fluent reader, the cost in natural phrasing exceeds the gain. |
| No contractions. No semicolons. | Optional. | A matter of style. |

## Readers with limited English

For a reader who is still learning English, move closer to full STE. Use only the simple present, simple past, and future tenses. Avoid `-ing` verb forms, idioms, and two-word verbs such as "carry out" and "set up". Prefer the common word when two words are equally exact.
