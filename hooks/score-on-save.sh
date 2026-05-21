#!/bin/bash
# score-on-save.sh — remind user to run /score-content after saving content files
# Trigger: PostToolUse (Write|Edit). Reads file path from stdin JSON.
# NOTE: Full AI scoring requires the scorer agent — this hook prints a reminder.
# Exit 0 always.

# Parse file path from stdin JSON
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('file_path', d.get('path', '')))
except:
    print('')
" 2>/dev/null || echo "")

if [ -z "$FILE" ]; then
    exit 0
fi

# Only process content files (.tex and .md)
case "$FILE" in
    *.tex|*.md) ;;
    *) exit 0 ;;
esac

# Skip non-content directories
case "$FILE" in
    .claude/*|scripts/*|hooks/*|docs/superpowers/*|docs/STATUS.md|docs/SESSION_LOG.md) exit 0 ;;
esac

# Skip placeholder files
if [ -f "$FILE" ] && grep -q "invoke /draft-" "$FILE" 2>/dev/null; then
    exit 0
fi

# Check if a quality report already exists for this file
SAFE=$(echo "$FILE" | sed 's/\.[^.]*$//' | tr '/' '_')
REPORT="docs/quality/${SAFE}-score.json"

if [ ! -f "$REPORT" ]; then
    echo ""
    echo "TIP: No quality score yet for $(basename $FILE). Run: /score-content $FILE"
else
    # Check if it still passes
    PASS=$(python3 -c "import json; d=json.load(open('$REPORT')); print('PASS' if d.get('pass', False) else 'FAIL')" 2>/dev/null || echo "UNKNOWN")
    echo "Quality: $PASS — $(basename $FILE) (run /score-content to refresh)"
fi

exit 0
