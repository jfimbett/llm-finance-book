# Slide Coverage: 11-regtech-compliance-aml

Source: `book/chapters/11-regtech-compliance-aml/chapter.tex`
Decks: `course/slides-html/11-regtech-compliance-aml/index.html` (lesson) + `practical.html`

---

## Concept Checklist

### Sections / subsections

- [x] §1 The Regulatory Landscape for AI in Finance
- [x] §1.1 EU AI Act — risk classification for financial AI systems (Reg. EU 2024/1689)
- [x] §1.2 MiFID II, Basel III, and model risk management (SR 11-7)
- [x] §1.3 GDPR and data privacy constraints on LLM use
- [x] §2 Anti-Money Laundering with LLMs
- [x] §2.1 The false-positive crisis in keyword-based AML screening
- [x] §2.2 Agentic LLM systems for adverse media screening
- [x] §2.3 RAG-based adverse media pipelines: architecture and design
- [x] §2.4 Adverse Media Index: quantitative risk scoring from text
- [x] §3 KYC and Sanctions Screening
- [x] §3.1 Entity resolution and name disambiguation
- [x] §3.2 Politically exposed persons (PEP) screening
- [x] §3.3 Beneficial ownership extraction from filings
- [x] §4 Regulatory Reporting Automation
- [x] §4.1 XBRL tagging and automated filing
- [x] §4.2 Suspicious activity report (SAR) drafting
- [x] §4.3 Stress test narrative automation
- [x] §5 Governance and Audit Trails
- [x] §5.1 Explainability requirements for compliance decisions
- [x] §5.2 Human-in-the-loop workflow design
- [x] §5.3 Model risk management for LLM-based compliance systems
- [x] Summary (five key takeaways)

### Named methods / models / results

- [x] EU AI Act risk tiers: unacceptable / high-risk / limited / minimal
- [x] High-risk AI: seven mandatory requirements (Annex III)
- [x] Provider vs. deployer distinction (EU AI Act)
- [x] MiFID II: kill switches, pre/post-trade limits, annual self-assessment
- [x] Basel III IRB: supervisory validation, back-testing, stress testing
- [x] SR 11-7 "model" definition (quantitative method…)
- [x] SR 11-7 three pillars: development, validation, governance
- [x] FSB (2024) challenges for existing MRM frameworks
- [x] GDPR Art. 5 — data minimisation (tension with RAG chunks)
- [x] GDPR Art. 9 — special category data (ethnicity, politics, convictions)
- [x] GDPR Art. 9(2)(g) — substantial public interest as legal basis for AML processing
- [x] GDPR Art. 17 — right to erasure (embedding deletion; fine-tuned weight problem)
- [x] GDPR Art. 22 — automated individual decision-making; human review right
- [x] GDPR Art. 22 example: A. Petrov, score 0.87, auto-declined
- [x] False positive rate (FPR) and precision (PPV) — formal definitions
- [x] AML keyword/fuzzy matching: Jaro-Winkler, Soundex, Metaphone
- [x] Agentic adverse media screening: 5-step workflow
- [x] Carlos Fernandez-Gutierrez screening example
- [x] RAG pipeline: 5 components — ingestion, vector store, retriever, reader/ranker, output formatter
- [x] Ingestion: 200–400 token chunks with overlap
- [x] Hybrid retrieval: dense embeddings + BM25 sparse
- [x] Reciprocal Rank Fusion (RRF) formula, κ = 60
- [x] Cross-encoder reranking (vs. bi-encoder retrieval)
- [x] Grammar-constrained decoding — structured JSON output (Willard & Louf, 2023)
- [x] Ngam (2026) Perceive–Reason–Act agentic AML loop
- [x] fig_rrf.png embedded on RRF slide (lesson deck) and RRF recap slide (practical deck)
- [x] Adverse Media Index (AMI) formula
- [x] AMI components: relevance r_i, credibility c_i, recency t_i, offence indicators e_i, severity weights w, baseline α
- [x] Temporal decay: t_i = exp(-λ(T−T_i)), e.g. λ = 0.01/day
- [x] Entity resolution as pair classification
- [x] Two-stage entity resolution: ANN blocking + cross-encoder scoring
- [x] Transliteration variance (Gaddafi / Qaddafi example)
- [x] Name-context resolution (Carlos Salinas example)
- [x] PEP: enhanced due diligence (EDD), FATF requirement
- [x] PEP family members and close associates (FaMCAs)
- [x] PEP relation extraction for self-updating registry
- [x] Beneficial ownership: UBO definition, shell/trust/nominee typologies
- [x] Beneficial ownership extraction → directed ownership graph
- [x] FATF Recommendation 24
- [x] Corporate Transparency Act (2021)
- [x] Meridian Capital Holdings → Apex Global → Sunridge BVI beneficial ownership chain
- [x] XBRL tagging: retrieval + LLM verification formula (λ interpolation)
- [x] US GAAP taxonomy: 20,000+ elements; flat classification fails (label sparsity)
- [x] SEC XBRL requirement (2009); EU ESEF/iXBRL
- [x] SAR: format, recipients (FinCEN / NCA / TRACFIN)
- [x] SAR risk: factual error misleads law enforcement
- [x] Ioannides et al. (2023) Gracenote.ai — GPT-4 compliance tool
- [x] Stress test narrative: RAG-grounded + chain-of-thought fact-check pass
- [x] Template-constrained generation + post-generation numerical verification
- [x] Explainability: retrieval transparency (top-3 passages + relevance scores)
- [x] Explainability: chain-of-thought rationale (Wei et al., 2022)
- [x] Explainability: post-hoc attribution — SHAP (Lundberg & Lee, 2017)
- [x] Attention weights: rough guide only, not standalone explanations (Clark et al., 2019)
- [x] HITL: automation bias (Batarseh et al., 2021)
- [x] HITL: 4 design dimensions (task decomp, uncertainty, override+feedback, queue ordering)
- [x] SR 11-7 extended for LLMs: development documentation, independent validation, governance
- [x] Validation: benchmark, adversarial, calibration, bias auditing, robustness

### Key numbers

- [x] FATF: 2–5% of global GDP laundered (~&#36;800 bn–&#36;2 tn annually)
- [x] AML FPR: 95%–99% (fewer than 1 in 20 flagged alerts is genuine)
- [x] Chunk size: 200–400 tokens with overlap
- [x] RRF κ = 60 (smoothing constant)
- [x] Temporal decay λ = 0.01/day (example value)
- [x] Real-time onboarding pipeline: < 30 seconds
- [x] US GAAP taxonomy: 20,000+ elements
- [x] SEC XBRL since 2009
- [x] SAR: skilled analyst spends 2–4 hours per complex SAR
- [x] Monitoring: weekly on 200 senior-reviewed labelled cases
- [x] Precision alert threshold: < 60%
- [x] Recall alert threshold: < 95%
- [x] Root-cause review triggered within 5 business days
- [x] Data retention: 7 years in tamper-evident log

### Citations (Author, year) from chapter.tex

- [x] EU AI Act — Reg. (EU) 2024/1689
- [x] Andhov & Amparo (2024) — legal analysis of EU AI Act for fintech
- [x] Passador (2024) — EU AI Act obligations for banking (ECB supervisory role)
- [x] FSB (2024) — AI in financial services stability report
- [x] SR 11-7 — Fed/OCC model risk management guidance (2011)
- [x] FATF (2021) — AML/CFT guidance
- [x] FinCEN (2020) — AML guidance; criticism of excessive low-quality SARs
- [x] Shirvanporzour (2025) — ML/DL/NLP for AML detection and compliance automation
- [x] Ngam (2026) — Perceive–Reason–Act agentic AML feature extraction
- [x] Lewis et al. (2020) — RAG original paper
- [x] Cormack et al. (2009) — reciprocal rank fusion
- [x] Reimers & Gurevych (2019) — cross-encoders / sentence encoders
- [x] Willard & Louf (2023) — grammar-constrained decoding
- [x] Gao et al. (2024) — RAG survey (hybrid retrieval, reranking)
- [x] ViracachaP (2024) — AI in RegTech (GDPR, AML, tax compliance efficiency)
- [x] Anand (2025) — AI-powered RegTech NLP for BSA/Dodd-Frank/SOX compliance
- [x] Ioannides et al. (2023) — Gracenote.ai GPT-4 governance/compliance tool
- [x] SEC (2009) — XBRL reporting requirement
- [x] Wei et al. (2022) — chain-of-thought prompting
- [x] Lundberg & Lee (2017) — SHAP
- [x] Clark et al. (2019) — attention weights not reliable standalone explanations
- [x] Batarseh et al. (2021) — automation bias survey
- [x] Lin et al. (2025) — RiskTagger crypto AML annotation agent
- [x] Doshi-Velez & Kim (2017) — interpretability (further reading)
- [x] Yao et al. (2022) — ReAct (cross-referenced via Lecture 4)

---

## Omissions

(No unchecked items remain — all omissions were addressed in P3/P4 edits.)
