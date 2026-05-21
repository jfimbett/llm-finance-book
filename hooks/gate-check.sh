#!/bin/bash
# gate-check.sh — block commit if staged content files have scores below threshold
# Called by pre-commit-checks.sh.
# Exit 0 = pass, Exit 1 = block.
# Trigger: pre-commit

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
    SCORE_FILE="docs/quality/${SAFE}-score.json"

    if [ ! -f "$SCORE_FILE" ]; then
        echo "  ADVISORY: no quality score for $file — run /score-content first"
        continue
    fi

    # Check each dimension
    RESULT=$(python3 - "$SCORE_FILE" "$THRESHOLD" << 'PYEOF'
import json, sys
score_file = sys.argv[1]
threshold = int(sys.argv[2])
try:
    report = json.load(open(score_file))
except Exception as e:
    print(f"ERROR: could not read {score_file}: {e}")
    sys.exit(0)
scores = report.get("scores", {})
failed = False
for dim, score in scores.items():
    if score < threshold:
        print(f"FAIL: {dim} score {score} < {threshold}")
        failed = True
if not failed:
    print("PASS")
PYEOF
)
    if echo "$RESULT" | grep -q "^FAIL:"; then
        echo "$RESULT" | grep "^FAIL:" | while IFS= read -r line; do
            echo "  QUALITY GATE FAILED: $file — ${line#FAIL: }"
        done
        FAILED=$((FAILED+1))
    elif echo "$RESULT" | grep -q "^ERROR:"; then
        echo "$RESULT"
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
