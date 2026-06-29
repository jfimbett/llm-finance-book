# Skeptical Review — Ch 04 LLM Agents and Finance Applications

Format: `SEVERITY · dimension_key · file:line — issue`. Scope tagged `local` or book-wide
(`book-repetition` / `cross-chapter-ordering` / `citation` / `code-figure`).
Audit date 2026-06-20. Audit only — no edits applied.

## BLOCKERS

- `BLOCKER · reproducibility · code/notebooks/04-llm-agents/demo.ipynb (whole file) — local/code-figure` —
  `demo.ipynb` is a pure placeholder: 0 code cells, 1 markdown cell reading
  "[Placeholder — fill in with demonstration code when drafting the chapter]". Yet the
  chapter explicitly promises "The complete Python implementation for this example is
  available in `code/notebooks/04-llm-agents/demo.ipynb`" **three times**
  (chapter.tex:419, chapter.tex:732, chapter.tex:1123). Every one of those promises is
  false; the reader cannot reproduce the tool-registration, two-agent extractor/classifier,
  or report-generation examples. This caps reproducibility and damages code_figure_correctness.

- `BLOCKER · notation_crossref · book/chapters/04-llm-agents/chapter.tex:763 — book-repetition/duplicate-label` —
  `\label{def:rag}` collides with `\label{def:rag}` in
  `book/chapters/02-llm-foundations/chapter.tex:1972`. Two competing formal
  `definition[Retrieval-Augmented Generation]` environments share one label: ch02 gives a
  three-stage pipeline definition; ch04 gives the marginalization definition (Eq.
  `eq:rag-marginal`). LaTeX will emit "multiply-defined labels" and any `\ref{def:rag}`
  resolves to whichever is compiled last. Must relabel one (e.g. `def:rag-marginal`) and
  cross-reference rather than re-define.

## MAJOR

- `MAJOR · citation_hygiene · book/bibliography.bib (zhang2024financebench) — citation` —
  Entry carries an unresolved audit stub `} % [CHECK] verify author list and title spelling`,
  and its `author = {Islam, Shariful and Zhu, Meng and Rahimi, Mostafa ...}` does not match
  the FinanceBench paper (arXiv 2311.11944), whose lead author is Pranab Islam et al. The
  recorded author list appears fabricated/incorrect. Cited at chapter.tex:1201. Verify and
  correct; NEEDS_EXTERNAL_VERIFICATION for the exact author roster.

- `MAJOR · citation_accuracy · book/chapters/04-llm-agents/chapter.tex:1380 — citation` —
  Chapter cites `\citep{esma2018mifid2}` for "MiFID II's record-keeping obligations
  (Article 16)". The bib entry `esma2018mifid2` is titled "Guidelines on Certain Aspects of
  the MiFID II **Suitability** Requirements" (ESMA35-43-1163) — a suitability guideline, not
  the Article-16 record-keeping source. Likely wrong source for the proposition. Verify the
  intended ESMA/MiFID II record-keeping reference. NEEDS_EXTERNAL_VERIFICATION.

- `MAJOR · citation_accuracy · book/bibliography.bib (kurshan2024agenticregulator) — citation` —
  Entry has `year = {2024}` but `journal = {arXiv preprint arXiv:2512.11933}`; arXiv ID
  2512.xxxxx denotes December 2025, inconsistent with the 2024 year. The strong claims drawn
  from it (chapter.tex:1478–1486: "self-regulation modules, firm-level governance blocks,
  regulator-hosted monitoring agents") cannot be locally verified. NEEDS_EXTERNAL_VERIFICATION.

- `MAJOR · non_repetition · book/chapters/05-business-valuation/chapter.tex:675–697 — book-repetition` —
  ch05 (reading position 9, AFTER this chapter) **re-introduces and re-derives ReAct**:
  `\citet{yao2022react} proposed the ReAct (Reason + Act) framework, which interleaves...`
  followed by its own Thought/Action/Observation enumeration — with NO `\Cref{ch:llm-agents}`
  at that point (ch05's only ref to ch04 is far away at chapter.tex:1024). This violates the
  SSOT designation: ch04 owns ReAct via `def:react-trajectory`. The defect lives in ch05, not
  here, but it is logged as a BOOK_WIDE item because this chapter is the SSOT.

## MINOR

- `MINOR · non_repetition · book/chapters/04-llm-agents/chapter.tex:762 — book-repetition` —
  Beyond the label collision, RAG is conceptually defined twice in the book (ch02:1970 and
  ch04:762). ch04's deeper marginalization treatment should open with an explicit
  `\Cref{...}` bridge to the ch02 pipeline definition ("recall the three-stage pipeline of
  Ch. … here we cast retrieval as a latent variable") to make the layering intentional.

- `MINOR · notation_crossref · book/chapters/04-llm-agents/chapter.tex:861 — local` —
  Equation `eq:hybrid-search` is `\label`'d but never `\eqref`'d anywhere; the label is dead
  weight. Harmless but a polish item.

- `MINOR · citation_hygiene · book/bibliography.bib (yao2022react) — citation` —
  Entry carries `} % [CHECK] venue confirmed ICLR 2023` audit comment; the comment itself
  states it is confirmed, so the marker should simply be removed for cleanliness. Cite key
  `wang2023survey` resolves but the bib `year` is 2024 (key implies 2023) — cosmetic key/year
  mismatch, not a resolution failure.

- `MINOR · completeness · book/chapters/04-llm-agents/chapter.tex:1505 — local` —
  The chapter ends abruptly after the governance `context` box closes; there is no
  end-of-chapter Summary / Key Takeaways / "what's next" bridge to the next reading-order
  chapter (09-financial-nlp-sentiment). Given the 8 learning objectives in the opening
  `remark` (chapter.tex:4–25), a closing synthesis would strengthen pedagogy and progressive
  learning.

## NIT

- `NIT · finance_examples · book/chapters/04-llm-agents/chapter.tex:1086,1174 — local` —
  Several illustrative numbers (latency "3.2 minutes", "60bps overweight", named position
  weights) are hypothetical. The earnings example is properly fenced by the remark at
  chapter.tex:1068–1070; the portfolio example `ex:portfolio-qa` (chapter.tex:1160) is not
  explicitly labelled hypothetical. Consider one shared disclaimer for consistency.

- `NIT · correctness · book/chapters/04-llm-agents/chapter.tex:119 — local` —
  "a 128,000-token context can hold approximately 100 pages of text" is a defensible
  round-number heuristic (~1.3k tokens/page) but is presented as fact; soften or cite.
