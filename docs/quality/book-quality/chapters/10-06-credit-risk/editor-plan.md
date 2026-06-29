# Editor Plan — Ch 06 Credit Risk (reading index 10)

Audit only — no edits applied. Date: 2026-06-20. Iteration 0.
Targeted, minimal edits. Protect all KEEP-tagged content (see constructive-review.md).

## MUST_FIX (blocks pass)

1. **`def:calibration` label collision (chapter.tex:382).** Rename this chapter's label to
   `def:credit-calibration` (or rename the ch07 one). Update any in-chapter `\ref`. BLOCKER ·
   notation_crossref · book-wide.
2. **`eq:lora` triple collision (chapter.tex:299).** Preferred: delete the LoRA equation block
   (lines 296–301) and replace with a one-sentence recap + `\Cref` to the ch03 SSOT. Minimal
   alternative: rename the label to `eq:lora-credit`. BLOCKER · notation_crossref + non_repetition.
3. **SR 11-7 date error (chapter.tex:652).** Change "In 2012" → "In 2011". MAJOR · correctness.
4. **Notebook stubs/placeholders.** Either implement or remove: (a) `demo.ipynb` (no code cells);
   (b) `exercises.ipynb`/`exercises_executed.ipynb` cell 5 placeholder; (c) the mojibake header in
   `exercises.ipynb` cell 6 and the non-UTF-8 bytes. The `illustration` (chapter.tex:860–872) points
   readers to this notebook, so it must be clean. MAJOR · reproducibility.

## SHOULD_FIX (raises a dimension toward ≥90)

5. **Add missing citations** for: CFPB mortgage-shopping study (chapter.tex:422), Sweeney 2002
   (chapter.tex:126), Lusardi & Mitchell 2011 financial-literacy battery (chapter.tex:534,549).
   Add bib entries + `\cite`. Until done these remain NEEDS_EXTERNAL_VERIFICATION (caps
   citation_accuracy at 89). citation_accuracy / completeness.
6. **Concept separation:** move the three heaviest derivations out of `context` into `deepdive`
   boxes — masked-softmax (lines 325–337), SHAP Shapley formula (eq:shap, lines 796–809), and the
   Gini proof (716–729). Keeps intuition layer readable standalone. concept_separation.
7. **Fix currency conflation** in the persona prompt (chapter.tex:552): either keep one currency per
   persona consistently or note the rough parity. finance_examples.
8. **Source the bureau-coverage and FICO/VantageScore figures** (chapter.tex:48, 58) or soften.
   correctness.

## OPTIONAL

9. Add a short closing synthesis section mapping results back to the 8 learning objectives.
10. Reconsider reuse of `campbell2006household` for the alternative-data claim (chapter.tex:64); a
    dedicated alternative-data reference would be a tighter anchor.
11. Strengthen the inline forward-pointer for AUROC at line 379 (already present; consider a
    one-line parenthetical definition so the term is self-contained on first appearance).

## DO_NOT_CHANGE (protect)

- Gini = 2·AUROC − 1 proof (716–729) — correct, SSOT.
- AUROC / KS definitions (662–704) — correct, SSOT.
- Structured-generation derivation + digit-by-digit example (305–373).
- Calibration definition content (381–390) — only the *label* changes, not the text.
- Maria & Thomas personas (544–572), serialisation example (268–290), API + GDPR-explanation
  examples (895–940, 1047–1056), SHAP waterfall table (815–840).
- Apple Card cold-open (35–39) and the modelling-arc narrative (188–242).

## BOOK_WIDE_ITEMS

- **BW-1 (notation_crossref):** `def:calibration` defined in both ch06:382 and ch07:400 — global
  rename needed; coordinate so exactly one chapter owns the label.
- **BW-2 (notation_crossref):** `eq:lora` defined in ch02:2189, ch03:786, ch06:299 — triple
  collision; ch03 should be the SSOT, others `\Cref` it.
- **BW-3 (non_repetition):** LoRA (ch06:294–301) and likely Merton/reduced-form (ch06:202–228)
  re-derive content owned by ch03 / a valuation-or-risk chapter; verify SSOT and cross-reference.
- **BW-4 (concept_ordering, downstream):** AUROC/KS/Gini/calibration/SHAP are defined here (read
  #10); verify ch12/ch13 `\Cref` these rather than redefining, and do not collide `def:calibration`.
