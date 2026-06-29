# Constructive Review — Ch 14 Financial Text Summarization (reading index 8)

Date: 2026-06-20 · Scope: chapter · Audit only (no edits)

## Overview
A strong, finance-first treatment of information extraction (NER, relation extraction),
document summarization (extractive/abstractive, 10-K, analyst notes, long documents),
table/numerical extraction (XBRL, FinQA, consistency checking), and evaluation (ROUGE,
BERTScore, factual consistency, human eval, dataset inventory). Well-positioned at index 8:
NER/transformer/token/RAG/sentiment prerequisites are all defined upstream.

## Preserve (tagged)

- **KEEP_AS_SINGLE_SOURCE_OF_TRUTH** — `chapter.tex:81-88` Definition of Structured/
  Semi/Unstructured Financial Text. Clean, reusable taxonomy; book's natural SSOT for this.
- **KEEP_AS_SINGLE_SOURCE_OF_TRUTH** — `chapter.tex:167-183` Definitions of Information
  Extraction vs Text Summarization (schema-driven vs content-driven). Precise, prevents
  the common conflation; should be the canonical reference for later chapters.
- **KEEP_AS_SINGLE_SOURCE_OF_TRUTH** — `chapter.tex:391-408` Extractive vs Abstractive
  definitions, with the faithfulness-by-construction insight. SSOT for summarization paradigms.
- **GOOD_FINANCE_EXAMPLE** — `chapter.tex:136-156` Entities-in-an-earnings-call example
  (Microsoft Q3 2023). Realistic, typed output schema, footnoted as illustrative. Reader
  can act on it. (Numbers explicitly flagged as illustrative — good hygiene.)
- **GOOD_FINANCE_EXAMPLE** — `chapter.tex:464-490` Earnings-report summarization with a
  constrained GPT-4 prompt; the "quote all numbers exactly as stated" technique is concrete
  and the % improvement is explicitly framed as illustrative ("suppose…", "would vary").
- **GOOD_TECHNICAL_EXPLANATION** — `chapter.tex:663-671` Remark "Arithmetic Reliability":
  route arithmetic to a code interpreter (ReAct). Correct, finance-relevant, well-motivated.
- **GOOD_TECHNICAL_EXPLANATION** — `chapter.tex:685-699` three-step consistency-checking
  pipeline (multi-source extract → normalise → cross-reference). Practical quality gate.
- **GOOD_TECHNICAL_EXPLANATION** — `chapter.tex:740-744` ROUGE limitation worked example
  ("net income declined 12%" vs "profit fell 12%"). Crisp motivation for BERTScore.
- **GOOD_BIG_PICTURE_EXPLANATION** — `chapter.tex:185-197` why IE serves databases and
  summarization serves readers; mapped to quant/IC/compliance personas. Excellent framing.
- **KEEP** — `chapter.tex:204` inline token definition with cross-ref to ch:llm-foundations;
  good just-in-time bridge.
- **KEEP** — `chapter.tex:249-259` Remark on annotation challenges (context-dependent type,
  nested entities, implicit "the issuer"). Domain-grounded and correct.
- **KEEP** — `chapter.tex:859-870` Remark on dataset selection (no single benchmark covers
  all tasks; build a private held-out test set). Sound, practitioner-useful caveat.
- **KEEP** — `chapter.tex:938-944` forward/back bridges to ch:business-valuation (XBRL/table
  parsing as DCF prerequisites) and to hallucination mitigation. Strong progressive-learning glue.
- **GOOD_FINANCE_EXAMPLE** — exercises notebook `exercises.ipynb` (cells c14d0002–c14d0008):
  real SEC EDGAR pipeline (CIK lookup, 10-K fetch, MD&A/Risk extraction, TF-IDF extractive
  summary, revenue regex) with [B]/[I]/[A] tags. Genuinely runnable against live EDGAR.

## What would most raise quality (constructive)
1. Add explicit `context`/`deepdive` separation around the math-heavy NER/RE/ROUGE/BERTScore
   passages so the big-picture reader can skip internals (currently all prose).
2. Resolve the FINER-139 attribution (see skeptical review) — likely Loukas et al. 2022, not
   Shah et al. 2023.
3. Clear the two `Needs verification before final release` bib notes (frattaroli2019,
   mukherjee2022ectsum) before release.
