# Editor Plan — 1 01-intro

> Synthesized by `audit-editor` from `constructive-review.md`, `skeptical-review.md`,
> and the concept-ordering / finance / citation / code-figure auditor outputs.
> **Dry-run: no edits applied.** Apply with `/iterate-book-quality 01`.

## Dimensions below 90 (targets)

| Dimension | Score | Addressed by |
|-----------|-------|--------------|
| non_repetition | 68 | T1 |
| notation_crossref | 60 | T1 |
| citation_accuracy | 84 | T2, T3 |
| code_figure_correctness | 82 | T4 |
| concept_ordering | 82 | T5 |
| progressive_learning | 88 | T1 |
| completeness | 88 | T6 |
| reproducibility | 55 | backlog (book-wide) |
| correctness | 88 | T4 |

## MUST_FIX (before re-scoring)

### T1 — Collapse ch01 §6–§7 duplicated derivations to intuition + cross-reference
[dimensions: non_repetition, notation_crossref, progressive_learning, concept_ordering] [scope: book-wide root cause, local edit here]
Location: `chapter.tex:1473–1736` (RNN, LSTM gates, scaled-dot-product attention, `prop:sqrt-dk`, multi-head, `def:mlm`)
Problem: Full re-derivation with proofs of material ch02 (read#3) owns; creates 9 duplicate `\label`s (`def:lstm`, `eq:lstm-*`, `eq:multihead`, `eq:rnn-jacobian`) and a `def:mlm` collision with ch03. ch01's own §Looking-Ahead already promises ch02 derives these from first principles.
Fix: Demote these passages to `context`-box intuition (keep the finance-anchored motivation), remove the duplicated proofs and the colliding `\label`s, and forward-reference with `\Cref{ch:llm-foundations}`. **ch02 is the single source of truth.**
Preserve (constructive KEEP): the §7 *preview* framing and the finance examples (earnings-call RNN, attention-in-finance motivation) — keep as intuition, do not delete the section wholesale; the reader still needs an attention preview at reading position 1.

### T2 — Fix ke2019predicting mischaracterization
[dimension: citation_accuracy] [scope: local]
Location: `chapter.tex:1728` (`rem:attention-finance`)
Problem: Describes `ke2019predicting` (a SESTM / topic-model paper) as an "attention-based model" with "attention weights." The same key is described correctly at line 1320.
Fix: Reword to describe the method accurately, or cite a genuinely attention-based finance paper if one is intended (only if already in `bibliography.bib`).

### T3 — Remove stale `% [CITE:]` comment on didisheim2025memory
[dimension: citation_accuracy] [scope: local]
Location: `chapter.tex:2011`
Problem: The inline `% [CITE:]` comment names a different paper than the resolved bib entry ("AI's Predictable Memory…").
Fix: Delete the misleading comment; the live `\cite` + bib are consistent. Flag the underlying memorization claim `NEEDS_EXTERNAL_VERIFICATION`.

### T4 — Reconcile the "tripled" claim with its figure
[dimensions: correctness, code_figure_correctness] [scope: local]
Location: `chapter.tex:402` + caption `413`
Problem: Prose says 10-K length "roughly tripled 1993–2023" but the figure's cached data is ~1.56x and non-monotonic; caption sample range/size slightly off.
Fix: Attribute "tripled" to the cited word-count series and note the figure plots alphabetic characters (a different metric), or soften the wording; correct caption to the actual year range/sample.

## SHOULD_FIX

### T5 — Local ordering nits
[dimension: concept_ordering] Move `def:corpus-vocab` before `def:textual-signal` (576); define `softmax` before its skip-gram use (1167).

### T6 — Name primitives at first use
[dimension: completeness] Name cross-entropy (AR/MLM losses) and softmax in one clause each for the mixed audience.

## OPTIONAL

- Companion-notebook pointer for an LM-vs-Harvard-IV negativity count (`finance_examples`, already ~90).

## DO_NOT_CHANGE (protected — constructive KEEP)

- §1 task-based automation framing (34–161) — `KEEP_AS_SINGLE_SOURCE_OF_TRUTH` (book's economic thesis).
- §3.2 textual-signal formalism `def:textual-signal` + `rem:identification` (572–658) — analytical backbone.
- §4 TF-IDF worked example (888–1014) — `GOOD_FINANCE_EXAMPLE`, every number load-bearing.
- §2 Loughran–McDonald register motivation (237–250) — best motivation of domain-specific NLP.
- API pricing table (1922–1954) — correctly hedged as illustrative 2024 list prices; do not "fix" numbers or strip hedges.

## Book-wide items → IMPLEMENTATION_BACKLOG.md

- Reproducibility hardening (User-Agent parameterization, GloVe/yfinance snapshots, `run_illustrations.sh` coverage, stale executed notebook) — a book-wide convention change, not a ch01-local edit.
- Delete the 3 stale `.bib` files (`bibliography.bib.new`, `bibliography_bibertool.bib`, `bibliography_test.bib`).

## Contradiction & length check

No internal contradictions. T1 **reduces** length (removes duplicated proofs); other tasks are net-neutral. No new sections added.

## Prediction

After MUST_FIX (T1–T4): non_repetition, notation_crossref, progressive_learning, concept_ordering, correctness, code_figure_correctness, citation_accuracy expected ≥90. completeness lifts to ≥90 with T6. **reproducibility remains <90** (needs the book-wide backlog work + external verification). Chapter pass = **NO until reproducibility is addressed**; 12–13 of 14 dimensions reachable in one iteration.
