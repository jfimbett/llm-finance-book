#!/bin/bash
# score-report.sh — print quality score table from all docs/quality/ JSON files
# Usage: bash scripts/score-report.sh

if [ ! -d "docs/quality" ] || [ -z "$(ls docs/quality/*-score.json 2>/dev/null)" ]; then
    echo "No quality reports found in docs/quality/"
    exit 0
fi

printf "%-45s %7s %6s %12s %9s %6s %8s\n" "File" "Clarity" "Rigor" "Completeness" "Pedagogy" "Style" "Status"
printf "%-45s %7s %6s %12s %9s %6s %8s\n" "$(printf '%0.s-' {1..45})" "-------" "------" "------------" "---------" "------" "--------"

for report in docs/quality/*-score.json; do
    [ -f "$report" ] || continue
    python3 << PYEOF
import json
with open("$report") as f:
    d = json.load(f)
file_short = d.get("file", "$report")
if len(file_short) > 44:
    file_short = "..." + file_short[-41:]
s = d.get("scores", {})
status = "PASS" if d.get("pass", False) else "FAIL"
print(f"{file_short:<45} {s.get('clarity','?'):>7} {s.get('rigor','?'):>6} {s.get('completeness','?'):>12} {s.get('pedagogy','?'):>9} {s.get('style','?'):>6} {status:>8}")
PYEOF
done
