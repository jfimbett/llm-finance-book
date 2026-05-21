#!/bin/bash
# new-topic.sh — CLI scaffold for a new chapter/lecture/notebook unit
# Usage: bash scripts/new-topic.sh --number 02 --name linear-algebra

set -euo pipefail

NUM=""
NAME=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --number) NUM="$2"; shift 2 ;;
        --name)   NAME="$2"; shift 2 ;;
        *) echo "Usage: new-topic.sh --number NN --name topic-name"; exit 1 ;;
    esac
done

if [ -z "$NUM" ] || [ -z "$NAME" ]; then
    echo "Usage: bash scripts/new-topic.sh --number NN --name topic-name"
    exit 1
fi

DIRNAME="${NUM}-${NAME}"
TITLE=$(echo "$NAME" | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')

echo "Scaffolding topic: $DIRNAME ($TITLE)"

# Check for conflicts
if [ -d "book/chapters/$DIRNAME" ]; then
    echo "Error: book/chapters/$DIRNAME already exists."
    exit 1
fi

# Create directories
mkdir -p "book/chapters/$DIRNAME/figures"
mkdir -p "course/lectures/$DIRNAME"
mkdir -p "code/notebooks/$DIRNAME"

# Chapter placeholder
cat > "book/chapters/$DIRNAME/chapter.tex" << EOF
\\chapter{${TITLE}}
\\label{ch:${NAME}}

% TODO: Replace this placeholder. Invoke /draft-chapter to generate a first draft.

\\section{Motivation}
\\label{sec:${NAME}-motivation}

[Placeholder]

\\section{Core Concepts}
\\label{sec:${NAME}-core}

[Placeholder]

\\section{Summary}
\\label{sec:${NAME}-summary}

[Placeholder]
EOF

touch "book/chapters/$DIRNAME/figures/.gitkeep"

# Lecture notes placeholder
cat > "course/lectures/$DIRNAME/notes.md" << EOF
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

# Slides placeholder
cat > "course/lectures/$DIRNAME/slides.tex" << EOF
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
  Invoke /draft-lecture to fill in slides.
\\end{frame}
\\end{document}
EOF

printf "# Exercises — Lecture ${NUM}: ${TITLE}\n\n**[B]** [Beginner exercise placeholder]\n\n**[I]** [Intermediate exercise placeholder]\n\n**[A]** [Advanced exercise placeholder]\n" > "course/lectures/$DIRNAME/exercises.md"

# Notebook placeholders
cat > "code/notebooks/$DIRNAME/demo.ipynb" << 'EOF'
{"cells":[{"cell_type":"markdown","id":"bb000001","metadata":{},"source":["# Demo\n\nInvoke `/draft-code` to generate this notebook."]}],"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.9.0"}},"nbformat":4,"nbformat_minor":5}
EOF
cat > "code/notebooks/$DIRNAME/exercises.ipynb" << 'EOF'
{"cells":[{"cell_type":"markdown","id":"cc000001","metadata":{},"source":["# Exercises\n\nInvoke `/draft-code` to generate exercise stubs."]}],"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.9.0"}},"nbformat":4,"nbformat_minor":5}
EOF

# Update STATUS.md
if [ -f "docs/STATUS.md" ]; then
    echo "| $NUM | $TITLE | No | No | — | — | — | — | — | No |" >> "docs/STATUS.md"
fi

# Update main.tex to include chapter
sed -i.bak "s|% Add new chapters here:.*|\\\\include{chapters/${DIRNAME}/chapter}\n% Add new chapters here: \\\\include{chapters/NN-name/chapter}|" book/main.tex 2>/dev/null && rm -f book/main.tex.bak || true

echo "Scaffolded: $DIRNAME"
git add "book/chapters/$DIRNAME" "course/lectures/$DIRNAME" "code/notebooks/$DIRNAME" "docs/STATUS.md" "book/main.tex" 2>/dev/null || true
git commit -m "chore: scaffold topic $DIRNAME" 2>/dev/null || true

echo "Done. Next: /draft-chapter $DIRNAME"

exit 0
