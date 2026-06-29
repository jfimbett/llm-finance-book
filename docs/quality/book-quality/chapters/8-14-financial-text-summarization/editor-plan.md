# Editor Plan — Ch 14 Financial Text Summarization (reading index 8)

Date: 2026-06-20 · Scope: chapter · Audit only — no edits applied.
Targeted, minimal edits. Protect all KEEP-tagged content from constructive-review.md.

## MUST_FIX (blocks ≥90)

1. **FINER-139 attribution** (citation_accuracy) — `chapter.tex:222, 840, 11, 918`.
   Verify externally: the 139-type "FINER-139" dataset is Loukas et al. 2022 ("FiNER:
   Financial Numeric Entity Recognition for XBRL Tagging", ACL 2022), NOT `shah2023finer`.
   If confirmed: add a `loukas2022finer` bib entry and re-point the FINER-139 citations to it;
   keep `shah2023finer` only where Shah's English/Greek FINER dataset is actually meant.
   Until verified, mark NEEDS_EXTERNAL_VERIFICATION.

2. **FINER-139 taxonomy description** (citation_accuracy) — `chapter.tex:223-228`. Reconcile
   the "Public Company / ETF / Interest Rate" subtype description with the actual dataset
   (XBRL numeric tags). Correct after (1) is resolved.

3. **Clear bib stub notes** (citation_hygiene) — `bibliography.bib`: remove
   `note = {Needs verification before final release}` from `frattaroli2019` and
   `mukherjee2022ectsum` after confirming the entries' bibliographic details (and the ECTSum
   "2,425 / ~7,000 words" figures used at chapter.tex:533-535, 828-831).

4. **Add concept-separation boxes** (concept_separation) — wrap the four equation blocks and
   their derivations in `deepdive` and the surrounding intuition in `context`:
   - `chapter.tex:266-308` NER token-classification head (eq:ner-classification)
   - `chapter.tex:339-352` relation scorer (eq:relation-score)
   - `chapter.tex:723-744` ROUGE-N (eq:rouge-n)
   - `chapter.tex:746-762` BERTScore (eq:bertscore)
   Goal: big-picture reader can skip internals; no new content, just environment wrapping.

## SHOULD_FIX

5. **Hard-coded chapter ref** (notation_crossref) — `chapter.tex:943`: replace "Chapter~13"
   with `\Cref{ch:llm-limitations-evaluation}` (confirm ch13's actual label).

6. **FINER-139 example sentence count** (correctness) — `chapter.tex:313`: verify/correct
   "approximately 900 annotated sentences" once attribution (1) is settled.

7. **demo.ipynb is a stub** (reproducibility) — flesh out
   `code/notebooks/14-financial-text-summarization/demo.ipynb` (currently 2 cells) with a real
   minimal demo of one chapter concept, or remove it and rely on exercises.ipynb.

## OPTIONAL

8. `chapter.tex:204`: change "Chapter~\ref{ch:llm-foundations}" to `\Cref{ch:llm-foundations}`
   for convention consistency (renders identically; not required).
9. `chapter.tex:573`: optionally generalise the "Gemini 1.5 Pro / as of 2024" exemplar to reduce
   time-boundedness.

## DO_NOT_CHANGE (protect)
- Definitions at `chapter.tex:81-88, 167-183, 391-408` (SSOTs).
- Earnings-call entity example `136-156`; GPT-4 prompt example `464-490` (illustrative numbers
  already hedged — keep the hedging).
- Arithmetic-reliability remark `663-671`; consistency-checking pipeline `685-699`.
- Bridges `204, 938-944`.
- exercises.ipynb EDGAR pipeline (real, [B]/[I]/[A] tagged).

## BOOK_WIDE_ITEMS
- BW1 (citation_hygiene): clear `Needs verification before final release` notes on
  frattaroli2019 and mukherjee2022ectsum in bibliography.bib (also surfaces in other chapters
  citing them).
- BW2 (citation): introduce a distinct `loukas2022finer` key if FINER-139 attribution fix
  requires it; audit other chapters that cite shah2023finer for the same FINER/FINER-139 mixup.
- BW3 (non_repetition): confirm ch13 cross-references ch14's ROUGE/BERTScore section
  (`sec:ch14-rouge-bertscore-metrics`) rather than re-deriving — designate ch14 as SSOT for
  summarization metrics.
- BW4 (citation_hygiene): stale auxiliary bib files (bibliography_bibertool.bib,
  bibliography_test.bib) present alongside bibliography.bib — book-wide cleanup.
