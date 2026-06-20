#!/usr/bin/env bash
# Regenerate all illustration figures by re-executing every exercises notebook.
# Run from the project root: bash code/run_illustrations.sh
set -e

NOTEBOOKS=(
  "code/notebooks/01-intro/exercises.ipynb"
  "code/notebooks/02-llm-foundations/exercises.ipynb"
  "code/notebooks/03-llm-training-finetuning/exercises.ipynb"
  "code/notebooks/04-llm-agents/exercises.ipynb"
  "code/notebooks/05-business-valuation/exercises.ipynb"
  "code/notebooks/06-credit-risk/exercises.ipynb"
  "code/notebooks/07-applications-future/exercises.ipynb"
)

for nb in "${NOTEBOOKS[@]}"; do
  echo "Executing $nb ..."
  jupyter nbconvert --to notebook --execute --inplace "$nb" \
    --ExecutePreprocessor.timeout=180
done

# Deterministic, network-free figure generators (preferred over live-data notebooks).
echo "Running deterministic figure generators ..."
python3 code/notebooks/05-business-valuation/gen_dcf_sensitivity.py
python3 code/notebooks/12-xai-explainability/gen_shap_attribution.py

echo "All illustration figures regenerated."
echo ""
echo "PDFs:"
ls book/chapters/*/figures/fig_illustration.pdf 2>/dev/null || echo "(none found)"
