#!/usr/bin/env python3
"""Stage and publish the public benchmark entry to the Hugging Face Hub."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STAGE_DIR = ROOT / "tmp" / "huggingface_entry"
DEFAULT_REPO_ID = "SproutSeeds/dormant-behavior-audit"

FILES_TO_STAGE = {
    ROOT / "benchmarks" / "public" / "HF_DATASET_CARD.md": Path("README.md"),
    ROOT / "findings" / "CodyMitchell_DormantPuzzle_Submission_V2_2026-03-06.pdf": Path(
        "dormant-behavior-audit-v1.0.0-reference-report.pdf"
    ),
    ROOT / "benchmarks" / "reference" / "dormant_puzzle_v1" / "benchmark_bundle_v0.json": Path(
        "dormant-behavior-audit-v1.0.0-reference-bundle.json"
    ),
    ROOT / "benchmarks" / "public" / "release_metadata.json": Path("release_metadata.json"),
    ROOT / "benchmarks" / "public" / "SUBMISSION_SCOREBOARD.md": Path("SUBMISSION_SCOREBOARD.md"),
}


def run(cmd: list[str], *, token: str | None = None) -> None:
    env = os.environ.copy()
    if token:
        env["HF_TOKEN"] = token
    subprocess.run(cmd, check=True, env=env)


def resolve_token(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    for name in ("HF_TOKEN", "HUGGINGFACE_HUB_TOKEN"):
        value = os.environ.get(name)
        if value:
            return value
    return None


def stage_files(stage_dir: Path) -> None:
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    stage_dir.mkdir(parents=True, exist_ok=True)
    for src, rel_dst in FILES_TO_STAGE.items():
        dst = stage_dir / rel_dst
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def check_logged_in() -> bool:
    result = subprocess.run(
        ["hf", "auth", "whoami"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and "Not logged in" not in result.stdout


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish the benchmark entry to the Hugging Face Hub")
    parser.add_argument("--repo-id", default=DEFAULT_REPO_ID)
    parser.add_argument("--stage-dir", default=str(DEFAULT_STAGE_DIR))
    parser.add_argument("--token", default=None, help="Optional Hugging Face token")
    parser.add_argument("--stage-only", action="store_true", help="Only build the staging directory")
    args = parser.parse_args()

    stage_dir = Path(args.stage_dir).resolve()
    token = resolve_token(args.token)

    stage_files(stage_dir)
    print(f"Staged Hugging Face dataset entry at: {stage_dir}")
    for rel_path in sorted(path.as_posix() for path in FILES_TO_STAGE.values()):
        print(f"  - {rel_path}")

    if args.stage_only:
        print("Stage-only mode enabled; no remote changes made.")
        return

    if not token and not check_logged_in():
        raise SystemExit(
            "Hugging Face authentication is required. Pass --token or set HF_TOKEN / "
            "HUGGINGFACE_HUB_TOKEN, or run `hf auth login` first."
        )

    repo_create_cmd = [
        "hf",
        "repo",
        "create",
        args.repo_id,
        "--repo-type",
        "dataset",
        "--exist-ok",
    ]
    upload_cmd = [
        "hf",
        "upload",
        args.repo_id,
        str(stage_dir),
        ".",
        "--repo-type",
        "dataset",
        "--commit-message",
        "Publish Dormant Behavior Audit v1.0.0 benchmark entry",
    ]
    if token:
        repo_create_cmd.extend(["--token", token])
        upload_cmd.extend(["--token", token])

    run(repo_create_cmd, token=token)
    run(upload_cmd, token=token)
    print(f"Published dataset entry to https://huggingface.co/datasets/{args.repo_id}")


if __name__ == "__main__":
    main()
