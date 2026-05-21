#!/bin/bash
# check-latex.sh — verify LaTeX compiles before commit (pre-commit integrity check)
# Called by pre-commit-checks.sh when a git commit is detected.
# Exit 0 = OK, Exit 1 = block commit

set -euo pipefail

if [ ! -f "book/main.tex" ]; then
    exit 0
fi

# Only run if there are staged .tex files
if ! git diff --cached --name-only | grep -q '\.tex$'; then
    exit 0
fi

echo "Checking LaTeX compilation..."

# Run pdflatex in draft mode (no PDF output) from book/ directory
cd book
if ! pdflatex -draftmode -interaction=nonstopmode main.tex > /dev/null 2>&1; then
    echo "LaTeX check: FAIL"
    grep "^! " main.log 2>/dev/null | head -20
    echo ""
    echo "Commit blocked: fix LaTeX errors first (see book/main.log)"
    exit 1
fi
cd ..

echo "LaTeX check: OK"
exit 0
