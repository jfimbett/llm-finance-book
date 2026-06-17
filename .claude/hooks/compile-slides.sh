#!/bin/bash
# compile-slides.sh — compile slides.tex after editing
# Trigger: PostToolUse (Write|Edit). Reads file path from stdin JSON.
# Exit 0 always (non-blocking).

INPUT=$(cat)
FILE=$(echo "$INPUT" | sed -n 's/.*"file_path" *: *"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$FILE" ]; then
    exit 0
fi

# Normalize backslashes to forward slashes (Windows paths)
FILE=$(echo "$FILE" | tr '\\' '/')

# Only trigger for slides.tex files in course/lectures/
if [[ "$FILE" =~ course/lectures/[^/]+/slides\.tex$ ]]; then
    DIR=$(dirname "$FILE")
    echo ""
    echo "Compiling slides: $DIR/slides.tex"
    (cd "$DIR" && pdflatex -interaction=nonstopmode slides.tex > /tmp/slides-compile.log 2>&1)
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "OK slides compiled: $DIR/slides.pdf"
    else
        ERROR=$(grep "^! " /tmp/slides-compile.log | head -3)
        echo "FAIL compiling $DIR/slides.tex"
        [ -n "$ERROR" ] && echo "$ERROR"
    fi
fi

exit 0
