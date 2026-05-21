#!/bin/bash
# validate-hooks.sh — checks all 13 hook scripts exist and have required headers

PASS=0
FAIL=0

check_hook() {
  local name="$1"
  local path=".claude/hooks/${name}.sh"

  if [ ! -f "$path" ]; then
    echo "  MISS  $path"
    FAIL=$((FAIL+1))
    return
  fi

  if ! head -3 "$path" | grep -q "^#!/bin/bash"; then
    echo "  NO_SHEBANG  $name"
    FAIL=$((FAIL+1))
    return
  fi

  if ! grep -q "^# Trigger:" "$path"; then
    echo "  NO_TRIGGER  $name"
    FAIL=$((FAIL+1))
    return
  fi

  if ! grep -q "^# Exit" "$path"; then
    echo "  NO_EXIT  $name"
    FAIL=$((FAIL+1))
    return
  fi

  if [ ! -x "$path" ]; then
    echo "  NOT_EXECUTABLE  $name"
    FAIL=$((FAIL+1))
    return
  fi

  echo "  OK  $name"
  PASS=$((PASS+1))
}

check_hook "check-latex"
check_hook "check-refs"
check_hook "check-bib"
check_hook "check-notation"
check_hook "check-numbering"
check_hook "auto-commit"
check_hook "update-status"
check_hook "session-log"
check_hook "scaffold-pairs"
check_hook "score-on-save"
check_hook "gate-check"
check_hook "iterate"
check_hook "notify-threshold"

echo ""
echo "Result: $PASS passed, $FAIL issues"
[ "$FAIL" -eq 0 ] && echo "All hooks valid." || exit 1
