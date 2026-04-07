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
    "reproduce": CommandSpec(
        module="scripts.reproduce_submission",
        summary="Run the flagship dormant puzzle reproduction pipeline.",
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
    "hf-publish": "publish-hf",
    "pypi-publish": "publish-pypi",
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
            "Examples:",
            "  dba reproduce --report-only --out-root artifacts/reproduction/20260305_230206",
            "  dba submit-init --task-json benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json --submission-id my_submission_v0",
            "  dba check-release --metadata-json benchmarks/public/release_metadata.json --out-json /tmp/release.json --out-md /tmp/release.md",
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

    command = ALIASES.get(args[0], args[0])
    spec = COMMANDS.get(command)
    if spec is None:
        print(f"Unknown command: {args[0]}", file=sys.stderr)
        print("Run `dba help` to see the available commands.", file=sys.stderr)
        return 2

    return _dispatch(spec.module, args[1:])
