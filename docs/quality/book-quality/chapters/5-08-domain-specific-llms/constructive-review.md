# Constructive Review — Ch 08 Domain-Specific Financial LLMs (reading index 5)

Audit only. Tags from RUBRIC.md §4.

## What is strong and must be preserved

- **KEEP_AS_SINGLE_SOURCE_OF_TRUTH — Financial language register.** §ch08-financial-language
  (lines 50–105) and `def:ch08-register` give a crisp three-axis characterisation
  (lexical specificity, numeric density, tabular embedding) of why finance text is
  out-of-distribution. This is the cleanest statement of the motivation in the book and
  should be the canonical reference for later chapters (09 sentiment, 14 summarization).

- **GOOD_BIG_PICTURE_EXPLANATION — opening `context` box.** Lines 28–47 frame the
  breadth-vs-specificity tension well and resolve it as "combine, not choose." Good use
  of the `context` environment for the bigger picture.

- **GOOD_TECHNICAL_EXPLANATION — DAPT formalisation.** `def:ch08-dapt` (lines 412–426)
  and the surrounding prose (386–449) correctly describe continued pre-training,
  reduced learning rate to mitigate catastrophic forgetting, token-budget heuristics,
  TAPT, and replay. The math (`eq:ch08-dapt`) is re-derivable and standard.

- **GOOD_FINANCE_EXAMPLE — central-bank communication corpus.** `ex:ch08-corpus-composition`
  (lines 489–518) is concrete, actionable, and realistic: token budgets per source,
  the hawkish/dovish FOMC task, and the honest caveat that the corpus is deliberately
  narrow. Reader can act on it.

- **GOOD_FINANCE_EXAMPLE — cost-optimal classifier.** `ex:ch08-deployment` (lines 808–828)
  walks a compliance team through a hybrid FinBERT+70B routing decision with explicit
  (illustrative) cost arithmetic and the right caveat that break-even is empirical.
  Pairs well with `def:ch08-effective-cost` (768–781).

- **GOOD_TECHNICAL_EXPLANATION — encoder vs decoder heuristic.** `remark` at 348–361
  ("fixed label space → encoder; open-ended output → decoder") is exactly the
  operational guidance a practitioner needs.

- **KEEP — two-FinBERT disambiguation.** Lines 220–241 carefully separate Araci (2019)
  FinBERT from Yang–Uy–Huang (2020) FinBERT/FinBERT-tone. This is a genuine source of
  confusion in the literature and the chapter handles it well; both keys resolve
  distinctly (`araci2019finbert`, `yang2020finbert`).

- **KEEP — contamination & hallucination remarks.** Lines 671–693 add the right caveats
  (data contamination inflating benchmarks; domain pre-training not eliminating
  hallucination) that keep the benchmark numbers honest.

- **KEEP_BUT_CLARIFY — execution-accuracy definition.** `def:ch08-execution-accuracy`
  (603–617) is correct for numeric tolerance matching; clarify that public FinQA
  execution accuracy is typically exact program-execution match, not an $\epsilon$-band,
  so the band framing is a generalisation (see skeptical review).

## Worth keeping but relocate / tighten

- **KEEP_BUT_CLARIFY — encoder–decoder subsection.** §ch08-encoder-decoder (187–208) opens
  by admitting the taxonomy "implicitly omits" the family it then describes. Better to
  fold this third family into `def:ch08-taxonomy` directly so the taxonomy is complete
  rather than self-correcting.

- **KEEP — corpus table.** `tab:ch08-corpus-summary` (523–543) is a useful at-a-glance map;
  numbers are order-of-magnitude and should stay flagged as approximate ("$\sim$").
