#!/bin/bash
# notify-threshold.sh — print banner when a file first passes all quality dimensions
# Trigger: PostToolUse after score-content writes a new report.
# Exit 0 always.

# Read the file path from stdin JSON (PostToolUse hook)
FILE=$(python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('file_path', d.get('path', '')))" 2>/dev/null || echo "")

# Only process docs/quality/*-score.json files
case "$FILE" in
    docs/quality/*-score.json) ;;
    *) exit 0 ;;
esac

[ -f "$FILE" ] || exit 0

# Check if the current file on disk has pass: true
PASS=$(python3 -c "
import json
try:
    d = json.load(open('$FILE'))
    print('true' if d.get('pass', False) else 'false')
except:
    print('false')
" 2>/dev/null || echo "false")

if [ "$PASS" != "true" ]; then
    exit 0
fi

# Check if the previous git version had pass: false (or didn't exist)
PREV_PASS=$(git show "HEAD:${FILE}" 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read())
    print('true' if d.get('pass', False) else 'false')
except: print('false')
" || echo "false")

if [ "$PREV_PASS" = "true" ]; then
    exit 0
fi

# First time passing — print banner
CHAPTER=$(basename "$FILE" | sed 's/-score\.json//' | tr '_' '/')
OVERALL=$(python3 -c "import json; d=json.load(open('$FILE')); print(d.get('overall', 0))" 2>/dev/null || echo "?")

echo ""
echo "============================================"
echo "  QUALITY GATE PASSED: $CHAPTER"
echo "  Overall score: $OVERALL/10"
echo "  All dimensions meet threshold."
echo "  Ready to run /release-chapter"
echo "============================================"
echo ""

exit 0
