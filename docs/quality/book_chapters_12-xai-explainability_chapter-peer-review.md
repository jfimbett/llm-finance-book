# Peer Review: Chapter 12 — Explainability and Interpretability of LLMs in Finance

**Book:** Large Language Models in Finance  
**Author:** Juan F. Imbet, Paris Dauphine - PSL University  
**Date:** 2026-05-31  
**Reviewer:** Anonymous (Academic Peer Review)  
**Verdict:** MINOR_REVISION

---

## Summary

This chapter provides a thorough and well-organised treatment of explainability and interpretability for large language models deployed in regulated financial settings. It covers the legal-regulatory motivation (EU AI Act, SR 11-7, ECOA, MiFID II), the main post-hoc attribution methods (SHAP, LIME, attention visualisation), LLM-native explanation mechanisms (chain-of-thought, counterfactuals, natural language justifications), three applied case studies, and evaluation paradigms for explanation quality. The topic is important, timely, and underserved in existing textbooks. The writing is clear and the level of technical rigour is appropriate for the stated mixed academic-industry audience.

The chapter is not ready for publication in its current form, but requires only targeted revisions (minor revision) rather than a fundamental rethink.

---

## Evaluation by Dimension

### 1. Significance and Relevance

**Rating: Strong**

The explainability challenge for LLMs in regulated finance is both practically urgent and intellectually substantive. The chapter correctly identifies the mismatch between the opaque computations of large transformers and the specific plain-language explanation requirements of ECOA, SR 11-7, EU AI Act Article 13, and MiFID II suitability assessments. This framing—explainability as a legal compliance requirement, not merely an ethical desideratum—is more practically grounded than much of the academic XAI literature and will be valuable to the book's target practitioners. The three case studies (hybrid credit pipeline, ECOA denial letter generation, MiFID II suitability disclosure) are well-chosen and cover the most consequential real-world deployment contexts.

### 2. Technical Correctness

**Rating: Mostly sound, with one significant gap**

The formal content is largely correct:

- The Shapley value formula (Definition 12.1, Equation 12.1) is stated correctly with the combinatorial weighting factor properly derived from the uniform ordering interpretation.
- The LIME objective (Definition 12.2) correctly specifies the kernel-weighted fidelity loss and the sparsity regulariser.
- The faithfulness-plausibility distinction (Definition 12.3) correctly follows Jacovi and Goldberg (2020) and is applied accurately in the analysis of attention weights.
- The sufficiency and comprehensiveness metrics (Equations 12.3–12.4) are standard and correctly stated.
- The regulatory analysis is accurate: the ECOA four-to-five specific reasons requirement, the 30-day notice window for Regulation B, and the MiFID II suitability pre-transaction requirement are all correctly described.

**Significant gap:** The chapter presents Integrated Gradients (Sundararajan et al. 2017) as the preferred audit-grade alternative to attention-based explanations (lines 392–396) and uses it in the MiFID II case study (line 688) without ever defining it. Given that the chapter provides full formal definitions for every other method it recommends, this asymmetry is conspicuous and weakens the chapter's claim to technical self-containment. A reader cannot evaluate the claim that Integrated Gradients provides "stronger faithfulness guarantees" without knowing what the method computes.

**Secondary gap:** The counterfactual generation procedure for discrete text inputs (lines 479–486) is described only in vague narrative terms despite the central importance of this operation for ECOA compliance. No specific algorithm, reference implementation, or even pseudocode is provided.

**Minor concern:** The self-consistency citation at line 445 appears to attribute a claim about structural detectability of differing reasoning traces to Wang et al. (2022), which is a paper about majority-voting over final answers. This citation should be verified and, if inaccurate, corrected.

### 3. Exposition Quality

**Rating: High**

The writing is direct, precise, and economical. Transitions between sections are clearly signposted (e.g., "Before examining methods designed specifically for language models..." at line 189; "The preceding sections developed the theoretical foundations. We now examine..." at lines 533–535). The pedagogical structure—legal motivation → formal methods → applied pipelines → evaluation → summary—is logical and effective.

The opening vignette (the loan officer receiving a model rejection she cannot explain) is an excellent pedagogical device that motivates the entire chapter. The Rudin remark (lines 173–183) presents a legitimate counter-view before defending the chapter's approach, demonstrating intellectual honesty.

The Further Reading section is particularly well-executed: it is specific, ordered by topic, and explicitly connects to other chapters in the book.

**Weakness:** The `\textbf{Stage N}` inline labels in Example 12.2 (lines 556–558) are stylistically inconsistent with the rest of the chapter's formatting conventions. Minor, but should be corrected.

### 4. Exercise Quality

**Rating: Absent — requires addition**

The chapter contains no exercises. This is the most significant structural deficiency. For a textbook chapter at this level, exercises are essential for consolidating learning and distinguishing the book from a survey article. The absence is particularly acute given that the chapter's learning objectives include several skill-based competencies (applying SHAP, designing counterfactual explanations, drafting ECOA notices) that are natural targets for exercises.

At minimum, the revised chapter should include:
- A [B]-difficulty exercise asking the reader to compute Shapley values for a small (three-feature) cooperative game by hand, reinforcing the formal definition.
- An [I]-difficulty exercise asking the reader to implement KernelSHAP for a pre-trained sentiment classifier applied to financial text, interpreting the output in a credit context.
- An [A]-difficulty exercise asking the reader to design an end-to-end explanation pipeline for a text-input LLM credit model that satisfies all four stages of the ECOA-compliant architecture described in Section 12.4.2, including the post-generation compliance filter.

---

## Specific Comments

1. **Line 392, citation key `sundararajan2020shapley`:** The Sundararajan & Taly (2017) Integrated Gradients paper is titled "Axiomatic Attribution for Deep Networks" and was published in ICML 2017, not 2020. The citation key conflates it with a different paper. Correct the key and verify the bibliography entry.

2. **Lines 394–396:** "Gradient-based attribution methods...provide stronger faithfulness guarantees." This claim needs either a formal statement of the guarantee (e.g., the completeness axiom, which IG satisfies) or a citation to a comparative evaluation. As stated it is assertoric.

3. **Lines 438–441, Definition 12.4 (faithfulness of traces):** The faithfulness condition — replacing $r_t$ with its negation causes the model to change $\hat{y}$ accordingly — is underspecified for non-binary outputs. The definition should clarify whether $\hat{y}$ is the argmax class label or a probability.

4. **Lines 479–486:** The two-stage algorithm for generating counterfactual explanations from text inputs is described in a single paragraph without algorithmic specificity. At minimum, cite a paper that implements such an approach (e.g., Polyjuice by Wu et al. 2021, or DiCE by Mothilal et al. 2020) and describe its key steps.

5. **Lines 724–729, Equation 12.3 (sufficiency):** The formula $1 - |f(x) - f(x_{e(x)})|$ is dimensionally problematic if $f$ produces probabilities in $[0,1]$, since sufficiency could be negative for large prediction gaps. Consider either normalising by the total prediction gap or re-stating as $1 - |f(x) - f(x_{e(x)})|/(f(x) - \mathbb{E}[f(X)])$.

6. **Lines 135, 668, 805, citation `cfainstitute2025xai`:** This 2025 CFA Institute report is cited three times. The bibliography entry should include the full URL and access date to allow readers to verify and retrieve the document.

7. **Section 12.3 (SR 11-7 gap):** Section 12.2 identifies SR 11-7 as requiring model-level documentation including sensitivity analysis and global feature importance. Sections 12.3 and 12.4 address only local, instance-level explanations. A brief treatment of global XAI instruments (global SHAP summary plots, partial dependence plots) with explicit reference back to SR 11-7 documentation requirements would close this gap.

---

## Verdict and Recommendation

**MINOR_REVISION**

The chapter makes a genuine contribution as a self-contained treatment of XAI/explainability for regulated financial LLM deployments. The core content is technically sound, the regulatory framing is accurate and detailed, and the exposition is of high quality. Revision should focus on: (1) adding exercises; (2) formally defining Integrated Gradients; (3) providing algorithmic detail for text-domain counterfactual generation; (4) adding brief global XAI coverage for SR 11-7 compliance; and (5) correcting the Sundararajan citation key and the self-consistency attribution claim. None of these require structural changes to the chapter.
