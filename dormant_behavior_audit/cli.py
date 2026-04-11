"""Unified CLI for the public Dormant Behavior Audit workflows."""

from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from pathlib import Path

from . import __version__


@dataclass(frozen=True)
class CommandSpec:
    module: str
    summary: str


COMMANDS: dict[str, CommandSpec] = {
    "doctor": CommandSpec(
        module="scripts.doctor",
        summary="Inspect local package assets, Python version, and required tools.",
    ),
    "list-tasks": CommandSpec(
        module="scripts.list_benchmark_tasks",
        summary="List bundled benchmark task manifests.",
    ),
    "show-task": CommandSpec(
        module="scripts.show_benchmark_task",
        summary="Show one bundled benchmark task manifest.",
    ),
    "list-submissions": CommandSpec(
        module="scripts.list_benchmark_submissions",
        summary="List bundled benchmark submission manifests.",
    ),
    "scoreboard": CommandSpec(
        module="scripts.show_scoreboard",
        summary="Print the checked-in submission scoreboard.",
    ),
    "reviewer-packet": CommandSpec(
        module="scripts.build_reviewer_packet",
        summary="Build a reviewer-grade static reproducibility packet.",
    ),
    "reproduce": CommandSpec(
        module="scripts.reproduce_submission",
        summary="Run the flagship dormant puzzle reproduction pipeline.",
    ),
    "check-public-safety": CommandSpec(
        module="scripts.check_public_safety",
        summary="Scan public files for sensitive paths, emails, tokens, and keys.",
    ),
    "check-artifact-hashes": CommandSpec(
        module="scripts.check_artifact_hashes",
        summary="Verify canonical public artifact hashes.",
    ),
    "check-package-size": CommandSpec(
        module="scripts.check_package_size",
        summary="Check built package artifact sizes.",
    ),
    "check-package-contents": CommandSpec(
        module="scripts.check_package_contents",
        summary="Check built wheels include public benchmark artifacts.",
    ),
    "verify-release": CommandSpec(
        module="scripts.check_public_release",
        summary="Run the local public-release validation suite.",
    ),
    "submit-init": CommandSpec(
        module="scripts.init_benchmark_submission",
        summary="Scaffold a benchmark submission manifest.",
    ),
    "submit-run": CommandSpec(
        module="scripts.run_benchmark_submission",
        summary="Build a benchmark submission bundle from a manifest.",
    ),
    "check-bundle": CommandSpec(
        module="scripts.check_benchmark_bundle",
        summary="Validate a benchmark bundle manifest and its artifact paths.",
    ),
    "check-task": CommandSpec(
        module="scripts.check_benchmark_task",
        summary="Validate a benchmark task manifest.",
    ),
    "check-submission": CommandSpec(
        module="scripts.check_benchmark_submission",
        summary="Validate and score a benchmark submission.",
    ),
    "check-release": CommandSpec(
        module="scripts.check_release_metadata",
        summary="Validate public release metadata and homepage/report URLs.",
    ),
    "check-starters": CommandSpec(
        module="scripts.check_submission_starters",
        summary="Validate starter profiles and reusable simulated examples.",
    ),
    "check-multiturn-suite": CommandSpec(
        module="scripts.check_multiturn_suite",
        summary="Validate the public conversation-shaped multi-turn suite.",
    ),
    "publish-hf": CommandSpec(
        module="scripts.publish_huggingface_entry",
        summary="Stage or publish the Hugging Face dataset entry.",
    ),
    "publish-pypi": CommandSpec(
        module="scripts.publish_pypi",
        summary="Check and publish built distributions to PyPI.",
    ),
    "orbit": CommandSpec(
        module="orbit.__main__",
        summary="Run the Orbit pipeline runner or TUI.",
    ),
}

ALIASES = {
    "submission-init": "submit-init",
    "submission-run": "submit-run",
    "submit-validate": "check-submission",
    "submit-package": "submit-run",
    "hf-publish": "publish-hf",
    "pypi-publish": "publish-pypi",
    "tasks": "list-tasks",
    "task": "show-task",
    "submissions": "list-submissions",
    "reviewer-quickstart": "reviewer-packet",
    "release-verify": "verify-release",
}


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _print_help() -> None:
    lines = [
        "Dormant Behavior Audit CLI",
        "",
        f"Version: {__version__}",
        f"Install root: {package_root()}",
        "",
        "Usage:",
        "  dba <command> [args...]",
        "",
        "Commands:",
    ]
    width = max(len(name) for name in COMMANDS)
    for name, spec in COMMANDS.items():
        lines.append(f"  {name.ljust(width)}  {spec.summary}")
    lines.extend(
        [
            "",
            "Utility:",
            "  dba help                Show this help text",
            "  dba version             Print the installed package version",
            "  dba root                Print the installed package root",
            "",
            "Composite command forms:",
            "  dba submit init [args...]        Alias for dba submit-init",
            "  dba submit validate [args...]    Alias for dba check-submission",
            "  dba submit package [args...]     Alias for dba submit-run",
            "  dba reproduce reference-case     Run the flagship reproduction command",
            "  dba reproduce multiturn-suite    Validate the public multi-turn suite",
            "  dba reproduce reviewer-packet    Build the reviewer-grade static packet",
            "",
            "Examples:",
            "  dba doctor",
            "  dba list-tasks",
            "  dba show-task meridian_trace_multiturn_candidate_v0",
            "  dba scoreboard",
            "  dba reviewer-packet --out-root reviewer_packet",
            "  dba verify-release --skip-scoreboard-build",
            "  dba reproduce --report-only --out-root artifacts/reproduction/20260305_230206",
            "  dba submit-init --task-json benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json --submission-id my_submission_v0",
            "  dba check-release --metadata-json benchmarks/public/release_metadata.json --out-json /tmp/release.json --out-md /tmp/release.md",
            "  dba check-package-contents",
            "  dba publish-hf --stage-only",
            "  dba publish-pypi --check-only",
        ]
    )
    print("\n".join(lines))


def _dispatch(module_name: str, argv: list[str]) -> int:
    module = importlib.import_module(module_name)
    entry = getattr(module, "main", None)
    if entry is None:
        raise SystemExit(f"Module {module_name} does not expose a main() entry point")

    old_argv = sys.argv[:]
    program_name = module_name.rsplit(".", 1)[-1]
    sys.argv = [program_name, *argv]
    try:
        result = entry()
    finally:
        sys.argv = old_argv

    return 0 if result is None else int(result)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args or args[0] in {"-h", "--help", "help"}:
        _print_help()
        return 0

    if args[0] in {"-V", "--version", "version"}:
        print(__version__)
        return 0

    if args[0] == "root":
        print(package_root())
        return 0

    if args[0] == "submit":
        if len(args) < 2:
            print("Usage: dba submit <init|validate|package> [args...]", file=sys.stderr)
            return 2
        submit_map = {
            "init": "submit-init",
            "validate": "check-submission",
            "package": "submit-run",
            "run": "submit-run",
        }
        command = submit_map.get(args[1])
        if command is None:
            print(f"Unknown submit subcommand: {args[1]}", file=sys.stderr)
            return 2
        spec = COMMANDS[command]
        return _dispatch(spec.module, args[2:])

    if args[0] == "reproduce" and len(args) >= 2:
        reproduce_map = {
            "reference-case": "reproduce",
            "multiturn-suite": "check-multiturn-suite",
            "reviewer-packet": "reviewer-packet",
            "quickstart": "reviewer-packet",
        }
        command = reproduce_map.get(args[1])
        if command is not None:
            spec = COMMANDS[command]
            return _dispatch(spec.module, args[2:])

    command = ALIASES.get(args[0], args[0])
    spec = COMMANDS.get(command)
    if spec is None:
        print(f"Unknown command: {args[0]}", file=sys.stderr)
        print("Run `dba help` to see the available commands.", file=sys.stderr)
        return 2

    return _dispatch(spec.module, args[1:])


if __name__ == "__main__":
    raise SystemExit(main())
