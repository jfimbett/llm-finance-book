# Editor Plan — Ch 12 (read #13) Explainability and Interpretability

Audit only; no edits applied. Date 2026-06-20. Iteration 0.
Smallest targeted changes to bring every dimension ≥90.

## MUST_FIX (blockers — chapter cannot pass)

1. **Fix dangling `\ref{ch:responsible-llms}`** — `chapter.tex:890`.
   No such label exists in the book. Either (a) retarget to an existing chapter that actually
   covers fairness/non-discrimination — `ch:credit-risk` (06) has the closest disparate-impact /
   ECOA fairness content — or (b) drop the sentence's cross-ref and keep the standalone claim, or
   (c) create the missing responsible-AI chapter at book level. Quickest local fix: retarget to
   `\Cref{ch:credit-risk}` (which already discusses ECOA non-discrimination). Fixes notation_crossref.

2. **Correct the Integrated Gradients citation** — `chapter.tex:393`.
   `\cite{sundararajan2020shapley}` is the wrong paper (it is "The Many Shapley Values", ICML 2020).
   Add a new bib entry for Sundararajan, Taly & Yan (2017), "Axiomatic Attribution for Deep
   Networks" (e.g. key `sundararajan2017axiomatic`) and cite that for Integrated Gradients. Do NOT
   reuse `sundararajan2020shapley`. Fixes citation_accuracy.

## SHOULD_FIX (majors — lift dimensions to release floor)

3. **Resolve the SHAP double-derivation (book-wide).** Designate ONE SSOT. Recommended: keep the
   full Shapley derivation HERE (`chapter.tex:206-243`) as the canonical statement, and in ch06
   (`06-credit-risk/chapter.tex:793-841`) replace the re-derivation of the axioms with a forward
   `\Cref{ch:xai-explainability}` reference, retaining only the credit-specific waterfall example.
   Add a back-reference here noting ch06's credit application. Lifts non_repetition; coordinates
   with the cross-chapter-ordering item below.

4. **Add a forward bridge from ch06 to this chapter for the Shapley formula** —
   `06-credit-risk/chapter.tex:796`. Since SHAP is *used* in ch06 (read #10) before its formal
   game-theoretic definition here (read #13), ch06 should say the axiomatic derivation is given in
   `\Cref{ch:xai-explainability}`. Lifts concept_ordering for the book; this chapter itself has no
   internal use-before-definition of SHAP.

5. **Replace or fill `demo.ipynb`** — `code/notebooks/12-xai-explainability/demo.ipynb`.
   Currently a 2-cell print stub. Either (a) make it a real demo of at least one in-chapter method
   (KernelSHAP token attribution on a toy BERT, or the LOO attribution already proven in
   `exercises.ipynb`), or (b) delete it and point the chapter to `exercises.ipynb` as the companion.
   Lifts reproducibility.

## OPTIONAL (minors/nits — polish toward 95)

6. Define Integrated Gradients in one line (path-integral of gradients from a baseline) at
   `chapter.tex:393-397`, or mark explicitly out of scope. (completeness)
7. Move/soften the KernelSHAP→LIME forward gloss at `chapter.tex:263`. (concept_ordering)
8. Add one figure: a SHAP waterfall or attention heatmap, regenerated from a notebook, for a
   chapter about attribution *visualisation*. (code_figure_correctness / pedagogy)
9. Fix grammar "The According to the CFA Institute" at `chapter.tex:135`. (notation_crossref nit)
10. Tighten the hedged CFA overreliance claim at `chapter.tex:801-802`. (pedagogy nit)
11. De-nest the "counterfactually faithful" parenthetical in `def:explanation-trace`
    (`chapter.tex:435-441`). (pedagogy)

## DO_NOT_CHANGE (protect)

- Shapley definition + axioms `chapter.tex:206-243` (SSOT candidate).
- Attention-as-explanation debate + faithfulness/plausibility `chapter.tex:349-397`.
- Faithfulness metrics (sufficiency/comprehensiveness) `chapter.tex:714-748`.
- LIME objective `chapter.tex:320-333`.
- Opening loan-officer `context` `chapter.tex:28-38`; stakeholder triad `113-147`; Rudin remark
  `172-182`.
- Worked finance examples: `ex:shap-credit` (254-289), `ex:hybrid-credit-pipeline` (553-590),
  `ex:mifid-disclosure` (673-701) — all correctly hedged as illustrative; keep the hedging.
- The honest LOO≠SHAP caveat in `exercises.ipynb` (cell-6) — do not overclaim it as SHAP.

## BOOK_WIDE_ITEMS

- **BW1 (concept_ordering / non_repetition):** SHAP defined+used in ch06 (read #10) and re-derived
  in ch12 (read #13). Designate SSOT (recommend ch12), add forward ref from ch06, strip ch06's
  axiom re-derivation. ch11 already defers to ch06 — reconcile so all three point to one SSOT.
- **BW2 (notation_crossref):** `\ref{ch:responsible-llms}` has no target in the book — either a
  missing responsible-AI/fairness chapter or a mis-typed label. Affects ch12:890; audit other
  chapters for the same dangling label.
- **BW3 (citation_hygiene):** Duplicate BibTeX key `wei2022emergent` in `book/bibliography.bib`.
  Book-level cleanup; not cited by ch12 but in its dependency.
- **BW4 (citation_accuracy):** Missing canonical Integrated Gradients reference
  (Sundararajan, Taly & Yan 2017) in the shared `.bib`; the present `sundararajan2020shapley`
  is a different paper. Add it book-wide.
