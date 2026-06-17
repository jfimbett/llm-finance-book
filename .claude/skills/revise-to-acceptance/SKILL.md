# /revise-to-acceptance

## Purpose

Work through a chapter's editor feedback file systematically, fixing each issue with the right agent, until `/full-review` returns READY_TO_RELEASE.

## When to Invoke

After `/full-review` produces a NEEDS_REVISION or MAJOR_REVISION_REQUIRED verdict and an editor feedback file exists at `docs/quality/[chapter]-editor-feedback.md`.

## Inputs Required

- Chapter file path: e.g., `book/chapters/01-intro/chapter.tex`
- Editor feedback file: inferred as `docs/quality/book_chapters_[NN-name]_chapter-editor-feedback.md`, or pass explicitly

## Steps

### Phase 1 — Load State

1. Read `TOPIC.md` for `quality_threshold` and `max_refine_iterations`.
2. Read the editor feedback file. Parse all issues marked `[ ]` (open). If none remain open: jump to Phase 3.
3. Print the open issue list with counts: `N BLOCKERs open, N MAJORs open, N MINORs open`.

### Phase 2 — Fix Issues (BLOCKERs → MAJORs → MINORs)

For each open issue in priority order:

#### 2a. Classify the fix type

| Issue type | Primary agent | Notes |
|-----------|--------------|-------|
| Missing section / unwritten LO | **book-writer** | Also invoke **exercise-designer** for exercises |
| Placeholder figure | **figure-designer** or **code-writer** | Use code-writer if a matplotlib/minted listing is preferred |
| Wrong `\cite{}` key | **fact-checker** to identify correct citation, then **chapter-surgeon** to apply it |
| Broken `\ref{}` / `\label{}` | **chapter-surgeon** | Quick textual replacement |
| Mathematical error in equation | **math-checker** to verify, then **chapter-surgeon** to apply fix |
| Missing code listing | **code-writer** | Return LaTeX minted block |
| Notation inconsistency | **chapter-surgeon** | Apply find-and-replace within specified scope |
| Prose/clarity issue | **editor** | Improve the named paragraph/section only |
| Ambiguous citation / footnote needed | **chapter-surgeon** | Insert parenthetical or footnote |

#### 2b. Invoke the agent

Provide the agent with:
- The chapter content (or the relevant excerpt)
- The exact issue description from the editor feedback file (location + problem + fix)
- An explicit scope constraint: "Fix only this specific issue. Do not change anything else."

#### 2c. Apply the output

- For **book-writer** output: insert the new LaTeX at the correct position in `chapter.tex` (after the last existing section, or at the location specified in the issue).
- For **chapter-surgeon** output: apply the patch at the stated location.
- For **code-writer** output: insert the `\begin{listing}...\end{listing}` block at the stated location.
- For **figure-designer** output: replace the placeholder `\begin{figure}...\end{figure}` block with the new one.

#### 2d. Verify and commit

1. Run `/score-content book/chapters/[NN-name]/chapter.tex` — check that no dimension regressed.
2. If a dimension regressed: note the regression, revert the change, mark the issue as `[!] FAILED — regression` in the feedback file, and continue to the next issue.
3. If scores are stable or improved: mark the issue as `[x]` in the feedback file.
4. Commit: `git add book/chapters/[NN-name]/chapter.tex docs/quality/ && git commit -m "fix(ch[NN]): [BLOCKER/MAJOR/MINOR] — [issue title]"`

Repeat for all open issues.

### Phase 3 — Full Review Gate

1. After all BLOCKERs and MAJORs are marked `[x]`, run `/full-review book/chapters/[NN-name]/chapter.tex`.
2. If the result is **READY_TO_RELEASE**: print success, commit the updated feedback file, and exit.
3. If the result is **NEEDS_REVISION** or **MAJOR_REVISION_REQUIRED**:
   - Parse the new feedback for any newly identified issues.
   - Append new issues (marked `[ ]`) to the editor feedback file under a new section `## Revision Round N`.
   - Increment the round counter.
   - If round counter ≥ `max_refine_iterations`: print `ITERATION LIMIT REACHED — human review required` and exit with non-zero status.
   - Return to Phase 2.

### Phase 4 — Done

Print:
```
=== Revision Complete ===
Chapter:  [file path]
Rounds:   N
Result:   READY_TO_RELEASE
```

Commit the final state: `chore(ch[NN]): revision complete — all editor issues resolved`

## Agent Selection Quick Reference

```
Missing content (whole sections) → book-writer
Missing exercises                → exercise-designer
Placeholder figure               → figure-designer
Code listing missing             → code-writer
Citation wrong                   → fact-checker → chapter-surgeon
Cross-ref broken                 → chapter-surgeon
Math error                       → math-checker → chapter-surgeon
Notation fix                     → chapter-surgeon
Prose/clarity                    → editor
```

## Error Handling

- **Agent returns empty output**: skip the issue, mark `[!] AGENT FAILED`, continue.
- **Score regresses after fix**: revert change, mark `[!] REGRESSION`, continue.
- **Editor feedback file missing**: print `ERROR: no editor feedback file found at [path]` and exit.
- **chapter.tex not found**: print `ERROR: chapter file not found at [path]` and exit.
- **All BLOCKERs still open after max iterations**: escalate to human with a summary of what was attempted.

## Expected Output

`chapter.tex` updated with all identified issues resolved, quality score ≥ threshold on all dimensions, and `/full-review` returning READY_TO_RELEASE. The editor feedback file updated with `[x]` on all resolved items. All intermediate fixes committed to git.
