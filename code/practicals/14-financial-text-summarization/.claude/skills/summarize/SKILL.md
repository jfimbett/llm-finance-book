---
name: summarize
description: Extract structured fields from the bundled filing, write a grounded summary, grade it, and save a report. Usage /summarize
---

# /summarize

Run the full Extract → Summarize → Grade → Check loop and save a report.

1. **Extract** (extractor agent):
   `python -m tools.extract > reports/_fields.json`
   If `schema_errors` is non-empty, stop and report — do not summarize an invalid extraction.
2. **Summarize** (summarizer agent): write a grounded summary from `reports/_fields.json`,
   citing the field name behind every figure, and save it to `reports/_summary.txt`.
3. **Grade** (grader agent):
   `python -m tools.grade --summary-file reports/_summary.txt`
4. **Gate**: if `figure_coverage < 1.0`, remove or correct the `unsupported_figures` and
   re-grade; if `faithfulness < 0.7`, tighten the summary to the extracted fields. Loop at
   most 3 times.
5. **Save** to `reports/summary.md`:
   - the extracted fields and their source spans,
   - the final summary with field citations,
   - the two scores and the verdict.

Try this to start:
- `/summarize`  → summarises the bundled Orion Dynamics Q3 FY2025 release.

To see the faithfulness check bite, make the summarizer state a figure that is not in
`reports/_fields.json` (e.g. revenue of $2.30 billion) and re-grade: `figure_coverage`
drops below 1.0 and the loop sends it back.
