"""Build or verify hashes for canonical public release artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "benchmarks/public/artifact_hash_manifest_v0.json"

DEFAULT_ARTIFACTS = [
    "CITATION.cff",
    "benchmarks/MULTITURN_SUITE_STATUS.json",
    "benchmarks/MULTITURN_SUITE_STATUS.md",
    "benchmarks/public/SUBMISSION_SCOREBOARD.json",
    "benchmarks/public/SUBMISSION_SCOREBOARD.md",
    "benchmarks/public/release_metadata.json",
    "benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json",
    "artifacts/submissions/SCOREBOARD.json",
    "artifacts/submissions/SCOREBOARD.md",
    "artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/repeated_run_summary_v0.json",
    "artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/LOCAL_REPEAT_SUMMARY.md",
    "artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/repeated_runs/repeated_run_summary_v0.json",
    "artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/repeated_runs/LOCAL_REPEAT_SUMMARY.md",
    "findings/DormantBehaviorAudit_ReferenceCase_Preprint_2026-04-07.pdf",
    "findings/PREPRINT_SUBMISSION.tex",
]


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def build_manifest(paths: list[str]) -> dict:
    files = []
    for rel in paths:
        path = ROOT / rel
        if not path.exists():
            raise FileNotFoundError(f"Missing artifact: {rel}")
        files.append(
            {
                "path": rel,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return {
        "schema_version": "artifact_hash_manifest_v0",
        "scope": "canonical public release and repeat-anchor artifacts",
        "hash_algorithm": "sha256",
        "files": files,
    }


def verify_manifest(manifest: dict) -> list[dict]:
    findings = []
    for entry in manifest.get("files", []):
        rel = entry["path"]
        path = ROOT / rel
        if not path.exists():
            findings.append({"status": "FAIL", "path": rel, "reason": "missing"})
            continue
        size = path.stat().st_size
        digest = sha256_file(path)
        if size != entry.get("size_bytes"):
            findings.append(
                {
                    "status": "FAIL",
                    "path": rel,
                    "reason": "size_mismatch",
                    "expected": entry.get("size_bytes"),
                    "actual": size,
                }
            )
        if digest != entry.get("sha256"):
            findings.append(
                {
                    "status": "FAIL",
                    "path": rel,
                    "reason": "sha256_mismatch",
                    "expected": entry.get("sha256"),
                    "actual": digest,
                }
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Build or verify canonical public artifact hashes")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Manifest JSON path")
    parser.add_argument("--build", action="store_true", help="Write a fresh manifest")
    parser.add_argument("--artifact", action="append", dest="artifacts", help="Repo-relative artifact path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path

    if args.build:
        manifest = build_manifest(args.artifacts or DEFAULT_ARTIFACTS)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {manifest_path.relative_to(ROOT)} with {len(manifest['files'])} artifacts")
        return 0

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    findings = verify_manifest(manifest)
    summary = {"artifacts": len(manifest.get("files", [])), "failures": len(findings)}
    print(json.dumps({"summary": summary, "findings": findings}, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
