# Constructive Review — Ch16 (reading order) / `15-privacy-local-models`

Audit only — no edits. Date: 2026-06-20. Reviewer persona: constructive-reviewer.

This is a strong, mature final chapter. Despite the prompt flag that it might be
"thin" (~459 lines), it is dense and well-structured: it covers four engineering
strategies (local deployment, anonymisation, privacy-preserving training,
privacy-aware architecture) with formal definitions, two theorems/propositions
with a proof sketch, worked examples, and a compliance table. It is closer to a
mid-length, high-rigor chapter than a stub. Below is what to PRESERVE.

## KEEP_AS_SINGLE_SOURCE_OF_TRUTH

- **Differential privacy core (sec:ch15-dp, lines 277–333).** `def:dp` (282),
  `thm:gaussian-mechanism` (296), `prop:composition` (319) with proof sketch (331).
  This is the only place in the book that formally develops (ε,δ)-DP, the Gaussian
  mechanism, DP-SGD's three modifications, and advanced composition. Designate this
  the book's SSOT for differential privacy and have other chapters `\Cref` it.
- **Federated learning / FedAvg (sec:ch15-federated, lines 335–359).** `def:fedavg`
  (342) with the FedAvg objective and server update. SSOT for FL in the book.
- **Memorisation / extraction / inference attacks (lines 41–112).** `def:memorisation`
  (49), `def:mia-advantage` (99). SSOT for the threat model.

## GOOD_TECHNICAL_EXPLANATION

- **Two-channel framing (training vs inference channel), lines 41–47.** Clean,
  correct mental model that organises the whole chapter. KEEP.
- **AWQ vs GPTQ deepdive (lines 173–177).** Accurate: AWQ's ~1% salient-weight
  insight via activation statistics and per-channel scaling; GPTQ's second-order /
  Hessian block reconstruction; the speed contrast. A genuinely good `deepdive` box.
- **DP-SGD three modifications (lines 309–313).** Per-example gradients, clipping to
  norm C, Gaussian noise N(0,σ²C²I). Correct and precise.
- **Proof sketch for composition (lines 331–333),** including post-processing
  immunity and the Rényi-DP inline definition. Re-derivable; KEEP.

## GOOD_BIG_PICTURE_EXPLANATION

- **Opening `context` (lines 30–36).** The Jan-2023 bank-policy + Samsung anecdote is
  vivid, finance-first, and correctly motivates the chapter. KEEP.
- **CIA-triad `context` (lines 77–79)** and the local-deployment `context` (127–129).
  Good big-picture scaffolding; correct use of `context` vs `deepdive` boxes.

## GOOD_FINANCE_EXAMPLE

- **Routing architecture for a commercial bank (ex:ch15-routing, lines 155–164).**
  Three-tier public/internal/client routing with audit logging. Concrete, actionable,
  finance-grounded. KEEP.
- **Financial NER pipeline (ex:ch15-ner, lines 206–225).** Antoine Dupont / NIF / IBAN
  / Champs-Élysées example with a typed-placeholder output table. Excellent, concrete,
  reader-runnable. KEEP.
- **Privacy-aware RAG for credit analysis (ex:ch15-rag, lines 374–385).** Five-step LBO
  query pipeline with local embedding, ACL-filtered retrieval, PII scan, audit log. KEEP.
- **Financial identifier taxonomy (lines 196–204):** IBAN/SWIFT/ISIN/CUSIP/LEI as NER
  entity types is a finance-specific contribution missing from generic NER treatments. KEEP.

## KEEP_BUT_CLARIFY

- **Llama license remark (lines 142–144).** The 700M-MAU clause and the "Meta Llama"
  naming requirement are attributed to the *Llama 2 Community License*; the naming
  requirement actually originates in the *Llama 3* license. Worth a one-word fix.
- **Compliance table (tab:ch15-compliance, lines 418–444).** Strong artefact; KEEP, but
  the MiFID II row cites no article and SR 11-7 appears here without being defined in
  this chapter (it is defined in ch11/ch06). Add an article cite / cross-ref.

## KEEP_BUT_MOVE / cross-reference

- **GDPR/CCPA/MiFID/DORA regulatory section (sec:ch15-regulation, 54–71).** Good content,
  but ch11 (regtech, reading #12, earlier) already has a dedicated GDPR subsection
  (`sec:ch11-gdpr-privacy`) covering Articles 5/17/22. KEEP the privacy-specific framing
  here (Art 17 ↔ machine unlearning, Art 22 ↔ DP) but cross-reference ch11 as the
  general regulatory SSOT to avoid re-derivation. See BOOK_WIDE_ITEMS.
