#!/bin/bash
# notify-threshold.sh — print banner when a file first passes all quality dimensions
# Trigger: PostToolUse after score-content writes a new report.
# Exit 0 always.

# Look for quality reports updated in the last commit
UPDATED_REPORTS=$(git diff --name-only HEAD~1..HEAD 2>/dev/null | grep 'docs/quality/.*-score\.json' || true)

if [ -z "$UPDATED_REPORTS" ]; then
    exit 0
fi

while IFS= read -r report; do
    [ -f "$report" ] || continue

    # Check if currently passing
    PASS=$(python3 -c "
import json
try:
    d = json.load(open('$report'))
    print('true' if d.get('pass', False) else 'false')
except:
    print('false')
" 2>/dev/null || echo "false")

    if [ "$PASS" != "true" ]; then
        continue
    fi

    # Check if this is the FIRST time it passed (previous version had pass=false or didn't exist)
    PREV_PASS=$(git show HEAD~1:"$report" 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print('true' if d.get('pass', False) else 'false')
except:
    print('false')
" 2>/dev/null || echo "false")

    if [ "$PREV_PASS" = "true" ]; then
        continue
    fi

    # Extract chapter name from report filename
    CHAPTER=$(basename "$report" | sed 's/-score\.json//' | tr '_' '/')
    OVERALL=$(python3 -c "import json; d=json.load(open('$report')); print(d.get('overall', 0))" 2>/dev/null || echo "?")

    echo ""
    echo "============================================"
    echo "  QUALITY GATE PASSED: $CHAPTER"
    echo "  Overall score: $OVERALL/10"
    echo "  All dimensions meet threshold."
    echo "  Ready to run /release-chapter"
    echo "============================================"
    echo ""

done <<< "$UPDATED_REPORTS"

exit 0
