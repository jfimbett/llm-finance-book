# Constructive Review — Ch 06 Credit Risk (reading index 10)

Audit only — no edits applied. Date: 2026-06-20.

This chapter is a strong, finance-first treatment with deep regulatory grounding and
mathematically careful derivations. The list below tags content worth protecting.

## KEEP_AS_SINGLE_SOURCE_OF_TRUTH

- **Gini = 2·AUROC − 1 derivation (lines 716–729).** A complete, correct change-of-variables
  proof from the CAP/Lorenz construction, ending with the exact identity. This is the book's
  natural single source of truth for the Gini/AUROC relationship. KEEP_AS_SINGLE_SOURCE_OF_TRUTH.
- **AUROC formal definition + probabilistic interpretation (lines 662–676, eq:auroc).** Clean
  TPR/FPR setup and the "P(S_+ > S_-)" interpretation. AUROC is *defined here*, not deferred to
  ch12/ch13, so this is the SSOT for discrimination metrics. KEEP_AS_SINGLE_SOURCE_OF_TRUTH.
- **KS statistic definition + empirical estimator (def:ks, eq:ks-empirical, lines 682–704).**
  Rigorous, with the correct argument that the sup is attained at an observed support point.
  KEEP_AS_SINGLE_SOURCE_OF_TRUTH.
- **Calibration definition (def:calibration, eq:calibration, lines 381–390).** Correct conditional-
  expectation definition plus reliability-diagram operationalisation. KEEP — but see the label-
  collision BLOCKER in the skeptical review (the *label* must be renamed, not the content).

## GOOD_TECHNICAL_EXPLANATION

- **Structured generation / constrained decoding (sec, lines 305–373).** The masked-softmax
  derivation (eq:softmax, eq:constrained-softmax) and the digit-by-digit JSON float example
  (lines 339–364) are an unusually clear and correct account of grammar-constrained decoding for
  probability extraction. The caveat that p̂ is "the floating-point number the model was guided to
  express," not its confidence, is an excellent and honest framing (line 364).
- **Platt vs. isotonic calibration (lines 392–412).** Both methods correctly stated; the remark on
  when to prefer each (data size, monotonicity, ECE/Brier evaluation) is practically actionable.
- **SHAP axioms + waterfall→reason-code mapping (lines 796–842).** The efficiency/symmetry/dummy
  axioms are correctly stated and the link from SHAP waterfall to FCRA adverse-action reason codes
  is the chapter's best technical-to-regulatory bridge.

## GOOD_FINANCE_EXAMPLE

- **Apple Card / Goldman Sachs cold-open (lines 35–39).** Real, well-known 2019 episode that
  motivates the entire regulatory framing. GOOD_BIG_PICTURE_EXPLANATION.
- **Maria & Thomas personas (ex:personas, lines 544–572).** Genuinely contrasting, grounded
  household profiles whose reasoning chains are coherent and pedagogically illuminating (loss-
  aversion vs. break-even analysis). Reader can act on the mechanism. GOOD_FINANCE_EXAMPLE.
- **Borrower-profile serialisation example (ex:serialisation, lines 268–290).** Concrete tabular→
  text template the reader can copy. GOOD_FINANCE_EXAMPLE.
- **Inference API request/response + plain-language GDPR explanation (ex:api lines 895–940;
  ex:gdpr-explanation lines 1047–1056).** Realistic, end-to-end, regulation-aware artifacts the
  reader can directly reuse. GOOD_FINANCE_EXAMPLE.
- **SHAP waterfall table (tab:shap-waterfall, lines 815–840).** Internally consistent (base 0.05 →
  final 0.102; values match the API response). GOOD_FINANCE_EXAMPLE.

## GOOD_BIG_PICTURE_EXPLANATION

- **Credit-risk modelling arc (lines 188–242):** Z-score → Merton → reduced-form → GBT → LLMs is a
  well-sequenced historical narrative that motivates *when* an LLM adds value (text-native features,
  thin-file borrowers, covenant reasoning). KEEP.
- **SR 11-7 three-pillar framing (lines 651–769)** and the **vintage/TTC-vs-PIT discussion
  (lines 772–790)** are finance-orientation strengths rarely found in ML texts.

## KEEP_BUT_CLARIFY

- **Merton block (lines 202–219)** and **reduced-form survival probability (eq:survival-prob).**
  Correct, but these are likely re-derived elsewhere (valuation/risk chapters). Confirm a single
  SSOT and cross-reference rather than re-derive (see non_repetition note).
- **LoRA block (lines 294–301, eq:lora).** Correct (factor-48 reduction verified), but LoRA's SSOT
  is ch03 (Training & Fine-Tuning, read #4). Keep a one-line recap + `\Cref`, drop the re-derivation,
  and fix the colliding `eq:lora` label (see skeptical review BLOCKER).
