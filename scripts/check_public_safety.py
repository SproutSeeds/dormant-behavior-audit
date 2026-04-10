"""Scan the public repository for common accidental disclosure patterns."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SCAN_PATHS = [
    "README.md",
    "RELEASE_STATE.md",
    "CLAIM_LEDGER.md",
    "REPRODUCIBILITY.md",
    "ROADMAP.md",
    "COLLABORATION.md",
    "WANTED.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "PUBLIC_RELEASE_CHECKLIST.md",
    "CITATION.cff",
    "pyproject.toml",
    "MANIFEST.in",
    ".github",
    "benchmarks",
    "artifacts",
    "docs",
    "dormant_behavior_audit",
    "findings",
    "problems",
    "scripts",
]

SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    ".venv",
}

TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".cff",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".json",
    ".jsonl",
    ".md",
    ".pdf",
    ".py",
    ".sh",
    ".svg",
    ".tex",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class Pattern:
    name: str
    regex: re.Pattern[str]
    severity: str
    guidance: str


PATTERNS = [
    Pattern(
        "local_home_path",
        re.compile(r"/Users/[A-Za-z0-9_.-]+"),
        "failure",
        "Replace personal home paths with repo-relative paths or documented env vars.",
    ),
    Pattern(
        "local_volume_path",
        re.compile(r"/Volumes/[^\s\"')\]}<>]+"),
        "failure",
        "Do not publish machine-local mounted volume paths.",
    ),
    Pattern(
        "dead_private_model_mount",
        re.compile(r"APFS_4TB_Backup|Drive_1_SSD_mirror|Drive 1 SSD"),
        "failure",
        "Keep model-store details in private docs or environment variables.",
    ),
    Pattern(
        "old_personal_email",
        re.compile(r"codyshanemitchell@gmail\.com|cody@codacli\.com", re.I),
        "failure",
        "Use the public business contact cody@frg.earth instead.",
    ),
    Pattern(
        "pypi_token",
        re.compile(r"\bpypi-[A-Za-z0-9_-]{40,}\b"),
        "failure",
        "Revoke the token and remove it from public history.",
    ),
    Pattern(
        "huggingface_token",
        re.compile(r"\bhf_[A-Za-z0-9]{25,}\b"),
        "failure",
        "Revoke the token and remove it from public history.",
    ),
    Pattern(
        "github_token",
        re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{30,}\b"),
        "failure",
        "Revoke the token and remove it from public history.",
    ),
    Pattern(
        "openai_token",
        re.compile(r"\bsk-[A-Za-z0-9_-]{30,}\b"),
        "failure",
        "Revoke the token and remove it from public history.",
    ),
    Pattern(
        "aws_access_key",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "failure",
        "Revoke the key and remove it from public history.",
    ),
    Pattern(
        "private_key_block",
        re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "failure",
        "Remove private keys immediately.",
    ),
]


def iter_text_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in paths:
        path = (ROOT / item).resolve()
        if not path.exists():
            continue
        if path.is_file():
            if path.suffix in TEXT_SUFFIXES:
                files.append(path)
            continue
        for child in path.rglob("*"):
            if any(part in SKIP_DIRS for part in child.relative_to(ROOT).parts):
                continue
            if child.is_file() and child.suffix in TEXT_SUFFIXES:
                files.append(child)
    return sorted(set(files))


def scan_file(path: Path) -> list[dict]:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "scripts/check_public_safety.py":
        # The scanner contains the literal patterns it is designed to catch.
        return []
    text = extract_text(path)

    findings: list[dict] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pattern in PATTERNS:
            if pattern.regex.search(line):
                findings.append(
                    {
                        "severity": pattern.severity,
                        "pattern": pattern.name,
                        "path": rel,
                        "line": line_no,
                        "guidance": pattern.guidance,
                    }
                )
    return findings


def extract_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        pdftotext = shutil.which("pdftotext")
        if pdftotext:
            proc = subprocess.run(
                [pdftotext, "-layout", str(path), "-"],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                errors="ignore",
            )
            if proc.returncode == 0:
                return proc.stdout
        # A byte-level fallback still catches accidentally embedded tokens or paths.
        return path.read_bytes().decode("utf-8", errors="ignore")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def write_markdown(path: Path, findings: list[dict], scanned: int) -> None:
    failures = [item for item in findings if item["severity"] == "failure"]
    lines = [
        "# Public Safety Scan",
        "",
        f"- Files scanned: `{scanned}`",
        f"- Findings: `{len(findings)}`",
        f"- Failures: `{len(failures)}`",
        "",
    ]
    if findings:
        lines.extend(["## Findings", ""])
        lines.append("| Severity | Pattern | File | Line | Guidance |")
        lines.append("|---|---|---|---:|---|")
        for item in findings:
            lines.append(
                f"| `{item['severity']}` | `{item['pattern']}` | `{item['path']}` | `{item['line']}` | {item['guidance']} |"
            )
    else:
        lines.append("No sensitive public-surface patterns were detected.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan public files for accidental disclosure patterns")
    parser.add_argument("--path", action="append", dest="paths", help="Repo-relative file or directory to scan")
    parser.add_argument("--out-json", default="", help="Optional JSON report path")
    parser.add_argument("--out-md", default="", help="Optional Markdown report path")
    args = parser.parse_args()

    scan_paths = args.paths or DEFAULT_SCAN_PATHS
    files = iter_text_files(scan_paths)
    findings: list[dict] = []
    for path in files:
        findings.extend(scan_file(path))

    report = {
        "schema_version": "public_safety_scan_v0",
        "files_scanned": len(files),
        "findings": findings,
        "summary": {
            "findings": len(findings),
            "failures": sum(1 for item in findings if item["severity"] == "failure"),
        },
    }

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.out_md:
        write_markdown(Path(args.out_md), findings, len(files))

    print(json.dumps(report["summary"], indent=2))
    return 1 if report["summary"]["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
