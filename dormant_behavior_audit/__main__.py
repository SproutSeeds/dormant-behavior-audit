"""Allow ``python -m dormant_behavior_audit``."""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
