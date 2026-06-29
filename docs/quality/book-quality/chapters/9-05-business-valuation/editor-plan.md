# Editor Plan — 9 05-business-valuation

> Synthesized by `audit-editor` from the chapter's constructive/skeptical reviews and
> the finance / concept-ordering / citation / code-figure auditors.
> **Dry-run: no edits applied.** Apply with `/iterate-book-quality 05`.

## Dimensions below 90 (targets)

| Dimension | Score | Addressed by |
|-----------|-------|--------------|
| completeness | 70 | T1 |
| finance_examples | 72 | T1 |
| finance_orientation | 86 | T1 |
| concept_ordering | 72 | T1, T2 |
| non_repetition | 58 | T3 |
| notation_crossref | 65 | T3 |
| citation_accuracy | 78 | T4, T5 |
| citation_hygiene | 88 | T5 |
| reproducibility | 62 | T6 + backlog |
| progressive_learning | 88 | T1, T2 |
| code_figure_correctness | 86 | T6 |

## MUST_FIX (before re-scoring)

### T1 — Integrate the orphaned valuation exercise + supply the WACC/CAPM derivation
[dimensions: completeness, finance_examples, finance_orientation, concept_ordering, progressive_learning] [scope: local, high-leverage]
Location: end of `subsec:bv-pipeline-casestudy` (after line 1091); plus a short WACC `definition`/`context` box near `eq:dcf` (84–105).
Problem: WACC drives every DCF but is never derived (no CAPM/r_E/r_D); the flagship case study is a synthetic composite SaaS firm while a complete, passing real AAPL DCF+comps Claude exercise sits orphaned at `exercises/valuation_example/` (never linked).
Fix (minimal — do NOT paste the exercise into prose): add one `remark` "Companion Exercise" box pointing to `exercises/valuation_example/`, and inside it state the CAPM cost of equity and resulting WACC for AAPL as supplied by the exercise — e.g. `r_E = r_f + \beta\,\mathrm{ERP}` with the exercise's numbers — plus a one-line reader exercise ("re-derive WACC and re-run the two-stage DCF; reproduce the error vs the $226.84 reference"). Add a brief WACC box deriving the weights and pointing `r_E` to CAPM.
Preserve (constructive KEEP): the FCFF/FCFE SSOT (320–368), the DCF/Gordon-Growth statement (81–105), the SaaS case study itself (keep, add the box after it), the AAPL heatmap (825–856), the error-propagation derivation (1146–1183). Use the exercise's documented numbers; do not invent figures.
Verification note: the finance-auditor and code-figure-auditor reported slightly different exercise outputs ($214.37 / $225.00 / $221.04 across `results/`); confirm the current committed `results/` values before quoting — treat any uncertainty as `NEEDS_EXTERNAL_VERIFICATION` rather than guessing.

### T2 — Reference CAPM at first use of r_E
[dimension: concept_ordering] [scope: local + cross-chapter]
Location: WACC box (T1) / `chapter.tex:85`
Problem: CAPM is never properly defined before reading index 9; only a stray inline form exists at read#7 (`ch09:411`).
Fix: When introducing `r_E`, `\Cref` the CAPM statement (or introduce CAPM in the WACC box). Decide the CAPM single source of truth book-wide (backlog cross-link).

### T3 — Remove the cosine-similarity redefinition (fixes repetition + label collision)
[dimensions: non_repetition, notation_crossref] [scope: book-wide root cause, local edit]
Location: `chapter.tex:921–926` (`definition` env + `eq:cosine-sim`); also `chapter.tex:678` (ReAct re-intro)
Problem: Cosine similarity is fully redefined a 4th time and reuses the colliding label `eq:cosine-sim` (also in ch01:868, ch02:2004); ReAct re-introduced though ch04 owns it.
Fix: Replace the cosine-similarity definition with a one-line reminder + `\Cref` to ch01 (the SSOT), deleting the colliding label. Reduce the ReAct re-introduction to a short reminder + `\Cref{ch:llm-agents}`.

### T4 — Fix frieder2023large wrong-paper citation
[dimension: citation_accuracy] [scope: citation]
Location: `chapter.tex:645`
Problem: Cites `frieder2023large` (entry title "LLMs and the ArXiv", 2302.00083) for GPT-4 arithmetic errors; the claim belongs to Frieder "Mathematical Capabilities of ChatGPT" (2301.13867).
Fix: Correct the bib entry's title/eprint to the math-capabilities paper, or add a correctly-keyed entry and cite it. Only use a key that resolves in `bibliography.bib`.

### T5 — Resolve shen2023nlp placeholder
[dimensions: citation_hygiene, citation_accuracy] [scope: citation]
Location: `chapter.tex:946` (EV/EBITDA-IQR claim) + bib entry
Problem: `shen2023nlp` is a placeholder ("Needs verification before final release") backing a substantive empirical claim.
Fix: Supply a verified source or soften/remove the numeric claim. Mark `NEEDS_EXTERNAL_VERIFICATION` until sourced — do not assert.

## SHOULD_FIX

### T6 — Notebook/figure reproducibility (local part)
[dimensions: reproducibility, code_figure_correctness] Fill `demo.ipynb` (it is cited ~10x as authoritative but is a stub) or stop citing it as the implementation; add a one-line note reconciling the $98.8B (yfinance) vs $108.8B (EDGAR) AAPL FCF; clean the placeholder cell + mojibake in `exercises.ipynb`.

## OPTIONAL

- §8 benchmarking: add a small quantitative results table or explicitly label the evidence qualitative (NIT toward `completeness`).
- "hallucinate" → "hallucinates" (954).

## DO_NOT_CHANGE (protected — constructive KEEP)

- FCFF/FCFE definitions + proof (320–368) — `KEEP_AS_SINGLE_SOURCE_OF_TRUTH`.
- DCF EV + terminal value (81–105) — definitive DCF statement.
- SaaS case study (1043–1091) — keep; add the companion box after it, do not replace.
- AAPL sensitivity heatmap + caption (825–856) — well-hedged, accurate.
- Error-propagation Taylor derivation (1146–1183).

## Book-wide items → IMPLEMENTATION_BACKLOG.md

- Designate the CAPM single source of truth and back-reference from ch05/ch10/ch13.
- Snapshot AAPL financial data for the figure (remove live yfinance/EDGAR dependence).
- The `eq:cosine-sim` collision is one instance of a book-wide cosine-similarity SSOT decision (ch01 owns it).

## Contradiction & length check

No contradictions. T3 reduces length; T1 adds one box (justified by the `completeness` BLOCKER). Net length change small and warranted.

## Prediction

After MUST_FIX (T1–T5): completeness, finance_examples, finance_orientation, concept_ordering, non_repetition, notation_crossref, progressive_learning, citation_accuracy, citation_hygiene expected ≥90. `reproducibility` and `code_figure_correctness` partially improved by T6 but `reproducibility` likely remains <90 pending the demo.ipynb fill + data snapshot (backlog). Chapter pass = **NO until reproducibility addressed**; ~12 of 14 reachable in 1–2 iterations.
