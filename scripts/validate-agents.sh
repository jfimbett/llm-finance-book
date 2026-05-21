#!/bin/bash
# validate-agents.sh — checks all 21 agent files exist and have required sections

PASS=0
FAIL=0

check_agent() {
  local name="$1"
  local path=".claude/agents/${name}.md"

  if [ ! -f "$path" ]; then
    echo "  MISS  $path"
    FAIL=$((FAIL+1))
    return
  fi

  local ok=1
  for section in "## Persona" "## Inputs" "## What to Do" "## Output Format" "## Scope Limits"; do
    if ! grep -q "$section" "$path"; then
      echo "  NO_SECTION  ${name}: missing '${section}'"
      FAIL=$((FAIL+1))
      ok=0
    fi
  done

  if [ "$ok" -eq 1 ]; then
    echo "  OK  $name"
    PASS=$((PASS+1))
  fi
}

check_agent "book-writer"
check_agent "lecture-writer"
check_agent "exercise-designer"
check_agent "figure-designer"
check_agent "code-writer"
check_agent "literature-reviewer"
check_agent "math-checker"
check_agent "statistics-reviewer"
check_agent "fact-checker"
check_agent "code-reviewer"
check_agent "editor"
check_agent "humanizer"
check_agent "proofreader"
check_agent "pedagogy-reviewer"
check_agent "accessibility-reviewer"
check_agent "consistency-checker"
check_agent "cross-ref-checker"
check_agent "structure-reviewer"
check_agent "scorer"
check_agent "critic"
check_agent "peer-reviewer"

echo ""
echo "Result: $PASS passed, $FAIL issues"
[ "$FAIL" -eq 0 ] && echo "All agents valid." || exit 1
