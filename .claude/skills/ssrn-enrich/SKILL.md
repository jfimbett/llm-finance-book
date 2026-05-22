# /ssrn-enrich

## Purpose

Enrich a book chapter with recent SSRN working papers: discover relevant preprints via
`ssrn-researcher`, generate `@unpublished` BibTeX entries, and weave citations and
explanatory prose into the chapter's LaTeX using the `editor` agent.

## When to Invoke

When a chapter has real draft content and you want to incorporate recent working papers
not yet published in journals — especially useful for fast-moving LLM-in-finance topics.
Run after `/draft-chapter` and before `/release-chapter`.

## Inputs Required

- Chapter identifier, e.g. `06-credit-risk` — required; ask if not provided
- `TOPIC.md` — for subject area and `quality_threshold`
- `book/chapters/NN-name/chapter.tex` — must contain real content (not placeholder text)

## Steps

1. Read `TOPIC.md` to extract the book's subject area and `quality_threshold`.

2. Read `book/chapters/NN-name/chapter.tex`. If the file still contains placeholder text
   (e.g. "invoke /draft-chapter"), stop immediately and tell the user:
   > "This chapter has not been drafted yet. Run `/draft-chapter NN-name` first."

3. **Invoke the `ssrn-researcher` agent** — provide:
   - The full chapter text
   - The topic string from `TOPIC.md`
   - Instruction: find 5–10 papers posted in the last 3 years

4. Receive the agent's structured output: one `PAPER:` block per paper.
   If the output contains a `WARNING: Only N papers found` line, relay that warning to
   the user but continue.

5. Resolve the target `.bib` file and append BibTeX entries:
   - Scan `book/chapters/NN-name/chapter.tex` for `\addbibresource{...}` or
     `\bibliography{...}` directives to identify the correct `.bib` file. If no directive
     is found, default to `book/bibliography.bib`.
   - If the resolved `.bib` file does not exist, create it as an empty file before
     proceeding.
   - Read the existing `.bib` file and collect all current entry keys.
   - For each new `@unpublished` entry from the researcher, check if its key already
     exists. If it does, append `_ssrn` to the incoming key (e.g. `Smith2024_ssrn`) and
     log: `NOTE: key Smith2024 already exists — renamed to Smith2024_ssrn.`
   - Append all new entries to the end of the `.bib` file.

6. **Invoke the `editor` agent** — provide:
   - The full chapter text (as last read in step 2)
   - The researcher's complete output (all `PAPER:` blocks, with any key renames applied)
   - This exact instruction:
     > "For each PAPER block, insert a `\cite{KEY}` marker at the location indicated by
     > its Section and Supports fields. Then extend the surrounding sentence, or add a
     > new sentence immediately after, to explain in one clause what this working paper
     > contributes. Do not produce bare parenthetical citations — the paper's contribution
     > must appear in the prose, not just in the cite marker."

7. Write the editor's revised chapter text to `book/chapters/NN-name/chapter.tex`.

8. Run `/audit-bibliography` to catch broken cite keys or missing required fields.
   If the audit reports any broken keys, resolve them before proceeding.

9. Run `/score-content book/chapters/NN-name/chapter.tex`.
   If any dimension is below `quality_threshold` from `TOPIC.md`, run
   `/refine-until-threshold book/chapters/NN-name/chapter.tex`.

10. Commit:
    ```
    git add book/chapters/NN-name/chapter.tex <resolved-bib-file>
    git commit -m "feat(chNN): enrich with SSRN working papers"
    ```
    Replace `NN` with the chapter number and `<resolved-bib-file>` with the actual `.bib`
    path identified in step 5.

## Expected Output

- `book/chapters/NN-name/chapter.tex` — updated with `\cite{}` markers and explanatory
  prose for each new working paper
- The chapter's `.bib` file (resolved from `\addbibresource`/`\bibliography`, defaulting to `book/bibliography.bib`) — new `@unpublished` entries appended at the end
- Quality scores at or above `quality_threshold` in all dimensions

## Error Handling

- **Fewer than 3 papers found**: relay the researcher's WARNING, proceed with what was
  found, do not abort.
- **BibTeX key collision**: rename with `_ssrn` suffix and log the rename; do not skip
  the paper.
- **Chapter is placeholder text**: stop immediately, direct user to `/draft-chapter`.
- **`/score-content` unavailable**: skip scoring and print:
  `Run /score-content book/chapters/NN-name/chapter.tex manually when available.`
- **`/audit-bibliography` reports broken keys**: do not commit until broken keys are
  resolved. Fix or remove the offending entry, then re-run the audit.
