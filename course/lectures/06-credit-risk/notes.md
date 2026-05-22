# Lecture 6: LLMs for Credit Risk Analysis

## Learning Objectives

By the end of this lecture, students should be able to:

1. Identify the main sources of credit data (bureau, alternative) and explain the regulatory constraints of FCRA, ECOA, and GDPR Article 22 that govern model design.
2. Apply standard preprocessing pipelines for credit data: anonymisation, class-imbalance correction, and missing-data handling.
3. Formulate default prediction as a language modelling task and fine-tune a BERT-family model using LoRA.
4. Extract implied default probabilities from a language model using constrained decoding and calibrate them with Platt scaling and isotonic regression.
5. Model household financial decisions under bounded rationality and use LLMs as decision-support agents grounded in utility theory.
6. Design persona agents that simulate heterogeneous household financial behaviour and calibrate their outputs against survey data.
7. Evaluate a credit model with AUROC, KS statistic, and Gini coefficient within the SR 11-7 governance framework.
8. Apply SHAP-based interpretability to an LLM credit decision system and produce GDPR-compliant adverse action notices.

---

## 1. Credit Data: Sources, Privacy, and Regulatory Constraints

### Motivation

In 2019 a viral tweet ignited a Congressional investigation. The subject was not a data breach or a rogue trading algorithm — it was a credit card credit limit. David Heinemeier Hansson, creator of Ruby on Rails, reported that his Apple Card credit limit was twenty times lower than his wife's, despite filing joint tax returns and sharing assets. Within days Senator Elizabeth Warren had written to Goldman Sachs, and the New York Department of Financial Services had opened a formal investigation.

The episode crystallised something practitioners had long known: automated credit decisions, even those built on carefully anonymised financial data, can embed and amplify discrimination in ways invisible to both lender and borrower. Credit data is simultaneously the richest behavioural dataset available to financial institutions and one of the most legally regulated.

### Credit Bureau Data

The three major US credit bureaus — Equifax, Experian, and TransUnion — each maintain files on roughly 220 million adults. A standard credit file contains identification data, account data (24–84 months of payment history per account), inquiry data, public records (bankruptcies), and collection accounts.

From this raw file, bureaus compute **credit scores**: the FICO score (introduced 1989) and the VantageScore (introduced 2006) both range from 300 to 850. FICO's publicly disclosed factor weights: payment history 35%, amounts owed 30%, length of credit history 15%, new credit 10%, credit mix 10%.

Bureau data is highly predictive of near-term default but has one critical limitation: it is circular — it records credit behaviour, so it is uninformative for the ~45 million US adults with thin or no credit files, a group disproportionately composed of recent immigrants, young adults, and lower-income households.

### Alternative Data Sources

To extend credit to thin-file consumers, lenders have increasingly incorporated alternative data:

- **Bank transaction data**: inflows, outflows, income volatility, and recurring expense patterns. Rich in signal but legally complex under the Electronic Fund Transfer Act and Dodd-Frank Section 1033.
- **Rent and utility payment data**: highly predictive because rent is often the largest recurring obligation, yet historically invisible to credit models.
- **Mobile and telecom payment data**: widely used in emerging-market credit scoring where bureau coverage is low.
- **Unstructured text**: application free-text fields, loan purpose statements, lender notes. LLMs are particularly relevant here — "the loan is for my daughter's medical emergency" carries a qualitatively different risk profile from "consolidating payday loans."

### Regulatory Constraints: FCRA, ECOA, and GDPR

**Fair Credit Reporting Act (FCRA)**: When a creditor takes an adverse action (denying credit or offering less favourable terms) based wholly or partly on a consumer reporting agency's information, it must provide a written adverse action notice with the specific reasons. This is the origin of the **reason code** system — every credit model deployed in the US must produce a short list of factors that drove an adverse decision. A transformer producing a single scalar from a high-dimensional embedding is not inherently reason-code compatible; post-hoc attribution methods (SHAP, Section 5) or architectural choices are required.

**Equal Credit Opportunity Act (ECOA) / Regulation B**: Prohibits discrimination on the basis of race, colour, religion, national origin, sex, marital status, age, and receipt of public assistance — not only intentional discrimination (disparate treatment) but also facially neutral practices producing discriminatory effects (disparate impact) unless justified by business necessity.

**GDPR Article 22**: In the EU, individuals have the right not to be subject to a decision based solely on automated processing that produces legal or similarly significant effects. Credit denials fall squarely within this definition. Even when permitted, the data subject retains the right to obtain human review, express their point of view, and contest the decision — the legal foundation for human-in-the-loop review workflows (Section 6).

### Preprocessing

**Anonymisation**: Direct identifiers (name, SSN, account number) must be removed or hashed. Beyond direct identifiers, credit data contains quasi-identifiers — combinations that uniquely identify individuals. Sweeney (2002) showed that 87% of the US population can be uniquely identified by ZIP code, date of birth, and sex alone. Standard techniques: tokenisation, generalisation (age → age bracket), suppression, and differential privacy (adding calibrated noise to training gradients).

**Class Imbalance**: Default rates lie in the range 1–10% over a 12-month horizon. A dataset with a 3% default rate contains 970,000 negatives and 30,000 positives; a model predicting "non-default" for all achieves 97% accuracy while providing zero discrimination. Standard approaches: oversampling (SMOTE), undersampling, cost-sensitive learning via loss weights, and threshold calibration. For LLM fine-tuning, cost-sensitive loss weighting is most practically tractable.

The balanced class weight for the positive class is:
$$w_+ = \frac{n}{2 n_+}$$
where $n_+$ is the number of default observations and $n$ the total. Using $w_+$ and $w_-$ in binary cross-entropy gives each class equal aggregate influence on the gradient.

**Missing Data**: Three missingness mechanisms must be distinguished. MCAR (missing completely at random): probability of missingness is independent of all data — mean imputation is unbiased. MAR (missing at random): missingness depends on observed data but not on the missing value itself — multiple imputation is consistent. MNAR (missing not at random): missingness depends on the unobserved value (e.g., a borrower omits income because it is very low) — standard methods are biased; sensitivity analysis is required.

For LLM-based models, a common approach is to serialise the feature vector as natural language, explicitly encoding missingness: `"[INCOME: MISSING] [EMPLOYMENT: SELF-EMPLOYED] [BUREAU_SCORE: 687]"`, allowing the model to learn the informational content of the missingness indicator from context.

---

## 2. Credit Risk Modelling with LLMs

### The Credit Risk Arc

The history of credit scoring is a succession of modelling paradigms.

**Altman Z-Score (1968)**: A linear discriminant function of five financial ratios:
$$Z = 1.2 X_1 + 1.4 X_2 + 3.3 X_3 + 0.6 X_4 + 1.0 X_5$$
where $X_1$ = working capital/total assets, $X_2$ = retained earnings/total assets, $X_3$ = EBIT/total assets, $X_4$ = market equity/book debt, $X_5$ = sales/total assets. Firms with $Z < 1.81$ are classified as distressed, $Z > 2.99$ as healthy. The model was estimated on sixty-six manufacturing firms and remains a benchmark today.

**Merton (1974)**: Equity as a European call option on the firm's assets. Default occurs if $V_T < D$. The risk-neutral default probability:
$$\text{PD}^{\text{Merton}} = \Phi(-d_2)$$
where $d_2 = d_1 - \sigma_V\sqrt{T-t}$ and $d_1 = [\ln(V_t/D) + (r + \frac{1}{2}\sigma_V^2)(T-t)] / (\sigma_V\sqrt{T-t})$. The model requires estimates of the unobserved asset value and volatility.

**Reduced-Form Models**: Model the default time $\tau$ as the first jump of an inhomogeneous Poisson process with stochastic intensity $\lambda_t$. The survival probability:
$$S(t,T) = \mathbb{E}\!\left[\exp\!\left(-\int_t^T \lambda_s \, ds\right) \bigg| \mathcal{F}_t\right]$$
These models fit observed credit spread term structures more tractably than structural models.

**Machine Learning (2015–2022)**: Gradient-boosted decision trees (XGBoost, LightGBM) became dominant for retail credit scoring. Advantages: native handling of missing values, capture of non-linear interactions, robustness to outliers. Primary limitation: operate exclusively on tabular features.

**Language Models for Credit**: LLMs add value in at least three scenarios: (1) text-native features (loan purpose statements, credit officer notes), (2) thin-file borrowers where alternative text data resists tabularisation, and (3) reasoning about complex commercial credit terms (covenant structures, waterfall provisions).

### Fine-Tuning for Default Prediction

**Task Formulation**: Three natural approaches:
- *Sequence classification*: serialise the borrower profile as text; fine-tune a BERT-family encoder to predict a binary label. The pooled `[CLS]` representation passes through a linear head with sigmoid activation.
- *Causal language modelling with label generation*: prompt a decoder-only model with a structured borrower description; ask it to generate a classification token. Leverages in-context learning; scales to few-shot settings.
- *Regression on probability*: fine-tune to output a scalar probability directly.

For most regulatory environments, sequence classification or structured generation are preferred.

**Input Serialisation**: A borrower profile must be converted to text with a consistent template:

> "Applicant: Age 34. Employment: full-time, 6 years tenure. Annual income: $58,000. Loan purpose: debt consolidation. Requested amount: $12,000. Bureau score: 672. Delinquencies (past 24 months): 1. Assess default risk:"

Variation in field ordering or phrasing introduces spurious variance in model outputs. Templates must be identical across training and inference.

**Parameter-Efficient Fine-Tuning (LoRA)**: Fine-tuning a full LLM on credit data is expensive and risks overfitting on the small labelled datasets typical of individual lenders. Low-Rank Adaptation (LoRA) constrains the weight update $\Delta W$ to a low-rank factorisation:
$$\Delta W = BA, \quad B \in \mathbb{R}^{d \times r}, \; A \in \mathbb{R}^{r \times d}, \quad r \ll d$$
Only $A$ and $B$ are updated; the original weights $W_0$ are frozen. With $r=8$ and $d=768$, LoRA reduces trainable parameters by a factor of ~48 relative to full fine-tuning.

### Structured Generation and Implied Default Probabilities

A decoder-only language model assigns probabilities to sequences of tokens. When we prompt such a model with a borrower description and ask for a default probability, the model's output is a distribution over its vocabulary at each position — not a single scalar. **Constrained decoding** provides a principled extraction mechanism.

The `outlines` library (Willard et al., 2023) implements efficient constrained decoding by intersecting the language model's next-token distribution with a finite automaton derived from a formal grammar. For credit scoring, we define the grammar to constrain the model to produce a JSON object with a single key `"pd"` mapped to a float in $[0, 1]$.

At each decoding step, only tokens that are valid continuations under the grammar receive non-zero probability:
$$P_{\text{constrained}}(x_{t+1} = v \mid x_{1:t}) = \frac{\exp(\ell_v) \cdot \mathbf{1}[v \in \mathcal{V}_{\text{valid}}(x_{1:t})]}{\sum_{u \in \mathcal{V}_{\text{valid}}(x_{1:t})} \exp(\ell_u)}$$

The model generates the JSON prefix `{"pd": ` and then generates the decimal representation of the probability digit by digit. The implied probability $\hat{p}$ is the floating-point number produced by this constrained generation process.

**Key insight**: $\hat{p}$ is not the model's *confidence* about a binary label — it is the specific floating-point number the model was guided to express. It reflects the model's internal representation of risk but is not guaranteed to be calibrated against the empirical default rate.

### Probability Calibration

A model is **well-calibrated** if, among all applications scored with predicted probability $\hat{p}$, the fraction that actually default is approximately $\hat{p}$:
$$\mathbb{E}[Y \mid \hat{P} = p] = p \quad \text{for all } p \in [0, 1]$$

Calibration is assessed via reliability diagrams: the unit interval is divided into $B$ bins; within each bin, the mean predicted probability is plotted against the observed default rate. A perfectly calibrated model produces points on the 45-degree diagonal.

**Platt Scaling**: Fit a logistic regression on the model's raw outputs on a held-out calibration set:
$$\hat{p}_{\text{Platt}}(x) = \sigma(a \cdot f(x) + b)$$
Parameters $a$ and $b$ absorb systematic over- or under-confidence. When $a < 1$ the model is overconfident; when $a > 1$ it is underconfident.

**Isotonic Regression**: A non-parametric calibration method that finds a non-decreasing step function minimising:
$$\hat{q} = \underset{q \in \mathbb{R}^n,\; q_1 \leq q_2 \leq \cdots \leq q_n}{\arg\min} \sum_{i=1}^{n} (q_i - y_i)^2$$

Solved by the pool adjacent violators (PAV) algorithm in $O(n)$ time. More flexible than Platt scaling but requires more calibration data.

*Choosing between them*: Platt scaling is preferred when the calibration set is small (hundreds of observations) or when the score is approximately log-odds-linear. Isotonic regression is preferred when sufficient calibration data is available (thousands of observations).

---

## 3. Household Decisions Under Uncertainty

### Bounded Rationality

In 2018, the CFPB published a study documenting that roughly one-third of US mortgage borrowers did not shop for their mortgage before accepting the first offer they received. The expected benefit of comparison shopping is substantial; the information is publicly available; yet many households do not shop. The explanation lies in Herbert Simon's **bounded rationality**: households satisfice rather than optimise, relying on heuristics, social norms, and trusted intermediaries.

Four sources of departure from the neoclassical benchmark:
1. *Computational complexity*: The full household optimisation is a high-dimensional stochastic control problem.
2. *Information asymmetry*: Credit terms, tax implications, and insurance structures involve specialised knowledge that most households lack.
3. *Dual-process cognition*: High-stakes financial decisions are often made in "System 1" mode — fast, affective, heuristic-driven.
4. *Preference inconsistency*: Hyperbolic discounting, loss aversion, and framing effects cause choices inconsistent with stated long-run preferences.

An agent exhibits **bounded rationality** if: (i) it has a finite cognitive capacity and cannot consider all alternatives simultaneously; (ii) it uses heuristic search procedures that terminate before exhausting the solution space; (iii) it accepts a solution meeting a satisficing threshold $\alpha$, which may itself depend on recent experience.

### LLMs as Decision-Support Agents

The decision-support role of an LLM is to extend the effective cognitive frontier of the household without replacing household judgment. This requires three functions:
1. **Information extraction**: parsing complex financial documents (mortgage term sheets, insurance policy exclusions) into structured, comparable summaries.
2. **Consequence tracing**: computing multi-period financial implications of a specific choice given the household's stated circumstances.
3. **Trade-off articulation**: presenting options in a format that makes relevant trade-offs legible without nudging toward a particular choice.

The third function requires particular care. A decision-support agent that consistently recommends the financially optimal choice in neoclassical terms may systematically undermine household autonomy, particularly when stated and revealed preferences diverge.

A practical architecture consists of: a *document ingestion layer* (RAG pipeline parsing term sheets), a *household profile module* (income, assets, liabilities, risk preferences), a *consequence engine* (computing expected outcomes across scenarios), and a *dialogue manager* (presenting trade-offs conversationally).

### Utility-Theoretic Framing

Expected utility theory provides the normative benchmark. A household with wealth $W_0$ choosing among $K$ alternatives selects:
$$a^* = \underset{k \in \{1, \ldots, K\}}{\arg\max} \; \mathbb{E}[U(W_0 + \Delta W_k)]$$

For constant relative risk aversion (CRRA) utility:
$$U(W) = \frac{W^{1-\gamma}}{1-\gamma}, \quad \gamma > 0$$

The parameter $\gamma$ is the risk aversion coefficient: $\gamma = 1$ corresponds to log utility, $\gamma = 2$ to moderate risk aversion, $\gamma > 5$ to high risk aversion.

LLMs contribute by eliciting utility parameters from natural language conversations: present binary lottery choices calibrated to identify indifference points, extract the stated indifference points, then fit a CRRA utility function by minimising the squared deviations between the stated indifference outcomes and the utility-implied equivalents. The quality of elicitation depends critically on the LLM's ability to conduct a coherent multi-turn dialogue without anchoring the household's responses.

---

## 4. Persona Agents and Behavioural Simulation

### Defining Personas

Argyle et al. (2023) showed that a large language model conditioned on a detailed demographic backstory reproduces the survey response distributions of the corresponding demographic group with striking fidelity — "silicon sampling." This is not a claim that LLMs have genuine preferences; it is an empirical observation that LLMs encode distributional information about how different types of people tend to reason.

A **persona specification** is a tuple $\Pi = (D, S, \Psi, L)$:
- $D$: demographic attributes (age, sex, household composition, geographic region, education level)
- $S$: socioeconomic attributes (employment type, income, wealth, housing tenure, existing debt)
- $\Psi$: psychological attributes (risk aversion $\gamma$, time preference $\delta$, financial anxiety)
- $L$: financial literacy level, operationalised via Lusardi and Mitchell's (2011) three-question battery

A complete specification yields a system prompt of ~200–400 words covering background, financial goals, knowledge limitations, and behavioural tendencies.

**Contrasting personas — Maria and Thomas**: Maria is 28 years old, works as a rideshare driver, earns $2,400/month with high variability, has $800 in savings, bureau score 584, no post-secondary education, and is highly averse to losing her apartment. Thomas is 52, a French secondary school teacher earning €48,000, married with €120,000 in savings, understands compounding and diversification, and has financial literacy score 3/3.

When both are presented with a loan choice between a 12% fixed-rate and an 8% variable-rate option (capped at 18%): Maria anchors on worst-case payment and chooses the fixed rate for security. Thomas frames it as a break-even problem, quantifies his capacity to absorb rate increases, and chooses the variable rate — setting aside the savings difference as a buffer. Both responses are coherent and defensible given the persona. Neither is "wrong."

### Multi-Persona Simulation

Running an ensemble of $N$ personas produces a distribution over decisions that approximates the population-level response:
$$\hat{P}(d = k) = \frac{1}{N} \sum_{i=1}^{N} \mathbf{1}[d_i = k]$$

Population-level disagreement is informative: it identifies which subgroups are sensitive to which product features, enabling targeted product design.

**Multi-persona dialogue** places multiple personas in a simulated conversation (e.g., a financial adviser and a client) and observes how the dialogue evolves. Useful for identifying persuasion gaps, stress-testing disclosure language, and training human advisers.

**Applications**: loan uptake modelling (estimate take-up rates and APR elasticity before live A/B tests), mortgage choice simulation (evaluate product suitability for different borrower profiles), and retirement planning (assess how different households respond to default enrolment and auto-escalation schemes).

### Calibration Against Survey Data

For persona simulation to be scientifically credible it must be validated against observed data. The ECB Household Finance and Consumption Survey and the US Survey of Consumer Finances provide calibration targets.

Three steps: (1) **Population alignment** — calibrate persona sampling so the joint distribution of demographic attributes matches the target survey using post-stratification weights; (2) **Behavioural alignment** — compare the weighted decision distribution to the observed distribution using calibration loss $\mathcal{L}_{\text{cal}} = \sum_k (\hat{P}_{\text{sim}}(d=k) - \hat{P}_{\text{survey}}(d=k))^2$; (3) **Prompt refinement** — when calibration loss is high, refine the persona specification. Common causes of misalignment: prompts that are too generic, prompts that fail to instantiate the specific regulatory context, and prompts that elicit aspirational rather than realistic behaviour.

---

## 5. Evaluation and Model Risk Management

### Credit-Specific Metrics

**AUROC**: The Area Under the ROC Curve equals the probability that a randomly drawn defaulter receives a higher score than a randomly drawn non-defaulter:
$$\text{AUROC} = P(S_+ > S_-)$$

The ROC curve traces (FPR($t$), TPR($t$)) as the decision threshold $t$ varies from 1 to 0. A model with no discrimination produces a 45-degree diagonal; a perfect model reaches the upper-left corner.

**KS Statistic**: The maximum separation between the empirical CDFs of the defaulter score distribution and the non-defaulter score distribution:
$$\text{KS} = \sup_{s \in [0,1]} |F_+(s) - F_-(s)|$$

Computed by sorting all observations by score and reading off the maximum vertical distance between the two cumulative fractions. KS above 0.40 is conventionally considered good for retail credit; above 0.60 is excellent.

**Gini Coefficient**: Also called the accuracy ratio:
$$\text{Gini} = 2 \cdot \text{AUROC} - 1$$

This identity holds exactly (not as an approximation) — it follows from the relationship between the CAP curve and the ROC curve. For a random model, Gini = 0; for a perfect model, Gini = 1. Retail credit models typically achieve Gini of 0.40–0.70.

### SR 11-7 Model Risk Framework

SR 11-7 (2011) defines a model as "a quantitative method, system, or approach that applies statistical, economic, financial, or mathematical theories, techniques, and assumptions to process input data into quantitative estimates." An LLM-based credit scoring system is unambiguously a model under this definition.

SR 11-7 requires three pillars:

**Model Development and Implementation**: document the theory and evidence base; quality and extent of data; limitations and uncertainties. For LLMs, additionally document: pre-training data provenance, fine-tuning data quality and vintage, and emergent behaviour at inference.

**Model Validation**: independent validation by a party separate from the development team. For LLMs, validation must include: conceptual soundness review, outcome analysis (vs. logistic regression or gradient-boosting benchmarks), sensitivity analysis (response to word-order changes, synonym substitution, missing fields), disparate impact testing (adverse action rates by protected class after controlling for legitimate credit factors), and adversarial probing.

**Governance**: formal model risk management policy. For LLMs, additionally address: model versioning (base model updates may trigger revalidation), prompt governance (system prompt changes constitute a model change), and vendor risk (if the LLM is accessed via API, the institution bears model risk for a model it does not control).

### Backtesting and Through-the-Cycle Validation

Two types of temporal degradation: **concept drift** (the relationship between features and default changes as the economy evolves) and **population drift** (the distribution of applicant characteristics changes).

**Vintage analysis**: group loans by origination quarter; track cumulative default rates over time; compare AUROC/KS across vintages to assess stability.

**Through-the-cycle (TTC) vs. point-in-time (PIT)**: Basel III Pillar 1 requires TTC PD estimates reflecting long-run average default rates. LLMs trained on recent data tend to produce PIT estimates. Converting PIT to TTC requires Platt scaling calibrated on a dataset spanning at least one full credit cycle (7–10 years).

### SHAP Interpretability

SHAP (SHapley Additive exPlanations) provides attribution rooted in cooperative game theory. The SHAP value for feature $j$ in input $x$:
$$\phi_j(x) = \sum_{S \subseteq \mathcal{F} \setminus \{j\}} \frac{|S|! \, (|\mathcal{F}| - |S| - 1)!}{|\mathcal{F}|!} \left[ f(S \cup \{j\}) - f(S) \right]$$

SHAP values satisfy three axioms: **efficiency** ($\sum_j \phi_j = f(x) - \mathbb{E}[f(x)]$, so values sum to the deviation from baseline), **symmetry** (identical contributors receive equal values), and **dummy** (a non-contributing feature receives zero).

For an LLM credit model with serialised tabular inputs, SHAP is computed by treating each field as a "feature" and computing the expected output change when each field is masked with a baseline value. The SHAP waterfall then directly maps to FCRA adverse action reason codes: the top positive contributors become adverse action reasons; top negative contributors are the factors that partially offset risk. This correspondence allows a compliant adverse action notice to be generated automatically.

<!-- BOOK-ONLY: Full proof of the Gini = 2·AUROC - 1 identity via the CAP curve Lorenz integral is in the chapter; summarising the result is sufficient for the lecture. -->

---

## 6. Deployment of a Credit Risk Application

### System Architecture

A production credit risk application built on an LLM consists of five subsystems:

1. **Feature Store**: single source of truth for model inputs; records retrieval timestamps and source systems for each feature value, enabling point-in-time reconstruction of any historical decision.
2. **Inference API**: receives a structured JSON payload, assembles the serialised text input, calls the LLM inference engine, and returns a structured response including predicted PD, calibrated PD, reason codes (from SHAP), and a unique decision identifier. The API contract is versioned.
3. **LLM Inference Serving**: two patterns — API-based (lower infrastructure burden, vendor dependency) and self-hosted (full data and model control). For credit decisions, the regulatory preference is for self-hosted models because the institution bears full responsibility regardless of the provider's data handling.
4. **Decision Record Database**: every credit decision persisted in an immutable append-only database; records may be supplemented but not overwritten.
5. **Monitoring and Alerting**: see below.

### Monitoring and Drift Detection

**Data drift**: the Population Stability Index (PSI) compares the distribution of each input feature between training and current deployment:
$$\text{PSI} = \sum_{b=1}^{B} (p_b - q_b) \ln\!\left(\frac{p_b}{q_b}\right)$$

PSI < 0.1 indicates stable distribution; 0.1–0.25 indicates moderate shift requiring investigation; > 0.25 indicates significant shift requiring model review.

For LLM-based models consuming text, embedding drift metrics (maximum mean discrepancy, Fréchet distance) are more appropriate than PSI applied to raw features.

**Model performance monitoring**: outcomes (defaults) are only observed with a lag of 30–90 days. Monitor proxy metrics immediately (score distribution, adverse action rate, model output entropy) and lagged outcome metrics (AUROC by vintage cohort).

**Alert tiers**: Yellow (investigate) — PSI > 0.1 for any key feature; Orange (escalate) — PSI > 0.25 or AUROC drops below acceptance threshold; Red (halt and review) — degenerate model output distribution, API error rate > 1%, or fair lending test failure.

### Human-in-the-Loop Review

GDPR Article 22, ECOA, and SR 11-7 each independently require that automated credit decisions be subject to genuine human review upon request. Three tiers:

- **Tier 1 — Clear approvals**: predicted PD well below risk appetite with no adverse flags. Human review limited to a random quality-control sample.
- **Tier 2 — Borderline cases**: predicted PD near the decision threshold, or a high-impact SHAP feature that the reviewer should verify. Active human review before decision communication.
- **Tier 3 — Appeals**: borrower has exercised their right (GDPR or FCRA) to request human review. The reviewer must have access to the complete decision record, including the SHAP explanation, and must document their independent assessment.

**Automation bias warning**: research shows that when an automated system's recommendation is displayed prominently, reviewers are strongly anchored to it. Mitigations: display the model recommendation only after the reviewer has formed an independent assessment, present the SHAP waterfall prominently, and require reviewers to document reasoning before seeing the model's decision.

### Regulatory Documentation

A complete model documentation package for SR 11-7 and GDPR Article 22 compliance includes:

**Model Development Report (MDR)**: business need and intended use; conceptual framework; training data (sources, vintage, sampling, label construction); model selection; in-sample and out-of-sample performance metrics; known limitations. For LLMs: additionally document base model provenance and licence, fine-tuning procedure and hyperparameters, any few-shot examples or system prompts, and the structured generation grammar.

**Model Validation Report (MVR)**: scope and approach; conceptual soundness findings; outcome analysis on an independent validation dataset; sensitivity analysis; fair lending analysis; model risk rating (Low, Moderate, High).

**GDPR Article 22 Transparency Documentation**: a plain-language explanation of the logic involved, the significance of the decision, and the envisaged consequences — translating SHAP values into language understandable by a consumer without financial or technical background. This plain-language generation is itself a task well-suited to a constrained LLM operating on the structured SHAP output.

---

## Summary

This lecture has traced the full stack of LLM-based credit risk: from data sourcing and regulatory constraints, through model design (fine-tuning, constrained generation, calibration), to household applications (decision support and persona simulation), model evaluation (AUROC, KS, Gini, SR 11-7), and production deployment (monitoring, human-in-the-loop, regulatory documentation).

The through-line is that credit AI is not merely a prediction problem — it is a regulated sociotechnical system. Every design choice from the loss function to the API schema has implications for fairness, explainability, and regulatory compliance. LLMs add significant value precisely in the tasks where traditional approaches fail: unstructured text, thin-file borrowers, complex reasoning — but only when embedded in a governance framework that meets the legal standard of accountability.
