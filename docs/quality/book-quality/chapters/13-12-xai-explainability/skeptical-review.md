# Skeptical Review — Ch 12 (read #13) Explainability and Interpretability

Audit only; no edits applied. Date 2026-06-20.
Format: `SEVERITY · dimension_key · file:line — issue`. Scope: local vs book-wide.

## BLOCKERS

- `BLOCKER · notation_crossref · book/chapters/12-xai-explainability/chapter.tex:890` —
  `\ref{ch:responsible-llms}` points to a label that **does not exist anywhere in the book**
  (verified: no `\label{ch:responsible-llms}` in any `book/chapters/*/chapter.tex`). There is
  no dedicated responsible-AI/fairness chapter. This renders as `??` in the PDF. Scope: local
  (the dangling ref is in this chapter) but the *root cause* is book-wide (missing chapter /
  wrong target). The "Further Reading" sentence claims a chapter "addresses fairness and bias…
  related to the non-discrimination requirements of ECOA" that has no home.

- `BLOCKER · citation_accuracy · book/chapters/12-xai-explainability/chapter.tex:393` —
  Misattribution. The text cites `\cite{sundararajan2020shapley}` for **Integrated Gradients**
  ("Gradient-based attribution methods, such as Integrated Gradients"). But the bib entry
  `sundararajan2020shapley` (bibliography.bib:2480) is Sundararajan & Najmi (2020), *"The Many
  Shapley Values for Model Explanation"* (ICML) — a paper about Shapley-value variants, NOT the
  Integrated Gradients paper. Integrated Gradients is Sundararajan, Taly & Yan (2017),
  *"Axiomatic Attribution for Deep Networks"*. The cited key is the wrong paper for the
  proposition; that key is also the *only* Sundararajan entry in the .bib, so the correct IG
  reference is simply missing. Scope: citation (local).

## MAJOR

- `MAJOR · non_repetition · book/chapters/12-xai-explainability/chapter.tex:197-243`
  vs `book/chapters/06-credit-risk/chapter.tex:793-841` — SHAP is **fully re-defined twice**.
  ch06 (read #10, earlier) independently introduces "SHAP (SHapley Additive exPlanations)…
  rooted in cooperative game theory", restates the same Efficiency/Symmetry/Dummy axioms, and
  gives its own SHAP waterfall example — without deferring to this chapter. ch11 (read #12)
  *does* defer "deeper treatment of SHAP-based explainability" to ch06, NOT here
  (`11-regtech-compliance-aml/chapter.tex:439`). So in reading order the SSOT is ambiguous and
  ch06 is the de-facto first/SSOT, yet this chapter re-derives from scratch with no cross-ref
  back. One concept, two full derivations. Scope: book-repetition / cross-chapter-ordering.

- `MAJOR · concept_ordering · book/chapters/06-credit-risk/chapter.tex:793` (book-wide) —
  SHAP and the Shapley formula are *used and defined* in ch06 (read #10), three chapters before
  the designated SSOT chapter (this one, read #13). ch06 line 439 of ch11 calls this chapter the
  one that "covers interpretability methods in full generality", implying THIS is the canonical
  introduction — but the canonical introduction comes *after* two chapters that already lean on
  SHAP. Either ch06 should cross-ref forward to `ch:xai-explainability` for the formal Shapley
  definition, or this chapter should be moved earlier. AUROC is self-contained in ch06
  (defined in §`subsec:credit-metrics`, not used before definition), so the AUROC half of the
  prompt's hypothesis does NOT reproduce — only SHAP does. Scope: cross-chapter-ordering.

- `MAJOR · reproducibility · code/notebooks/12-xai-explainability/demo.ipynb` —
  `demo.ipynb` is a 2-cell stub: it imports numpy/pandas and prints "Chapter 12 demo notebook".
  It demonstrates none of the chapter's methods (no SHAP, LIME, attention, CoT, counterfactual,
  sufficiency/comprehensiveness). The chapter's claim that text-SHAP is "reproducible given the
  random seed" (588) has no runnable companion. The `exercises.ipynb` IS real and substantial
  (EDGAR fundamentals, logistic regression, leave-one-out attribution, model card) and is
  honest that LOO ≠ SHAP, but it does not regenerate any in-chapter figure/table. Scope: local.

## MINOR

- `MINOR · code_figure_correctness · book/chapters/12-xai-explainability/figures/` —
  Figures directory is empty (only `.gitkeep`); the chapter contains **no `\includegraphics` and
  no `figure` environment**. No figure contradicts prose because there are no figures. Dimension 3
  is therefore scored on the worked numeric tables/examples only (which are internally consistent
  and labelled illustrative). Not a defect, but the absence of any visual (e.g. a SHAP waterfall
  or attention heatmap) for a chapter whose subject is *visualisation of attributions* is a
  pedagogical gap. Scope: local.

- `MINOR · concept_ordering · book/chapters/12-xai-explainability/chapter.tex:263` —
  Forward reference: KernelSHAP is glossed as "a LIME-based Shapley approximation… see
  Definition `def:lime-objective`" inside `ex:shap-credit`, but `def:lime-objective` appears later
  at 320-333. Minor use-before-definition (mitigated by the explicit forward `\ref`). Scope: local.

- `MINOR · completeness · book/chapters/12-xai-explainability/chapter.tex:393-397` —
  Integrated Gradients is introduced as the recommended "audit-grade" gradient method but never
  defined (no formula, no path-integral statement). For a chapter this rigorous about SHAP/LIME,
  the asymmetry is noticeable. A one-line definition or explicit "out of scope" would close it.
  Scope: local.

- `MINOR · citation_accuracy · book/chapters/12-xai-explainability/chapter.tex:511-520,639-647` —
  Eight SSRN working papers (`RaneChoudharyRane2023`, `MohsinNasim2025`, `TatsatShater2025`,
  `CetintavEtAl2024`, `Schmitt2024`, `Desai2024`, `Lakarasu2024`) and the `cfainstitute2025xai`
  report carry substantive claims ("GPT-4o translates SHAP outputs", "five regulatory audit
  categories including BSA/AML", "Article 13 transparency obligations") that cannot be verified
  against the source from the repo. Mark `NEEDS_EXTERNAL_VERIFICATION` (caps citation_accuracy at
  89). Keys resolve and are well-formed; this is accuracy-of-description, not hygiene. Scope: citation.

- `MINOR · citation_hygiene · book/bibliography.bib:wei2022emergent` —
  `wei2022emergent` is a **duplicate key** in the shared bibliography (appears twice). NOT cited
  by this chapter, so it does not affect this chapter's compile, but it is a book-level hygiene
  defect in the .bib this chapter depends on. Scope: book-wide / citation.

## NIT

- `NIT · pedagogy · book/chapters/12-xai-explainability/chapter.tex:801-802` —
  "Research consistent with CFA Institute guidance suggests that explanations may reduce
  overreliance" hedges heavily ("may", "consistent with"); fine as written but borders on a claim
  doing rhetorical work without a primary empirical cite. Scope: local.

- `NIT · notation_crossref · book/chapters/12-xai-explainability/chapter.tex:135` —
  "The According to the CFA Institute" — stray leftover word "The" before "According" (grammar).
  Scope: local.
