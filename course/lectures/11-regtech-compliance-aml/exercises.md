# Exercises — Lecture 11: RegTech, Compliance, and Anti-Money Laundering

## Exercise 1 [B]
**Topic:** The Regulatory Landscape for AI in Finance

The EU AI Act introduces a risk-based classification system for AI applications. Under this framework, certain financial AI systems are designated as "high-risk."

(a) List three categories of financial AI use cases that the EU AI Act would likely classify as high-risk, and briefly explain the rationale for each classification.

(b) How does the SR 11-7 guidance from the Federal Reserve differ from the EU AI Act in its approach to model risk? What are the key obligations it places on banks that deploy models for credit, trading, or compliance decisions?

(c) A bank wants to deploy an LLM to assist relationship managers in generating client communications. Identify two GDPR provisions that are directly relevant to this deployment and explain how they constrain the system's design.

## Exercise 2 [I]
**Topic:** KYC and Sanctions Screening

A compliance team maintains a customer database with names in Latin script and needs to screen against a sanctions list that includes names in Arabic, Cyrillic, and Chinese scripts, as well as multiple transliterations.

(a) Write a Python function `fuzzy_match_names(query: str, candidates: list[str], threshold: float) -> list[tuple[str, float]]` that returns all candidate names whose fuzzy similarity score (using any library of your choice, e.g., `rapidfuzz`) meets or exceeds the threshold. Return results as a list of `(name, score)` tuples sorted by descending score.

(b) Describe two limitations of purely string-based fuzzy matching for PEP and sanctions screening, and explain how an LLM-based embedding approach could address each limitation.

(c) Using the Hugging Face `transformers` library and a multilingual model (e.g., `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`), write a short code snippet that encodes a query name and a list of candidate names, then ranks candidates by cosine similarity.

## Exercise 3 [A]
**Topic:** Governance and Audit Trails

Model risk management frameworks such as SR 11-7 were designed for traditional statistical models. LLMs introduce qualitatively new failure modes (hallucination, prompt injection, distributional shift) that these frameworks did not anticipate.

(a) Identify three LLM-specific failure modes that are not adequately addressed by the SR 11-7 validation framework. For each, propose a concrete testing or monitoring procedure a compliance team could adopt.

(b) Design a human-in-the-loop workflow for an LLM-assisted SAR drafting system. Your design should specify: (i) which steps are fully automated, (ii) which steps require human review, (iii) what information is surfaced to the human reviewer, and (iv) how the system maintains an immutable audit trail.

(c) Regulators are beginning to require that AI-driven compliance decisions be explainable. Critically assess whether current LLM explainability techniques (e.g., attention visualization, LIME, SHAP applied to token embeddings) are sufficient to meet regulatory explainability standards. What open research challenges remain?
