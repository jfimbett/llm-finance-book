#!/usr/bin/env bash
# Regenerate book figures from the AUTHOR "figures" track.
#
# Each chapter's deterministic generators live in code/figures/<chapter>/gen_*.py
# and write straight into book/chapters/<chapter>/figures/. They are network-free
# where possible; a few (gensim GloVe, live SEC EDGAR) need internet on first run
# and then cache locally.
#
# Usage (from the repo root):
#   pip install -e code            # makes the shared `llmfin` package importable
#   bash code/build_figures.sh     # all chapters
#   bash code/build_figures.sh 01-intro   # one chapter
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$ROOT/code/src:${PYTHONPATH:-}"
GLOB="${1:-*}"

shopt -s nullglob
fail=0
found=0
for gen in "$ROOT"/code/figures/$GLOB/gen_*.py; do
  found=1
  echo "→ $(basename "$(dirname "$gen")")/$(basename "$gen")"
  if ! python3 "$gen"; then
    echo "   [FAILED] $gen"
    fail=1
  fi
done

[ "$found" -eq 0 ] && { echo "No generators matched code/figures/$GLOB/gen_*.py"; exit 1; }
[ "$fail" -eq 0 ] && echo "All figure generators completed." || echo "Some generators failed (see above)."
exit $fail
