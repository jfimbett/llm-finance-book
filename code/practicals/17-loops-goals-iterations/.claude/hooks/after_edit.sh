#!/usr/bin/env bash
# PostToolUse hook: runs after every Edit/Write (wired in .claude/settings.json).
#
# It re-scores the working draft against the deterministic target metric so the
# agent gets the number — and the exact list of still-missing facts — the instant
# it edits reports/draft.md. This is the "hook after each iteration": feedback is
# pushed by the harness, not pulled by the model, so the loop cannot skip the check.
#
# Never fails the edit: it only reports. The loop ends on the tools/check.py gate.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DRAFT="$ROOT/reports/draft.md"

cd "$ROOT"

if [[ -f "$DRAFT" ]]; then
  echo "[hook] scoring reports/draft.md against the target metric..."
  python3 -m tools.metric --candidate "$DRAFT" || true
else
  echo "[hook] no reports/draft.md yet — nothing to score."
fi

# Keep the deterministic tools honest on every edit.
echo "[hook] running tests..."
python3 -m pytest -q || true
