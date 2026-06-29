# Skeptical Review — Ch. 11 RegTech, Compliance, AML (reading index 12)

**Date:** 2026-06-20 · **Scope:** chapter · **Audit only — no edits.**
Format: `SEVERITY · dimension_key · file:line — issue`. Scope tag: local / book-wide.

## BLOCKER

- `BLOCKER · notation_crossref · book/chapters/11-regtech-compliance-aml/chapter.tex:172`
  — references `Figure~\ref{fig:ch11-rag-pipeline}` ("Figure~\ref{...} describes the
  dataflow conceptually"), but there is **no `\begin{figure}` and no
  `\label{fig:ch11-rag-pipeline}` anywhere in the chapter**, and `figures/` contains
  only `.gitkeep` (zero figure files). This is a dangling `\ref` → compiles to "Figure
  ??" and breaks the cross-reference gate. (local)
- `BLOCKER · code_figure_correctness · figures/ + chapter.tex:172` — the prose
  promises a dataflow figure that does not exist. Either the figure must be created or
  the sentence/`\ref` removed. (local / code-figure)

## MAJOR

- `MAJOR · citation_accuracy · chapter.tex:162,197,431 (key chen2025aml)` — the
  Adverse Media Index is attributed to `chen2025aml`, an arXiv entry with ID
  `arXiv:2602.23373` (bibliography.bib). `2602` decodes to **Feb 2026**, which is in
  the *future* relative to the entry's `year=2025` and to the chapter; the AMI
  formula `eq:ami-score` is presented as "developed in this chapter" yet credited to
  this paper. The arXiv ID is internally inconsistent and very likely fabricated.
  NEEDS_EXTERNAL_VERIFICATION; if unverifiable, the attribution should be softened to
  "as formalised here" and the citation removed. (citation)
- `MAJOR · non_repetition · chapter.tex:93–104 vs book/chapters/15-privacy-local-models/chapter.tex:54–63,426–434`
  — GDPR Articles 5, 17, 22 are explained in detail in BOTH ch11 and ch15
  (privacy), with NO cross-reference in either direction. Two competing sources of
  truth for the same statutory provisions; the two chapters even use different bib
  keys for GDPR (`euaiact2024`/none here vs `gdpr2016` in ch15). One must be SSOT and
  the other `\Cref` to it. (book-wide / book-repetition)
- `MAJOR · non_repetition · chapter.tex:75–82 vs ch15:54` — MiFID II is also
  re-introduced in both chapters; same SSOT problem, smaller scope. (book-wide)
- `MAJOR · reproducibility · code/notebooks/11-regtech-compliance-aml/demo.ipynb`
  — `demo.ipynb` is a stub: it imports numpy/pandas and prints "Chapter 11 demo
  notebook" with zero implementation of any chapter concept (no RRF, no AMI, no entity
  resolution, no XBRL retrieval). None of the chapter's equations
  (`eq:rrf-fusion`, `eq:ami-score`, `eq:xbrl-retrieval-score`) is demonstrated.
  (code-figure)

## MINOR

- `MINOR · citation_hygiene · book/bibliography.bib (fincen2020aml)` — entry carries
  an inline `% [CITE: verify precise report title]` flag and a `note` that hedges the
  content ("Covers SAR filing rates and estimates of false-positive burden"). The
  precise FinCEN report title is unverified. The chapter leans on this key for the
  load-bearing 95–99% FPR claim (line 137) and the "excessive low-quality SARs"
  criticism (line 140). NEEDS_EXTERNAL_VERIFICATION. (citation)
- `MINOR · citation_accuracy · chapter.tex:43,290,142,165 (SSRN keys
  AndhovAmparo2024, Passador2024, ViracachaP2024, Anand2025, Shirvanporzour2025,
  Ngam2026, IoannidesEtAl2023)` — seven `@unpublished` SSRN working papers cited with
  specific claims about their content; all resolve in the bib but none is locally
  verifiable. The descriptions are plausible and well-matched to titles, but the
  attributed specifics (e.g. Ngam2026's "Perceive-Reason-Act loop … compiles
  regulatory text into executable AML detection features", line 165) cannot be
  checked. NEEDS_EXTERNAL_VERIFICATION → caps citation_accuracy at 89. (citation)
- `MINOR · correctness · chapter.tex:137` — "AML screening systems operate with FPR
  values between 95% and 99%". The quantity practitioners usually cite at this
  magnitude is the *false-discovery rate* (1 − PPV, share of alerts that are false),
  not FPR = |P̂∩N|/|N| as just defined in `eq:fpr-aml` (line 135). With that
  denominator (all true negatives), 95–99% FPR is implausibly high. The number is
  being used as 1−PPV but labelled FPR — a definitional slip in an otherwise careful
  definition box. (local)
- `MINOR · completeness · chapter.tex:223–281 (KYC/sanctions section)` — sanctions
  screening is motivated (OFAC/EU/UN, line 227) but the chapter never states the
  asymmetric-cost / near-100%-recall threshold rationale until `def:entity-resolution`
  line 251; a one-line caveat earlier that *missing* a sanctions hit is categorically
  worse than a false positive would tighten the bridge. (local)

## NIT

- `NIT · notation_crossref · chapter.tex:33,98,118` British spelling
  ("digitalisation", "minimisation", "programmes") — consistent within the chapter;
  verify it matches the book-wide convention. (local)
- `NIT · concept_separation · chapter.tex` — the chapter uses `context`, `definition`,
  `example`, `remark` well but never uses a `deepdive` box; the heavier architectural
  detail (RAG internals, RRF math) sits in plain body text. Acceptable, but a
  `deepdive` wrapper around lines 180–188 would sharpen the big-picture/internals
  split. (local)
