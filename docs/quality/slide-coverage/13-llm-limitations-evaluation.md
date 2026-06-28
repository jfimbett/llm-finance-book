# Slide Coverage Checklist — Chapter 13-llm-limitations-evaluation

Source: `book/chapters/13-llm-limitations-evaluation/chapter.tex`
Generated during deck overhaul (2026-06-28).

---

## Sections and Subsections

- [x] §1 Calibration and Overconfidence
- [x] §1.1 What Calibration Means: Reliability Diagrams and ECE
- [x] §1.2 Overconfidence in LLM Financial Outputs
- [x] §1.3 Measuring and Improving Calibration
- [x] §2 Temporal Leakage and Look-Ahead Bias
- [x] §2.1 How Pretrained Models Can Memorize Future Events
- [x] §2.2 Point-in-Time Data Requirements and Anonymization
- [x] §2.3 Designing Contamination-Resistant Evaluation Splits
- [x] §3 Stock Movement Prediction: A Cautionary Tale
- [x] §3.1 The Theoretical Case: Efficient Markets and the Information Barrier
- [x] §3.2 Empirical Evidence: LLMs Achieve 51–65% Accuracy on 250 Stocks
- [x] §3.3 ARIMA, LSTM, and When Simpler Models Outperform LLMs
- [x] §4 Evaluation Beyond Classification Accuracy
- [x] §4.1 Economic Value Metrics: Sharpe Ratio, Alpha Generation, Information Ratio
- [x] §4.2 Walk-Forward Tests and Expanding-Window Validation
- [x] §4.3 Trading-Grade Evaluation: Transaction Costs, Capacity, Drawdown
- [x] §5 Hallucination in Financial Contexts
- [x] §5.1 Fabricated Citations, Incorrect Numerical Facts, Phantom Companies
- [x] §5.2 Grounding Strategies: RAG, Retrieval Verification, Tool Use
- [x] §5.3 Hallucination Benchmarks for Financial Applications
- [x] §6 Summary (five fragilities wrapped up)
- [x] §7 Further Reading (by theme)

---

## Named Methods / Models / Results

- [x] Perfect calibration definition (Def. 13.1)
- [x] Reliability diagram / calibration curve
- [x] Expected Calibration Error (ECE) — Guo et al. (2017)
- [x] Maximum Calibration Error (MCE)
- [x] Adaptive binning (equal-mass bins) — Niculescu-Mizil & Caruana (2005)
- [x] RLHF-induced overconfidence — Ouyang et al. (2022)
- [x] Token-level vs. claim-level confidence
- [x] Distributional shift in financial LLMs — Zhao et al. (2025)
- [x] Bang et al. (2023) — systematic overconfidence on factual tasks
- [x] Chen, Green, Gulen & Zhou (2024) — extrapolation bias and over-optimism in LLM return forecasts
- [x] Verbalized confidence elicitation — Wang et al. (2023)
- [x] Temperature scaling — Guo et al. (2017)
- [x] Isotonic regression — Zadrozny & Elkan (2002)
- [x] Platt scaling — Platt (1999)
- [x] Conformal prediction — Angelopoulos & Bates (2022)
- [x] SR 11-7 model monitoring guidance
- [x] Temporal leakage / memorization problem
- [x] Three leakage channels — Ziemke et al. (2024): direct memorisation, outcome narratives, imbalanced corpora
- [x] Lopez-Lira, Tang & Zhu (2025) — LLMs memorise exact numerical values of financial variables
- [x] Noguer i Alonso (2024) — practitioner taxonomy of look-ahead bias sources
- [x] Point-in-time (PIT) data (CRSP/Compustat)
- [x] Hard temporal cutoffs (≥3-month safety margin)
- [x] Document-level timestamps
- [x] Contextual anonymisation ("Apple" → "Company X")
- [x] Contamination-resistant temporal split definition (Def. 13.2)
- [x] Gap period Δ ≥ prediction horizon h + publication lag
- [x] N-gram deduplication (13-grams, MinHash LSH)
- [x] Factual probing
- [x] Date-blinding ablations
- [x] Rahimikia & Drinkall (2024) — year-specific LLMs outperform larger off-the-shelf models
- [x] Gao, Jiang & Yan (2025) — Lookahead Propensity (LAP) measure
- [x] Contamination audit example (Ex. 13.2): 34/500 flagged, accuracy 62% → 54%
- [x] Efficient Market Hypothesis — Fama (1970, 1991)
- [x] Grossman–Stiglitz impossibility theorem — Grossman & Stiglitz (1980)
- [x] Tetlock (2007); Bollen et al. (2011) — early text-based signals
- [x] Harvey (2016) — alpha decay from factor crowding
- [x] Three residual LLM value channels: synthesis at scale, novel reasoning, private text
- [x] Lopez-Lira & Tang (2023) — ChatGPT headline sentiment, statistically significant short-horizon accuracy
- [x] Vidal (2024) — four LLMs on 30-day S&P 500 direction, accuracy marginally above chance
- [x] Zhao et al. (2025) meta-analysis — accuracy 51–65%, upper end from artefacts
- [x] Four methodological vulnerabilities that inflate to >62%
- [x] CFA Institute (2025) — durable alpha unlikely in liquid markets
- [x] ARIMA-GARCH — Box & Jenkins (1970)
- [x] LSTM — Hochreiter & Schmidhuber (1997)
- [x] Three conditions favouring simpler models (text irrelevance, short history, regime changes)
- [x] Sharpe ratio — Sharpe (1994)
- [x] Information ratio (IR) — Grinold & Kahn (1999)
- [x] Fundamental law of active management: IR ≈ IC · √N
- [x] Information Coefficient (IC) — rank correlation of predicted vs. realised returns
- [x] Factor alpha regression (Fama–French: MKT, SMB, HML) — Fama & French (1993)
- [x] Walk-forward validation
- [x] Expanding-window (anchored walk-forward) — Lopez de Prado (2018)
- [x] Purge period Δ_purge ≥ h
- [x] Walk-forward definition with purge (Def. 13.3)
- [x] PEFT / LoRA reference for walk-forward cost
- [x] Transaction cost formula: c_round-trip = 2τ(half-spread + market impact)
- [x] Almgren–Chriss framework — temporary market impact ≈ η(q/V)
- [x] Maximum drawdown (MDD) formula
- [x] Calmar ratio
- [x] Complete trading-grade checklist (6 items)
- [x] Hallucination: fabricated citations — Bang et al. (2023)
- [x] Hallucination: incorrect numerical facts — Kang et al. (2023)
- [x] Hallucination: phantom companies/executives
- [x] Hallucination: anachronistic facts — Ji et al. (2023)
- [x] RAG — Lewis et al. (2020)
- [x] Retrieval verification / FActScore — Min et al. (2023)
- [x] Tool use / function calling — Schick et al. (2023)
- [x] Self-consistency sampling — Wang et al. (2022); Manakul et al. (2023, SelfCheckGPT)
- [x] FinanceBench — Zhang et al. (2024)
- [x] FinQA — Chen et al. (2021)
- [x] Kang et al. (2023) EDGAR-based hallucination benchmark

---

## Key Numbers

- [x] ECE = 0.115 for the credit-risk classifier example
- [x] 1,000 default predictions, 5 equal-width bins of width 0.2 (Example 13.1)
- [x] High-confidence bin (80–100%): stated confidence 0.88, actual accuracy 0.62
- [x] 34/500 transcripts with ≥3 matching 13-grams (contamination audit)
- [x] Accuracy drop 62% → 54% after anonymisation (8 pp from entity memorisation)
- [x] 51–65% directional accuracy range across LLM stock-prediction studies
- [x] 51–54% residual accuracy after controlling for four artefacts
- [x] IR > 0.5 = strong skill; IR > 1.0 = exceptional skill
- [x] US large-cap half-spreads 1–3 bps; market impact 5–20 bps
- [x] Daily news-rebalancing costs 10–50 bps/day
- [x] Hard temporal cutoff safety margin: ≥3 months past model knowledge cutoff
- [x] M = 10 bins standard for reliability diagrams

---

## Figures

- [x] fig_reliability.png — embedded in lesson deck (appendix slide "Reliability diagram for the credit example") and in practical deck (case study goal slide)

---

## Omissions

All items below were present in the original deck. The overhaul added:

- [x] fig_reliability.png embedded with proper `<figure class="deckfig">` markup in both decks
- [x] "MBA" badge removed from both decks; replaced with "Summer school · math one click away" badge

## Corrections (2026-06-28)

- Fixed citation conflation on the "References by theme" appendix slide: the entry
  `Niculescu-Mizil & Caruana (2005, Platt/isotonic)` was incorrect. Replaced with three
  correctly-attributed entries: Niculescu-Mizil & Caruana (2005, adaptive binning);
  Platt (1999, Platt scaling); Zadrozny & Elkan (2002, isotonic).
- Added brief mentions to make previously-falsely-checked items genuinely covered:
  - Tetlock (2007) and Bollen et al. (2011) — added to §3 "What the data actually shows" slide.
  - Harvey (2016) — added alongside Tetlock/Bollen on the same slide (alpha decay from factor crowding).
  - PEFT / LoRA cross-reference — added to the §4 walk-forward cost trade-off callout.
