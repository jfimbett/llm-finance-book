#!/usr/bin/env bash
# timed-commit.sh — safety-net commit when enough time has passed.
#
# Teaching hook for Practical 4 (LLM Agents). Wired to the Claude Code "Stop"
# event so it runs at the end of each assistant turn:
#   "Stop": [{ "hooks": [{ "type": "command",
#       "command": ".claude/hooks/timed-commit.sh" }]}]
#
# Logic: if the working tree is dirty AND the last commit is older than
# COMMIT_INTERVAL_MIN minutes, stage everything and commit. Otherwise do
# nothing. Always exits 0 so it never blocks the session.
#
# All git operations are scoped to THIS practical folder (the "-- ." pathspec),
# so it behaves identically whether the folder is its own repo or nested inside a
# larger monorepo: it only ever stages and commits files under this directory.
#
# Cline has no event hooks — see templates/cline/git-hooks-README.md for the
# portable watch-loop / cron fallback that reuses this same script.

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." 2>/dev/null && pwd)}"
cd "$ROOT" 2>/dev/null || exit 0

# Consume any stdin payload so the hook never sees a broken pipe.
cat >/dev/null 2>&1 || true

COMMIT_INTERVAL_MIN="${COMMIT_INTERVAL_MIN:-15}"

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

# Nothing changed *in this folder*? Stop. (scoped with the "-- ." pathspec)
if [ -z "$(git status --porcelain -- . 2>/dev/null)" ]; then
    exit 0
fi

NOW="$(date +%s 2>/dev/null || echo 0)"
LAST="$(git log -1 --format=%ct -- . 2>/dev/null || echo 0)"   # last commit touching this folder
ELAPSED_MIN=$(( (NOW - LAST) / 60 ))

# No commit has touched this folder yet (LAST=0) also triggers a first safety commit.
if [ "$LAST" -ne 0 ] && [ "$ELAPSED_MIN" -lt "$COMMIT_INTERVAL_MIN" ]; then
    exit 0
fi

git add -A -- . 2>/dev/null || true
# Stop if nothing under this folder is staged.
git diff --cached --quiet -- . 2>/dev/null && exit 0

STAMP="$(date '+%Y-%m-%d %H:%M' 2>/dev/null || echo now)"
# The "-- ." pathspec commits only this folder's changes, ignoring anything
# staged elsewhere in a surrounding monorepo.
git commit -m "chore: timed safety commit (${STAMP})" -- . >/dev/null 2>&1 || true
exit 0
