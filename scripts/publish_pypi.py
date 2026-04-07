#!/usr/bin/env python3
"""Publish built distributions to PyPI using an ORP-managed token when available."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIST_DIR = ROOT / "dist"
DEFAULT_SECRET_ALIAS = "pypi-primary"
PACKAGE_NAME = "dormant-behavior-audit"
TOKEN_ENV_VARS = ("TWINE_PASSWORD", "PYPI_API_TOKEN", "PYPI_TOKEN")


def twine_base_command() -> list[str]:
    if importlib.util.find_spec("twine") is not None:
        return [sys.executable, "-m", "twine"]
    if shutil.which("uv"):
        return ["uv", "run", "--with", "twine", "python", "-m", "twine"]
    raise SystemExit("Twine is not installed and `uv` is unavailable. Install `twine` or `uv` first.")


def run(cmd: list[str], *, env: dict[str, str] | None = None, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        check=True,
        env=env,
        text=True,
        capture_output=capture_output,
    )


def discover_distributions(dist_dir: Path) -> list[Path]:
    files = sorted(path for path in dist_dir.glob("*") if path.is_file())
    distributions = [path for path in files if path.suffix == ".whl" or path.name.endswith(".tar.gz")]
    if not distributions:
        raise SystemExit(f"No distribution artifacts found under {dist_dir}. Run `uv build` first.")
    return distributions


def resolve_orp_token(alias: str) -> str | None:
    if not shutil.which("orp"):
        return None
    result = subprocess.run(
        [
            "orp",
            "secrets",
            "resolve",
            alias,
            "--reveal",
            "--local-first",
            "--json",
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    value = payload.get("value")
    return str(value).strip() if value else None


def resolve_token(secret_alias: str, *, no_orp: bool) -> tuple[str | None, str | None]:
    if not no_orp:
        token = resolve_orp_token(secret_alias)
        if token:
            return token, f"ORP secret `{secret_alias}`"
    for env_name in TOKEN_ENV_VARS:
        value = os.environ.get(env_name, "").strip()
        if value:
            return value, f"environment variable `{env_name}`"
    return None, None


def project_url(repository: str) -> str:
    if repository == "testpypi":
        return f"https://test.pypi.org/project/{PACKAGE_NAME}/"
    return f"https://pypi.org/project/{PACKAGE_NAME}/"


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish built distributions to PyPI")
    parser.add_argument("--dist-dir", default=str(DEFAULT_DIST_DIR), help="Directory containing wheel and sdist artifacts")
    parser.add_argument(
        "--repository",
        choices=("pypi", "testpypi"),
        default="pypi",
        help="Upload target (default: pypi)",
    )
    parser.add_argument(
        "--secret-alias",
        default=DEFAULT_SECRET_ALIAS,
        help=f"ORP secret alias to resolve before upload (default: {DEFAULT_SECRET_ALIAS})",
    )
    parser.add_argument("--no-orp", action="store_true", help="Skip ORP secret resolution and rely on environment variables")
    parser.add_argument("--skip-existing", action="store_true", help="Pass --skip-existing to Twine upload")
    parser.add_argument("--check-only", action="store_true", help="Only run `twine check` against dist artifacts")
    args = parser.parse_args()

    dist_dir = Path(args.dist_dir).resolve()
    distributions = discover_distributions(dist_dir)
    print("Distributions:")
    for path in distributions:
        print(f"  - {path}")

    twine_cmd = twine_base_command()
    check_cmd = [*twine_cmd, "check", *[str(path) for path in distributions]]
    print("Running Twine check...")
    run(check_cmd)

    if args.check_only:
        print("Check-only mode enabled; no upload attempted.")
        return 0

    token, token_source = resolve_token(args.secret_alias, no_orp=args.no_orp)
    if not token:
        raise SystemExit(
            "No PyPI token found. Save one with ORP or set TWINE_PASSWORD / PYPI_API_TOKEN / PYPI_TOKEN first."
        )

    upload_cmd = [*twine_cmd, "upload"]
    if args.repository == "testpypi":
        upload_cmd.extend(["--repository", "testpypi"])
    if args.skip_existing:
        upload_cmd.append("--skip-existing")
    upload_cmd.extend(str(path) for path in distributions)

    env = os.environ.copy()
    env["TWINE_USERNAME"] = "__token__"
    env["TWINE_PASSWORD"] = token
    env["TWINE_NON_INTERACTIVE"] = "1"

    print(f"Resolved token from {token_source}.")
    print(f"Uploading to {args.repository}...")
    run(upload_cmd, env=env)
    print(f"Published: {project_url(args.repository)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
