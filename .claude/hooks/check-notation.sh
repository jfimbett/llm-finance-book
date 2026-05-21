#!/bin/bash
# check-notation.sh — advisory check for undefined math commands (WARNING only, never blocks)
# Exit 0 always

STAGED_TEX=$(git diff --cached --name-only | grep '\.tex$' || true)
if [ -z "$STAGED_TEX" ]; then
    exit 0
fi

# Known standard LaTeX math commands (not exhaustive but covers common usage)
STANDARD='\frac \sum \int \prod \lim \sup \inf \min \max \mathbb \mathcal \mathrm \mathbf \text \left \right \cdot \ldots \dots \alpha \beta \gamma \delta \epsilon \zeta \eta \theta \iota \kappa \lambda \mu \nu \xi \pi \rho \sigma \tau \upsilon \phi \chi \psi \omega \Gamma \Delta \Theta \Lambda \Xi \Pi \Sigma \Upsilon \Phi \Psi \Omega \partial \nabla \infty \in \notin \subset \subseteq \cup \cap \setminus \emptyset \forall \exists \neg \wedge \vee \implies \iff \leq \geq \neq \approx \equiv \sim \perp \parallel \times \otimes \oplus \to \leftarrow \mapsto \hat \bar \tilde \vec \dot \ddot'

# Collect defined commands from preamble.tex
DEFINED=""
if [ -f "book/preamble.tex" ]; then
    DEFINED=$(grep -oh '\\newcommand{\\[^}]*}' book/preamble.tex 2>/dev/null | sed 's/\\newcommand{//;s/}//' || true)
fi

WARNINGS=0
while IFS= read -r file; do
    [ -f "$file" ] || continue
    # Find commands in math mode (simple heuristic: lines containing $...$ or \[...\])
    USED_COMMANDS=$(grep -oh '\\[a-zA-Z]*' "$file" 2>/dev/null | sort -u || true)
    while IFS= read -r cmd; do
        [ -z "$cmd" ] && continue
        if ! echo "$STANDARD" | grep -qw "$cmd" && ! echo "$DEFINED" | grep -qw "$cmd"; then
            echo "  NOTATION WARNING: unknown command '$cmd' in $file"
            WARNINGS=$((WARNINGS+1))
        fi
    done <<< "$USED_COMMANDS"
done <<< "$STAGED_TEX"

if [ "$WARNINGS" -gt 0 ]; then
    echo "Notation check: $WARNINGS warnings (advisory — not blocking)"
fi

exit 0
