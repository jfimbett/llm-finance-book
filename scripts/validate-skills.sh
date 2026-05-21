#!/bin/bash
# validate-skills.sh — checks all 22 skill files exist and have required sections

PASS=0
FAIL=0

check_skill() {
  local name="$1"
  local path=".claude/skills/${name}.md"

  if [ ! -f "$path" ]; then
    echo "  MISS  $path"
    FAIL=$((FAIL+1))
    return
  fi

  local ok=1
  for section in "## Purpose" "## When to Invoke" "## Inputs Required" "## Steps" "## Expected Output" "## Error Handling"; do
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

check_skill "new-topic"
check_skill "draft-chapter"
check_skill "draft-lecture"
check_skill "draft-exercises"
check_skill "draft-figures"
check_skill "draft-code"
check_skill "score-content"
check_skill "critique"
check_skill "peer-review"
check_skill "refine-until-threshold"
check_skill "full-review"
check_skill "audit-notation"
check_skill "audit-cross-refs"
check_skill "sync-lecture-chapter"
check_skill "audit-bibliography"
check_skill "build-book"
check_skill "build-slides"
check_skill "release-chapter"
check_skill "commit-progress"
check_skill "session-summary"
check_skill "topic-status"
check_skill "interview-me"

echo ""
echo "Result: $PASS passed, $FAIL issues"
[ "$FAIL" -eq 0 ] && echo "All skills valid." || exit 1
