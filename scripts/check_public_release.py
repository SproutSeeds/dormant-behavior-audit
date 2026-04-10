"""Run the local public-release validation suite."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(label: str, cmd: list[str]) -> bool:
    print(f"== {label}")
    result = subprocess.run(cmd, cwd=ROOT)
    print()
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run public release validation checks")
    parser.add_argument("--skip-scoreboard-build", action="store_true")
    parser.add_argument("--require-dist", action="store_true")
    args = parser.parse_args()

    checks = [
        ("public safety", [sys.executable, "scripts/check_public_safety.py"]),
        ("artifact hashes", [sys.executable, "scripts/check_artifact_hashes.py"]),
        ("submission starters", [sys.executable, "scripts/check_submission_starters.py"]),
        ("multi-turn suite", [sys.executable, "scripts/check_multiturn_suite.py"]),
        ("package size", [sys.executable, "scripts/check_package_size.py"] + (["--require-dist"] if args.require_dist else [])),
    ]
    if not args.skip_scoreboard_build:
        checks.insert(4, ("scoreboard rebuild", [sys.executable, "scripts/build_submission_scoreboard.py"]))

    failures = [label for label, cmd in checks if not run(label, cmd)]
    if failures:
        print("Public release checks failed: " + ", ".join(failures))
        return 1
    print("Public release checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
