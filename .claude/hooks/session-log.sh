#!/bin/bash
# session-log.sh — append one-line session summary to docs/SESSION_LOG.md
# Trigger: Stop (session end).
# Exit 0 always.

# Anchor to the project root so relative paths work regardless of the hook's cwd.
ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." 2>/dev/null && pwd)}"
cd "$ROOT" 2>/dev/null || exit 0

LOGFILE="docs/SESSION_LOG.md"
DATE=$(date +%Y-%m-%d 2>/dev/null || echo "unknown")

# Count changed files (approximate: last 10 commits or since session start)
FILES=$(git diff --name-only HEAD~5..HEAD 2>/dev/null | wc -l | tr -d ' ' || echo "0")

# Get last 3 commit subjects
COMMITS=$(git log --oneline -3 --format="%s" 2>/dev/null | tr '\n' '; ' | sed 's/; $//' || echo "no commits")

# Append to log
if [ ! -f "$LOGFILE" ]; then
    printf "# Session Log\n\n> Auto-appended by session-log.sh.\n\n| Date | Files Changed | Recent Commits | Open Items |\n|------|---------------|----------------|------------|\n" > "$LOGFILE"
fi

printf "| %s | %s files | %s | — |\n" "$DATE" "$FILES" "$COMMITS" >> "$LOGFILE"

# Commit the log update silently
git add "$LOGFILE" 2>/dev/null || true
git diff --cached --quiet 2>/dev/null || git commit -m "chore: session log $DATE" 2>/dev/null || true

exit 0
