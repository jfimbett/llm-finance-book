# Editor Plan — Ch 08 Domain-Specific Financial LLMs (reading index 5)

Audit only — no edits applied. Smallest targeted changes to reach ≥90 on every dimension.

## MUST_FIX (blocks pass)

1. **Verify or hedge BloombergGPT corpus numbers.** chapter.tex:285–298. Confirm 50B
   params / ~708B tokens / 363B+345B split against `wu2023bloomberggpt`; if confirmed, add a
   page/section anchor in the bib note. If not confirmable, soften to "approximately."
   (citation_accuracy)

2. **Replace the stub notebook with a real demo.** code/notebooks/08-domain-specific-llms/
   demo.ipynb currently prints a string only. Add at least one runnable cell that exercises a
   chapter concept (e.g. load FinBERT via HF `transformers`, classify the
   `ex:ch08-finbert-earnings` excerpt, OR compute `eq:ch08-effective-cost` over a grid and
   plot it into figures/). This is the single biggest lever for reproducibility +
   code_figure_correctness. (reproducibility, code_figure_correctness)

3. **Verify the headline benchmark numerics** at 226–228 (FinBERT +15 F1, 1.8B words),
   630–639 (0.88/0.72/0.80 F1s), 561–572 (FinQA 8,281 / 68–72% / 55–60%), 586–601
   (FinBen 36/24/5), 651–664 (RahimikiaDrinkall 50×). Where unverifiable, tag inline as
   "as reported by [cite]" rather than stating as ground truth. (citation_accuracy)

4. **Resolve `shah2022flue` stub.** Remove the `note = {Needs verification before final
   release}`, replace `and others` with the full author list, and add pages/venue — or
   downgrade the FLUE claims (574–584) to clearly attributed reported results. (citation_hygiene)

## SHOULD_FIX

5. **Complete the taxonomy definition.** Fold the encoder–decoder/T5 family into
   `def:ch08-taxonomy` (170–184) so §ch08-encoder-decoder (187–208) no longer opens by
   admitting the taxonomy omitted it. (concept_ordering, concept_separation)

6. **Label illustrative cost figures.** Add one clause to `ex:ch08-deployment` (808–828)
   noting the dollar/throughput/accuracy numbers are illustrative, not benchmarked.
   (finance_examples)

7. **Clarify execution-accuracy metric.** In `def:ch08-execution-accuracy` (603–617) note
   that FinQA's standard metric is exact program-execution match; the $\epsilon$-band is a
   generalisation. (correctness)

## OPTIONAL

8. Fix `liu2018` key→`liu2019` (or set year/key consistent) in the shared bib. (citation_hygiene)
9. Add an explicit one-line forward-pointer caveat where RAG (`ch:llm-agents`, line 359)
   and the EU AI Act (`ch:applications-future`, 689/903) are referenced, noting these are
   developed later. (notation_crossref)
10. Populate figures/ with a regenerated cost-curve or benchmark bar chart sourced from the
    rebuilt notebook. (reproducibility)

## DO_NOT_CHANGE (protect)

- `def:ch08-register` + §ch08-financial-language (50–105) — canonical motivation; single
  source of truth.
- DAPT formalisation `def:ch08-dapt` + eq:ch08-dapt (386–449) — correct and clean.
- Two-FinBERT disambiguation (220–241) — resolves a real literature ambiguity.
- `ex:ch08-corpus-composition` (489–518) and the encoder/decoder heuristic remark (348–361).
- Contamination + hallucination remarks (671–693).

## BOOK_WIDE_ITEMS

- **BW1 — Working-paper / arXiv-stub verification debt.** `wu2023bloomberggpt`,
  `araci2019finbert`, `chen2021finqa`, `xie2024finben`, `shah2022flue` are arXiv/EMNLP stubs;
  `Keshri2025`, `RahimikiaDrinkall2024`, `Yang2023`, `Hirano2024a/b`, `Zhang2023`, `Liu2024`,
  `CookKazinnik2023` are SSRN `@unpublished`. Needs a book-level verification pass; affects
  every chapter citing these. (citation_accuracy, citation_hygiene)
- **BW2 — `shah2022flue` stub note + incomplete authors** lives in shared bib; resolve once.
- **BW3 — `liu2018` key/year (2019) mismatch** in shared bib; normalise once.
- **BW4 — Stub paired notebooks** (demo.ipynb pattern) likely repeats across chapters;
  needs a book-wide reproducibility sweep.
