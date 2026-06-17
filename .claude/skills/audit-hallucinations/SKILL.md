# /audit-hallucinations

## Purpose

Detect hallucinations across every book chapter — fabricated statistics, phantom benchmarks, invented regulations, synthetic data presented as real, and non-existent code dependencies — using the hallucination-detector agent in parallel across all chapters.

## When to Invoke

- Before any chapter release
- After AI-assisted drafting of new chapters
- As part of the final pre-publication audit

## Inputs Required

- All `book/chapters/*/chapter.tex` files (collected automatically)
- Corresponding `code/notebooks/*/exercises.ipynb` files (matched by chapter number, included when present)

## Steps

1. **Discover chapters**
   Collect all `chapter.tex` paths by globbing `book/chapters/*/chapter.tex`, sorted by chapter number. If none exist, print "No chapters found — run /draft-chapter first" and exit.

2. **Ensure output directory**
   Create `docs/quality/hallucination-audit/` if it does not exist.

3. **Dispatch agents in parallel**
   For each chapter directory `book/chapters/NN-slug/`:
   - Read `book/chapters/NN-slug/chapter.tex`
   - Check whether `code/notebooks/NN-slug/exercises.ipynb` exists; if so, include it
   - Spawn one **hallucination-detector** agent with:
     - The full text of `chapter.tex`
     - The notebook content (if present)
     - `TOPIC.md` for domain context
   - All agents run concurrently — do not wait for one before starting the next

4. **Collect results**
   Gather every agent's output. For each chapter:
   - If the verdict is `CLEAN`: record chapter as clean (no file written)
   - If the verdict is `HALLUCINATIONS FOUND`: save the full markdown report to
     `docs/quality/hallucination-audit/chNN-hallucination-report.md`
     (where `NN` is the two-digit chapter number)

5. **Print summary table**
   After all agents finish, print:

   ```
   === Hallucination Audit Summary ===

   | Chapter | Title                        | Status         | H-text | H-code |
   |---------|------------------------------|----------------|--------|--------|
   | ch01    | Introduction                 | CLEAN          |   0    |   0    |
   | ch02    | LLM Foundations              | ISSUES FOUND   |   2    |   1    |
   ...

   Total chapters audited: N
   Chapters with issues:   M
   Reports saved to: docs/quality/hallucination-audit/
   ```

   Fill H-text and H-code from each agent's summary table. Use 0 for CLEAN chapters.

6. **Aggregate report**
   Write `docs/quality/hallucination-audit/SUMMARY.md` with:
   - The summary table above
   - A section "Chapters Requiring Attention" listing each chapter with issues and its report path
   - A section "Clean Chapters" listing all chapters that passed

7. **Commit**
   Stage and commit:
   ```
   git add docs/quality/hallucination-audit/
   git commit -m "docs: hallucination audit report"
   ```

## Expected Output

- Per-chapter markdown reports in `docs/quality/hallucination-audit/chNN-hallucination-report.md` (only for chapters with findings)
- `docs/quality/hallucination-audit/SUMMARY.md`
- Summary table printed to console

## Error Handling

- If `chapter.tex` is a placeholder (fewer than 100 lines or contains `% PLACEHOLDER`): skip the chapter and note it as SKIPPED in the summary table.
- If a notebook is malformed JSON: log "notebook parse error" for that chapter and continue with text-only analysis.
- If the hallucination-detector agent returns no structured output: mark the chapter as ERROR in the summary and continue.
- If `docs/quality/` does not exist: create the full path before saving.
