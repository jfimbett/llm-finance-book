# Editor Plan — Chapter 3 (reading order) · `02-llm-foundations`

Audit date: 2026-06-20 · Scope: chapter · Auditor: audit-editor
File: `book/chapters/02-llm-foundations/chapter.tex`
SSOT = single source of truth. Targeted, minimal edits; protect all KEEP-tagged content
(see constructive-review.md). **Audit only — this plan is not yet applied.**

---

## MUST_FIX (blocks pass; each maps to a BLOCKER/MAJOR)

1. **Resolve the 12 ch01↔ch02 label collisions.** [target: notation_crossref, non_repetition]
   - SSOT: ch02 owns LSTM (`def:lstm`, `eq:lstm-*`), `eq:rnn-jacobian`, `eq:multihead`,
     `def:hallucination`, `eq:cosine-sim`, `tab:api-costs`.
   - Action: in `01-intro/chapter.tex`, **rename or remove** the colliding labels. Preferred:
     remove ch01's re-derivation of LSTM + multi-head and replace with a one-line
     `\Cref{def:lstm}`/`\Cref{def:mha}` forward pointer (ch01 is read first, so phrase as
     "developed in full in \Cref{ch:llm-foundations}"). Verify with
     `comm -12 <(labels ch01) <(labels ch02)` → empty.

2. **Replace the fabricated roadmap table `tab:roadmap`.** [target: correctness, completeness]
   - `chapter.tex:2563-2595`. Current rows describe a non-existent book. Rebuild the table from
     the actual `book/main.tex` reading order (01→16→02→03→08→04→09→14→05→06→10→11→12→13→07→15)
     using `\nameref`/`\Cref{ch:...}` so it stays in sync, OR delete the per-chapter "Ch.N" column
     and key connections that no longer hold.

3. **Replace 15 hard-coded "Chapter~N" prose refs with `\Cref{ch:...}`.** [target: notation_crossref]
   - `chapter.tex:24,160,346` (→ `\Cref{ch:intro}`), and 1339,1405,1425,1427,1819,2501,2502,2519,
     2527,2560,2598,2599. Use the chapter `\label`s, never literal numbers.

4. **Populate `demo.ipynb` or re-point the six prose references.** [target: code_figure_correctness,
   reproducibility]
   - `chapter.tex:1690,1716,1841,1849,1855,2079`. Either (a) fill
     `code/notebooks/02-llm-foundations/demo.ipynb` with the promised runnable code (temperature
     sampling, JSON/tool-use extraction, OpenAI/Anthropic/HuggingFace calls, FAISS RAG), or
     (b) point these references to `exercises.ipynb` (which is real, 22 cells) if that is where the
     code actually lives. Today the promise is unfulfilled.

5. **Delete the duplicate `wei2022emergent` bib entry.** [target: citation_hygiene]
   - `book/bibliography.bib` lines 1727 and 3175 are identical; remove one.

## SHOULD_FIX

6. **Verify uncited-but-claimed statistics.** [target: citation_accuracy → cap 89 until done]
   - Araci-FinBERT "97% / +8pp" (`chapter.tex:1091`) and `chen2024uncertainty` "Sharpe +20%"
     (`chapter.tex:2356`): confirm against the source papers; mark NEEDS_EXTERNAL_VERIFICATION
     until checked.

7. **Add an intra-chapter big-picture path through the math.** [target: concept_separation]
   - The long `deepdive` runs (doc-repr 48-338, sequential 344-613, transformer 619-1121) would
     benefit from a 2-3 sentence `context` recap so the big-picture-only reader has a standalone path.

## OPTIONAL

8. Add a one-line note in the `illustration` env (`chapter.tex:1136-1149`) on how to regenerate
   `fig_illustration.pdf` from the notebook (seed / script path), for reproducibility 100-tier.

## DO_NOT_CHANGE (protect — KEEP-tagged)

- All math derivations: attention (787-857), √d_k (818-827), positional encoding + proof (889-943),
  LSTM cell-state argument (454-505), vanishing-gradient bound (407-429), KD/forward-KL (2126-2163),
  LoRA arithmetic (2183-2207), temperature/sampling (1452-1531).
- Finance worked examples: merger valuation (1243-1272), FinBERT-two-models (1084-1101),
  cost example (1910-1918), FinanceBench (2091-2096), hallucination example (2303-2314).
- The `context`/`deepdive` opener narratives — exemplary separation; preserve voice.

## BOOK_WIDE_ITEMS (escalate to /iterate-book-quality / book-level editor)

- **BW-1** (BLOCKER): ch01↔ch02 12-label collision — fix belongs in `01-intro` (item 1). SSOT=ch02.
- **BW-2** (BLOCKER): ch01 duplicate derivation of RNN/vanishing-gradient/attention/multi-head/LSTM —
  thin ch01 to `\Cref` pointers; ch02 remains SSOT for these internals.
- **BW-3** (MAJOR): `wei2022emergent` duplicate bib key (item 5) — a bibliography-wide hygiene fix.
- **BW-4** (MAJOR): Wrong roadmap table + wrong Chapter~N refs (items 2,3) reflect a book-wide
  numeric-vs-reading-order drift; audit other chapters for the same hard-coded-number pattern.
