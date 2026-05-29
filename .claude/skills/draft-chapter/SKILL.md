# /draft-chapter

## Purpose

Generate a first draft of a book chapter or appendix by orchestrating the literature-reviewer, book-writer, math-checker, and editor agents in sequence.

## When to Invoke

After `/new-topic` has scaffolded the chapter or appendix directory. The target `chapter.tex` should still contain placeholder content.

## Inputs Required

- Chapter identifier (e.g., `01-intro`) or appendix identifier (e.g., `A-math-review`) — ask if not provided
- `TOPIC.md` — for subject, audience, and depth
- Any outline, notes, or reference material the user wants to provide (optional)

## Path Resolution

Determine the target file based on the identifier format:

- **Chapter** (numeric prefix, e.g., `01-intro`): `book/chapters/01-intro/chapter.tex`
- **Appendix** (single uppercase letter prefix, e.g., `A-math-review`): `book/appendices/A-math-review/chapter.tex`

If the user passes a full path, use it directly.

## Steps

1. Read `TOPIC.md` to understand the subject, audience, and `book_depth` setting.
2. Resolve the target path using the identifier (see Path Resolution above). Verify `chapter.tex` exists. If it still contains placeholder text, proceed. If it already has real content, ask the user whether to overwrite.
3. **Invoke the literature-reviewer agent**: provide the topic and ask it to suggest 3–7 relevant references with BibTeX entries. Append the returned BibTeX entries to `book/bibliography.bib`.
4. **Invoke the book-writer agent**: provide the topic, audience from `TOPIC.md`, and any user-supplied notes. Ask it to draft all sections as LaTeX, using the standard structure (Motivation, Core Concepts, Examples, Summary). Write the output to the resolved `chapter.tex`.
5. **Invoke the math-checker agent** on the draft: verify all derivations and proofs. If the verdict is FAIL, return to the book-writer agent with the specific issues to fix. Repeat until PASS or after 2 iterations (flag for human review if still failing).
6. **Invoke the editor agent** on the verified draft: ask it to improve clarity and flow. Apply the returned edits to `chapter.tex`.
7. Run `/score-content [resolved path]` to get the initial quality scores.
8. If any dimension is below `quality_threshold` from `TOPIC.md`, run `/refine-until-threshold [resolved path]`.
9. Commit:
   - Chapter: `git add book/chapters/NN-name/ book/bibliography.bib && git commit -m "feat(chNN): draft [topic name] chapter"`
   - Appendix: `git add book/appendices/A-name/ book/bibliography.bib && git commit -m "feat(appA): draft [topic name] appendix"`

## Expected Output

A complete `chapter.tex` with real content (sections, theorems, proofs, examples), bibliography entries added to `bibliography.bib`, and a quality score report in `docs/quality/`.

## Error Handling

- If the book-writer produces a draft with `% CHECK:` syntax flags, note them but do not block — they can be fixed in a later editing pass.
- If math-checker fails twice: commit the draft as-is with a `[NEEDS_HUMAN_REVIEW]` prefix in the commit message and print a clear warning.
- If `/score-content` is not available: skip scoring and remind the user to run it manually.
