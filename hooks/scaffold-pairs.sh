#!/bin/bash
# scaffold-pairs.sh — auto-create paired lecture/notebook when a new chapter is created
# Trigger: PostToolUse (Write). Reads file path from stdin JSON.
# Exit 0 always.

# Parse file path from stdin JSON
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('file_path', d.get('path', '')))
except:
    print('')
" 2>/dev/null || echo "")

# Only act on new chapter.tex files
if [[ ! "$FILE" =~ book/chapters/([0-9]{2}-[^/]+)/chapter\.tex$ ]]; then
    exit 0
fi

DIRNAME="${BASH_REMATCH[1]}"
NUM="${DIRNAME:0:2}"
NAME="${DIRNAME:3}"
TITLE=$(echo "$NAME" | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')

# Create lecture dir if it doesn't exist
LECDIR="course/lectures/$DIRNAME"
if [ -d "$LECDIR" ]; then
    exit 0
fi

mkdir -p "$LECDIR"

# Create placeholder lecture files
cat > "$LECDIR/notes.md" << EOF
# Lecture ${NUM}: ${TITLE}

**Paired chapter:** \`book/chapters/$DIRNAME/chapter.tex\`
**Learning objectives:**
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## 1. Motivation

[Placeholder — invoke /draft-lecture to generate]

## 2. Core Concepts

[Placeholder]

## 3. Summary

[Placeholder]
EOF

cat > "$LECDIR/slides.tex" << EOF
\\documentclass{beamer}
\\usetheme{Madrid}
\\usepackage{amsmath, amssymb}
\\title{Lecture ${NUM}: ${TITLE}}
\\author{AUTHOR NAME}
\\institute{INSTITUTION}
\\date{\\today}
\\begin{document}
\\begin{frame}\\titlepage\\end{frame}
\\begin{frame}{Placeholder}
  Invoke /draft-lecture to generate slides.
\\end{frame}
\\end{document}
EOF

printf "**Exercise placeholder**\n\n[Invoke /draft-exercises to generate]\n" > "$LECDIR/exercises.md"

cat > "${LECDIR}/solutions.md" << PLACEHOLDER
# Solutions — Lecture ${NUM}: ${TITLE}

> Placeholder — replace with actual solutions.
PLACEHOLDER

# Create notebook dir
NBDIR="code/notebooks/$DIRNAME"
mkdir -p "$NBDIR"
cat > "$NBDIR/demo.ipynb" << 'EOF'
{"cells":[{"cell_type":"markdown","id":"aa000001","metadata":{},"source":["# Demo\n\nInvoke `/draft-code` to generate this notebook."]}],"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.9.0"}},"nbformat":4,"nbformat_minor":5}
EOF

echo "Auto-scaffolded lecture and notebook for $DIRNAME"

# Stage new files
git add "$LECDIR" "$NBDIR" 2>/dev/null || true

# Update book/main.tex to include the new chapter
MAIN_TEX="book/main.tex"
if [ -f "$MAIN_TEX" ]; then
  DIR_SEGMENT="$DIRNAME"
  INCLUDE_LINE="\\\\include{chapters/${DIR_SEGMENT}/chapter}"
  # Only add if not already present
  if ! grep -q "include{chapters/${DIR_SEGMENT}/chapter}" "$MAIN_TEX"; then
    sed -i.bak "s|% Add new chapters here|${INCLUDE_LINE}\n% Add new chapters here|" "$MAIN_TEX" 2>/dev/null \
      && rm -f "${MAIN_TEX}.bak" || true
    git add "$MAIN_TEX" 2>/dev/null || true
  fi
fi

exit 0
