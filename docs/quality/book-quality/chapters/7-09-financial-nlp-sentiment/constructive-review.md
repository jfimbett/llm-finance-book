# Constructive Review — Ch 09 Financial NLP and Sentiment Analysis (reading index 7)

Audit only — no edits applied. Date: 2026-06-20.

This chapter is, by content, one of the strongest in the book: a coherent finance-first
arc from "text as data" through methods, applications by source, signal construction, and
production engineering. The task below is to preserve that strength while flagging real
issues for the editor. Preservation tags follow RUBRIC §4.

## Worth keeping (preservation-tagged)

- **`KEEP_AS_SINGLE_SOURCE_OF_TRUTH` — Sources taxonomy (sec:ch09-text-sources, lines 39–86).**
  The four-axis framing (frequency / curation / audience / regulatory oversight) and the
  per-source treatment (social, wires/news, earnings calls, SEC filings, central bank) is
  the most complete and best-organised treatment of financial text sources in the book.
  This should be the designated single source of truth; other chapters should `\Cref` here.

- **`GOOD_TECHNICAL_EXPLANATION` — LM vs Harvard GI contrast (lines 141–171).**
  The "liability/tax/cost are neutral in finance" explanation of why a finance lexicon is
  needed is precise and correctly attributed to `loughran2011liability`. The net-sentiment
  ratio (eq:lm-sentiment) and worked MD&A example (ex:lm-example, lines 150–169) are a
  clean, re-derivable illustration. Note the worked arithmetic (-3/35 ≈ -0.086) is correct.

- **`GOOD_TECHNICAL_EXPLANATION` — FinBERT classifier head (eq:finbert-classifier, lines 183–192).**
  Softmax-over-[CLS] formulation is correct and the context-sensitivity advantage over
  lexicons (negation, hedging) is well argued. Cross-references BERT architecture to
  `ch:llm-foundations` rather than re-deriving — exactly right.

- **`GOOD_TECHNICAL_EXPLANATION` — Krippendorff's alpha (sec:ch09-evaluation, lines 521–534).**
  Both nominal and ordinal variants given; the α≥0.667 / α≥0.800 thresholds are the
  standard Krippendorff values. The ordinal difference function is correctly stated. The
  caveat that macro-F1 matters because "neutral" dominates (lines 552–563) is an excellent,
  finance-aware point.

- **`GOOD_BIG_PICTURE_EXPLANATION` — Short- vs long-horizon predictability (sec:ch09-horizon-predictability, lines 433–448).**
  The attention/price-pressure vs fundamental-information dichotomy, and the closing remark
  (lines 446–448) on why academia targets long horizon and industry the short, is a genuinely
  useful synthesis.

- **`GOOD_FINANCE_EXAMPLE` — Fine-tuning FinBERT on earnings-call sentences (ex:finbert-finetuning, lines 293–310).**
  End-to-end, realistic, with concrete hyperparameters and the honest "illustrative order of
  magnitude" framing on F1 (0.70–0.80 vs 0.60–0.65). Reader can act on it.

- **`KEEP` — Signal-construction section (sec:ch09-sentiment-to-signal, lines 359–448).**
  Z-scoring within industry-year (eq:zscore-sentiment), stationarity/unit-root caveats,
  sentiment-inflation warning, CAR definition (def:car) and the SUE-conditioned predictive
  regression (eq:sentiment-predictive-regression) are all correct and finance-grounded.

- **`GOOD_FINANCE_EXAMPLE` — SVB bank-run and mutual-fund-flow studies (lines 247–249, 593).**
  `cookson2026bankrun` (JFE 2026) and `gilbazo2025tweeting` (Management Science 2025) are
  real, published, peer-reviewed entries (verified in bibliography.bib) and tie social-media
  text to concrete financial outcomes. Strong, current, defensible.

- **`KEEP` — Production engineering (sec:ch09-inference-at-scale, lines 492–513).**
  Batch vs streaming, ONNX/quantisation, <100 ms FOMC latency, distillation — this is the
  industry-practitioner content the mixed audience needs and few textbooks include.

## Cross-cutting strengths

- Finance-first throughout: every method is motivated by a financial decision problem.
- Honest about limitations (replication caveats on `bollen2011twitter`, reverse causality
  in social media, information-vs-policy effect in FOMC text). This restraint is valuable.
- Exercises notebook (`exercises.ipynb`) is real and substantive (EDGAR + yfinance event
  study), with [B]/[I]/[A] difficulty tags — keep it.
