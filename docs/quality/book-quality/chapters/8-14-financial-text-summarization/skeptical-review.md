# Skeptical Review — Ch 14 Financial Text Summarization (reading index 8)

Date: 2026-06-20 · Scope: chapter · Audit only (no edits)
Format: `SEVERITY · dimension_key · file:line — issue` · scope tag in parentheses.

## BLOCKER
(none — no factually broken math, no unresolved \ref/\cite, no fabricated stats presented as real)

## MAJOR

- MAJOR · citation_accuracy · chapter.tex:222-229, 840-843, 11, 918 (citation) —
  "FINER-139 \citep{shah2023finer} … annotates 139 fine-grained entity types." The 139-type
  FINER-139 benchmark is from Loukas, Fergadiotis, Chalkidis et al., "FiNER: Financial Numeric
  Entity Recognition for XBRL Tagging" (ACL 2022). The cited `shah2023finer` is a DIFFERENT
  paper: Shah et al. (2023) "FINER: Financial Named Entity Recognition Dataset and Monolingual
  Models for English and Greek" (FinNLP@IJCNLP-AACL) — not a 139-class taxonomy. Probable
  misattribution of the named "FINER-139" dataset and its 139-type count to the wrong source.
  NEEDS_EXTERNAL_VERIFICATION. Caps citation_accuracy at 89.

- MAJOR · citation_accuracy · chapter.tex:223-228 (citation) — Description says FINER-139's
  taxonomy decomposes into "Public Company, ETF, Interest Rate" type subtypes. FINER-139 (Loukas
  2022) is a numeric-entity / XBRL-tag recognition benchmark whose 139 classes are numeric XBRL
  tags (e.g., us-gaap monetary concepts), not generic org/instrument subtypes. The described
  taxonomy appears inconsistent with the actual dataset. NEEDS_EXTERNAL_VERIFICATION.

- MAJOR · citation_hygiene · book/bibliography.bib (frattaroli2019 entry), cited at
  chapter.tex:134 (citation) — bib entry carries `note = {Needs verification before final
  release}`: an unresolved stub marker. Not release-clean.

- MAJOR · citation_hygiene · book/bibliography.bib (mukherjee2022ectsum entry), cited at
  chapter.tex:441,533,828,921 (citation) — ECTSum bib entry carries `note = {Needs verification
  before final release}`. ECTSum is load-bearing (primary long-doc summarization benchmark);
  the stub note must be cleared. Also verify the "2,425 transcripts" and "~7,000 words avg"
  figures (chapter.tex:533-535, 828-831) against the paper.

- MAJOR · concept_separation · chapter.tex:266-308, 339-352, 723-780 (local) — The chapter
  uses ZERO `context`/`deepdive` boxes. Math-heavy internals (NER softmax head eq.
  \eqref{eq:ner-classification}; bilinear relation scorer \eqref{eq:relation-score}; ROUGE-N
  \eqref{eq:rouge-n}; BERTScore cosine \eqref{eq:bertscore}) are interleaved with big-picture
  prose with no environment-level delineation. Rubric dim 2 ≥90 requires the two layers be
  clearly separated (e.g. context vs deepdive) so the reader can follow either alone. Caps
  concept_separation below 90.

## MINOR

- MINOR · notation_crossref · chapter.tex:943 (local) — hard-coded prose ref "Chapter~13"
  instead of `\Cref{ch:llm-limitations-evaluation}` (or whatever ch13's label is). Rubric dim 12
  forbids hard-coded chapter-number prose refs. (Note: line 204 "Chapter~\ref{ch:llm-foundations}"
  is acceptable since \ref resolves to a number, but \Cref is the cleaner convention.)

- MINOR · correctness · chapter.tex:310-325 (local) — Example claims "training set contains
  approximately 900 annotated sentences" for FINER-139 and "10 epochs … ~20 minutes on a single
  A100." Given the FINER-139 attribution uncertainty above, the 900-sentence figure is unverified;
  FINER-139 (Loukas 2022) is a large corpus (~1M+ sentences), so "900 sentences" may be wrong.
  NEEDS_EXTERNAL_VERIFICATION.

- MINOR · correctness · chapter.tex:573-576 (local) — "commercial models with extended context
  windows of 128K to 1M tokens — such as Gemini 1.5 Pro" is time-bound ("as of 2024"); acceptable
  but verify it remains the intended exemplar. Low risk (hedged with "as of 2024").

- MINOR · code_figure_correctness · chapter.tex:318 (code-figure) — $C = 2 \times 139 + 1 = 279$
  is internally correct (BIO: B-/I- per type + O). Keep; just flag it depends on the 139 figure.

- MINOR · reproducibility · code/notebooks/14-financial-text-summarization/demo.ipynb (code-figure)
  — demo.ipynb is a 2-cell stub (`print("Chapter 14 demo notebook")`), not a real demonstration
  of any chapter concept. The exercises.ipynb is real; demo.ipynb is a placeholder.

## NIT

- NIT · finance_examples · chapter.tex:141 (finance-example) — Microsoft $56.5B Q3 FY2023 figure
  is footnoted as illustrative/consult-filings. Good practice; no action.
- NIT · citation_hygiene · book/ contains bibliography_bibertool.bib and bibliography_test.bib
  alongside bibliography.bib (book-wide) — potential stale-.bib confusion; not chapter-specific.

## Book-wide observations (not local to ch14)
- (book-repetition) ROUGE/BERTScore/NER/RAG also appear in ch13 (llm-limitations-evaluation),
  ch02, ch03, ch04. Ch14 is the natural SSOT for ROUGE/BERTScore/summarization metrics; verify
  ch13 cross-references here rather than re-deriving. Ch14's overlap is cross-referenced
  (\ref{sec:ch14-rouge-bertscore-metrics}) and appropriate.
- (citation) Two `Needs verification before final release` stub notes in bibliography.bib touch
  this chapter (frattaroli2019, mukherjee2022ectsum) — these are book-wide bib-hygiene debt.
