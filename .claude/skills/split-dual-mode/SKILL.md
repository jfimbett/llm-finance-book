# /split-dual-mode

## Purpose

Wrap each section (or subsection group) of a chapter in the appropriate dual-mode
box: `\begin{context}` for practitioner-facing content ("the bigger picture") or
`\begin{deepdive}` for technical content ("under the hood"). This reproduces for
any chapter the typographic treatment already applied to chapters 01 and 02.

## When to Invoke

After a chapter draft exists and has been reviewed for content quality. Run once
per chapter. Safe to re-run: the skill detects already-correctly-boxed content
and skips it.

## Inputs Required

- Chapter number or path (e.g., `03` or `book/chapters/03-llm-training-finetuning/chapter.tex`).
  If not provided, ask the user once.
- No other files are needed beyond the chapter itself.

## Boxing Rules

### Box types

| Environment | Rendered label | Use when… |
|---|---|---|
| `\begin{context}…\end{context}` | "the bigger picture" | Narrative, history, motivation, finance applications, governance, deployment, practical guidance, intuition-building, "looking ahead" transitions |
| `\begin{deepdive}…\end{deepdive}` | "under the hood" | Mathematical derivations, formal definitions, algorithm descriptions, architecture details, implementation specifics, formal benchmarking and evaluation metrics |

### What never gets a box

- The `\chapter{…}` heading line and its `\label{}`
- The `\begin{remark}[Learning Objectives]…\end{remark}` block at the chapter top
- The chapter summary paragraph(s) at the very end (after the last numbered section),
  unless they form a dedicated `\section{Chapter Summary}` — in that case wrap in
  a context box

### Granularity

1. **Default — one box per top-level section.** The box opens immediately after
   `\label{sec:…}` (on a blank line) and closes immediately before the next
   `\section{` or `\printbibliography` or end of file.

2. **Per-subsection — use only when subsections within one section clearly split
   between applied and technical.** For example: the first N subsections are
   practical guidance → context; the next M subsections are mathematical → deepdive.
   In that case, open and close a box around each group of like-natured subsections.
   A single `\subsection{}` heading may appear either inside or immediately before
   a box; it should never be split across two different boxes.

3. **Never nest boxes.** If a section already contains a small `\begin{context}` or
   `\begin{deepdive}` snippet wrapping just a few paragraphs, remove that inner
   wrapper — absorb the content into the surrounding section-level box.

### Classifying a section

Ask these questions about the section's content:

- Does the section spend the majority of its lines on prose explanation, financial
  application examples, institutional context, historical narrative, or qualitative
  trade-offs? → **context**
- Does the section spend the majority of its lines on numbered equations, formal
  definitions (`\begin{definition}`), algorithm steps, or code? → **deepdive**
- Is the section genuinely 50/50? → classify by the opening paragraph's character
  (the opening sets the reader's expectations for the section).

### Opening prose inside a box

When a box opens, the first paragraph should orient the reader. If the existing
first paragraph is a dry technical statement, prepend or rewrite it to be a
1–2 sentence orienting sentence:
- For a context box: connect the section topic to a practitioner problem or a
  concrete financial scenario.
- For a deepdive box: state what the reader will be able to derive or implement
  after finishing the section.

Keep the rewrite minimal — the goal is a smooth entry into the box, not a full
section rewrite. The rest of the section content stays verbatim.

## Steps

1. Read `TOPIC.md` to confirm the chapter scope and audience.

2. Resolve the target file path. Accept `03`, `ch03`, or a full path. Map to
   `book/chapters/NN-name/chapter.tex`. If ambiguous, ask the user.

3. Read the full chapter file.

4. **Audit existing boxes.** Identify every `\begin{context}`, `\end{context}`,
   `\begin{deepdive}`, `\end{deepdive}` in the file and note their line ranges.
   Determine whether each box already correctly spans a full section or subsection
   group. Boxes that span only a few paragraphs within a larger unboxed section are
   "partial" and must be removed and replaced by the section-level box.

5. **Plan the boxing.** For each top-level section, decide:
   - Box type (context or deepdive), or
   - Per-subsection split (list which subsections get which type)
   
   Write out the plan as a compact bullet list before making any edits (this
   serves as your working document — do not output it to the user, keep it
   internal).

6. **Apply the boxes.** Edit `chapter.tex` section by section:
   a. Remove any partial inner boxes identified in step 4.
   b. Insert `\begin{boxtype}` on a blank line after `\label{sec:…}` (or after
      `\subsection{…}\label{…}` for per-subsection mode).
   c. Insert `\end{boxtype}` on a blank line before the next `\section{`,
      `\subsection{` (when switching box type), or end of chapter body.
   d. If the opening paragraph needs orienting prose (step "Opening prose inside
      a box"), apply that minimal edit now.

7. **Validate the result.** Check:
   - Every `\begin{context}` has a matching `\end{context}` in the same file.
   - Every `\begin{deepdive}` has a matching `\end{deepdive}` in the same file.
   - No box is nested inside another box.
   - The chapter heading, learning-objectives remark, and any post-section summary
     prose are outside all boxes.
   - The total line count of the file has not decreased by more than 5 lines
     (content must not be deleted, only wrappers added/removed).

8. **Compile to verify.** Run the build from `book/`:
   ```
   pdflatex -interaction=nonstopmode main.tex
   ```
   Check `main.log` for lines starting with `! `. If errors exist, diagnose and
   fix before proceeding.

9. **Commit.** Stage and commit the chapter file:
   ```
   git add book/chapters/NN-name/chapter.tex
   git commit -m "feat(chNN): wrap sections in context/deepdive boxes (dual-mode split)"
   ```

## Expected Output

A `chapter.tex` where:
- Every top-level section's content (or clearly-typed subsection group) is wrapped
  in exactly one `\begin{context}` or `\begin{deepdive}` box.
- No content has been removed.
- The file compiles without LaTeX errors.
- The visual result matches the style of `book/chapters/01-intro/chapter.tex` and
  `book/chapters/02-llm-foundations/chapter.tex`.

## Examples of classification

The following are examples drawn from chapters already processed; use them to
calibrate judgment on new chapters:

| Section title (ch01/ch02) | Box type |
|---|---|
| A Brief History of Textual Analysis in Finance | context |
| Why Text Matters in Finance | context |
| Classical Text Representations | deepdive |
| Word Embeddings | deepdive |
| Document-Level Representations | deepdive |
| Sequential Models: From RNNs to Attention | deepdive |
| The Transformer Architecture | deepdive |
| The Modern LLM Landscape | context |
| Temperature, Sampling (math subsections) | deepdive |
| Sampling Strategy Selection for Financial Tasks | context |
| Structured Generation | deepdive |
| Working with LLMs via API | context |
| Retrieval-Augmented Generation | deepdive |
| Hallucinations: Detection and Mitigation | context |
| Limitations and Responsible Use | context |

## Error Handling

- **File not found:** Print the resolved path and ask the user to confirm the
  chapter number.
- **Compilation errors after boxing:** The most common cause is a box that opens
  inside a `tabular`, `equation`, or `lstlisting` environment. Find the offending
  `\begin{…}` and move it outside the inner environment.
- **Nested box detected during validation:** Remove the inner box wrapper; keep
  the content.
- **Chapter already fully boxed:** Print "Chapter NN is already fully boxed —
  nothing to do." and exit without committing.
