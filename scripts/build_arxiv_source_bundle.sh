#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAGING="$(mktemp -d /tmp/dba-arxiv-src.XXXXXX)"
OUT="${1:-/tmp/dormant-behavior-audit-arxiv-source-$(date +%Y%m%d).tar.gz}"

trap 'rm -rf "$STAGING"' EXIT

cp "$ROOT/findings/PREPRINT_SUBMISSION.tex" "$STAGING/"

cat > "$STAGING/00README.XXX" <<'EOF'
Main file: PREPRINT_SUBMISSION.tex
Compiler: xelatex

This upload bundle is the public preprint source for:
"Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit"
EOF

tar -C "$STAGING" -czf "$OUT" PREPRINT_SUBMISSION.tex 00README.XXX
echo "Wrote $OUT"
