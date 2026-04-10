"""Check that built package artifacts stay within expected size bounds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def mb(size_bytes: int) -> float:
    return size_bytes / (1024 * 1024)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Python distribution artifact sizes")
    parser.add_argument("--dist-dir", default="dist", help="Directory containing built distributions")
    parser.add_argument("--max-wheel-mb", type=float, default=25.0)
    parser.add_argument("--max-sdist-mb", type=float, default=50.0)
    parser.add_argument("--require-dist", action="store_true", help="Fail if no dist artifacts are present")
    args = parser.parse_args()

    dist_dir = Path(args.dist_dir)
    if not dist_dir.is_absolute():
        dist_dir = ROOT / dist_dir

    artifacts = sorted(dist_dir.glob("*")) if dist_dir.exists() else []
    artifacts = [path for path in artifacts if path.is_file()]

    findings = []
    for path in artifacts:
        size = mb(path.stat().st_size)
        if path.suffix == ".whl":
            limit = args.max_wheel_mb
        elif path.name.endswith(".tar.gz") or path.suffix == ".zip":
            limit = args.max_sdist_mb
        else:
            continue
        if size > limit:
            findings.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "size_mb": round(size, 3),
                    "limit_mb": limit,
                }
            )

    if args.require_dist and not artifacts:
        findings.append({"path": str(dist_dir), "reason": "no_distribution_artifacts"})

    report = {
        "schema_version": "package_size_check_v0",
        "artifacts": [
            {"path": path.relative_to(ROOT).as_posix(), "size_mb": round(mb(path.stat().st_size), 3)}
            for path in artifacts
        ],
        "summary": {"artifacts": len(artifacts), "failures": len(findings)},
        "findings": findings,
    }
    print(json.dumps(report, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
