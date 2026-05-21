#!/bin/bash
# validate-scaffold.sh — verifies the scaffold is complete
# Run: bash scripts/validate-scaffold.sh

PASS=0
FAIL=0

check() {
  if [ -e "$1" ]; then
    echo "  OK  $1"
    PASS=$((PASS+1))
  else
    echo "MISS  $1"
    FAIL=$((FAIL+1))
  fi
}

echo "=== Scaffold Validation ==="

# Core config
check "TOPIC.md"
check "README.md"
check ".gitignore"

# Claude config
check ".claude/CLAUDE.md"
check ".claude/settings.json"
check ".claude/agents"
check ".claude/skills"
check ".claude/hooks"

# Book
check "book/main.tex"
check "book/preamble.tex"
check "book/bibliography.bib"
check "book/chapters/01-intro/chapter.tex"

# Course
check "course/lectures/01-intro/notes.md"
check "course/lectures/01-intro/slides.tex"
check "course/lectures/01-intro/exercises.md"
check "course/lectures/01-intro/solutions.md"

# Code
check "code/src/__init__.py"
check "code/notebooks/01-intro/demo.ipynb"
check "code/requirements.txt"
check "code/tests/__init__.py"

# Docs
check "docs/STATUS.md"
check "docs/SESSION_LOG.md"
check "docs/quality"

echo ""
echo "Result: $PASS passed, $FAIL missing"
[ "$FAIL" -eq 0 ] && echo "Scaffold complete." || exit 1
