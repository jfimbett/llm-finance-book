# Editor Plan — Ch 04 LLM Agents and Finance Applications

Reading index 6 · slug `04-llm-agents` · audit date 2026-06-20 · iteration 0.
Audit only — no edits applied. Items ordered by blocking severity. Cite file:line.

## MUST_FIX (block pass; ≥90 unreachable until resolved)

1. **Provide a real `demo.ipynb` OR redirect the prose.** `code/notebooks/04-llm-agents/demo.ipynb`
   is a 0-code-cell placeholder, but chapter.tex:419, :732, :1123 each promise "the complete
   Python implementation … is available in demo.ipynb". Either populate `demo.ipynb` with the
   tool-registration, two-agent extractor/classifier, and report-generation code that the prose
   describes, or repoint those three sentences to `exercises.ipynb` (which is real). Smallest
   correct fix raises `reproducibility` and `code_figure_correctness`. (dim 13, 3)

2. **Resolve the `def:rag` duplicate label.** Defined at chapter.tex:763 AND
   `02-llm-foundations/chapter.tex:1972`. Relabel ch04's to e.g. `def:rag-marginal`, then add a
   one-line `\Cref` bridge to the ch02 pipeline definition so the layering is intentional rather
   than colliding. (dim 12, 6)

3. **Fix `zhang2024financebench` bib entry.** Remove the `% [CHECK] verify author list` stub and
   correct the author roster (currently "Islam, Shariful and Zhu, Meng …" — does not match
   FinanceBench arXiv 2311.11944 / Pranab Islam et al.). NEEDS_EXTERNAL_VERIFICATION for exact
   authors. (dim 9, 10)

## SHOULD_FIX (each lowers a dimension below 90)

4. **Verify `esma2018mifid2` is the right source for Article 16 record-keeping** (cited
   chapter.tex:1380). Current entry is the MiFID II *Suitability* guideline, not the
   record-keeping obligation. Swap to the correct ESMA/MiFID II reference or rephrase the claim.
   NEEDS_EXTERNAL_VERIFICATION. (dim 10)

5. **Reconcile `kurshan2024agenticregulator` year vs arXiv ID** (`2024` vs `2512.11933` → Dec
   2025) in bibliography.bib; verify the cited claims at chapter.tex:1478–1486.
   NEEDS_EXTERNAL_VERIFICATION. (dim 9, 10)

6. **Add an end-of-chapter Summary / bridge** after chapter.tex:1505 tying the 8 learning
   objectives together and pointing to the next reading-order chapter (09-financial-nlp-sentiment).
   Use a `remark` or `context` box (no new env). (dim 14, 5)

## OPTIONAL

7. Remove the dead `\label{eq:hybrid-search}` (chapter.tex:861) or add an `\eqref` to it.
8. Remove the now-redundant `% [CHECK] venue confirmed ICLR 2023` comment on `yao2022react`.
9. Add explicit "illustrative/hypothetical" framing to `ex:portfolio-qa` (chapter.tex:1160), to
   match the disclaimer already present for the earnings example (chapter.tex:1068–1070).
10. Soften or cite the "128k tokens ≈ 100 pages" heuristic (chapter.tex:119–121).

## DO_NOT_CHANGE (protect — see constructive-review)

- PRA loop `def:pra-loop` (chapter.tex:92–109) and ReAct ownership `def:react-trajectory`
  (chapter.tex:158–168) — KEEP_AS_SINGLE_SOURCE_OF_TRUTH.
- Memory taxonomy (chapter.tex:268–283), hybrid search (chapter.tex:834–881), chunking
  (chapter.tex:913–926), RAGAS (chapter.tex:957–973), audit-trail chained hash
  (chapter.tex:1385–1399), prompt-injection/confused-deputy treatment (chapter.tex:1411–1469).
- `context`/`deepdive` section structure throughout — strong concept_separation.
- Figure `fig:ch04-illustration` and its matching notebook code (exercises.ipynb cells 1,3).
- Finance examples `ex:react-filing`, `ex:db-tools`, `ex:multi-agent-research`,
  `ex:portfolio-qa`, `rem:signal-staleness`.

## BOOK_WIDE_ITEMS

- **BW-1 (non_repetition / SSOT):** ch05 `05-business-valuation/chapter.tex:675–697` re-derives
  ReAct (Thought/Action/Observation) without `\Cref{ch:llm-agents}` at the point of
  re-derivation. ch04 is the SSOT; ch05 should cross-reference and not re-define. Owner: ch05
  editor. (This chapter is correct; logged here because it is the SSOT.)
- **BW-2 (notation_crossref / duplicate label):** `def:rag` collides across
  `02-llm-foundations:1972` and `04-llm-agents:763`. Coordinate the rename with the ch02 editor
  so exactly one definition keeps `def:rag` and the other relabels + cross-refs.
- **BW-3 (non_repetition):** RAG is formally defined in two chapters (ch02 pipeline view, ch04
  marginalization view). Decide the SSOT split (recommend: ch02 owns the pipeline/intro, ch04
  owns the latent-variable/marginalization deep dive with an explicit bridge) and enforce
  cross-refs both directions.
