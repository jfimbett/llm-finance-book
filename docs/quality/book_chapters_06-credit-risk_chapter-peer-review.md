# Peer Review: Chapter 6 — LLMs for Credit Risk Analysis

**Manuscript:** "Large Language Models in Finance" — Chapter 6  
**Reviewer:** Anonymous  
**Date:** 2026-05-31  
**Verdict:** MINOR_REVISION

---

## 1. Significance

The chapter addresses a genuinely important and timely topic. Credit risk is one of the highest-stakes applications of automated decision-making, and the intersection with LLMs raises novel questions in model governance, interpretability, and regulatory compliance that are not adequately treated in the existing textbook literature. The decision to integrate technical modelling (fine-tuning, constrained decoding, SHAP) with regulatory frameworks (FCRA, ECOA, GDPR, SR 11-7) and behavioural economics (bounded rationality, persona simulation) within a single chapter is ambitious and largely successful. The chapter would be a valuable contribution to any graduate curriculum in quantitative finance or financial technology.

---

## 2. Technical Correctness

**Strengths:**

- The Gini = 2·AUROC − 1 identity is derived formally and correctly using the CAP/Lorenz curve framework. The proof is rigorous and self-contained, which is rare in textbooks that typically state this identity without proof.
- The Merton structural model equations (Eq. 6.3–6.5) are correct. The definition of the risk-neutral default probability $\Phi(-d_2)$ is consistent with standard usage.
- The LoRA parameterisation (Eq. 6.7) is correctly stated. The parameter reduction calculation ($r=8$, $d=768$ giving factor ~48) is approximately correct: full fine-tuning of one weight matrix requires $d^2 = 589{,}824$ parameters; LoRA requires $2dr = 12{,}288$, a reduction of approximately 48×. This arithmetic is correct.
- The SHAP Shapley value formula (Eq. 6.19) is the standard formulation from Lundberg and Lee (2017). The three axioms (Efficiency, Symmetry, Dummy) are correct and sufficient to characterise the Shapley value uniquely.
- The constrained decoding formulation (Eq. 6.9–6.10) correctly presents masked softmax normalisation. The intuition that the implied probability is not the model's confidence but a generated number is an important and correctly-stated distinction.

**Technical concerns:**

1. The utility-fitting objective (Eq. 6.12) is presented as a squared deviation from the expected utility of the lottery, but the objective is only zero at a true indifference point if the CRRA utility values on both sides of the expression are on the same scale. The use of $U_\gamma(\varepsilon)$ as a floor introduces a scale dependency on the choice of $\varepsilon$ that is not discussed. For $\gamma > 1$, different values of $\varepsilon$ yield qualitatively different $\hat\gamma$ estimates. This should be acknowledged and a recommended value of $\varepsilon$ suggested.

2. The definition of the KS statistic (Eq. 6.14) writes the second equality $\sup_s |F_+(s) - F_-(s)| = \sup_s |\text{TPR}^{-1}(s) - \text{FPR}^{-1}(s)|$. The second expression is not standard: TPR and FPR are functions of the threshold $t$, not of $s$, so $\text{TPR}^{-1}$ has an unusual meaning here. The intent appears to be to express the KS statistic in terms of the ROC parameterisation, but the notation is non-standard and may confuse readers. The definition should either be corrected or a footnote added clarifying the notation.

3. The PSI formula (Eq. 6.18) requires $q_b > 0$ for all bins to avoid undefined $\ln(p_b/q_b)$. This is a common practical failure mode that is not mentioned. A practical note on bin merging or floor values is needed.

---

## 3. Exposition Quality

**Strengths:**

- The opening narrative (Apple Card controversy, CFPB mortgage shopping study) is exceptionally well-crafted. It situates the technical content within high-stakes real-world events that are intrinsically motivating for the target audience.
- The credit scoring arc (Section 6.2.1) provides an excellent historical and modelling context that guides the reader from simple discriminant analysis through structural models to LLMs. This narrative structure is pedagogically superior to a purely technical presentation.
- The Maria and Thomas persona examples (Example 6.3) are the strongest single pedagogical element in the chapter. They make abstract concepts from utility theory and bounded rationality tangible and memorable, and they correctly model the contrasting reasoning styles without caricature.
- Section transitions are generally smooth, and forward/backward cross-references are appropriately placed.

**Exposition concerns:**

1. **Fairness metrics gap.** The chapter discusses ECOA's disparate-impact prohibition in detail (Section 6.1.2) and SR 11-7's requirement for disparate-impact testing (Section 6.5.2), but provides no formal definition of any fairness metric. Readers are told that disparate-impact testing is required but are not equipped to perform it. At minimum, demographic parity difference and equalised odds difference should be formally defined, with a note on their relationship to the ECOA business-necessity defence.

2. **MMD and Fréchet distance undefined.** Section 6.6.2 recommends maximum mean discrepancy (MMD) and Fréchet distance for embedding drift detection without defining either concept. Readers encountering these terms for the first time are left without a foundation for implementation.

3. **Exercise set is severely underdeveloped.** Only one exercise exists for a chapter that spans credit data, default prediction, probability calibration, persona simulation, model risk governance, and deployment. This is the most significant structural weakness. The project's own conventions (CLAUDE.md) require at least one exercise at each of `[B]`, `[I]`, and `[A]` difficulty levels. The current chapter does not satisfy this requirement.

---

## 4. Exercise Quality

The single exercise present (Illustration Exercise 6.1, ROC curve and KS statistic on UCI German Credit) is well-designed: it is concrete, reproducible, and maps directly to defined metrics (AUROC, KS, Gini). Part (a) verifies the Gini identity computationally, which is good practice. Parts (b) and (c) extend naturally to feature encoding and model interpretation.

However, the chapter's scope demands a substantially richer exercise set. The following gaps are significant:

- No exercise on fine-tuning or LoRA implementation.
- No exercise on probability calibration (Platt scaling or isotonic regression).
- No exercise on constrained decoding or structured generation.
- No exercise on persona simulation or calibration against survey data.
- No exercise on SHAP computation or adverse action reason generation.
- No exercise on PSI or drift detection.

The exercises that exist are of high quality; there are simply far too few of them.

---

## 5. Minor Issues

- Line 699: the second equality in Definition 6.4 (KS statistic) uses non-standard notation for $\text{TPR}^{-1}$ and $\text{FPR}^{-1}$; should be clarified or removed.
- Line 847–848: `\captionof{table}` inside a non-float environment risks caption counter inconsistency; should be a proper `table` float.
- Definition 6.3 (Bounded Rationality, line 442) should include a direct citation to Simon (1955), which is already in the bibliography.
- The LoRA formula (Eq. 6.7) silently assumes a square weight matrix; a footnote for the general rectangular case would be helpful for readers familiar with the original paper.

---

## 6. Verdict: MINOR_REVISION

The chapter is technically sound, well-written, and addresses an important topic with appropriate depth and regulatory grounding. The primary issues are:

1. **Critical:** The exercise set must be expanded to cover all major sections (fine-tuning, calibration, persona simulation, SHAP, deployment), with difficulty tags `[B]`, `[I]`, `[A]`.
2. **Important:** Fairness metrics (demographic parity, equalised odds) must be formally defined to back up the ECOA disparate-impact discussion.
3. **Important:** MMD and Fréchet distance should be defined or referenced.
4. **Minor:** KS definition notation, PSI bin-zero caveat, utility-fit $\varepsilon$ sensitivity, `\captionof` float issue, bounded rationality citation.

None of these issues require structural revision of the chapter. They can be addressed in a targeted revision without re-writing existing content. The chapter is recommended for **MINOR_REVISION** with no re-review required if the issues above are addressed.
