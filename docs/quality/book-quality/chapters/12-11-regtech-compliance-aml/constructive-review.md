# Constructive Review — Ch. 11 RegTech, Compliance, AML (reading index 12)

**Date:** 2026-06-20 · **Scope:** chapter · **Audit only — no edits.**

This is a substantial, well-structured chapter (439 lines, 5 sections, multiple
definitions/examples/remarks). It is NOT a thin/placeholder chapter — the prose is
mature and finance-first. The items below are worth preserving.

## KEEP_AS_SINGLE_SOURCE_OF_TRUTH

- **`def:eu-ai-act-tiers` (lines 45–54) + the seven high-risk obligations (lines 58–67).**
  Clear, correct enumeration of the EU AI Act four-tier risk model and Annex III
  high-risk requirements. This is the natural SSOT for the AI Act in the book; ch15
  (privacy) should `\Cref` here rather than re-explain. KEEP_AS_SINGLE_SOURCE_OF_TRUTH.
- **`def:model-risk-sr117` (lines 86–89) and the SR 11-7 three-pillar framing
  (lines 84, 377–390).** Accurate paraphrase of the SR 11-7 model definition (the
  quoted definition matches the guidance) and a genuinely novel, well-reasoned
  application to LLMs. KEEP_AS_SINGLE_SOURCE_OF_TRUTH for SR 11-7 in the book.

## GOOD_FINANCE_EXAMPLE

- **`ex:gdpr-article22` — A. Petrov adverse-media false positive (lines 106–111).**
  Concrete, realistic, ties GDPR Art. 22 rights to an audit-log architectural
  requirement. Reader can act on it. GOOD_FINANCE_EXAMPLE.
- **`ex:agentic-adverse-media` — Carlos Fernandez-Gutierrez 5-step agent workflow
  (lines 151–163).** Grounded, decomposes the agent loop into concrete steps. GOOD_FINANCE_EXAMPLE.
- **`ex:bo-extraction` — Meridian Capital / Apex Global / Sunridge BVI chain
  (lines 276–281).** Excellent illustration of multi-hop beneficial-ownership
  traversal terminating in an opacity jurisdiction. GOOD_FINANCE_EXAMPLE.
- **`ex:mrm-llm-ams` — full MRM governance structure with named roles, monitoring
  thresholds, 7-year tamper-evident log (lines 392–407).** Operationally precise;
  the kind of concrete artefact practitioners want. GOOD_FINANCE_EXAMPLE.

## GOOD_TECHNICAL_EXPLANATION

- **The false-positive crisis framing (lines 123–142)** including `def:fp-rate-aml`
  with the FPR/PPV equation (`eq:fpr-aml`). Correct definitions; motivates LLMs from
  a genuine finance pain point. GOOD_TECHNICAL_EXPLANATION.
- **RAG adverse-media architecture (lines 167–192)** — five named components, hybrid
  BM25+dense retrieval, RRF (`eq:rrf-fusion`, κ=60 correct), cross-encoder rerank,
  grammar-constrained structured output. Technically sound and current. GOOD_TECHNICAL_EXPLANATION.
- **Adverse Media Index `def:adverse-media-index` + `eq:ami-score` (lines 199–220).**
  A coherent, calibratable scoring construction (relevance × credibility × recency ×
  offence-severity weights, logistic squashing). Internally consistent. KEEP.

## GOOD_BIG_PICTURE_EXPLANATION

- **Section-opening `context` boxes** (lines 32–38, 117–121, 226–230, 287–291, 336–340)
  consistently separate the bigger-picture motivation from the under-the-hood detail.
  Good `context` vs body separation. GOOD_BIG_PICTURE_EXPLANATION.
- **Governance section (lines 333–407):** the argument that "governance is as important
  as the model" is well made and finance-appropriate. KEEP.

## KEEP_BUT_CLARIFY

- **Entity resolution two-stage pipeline (lines 232–254)** is good but should
  `\Cref{sec:ch11-rag-adverse-media}` explicitly when it says the pattern "mirrors the
  retriever-ranker architecture" (line 254 already cites `gao2024retrieval` — fine).

## KEEP_BUT_MOVE / cross-ref hooks already present

- The chapter already cross-refs `ch:llm-agents` (ReAct), `ch:credit-risk` (GDPR/SR
  11-7 in credit), and `ch:xai-explainability` (lines 165, 439). These resolve and are
  good progressive-learning bridges. KEEP.
