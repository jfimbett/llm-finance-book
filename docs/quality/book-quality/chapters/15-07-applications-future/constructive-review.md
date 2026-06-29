# Constructive Review — Ch. 07 Applications & Future Trends (reading index 15)

Scope: `book/chapters/07-applications-future/chapter.tex` (598 lines), paired notebooks, figure.
Audit only — no edits.

## Worth keeping (preservation tags)

- **KEEP_AS_SINGLE_SOURCE_OF_TRUTH** — `chapter.tex:116-124` `def:deployment-patterns`
  (zero-shot / RAG / fine-tuning) and `chapter.tex:151-160` `def:arch-families`
  (encoder-only / decoder-only / enc-dec / agentic). This is the book's cleanest
  consolidated taxonomy of LLM deployment choices; the two decision tables
  (`tab:deployment-heuristics` 130-143, `tab:arch-decision` 166-188) are a genuinely
  useful practitioner artifact. GOOD_BIG_PICTURE_EXPLANATION.

- **KEEP / GOOD_FINANCE_EXAMPLE** — `chapter.tex:208-217` `def:workflow-dag` plus the
  three automation patterns (221-225) and three worked finance workflows
  (Earnings-call pipeline 232-233; EDGAR filing monitor 235-236; trade-surveillance
  narrative 238-239). Finance-first, concrete, actionable, and the EDGAR monitor is
  actually implemented in the exercises notebook (real `requests` calls to EDGAR).

- **KEEP / GOOD_TECHNICAL_EXPLANATION** — `chapter.tex:295-300` hybrid retrieval with
  reciprocal-rank-fusion `eq:rrf` ($k=60$). Correct, parameter-free, well-motivated by
  the financial-document numeric-query failure mode (282).

- **KEEP_AS_SINGLE_SOURCE_OF_TRUTH (fairness block)** — `chapter.tex:381-416`:
  `def:demographic-parity`, `def:equalized-odds`, `def:calibration` (within-group),
  and `prop:fairness-impossibility` citing `chouldechova2017fair`. These three fairness
  criteria + impossibility result are not derived in credit-risk; this is their single
  canonical home. Mathematically correct statement of the impossibility result.
  (NOTE: the *label* `def:calibration` collides with credit-risk — see skeptical review;
  the content is fine, the label is the bug.)

- **KEEP / GOOD_BIG_PICTURE_EXPLANATION** — `chapter.tex:453-469` SR 11-7 three-lines-of-
  defence mapped onto LLM specifics, with the SR 11-7 documentation checklist
  `ex:sr117-checklist` (466-469). Strong governance content, finance-grounded.

- **KEEP** — `chapter.tex:480-489` GDPR Art. 22 / MiFID II record-keeping treatment, and
  the OpenClaw privacy-by-default framing (304-317). Ties the chapter to the privacy
  chapter (reading index 16) naturally.

- **KEEP / GOOD_BIG_PICTURE_EXPLANATION** — `chapter.tex:562-590` open-research-problems
  and "Path Forward" close. Five well-scoped open problems, each anchored to a finance
  motivation; the closing is rousing without overclaiming. `chen2024uncertainty`,
  `didisheim2025memory`, `LopezLira2025trade` are woven in to support concrete claims
  (uncertainty quantification, look-ahead/memory bias, multi-agent systemic risk).

- **KEEP** — figure honesty: `exercises.ipynb` cell [1] explicitly flags that GPT-4 FinQA
  (0.68) has no official OpenAI figure and BloombergGPT FPB (0.85) is the accuracy
  metric, with "verify against original papers" warnings. Model commendable transparency.

## Strengths summary
Finance-first throughout; deployment/governance framing is the chapter's unique value
and is not redundant with earlier chapters. Cross-references use `\ref{ch:...}` labels,
not hard-coded numbers. All 26 `\cite` keys resolve.
