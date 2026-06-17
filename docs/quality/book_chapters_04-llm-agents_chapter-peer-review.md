# Peer Review: Chapter 4 — LLM Agents and Finance Applications

**Manuscript:** book/chapters/04-llm-agents/chapter.tex  
**Reviewer:** Anonymous  
**Date:** 2026-05-31  
**Venue:** Large Language Models in Finance (textbook manuscript)  
**Verdict:** MAJOR_REVISION

---

## Summary

This chapter addresses LLM-based agent architectures and their application to finance, covering the perceive-reason-act cycle, ReAct and Reflexion patterns, tool use, workflow orchestration, retrieval-augmented generation, five finance-specific applications, and a governance/safety section. The scope is appropriate and well-calibrated for the intended audience. The theoretical grounding is generally sound, the finance applications are concrete and practically relevant, and the writing is clear. However, the chapter has two critical structural deficiencies and several technical gaps that require major revision before the chapter is ready for student use.

---

## 1. Significance

**Score: High**

The topic is highly timely and relevant. LLM agents represent the frontier of applied AI in financial services, and there is a genuine shortage of textbook-quality treatments that bridge theory (formal agent definitions, RAG formalisation) with practice (Python tool registration, multi-agent pipelines, governance frameworks). The chapter's coverage of adversarial robustness, regulatory obligations (MiFID II, EU AI Act), and human-in-the-loop design patterns is particularly valuable for an industry-facing audience and is not found in comparable texts.

The selection of finance applications (earnings call analysis, report generation, portfolio assistants, filing Q&A, trading signals) covers the most commercially deployed use cases and is well-supported by recent literature citations. The FinanceBench benchmark result (GPT-4-Turbo incorrectly answers 81% of filing Q&A questions) is an appropriately sobering data point that prevents the chapter from reading as uncritical advocacy.

---

## 2. Technical Correctness

**Score: Good with reservations**

**Strengths:**
- The PRA loop formalisation (Definition 4.2) correctly declares all necessary spaces including the environment state space.
- The RAG marginal (Equation 4.4) is properly normalised with the sum-over-corpus formulation.
- BM25 (Equation 4.6) is correctly stated with the IDF term explicitly defined in-line.
- The hybrid search score (Equation 4.7) correctly addresses the scale mismatch between cosine similarity and BM25 scores through min-max normalisation and offers RRF as a scale-free alternative.
- The chained-hash audit trail (Definition 4.12) is a well-formed tamper-evidence construction.
- The Reflexion loop definition (Definition 4.4) correctly distinguishes within-episode PRA iteration from cross-episode self-improvement.

**Issues requiring correction:**

1. **Tree-of-Thought citation (line 202):** Tree-of-Thought prompting is attributed to `\cite{wang2023survey}`, which is a survey of LLM agents, not the original ToT paper. The correct citation is Yao et al. (2023), "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" (NeurIPS 2023). This misattribution would be noticed by any reader familiar with the literature.

2. **DCF tool: undeclared numerical precondition (Listing 4.1, lines 434-459):** The Gordon Growth Model terminal value formula requires WACC > terminal growth rate. When this condition fails, the formula produces a negative or undefined enterprise value. The Pydantic schema validates each field in isolation and cannot enforce the cross-field constraint. A runtime guard is needed. For a pedagogical listing used by students learning both LLMs and finance, this silent failure mode is a teaching risk.

3. **ANN approximation factor definition (Definition 4.9, lines 834-844):** The approximation guarantee is stated in terms of Euclidean distance (`\|\mathbf{q} - \mathbf{v}\|`), but the retrieval criterion in Equation 4.3 and throughout the chapter uses cosine similarity. Euclidean and cosine metrics are not equivalent in general. The definition should either (a) be restated in terms of cosine distance `(1 - cosine)`, or (b) note explicitly that the ANN guarantee applies under a metric consistent with the retrieval criterion used.

4. **RAGAS faithfulness metric (Definition 4.11):** The definition describes faithfulness as "the fraction of claims in $a$ directly supported by at least one chunk in $\mathcal{C}$." This is the correct conceptual definition, but RAGAS implements this via an LLM judge, which introduces model-dependent variance. The definition does not acknowledge this implementation dependency. For academic rigour, a note that the metric is an LLM-approximated quantity with known reliability limitations would be appropriate.

5. **Equation 4.7 (citation-verified answer, line 1299-1305):** The notation $\hat{a} = \{s_j \in a : ...\}$ treats $a$ as a set, but $a$ has previously been defined as a generated answer (a string). The chapter should introduce a decomposition operator $\text{Claims}(a) = \{s_1, \ldots, s_m\}$ before defining the filtered answer.

---

## 3. Exposition Quality

**Score: Good with significant structural issues**

**Strengths:**
- The motivating context boxes are effective and make excellent use of concrete institutional examples (Morgan Stanley advisor tool, Mata v. Avianca brief, hedge fund earnings monitor).
- The ReAct filing retrieval example (Example 4.2, lines 227-255) is a model of how to trace an agent trajectory in a textbook format.
- The portfolio Q&A interaction (Example 4.7, lines 1246-1259) correctly emphasises the data vintage transparency requirement — a practically important point often omitted in tutorial treatments.
- The governance section correctly identifies prompt injection as the key adversarial risk and the four-layer defence hierarchy is well-structured.
- The signal staleness remark (Remark 4.2, lines 1342-1353) is a valuable practitioner warning that prevents over-interpretation of the trading signals section.

**Issues requiring correction:**

1. **Critical structural defect — §4.3 and §4.5 wrapped in `\begin{context}`:** The context environment is used as the primary content wrapper for §4.3 (Skills, Hooks, Frameworks, Multi-Agent; lines 556-768) and §4.5 (all five finance applications; lines 1075-1355), as well as §4.6 (Governance; lines 1362-1593). These sections contain formal definitions, equations, code listings, and substantive technical content. Placing this material inside a context box — which is typographically and semantically a motivating sidebar — is structurally incorrect and likely a copy error (missing `\end{context}` at the close of the introductory paragraphs). The deepdive environment, used correctly in §4.1 and §4.2, should be used for the substantive technical content in §4.3, §4.5, and §4.6.

2. **Absent exercise suite:** A single exercise (lines 1058-1070) covering only RAG retrieval ranking is insufficient for a chapter of this scope with 8 learning objectives. Per the project's conventions, at least one beginner [B], one intermediate [I], and one advanced [A] exercise must be present. The missing exercises span: implementing a ReAct loop from scratch [I], designing a tool suite for a financial task [I], comparing memory architectures for a given scenario [B], building a multi-agent pipeline [A], conducting a RAGAS evaluation [I], and deploying a governance-compliant agent with HITL checkpoints [A]. Without these exercises, students have no structured practice vehicle for Objectives 1-4 and 6-8.

3. **No framework code example:** §4.3.3 discusses LangChain, LlamaIndex, and AutoGen in well-structured prose but provides no code. Given that Objective 6 requires readers to "orchestrate multi-agent workflows using at least one modern framework," the absence of even a minimal working example is a significant pedagogical gap.

4. **Section 4.3 subsection 4.3.3 LangChain description may be outdated:** The description of LangChain's "LangChain Expression Language (LCEL)" as the declarative composition API and the characterisation of its agent module as implementing "ReAct-style loops with configurable tool libraries" is accurate for LangChain v0.1. LangChain v0.2+ deprecated several of these APIs in favour of LangGraph for agentic workflows. A note on version applicability or a pointer to LangGraph would prevent confusion for readers implementing the examples.

---

## 4. Exercise Quality

**Score: Poor**

The chapter contains exactly one exercise (lines 1058-1070). It is a well-designed illustration exercise linking to a companion notebook, but it covers only one learning objective (RAG retrieval ranking, partially addressing Objective 5). The following exercises are absent:

- **[B] Beginner:** Trace through the PRA loop definition step-by-step for a given financial scenario; identify observation, memory update, and action at each step.
- **[B] Beginner:** Given a set of queries and document types, classify the appropriate memory architecture (in-context, RAG, persistent) for each.
- **[I] Intermediate:** Implement a minimal ReAct-style agent that uses a mock tool to answer a financial question; trace the thought-action-observation sequence.
- **[I] Intermediate:** Design and implement a tool suite (3 tools with Pydantic schemas) for a portfolio analysis task; test with sample inputs including error cases.
- **[I] Intermediate:** Evaluate a RAG pipeline using RAGAS metrics on a sample of FinanceBench questions; identify the primary failure mode (low faithfulness vs. low recall).
- **[A] Advanced:** Implement a two-agent system (analyst + compliance checker) using AutoGen; demonstrate that the compliance agent blocks a hallucinated recommendation.
- **[A] Advanced:** Design a governance-compliant agent architecture for an investment recommendation workflow; specify HITL checkpoints, audit trail schema, and prompt injection defences.

The present exercise provides no difficulty tag and has no beginner-level entry point. This must be remedied before the chapter can be used for teaching.

---

## 5. Minor Comments

- Line 86: `\cite{wang2023survey}` for the PRA cycle derivation from reinforcement learning is acceptable since the survey paper covers this, but a primary RL textbook citation (e.g., Sutton and Barto) would be more appropriate for the foundational attribution.
- Lines 425-426: Unused imports (`Optional`, `datetime`) in Listing 4.1 should be removed.
- Lines 647-648: The cited years for LangChain (2022) and LlamaIndex (2022) are correct for initial releases but the frameworks have undergone major version changes; a note on the version context would be helpful.
- Line 905 (BM25 parameter range): The text states $k_1 \in [1.2, 2.0]$ and $b = 0.75$ as "tuning parameters." These are conventional defaults, not formal tuning ranges. The text implies they should be tuned on a held-out set (which is correct) but the ranges given are Okapi BM25 defaults, not general bounds.

---

## Verdict: MAJOR_REVISION

The chapter has strong intellectual content and would be an excellent resource once the structural and completeness issues are addressed. The two BLOCKERs (absent exercise suite; sections 4.3/4.5/4.6 wrapped in context environments) and the technical corrections (ToT citation, DCF precondition, ANN metric consistency, equation notation) require substantive revision. The revised chapter should be re-reviewed, with particular attention to the exercise suite and the context/deepdive environment usage.
