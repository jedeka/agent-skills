---
name: anomaly-hunting
description: Use this skill whenever the user is looking at data, results, experimental output, logs, plots, or literature and might be encountering something surprising, anomalous, or that does not fit expectations. Triggers include "that's weird", "unexpected result", "this number looks off", "why is this happening", "outlier", "this shouldn't", "too good to be true", "huh", "I noticed". Use this proactively when reviewing any results, to surface what does not fit instead of smoothing over it. Its job is to catch real discoveries before they get explained away as noise, and to separate genuine phenomena from artifacts. Do NOT use it to validate a success you were hoping for (use honest-iteration) or to attack a finished published claim (use red-teaming-research).
---

# Anomaly hunting (the prepared mind)

Much great science begins not with "Eureka" but with "that's funny." A surprise is the place where your model is wrong, and where your model is wrong is where the discovery is. This skill surfaces what does not fit, separates real phenomena from artifacts, and stops genuine discoveries from being explained away. It is the symmetric twin of honest-iteration: that skill stops you *believing a false success*; this one stops you *discarding a true surprise*.

## 1. Hunt for what does not fit

Actively scan results, data, logs, and claims for the observation your current model did not predict: the outlier, the number that is too good, the case that fails when it should not, the curve that bends the wrong way, the result that holds when you expected it to break. Do not smooth these over. A clean story with no anomalies often means you stopped looking, not that there was nothing there.

## 2. Quantify the surprise (Bayesian)

Rank surprises by how strongly they violate what you expected, not by how interesting they feel. The larger the gap between predicted and observed, the more information the observation carries. The biggest violations of your model are the highest-value things in the room.

## 3. Resist explaining it away

The default reflex is to rationalize an anomaly back into your existing model: "probably a bug, noise, a fluke." That reflex discards exactly the signal that matters. Before dismissing, ask: *if this were real, what would it mean?* Hold the anomaly open long enough to answer.

## 4. But triage artifact vs phenomenon (mandatory)

Most surprises are artifacts: a bug, a data leak, a measurement error, a coincidence in noise. So the first probe on any anomaly is the cheapest disconfirming check — re-run, re-seed, inspect the pipeline, verify the measurement. Only a surprise that *survives* the artifact check is a phenomenon. Skip this and anomaly-hunting becomes chasing ghosts; this step is the false-positive guard that keeps curiosity honest.

## 5. Chase the survivors

An anomaly that is real and violates your model is the most valuable lead you have. Promote it: turn it into a question and hypothesis (hand to research-ideation) and design the discriminating experiment that would explain it (experiment-design). The anomaly that survives is often a better problem than the one you started on.

## Output

A ranked list of surprises, each tagged **artifact / unresolved / real-phenomenon**, with the cheapest check to resolve the unresolved ones, and for confirmed phenomena, the question they raise.
