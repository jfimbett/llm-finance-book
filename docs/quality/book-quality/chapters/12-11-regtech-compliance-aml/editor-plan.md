# Editor Plan — Ch. 11 RegTech, Compliance, AML (reading index 12)

**Date:** 2026-06-20 · **Scope:** chapter · **Audit only — no edits applied.**
Targeted, minimal edits. Protect all KEEP-tagged content in constructive-review.md.

## MUST_FIX (blocks pass)

1. **Resolve the dangling figure reference** (chapter.tex:172). Either
   (a) add a real `figure` environment with `\label{fig:ch11-rag-pipeline}` and a
   committed asset in `figures/` depicting the five-component RAG dataflow
   (ingestion → vector store → retriever → reader/ranker → output formatter), OR
   (b) remove the sentence "Figure~\ref{fig:ch11-rag-pipeline} describes the dataflow
   conceptually." and rely on the five `\textbf{}` component paragraphs that follow.
   Fixes the BLOCKER in notation_crossref and code_figure_correctness.
   (Recommendation: option (a) — the chapter genuinely benefits from the diagram; an
   actual figure also moves reproducibility/code_figure off N/A toward positive
   evidence.)

2. **De-risk the `chen2025aml` citation** (chapter.tex:162,197,431). Verify the arXiv
   ID `2602.23373` externally. If it cannot be confirmed (the `2602` = Feb-2026 stamp
   is anomalous), remove the attribution of the Adverse Media Index to this paper and
   present `def:adverse-media-index`/`eq:ami-score` as the book's own construction.
   Do not invent a replacement citation. Fixes citation_accuracy MAJOR.

## SHOULD_FIX

3. **GDPR / MiFID II single-source-of-truth** (book-wide). Designate ch11
   §`sec:ch11-gdpr-privacy` and §`sec:ch11-regulatory-landscape` as SSOT for the AI
   Act + GDPR-in-compliance, and have ch15 (`15-privacy-local-models`) `\Cref` back to
   them for the shared Articles 5/17/22 material (or vice-versa). Reconcile the GDPR
   bib key (`euaiact2024`+prose here vs `gdpr2016` in ch15 — add `gdpr2016` cite here
   or align). Add a one-line cross-ref in each direction. Raises non_repetition.

4. **Fix the FPR-vs-FDR labelling** (chapter.tex:135–137). Either redefine the 95–99%
   figure as the false-discovery rate / (1 − PPV) consistent with the existing
   `eq:fpr-aml`, or rephrase line 137 to "fewer than one in twenty *flagged alerts* are
   genuine matches (a precision/PPV of 1–5%)" without calling it FPR. Raises correctness.

5. **Promote `demo.ipynb` from stub to real** (code/notebooks/11-…/demo.ipynb).
   Implement at least one chapter artefact deterministically — recommended: RRF fusion
   (`eq:rrf-fusion`) and an AMI scoring toy (`eq:ami-score`) on synthetic documents,
   seeded. Raises reproducibility and gives code_figure_correctness positive evidence.

6. **Resolve `fincen2020aml` title flag** (bibliography.bib). Confirm the exact FinCEN
   report title and remove the `% [CITE: verify…]` comment, or replace with a
   verifiable FinCEN/FATF source for the 95–99% FPR and "excessive low-quality SARs"
   claims. Raises citation_hygiene.

## OPTIONAL

7. Wrap the RAG internals (chapter.tex:180–188, RRF + cross-encoder detail) in a
   `deepdive` box to sharpen big-picture/under-the-hood separation.
8. Add a one-line caveat at the top of §`sec:ch11-entity-resolution` that missing a
   true sanctions hit categorically outweighs a false-positive review cost, foreshadowing
   the near-100%-recall threshold in `def:entity-resolution`.

## DO_NOT_CHANGE (protect)

- `def:eu-ai-act-tiers`, the seven high-risk obligations, `def:model-risk-sr117`,
  `def:fp-rate-aml`, `def:adverse-media-index`/`eq:ami-score`, `eq:rrf-fusion`.
- All four worked examples: `ex:gdpr-article22`, `ex:agentic-adverse-media`,
  `ex:bo-extraction`, `ex:mrm-llm-ams`.
- The section-opening `context` boxes and the governance section argument.
- Existing resolving cross-refs to `ch:llm-agents`, `ch:credit-risk`,
  `ch:xai-explainability`, `ch:llm-foundations`.

## BOOK_WIDE_ITEMS

- **BW-1 (non_repetition):** GDPR Arts. 5/17/22 duplicated in ch11 §gdpr-privacy and
  ch15 §54–63/426–434 with no cross-ref; pick one SSOT, cross-ref the other, align the
  GDPR bib key (`euaiact2024`/prose vs `gdpr2016`).
- **BW-2 (non_repetition):** MiFID II re-introduced in both ch11 (§mifid-basel) and
  ch15 (§54). Cross-ref to a single SSOT.
- **BW-3 (citation_accuracy):** 7 SSRN `@unpublished` keys + `chen2025aml` arXiv +
  `fincen2020aml` need external verification book-wide (several reused across chapters).
