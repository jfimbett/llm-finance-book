---
name: compare
description: Run a finance text task through the general and finance-domain classifiers, score both against gold labels, and report which wins and why. Usage /compare
---

# /compare

Run the general-vs-domain comparison and save a grounded report.

1. **Baseline** (generalist agent):
   `python -m tools.general`
   Record the general-purpose accuracy and the sentences it missed.
2. **Domain** (specialist agent):
   `python -m tools.domain`
   Record the finance-domain accuracy and the sentences it flipped.
3. **Adjudicate** (adjudicator agent):
   `python -m tools.compare --json`
   This is the source of truth: `general_accuracy`, `domain_accuracy`, `winner`,
   `margin`, and `domain_wins` (each with its `deciding_terms`).
4. **Write the verdict.** State both accuracies and the winner, then explain the gap by
   citing the deciding finance terms from `domain_wins` — e.g. the general lexicon scoring
   `beat` as negative, never seeing `headwinds`/`impairment`, and misreading `liability`
   as negative. Every number and term must come from step 3's output; cite nothing else.
5. **Save** to `reports/compare.md`:
   - both accuracies and the winner with its margin,
   - the table of sentences the domain classifier won, with the deciding terms,
   - one sentence on why domain adaptation helped on this finance text.

Run it on a single sentence instead:
- `python -m tools.general "Revenue beat guidance and margins expanded."`
- `python -m tools.domain "Revenue beat guidance and margins expanded."`
  The two labels disagree on `beat` — the smallest version of the whole point.
