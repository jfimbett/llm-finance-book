# Editor Plan — Ch. 13 (read #14) LLM Limitations and Rigorous Evaluation

Audit only. This plan lists targeted edits for a later `/iterate-book-quality` pass.
Line refs into `book/chapters/13-llm-limitations-evaluation/chapter.tex` unless noted.

## MUST_FIX (blocks pass)

1. **[citation_hygiene · book-wide] Remove duplicate `wei2022emergent`.**
   `book/bibliography.bib:1727` and `:3175` both define `@article{wei2022emergent,...}`.
   Delete one (keep the one carrying `note = {arXiv:2206.07682}`). This is a book-build
   blocker, not local to ch13, but ch13 holds the eval/limitations bib block in the audit
   plan. → BOOK_WIDE.

2. **[concept_ordering + non_repetition · book-wide] Reconcile the calibration SSOT.**
   ch06 (read #10) already owns `def:calibration` (06-credit-risk/chapter.tex:381) plus
   reliability diagrams, Platt, isotonic, ECE, Brier. Decide ONE owner:
   - Option A (recommended): make THIS chapter the SSOT (it has the fuller treatment:
     ECE/MCE eqs, RLHF mechanism, conformal). Then in ch06 replace the re-derivation with
     `\Cref{sec:ch13-calibration-overconfidence}` and a one-line pointer; keep ch06's
     credit-specific usage.
   - Option B: keep ch06 as SSOT (it is read first) and have ch13 open the calibration
     section by `\Cref{def:calibration}` then add only the LLM-specific overconfidence
     mechanism + conformal, deleting `def:ch13-perfect-calibration`.
   Either way: add the missing cross-reference (currently neither chapter cites the other)
   and remove one of the two near-identical definitions. → BOOK_WIDE.

3. **[citation_accuracy] Fix Fama-French factor citation, line 636.**
   "Fama-French market, size, and value factors" is mis-attributed to
   `\cite{fama1970efficient}` (the 1970 EMH paper). Replace with a Fama & French (1993)
   three-factor key. The bib appears to lack one → add `famafrench1993` (or correct
   existing) and cite it. → `NEEDS_EXTERNAL_VERIFICATION` for exact bib fields.

## SHOULD_FIX

4. **[correctness] ECE display typo, line 118.** `0.012 \cdot 0.03` → `0.12 \cdot 0.03`.
   Final answer (0.115) is unaffected; fix the intermediate factor.

5. **[notation_crossref] Almgren-Chriss dangling `P`, lines 711–714.** Either remove
   "$P$ the price" from the variable gloss or rewrite temporary impact in price units so
   $P$ is actually used.

6. **[citation_hygiene] Clear the `% [CHECK]` on `zhang2024financebench`.** Verify author
   list / title against arXiv:2311.11944 and drop the inline `[CHECK]` comment once
   confirmed. → `NEEDS_EXTERNAL_VERIFICATION`.

7. **[citation_hygiene] Fix `ziemke2024temporal`.** Replace `author = {Ziemke, Matthias
   and others}` with the verified author list, and reconcile `year = {2024}` with the
   arXiv id 2510.05533 (Oct 2025). Primary ref for the temporal-leakage section.
   → `NEEDS_EXTERNAL_VERIFICATION`.

## OPTIONAL

8. **[reproducibility] Flesh out or de-scope `demo.ipynb`.** `code/notebooks/13-.../
   demo.ipynb` is a 2-cell stub (imports + a print). A runnable ECE/reliability-diagram
   demo (matching `ex:ch13-ece-credit`) plus a contamination-audit n-gram demo would make
   the chapter reproducible. `exercises.ipynb` (11 KB) exists and was not deeply audited.
   The chapter does not depend on either, so this does not block.

9. **[pedagogy] NIT** — consider moving the LoRA parenthetical out of the `definition`
   body at line 674 into a `remark`.

## DO_NOT_CHANGE (protect)

- Temporal-leakage taxonomy + `def:ch13-temporal-split` + `ex:ch13-contamination-audit`
  (lines 244–412). SSOT, verified arithmetic, correct citations.
- Hallucination taxonomy + grounding strategies (lines 742–877).
- EMH / Grossman-Stiglitz information-barrier framing (lines 429–472).
- Economic-value metrics block: Sharpe/IR/fundamental-law/factor-alpha equations and the
  trading-grade checklist (lines 578–739) — EXCEPT the line-636 citation fix and the
  line-711 notation tweak above.
- Learning objectives, Summary, Further Reading.

## BOOK_WIDE_ITEMS

- **B1.** Duplicate bib key `wei2022emergent` (bibliography.bib:1727 & :3175) — build
  blocker. (= MUST_FIX 1)
- **B2.** Calibration SSOT conflict: `def:calibration` (ch06, read #10) vs
  `def:ch13-perfect-calibration` (ch13, read #14) + duplicated Platt/isotonic/ECE; pick
  one owner and cross-reference. (= MUST_FIX 2)
- **B3.** Forward-use of calibration & Sharpe ratio before ch13's "foundational"
  definitions: ch06 uses calibration/AUROC/ECE (read #10), ch10 uses Sharpe ratio
  extensively (read #11), both before ch13 defines them (read #14). Add cross-references
  so the reading-order dependency is explicit (relates to B2).
