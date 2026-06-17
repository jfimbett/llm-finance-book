# Peer Review: book/chapters/07-applications-future/chapter.tex

**Manuscript:** Chapter 7 — Other Applications in Finance and Future Trends
**Book:** *Large Language Models in Finance* (Juan F. Imbet, Paris Dauphine – PSL University)
**Date:** 2026-05-31
**Reviewer:** Anonymous

---

## 1. Significance

**Rating: Strong**

This chapter addresses a genuine gap in the current LLM-in-finance literature: most papers and textbook chapters treat individual applications in isolation, while practitioners must make cross-cutting decisions about architecture selection, deployment governance, and regulatory compliance. The chapter's synthesis of deployment pattern selection heuristics (Tables 1 and 2), its application of the SR 11-7 model risk management framework to LLMs, and its formally stated fairness impossibility result all represent contributions that practitioners and researchers will find directly useful. The five open research problems are well-chosen and well-framed; the calibrated uncertainty quantification and feedback loop detection problems in particular are both underappreciated and tractable.

---

## 2. Technical Correctness

**Rating: Satisfactory with minor reservations**

The formal content is essentially correct throughout.

- The DAG workflow definition (Definition 3, lines 208–217) is standard and correctly stated.
- The fairness definitions (Definitions 7–9) and the impossibility proposition (Proposition 1) are accurately attributed to Chouldechova (2017) and Kearns & Roth (2019) and correctly stated.
- The reciprocal rank fusion formula (Equation 1) uses the conventional k=60 smoothing constant correctly.
- The SR 11-7 documentation checklist (Example 4) is accurate and reflects current regulatory interpretation.
- The GDPR Article 22 and MiFID II record-keeping discussion is accurate as of the 2024 EU AI Act adoption.

**Reservations:**

1. **OpenClaw (Section 3.3, lines 402–493):** The subsection makes specific factual claims about an open-source project's capabilities (privacy-by-default, local inference, multi-channel messaging) without independent citation or benchmark evidence. In academic publication, product-specific capabilities must be independently verified or qualified as the developer's claims.

2. **Code listing (Listing 1, lines 244–341):** The `classify_filing` function imports `json` inside the function body (line 291) — a Python anti-pattern — and contains no error handling for `json.JSONDecodeError`, which will crash the monitor loop on any non-JSON model output. A chapter that devotes substantive attention to production reliability and hallucination mitigation should not introduce a reliability anti-pattern in its primary code example.

---

## 3. Exposition Quality

**Rating: Strong**

The chapter is exceptionally well written for a technical text. Highlights:

- The retrospective "Where We Have Been" framing in Section 1 is effective and distinguishes this synthesis chapter from a mere appendix.
- The parallel definitional structure for fairness criteria facilitates comparison and cross-reference.
- The closing three-way distinction between "informational," "advisory," and "executive" agent outputs is a concise and practically useful conceptual contribution not present in the cited literature in this form.
- Prose is natural and free of the formulaic hedging and inflated structure that characterises much recent LLM-adjacent literature.

**One weakness:** The figure caption at lines 661–671 embeds three benchmark citations ("Chen et al., 2021", "Malo et al., 2014", "Maia et al., 2018") as plain text rather than `\cite{}` commands. These will not appear in the bibliography and cannot be cross-referenced. This is a formatting defect inconsistent with the chapter's otherwise careful citation practice.

---

## 4. Exercise Quality

**Rating: Inadequate**

The chapter contains a single formal exercise (Exercise ex:ch07-illustration, lines 674–688), which asks the reader to reproduce and extend a benchmark comparison figure. The exercise is suitable at intermediate difficulty but:

- It does not test the deployment pattern decision framework (Learning Objective 2).
- It does not test workflow DAG construction or any of the three automation patterns (Learning Objective 3).
- It does not test fairness metric computation or the impossibility result (Learning Objective 5).
- It does not test SR 11-7 documentation requirements (Learning Objective 6).
- It lacks a difficulty tag (`[B]`, `[I]`, or `[A]`).

For a chapter with eight stated learning objectives, one untagged exercise at a single difficulty level is insufficient for course-facing use. The required minimum per project conventions is one exercise at each of three difficulty levels.

---

## 5. Summary Assessment

| Criterion | Rating |
|---|---|
| Significance | Strong |
| Technical correctness | Satisfactory (with reservations) |
| Exposition quality | Strong |
| Exercise quality | Inadequate |

---

## 6. Required Revisions

1. **MAJOR — Exercise set:** Add at minimum two exercises covering at least three additional learning objectives, spanning [B] and [A] difficulty levels. Tag all exercises with `[B]`, `[I]`, or `[A]`.

2. **MAJOR — OpenClaw citations:** Either add independent citation or benchmark evidence for the capabilities described in Section 3.3, or explicitly qualify the claims as developer-reported (e.g., "according to the project documentation..."). Reframe if necessary as a design-pattern illustration rather than an authoritative tool recommendation.

3. **MAJOR — Figure caption citations:** Replace inline author-year strings in the `fig:ch07-illustration` caption with proper `\cite{}` commands and verify the corresponding bibliography entries exist.

4. **MINOR — Code error handling:** Add try/except around the `json.loads` call in `classify_filing` and move `import json` to module level.

5. **MINOR — Architecture table footnote:** Add a footnote to Table 2 clarifying that "Decoder-only: Weak" for labelled fine-tuning data refers to the data-scarce regime, not to the general impossibility of fine-tuning decoder-only models.

---

## Verdict

**MINOR_REVISION**

The chapter is of publication quality on its substantive content and exposition. None of the required revisions involve restructuring the chapter. The exercise gap is the most consequential issue for course use; the OpenClaw and citation issues are straightforward to correct.
