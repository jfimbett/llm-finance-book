#!/bin/bash
# auto-commit.sh — auto-commit file writes when auto_commit=true in TOPIC.md
# Trigger: PostToolUse (Write|Edit). Reads file path from stdin JSON.
# Exit 0 always (errors are non-fatal for auto-commit)

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

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    exit 0
fi

# Check auto_commit setting
AUTO=$(grep 'auto_commit:' TOPIC.md 2>/dev/null | sed 's/auto_commit://' | tr -d ' \r\n')
if [ "$AUTO" != "true" ]; then
    exit 0
fi

# Skip non-content files
case "$FILE" in
    .claude/*|scripts/*|hooks/*|docs/superpowers/*) exit 0 ;;
    docs/quality/*|docs/STATUS.md|docs/SESSION_LOG.md|TOPIC.md) exit 0 ;;
esac

# Determine commit type/scope from file path
SCOPE="misc"
TYPE="feat"
if [[ "$FILE" =~ book/chapters/([0-9]{2})- ]]; then
    SCOPE="ch${BASH_REMATCH[1]}"
elif [[ "$FILE" =~ course/lectures/([0-9]{2})- ]]; then
    SCOPE="lec${BASH_REMATCH[1]}"
elif [[ "$FILE" =~ code/notebooks/([0-9]{2})- ]] || [[ "$FILE" =~ code/src/ ]]; then
    NUM=$(echo "$FILE" | grep -o '[0-9][0-9]-' | head -1 | tr -d '-' || echo "")
    SCOPE="code${NUM:-}"
    TYPE="feat"
elif [[ "$FILE" =~ \.claude/agents/ ]]; then
    SCOPE="agents"; TYPE="chore"
elif [[ "$FILE" =~ \.claude/skills/ ]]; then
    SCOPE="skills"; TYPE="chore"
elif [[ "$FILE" =~ \.claude/hooks/ ]]; then
    SCOPE="hooks"; TYPE="chore"
fi

BASENAME=$(basename "$FILE")
MSG="${TYPE}(${SCOPE}): update ${BASENAME}"

# Stage and commit (silently if nothing to commit)
git add "$FILE" 2>/dev/null || true
git diff --cached --quiet 2>/dev/null && exit 0
git commit -m "$MSG" 2>/dev/null || true

exit 0
