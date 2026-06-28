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

# Create HTML slide deck stubs (lesson + practical) per course/slides-html/AUTHORING.md
SLIDEDIR="course/slides-html/$DIRNAME"
LECNUM=$((10#$NUM))
mkdir -p "$SLIDEDIR"
for DECK in index practical; do
  if [ "$DECK" = "index" ]; then DTITLE="Lecture ${NUM}: ${TITLE}"; KIND="Lecture"; else DTITLE="Practical ${NUM}: ${TITLE}"; KIND="Practical session"; fi
  cat > "$SLIDEDIR/$DECK.html" << HTMLEOF
<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${DTITLE}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<link rel="stylesheet" href="../assets/slides.css">
<script>window.DECK_META = { course: "LLM in Finance", lecture: ${LECNUM} };</script>
<script defer src="../assets/slides.js"></script>
</head><body><div class="deck"><div class="stage">
  <section class="slide title-slide current">
    <div class="kicker">Large Language Models in Finance · ${KIND} ${LECNUM}</div>
    <h1>${TITLE}</h1>
    <div class="sub">Placeholder deck — invoke /draft-lecture to generate.</div>
    <span class="badge">Summer school · math one click away — press <b>m</b> or click ⚙ "Under the hood"</span>
  </section>
  <section class="slide section-slide">
    <div class="secnum">01</div>
    <h2>Section title</h2>
    <div class="secsub">Invoke /draft-lecture to populate this deck from book/chapters/$DIRNAME/chapter.tex (follow course/slides-html/AUTHORING.md).</div>
  </section>
</div></div></body></html>
HTMLEOF
done

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
git add "$LECDIR" "$NBDIR" "$SLIDEDIR" 2>/dev/null || true

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
