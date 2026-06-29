# Skeptical Review — 9 · 05-business-valuation (LLMs for Business Valuation)

Reading index 9 (order: 01,16,02,03,08,04,09,14,**05**,06,10,11,12,13,07,15).
File: `book/chapters/05-business-valuation/chapter.tex` (1241 lines).

## Issues (ranked)

### BLOCKER

[BLOCKER · completeness · local] chapter.tex:84–85, and 36 uses of `WACC` throughout —
WACC is the single most sensitive DCF input and is used pervasively (§1.2 eq:dcf,
§2.1 example, §5.3 case study at 9%, §6 Monte Carlo, §8 error propagation) but is
**never derived or estimated**. The only treatment is an inline parenthetical formula
`WACC = w_E r_E + w_D r_D(1-τ)` on line 85. There is no CAPM, no cost-of-equity
(`r_E`) estimation, no cost-of-debt (`r_D`), no beta/risk-free/equity-risk-premium
discussion, and no WACC-estimation subsection. CAPM appears nowhere in the book in
reading order before chapter 9 (grep over reading-#1..#6 returns nothing), so the
reader has no source-of-truth to fall back on. The rubric names this verbatim as the
canonical completeness failure (RUBRIC §1, `completeness` anchor: "0 = major gaps
(e.g. WACC never derived)").
  Fix: Add a subsection to §1.2 or §3 ("Estimating the Discount Rate") that derives
  WACC: define CAPM `r_E = r_f + β(E[r_m] − r_f)`, give cost of debt from yield/credit
  spread, the tax shield, and market-value weights; then wire it to the AAPL CAPM
  computation already implemented in the orphaned exercise (WACC = 8.84% in
  `exercises/valuation_example/results/dcf_result.json`). This simultaneously closes
  the orphan gap below.

### MAJOR

[MAJOR · finance_examples · finance-example] chapter.tex:1043–1091 (§5.3 case study);
orphan at `exercises/valuation_example/` — The chapter's only worked end-to-end case
study uses a **stylised composite SaaS firm** ("specific company names and figures are
illustrative", line 1047–1048) with invented FCF tables. Meanwhile a *complete, real*
AAPL DCF+comps multi-agent exercise exists at `exercises/valuation_example/` with real
SEC-XBRL data (`data/aapl_fy2024.json`), a two-stage CAPM-based DCF
(`results/dcf_result.json`: intrinsic $225.00 vs reference $226.84, −0.81% error),
comps (`results/comps_result.json`: P/E + EV/EBITDA triangulated $217.09), accuracy
validation, and Claude skills (`/estimate-wacc`, `/run-dcf`, `/run-comps`,
`/iterate-to-target`). `grep -rn valuation_example book/` returns **nothing** — it is
fully ORPHANED and unreferenced. RUBRIC `finance_examples` ≥90 explicitly requires
"integrated (cf. wiring in `exercises/valuation_example/`), reader can run them."
  Fix: Reference and wire the exercise into §5.3 (and §8 benchmarking). Replace or
  supplement the synthetic SaaS case with the reproducible AAPL run, or at minimum add
  an `\illustration`/`example` box pointing readers to `exercises/valuation_example/`
  with its README quick-start. This is the designated grounded example for the chapter.

[MAJOR · notation_crossref · book-repetition] chapter.tex:926 — Label collision:
`\label{eq:cosine-sim}` is defined three times across the book —
`01-intro/chapter.tex:868`, `02-llm-foundations/chapter.tex:2004`, and here
(`05/chapter.tex:926`). LaTeX silently uses the last definition; any `\eqref{eq:cosine-sim}`
resolves ambiguously. RUBRIC `notation_crossref` ≥90 requires "no label collisions."
  Fix: Rename this chapter's equation label to a chapter-scoped key (e.g.
  `eq:bv-cosine-sim`) and update its single in-section reference. (Same applies to the
  duplicate in ch02 if it is independent.)

### MINOR

[MINOR · non_repetition · book-repetition] chapter.tex:919–932 (§6.3,
def:cosine-similarity) — Cosine similarity is **re-defined here as a formal
`\begin{definition}`** with full `a·b/(‖a‖‖b‖) ∈ [−1,1]` exposition, although it is
already introduced earlier in reading order: ch01 (reading #1, §"cosine similarity…
lies in [−1,1]", lines 868–874) and ch04 LLM-agents (reading #6, line 298–299:
"cosine similarity between vectors u,v is u⊤v/(‖u‖‖v‖)"). Embedding is likewise defined
earlier (`def:word-embedding`, ch01:1099). RUBRIC `non_repetition` ≥90 requires "one
designated single source of truth per concept… cross-referenced via `\ref`, not
re-derived."
  Fix: Replace the standalone definition with a one-line recall + `\Cref` to ch01's
  cosine-similarity equation / `def:word-embedding`; keep only the finance-specific
  application (MD&A peer retrieval). Do not re-derive the [−1,1] range.

[MINOR · correctness · local] chapter.tex:401–405 (ex:fcff-example) — The "~$15.2B"
DCF figure is correct (recomputed: FCFF 713.6 → EV $15.17B, ≈3.6× revenue, matches
text), and the prior score JSON's flagged "$15.2B vs $13.3B ReAct-trace inconsistency"
is now **stale/resolved**: the $13.3B ReAct trace has been removed (the §4 ReAct/code-
interpreter blocks now read "complete Python implementation… in demo.ipynb"), so $13.3B
no longer appears anywhere in the file (`grep 13.3` → only the unrelated "13" none).
No live inconsistency remains.
  Fix: None required for arithmetic; if `docs/quality/.../score.json` still cites the
  $13.3B inconsistency, update it — the defect is gone, the example is internally
  consistent. (Case-study figures at §5.3 also recompute exactly: base EV $16.98B≈$17.0B,
  equity $16.18B, $57.78≈$57.9/share, comps 24.5×$1.225B=$30.0B — all KEEP.)

[MINOR · completeness · local] chapter.tex:1104–1130 (§8.1 benchmarking) — The
benchmarking subsection presents only qualitative "rough illustration" prose
(coverage ">90%/>75%", MAVE "broadly comparable") with **no concrete empirical results
table**. For a chapter whose objective 8 is "evaluate accuracy and efficiency
benchmarks," this leaves the central empirical claim ungrounded.
  Fix: Add a small results table (even from the orphan's `results/accuracy.json`, which
  contains the AAPL −0.81% DCF error and comps deltas) or label the numbers explicitly
  as illustrative targets and cite the source benchmark precisely.

[MINOR · reproducibility · code-figure] chapter.tex:230, 263, 416, 531, 667, 693, 773,
801, 901, 940 — ~10 code locations collapse to the identical sentence "The complete
Python implementation for this example is available in
`code/notebooks/05-business-valuation/demo.ipynb`." None of the actual code (EDGAR
fetch, FCFF function, ReAct loop, Monte Carlo, embedding search) is shown in-text, and
the chapter does not confirm `demo.ipynb` is a real, executable notebook vs. a stub.
The figure (fig:ch05-illustration) is "illustrative… depends on filing date used,"
i.e. not seed-pinned.
  Fix: Confirm `demo.ipynb` exists and runs; pin the figure to a snapshotted AAPL FCF
  (date-anchored) so Figure~\ref{fig:ch05-illustration} is regenerable. Show at least
  the FCFF function and the Monte Carlo core in-text (they are short and load-bearing).

### NIT

[NIT · pedagogy · local] chapter.tex:954 (§6.4) — Grammar: "Prompt-based selection
leverages broad world knowledge but **hallucinate**" → "hallucinates" (subject is
singular "selection"). Flagged in prior score JSON; still present.
  Fix: "but may hallucinate."

[NIT · correctness · local] chapter.tex:354–360 (prop:fcff-fcfe-relation) — The proof
is correct but telegraphic ("rearranging yields"); for a book targeting mixed
academic/industry readers, the one-line algebra (subtract `InterestExp·(1−τ)`, cancel
NI) could be spelled out.
  Fix: Add the explicit intermediate line.

## Per-dimension risk (which dimensions likely FAIL <90)

- `correctness`: **OK** — all worked DCF arithmetic recomputes exactly ($15.2B, $17.0B,
  comps $30.0B, error-prop ≈17.6%); the prior flagged $15.2B/$13.3B inconsistency is
  resolved (trace removed). Minor telegraphic proof only.
- `concept_separation`: **OK** — clean `context` (intuition/intro/pipeline) vs
  `deepdive` (formulas/agents) split; reader can follow either layer.
- `code_figure_correctness`: **AT-RISK** — code is hidden behind 10 identical
  "see notebook" stubs; figure is illustrative/undated. Can't confirm match-to-prose.
- `concept_ordering`: **OK** — concepts (FCFF, CoT, ReAct, embeddings) defined before
  use; cosine/embedding rely on earlier chapters (correct ordering) but are re-derived
  (a non_repetition issue, not ordering).
- `progressive_learning`: **OK** — builds on ch04 agents (`\ref{ch:llm-agents}`),
  smooth curve single-firm → pipeline.
- `non_repetition`: **AT-RISK** — cosine similarity & embedding re-defined though owned
  by ch01/ch04 (MINOR above); fix is a recall + `\Cref`.
- `finance_orientation`: **OK** — finance-first; every technique tied to a DCF/comps step.
- `finance_examples`: **FAIL** — sole case study is a synthetic composite; the real,
  reproducible AAPL DCF+comps exercise (`exercises/valuation_example/`) is orphaned and
  unreferenced. Rubric ≥90 explicitly demands this wiring.
- `citation_hygiene`: **OK** — all 18 cite keys resolve in `.bib`; no missing keys.
- `citation_accuracy`: **AT-RISK / NEEDS_EXTERNAL_VERIFICATION** — descriptions (wei2022chain
  CoT, yao2022react, schick2023toolformer, hu2022lora, LopezLiraTang2023, shen2023nlp
  "embedding peers outperform SIC peers") read correctly but the empirical-result
  attributions (shen2023nlp, zhang2024financebench MAVE claim) are not locally verifiable.
- `completeness`: **FAIL** — WACC used 36× but never derived/estimated (no CAPM); §8
  benchmarking has no results table. (BLOCKER above.)
- `notation_crossref`: **FAIL** — `eq:cosine-sim` label collision across ch01/ch02/ch05;
  silently resolves to wrong target. (`Chapter~\ref{ch:llm-agents}` on line 1024 is a
  proper `\ref`, not a hard-coded number — OK.)
- `reproducibility`: **AT-RISK** — figure not seed/date-pinned; notebook reality
  unconfirmed; orphan exercise is reproducible but not wired in.
- `pedagogy`: **OK** (≈AT-RISK) — objectives map 1:1 to sections; "hallucinate" grammar
  nit; only one in-chapter exercise/illustration.

## One-paragraph assessment

Three things block ≥90. (1) **WACC is never derived or estimated** (BLOCKER,
`completeness`): it drives every DCF in the chapter yet appears only as an inline
formula, with no CAPM and no upstream source-of-truth — the rubric names this exact gap.
(2) The **real, reproducible AAPL DCF+comps exercise** at `exercises/valuation_example/`
is fully **orphaned** (`grep -rn valuation_example book/` → nothing) while the chapter's
only case study is a synthetic composite firm (MAJOR, `finance_examples`) — and that
same exercise already contains the CAPM WACC (8.84%) needed to close gap (1). (3) A
**`eq:cosine-sim` label collision** across ch01/ch02/ch05 plus the **re-derivation of
cosine similarity/embeddings** owned by ch01/ch04 sink `notation_crossref` and
`non_repetition`. The arithmetic is sound and the prior score's $15.2B/$13.3B
inconsistency is now stale (the $13.3B ReAct trace was removed). Fix WACC + wire the
AAPL exercise + scope the cosine label/definition, and the chapter clears the floor on
correctness, ordering, and finance orientation.
