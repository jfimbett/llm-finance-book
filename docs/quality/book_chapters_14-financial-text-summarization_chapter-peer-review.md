# Peer Review: Chapter 14 — Financial Text Summarization and Information Extraction

**Manuscript:** "Large Language Models in Finance," Chapter 14  
**Reviewer:** Anonymous  
**Date:** 2026-05-31  
**Verdict:** MINOR_REVISION

---

## Summary

Chapter 14 covers information extraction and text summarization in financial documents,
spanning named entity recognition, relation extraction, financial document summarization,
table and numerical data extraction, and evaluation methodology. The chapter is well
organized and technically competent. It addresses a genuinely important topic that sits
at the intersection of NLP methodology and applied finance, and the treatment is
appropriately pitched for a mixed academic and industry audience. The writing is clear,
the literature coverage is strong, and the worked examples are pedagogically effective.
However, several issues require revision before the chapter meets the standards for a
research-grade textbook.

---

## 1. Significance

**Rating: High**

The topic is timely and commercially significant. Financial information extraction and
summarization are among the most active deployment areas for LLMs in practice, and the
literature coverage includes recent high-quality papers (ECTSum, FINER-139, FinQA,
SEC-BERT, FactCC) alongside foundational references (ROUGE, BERTScore, Loughran and
McDonald, Tetlock). The chapter's scope—from structured XBRL extraction through
abstractive summarization evaluation—is appropriately ambitious and the material
constitutes a coherent unit.

The inclusion of recent practitioner-oriented results (CookKazinnik2023, Siano2025,
LiGao2023, ShafferWang2024, ErnstbergerNazemi2025, WangWang2025) is a strength that
distinguishes this chapter from typical textbook treatments and connects academic
methodology to real-world deployment concerns.

---

## 2. Technical Correctness

**Rating: Mostly Correct — One Citation Error Requires Correction**

The technical content is largely accurate:

- The BIO labeling formalism and the cross-entropy NER loss are correctly described.
- The ROUGE-N formula (Equation 3) correctly expresses recall-oriented n-gram overlap
  against a reference set.
- The BERTScore cosine similarity formulation is correct, and the discussion of greedy
  token matching for precision and recall is accurate.
- The FactCC NLI-based factual consistency framework is correctly characterized.
- The joint entity-and-relation extraction scoring function (Equation 2) is a correct
  summary of the DyGIE++ architecture.

**Issue requiring correction:**

In Section 2.4 (Relation Extraction), the text states that cross-sentence relation
extraction has achieved gains on "DocRED and its financial adaptations" and cites
`\cite{chen2021finqa}`. The chen2021finqa paper is the FinQA numerical reasoning paper;
it is not a DocRED financial adaptation. This is a factual bibliographic error. The
author should either cite an appropriate DocRED financial adaptation paper or remove the
phrase "and its financial adaptations."

**Minor technical note:**

The claim that "LLMs are unreliable calculators" in the Arithmetic Reliability remark is
correct and the ReAct code-interpreter recommendation is sound, but the remark would
benefit from a quantitative estimate of the error rate (e.g., citing a benchmark) to
substantiate the claim rather than leaving it as an assertion.

---

## 3. Exposition Quality

**Rating: Good — Minor Revision Needed**

The chapter's exposition is generally strong:

- The opening section effectively motivates the information extraction problem with
  concrete institutional examples (portfolio manager reading 10-Ks, compliance officer
  scanning contracts).
- The taxonomy of structured/semi-structured/unstructured text (Definition 1) is precise
  and practically useful.
- The learning objectives at the top of the chapter are specific and measurable, which
  is commendable.
- The Further Reading section is well-curated and provides clear entry points for deeper
  study.

**Issues requiring revision:**

1. **Exercises are absent.** A textbook chapter without exercises is incomplete for
   a student audience. At minimum, the chapter should include three to five exercises
   spanning different difficulty levels: one definitional/conceptual exercise, one
   implementation exercise (e.g., fine-tune a NER model on FINER-139), and one
   research/analysis exercise (e.g., compare ROUGE vs. BERTScore on ECTSum).

2. **No companion code reference.** The chapter describes detailed implementation
   pipelines (NER fine-tuning, table extraction, consistency checking) but does not
   point readers to runnable code. This is a significant gap for the book's intended
   engineering audience.

3. **`\paragraph*{}` usage violates prose style conventions.** Section 1.2 uses
   `\paragraph*{}` labels (Organisation entities, Temporal expressions, Monetary
   figures, Legal and contractual entities) as inline headings. This substitutes
   structural labels for narrative transitions and weakens the prose. The content
   should be integrated into flowing paragraphs.

4. **Spelling inconsistency.** The chapter alternates between "summarization" (US,
   used in headings and definitions) and "summarisation" (UK, used in running prose).
   One convention should be adopted consistently throughout.

5. **Paragraph break needed in Section 5.1.** The transition from the WangWang2025
   citation to the bolded "Factual consistency metrics are designed to catch these
   errors" is abrupt and visually confusing. A new paragraph should begin at this point.

---

## 4. Exercise Quality

**Rating: N/A — No Exercises Present**

The chapter contains no end-of-chapter exercises, which is a gap relative to the
book's conventions and the pedagogical needs of the target audience. See the
exposition quality section for recommendations.

---

## 5. Specific Comments

| Location | Issue | Severity |
|---|---|---|
| Sec. 2.4, ~line 368 | `\cite{chen2021finqa}` cited for DocRED financial adaptations — incorrect | Major |
| Sec. 1.2, ~lines 106–134 | `\paragraph*{}` inline labels — violates style convention | Minor |
| Ex. 2, ~line 322 | Fine-tuning performance "substantially exceeds" — no quantification | Minor |
| Ex. 3, ~line 485 | "40% reduction in number errors" — no citation or attribution | Minor |
| Sec. 4.3, ~line 767 | No paragraph break before "Factual consistency metrics" | Minor |
| Sec. 2.1, ~lines 230–239 | FinNER and FinRE lack bibliographic citations | Minor |
| Further Reading, ~line 941 | "Chapter~13" hard-coded — should use `\ref{}` | Minor |
| Throughout | "summarization" / "summarisation" inconsistency | Minor |
| End of chapter | No exercises section | Major |
| End of chapter | No companion code notebook reference | Major |

---

## 6. Verdict: MINOR_REVISION

The chapter is well-written and technically sound on the whole. The core content—NER
fine-tuning, summarization pipelines, XBRL extraction, evaluation methodology—is
accurate and well-referenced. The required revisions are straightforward: correct the
DocRED citation error, add exercises, add a companion code notebook reference, fix the
`\paragraph*{}` labels, standardize spelling, and address the minor prose issues. None
of these require substantive rewriting of the technical content. The chapter should be
accepted after these revisions are verified.
