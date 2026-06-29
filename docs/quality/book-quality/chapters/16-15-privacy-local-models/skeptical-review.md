# Skeptical Review — Ch16 (reading order) / `15-privacy-local-models`

Audit only — no edits. Date: 2026-06-20. Format: `SEVERITY · dimension_key · file:line — issue`.
File = `book/chapters/15-privacy-local-models/chapter.tex` unless noted.

## LOCAL issues

- MAJOR · citation_accuracy · chapter.tex:136 — `\citep{touvron2023llama}` is attached to a
  paragraph whose claims are about **Llama 2** ("Llama 2, released in mid-2023 … 7B to 70B …
  Llama 3 and Llama 3.1"). The key `touvron2023llama` resolves to *"LLaMA: Open and Efficient
  Foundation Language Models"* (Touvron et al., Feb 2023) — the original LLaMA (v1) paper,
  which does NOT cover Llama 2, Llama 3, the 70B instruction-tuned variants, or 4-bit VRAM
  figures. Wrong paper for the proposition. Needs the Llama 2 paper (Touvron et al. 2023b,
  "Llama 2: Open Foundation and Fine-Tuned Chat Models") or a hedge of the claim.

- MINOR · correctness · chapter.tex:143 — License remark: the "Meta Llama" naming requirement
  is from the **Llama 3** Community License, not the Llama 2 Community License; the 700M-MAU
  clause IS Llama 2. Conflation of two license generations in one sentence.

- MINOR · correctness · chapter.tex:169 — "The best available open-weight models as of 2025 are
  competitive with GPT-3.5-class performance … but lag behind GPT-4." This was defensible at
  drafting time but is a fast-moving, time-stamped claim (Llama 3.1 405B, Qwen2.5, DeepSeek
  already matched/exceeded GPT-4-class on several benchmarks by 2025). Time-bound; risks
  becoming false. Recommend softening or dating explicitly. NEEDS_EXTERNAL_VERIFICATION.

- MINOR · correctness · chapter.tex:304 — `thm:gaussian-mechanism` states the guarantee "for any
  ε ∈ (0,1)". The classical Dwork–Roth Gaussian-mechanism bound σ=Δ₂f·√(2 ln(1.25/δ))/ε indeed
  requires ε<1; this is stated correctly. NIT-level: the (0,1) restriction is a property of this
  particular analytic bound, not of the Gaussian mechanism in general (analytic Gaussian
  mechanism removes it) — a one-clause caveat would prevent overclaiming. Borderline NIT/MINOR.

- MINOR · completeness · chapter.tex:61 — Right to erasure (Art 17) is correctly flagged as
  colliding with the open problem of machine unlearning, but "machine unlearning" is named
  without a citation and never elaborated; a reader cannot act on it. Add one reference.

- MINOR · finance_examples · code/notebooks/15-privacy-local-models/demo.ipynb — The demo
  notebook is effectively a STUB: a single markdown cell listing four intended demonstrations
  and a prerequisites line, with ZERO code cells. The chapter's reproducibility story (spaCy
  NER masking, local Llama/Mistral, DP wrapper, privacy-aware RAG) is asserted in the demo's
  TOC but not implemented. (The sibling `exercises.ipynb` IS real and substantial.)

- MINOR · pedagogy · chapter.tex:4–24 — Learning Objectives are placed inside a `\begin{remark}`
  box. Per RUBRIC §5 the available boxes are correct, but objectives that promise the reader will
  "Select and deploy an open-weight model … for a given hardware budget" (obj. 4) and "Design a
  text anonymisation pipeline" (obj. 5) are only partially deliverable from the chapter alone
  given the empty demo notebook (see above). Objective/delivery gap.

- NIT · notation_crossref · chapter.tex:440 — Table row introduces "SR 11-7 (US) / ECB
  expectations" with no `\cite` and no `\Cref` to where SR 11-7 is defined (ch06/ch11). First
  use in THIS chapter is undefined-in-place.

- NIT · concept_separation · chapter.tex:315 — "moments accountant" is defined inline
  parenthetically AND again inline in the proof sketch (line 332 defines Rényi divergence
  inline). Two inline definitions of accountant machinery in close proximity; could be a single
  `deepdive`. Minor.

## BOOK-WIDE issues

- MAJOR · non_repetition · cross-chapter — GDPR is covered in BOTH ch11
  (`11-regtech-compliance-aml/chapter.tex:93` `\subsection{GDPR and data privacy constraints}`,
  Articles 5/17/22, `ex:gdpr-article22`) AND ch15 (chapter.tex:54–71, Articles 22/17/83). Ch11 is
  reading #12 (earlier); ch15 is #16. Neither chapter cross-references the other on GDPR. Two
  parallel treatments of Articles 17 and 22 with no designated single source of truth. Decide the
  SSOT (recommend ch11 for general GDPR; ch15 keeps only the privacy-specific Art 17↔unlearning /
  Art 22↔DP linkage) and add `\Cref`.

- MINOR · non_repetition · cross-chapter — Open-weight models + quantisation overlap Appendix C
  (`C-huggingface-local/chapter.tex`): Llama/Mistral/Phi, GGUF/4-bit, llama.cpp/Ollama, VRAM
  budgets, QLoRA. Ch15 sec:ch15-open-weight (131–144) and sec:ch15-quantisation (166–177) are
  conceptual; Appendix C is the hands-on SSOT. Acceptable as complementary, BUT neither cross-
  references the other. Add a `\Cref{...}` pointer from ch15 to Appendix C.

- MINOR · non_repetition · cross-chapter — MiFID II record-keeping (ch15:65) overlaps ch11 MiFID II
  treatment (`11-...:75–80`, `sec:ch11-mifid-basel`). Same SSOT concern as GDPR.

## Things checked and found CLEAN

- citation_hygiene: all 16 `\cite` keys resolve to exactly one entry in `book/bibliography.bib`
  (abadi2016deep, carlini2021extracting, carlini2022quantifying, dora2022, dwork2014algorithmic,
  esma2018mifid2, frantar2022gptq, gdpr2016, honnibal2017spacy, jiang2023mistral, lin2023awq,
  mcmahan2017communication, perez2022ignore, shokri2017membership, sweeney2002k, touvron2023llama).
  No dupes, no stubs. (Note: the touvron key is clean but mis-applied — that is a citation_accuracy,
  not citation_hygiene, issue.)
- notation_crossref: every internal `\ref`/`\eqref` (ex:ch15-ner, sec:ch15-reidentification,
  prop:composition, tab:ch15-compliance, sec:ch15-*) resolves to a `\label` defined in-file or to
  `ch:llm-training-finetuning` / `ch:llm-agents` (both defined). No hard-coded "Chapter N" prose
  numbers — uses `Chapter~\ref{...}`. No label collisions.
- correctness (math): Gaussian-mechanism σ (eq:ch15-gaussian) and advanced-composition ε'
  (eq:ch15-advanced-comp) match Dwork–Roth. FedAvg objective/update (eqs) match McMahan et al.
  Mistral 7B > Llama 2 13B on most benchmarks (138) matches the Mistral paper.
