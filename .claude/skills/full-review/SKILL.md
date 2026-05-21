# /full-review

## Purpose

Run a comprehensive review of a content file: scoring, critique, and peer review in sequence, consolidated into one report.

## When to Invoke

Before marking a chapter as released. Run after the chapter draft is complete and initial quality scores are acceptable.

## Inputs Required

- File path: a `chapter.tex` or lecture directory

## Steps

1. Run `/score-content [file]` — print scores and status.
2. Run `/critique [file]` — print ranked issue list.
3. Run `/peer-review [file]` — print referee report and verdict.
4. Print a consolidated summary:
   ```
   === Full Review Summary ===
   Quality Score:  N.N/10 (PASS/FAIL)
   BLOCKERs:       N
   MAJORs:         N
   Peer Verdict:   ACCEPT | MINOR_REVISION | MAJOR_REVISION | REJECT
   
   Recommendation: READY_TO_RELEASE | NEEDS_REVISION | MAJOR_REVISION_REQUIRED
   ```
   - READY_TO_RELEASE: score passes, 0 BLOCKERs, peer verdict ACCEPT or MINOR_REVISION
   - NEEDS_REVISION: score passes but BLOCKERs or MAJORs present, or peer verdict MINOR_REVISION
   - MAJOR_REVISION_REQUIRED: score fails or peer verdict MAJOR_REVISION or REJECT

## Expected Output

Three reports printed in sequence, followed by a consolidated summary with a clear recommendation.

## Error Handling

- If any sub-skill fails (e.g., scorer agent unavailable): report which sub-skill failed and continue with the remaining ones.
- If the file is a placeholder: print a warning and stop.
