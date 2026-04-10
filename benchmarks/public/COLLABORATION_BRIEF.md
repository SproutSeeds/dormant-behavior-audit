# Collaboration Brief

This note is the short external-facing summary for researchers, labs, and benchmark collaborators who want to understand what this project offers and how to engage with it.

## What this project is

`Dormant Behavior Audit` is a benchmark direction for discovering, validating, and reporting latent model behaviors that ordinary capability evaluations can miss.

The current release centers on one flagship reference case:

- the dormant puzzle investigation and its normalized benchmark bundle

Around that reference case, the repo already includes:

- benchmark charter and governance docs,
- seeded local task manifests,
- a public stateful multi-turn candidate/control pair,
- baseline method contracts,
- submission packet schemas and checkers,
- a public scoreboard and suite-status layer,
- and reproducibility artifacts that emphasize claim-level consistency rather than exact JSON replay.

## Why this is useful

This work is meant to be useful for:

- model eval teams that want stronger control-family and false-positive discipline,
- interpretability groups that want benchmark-backed latent-behavior case studies,
- red-team and assurance teams that need evidence-backed audit packets,
- and benchmark maintainers who want reusable artifact standards rather than one-off writeups.

## What is already release-ready

The strongest current assets are:

- the dormant puzzle reference report,
- the benchmark reference bundle,
- the reproducibility and tightening bundles,
- the public multi-turn suite and checked-in reference packets,
- the benchmark charter and bundle spec,
- and the seeded-task plus external-submission pathway.

## Good first collaboration shapes

Low-friction ways to work together:

- run an external replication on one seeded local task,
- replicate the public multi-turn candidate lane against the matched clean-control lane,
- submit a new method packet against the existing benchmark contract,
- contribute a clean-control or mechanism-calibration task,
- run a partner-approved audit on a model family using the same reporting standard,
- or help validate the benchmark bundle/checker workflow on another lab's infrastructure.

## What a strong collaborator contribution looks like

A strong contribution is:

- explicit about budget and access mode,
- clear about what is benchmark-owned versus historical evidence,
- careful about controls and nearby false positives,
- honest about stochasticity and uncertainty,
- and packaged as a reusable artifact bundle rather than a loose anecdote.

## What not to optimize for

This project is not trying to reward:

- one lucky trigger guess,
- heavy uncontrolled API traffic,
- a leaderboard detached from evidence quality,
- or the strongest-sounding claim regardless of controls.

## Suggested next-step asks

If someone is interested, the best first ask is one of:

1. "Point me to the cleanest seeded task and baseline to replicate."
2. "Point me to the public multi-turn pair and the shortest path to a starter packet."
3. "Show me how to package a submission under the benchmark contract."
4. "Help us design a partner-approved audit packet for a model family we care about."
5. "Show me the shortest path from the reference report to the normalized benchmark bundle."

## Internal note

When the repo goes fully public, link this brief from:

- the top-level README,
- the benchmark landing assets,
- the announcement post,
- and any direct outreach email or collaboration memo.
