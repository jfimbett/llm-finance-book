#!/bin/bash
# check-refs.sh — scan for undefined LaTeX references in staged files
# Exit 0 = OK, Exit 1 = block commit
# Trigger: pre-commit

set -euo pipefail

STAGED_TEX=$(git diff --cached --name-only | grep '\.tex$' || true)
if [ -z "$STAGED_TEX" ]; then
    exit 0
fi

echo "Checking LaTeX references..."

# Collect all \label{KEY} definitions from entire book/
ALL_LABELS=$(grep -rho '\\label{[^}]*}' book/ 2>/dev/null | sed 's/.*\\label{//;s/}//' | sort -u || true)

BROKEN=0
while IFS= read -r file; do
    [ -f "$file" ] || continue
    # Extract all \ref{} and \eqref{} usages
    while IFS= read -r key; do
        if ! echo "$ALL_LABELS" | grep -qx "$key"; then
            echo "  Undefined ref: \\ref{$key} in $file"
            BROKEN=$((BROKEN+1))
        fi
    done < <(grep -oh '\\[a-zA-Z]*ref{[^}]*}' "$file" 2>/dev/null | sed 's/.*{//;s/}//' || true)
done <<< "$STAGED_TEX"

if [ "$BROKEN" -gt 0 ]; then
    echo "Reference check: FAIL ($BROKEN undefined references)"
    exit 1
fi

echo "Reference check: OK"
exit 0
