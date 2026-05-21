#!/bin/bash
# gate-check.sh — block commit if staged content files have scores below threshold
# Called by pre-commit-checks.sh.
# Exit 0 = pass, Exit 1 = block.
# Trigger: pre-commit

set -euo pipefail

# Read threshold
THRESHOLD=$(grep 'quality_threshold:' TOPIC.md 2>/dev/null | sed 's/quality_threshold://' | tr -d ' \r\n')
THRESHOLD="${THRESHOLD:-7}"

STAGED=$(git diff --cached --name-only 2>/dev/null | grep -E '\.(tex|md)$' || true)
if [ -z "$STAGED" ]; then
    exit 0
fi

FAILED=0

while IFS= read -r file; do
    # Skip non-content files
    case "$file" in
        .claude/*|scripts/*|hooks/*|docs/superpowers/*|docs/STATUS.md|docs/SESSION_LOG.md) continue ;;
        README.md|TOPIC.md) continue ;;
    esac

    # Derive quality report path
    SAFE=$(echo "$file" | sed 's/\.[^.]*$//' | tr '/' '_')
    REPORT="docs/quality/${SAFE}-score.json"

    if [ ! -f "$REPORT" ]; then
        echo "  ADVISORY: no quality score for $file — run /score-content first"
        continue
    fi

    # Check each dimension
    python3 << PYEOF
import json, sys
threshold = int("$THRESHOLD")
report = json.load(open("$REPORT"))
scores = report.get("scores", {})
failed = False
for dim, score in scores.items():
    if score < threshold:
        print(f"  QUALITY GATE FAILED: $file — {dim} score {score} < {threshold}")
        failed = True
if failed:
    sys.exit(1)
PYEOF
    STATUS=$?
    if [ "$STATUS" -ne 0 ]; then
        FAILED=$((FAILED+1))
    fi
done <<< "$STAGED"

if [ "$FAILED" -gt 0 ]; then
    echo ""
    echo "Commit blocked: $FAILED file(s) below quality threshold ($THRESHOLD/10)"
    echo "Run /refine-until-threshold on each failing file, then retry."
    exit 1
fi

echo "Quality gate: OK (all scored files meet threshold $THRESHOLD/10)"
exit 0
