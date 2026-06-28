# Slide Coverage — 06 Credit Risk

Source: `book/chapters/06-credit-risk/chapter.tex`

## Checklist

### Sections / Subsections
- [x] §1 Credit data: sources, privacy, regulatory constraints
- [x] §1.1 Credit bureau data and alternative data sources
- [x] §1.2 Regulatory constraints: GDPR, FCRA, ECOA
- [x] §1.3 Preprocessing: anonymisation, class imbalance, missing data
- [x] §2 Credit risk modelling with LLMs
- [x] §2.1 Credit risk arc: Z-score → Merton → Reduced-form → Gradient boosting → LLMs
- [x] §2.2 Fine-tuning for default prediction (task formulation, serialisation, LoRA)
- [x] §2.3 Structured generation and implied default probabilities
- [x] §2.4 Probability calibration: Platt scaling and isotonic regression
- [x] §3 Household decisions under uncertainty
- [x] §3.1 Bounded rationality and the household decision problem
- [x] §3.2 LLMs as decision-support agents
- [x] §3.3 Utility-theoretic framing and preference elicitation
- [x] §4 Persona agents and behavioural simulation
- [x] §4.1 Defining agent personas (D, S, Ψ, L)
- [x] §4.2 Multi-persona dialogue and population-level disagreement
- [x] §4.3 Applications: loan uptake, mortgage choice, retirement planning
- [x] §4.4 Calibrating simulated behaviour against survey data
- [x] §5 Evaluation and model risk management
- [x] §5.1 Credit-specific metrics: AUROC, KS statistic, Gini coefficient
- [x] §5.2 SR 11-7 model risk framework applied to LLM governance
- [x] §5.3 Disparate impact testing / four-fifths rule (DIR)
- [x] §5.4 Backtesting and through-the-cycle validation
- [x] §5.5 SHAP interpretability for credit decisions
- [x] §6 Deployment of a credit risk application
- [x] §6.1 System architecture (five subsystems)
- [x] §6.2 Inference API design and request/response format
- [x] §6.3 API-based vs self-hosted LLM serving
- [x] §6.4 Monitoring: PSI, embedding drift, alert tiers
- [x] §6.5 Human-in-the-loop review workflows (three tiers)
- [x] §6.6 Regulatory documentation: MDR, MVR, GDPR Art. 22
- [x] §6.7 Model inventory and change triggers

### Named Methods / Models / Results
- [x] FICO score (1989, Fair Isaac Corporation)
- [x] VantageScore (2006, joint venture of three bureaus)
- [x] Altman Z-score (altman1968financial, 66 manufacturing firms)
- [x] Merton (1974) structural model — equity as call option on firm assets
- [x] Reduced-form / intensity-based models (duffie2003credit)
- [x] Gradient boosting (XGBoost, LightGBM)
- [x] FinBERT (yang2020finbert) and BloombergGPT (wu2023bloomberggpt)
- [x] Sequence classification (BERT encoder + CLS head)
- [x] Causal LM with label generation (few-shot)
- [x] LoRA — Low-Rank Adaptation
- [x] Constrained decoding via context-free grammars (willard2023efficient / outlines library)
- [x] Verbatim probability extraction (label token logits)
- [x] Platt scaling (platt1999probabilistic)
- [x] Isotonic regression (zadrozny2002transforming) + PAV algorithm O(n)
- [x] Simon (1955) bounded rationality / satisficing
- [x] Kahneman (2011) System 1 / System 2 dual-process cognition
- [x] CRRA utility — constant relative risk aversion
- [x] Argyle et al. (2023) silicon sampling
- [x] Lusardi and Mitchell (2011) 3-question financial literacy battery
- [x] Multi-persona dialogue (simulated conversation between persona instances)
- [x] Population stability index (PSI)
- [x] Maximum mean discrepancy (MMD) for embedding drift
- [x] SHAP / Shapley value (lundberg2017unified)
- [x] Disparate impact ratio (DIR) / four-fifths rule
- [x] SR 11-7 (sr117, Fed/OCC 2011)
- [x] Basel II/III Pillar 1 through-the-cycle (TTC) PD
- [x] Vintage analysis (backtesting framework)
- [x] SMOTE (Synthetic Minority Over-sampling Technique)
- [x] MCAR / MAR / MNAR missingness mechanisms
- [x] Sweeney (2002) re-identification — 87% uniquely identifiable
- [x] CFPB Special Purpose Credit Programmes (SPCP)
- [x] ECB Household Finance and Consumption Survey (ecb2020hfcs)
- [x] US Survey of Consumer Finances (SCF)
- [x] Cumulative Accuracy Profile (CAP) curve

### Key Numbers
- [x] 200–230 million US adults with credit bureau files
- [x] FICO range: 300–850
- [x] FICO weights: payment history 35%, amounts owed 30%, length 15%, new credit 10%, mix 10%
- [x] Sweeney (2002): 87% of US population uniquely identifiable from ZIP + DOB + sex
- [x] Default rates: 1–10% over a 12-month horizon
- [x] Z-score dataset: 66 manufacturing firms
- [x] Z-score cutoffs: Z < 1.81 distressed; Z > 2.99 healthy
- [x] LoRA: r = 8, d = 768 → ~48× fewer trainable parameters
- [x] Mortgage shopping (CFPB 2018): 1/3 borrowers did not shop; avg. ~$300/year more in interest
- [x] Maria persona: 28yo, $2,400/month, $800 savings, bureau score 584
- [x] Thomas persona: 52yo, €48,000 salary, €120,000 savings, γ ≈ 2
- [x] AUROC: good > 0.70, excellent > 0.80
- [x] KS: good > 0.40, excellent > 0.60
- [x] Gini (retail): typical range 0.40–0.70
- [x] DIR four-fifths rule: DIR < 0.80 = presumptive adverse impact
- [x] PSI thresholds: < 0.1 stable; 0.1–0.25 investigate; > 0.25 model review
- [x] TTC calibration dataset: ≥ 7–10 years (one full credit cycle)
- [x] Validated simulation standard: 60–70% of observed cross-sectional variation
- [x] Constrained decoding worked example: digit logits → implied PD 0.23

### Citations
- [x] (cfpb2013ecoa) — thin-file consumers, 45 M+ US adults
- [x] (campbell2006household) — household decisions, alternative data, retirement defaults
- [x] (altman1968financial) — Z-score
- [x] (merton1974pricing) — structural model
- [x] (duffie2003credit) — reduced-form / intensity models
- [x] (yang2020finbert) — FinBERT
- [x] (wu2023bloomberggpt) — BloombergGPT
- [x] (willard2023efficient) — outlines constrained decoding
- [x] (platt1999probabilistic) — Platt scaling
- [x] (zadrozny2002transforming) — isotonic regression
- [x] (simon1955behavioral) — bounded rationality
- [x] (kahneman2011thinking) — dual-process cognition
- [x] (argyle2023out) — silicon sampling
- [x] Lusardi and Mitchell (2011) — financial literacy battery
- [x] (ecb2020hfcs) — ECB HFCS survey
- [x] (sr117) — SR 11-7
- [x] (lundberg2017unified) — SHAP
- [x] Sweeney (2002) — re-identification

## Omissions

All items above are now covered in the lesson deck (index.html) or appendix. No unchecked omissions remain.
