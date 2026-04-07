"""Allow ``python -m orbit`` for either TUI or headless pipeline runs."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from orbit.core.orbit import run_headless, run_tui


def main() -> None:
    parser = argparse.ArgumentParser(description="Orbit pipeline runner")
    parser.add_argument("--scope", help="Scope YAML path for a headless run")
    parser.add_argument("--state-dir", default="data/state", help="Directory for pipeline state files")
    args = parser.parse_args()

    if args.scope:
        state = asyncio.run(
            run_headless(
                scope_yaml=Path(args.scope),
                state_dir=Path(args.state_dir),
            )
        )
        print(f"{state.status} {len(state.findings)} findings")
        return

    run_tui(state_dir=Path(args.state_dir))


if __name__ == "__main__":
    main()
