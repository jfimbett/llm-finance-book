# /draft-chapter

## Purpose

Generate a first draft of a book chapter by orchestrating the literature-reviewer, book-writer, math-checker, and editor agents in sequence.

## When to Invoke

After `/new-topic` has scaffolded the chapter directory. The target `chapter.tex` should still contain placeholder content.

## Inputs Required

- Chapter number/name (e.g., `01-intro`) — ask if not provided
- `TOPIC.md` — for subject, audience, and depth
- Any outline, notes, or reference material the user wants to provide (optional)

## Steps

1. Read `TOPIC.md` to understand the subject, audience, and `book_depth` setting.
2. Verify `book/chapters/NN-name/chapter.tex` exists. If it still contains placeholder text ("invoke /draft-chapter"), proceed. If it already has real content, ask the user whether to overwrite.
3. **Invoke the literature-reviewer agent**: provide the chapter topic and ask it to suggest 3–7 relevant references with BibTeX entries. Append the returned BibTeX entries to `book/bibliography.bib`.
4. **Invoke the book-writer agent**: provide the chapter topic, audience from `TOPIC.md`, and any user-supplied notes. Ask it to draft all sections of the chapter as LaTeX, using the chapter template structure (Motivation, Core Concepts, Examples, Summary). Write the output to `book/chapters/NN-name/chapter.tex`.
5. **Invoke the math-checker agent** on the draft: pass the chapter content and ask for verification of all derivations and proofs. If the verdict is FAIL, return to the book-writer agent with the specific issues to fix. Repeat until PASS or after 2 iterations (flag for human review if still failing).
6. **Invoke the editor agent** on the verified draft: ask it to improve clarity and flow. Apply the returned edits to `chapter.tex`.
7. Run `/score-content book/chapters/NN-name/chapter.tex` to get the initial quality scores.
8. If any dimension is below `quality_threshold` from `TOPIC.md`, run `/refine-until-threshold book/chapters/NN-name/chapter.tex`.
9. Commit: `git add book/chapters/NN-name/ book/bibliography.bib && git commit -m "feat(chNN): draft [topic name] chapter"`

## Expected Output

A complete `chapter.tex` with real content (sections, theorems, proofs, examples), bibliography entries added to `bibliography.bib`, and a quality score report in `docs/quality/`.

## Error Handling

- If the book-writer produces a draft with `% CHECK:` syntax flags, note them but do not block — they can be fixed in a later editing pass.
- If math-checker fails twice: commit the draft as-is with a `[NEEDS_HUMAN_REVIEW]` prefix in the commit message and print a clear warning.
- If `/score-content` is not available: skip scoring and remind the user to run it manually.
