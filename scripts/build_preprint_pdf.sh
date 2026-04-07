#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="$ROOT/findings/PREPRINT_SUBMISSION.tex"
OUTPUT="${1:-$ROOT/findings/DormantBehaviorAudit_ReferenceCase_Preprint_2026-04-07.pdf}"

if ! command -v xelatex >/dev/null 2>&1; then
  echo "xelatex is required to build the preprint PDF." >&2
  exit 1
fi

BUILD_DIR="$(mktemp -d /tmp/dba-preprint-build.XXXXXX)"
trap 'rm -rf "$BUILD_DIR"' EXIT

xelatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" "$SOURCE" >/dev/null
xelatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" "$SOURCE" >/dev/null

cp "$BUILD_DIR/PREPRINT_SUBMISSION.pdf" "$OUTPUT"
echo "Wrote $OUTPUT"
