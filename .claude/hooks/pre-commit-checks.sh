#!/bin/bash
# pre-commit-checks.sh — intercepts git commit calls and runs integrity/quality checks
# Called by PreToolUse hook on any Bash command.
# Reads tool input from stdin to check if this is a git commit operation.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('command', ''))" 2>/dev/null || echo "")

# Only run on git commit commands
if [[ "$COMMAND" != *"git commit"* ]]; then
    exit 0
fi

# Each check script exits 1 to block the commit on failure.
for script in \
    .claude/hooks/check-latex.sh \
    .claude/hooks/check-refs.sh \
    .claude/hooks/check-bib.sh \
    .claude/hooks/check-notation.sh \
    .claude/hooks/check-numbering.sh \
    .claude/hooks/gate-check.sh; do
    if [ -f "$script" ]; then
        bash "$script" || exit 1
    fi
done

exit 0
