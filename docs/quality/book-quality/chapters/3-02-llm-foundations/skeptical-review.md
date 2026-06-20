# Skeptical Review — Chapter 3 (reading order) · `02-llm-foundations`

Audit date: 2026-06-20 · Scope: chapter · Auditor: skeptical-reviewer
File: `book/chapters/02-llm-foundations/chapter.tex`
Format: `SEVERITY · dimension_key · file:line — issue`

---

## A. LOCAL issues (this chapter / its own labels & refs)

- BLOCKER · code_figure_correctness · chapter.tex:1690,1716,1841,1849,1855,2079 — The chapter
  references `code/notebooks/02-llm-foundations/demo.ipynb` **six times** as "The complete Python
  implementation for this example is available in demo.ipynb", but `demo.ipynb` is a **583-byte
  stub** containing a single markdown cell and **zero code**. Every API / structured-generation /
  RAG code promise in the chapter is unfulfilled.

- BLOCKER · correctness · chapter.tex:2563-2595 — Roadmap table `tab:roadmap` ("Chapter-by-Chapter
  Overview") describes a book structure that **does not exist**. It lists "Ch.3 Sentiment Analysis,
  Ch.4 Information Extraction, Ch.5 Earnings Calls, Ch.6 RAG, Ch.7 Fine-tuning, ...". The actual
  book (per `book/main.tex`) has, after this chapter, "Training and Fine-Tuning", "Domain-Specific
  Financial LLMs", "LLM Agents", "Financial NLP and Sentiment", etc. The entire table is stale /
  fabricated relative to the real table of contents. This will mislead every reader.

- MAJOR · notation_crossref · chapter.tex:24,160,346,1339,1405,1425,1427,1819,2501,2502,2519,2527,2560,2598,2599
  — **15 hard-coded "Chapter~N" prose references**, which RUBRIC dim-12 explicitly forbids
  ("no hard-coded chapter-number prose refs"). Worse, the numbers use folder/numeric order and are
  **wrong in reading order**: e.g. line 1339 "Chapter~3 (LLM Training and Fine-Tuning)" and line 1819
  "(Chapter~5)" for RAG do not match either reading order or the (also-wrong) roadmap table.
  Must become `\Cref{ch:...}`.

- MINOR · concept_separation · chapter.tex:48-338, 344-613, 619-1121 — Three of the longest
  `deepdive` blocks (doc-repr, sequential, transformer) run for hundreds of lines with no
  intervening `context` summary. The context/deepdive separation is excellent at section openers
  but a reader who wants only the big picture has no standalone path through the core math sections.

- NIT · pedagogy · chapter.tex:4-19 — Learning Objectives promise "implement structured JSON
  extraction ... using Python" and "Build a retrieval-augmented generation pipeline", but the
  Python that would let the reader *do* this lives only in the stub `demo.ipynb` (see BLOCKER above),
  so the objective is currently unmeetable from the materials.

- NIT · citation_accuracy · chapter.tex:1091-1093 — "over 97% accuracy ... outperforming general
  BERT-base by approximately 8 percentage points" (Araci FinBERT, all-agree split). Plausible and
  consistent with the paper but not verifiable from local files → NEEDS_EXTERNAL_VERIFICATION.

- NIT · citation_accuracy · chapter.tex:2356-2362 — `chen2024uncertainty` "Sharpe ratio ~20% above
  benchmark" claim is specific; not locally verifiable → NEEDS_EXTERNAL_VERIFICATION.

---

## B. BOOK-WIDE issues (cross-chapter; flag for book-level editor)

- BLOCKER · notation_crossref / non_repetition · book-repetition — **12 duplicate `\label`s shared
  with ch01** (`01-intro/chapter.tex`):
  `def:lstm`, `eq:lstm-forget`, `eq:lstm-input`, `eq:lstm-candidate`, `eq:lstm-cell`,
  `eq:lstm-output`, `eq:lstm-hidden`, `eq:rnn-jacobian`, `eq:multihead`, `def:hallucination`,
  `eq:cosine-sim`, `tab:api-costs`.
  ch01 defines `def:lstm` at `01-intro/chapter.tex:1584`, `eq:rnn-jacobian` at :1533,
  `eq:multihead` at :1710, etc. LaTeX will emit "multiply-defined labels" and every `\ref`/`\eqref`
  to these resolves ambiguously. This is a hard build/cross-ref defect.

- BLOCKER · non_repetition / concept_separation · book-repetition — ch01 (reading #1)
  **fully re-derives** the RNN recurrence + vanishing gradient (`01-intro` §"Recurrent Neural
  Networks and the Vanishing Gradient", lines 1473-1614), scaled dot-product attention, and
  multi-head attention (§"Scaled Dot-Product Attention and the Transformer", lines 1615-1710).
  The audit charter designates **ch02 as the single source of truth** for transformer/attention/
  √d_k/multi-head/LSTM/MLM internals — but ch01 currently owns colliding copies. One copy must be
  demoted to a `\Cref` pointer. SSOT decision: keep the derivations in ch02, thin ch01.

- MAJOR · citation_hygiene · citation — Duplicate bib entry: `wei2022emergent` is defined **twice**
  in `book/bibliography.bib` (lines 1727 and 3175), identical content. biber will warn/error on the
  repeated key. Delete one.

- MINOR · progressive_learning · cross-chapter-ordering — The chapter forward-references RAG
  (`sec:rag`) and hallucinations from the landscape/sampling `context` boxes before they are defined
  later in the same chapter; intra-chapter this is fine (all resolve), but combined with the wrong
  roadmap table and wrong Chapter~N refs it muddies the reader's mental model of book order.

---

## Severity roll-up
- BLOCKERS: 4 (demo.ipynb stub; fabricated roadmap table; ch01 label collisions; ch01 SSOT duplication)
- MAJOR: 2 (hard-coded Chapter~N refs; duplicate wei2022emergent bib key)
- MINOR: 3 · NIT: 3
