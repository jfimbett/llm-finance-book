#!/bin/bash
# build-book.sh — compile the LaTeX book to PDF
# Usage: bash scripts/build-book.sh [--open]

set -euo pipefail

if [ ! -f "book/main.tex" ]; then
    echo "Error: book/main.tex not found. Run from the repo root."
    exit 1
fi

echo "Building book..."
cd book

pdflatex -shell-escape -interaction=nonstopmode main.tex
biber main
pdflatex -shell-escape -interaction=nonstopmode main.tex
pdflatex -shell-escape -interaction=nonstopmode main.tex

# Check for errors
if grep -q "^! " main.log 2>/dev/null; then
    echo "Build FAILED. Errors:"
    grep "^! " main.log | head -20
    exit 1
fi

echo "Build succeeded: book/main.pdf"

# Open PDF if requested
if [ "${1:-}" = "--open" ]; then
    case "$(uname)" in
        Darwin) open main.pdf ;;
        Linux)  xdg-open main.pdf 2>/dev/null || echo "PDF at book/main.pdf" ;;
        MINGW*|CYGWIN*|MSYS*) start main.pdf ;;
    esac
fi

exit 0
