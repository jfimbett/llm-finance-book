#!/usr/bin/env bash
# Build web PNGs for chapters that have a matplotlib generator or an existing figure PDF.
# Inline-SVG chapters (03 04 06 14 16 17) are authored by hand, not here.
set -u
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
OUT_ROOT="$ROOT/course/slides-html/assets/figures"

for ch in 01-intro 02-llm-foundations 05-business-valuation 07-applications-future \
          08-domain-specific-llms 09-financial-nlp-sentiment 10-portfolio-quant-trading \
          11-regtech-compliance-aml 12-xai-explainability 13-llm-limitations-evaluation \
          15-privacy-local-models; do
  out="$OUT_ROOT/$ch"; mkdir -p "$out"
  nbdir="$ROOT/code/notebooks/$ch"
  if compgen -G "$nbdir/gen_*.py" > /dev/null; then
    for g in "$nbdir"/gen_*.py; do
      echo "RUN  $ch/$(basename "$g")"
      ( cd "$nbdir" && python3 "$(basename "$g")" ) || echo "WARN generator failed: $g"
    done
  fi
  # collect any PNGs the generators wrote into the book figures dir
  figdir="$ROOT/book/chapters/$ch/figures"
  if compgen -G "$figdir/*.png" > /dev/null; then cp -f "$figdir"/*.png "$out"/; fi
  # fallback: convert any figure PDF (except the generic illustration) to PNG
  if compgen -G "$figdir"/*.pdf > /dev/null; then
    for pdf in "$figdir"/*.pdf; do
      base="$(basename "${pdf%.pdf}")"
      [ "$base" = "fig_illustration" ] && continue
      [ -f "$out/$base.png" ] && continue
      echo "CONV $ch/$base.pdf -> png"
      pdftoppm -png -r 160 -singlefile "$pdf" "$out/$base"
    done
  fi
  echo "DONE $ch -> $(ls "$out" 2>/dev/null | tr '\n' ' ')"
done
