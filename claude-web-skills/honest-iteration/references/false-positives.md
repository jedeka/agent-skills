# How fast probes lie (false-positive taxonomy)

A "successful" probe is the most dangerous output in exploration, because you are moving fast, have no test suite, and want it to be true. Before believing one, check it against the classes below.

**The universal test:** perturb something that should not matter — the seed, the data split, a constant, the specific example. If the result vanishes, it was never real.

## Data / leakage
- The answer is in the input (label leakage; the target leaks through a feature).
- Train and test overlap; the model simply memorized the toy set.
- The eval case is too easy or cherry-picked and does not represent the real problem.

## Code / bug-as-success
- A bug hardcodes or short-circuits the result — it returns the very constant you were hoping for.
- The metric is computed wrong in a direction that flatters.
- The probe silently tests something easier than the crux: the hard part got stubbed and never re-enabled.

## Statistics / noise
- A single run landed well by chance; re-seed and it is gone.
- You are reading a pattern into variance — the difference is within run-to-run noise.
- Best-of-many: you ran it five times and remember the one that worked.

## Cognition / confirmation
- You interpreted an ambiguous result as success because you wanted it.
- You moved the goalpost so the result counts.
- You overfit to the single example in front of you; it will not generalize one inch.

## The one-question filter
"If I change the thing that should not matter, does the result hold?" If you have not checked, you do not yet have a result — you have a hope.
