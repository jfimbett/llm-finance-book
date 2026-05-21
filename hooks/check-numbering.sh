#!/bin/bash
# check-numbering.sh — verify chapter/lecture pairs exist (advisory, never blocks)
# Exit 0 always

echo "Checking chapter/lecture pairing..."

UNPAIRED=0

# Find all chapter numbers
for dir in book/chapters/[0-9][0-9]-*/; do
    [ -d "$dir" ] || continue
    NUM=$(basename "$dir" | cut -c1-2)
    # Check if matching lecture exists
    if ! ls -d course/lectures/${NUM}-*/ 2>/dev/null | head -1 | grep -q "${NUM}-"; then
        echo "  WARNING: chapter $NUM has no matching lecture directory"
        UNPAIRED=$((UNPAIRED+1))
    fi
done

# Find all lecture numbers
for dir in course/lectures/[0-9][0-9]-*/; do
    [ -d "$dir" ] || continue
    NUM=$(basename "$dir" | cut -c1-2)
    # Check if matching chapter exists
    if ! ls -d book/chapters/${NUM}-*/ 2>/dev/null | head -1 | grep -q "${NUM}-"; then
        echo "  WARNING: lecture $NUM has no matching chapter directory"
        UNPAIRED=$((UNPAIRED+1))
    fi
done

if [ "$UNPAIRED" -gt 0 ]; then
    echo "Numbering check: $UNPAIRED unpaired directories (advisory — not blocking)"
else
    echo "Numbering check: OK (all chapters/lectures paired)"
fi

exit 0
