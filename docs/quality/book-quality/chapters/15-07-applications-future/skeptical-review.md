# Skeptical Review — Ch. 07 Applications & Future Trends (reading index 15)

Format: `SEVERITY · dimension_key · file:line — issue` · scope.
Audit only — no edits.

## BLOCKERS

- **BLOCKER · notation_crossref · book/chapters/07-applications-future/chapter.tex:400 —
  Label collision `def:calibration`.** Defined here as "Calibration Within Group"
  (fairness), but ALSO defined in `book/chapters/06-credit-risk/chapter.tex:382` as
  "Calibration" (PD vs observed default rate) — two *different* concepts, same key.
  LaTeX emits "multiply-defined labels"; `\ref{def:calibration}` at chapter.tex:379 (the
  "Definitions~\ref{def:demographic-parity}--\ref{def:calibration}" range) resolves
  ambiguously / to the wrong definition. This is the exact duplicate flagged in
  RUBRIC.md §2 line 151. Scope: cross-chapter / notation. Fix: rename ch07's label to
  e.g. `def:calibration-within-group` and update the in-chapter `\ref`.

- **BLOCKER · code_figure_correctness · chapter.tex:243 and chapter.tex:334 —
  prose points readers to a STUB notebook.** Both lines say "The complete Python
  implementation for this example is available in
  `code/notebooks/07-applications-future/demo.ipynb`", but `demo.ipynb` contains a single
  markdown cell ending "[Placeholder — fill in with working code as the chapter is
  drafted]" (1 cell, no code). The actual working code (EDGAR 8-K monitor; OpenClaw-style
  skills) lives in `exercises.ipynb`, not `demo.ipynb`. Reader following the pointer hits
  an empty placeholder. Scope: code-figure / reproducibility. Fix: populate `demo.ipynb`
  or repoint prose to `exercises.ipynb`.

## MAJOR

- **MAJOR · correctness · chapter.tex:38 — "Six chapters ago".** This chapter is at
  reading index 15; `ch:intro` is index 1. The opening "Six chapters ago, this book
  opened with a question..." is a stale numeric reference from the pre-reorder folder
  numbering. It is factually wrong against the `main.tex` reading order. Scope: local /
  cross-chapter-ordering.

- **MAJOR · correctness · chapter.tex:56-82 (`tab:chapter-map`).** The "Chapter map"
  table numbers chapters 1–7 using OLD folder numbers (1=Intro, 4=Agents, 5=Valuation,
  6=Credit, 7=this chapter). In reading order these are 1, 6, 9, 10, 15. The table thus
  presents a chapter numbering that contradicts the book's actual reading sequence and
  omits 9 of the 16 chapters (foundations of summarisation, sentiment, domain-specific,
  portfolio, regtech, xai, limitations, ai-ml-finance-text, privacy). A reader cross-
  checking the table against the TOC will be confused. Scope: local / book-repetition-of-
  stale-numbering. (The `\ref{ch:...}` prose refs at 42 are correct; only the *table's*
  hard-coded "Ch. N" column and the narrative numbering are wrong.)

- **MAJOR · citation_accuracy · chapter.tex:147 — FinanceBench "roughly 80%" claim.**
  "frontier models correctly answer ... roughly 80% of financial QA questions on the
  first attempt" attributed to `zhang2024financebench`. The published FinanceBench result
  is notably *lower* for several configurations (closed-book performance is poor; even
  strong RAG setups miss a large share). The specific "80%" figure cannot be verified
  locally and risks overstating the benchmark. → NEEDS_EXTERNAL_VERIFICATION. Scope:
  citation.

## MINOR

- **MINOR · citation_accuracy · figure caption chapter.tex:505-514 / exercises.ipynb cell
  [1] — GPT-4 FinQA = 0.68 and BloombergGPT FPB = 0.85.** The notebook itself flags GPT-4
  FinQA as "approx; no official OpenAI FinQA figure — verify" and BloombergGPT FPB as the
  accuracy (not F1) metric. Honest, but the printed figure still ships unverified numbers.
  → NEEDS_EXTERNAL_VERIFICATION. Scope: code-figure.

- **MINOR · non_repetition / notation_crossref · chapter.tex:363 — "The credit chapter
  introduced bias...".** Prose reference to the credit chapter without an explicit
  `\Cref{ch:credit-risk}` hyperlink (the rest of the chapter uses labelled refs). Scope:
  local.

- **MINOR · finance_examples · chapter.tex:531 — illustration points to
  `exercises.ipynb`, "Illustration section".** Correct target (the figure IS generated
  there), but inconsistent with the two `demo.ipynb` pointers — reader cannot tell which
  notebook is canonical. Scope: code-figure.

- **MINOR · completeness · chapter.tex:218-225 — three automation patterns defined but
  the "complete Python implementation" promised at 241-243 is absent** (stub notebook).
  The DAG definition and patterns are not backed by runnable code as the prose implies.
  Scope: local.

- **NIT · concept_separation · whole chapter.** Almost every subsection is wrapped in a
  single large `context` box; there is essentially no `deepdive` box despite under-the-
  hood material (RRF math, SHAP-on-embeddings, KL-divergence drift). Big-picture/internal
  layering is flat. Does not block but caps concept_separation below 90. Scope: local.

## Book-wide items
1. `def:calibration` duplicate label (ch06 + ch07) — fix one. (BLOCKER above.)
2. Stale folder-number references ("Six chapters ago"; `tab:chapter-map` Ch.1–7 column)
   — symptomatic of pre-reorder numbering surviving into prose; audit other near-final
   chapters for the same pattern.
3. SSRN working-paper citations (`NoguerFAIR2025`, `chen2024uncertainty`,
   `didisheim2025memory`, `BaloghDidisheim2025`, `FSB2024stability`, `LopezLira2025trade`)
   — unverifiable locally; book-level external verification pass recommended.
