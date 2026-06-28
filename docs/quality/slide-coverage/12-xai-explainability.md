# Slide Coverage — 12-xai-explainability

Source: `book/chapters/12-xai-explainability/chapter.tex`
Decks: `course/slides-html/12-xai-explainability/index.html` (lesson) + `practical.html`

---

## Checklist

### Sections / Subsections

- [x] Why Explainability Matters in Regulated Finance
- [x] Legal Requirements: EU AI Act, SR 11-7, ECOA (GDPR Art. 22, FCRA)
- [x] Stakeholder Expectations: Clients, Regulators, Auditors
- [x] The Black-Box Problem for LLMs (Rudin 2019 rejoinder)
- [x] Classical XAI Methods Applied to LLMs
- [x] SHAP Values: From Tree Models to Language Models
- [x] LIME for Local, Model-Agnostic Explanations
- [x] Attention Visualization: Promise and Limitations
- [x] LLM-Native Explainability Mechanisms
- [x] Chain-of-Thought Reasoning as an Explanation Trace
- [x] Counterfactual Explanations: What Would Change the Decision?
- [x] Natural Language Justifications for Automated Decisions
- [x] Case Studies in Financial Explainability
- [x] Credit Scoring: Explaining Rejection to Applicants (hybrid pipeline)
- [x] Loan Denial Letters Compliant with ECOA/FCRA
- [x] Investment Recommendation Disclosures under MiFID II
- [x] Evaluating the Quality of Explanations
- [x] Faithfulness: sufficiency + comprehensiveness
- [x] Completeness and Plausibility Metrics
- [x] Human-Subject Studies with Financial Domain Experts
- [x] Summary / Further Reading

### Named Methods / Results / Models

- [x] Shapley value (cooperative game theory, Shapley 1953)
- [x] SHAP — Lundberg & Lee (2017) unified additive attribution
- [x] KernelSHAP (sampling approximation for neural nets / LLMs)
- [x] TreeSHAP — Lundberg et al. (2020), exact polynomial-time for trees
- [x] LIME — Ribeiro et al. (2016), local surrogate
- [x] Attention weights / attention visualization
- [x] Integrated Gradients — Sundararajan et al. (2017)
- [x] Chain-of-thought prompting — Wei et al. (2022)
- [x] Self-consistency — Wang et al. (2022)
- [x] Counterfactual explanations — Wachter et al. (2017)
- [x] Mechanistic interpretability — TatsatShater (2025)
- [x] Faithfulness vs. plausibility distinction — Jacovi & Goldberg (2020)
- [x] Explanation trace (definition)
- [x] Counterfactual explanation (optimisation definition)
- [x] Sufficiency metric (Eq.)
- [x] Comprehensiveness metric (Eq.)
- [x] SHAP Efficiency / Symmetry / Dummy axioms

### Key Numbers

- [x] P(creditworthy) = 0.14, baseline 0.50 (BERT example)
- [x] KernelSHAP 500 samples (BERT fine-tune)
- [x] SHAP values: "struggled" −0.089, "declining" −0.073, "down 30%" −0.061, "competitive" −0.047, "restaurant" −0.038, "pandemic" −0.029, "operates" +0.012
- [x] Prediction gap 0.50 − 0.14 = 0.36
- [x] Hybrid pipeline: 42 structured vars, KernelSHAP 1,000 samples (DistilBERT)
- [x] DTI 54 % vs 45 % threshold; revenue −28 % YoY; cash reserve 0.8 months (threshold 3)
- [x] SHAP values in pipeline: −0.18, −0.12, −0.09, −0.07, −0.05
- [x] MiFID II: n = 12,000 clients; 2 % quarterly human sample; ~0.3 % revision rate
- [x] Reg. B: 30-day adverse-action notice; 4–5 principal reasons

### Citations (Author, year)

- [x] Miller (2019) — explanation defined
- [x] SR 11-7 — model risk management (Fed)
- [x] Arrieta et al. (2020) — full XAI taxonomy
- [x] Rane, Choudhary & Rane (2023) — XAI in financial domain survey
- [x] EU AI Act (2024) — Annex III high-risk classification
- [x] CFPB / Reg. B (2013) — ECOA adverse-action requirements
- [x] Doshi-Velez & Kim (2017) — rigorous evaluation framework
- [x] Shapley (1953) — axiomatic uniqueness
- [x] Lundberg & Lee (2017) — SHAP
- [x] Lundberg et al. (2020) — TreeSHAP
- [x] Ribeiro et al. (2016) — LIME
- [x] Vaswani et al. (2017) — attention mechanism
- [x] Clark et al. (2019) — BERT attention heads and syntactic relations
- [x] Jain & Wallace (2019) — attention not a unique explanation
- [x] Wiegreffe & Pinter (2019) — attention as diagnostic
- [x] Jacovi & Goldberg (2020) — faithfulness / plausibility distinction
- [x] Sundararajan et al. (2017) — Integrated Gradients
- [x] Wei et al. (2022) — chain-of-thought
- [x] Wang et al. (2022) — self-consistency
- [x] Wachter et al. (2017) — counterfactual explanations
- [x] Mehrabi et al. (2021) — fairness auditing separate from attribution
- [x] Tatsat & Shater (2025) — mechanistic interpretability for financial LLMs
- [x] Cetintav et al. (2024) — GPT-4o translating SHAP outputs to natural language
- [x] Schmitt (2024) — AutoML + SHAP complementarity in credit scoring
- [x] Desai (2024) — Shapley + information-theoretic framework for regulatory audit
- [x] Lakarasu (2024) — XAI-prompted compliance platform, EU AI Act Art. 13
- [x] ESMA / MiFID II suitability guidelines (2018)
- [x] CFA Institute (2025) — industry XAI survey, investment management
- [x] Nauta et al. (2023) — anecdotal evaluation paradigms
- [x] Mohsin & Nasim (2025) — bibliometric review of XAI in finance

---

## Omissions

All checklist items are now covered in the updated decks. No unchecked items remain.
