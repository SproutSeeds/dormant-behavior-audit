"""Print the checked-in public benchmark scoreboard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Show the checked-in public submission scoreboard")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of the Markdown table")
    args = parser.parse_args()

    if args.json:
        print((ROOT / "artifacts/submissions/SCOREBOARD.json").read_text(encoding="utf-8"))
    else:
        print((ROOT / "artifacts/submissions/SCOREBOARD.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
