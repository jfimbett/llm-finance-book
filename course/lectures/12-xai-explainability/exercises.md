# Exercises — Lecture 12: Explainability and XAI in Finance

## Exercise 1 [B]
**Topic:** Why Explainability Matters in Regulated Finance

The EU AI Act classifies credit scoring and loan evaluation as high-risk AI applications. In your own words, explain why explainability is a legal requirement in this context and not merely a desirable property. Identify at least two specific obligations that a financial institution using an LLM-based credit model must fulfill under the EU AI Act or SR 11-7, and describe how failing to meet them could result in regulatory sanction.

## Exercise 2 [I]
**Topic:** LLM-Native Explainability Mechanisms

A consumer bank wants to use an LLM to generate ECOA-compliant loan denial letters. Using a language model of your choice (e.g., via the Hugging Face `transformers` library or the OpenAI API), implement a Python function `generate_denial_letter(applicant_profile: dict, model_decision: str) -> str` that produces a denial letter containing: (a) the primary reason for denial, (b) the specific factors that drove the decision, and (c) information about the applicant's right to obtain a free copy of their credit report. Test your function on at least two synthetic applicant profiles with different denial reasons.

## Exercise 3 [A]
**Topic:** Evaluating the Quality of Explanations

Design and describe a human-subject evaluation study to assess the faithfulness and usefulness of LLM-generated explanations for investment recommendation disclosures under MiFID II. Your answer should address: (a) the participant pool (who are the domain experts and why), (b) the stimuli (what explanation types will be compared), (c) the metrics you will collect (both quantitative and qualitative), (d) a proposed statistical analysis plan, and (e) at least two potential confounds and how you would control for them. Conclude by discussing what a positive result would imply for the regulatory acceptability of LLM-generated MiFID II disclosures.
