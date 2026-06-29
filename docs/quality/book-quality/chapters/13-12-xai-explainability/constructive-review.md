# Constructive Review — Ch 12 (read #13) Explainability and Interpretability

Audit only; no edits applied. Date 2026-06-20.

This is a strong, mature chapter. It is finance-first throughout, technically careful,
and unusually honest about the faithfulness/plausibility gap. Most content should be
preserved. Items below are tagged with the preservation vocabulary from RUBRIC.md §4.

## Keep as single source of truth / good technical explanation

- **`KEEP_AS_SINGLE_SOURCE_OF_TRUTH` — Shapley value definition and axioms.**
  `chapter.tex:206-243` (Definition `def:shapley-value`, eq. `eq:shapley-value`) plus the
  Efficiency/Symmetry/Dummy properties (231-238) are the cleanest, most rigorous statement
  of SHAP in the book. The cooperative-game-theory derivation is correct and re-derivable.
  NOTE the conflict flagged in the skeptical review: ch06 (`06-credit-risk/chapter.tex:793-841`,
  read #10, i.e. BEFORE this chapter) independently re-defines SHAP and restates the same
  three axioms. This chapter should be the SSOT; the duplication is a book-wide item.

- **`GOOD_TECHNICAL_EXPLANATION` — attention-as-explanation treatment.**
  `chapter.tex:349-397`. The Jain–Wallace vs Wiegreffe–Pinter debate and its resolution via
  Jacovi–Goldberg's faithfulness/plausibility distinction (`def:faithfulness-plausibility`,
  377-385) is exemplary. The consequence-for-finance framing (387-391) is exactly right.

- **`GOOD_TECHNICAL_EXPLANATION` — faithfulness metrics (sufficiency / comprehensiveness).**
  `chapter.tex:714-748`, eqs `eq:sufficiency`, `eq:comprehensiveness`. Correct, well-motivated,
  and the per-method analysis (745-748: SHAP satisfies efficiency→sufficiency; LIME may fail
  sufficiency; attention fails comprehensiveness) is a genuine technical payoff.

- **`GOOD_TECHNICAL_EXPLANATION` — LIME objective.**
  `chapter.tex:320-333` (`def:lime-objective`, `eq:lime-objective`). Correct fidelity-loss +
  complexity-penalty formulation; the locality kernel is introduced before use (318).

## Good big-picture explanation

- **`GOOD_BIG_PICTURE_EXPLANATION` — opening loan-officer scenario.** `chapter.tex:28-38`
  (`context` box). Concrete, memorable framing of why explainability is a *legal* not merely
  ethical problem. Keep.

- **`GOOD_BIG_PICTURE_EXPLANATION` — stakeholder triad.** `chapter.tex:113-147` (clients /
  regulators / auditors with differing tolerances). A real design insight, not filler.

- **`GOOD_BIG_PICTURE_EXPLANATION` — Rudin rejoinder.** `chapter.tex:172-182` (`remark`).
  Honest treatment of the "just use interpretable models" position and why structured+text
  fusion complicates it. Keep.

## Good finance examples

- **`GOOD_FINANCE_EXAMPLE` — SHAP credit attribution.** `chapter.tex:254-289`
  (`ex:shap-credit`). Token-level attributions tied to an ECOA adverse-action statement;
  the values sum sensibly toward the 0.36 prediction gap. Clearly labelled illustrative.

- **`GOOD_FINANCE_EXAMPLE` — hybrid 3-stage credit pipeline.** `chapter.tex:553-590`
  (`ex:hybrid-credit-pipeline`). The structured prompt with explicit "do not introduce
  factors not listed" guardrail is a reusable, realistic pattern.

- **`GOOD_FINANCE_EXAMPLE` — MiFID II suitability disclosure.** `chapter.tex:673-701`
  (`ex:mifid-disclosure`). The 0.3% revision rate is correctly hedged as illustrative
  ("For illustration, suppose…", 698), which is the right way to present synthetic numbers.

## Keep but clarify

- **`KEEP_BUT_CLARIFY` — KernelSHAP parenthetical.** `chapter.tex:263`. The inline gloss
  "(a LIME-based Shapley approximation using a specific kernel choice; see Definition
  `def:lime-objective`)" forward-refers to LIME, which is defined two subsections later
  (299-333). Mild forward dependency; either soften or move. See concept-ordering note.

- **`KEEP_BUT_CLARIFY` — explanation-trace faithfulness definition.** `chapter.tex:435-441`
  (`def:explanation-trace`). The nested parenthetical defining "counterfactually faithful"
  inside the `\emph{}` is hard to parse. Content is correct; presentation could be split.

## Concept separation

The chapter uses `context` for big-picture framing and `remark` for caveats, but makes
**no use of `deepdive`** despite heavy under-the-hood material (Shapley combinatorics,
KernelSHAP marginalisation, gradient attribution). Dimension 2 is good, not excellent,
largely because the technical/intuitive layers are interleaved in body prose rather than
boxed. This is an enhancement, not a defect — do not over-box working content.
