#!/usr/bin/env bash
# log-interaction.sh — append one timestamped line per LLM interaction.
#
# Teaching hook for Practical 4 (LLM Agents). It turns the abstract "audit
# hook" from the lecture into a real, tamper-evident trail of what the model
# saw and did.
#
# Claude Code wiring (.claude/settings.json):
#   "UserPromptSubmit": [{ "hooks": [{ "type": "command",
#       "command": ".claude/hooks/log-interaction.sh" }]}],
#   "PostToolUse":      [{ "hooks": [{ "type": "command",
#       "command": ".claude/hooks/log-interaction.sh" }]}]
#
# Claude Code passes a JSON event object on stdin. We record the event name
# and a short, human-readable summary, then always exit 0 so a logging
# failure never interrupts the session.

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." 2>/dev/null && pwd)}"
cd "$ROOT" 2>/dev/null || exit 0

LOG_DIR="logs"
LOG_FILE="$LOG_DIR/llm-interactions.log"
mkdir -p "$LOG_DIR" 2>/dev/null || exit 0

TS="$(date '+%Y-%m-%dT%H:%M:%S%z' 2>/dev/null || echo unknown)"
PAYLOAD="$(cat 2>/dev/null || true)"

read -r -d '' PYSCRIPT <<'PY' || true
import sys, json
data = sys.stdin.read()
try:
    d = json.loads(data)
except Exception:
    print("(no structured payload)")
    sys.exit(0)
event = d.get("hook_event_name", "event")
if "prompt" in d:                                  # UserPromptSubmit
    p = " ".join(str(d["prompt"]).split())
    print("%s | prompt: %s" % (event, p[:160]))
elif "tool_name" in d:                             # Pre/PostToolUse
    ti = d.get("tool_input", {}) or {}
    detail = ti.get("file_path") or ti.get("command") or ti.get("pattern") or ""
    detail = " ".join(str(detail).split())
    print(("%s | tool: %s %s" % (event, d.get("tool_name", ""), detail[:120])).rstrip())
else:
    print(event)
PY

SUMMARY="$(printf '%s' "$PAYLOAD" | python3 -c "$PYSCRIPT" 2>/dev/null || echo '(unparsed)')"
printf '%s | %s\n' "$TS" "$SUMMARY" >> "$LOG_FILE"
exit 0
