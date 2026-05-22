# Exercises — Lecture 6: LLMs for Credit Risk Analysis

---

**Exercise 1 [B] — Calibrating Implied Default Probabilities**

Using the Lending Club public loan dataset (or any open credit dataset), prompt a pre-trained language model to produce a structured JSON output of the form `{"default_probability": <float>}` for each loan description. Use constrained decoding (e.g., the `outlines` or `guidance` library) to guarantee well-formed JSON.

1. Extract the scalar default probability from the structured output for 500 loans.
2. Compare the raw LLM-implied probabilities against observed default rates by decile. Plot the calibration curve.
3. Apply Platt scaling to recalibrate the probabilities. Report the Brier score before and after calibration.
4. Discuss what the miscalibration pattern (if any) tells you about the model's training data relative to the credit domain.

*(Covers Section 2: Credit Risk Modelling with LLMs)*

---

**Exercise 2 [I] — Persona Agents for Mortgage Choice**

Design a persona-agent experiment in which LLM agents representing households with different economic characteristics make a mortgage product choice between a fixed-rate and a variable-rate mortgage under specified macroeconomic conditions.

1. Define at least four personas that vary along three dimensions: income level (low / high), financial literacy (low / high), and risk aversion (low / high). Write a system prompt for each persona that encodes these characteristics consistently.
2. Present each persona with the same mortgage choice scenario (loan amount, current rates, projected rate paths) and record the choice and stated reasoning.
3. Vary the macroeconomic scenario (rising rates, falling rates, uncertain rates) and collect choices across all personas and scenarios ($4 \times 3 = 12$ responses minimum).
4. Analyse whether the persona differences produce choice patterns consistent with economic theory (e.g., more risk-averse agents preferring fixed rates). Identify any persona that behaves inconsistently.
5. Discuss how you would calibrate the personas against the Bank for International Settlements Household Finance and Consumption Survey data.

*(Covers Section 4: Persona Agents and Behavioural Simulation)*

---

**Exercise 3 [A] — End-to-End Credit Risk Pipeline with SR 11-7 Documentation**

Build and document a production-ready credit risk pipeline that uses a fine-tuned language model for default prediction. The pipeline should cover the full model lifecycle from data to deployment.

1. **Data:** Obtain a credit dataset (e.g., Give Me Some Credit, Home Credit Default Risk, or HMDA data). Document data sources, lineage, and any protected attributes present. Apply a debiasing step and verify demographic parity and equal opportunity metrics before and after.
2. **Model:** Fine-tune a BERT-class model (or use LoRA on a larger model) for binary default classification. Report AUROC, KS statistic, and Gini coefficient on a held-out test set stratified by vintage year.
3. **Interpretability:** Apply SHAP to produce a feature importance ranking and a per-instance explanation for ten randomly selected decisions. Write a one-paragraph "right to explanation" statement as required by GDPR Article 22 for three of these decisions.
4. **Monitoring:** Design a monitoring schema: define at least two statistical tests for input data drift and one test for output probability drift. Specify alert thresholds and escalation procedures.
5. **Documentation:** Produce a model risk document following the SR 11-7 framework structure: (a) model overview and purpose, (b) data and assumptions, (c) conceptual soundness, (d) outcome analysis, (e) ongoing monitoring plan.

*(Covers Sections 2, 5, and 6: Modelling, Evaluation, and Deployment)*
