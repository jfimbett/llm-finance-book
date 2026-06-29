# /reshape-chapter

## Purpose

Modify an existing book chapter or appendix based on user-provided ideas, feedback, reviewer comments, new structure, missing material, or requested changes.

Unlike `/draft-chapter`, this command does **not** generate a chapter from scratch. It reshapes an already drafted `chapter.tex` while preserving the chapter's existing intellectual core, citations, labels, cross-references, and project style.

## When to Invoke

Use this command when the user wants to revise, restructure, expand, compress, clarify, or otherwise improve an existing chapter or appendix.

Examples:

* “Reshape chapter 04 to emphasize credit risk stress testing.”
* “Incorporate this referee feedback into chapter 07.”
* “Make the motivation stronger and add a running example.”
* “Reorganize the chapter around bank default prediction instead of generic classification.”
* “Add more intuition before the math.”
* “Make the chapter less technical for MBAs.”
* “Move the empirical example earlier.”
* “Add a section on stress scenarios and regulatory capital.”
* “Rewrite this appendix to be shorter and more focused.”

Run this after `/draft-chapter` has produced real content.

## Inputs Required

* Chapter identifier, appendix identifier, or full path:

  * Chapter identifier: `NN-name`, e.g. `04-credit-risk`
  * Appendix identifier: `A-math-review`
  * Full path: `book/chapters/04-credit-risk/chapter.tex`
* User-provided reshape instructions:

  * ideas
  * changes
  * feedback
  * reviewer comments
  * outline changes
  * tone/depth changes
  * specific sections to modify
* `TOPIC.md` — for audience, subject, quality threshold, and `book_depth`

Optional:

* Supporting notes or pasted reviewer feedback
* Additional references to include
* Desired target structure
* Desired target length
* Specific sections to preserve unchanged

---

## Path Resolution

Determine the target file based on the identifier format:

* **Chapter** with numeric prefix, e.g. `04-credit-risk`:

```text
book/chapters/04-credit-risk/chapter.tex
```

* **Appendix** with uppercase letter prefix, e.g. `A-math-review`:

```text
book/appendices/A-math-review/chapter.tex
```

* **Full path**:

Use the path directly.

If the resolved `chapter.tex` does not exist, stop and tell the user to run `/new-topic` first.

---

## Revision Philosophy

The goal is controlled reshaping, not blind rewriting.

Preserve unless the user explicitly asks otherwise:

* chapter title
* core argument
* existing correct equations
* valid theorem/proof environments
* useful examples
* existing labels and references
* existing citations
* terminology already standardized elsewhere in the book
* notation conventions
* links to companion lectures or exercises

Modify aggressively only when required by the user's feedback.

When in doubt, prefer:

* local edits over global rewrites
* restructuring over deleting
* adding connective explanation over simplifying away substance
* preserving labels over renaming labels
* improving motivation and flow before changing mathematical content

---

## Steps

1. Read `TOPIC.md` to understand:

   * subject
   * audience
   * `book_depth`
   * `quality_threshold`
   * notation and style expectations, if specified

2. Resolve the target path using the input identifier.

3. Read the current `chapter.tex`.

4. Verify that the chapter contains real content.

   * If the file is mostly `[Placeholder]`, stop and tell the user to run `/draft-chapter` first.
   * If the chapter has real content, proceed.

5. Parse the user's reshape request into an explicit revision plan.

   Create a short internal checklist with:

   * sections to revise
   * sections to preserve
   * new sections/subsections to add
   * sections/subsections to delete or merge
   * changes in emphasis
   * changes in audience depth
   * new examples, applications, or exercises implied by the request
   * citations or references that may need to be added
   * mathematical claims that need re-checking

6. If the requested change affects the chapter structure, invoke the `outline-curator` agent.

   Provide:

   * current section and subsection headings
   * the user's requested changes
   * the audience and depth from `TOPIC.md`
   * the intended role of the chapter in the book

   Ask the agent to return a revised outline with one of:

```text
STATUS: APPROVED
STATUS: NEEDS_REVISION
```

If `STATUS: NEEDS_REVISION`, address the issues and re-run the agent.

Do not exceed three outline-curator iterations. If still unresolved after three iterations, surface the remaining structural issues to the user and ask for guidance.

7. If the request adds new academic content, empirical claims, models, examples, or references, invoke the `literature-reviewer` agent.

   Ask for:

   * 3–7 relevant references if needed
   * BibTeX entries for genuinely new references only
   * a short explanation of where each reference belongs

   Append only new BibTeX entries to `book/bibliography.bib`.

   Do not add duplicate BibTeX keys.

8. Invoke the `book-writer` agent for the substantive reshape.

   Provide:

   * current `chapter.tex`
   * the user's reshape instructions
   * approved revised outline, if any
   * audience and depth from `TOPIC.md`
   * references to add or emphasize
   * explicit preservation constraints

   Ask the agent to return a revised complete `chapter.tex`, not a patch, unless the user explicitly requested a narrow patch.

   The output must:

   * preserve valid LaTeX syntax
   * preserve existing labels where possible
   * add labels for any new section, subsection, theorem, proposition, example, or figure placeholder
   * avoid duplicate labels
   * preserve or improve cross-references
   * maintain the book's notation conventions
   * avoid unsupported empirical or bibliographic claims
   * keep placeholders only if the user explicitly requested an outline-level revision

9. Write the revised output to the resolved `chapter.tex`.

10. Invoke the `math-checker` agent if the reshape changed any of the following:

* equations
* derivations
* propositions
* theorems
* proofs
* optimization problems
* statistical assumptions
* model definitions
* identification arguments
* empirical estimands

Ask the math-checker to verify correctness and return:

```text
VERDICT: PASS
```

or

```text
VERDICT: FAIL
```

If `VERDICT: FAIL`, send the issues back to the `book-writer` agent and revise.

Repeat until `PASS`, or stop after two failed repair attempts.

If still failing after two attempts, keep the best revised version, add a visible LaTeX comment near the unresolved material:

```latex
% NEEDS_HUMAN_REVIEW: [brief description of unresolved issue]
```

and continue.

11. Invoke the `editor` agent.

Ask it to improve:

* clarity
* flow
* transitions
* paragraph structure
* consistency with the rest of the book
* terminology
* motivation
* summary and takeaways

The editor must not alter mathematical meaning.

Apply the editor's revised version to `chapter.tex`.

12. Run a label and citation sanity check.

Verify:

* no duplicate labels were introduced
* no obvious broken `\ref`, `\Cref`, `\cite`, or `\autoref` commands were introduced
* no citation key was used without appearing in `book/bibliography.bib`
* no old section label now points to a misleading section
* no hard-coded chapter numbers were introduced

13. Run `/score-content [resolved path]`.

14. If any score is below `quality_threshold` from `TOPIC.md`, run:

```text
/refine-until-threshold [resolved path]
```

Focus the refinement on the dimensions most affected by the reshape request.

15. Run a local build check when possible.

Prefer:

```bash
bash scripts/build-book.sh
```

If unavailable, run the project's standard LaTeX build command.

If the build fails, fix errors introduced by the reshape.

16. Create a short reshape report in `docs/quality/` if that folder exists.

Suggested filename:

```text
docs/quality/reshape-NN-name.md
```

or for appendices:

```text
docs/quality/reshape-A-name.md
```

The report should include:

```markdown
# Reshape Report: NN-name

## User Request

[Brief summary of the requested change]

## Main Changes Applied

- [Change 1]
- [Change 2]
- [Change 3]

## Sections Modified

- [Section name]
- [Section name]

## New References Added

- [Citation key or "None"]

## Math Checker

PASS / NEEDS_HUMAN_REVIEW / NOT RUN

## Score Summary

[Paste score-content summary if available]

## Remaining Issues

- [Issue or "None"]
```

17. Commit the changes.

For chapters:

```bash
git add book/chapters/NN-name/chapter.tex book/bibliography.bib docs/quality/reshape-NN-name.md
git commit -m "revise(chNN): reshape [topic name] chapter"
```

For appendices:

```bash
git add book/appendices/A-name/chapter.tex book/bibliography.bib docs/quality/reshape-A-name.md
git commit -m "revise(appA): reshape [topic name] appendix"
```

If there are no new bibliography entries, do not include `book/bibliography.bib`.

If the quality report was not created, do not include `docs/quality/...`.

---

## Expected Output

A revised `chapter.tex` or appendix `chapter.tex` that incorporates the user's requested changes while preserving project consistency.

The command should report:

* target file modified
* summary of changes
* sections changed
* references added, if any
* math-checker result
* content score result, if available
* build result, if available
* commit hash

---

## Error Handling

* If the chapter does not exist: stop and tell the user to run `/new-topic` first.
* If the chapter is still placeholder-only: stop and tell the user to run `/draft-chapter` first.
* If the user asks for changes but gives no actual feedback or direction: ask for the missing reshape instructions.
* If the requested change conflicts with `TOPIC.md`, follow the user's explicit request but mention the conflict in the reshape report.
* If the requested change requires new references and `literature-reviewer` is unavailable, proceed with clearly marked citation placeholders:

```latex
% CHECK: add citation for [claim]
```

* If `book/bibliography.bib` cannot be found, create it only if the project convention allows it; otherwise report the missing file.
* If the math-checker fails twice, continue with a `NEEDS_HUMAN_REVIEW` marker and use a commit message prefix:

```text
[NEEDS_HUMAN_REVIEW] revise(chNN): reshape [topic name] chapter
```

* If `/score-content` is unavailable, skip scoring and remind the user to run it manually.
* If the build fails for reasons unrelated to the reshaped chapter, report that the reshape was completed but the full book build is blocked by pre-existing errors.

---

## Example Invocation

```text
/reshape-chapter 04-credit-risk

Reshape this chapter so that the central running example is a corporate credit-risk stress test.

The chapter should start from a lender trying to estimate default risk under normal conditions, then introduce a macro stress scenario with higher unemployment, lower GDP growth, and tighter refinancing conditions.

Make the ML material feel less abstract by connecting feature selection, calibration, and model validation to the credit-risk use case. Add a section explaining how stress testing differs from ordinary prediction. Keep the math, but add more intuition before each formal object.
```

## Example Expected Changes

The command should revise the chapter so that:

* the motivation is built around credit-risk stress testing;
* the running example appears early and returns throughout the chapter;
* abstract modeling concepts are tied to probability of default, loss given default, and exposure at default;
* the chapter distinguishes prediction accuracy from stress-scenario usefulness;
* any new stress-testing or credit-risk claims are cited;
* the final summary explains what the reader should remember about using models under stressed conditions.
