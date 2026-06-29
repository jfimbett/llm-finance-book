# Editor Plan — Ch16 (reading order) / `15-privacy-local-models`

Audit only — no edits applied. Date: 2026-06-20.
Smallest targeted changes to bring every dimension to ≥90.

## MUST_FIX (blocks a dimension below 90)

1. **citation_accuracy — fix the Llama 2 citation (chapter.tex:136).**
   `\citep{touvron2023llama}` (original LLaMA v1, "Open and Efficient Foundation
   Language Models") is mis-applied to a paragraph about Llama 2 / 3 / 3.1. Either
   add a `llama2_2023`-style bib entry ("Llama 2: Open Foundation and Fine-Tuned Chat
   Models", Touvron et al. 2023b) and cite it for the Llama 2 sentence, or restrict
   the existing cite to the LLaMA-v1 lineage claim and hedge the Llama 2/3 specifics.
   Until corrected, citation_accuracy is capped (mis-attribution = below 90).

2. **non_repetition (BOOK_WIDE) — designate a GDPR single source of truth.**
   GDPR Articles 17/22 are developed independently in ch11 (`sec:ch11-gdpr-privacy`)
   and ch15 (sec:ch15-regulation). Pick ch11 as the general GDPR SSOT; trim ch15's
   regulatory subsection to the privacy-specific angles (Art 17 ↔ machine unlearning,
   Art 22 ↔ DP, Art 83 fines) and insert `\Cref{sec:ch11-gdpr-privacy}` (and the
   reverse pointer in ch11). Same treatment for MiFID II overlap.

## SHOULD_FIX (raises a dimension comfortably above floor / removes risk)

3. **reproducibility — implement or honestly relabel `demo.ipynb`.**
   The demo notebook is a stub (1 markdown cell, 0 code). Either implement the four
   advertised demos (spaCy NER masking, local Llama/Mistral inference, DP gradient
   wrapper, privacy-aware RAG with audit log) or change the chapter's reproducibility
   claim so it does not promise runnable demos that do not exist. (exercises.ipynb is
   fine and can stay.)

4. **correctness — fix the Llama license conflation (chapter.tex:143).**
   Move the "Meta Llama" naming requirement to the Llama 3 license, or state both
   generations explicitly. One-clause fix.

5. **correctness — date or soften the GPT-3.5/GPT-4 capability claim (chapter.tex:169).**
   Add "as of early 2025" framing or hedge; the open-weight-vs-GPT-4 gap is closing fast.

6. **non_repetition / discoverability — cross-reference Appendix C** from
   sec:ch15-open-weight and sec:ch15-quantisation (`\Cref{...}` to the
   `C-huggingface-local` deployment appendix). One-line additions.

## OPTIONAL

7. **completeness — add a citation for "machine unlearning"** (chapter.tex:61) so the
   open-problem claim is actionable.
8. **notation_crossref — add an article cite to the MiFID II row** and a `\Cref` to the
   SR 11-7 definition (ch06/ch11) in tab:ch15-compliance (chapter.tex:438–440).
9. **correctness — one-clause caveat on the Gaussian-mechanism ε∈(0,1) restriction**
   (chapter.tex:304) noting the analytic Gaussian mechanism lifts it.

## DO_NOT_CHANGE (protected — see constructive-review.md)

- def:dp, thm:gaussian-mechanism, prop:composition + proof sketch (277–333) — SSOT for DP.
- def:fedavg and the FedAvg section (335–359) — SSOT for federated learning.
- def:memorisation, def:mia-advantage and the attack taxonomy (41–112).
- AWQ/GPTQ deepdive (173–177).
- ex:ch15-routing, ex:ch15-ner, ex:ch15-rag — all three worked finance examples.
- Opening context anecdote (30–36) and the CIA-triad context (77–79).
- Financial-identifier NER taxonomy (196–204) and rem:ch15-summary (448–459).

## BOOK_WIDE_ITEMS

- **B1 (MAJOR, non_repetition):** GDPR Articles 17/22 duplicated across ch11
  (`sec:ch11-gdpr-privacy`, reading #12) and ch15 (sec:ch15-regulation, #16); no
  cross-reference either way. Designate ch11 as GDPR SSOT; ch15 keeps only
  privacy-specific linkage and `\Cref`s ch11.
- **B2 (MINOR, non_repetition):** MiFID II record-keeping duplicated across ch11
  (`sec:ch11-mifid-basel`) and ch15:65. Same SSOT/cross-ref fix.
- **B3 (MINOR, non_repetition):** Open-weight models + quantisation (Llama/Mistral/Phi,
  GGUF, llama.cpp/Ollama, VRAM, QLoRA) overlap Appendix C (`C-huggingface-local`).
  Complementary (conceptual vs hands-on) but uncross-referenced; add `\Cref` from ch15
  to Appendix C. Appendix C is the hands-on SSOT.
- **B4 (MINOR, citation_accuracy/book-wide):** Verify the Llama 2 paper has a bib entry
  book-wide; if other chapters also cite `touvron2023llama` for Llama 2/3 claims, fix
  globally.
