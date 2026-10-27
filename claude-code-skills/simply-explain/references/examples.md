# Worked examples

Three topics that are often explained wrongly. Each has a weak version, the ledger, a strong version, and a note on what the strong version did. Every number below was computed, not recalled.

The weak versions of the p-value and the eigenvector pass `explain_check.py` with no findings. Their defect is a false claim, and a false claim is invisible to a surface check. Only the ledger test and the unlearn test catch it.

## Contents

- [The p-value](#the-p-value)
- [The CAP theorem](#the-cap-theorem)
- [Eigenvectors](#eigenvectors)

## The p-value

Field: statistics. Reader: the default outsider. Depth: `standard`.

### Weak version

> The p-value is the probability that your result happened by chance. A p-value of 0.03 means there is a 97% chance that the effect is real.

Both sentences fail the unlearn test. A p-value is computed under the assumption that chance alone is at work, so it cannot be the probability of that assumption. The second sentence reverses a conditional: it gives the probability of a hypothesis given the data, and a p-value does not measure that.

### Ledger

- The p-value is computed under the null hypothesis (no effect) and the other assumptions of the statistical model.
- It is the probability, under those assumptions, of data at least as extreme as the data observed.
- It is not the probability that the null hypothesis is true.
- A cutoff, often 0.05, is fixed before the data are seen. A result below the cutoff is called statistically significant. When the null hypothesis is true, this rule gives a false alarm at most that often.
- The p-value does not measure the size of an effect. With enough data, a small effect gives a small p-value.
- "As extreme" depends on the test: one direction or both.

### Strong version

> A p-value answers one narrow question: if nothing were going on, how often would chance alone produce data at least this extreme?
>
> Suppose you suspect that a coin favors heads. You flip it 100 times and get 60 heads. Start from the dull assumption that the coin is fair, which statisticians call the null hypothesis, and ask how often a fair coin would give a result this lopsided. The answer is about 2.8% of the time. That 2.8% is the p-value: p = 0.028.
>
> So a small p-value means that the data would be rare if the null hypothesis were true. By convention, researchers fix a cutoff before they see the data, often 0.05, and call a result "statistically significant" when p falls below the cutoff. Under this rule, a fair coin is wrongly flagged in at most 5% of experiments.
>
> The number has three limits. First, it is not the probability that the coin is fair: the calculation assumed a fair coin, so it cannot report on that assumption. Second, it does not measure the size of the bias. In 10,000 flips, 5,100 heads gives p = 0.023, although heads came up only 51% of the time. Third, it depends on what counts as extreme. If 40 or fewer heads would have surprised you as much, then both directions count, p doubles to 0.057, and the result no longer passes the cutoff.

### What it did

The point comes first and is exact. One case, the coin, runs through every paragraph, including the limits. The mechanism is one step: assume a fair coin, then count how often a fair coin does this. The real terms, "null hypothesis" and "statistically significant", arrive after the reader has seen what they name. Each limit is a number from the same case.

## The CAP theorem

Field: distributed systems. Reader: `--for "a backend developer who has not run replicated databases"`. Depth: `standard`.

### Weak version

> The CAP theorem says that a distributed system can have only two of three properties: consistency, availability, and partition tolerance. So you pick two.

"Pick two" presents three symmetric options, and one of them is "consistent and available, with no partition tolerance". Machines that talk over a network cannot choose to have no network failures. The choice that remains is narrower, and it arises only during a failure.

### Ledger

- The setting is data copied onto several machines that exchange messages over a network.
- A partition is a network failure in which some machines cannot reach others.
- Consistency here means linearizability: every read returns the most recent completed write, as if one copy existed.
- Availability means that every request to a working machine gets a response that is not an error.
- During a partition, no system can guarantee both consistency and availability. Eric Brewer conjectured this in 2000; Seth Gilbert and Nancy Lynch proved it in 2002.
- With no partition, a system can provide both.

### Strong version

> The CAP theorem, named for consistency, availability, and partition tolerance, says what a replicated database must give up when its network fails. During the failure it can stay consistent, which means correct, or stay available, which means responsive. It cannot guarantee both.
>
> Take a seat-booking service that keeps two copies of its data, one in Paris and one in Tokyo, and keeps them equal by sending every change across the link between the two cities. Now that link fails. This failure is called a network partition: both machines still run, and neither can reach the other.
>
> A customer in Paris books the last seat, 14C. A second customer then asks Tokyo whether 14C is free. Tokyo has not heard about the booking and cannot find out, so it has two options. It can answer from its own copy and say that the seat is free, which is wrong, or it can refuse to answer until the link returns. The first option keeps the service available and breaks consistency; the second keeps consistency and breaks availability. No third option exists, because a correct answer needs information that sits on the far side of the broken link.
>
> Now the exact terms. A database is consistent when every read returns the latest completed write, as if only one copy existed. Availability means that every request to a working machine gets a real answer and not an error. Partition tolerance means that the database keeps its guarantees while messages between machines are lost. Eric Brewer proposed the theorem in 2000, and Seth Gilbert and Nancy Lynch proved it in 2002.
>
> Two limits matter in practice. The popular summary, "pick two of three", misleads: a system on a real network cannot opt out of partitions, so the choice is one of two, and it arises only while a partition lasts. While the network works, a system can be both consistent and available.

### What it did

The case carries the proof. Tokyo's two options are the two halves of the theorem, and the sentence about the far side of the link is the reason no third option exists. The terms are defined after the reader has watched each one fail. The common wrong picture is named and refuted, with the reason.

## Eigenvectors

Field: linear algebra. Reader: `--for "someone who can multiply a matrix by a vector"`. Depth: `standard`.

### Weak version

> An eigenvector is a vector that does not change when you multiply it by the matrix.

False for almost every eigenvector. The vector usually changes length, and it can reverse. Only the line it lies on is kept.

### Ledger

- A is a square matrix, v is a nonzero vector, and λ is a number.
- v is an eigenvector of A with eigenvalue λ when Av = λv.
- A keeps v on its own line through the origin and scales it by λ. A negative λ reverses v. A zero λ sends v to the zero vector.
- The zero vector is excluded by definition.
- Every nonzero multiple of an eigenvector is an eigenvector with the same eigenvalue.
- Applying A to an eigenvector k times multiplies it by λ to the power k.
- Some real matrices have no real eigenvectors. A rotation of the plane by 90 degrees is one.

### Strong version

> An eigenvector of a matrix is a nonzero vector that the matrix keeps on its own line. The matrix can stretch the vector, shrink it, or reverse it, but cannot turn it off that line. The stretch factor is called the eigenvalue.
>
> Take the matrix A with rows (2, 1) and (1, 2). Multiply A by the vector (1, 0) and you get (2, 1): the vector has turned. Now multiply A by (1, 1). You get (3, 3), which is 3 times (1, 1), so the matrix kept this vector on its line and stretched it by a factor of 3. So (1, 1) is an eigenvector of A with eigenvalue 3. One more: A times (1, −1) is (1, −1), which makes (1, −1) an eigenvector too, with eigenvalue 1.
>
> The general statement is one line. A nonzero vector v is an eigenvector of a square matrix A when Av = λv for some number λ, and λ is the eigenvalue. Three conditions sit in that line. The matrix is square, so that input and output live in the same space and their directions can be compared. The zero vector is excluded, because A times zero is zero for every matrix, which would tell us nothing about A. And λ can be negative, which reverses the vector, or zero, which sends it to the zero vector.
>
> Eigenvectors earn their place when a matrix is applied many times. Applying A to (1, 1) ten times multiplies the vector by 3 ten times, so the result is 59,049 times (1, 1), with no matrix arithmetic needed.
>
> Two limits. Eigenvectors come as whole lines: (2, 2) and (−5, −5) are also eigenvectors of A, with the same eigenvalue 3. And some matrices have no eigenvector with real entries: a rotation of the plane by 90 degrees turns every vector off its line, so that matrix has none.

### What it did

The first vector tried, (1, 0), is not an eigenvector. The reader sees the ordinary behavior before the special one, so the definition has something to stand against. The formula arrives in the third paragraph, after each of its parts has a number attached. Every hypothesis in the definition gets its reason. The payoff is computed: 3 to the power 10 is 59,049.
