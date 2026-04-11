#!/usr/bin/env python3
"""Build a reviewer-grade reproducibility packet without model or API calls."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPRODUCTION_ROOT = ROOT / "artifacts" / "reproduction" / "20260305_230206"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def packet_rel(path: Path, out_root: Path) -> str:
    try:
        return path.relative_to(out_root).as_posix()
    except ValueError:
        return path.name


def display_command(command: list[str], out_root: Path) -> list[str]:
    display: list[str] = []
    for index, arg in enumerate(command):
        if index == 0 and Path(arg) == Path(sys.executable):
            display.append("python3")
            continue
        path = Path(arg)
        if path.is_absolute():
            try:
                display.append(path.relative_to(ROOT).as_posix())
                continue
            except ValueError:
                pass
            try:
                display.append("$PACKET/" + path.relative_to(out_root).as_posix())
                continue
            except ValueError:
                display.append(path.name)
                continue
        display.append(arg)
    return display


def run_capture(label: str, command: list[str], log_dir: Path, out_root: Path) -> dict[str, Any]:
    safe_label = label.replace(" ", "_").replace("/", "_")
    env = os.environ.copy()
    env.setdefault("PYTHONPYCACHEPREFIX", "/tmp/pycache")
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    stdout_path = log_dir / f"{safe_label}.stdout.txt"
    stderr_path = log_dir / f"{safe_label}.stderr.txt"
    stdout_path.write_text(result.stdout, encoding="utf-8")
    stderr_path.write_text(result.stderr, encoding="utf-8")
    return {
        "id": safe_label,
        "label": label,
        "command": display_command(command, out_root),
        "returncode": result.returncode,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "stdout": "$PACKET/" + packet_rel(stdout_path, out_root),
        "stderr": "$PACKET/" + packet_rel(stderr_path, out_root),
    }


def copy_if_present(source: Path, destination: Path, out_root: Path) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        return {
            "source": rel(source),
            "destination": "$PACKET/" + packet_rel(destination, out_root),
            "status": "missing",
        }
    shutil.copy2(source, destination)
    return {
        "source": rel(source),
        "destination": "$PACKET/" + packet_rel(destination, out_root),
        "status": "copied",
    }


def copy_first_present(sources: list[Path], destination: Path, out_root: Path) -> dict[str, Any]:
    for source in sources:
        if source.exists():
            return copy_if_present(source, destination, out_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    return {
        "source": " or ".join(rel(source) for source in sources),
        "destination": "$PACKET/" + packet_rel(destination, out_root),
        "status": "missing",
    }


def git_value(args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
    except Exception:
        return "unavailable"
    return result.stdout.strip() or "unavailable"


def summarize_scoreboard(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "missing"}
    data = read_json(path)
    summary = data.get("summary", {})
    rows = data.get("rows", [])
    return {
        "status": "present",
        "num_submissions": summary.get("num_submissions", len(rows)),
        "zero_failure_submissions": summary.get("zero_failure_submissions"),
        "zero_incremental_api_submissions": summary.get("zero_incremental_api_submissions"),
        "interpretation_counts": summary.get("interpretation_counts", {}),
    }


def summarize_multiturn(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "missing"}
    data = read_json(path)
    summary = data.get("summary", {})
    return {
        "status": "present",
        "candidate_task_id": summary.get("candidate_task_id"),
        "control_task_id": summary.get("control_task_id"),
        "second_control_task_id": summary.get("second_control_task_id"),
        "candidate_repeat_status": summary.get("candidate_repeat_status"),
        "clean_control_repeat_status": summary.get("clean_control_repeat_status"),
        "second_clean_control_repeat_status": summary.get("second_clean_control_repeat_status"),
        "alignment_passed": summary.get("alignment_passed"),
    }


def package_visible_hash_manifest(out_root: Path) -> tuple[Path, list[str]]:
    source_manifest = ROOT / "benchmarks" / "public" / "artifact_hash_manifest_v0.json"
    manifest = read_json(source_manifest)
    visible_files = []
    skipped = []
    for entry in manifest.get("files", []):
        if (ROOT / entry["path"]).exists():
            visible_files.append(entry)
        else:
            skipped.append(entry["path"])
    if not skipped:
        return source_manifest, []
    package_manifest = {
        **manifest,
        "scope": manifest.get("scope", "") + " (package-visible subset)",
        "files": visible_files,
        "skipped_missing_from_installed_package": skipped,
    }
    path = out_root / "package_visible_artifact_hash_manifest_v0.json"
    write_json(path, package_manifest)
    return path, skipped


def format_command(command: list[str]) -> str:
    return " ".join(command)


def build_markdown(payload: dict[str, Any]) -> str:
    checks = payload["checks"]
    failures = [check for check in checks if check["status"] != "PASS"]
    scoreboard = payload["scoreboard_summary"]
    multiturn = payload["multiturn_summary"]
    command_rows = [
        "| Status | Check | Command | Logs |",
        "|---|---|---|---|",
    ]
    for check in checks:
        command_rows.append(
            f"| {check['status']} | {check['label']} | `{format_command(check['command'])}` | `{check['stdout']}` / `{check['stderr']}` |"
        )

    lines = [
        "# Reviewer Reproducibility Packet",
        "",
        "This packet is the fastest reviewer-facing verification path for Dormant Behavior Audit.",
        "It intentionally avoids fresh model-weight downloads, API calls, paid services, and human contact.",
        "",
        "## Summary",
        "",
        f"- Generated: `{payload['generated_at']}`",
        f"- Repository root inspected: `{payload['repository']['root']}`",
        f"- Git commit: `{payload['repository']['commit']}`",
        f"- Git status: `{payload['repository']['status']}`",
        f"- Python: `{payload['environment']['python']}`",
        f"- Platform: `{payload['environment']['platform']}`",
        f"- Check failures: `{len(failures)}`",
        "",
        "## Core Evidence Snapshot",
        "",
        f"- Scoreboard submissions: `{scoreboard.get('num_submissions', 'unknown')}`",
        f"- Scoreboard zero-failure submissions: `{scoreboard.get('zero_failure_submissions', 'unknown')}`",
        f"- Scoreboard zero-incremental-API submissions: `{scoreboard.get('zero_incremental_api_submissions', 'unknown')}`",
        f"- Multi-turn candidate lane: `{multiturn.get('candidate_task_id', 'unknown')}`",
        f"- Qwen2 clean-control lane: `{multiturn.get('control_task_id', 'unknown')}`",
        f"- Qwen2.5 clean-control lane: `{multiturn.get('second_control_task_id', 'unknown')}`",
        f"- Multi-turn alignment passed: `{multiturn.get('alignment_passed', 'unknown')}`",
        "",
        "## Commands Run",
        "",
        *command_rows,
        "",
        "## Copied Reviewer Materials",
        "",
    ]
    for item in payload["copied_materials"]:
        lines.append(f"- `{item['destination']}` from `{item['source']}`: `{item['status']}`")
    if payload.get("package_visible_hash_skips"):
        lines.extend(
            [
                "",
                "## Package-visible Hash Subset",
                "",
                "The installed-wheel packet used a package-visible subset of the public hash manifest because",
                "the following source-checkout-only files were not present inside the wheel:",
            ]
        )
        for skipped in payload["package_visible_hash_skips"]:
            lines.append(f"- `{skipped}`")
    lines.extend(
        [
            "",
            "## How To Read This Packet",
            "",
            "Start with `REVIEWER_QUICKSTART.md`, then inspect `TRACEABILITY_MATRIX.md`, `CLAIM_LEDGER.md`,",
            "`SCOREBOARD.md`, and `MULTITURN_SUITE_STATUS.md`. The machine-readable manifest is",
            "`reviewer_packet_manifest.json`.",
            "",
            "## Boundary",
            "",
            "Passing this packet means the public release artifacts are internally consistent and reproducible",
            "at the static/package-review level. It does not prove universal dormant-behavior detection, and",
            "it does not replace independent model reruns.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_commands(out_root: Path, reproduction_root: Path) -> str:
    lines = [
        "# Reproduction Commands",
        "",
        "Use these commands from a fresh clone for the fastest reviewer path.",
        "",
        "## Ten-minute artifact review",
        "",
        "```bash",
        "python3 scripts/check_public_safety.py",
        "python3 scripts/check_artifact_hashes.py",
        "python3 scripts/check_multiturn_suite.py",
        "python3 scripts/check_submission_starters.py",
        "python3 scripts/build_reviewer_packet.py --out-root reviewer_packet",
        "```",
        "",
        "## Package-native review",
        "",
        "```bash",
        "pipx install dormant-behavior-audit",
        "dba doctor",
        "dba scoreboard --json",
        "dba reviewer-packet --out-root reviewer_packet",
        "```",
        "",
        "## Checked-in reference report refresh",
        "",
        "This verifies the existing reference reproduction report without fresh hosted API calls.",
        "",
        "```bash",
        f"python3 scripts/reproduce_submission.py --report-only --out-root {rel(reproduction_root)}",
        "```",
        "",
        "## Full local rerun",
        "",
        "Only use this when local model weights and suitable hardware are available.",
        "",
        "```bash",
        "python3 scripts/reproduce_submission.py",
        "```",
        "",
        f"Last packet output root: `{out_root}`",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a reviewer-grade reproducibility packet")
    parser.add_argument(
        "--out-root",
        default="",
        help="Directory for the generated reviewer packet. Defaults to ./dba_reviewer_packet_<UTC timestamp>.",
    )
    parser.add_argument(
        "--reproduction-root",
        default=str(DEFAULT_REPRODUCTION_ROOT),
        help="Checked-in reproduction root used for report-only reference-case guidance.",
    )
    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Assemble copied materials without rerunning validation commands.",
    )
    args = parser.parse_args()

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_root = Path(args.out_root) if args.out_root else Path.cwd() / f"dba_reviewer_packet_{stamp}"
    out_root.mkdir(parents=True, exist_ok=True)
    log_dir = out_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    reproduction_root = Path(args.reproduction_root)

    checks: list[dict[str, Any]] = []
    if not args.skip_checks:
        hash_manifest, skipped_hash_entries = package_visible_hash_manifest(out_root)
        checks.append(run_capture("doctor", [sys.executable, str(ROOT / "scripts" / "doctor.py")], log_dir, out_root))
        checks.append(
            run_capture(
                "public safety",
                [sys.executable, str(ROOT / "scripts" / "check_public_safety.py")],
                log_dir,
                out_root,
            )
        )
        checks.append(
            run_capture(
                "artifact hashes",
                [sys.executable, str(ROOT / "scripts" / "check_artifact_hashes.py"), "--manifest", str(hash_manifest)],
                log_dir,
                out_root,
            )
        )
    else:
        skipped_hash_entries = []
    if not args.skip_checks:
        checks.append(
            run_capture(
                "submission starters",
                [sys.executable, str(ROOT / "scripts" / "check_submission_starters.py")],
                log_dir,
                out_root,
            )
        )
        checks.append(
            run_capture(
                "multi-turn suite",
                [
                    sys.executable,
                    str(ROOT / "scripts" / "check_multiturn_suite.py"),
                    "--out-json",
                    str(out_root / "MULTITURN_SUITE_STATUS.json"),
                    "--out-md",
                    str(out_root / "MULTITURN_SUITE_STATUS.md"),
                ],
                log_dir,
                out_root,
            )
        )
        checks.append(
            run_capture(
                "scoreboard json",
                [sys.executable, str(ROOT / "scripts" / "show_scoreboard.py"), "--json"],
                log_dir,
                out_root,
            )
        )
    if args.skip_checks:
        checks.append(
            {
                "id": "skipped",
                "label": "validation commands",
                "command": ["--skip-checks"],
                "returncode": 0,
                "status": "PASS",
                "stdout": "",
                "stderr": "",
            }
        )

    copied_materials = [
        copy_first_present(
            [ROOT / "REVIEWER_QUICKSTART.md", ROOT / "benchmarks" / "public" / "REVIEWER_QUICKSTART.md"],
            out_root / "REVIEWER_QUICKSTART.md",
            out_root,
        ),
        copy_first_present(
            [ROOT / "TRACEABILITY_MATRIX.md", ROOT / "benchmarks" / "public" / "TRACEABILITY_MATRIX.md"],
            out_root / "TRACEABILITY_MATRIX.md",
            out_root,
        ),
        copy_first_present(
            [ROOT / "CLAIM_LEDGER.md", ROOT / "benchmarks" / "public" / "CLAIM_LEDGER.md"],
            out_root / "CLAIM_LEDGER.md",
            out_root,
        ),
        copy_if_present(ROOT / "benchmarks" / "public" / "ARXIV_ENDORSEMENT_PACKET.md", out_root / "ARXIV_ENDORSEMENT_PACKET.md", out_root),
        copy_if_present(ROOT / "artifacts" / "submissions" / "SCOREBOARD.json", out_root / "SCOREBOARD.json", out_root),
        copy_if_present(ROOT / "artifacts" / "submissions" / "SCOREBOARD.md", out_root / "SCOREBOARD.md", out_root),
        copy_if_present(ROOT / "benchmarks" / "public" / "artifact_hash_manifest_v0.json", out_root / "artifact_hash_manifest_v0.json", out_root),
        copy_if_present(ROOT / "benchmarks" / "MULTITURN_SUITE_STATUS.json", out_root / "MULTITURN_SUITE_STATUS.checked_in.json", out_root),
        copy_if_present(ROOT / "benchmarks" / "MULTITURN_SUITE_STATUS.md", out_root / "MULTITURN_SUITE_STATUS.checked_in.md", out_root),
        copy_if_present(reproduction_root / "reproduction_report.md", out_root / "reference_reproduction_report.md", out_root),
        copy_if_present(reproduction_root / "findings" / "claim_consistency_report.md", out_root / "reference_claim_consistency_report.md", out_root),
    ]

    commands_path = out_root / "REPRODUCTION_COMMANDS.md"
    commands_path.write_text(build_commands(out_root, reproduction_root), encoding="utf-8")
    copied_materials.append(
        {
            "source": "generated",
            "destination": "$PACKET/" + packet_rel(commands_path, out_root),
            "status": "written",
        }
    )

    multiturn_json = out_root / "MULTITURN_SUITE_STATUS.json"
    if not multiturn_json.exists():
        multiturn_json = ROOT / "benchmarks" / "MULTITURN_SUITE_STATUS.json"
    scoreboard_json = out_root / "SCOREBOARD.json"

    payload: dict[str, Any] = {
        "schema_version": "reviewer_reproducibility_packet_v0",
        "generated_at": utc_now(),
        "repository": {
            "root": "package_or_checkout_root",
            "local_paths_redacted": True,
            "commit": git_value(["rev-parse", "HEAD"]),
            "branch": git_value(["branch", "--show-current"]),
            "status": git_value(["status", "--short"]) or "clean",
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "checks": checks,
        "scoreboard_summary": summarize_scoreboard(scoreboard_json),
        "multiturn_summary": summarize_multiturn(multiturn_json),
        "package_visible_hash_skips": skipped_hash_entries,
        "copied_materials": copied_materials,
    }

    manifest_path = out_root / "reviewer_packet_manifest.json"
    write_json(manifest_path, payload)
    (out_root / "REVIEWER_PACKET.md").write_text(build_markdown(payload), encoding="utf-8")

    failures = [check for check in checks if check["status"] != "PASS"]
    print(f"Reviewer packet: {out_root}")
    print(f"Manifest: {manifest_path}")
    print(f"Checks: {len(checks) - len(failures)} passed, {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
