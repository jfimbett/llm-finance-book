#!/bin/bash
# check-bib.sh — validate BibTeX entries have required fields
# Exit 0 = OK, Exit 1 = block commit

set -euo pipefail

BIB="book/bibliography.bib"
if [ ! -f "$BIB" ]; then
    exit 0
fi

# Only run if .bib or .tex files are staged
if ! git diff --cached --name-only | grep -qE '\.(bib|tex)$'; then
    exit 0
fi

echo "Checking bibliography..."

INVALID=0
CURRENT_TYPE=""
CURRENT_KEY=""
FIELDS=""

while IFS= read -r line; do
    # Start of entry
    if [[ "$line" =~ ^@([a-zA-Z]+)\{([^,]+), ]]; then
        CURRENT_TYPE=$(echo "${BASH_REMATCH[1]}" | tr '[:upper:]' '[:lower:]')
        CURRENT_KEY="${BASH_REMATCH[2]}"
        FIELDS=""
    fi
    # Field detected
    if [[ "$line" =~ ^[[:space:]]*([a-zA-Z]+)[[:space:]]*= ]]; then
        FIELD=$(echo "${BASH_REMATCH[1]}" | tr '[:upper:]' '[:lower:]')
        FIELDS="$FIELDS $FIELD"
    fi
    # End of entry
    if [[ "$line" =~ ^\} ]] && [ -n "$CURRENT_KEY" ]; then
        REQUIRED=""
        case "$CURRENT_TYPE" in
            article)      REQUIRED="author title journal year" ;;
            book)         REQUIRED="author title publisher year" ;;
            inproceedings) REQUIRED="author title booktitle year" ;;
        esac
        for req in $REQUIRED; do
            if ! echo "$FIELDS" | grep -qw "$req"; then
                echo "  Missing '$req' in @$CURRENT_TYPE{$CURRENT_KEY}"
                INVALID=$((INVALID+1))
            fi
        done
        CURRENT_KEY=""
    fi
done < "$BIB"

if [ "$INVALID" -gt 0 ]; then
    echo "Bibliography check: FAIL ($INVALID invalid entries)"
    exit 1
fi

echo "Bibliography check: OK"
exit 0
