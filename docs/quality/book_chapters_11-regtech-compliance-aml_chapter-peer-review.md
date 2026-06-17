# Peer Review: Chapter 11 — RegTech, Compliance, and Anti-Money Laundering

**Manuscript:** *Large Language Models in Finance*, Chapter 11  
**Author:** Juan F. Imbet (Paris Dauphine – PSL University)  
**Reviewer:** Anonymous  
**Date:** 2026-05-31  
**Verdict:** MINOR_REVISION

---

## Summary

This chapter provides a thorough and well-organised treatment of large language models applied to regulatory technology, compliance, and anti-money laundering. The author demonstrates command of both the regulatory landscape (EU AI Act, MiFID II, Basel III, SR 11-7, GDPR, FATF) and the underlying technical architectures (RAG pipelines, entity resolution, agentic systems). The writing is clear, the formal definitions are precise, and the examples are well-chosen and grounded in realistic scenarios. The chapter would be a valuable addition to any LLM-in-finance textbook and addresses an underserved area of the applied NLP literature. The revisions requested below are minor in nature and do not require fundamental restructuring.

---

## 1. Significance

**Assessment: Strong**

The chapter addresses a genuinely important and timely intersection: the deployment of LLMs in high-stakes regulatory environments where explainability, auditability, and governance are not optional engineering concerns but legal requirements. The author correctly identifies that most existing LLM literature focuses on capability without adequate attention to governance, and the chapter fills this gap effectively. The combination of formal scoring frameworks (Adverse Media Index, Equation 4) with practical workflow design and governance requirements is particularly valuable for the practitioner audience.

The decision to include the EU AI Act risk-tier classification as a first-order organising framework is well-judged; it situates the chapter's technical content within the regulatory reality that financial institutions face today.

**Minor concern:** The chapter claims that the Adverse Media Index (AMI) formulation in Equation 3 follows \citet{chen2025aml}. If this is original work developed for the book, the attribution should be clarified. If it is a direct reproduction of the cited paper's formulation, the components (especially the logistic function application and the recency decay factor) should be compared to the source to ensure they are faithfully reproduced.

---

## 2. Technical Correctness

**Assessment: Mostly correct; one verification needed**

**Formal definitions:** The four definitions (EU AI Act tiers, FPR/PPV in AML screening, model risk under SR 11-7, entity resolution as pair classification) are all technically sound. The FPR and PPV formulas in Definition 3 are correct set-theoretic expressions. The AMI formula is well-specified and internally consistent.

**Equations:**
- Equation 1 (FPR/PPV): Correct.
- Equation 2 (RRF): Correct reciprocal rank fusion formulation consistent with Cormack and Lynam (2009).
- Equation 3 (AMI): Correct. The dimensionality of $\mathbf{w}^\top \mathbf{e}_i$ is consistent ($\mathbf{w} \in \mathbb{R}^K$, $\mathbf{e}_i \in \{0,1\}^K$). The logistic wrapper ensures the output is in $[0,1]$.
- Equation 4 (XBRL retrieval): Functionally correct but requires a typographic check — the LaTeX source should be verified to ensure the closing `\right]` bracket is present and the equation renders without a mismatched delimiter.

**Claim requiring citation:** The statement that global AML compliance costs exceeded $270 billion annually (Section 4 context) is a specific quantitative claim presented without any citation. This must be sourced.

**Claim requiring additional support:** The 95–99% FPR range for AML screening systems (Definition 3) is supported by a single FinCEN citation. Given that this statistic is the motivating empirical fact for the entire AML-with-LLMs argument, corroboration from additional independent studies (academic or industry) would strengthen the claim.

**Unsupported comparative assertion:** The statements in Section 3 that LLMs "substantially outperform rule-based systems" and that "relation extraction at scale is a task where LLMs substantially outperform rule-based systems" (Section 3.3) are presented without any performance benchmarks or citations. In a rigorous academic text, quantitative comparisons should be substantiated.

---

## 3. Exposition Quality

**Assessment: High; minor stylistic note**

The chapter's structure is logical and well-signposted. The context boxes that open each major section are an effective device: they orient the reader, provide motivation, and establish stakes before technical detail begins. The progression from regulatory framework to technical architecture to governance to summary is coherent and appropriate for the subject.

The worked examples are strong. The GDPR Article 22 / A. Petrov example (Example 11.1) is particularly effective: it concretises an abstract legal right in a scenario that directly motivates the technical design requirements that follow. The MRM governance example (Example 11.3) provides a practical instantiation of the abstract framework that practitioners will find directly applicable.

**Stylistic note:** Several sentences in Section 1 are overly long (upwards of 70–80 words), particularly the sentence enumerating five overlapping regulatory frameworks in the second paragraph of the regulatory landscape context box. Breaking these into shorter sentences would improve readability without any loss of precision.

**Missing code examples:** The book targets engineers, data scientists, and quants, and Python is specified as the project language. Chapter 11 contains no code examples, notebook references, or implementation illustrations. While this may be a deliberate choice for a governance-heavy chapter, even a minimal illustration — a short Python snippet showing a RAG pipeline query or a structured JSON output for an adverse media screening result — would bridge the conceptual treatment with the practitioner's daily toolkit. This is the chapter's most significant pedagogical gap.

**Missing exercises:** The project's quality conventions require exercises at beginner, intermediate, and advanced levels. No exercises are present. This is a structural deficiency that should be addressed in revision.

---

## 4. Exercise Quality

**Assessment: Not present — must be added**

The chapter contains no exercises. For a book targeting a mixed academic and practitioner audience, exercises are essential for consolidating learning. The chapter covers material that is highly amenable to well-designed exercises:

- **Beginner:** Calculate the FPR and PPV for a simple AML screening scenario given $|P|$, $|N|$, and $|\hat{P}|$ values.
- **Intermediate:** Design a RAG-based adverse media pipeline for a specific subject type, specifying retrieval, ranking, and scoring components, and calculate an AMI score given hypothetical document inputs.
- **Advanced:** Implement a Python prototype of the XBRL tagging system described in Section 4.1, using a sentence embedding model and cosine similarity retrieval over a small XBRL taxonomy excerpt.

---

## 5. Required Revisions for MINOR_REVISION

1. **Add citation for the $270 billion AML compliance cost figure** (Section 4 context box).
2. **Add 1–2 additional citations for the 95–99% FPR claim** (Definition 3 / Section 2.1).
3. **Add citations or benchmark data for comparative LLM performance claims** in Section 3.1 (entity resolution) and Section 3.3 (relation extraction).
4. **Verify Equation 4 bracket matching** in the compiled PDF; correct if a delimiter is missing.
5. **Add at least one Python code example** illustrating a core technical concept from the chapter (RAG pipeline, entity resolution, XBRL tagging, or AMI calculation).
6. **Add exercises** at beginner, intermediate, and advanced levels (project convention requires at least one of each).
7. **Clarify the AMI attribution**: confirm whether Equation 3 is original or reproduced from \citet{chen2025aml}, and adjust the attribution language accordingly.

---

## 6. Optional Suggestions (Non-blocking)

- A brief subsection or remark on the FATF risk-based approach would give that framework parity with the other four frameworks discussed in Section 1.
- The cross-reference to `Chapter ch:xai-explainability` in the Further Reading section should be verified as a valid compiled label; if the chapter does not yet exist, the reference should be qualified as "(forthcoming)".
- Breaking the longest sentences in Section 1 into two shorter sentences would improve scannability.

---

## Verdict: MINOR_REVISION

The chapter is well-written, technically sound, and covers its topic comprehensively. The required revisions are targeted additions (citations, code example, exercises) that do not require restructuring or substantive rewriting. Upon completion of the revisions listed above, the chapter should be ready for acceptance.
