# Collaboration

The easiest way to help is to make the benchmark easier to trust, reproduce, or
extend.

## Route 1: Reproduce A Task

Start with a checked-in packet and rerun the validation scripts:

```bash
python3 scripts/check_submission_starters.py
python3 scripts/check_multiturn_suite.py
python3 scripts/build_submission_scoreboard.py
```

Useful output:

- a short note saying what environment you used,
- whether the checks passed,
- any drift or confusing instructions you found.

## Route 2: Submit A Method Run

Create a starter manifest:

```bash
dba submit init --starter-profile qwen2-7b-multiturn-clean-control --out-json /tmp/submission.json
```

Then validate and package it:

```bash
dba submit validate /tmp/submission.json
dba submit package /tmp/submission.json
```

## Route 3: Propose A Task

Good task proposals include:

- a clear candidate/control split,
- a stated model scope,
- a reason the task tests a distinct failure mode,
- a reproducibility plan,
- and a conservative interpretation boundary.

## Route 4: Audit The Methodology

High-value audits include:

- checking whether public claims match checked artifacts,
- identifying missing controls,
- finding overclaiming language,
- stress-testing scorer assumptions,
- or improving release hygiene.

## Current Help Wanted

- Independent reruns of the public multi-turn candidate/control pair.
- Additional clean controls for stateful tasks.
- A second benchmark-visible stateful candidate lane.
- Review of the preprint before broader submission.
- Better visualization of task families and evidence support.
