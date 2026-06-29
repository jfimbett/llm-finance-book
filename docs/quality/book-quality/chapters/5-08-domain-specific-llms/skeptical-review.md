# Skeptical Review — Ch 08 Domain-Specific Financial LLMs (reading index 5)

Audit only. Format: `SEVERITY · dimension_key · file:line — issue`. Scope tags per RUBRIC.md §3.
File = book/chapters/08-domain-specific-llms/chapter.tex unless noted.

## BLOCKER

- BLOCKER · citation_accuracy · chapter.tex:285–298 — **BloombergGPT token totals need
  external verification.** Chapter states 50B params, ~708B total tokens, 363B
  Bloomberg-proprietary + 345B public. The bib entry `wu2023bloomberggpt` is an arXiv
  stub with no page/figure anchors. (For the record, the public report's FinPile is
  ~363B and the public mix ~345B for ~708B total, 50B params — but this must be
  confirmed against the source, not asserted.) Scope: citation. → NEEDS_EXTERNAL_VERIFICATION.

- BLOCKER · reproducibility · code/notebooks/08-domain-specific-llms/demo.ipynb — **Paired
  notebook is a stub.** demo.ipynb contains only an import + `print("Chapter 08 demo
  notebook")`; it demonstrates none of the chapter's concepts (DAPT, FinBERT inference,
  cost model). figures/ holds only `.gitkeep`. No figure or worked-code artifact is
  regenerable. Scope: code-figure. Caps reproducibility well below 90.

## MAJOR

- MAJOR · citation_accuracy · chapter.tex:226–228 — **FinBERT "+15 F1 / 1.8B words" needs
  verification.** Quantitative claims (≈1.8B-word corpus; ~15 pp F1 gain over BERT-base)
  attributed to `araci2019finbert` (arXiv stub). Plausible but not locally verifiable.
  Scope: citation. → NEEDS_EXTERNAL_VERIFICATION.

- MAJOR · citation_accuracy · chapter.tex:630–639 — **Specific F1 figures (FinBERT 0.88,
  BERT-base 0.72, RoBERTa 0.80 on Financial PhraseBank) need verification.** Precise
  numerics presented as fact; source is an arXiv stub. Scope: citation.
  → NEEDS_EXTERNAL_VERIFICATION.

- MAJOR · citation_accuracy · chapter.tex:243–251 — **SEC-BERT "~3B tokens" / NER
  outperformance** attributed to `loukas2022secbert`. Note the cited paper is the SEC-BERT
  / financial-domain LM line (Loukas et al.); the precise token count and the claim that
  it beats "domain-adapted FinBERT" should be checked against the source. Scope: citation.
  → NEEDS_EXTERNAL_VERIFICATION.

- MAJOR · citation_accuracy · chapter.tex:561–572 — **FinQA scale & leaderboard numbers**
  ("8,281 QA pairs", specialist 68–72%, GPT-4-class 55–60%) need verification against
  `chen2021finqa` and the live leaderboard; leaderboard figures drift over time. Scope:
  citation. → NEEDS_EXTERNAL_VERIFICATION.

- MAJOR · citation_hygiene · book/bibliography.bib (`shah2022flue`) — **Stub flag left in
  bib.** Entry carries `note = {Needs verification before final release}` and uses
  `author = {... and others}` with no pages/volume. FLUE benchmark claims at chapter.tex:
  574–584 inherit this uncertainty. Scope: citation. Lowers citation_hygiene.

- MAJOR · citation_accuracy · chapter.tex:586–601 — **FinBen "36 datasets / 24 tasks / 5
  categories"** attributed to `xie2024finben` (arXiv 2402.12659). Verify counts and the
  NeurIPS D&B venue claim. Scope: citation. → NEEDS_EXTERNAL_VERIFICATION.

- MAJOR · citation_accuracy · chapter.tex:651–664 — **RahimikiaDrinkall2024 "up to 50×
  parameter count" return-prediction claim** rests on an SSRN working paper
  (`#4963618`, `@unpublished`). The strong "outperform up to 50 times their parameter
  count" assertion must be verified against the paper. Scope: citation.
  → NEEDS_EXTERNAL_VERIFICATION.

## MINOR

- MINOR · concept_ordering · chapter.tex:187–208 — **Taxonomy self-correction.**
  §ch08-encoder-decoder opens "A third architectural family that the taxonomy above
  implicitly omits…", i.e. `def:ch08-taxonomy` (170–184) is incomplete and patched in
  the next subsection. Fold the encoder–decoder family into the definition. Scope: local.

- MINOR · citation_hygiene · book/bibliography.bib (`liu2018`) — **Key/year mismatch.**
  Key `liu2018` but `year = {2019}` (RoBERTa, arXiv:1907.11692). Cited at chapter.tex:881
  as "RoBERTa pretraining improvements." Harmless but a hygiene smell. Scope: citation.

- MINOR · citation_accuracy · chapter.tex:298–302, 304–319, 321–338, 801–806 —
  **Secondary SSRN/working-paper citations** (`Keshri2025`, `Yang2023`, `Hirano2024a/b`,
  `Zhang2023`, `Liu2024`, `CookKazinnik2023`) are `@unpublished`/SSRN. Descriptions are
  plausible and hedged, but each is locally unverifiable. Scope: citation.
  → NEEDS_EXTERNAL_VERIFICATION.

- MINOR · correctness · chapter.tex:603–617 — **Execution accuracy definition is a
  generalisation.** FinQA's official metric is exact program-/answer-execution match;
  presenting it as an $\epsilon$-tolerance band (eq:ch08-execution-accuracy) is a defensible
  abstraction but slightly overstates the standard practice. Scope: local.

- MINOR · finance_examples · chapter.tex:808–828 — **Cost numbers are illustrative but
  unlabelled as such.** "\$200–\$600", "\$400/mo", "1,000 paragraphs/sec on a T4", 88% vs
  93% accuracy are invented for the worked example. They are reasonable, but a one-line
  "illustrative figures" caveat would prevent readers treating them as benchmarked.
  Scope: finance-example.

- MINOR · code_figure_correctness · chapter.tex (whole) — **No figures; tables/worked
  numbers only.** `tab:ch08-corpus-summary` numbers are order-of-magnitude approximations
  ($\sim$); fine as labelled, but unbacked by any regenerable artifact. Scope: code-figure.

## NIT

- NIT · notation_crossref · chapter.tex:359,689,903 — Forward references to
  `ch:llm-agents` (read pos 6) and `ch:applications-future` (read pos 15) from pos 5. All
  labels resolve; these are legitimate forward pointers (RAG, EU AI Act) not
  use-before-definition, but they front-load dependencies on not-yet-read chapters.
  Scope: cross-chapter-ordering.

- NIT · non_repetition · chapter.tex:410 — MLM/CLM re-glossed here though introduced in
  chs 01/02; the sentence correctly cross-refs `ch:intro`/`ch:llm-foundations`, so the
  overlap is intentional and signposted. Scope: book-repetition.

## Local vs book-wide

- **Local:** taxonomy self-correction (187–208); execution-accuracy framing; illustrative
  cost numbers not labelled.
- **Book-wide:** SSRN/arXiv-stub verification debt (BloombergGPT, FinBERT F1s, FinQA/FinBen
  counts, RahimikiaDrinkall 50× claim) recurs across chapters that cite these same papers;
  `shah2022flue` stub note and `liu2018` key/year mismatch live in the shared bib and
  affect every chapter citing them.
