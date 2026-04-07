#!/usr/bin/env python3
"""Check whether the benchmark's hosted comparator models are available on the model host."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from benchmarks.model_host import inspect_model_host_readiness


def main() -> None:
    print(json.dumps(inspect_model_host_readiness(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
