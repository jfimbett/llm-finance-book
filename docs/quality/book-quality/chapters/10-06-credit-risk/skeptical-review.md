# Skeptical Review — Ch 06 Credit Risk (reading index 10)

Audit only — no edits applied. Date: 2026-06-20.
Format: `SEVERITY · dimension_key · file:line — issue`. Scope tagged local vs book-wide.

## BLOCKERS

- **BLOCKER · notation_crossref · chapter.tex:382 — `def:calibration` label collides book-wide.**
  `\label{def:calibration}` is defined here (ch06, "Calibration") AND in
  `chapters/07-applications-future/chapter.tex:400` ("Calibration Within Group"). LaTeX emits a
  "multiply-defined labels" warning and any `\ref{def:calibration}` resolves to the *last* one.
  Scope: book-wide. Fix: rename one (e.g. `def:credit-calibration` here). Matches the rubric's
  known-duplicate note (RUBRIC §2.6).
- **BLOCKER · notation_crossref · chapter.tex:299 — `eq:lora` triple label collision.**
  `\label{eq:lora}` is defined in ch02 (`02-llm-foundations/chapter.tex:2189`), ch03
  (`03-llm-training-finetuning/chapter.tex:786`), AND here. Three definitions of the same label →
  broken `\eqref{eq:lora}` resolution book-wide. Scope: book-wide. Fix: rename this one (e.g.
  `eq:lora-credit`) or, preferably, drop the re-derivation and `\Cref` the ch03 SSOT.

## MAJOR

- **MAJOR · correctness · chapter.tex:652 — SR 11-7 date error.** Prose says "In 2012, the Federal
  Reserve and the OCC jointly issued Supervisory Letter SR 11-7." SR 11-7 was issued **April 4,
  2011** (the bib entry `sr117` correctly says `year={2011}`). Internal contradiction + factual
  error. Scope: local. Fix: change "2012" → "2011".
- **MAJOR · non_repetition · chapter.tex:294–301 — LoRA re-derived.** LoRA (ΔW = BA, eq:lora) is
  the single source of truth in ch03 (Training & Fine-Tuning, read #4, `eq:lora` there). Re-deriving
  it with its own equation block here duplicates content instead of cross-referencing. Scope:
  book-repetition. Fix: one-line recap + `\Cref{...}` to ch03; remove the equation (which also
  removes the label collision above).
- **MAJOR · reproducibility · code/notebooks/06-credit-risk/demo.ipynb — demo notebook is a stub.**
  `demo.ipynb` is a single markdown cell listing topics ("Constrained JSON generation…, Platt
  scaling…, isotonic…") with **no code cells**. The chapter's most distinctive technical content
  (structured generation §subsec:structured-gen, calibration §subsec:calibration, persona agents)
  has no runnable companion. Scope: code-figure. Fix: implement the demo or remove the claim that a
  demo exists.
- **MAJOR · reproducibility · code/notebooks/06-credit-risk/exercises.ipynb:cell5 — leftover
  placeholder cell.** Cell 5 is a scaffolding stub: "[Placeholder — fill in with exercise starter
  code when drafting the chapter]". It survives into `exercises_executed.ipynb:cell5` too. The
  chapter's `illustration` (chapter.tex:860–872) points readers to this notebook's "Illustration
  section"; the placeholder undermines that. Scope: code-figure.
- **MAJOR · citation_accuracy · multiple — several quantitative claims are unsourced/unverifiable.**
  All flagged NEEDS_EXTERNAL_VERIFICATION (caps citation_accuracy at 89):
  - chapter.tex:422–423 — "CFPB 2018 study: ~1/3 of mortgage borrowers did not shop; ~$300/yr
    more interest". No citation key; not in bib. Plausible but unverified.
  - chapter.tex:126 — "Sweeney's (2002) finding that 87% … ZIP+DOB+sex". Correct attribution but
    no bib entry / `\cite`. (Sweeney's widely-cited figure; add citation.)
  - chapter.tex:534 / 549 — "Lusardi and Mitchell's (2011) three-question battery". Named in prose
    but no `\cite` and no bib entry.
  - chapter.tex:58 — FICO factor weights (35/30/15/10/10) and FICO 1989 / VantageScore 2006 dates:
    correct to public knowledge but unsourced.

## MINOR

- **MINOR · correctness · chapter.tex:48 — bureau coverage "200–230 million" hedged but unsourced.**
  Hedge language is honest ("figures … vary"); a citation would lift it to ≥90.
- **MINOR · notation_crossref · chapter.tex:379 — forward use of AUROC.** AUROC is used at line 379
  (calibration) before its definition at line 674. *Mitigated* by an explicit inline pointer
  "(defined in Section~\ref{subsec:credit-metrics} below)". Acceptable; not a blocker, but a reader
  meeting AUROC for the first time still hits the term before the definition.
- **MINOR · finance_examples · chapter.tex:552 — currency conflation in persona prompt.** The
  mortgage prompt mixes "\$20,000 / €20,000" and "\$444/€444" for Maria (USD) and Thomas (EUR);
  treating \$ and € as equal amounts is a small realism slip in an otherwise excellent example.
- **MINOR · reproducibility · exercises.ipynb:cell6 — mojibake.** Header "Data Lab � SEC EDGAR"
  (U+FFFD replacement char) and the file is not valid UTF-8 (decode error on byte 0x97 / en-dash).
  Scope: code-figure.
- **MINOR · concept_separation · whole chapter — every section is one big `context` box.** All five
  sections wrap their entire body in a single `context` environment (lines 33, 182, 420, 514, 651,
  878). The book's separation idiom is `context` (big picture) vs `deepdive` (under the hood);
  putting the masked-softmax derivation, SHAP Shapley formula, and Gini proof inside `context`
  blurs that distinction. The reader cannot peel "intuition" from "internals" by box type.

## NIT

- **NIT · citation_hygiene · chapter.tex:64 — `\cite{campbell2006household}` used for "alternative
  data" claim.** Campbell (2006) "Household Finance" is a survey of household finance, a slightly
  loose anchor for an alternative-data sentence; the same key is reused 3× (lines 64, 431, 621) for
  distinct claims, two of which fit better than this one.
- **NIT · pedagogy · chapter.tex:4–27 — 8 learning objectives, no summary/recap.** Objectives are
  strong but the chapter ends abruptly at the deployment section with no closing synthesis tying the
  arc back to the objectives.

## Cross-chapter ordering note

AUROC, KS, Gini, calibration, SHAP are all *defined in this chapter*. Confirm downstream chapters
ch12 (xai) and ch13 (limitations/eval) `\Cref` these definitions rather than re-deriving — and that
they do not redefine `def:calibration` (ch07 already collides; see BLOCKER).
