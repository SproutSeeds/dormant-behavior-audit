# Dormant Behavior Audit Benchmark Charter

## 1. Purpose

The Dormant Behavior Audit Benchmark exists to measure whether an evaluator can discover, validate, and report latent model behaviors that do not reliably appear in ordinary capability evaluations.

This benchmark is designed to evaluate auditing skill, not prompt-hacking cleverness.

## 2. Core question

A benchmark submission should answer:

- does the model exhibit a dormant or latent behavior,
- what trigger family or activating concept best explains it,
- how specific the effect is relative to nearby controls,
- how stable the claim is across reruns,
- and what evidence supports the claim.

## 3. What this benchmark is

This benchmark is:

- local-first,
- non-invasive,
- black-box-method first,
- evidence-rich,
- control-driven,
- and claim-level reproducible.

In practice, that means the benchmark should primarily run on benchmark-owned, open-weight, or otherwise permissioned systems, while rewarding methods that work from prompts and outputs before relying on internals.

## 4. What this benchmark is not

This benchmark is not:

- a one-string guessing game,
- a benchmark that depends on repeated traffic against third-party services,
- a leaderboard built only on scalar scores,
- a substitute for ordinary capability or safety evaluations,
- or a purely mechanistic interpretability benchmark.

The Jane Street dormant-model puzzle is a motivating reference case and historical packet, not infrastructure the benchmark should depend on.

## 5. Primary benchmark layers

The benchmark has three layers:

1. Seeded reference tasks.
   Benchmark-owned or open-weight models with planted dormant behaviors and clear scoring targets.

2. Baseline and submitted methods.
   Transparent black-box or hybrid audit methods that attempt to recover and validate the behavior.

3. Artifact and scoring standard.
   A common reporting format for claims, controls, reruns, and raw evidence.

## 6. Primary tracks

The benchmark should support:

- trigger-family discovery,
- specificity and control-family suppression,
- repeated-run stability,
- cross-model divergence,
- multilingual and paraphrase sensitivity,
- hybrid corroboration for open-weight models,
- and regression analysis across model variants.

## 7. Canonical evaluation process

A standard evaluation should:

1. run a fixed prompt battery,
2. compare candidate families against nearby controls,
3. measure behavior shift and family recovery,
4. repeat key tests when the target is stochastic,
5. and produce a claim packet rather than only a numeric score.

## 8. Evidence standard

Strong benchmark artifacts should include:

- a run manifest,
- prompt and response examples,
- control-family results,
- repeated-run summaries when needed,
- a claim-level consistency report,
- and a concise narrative that distinguishes supported claims from suggestive evidence.

## 9. Access and ethics stance

The benchmark should be run in a way that is respectful of external systems and operators.

That means:

- benchmark development should primarily use local or benchmark-owned models,
- repeated traffic against third-party APIs is not required for benchmark participation,
- third-party black-box systems should be treated as optional case studies or partner-approved evaluations,
- and low-cost, low-volume probing is preferred whenever remote access is used.

## 10. Relationship to black-box evaluation

Black-box evaluation remains central to the benchmark.

However, "black-box" describes the audit method, not a requirement that the target be a commercial remote API. A local open-weight model can still be evaluated in a black-box way if the method only uses prompts and outputs.

## 11. Near-term implementation direction

The benchmark should prioritize:

- seeded local reference tasks,
- transparent baseline methods,
- reusable schemas and checkers,
- hybrid methods that add corroboration without overstating certainty,
- and additional seeded tasks that are not all anchored to one family or one vendor story.

## 12. Public claim

The benchmark's public claim should be:

Dormant behavior auditing is a distinct evaluation problem that deserves its own tasks, methods, artifact standards, and reporting norms.
