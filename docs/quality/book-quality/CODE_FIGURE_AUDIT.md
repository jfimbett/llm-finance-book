# CODE_FIGURE_AUDIT.md

> Code/figure existence, figure↔prose match, and reproducibility. Drives `RUBRIC.md`
> dims 3 (`code_figure_correctness`) and 13 (`reproducibility`).
> **Status: VERIFIED across all 16 chapters (2026-06-20 full audit).** Static review only
> — no networked code executed.

## Headline finding: every `demo.ipynb` is a stub

All **16** `code/notebooks/*/demo.ipynb` are placeholder stubs (<1.7 KB; most ~700 bytes,
imports + one `print`), yet chapter prose repeatedly cites `demo.ipynb` as "the complete
Python implementation." This single pattern caps `reproducibility` and
`code_figure_correctness` book-wide. The real runnable code, where it exists, lives in
`exercises.ipynb` (genuine in ch01, 02, 03, 05, 06, 11, 15, 16; toy/partial elsewhere).

```
demo.ipynb sizes (bytes): 01:1610 02:583 03:936 04:944 05:992 06:1051 07:986 08:685
09:691 10:702 11:701 12:688 13:702 14:710 15:1004 16:790   — all stubs
```

## Figure coverage (book-wide)

| Chapters (folder #) | Figures present? |
|---------------------|------------------|
| ch01–ch07 | `fig_illustration.pdf` each; ch01 also EDGAR + king-analogy |
| ch08–ch16 + all appendices | **empty `figures/` (`.gitkeep` only)** — no figures |

- **Dangling ref (BLOCKER):** ch11 `\ref{fig:ch11-rag-pipeline}` (chapter.tex:172) — figure
  never defined; renders `??`. One root cause for two failing dimensions in ch11.
- ch08 also lacks the `\illustration` block that ch01–07 have.

## Per-chapter results (all 16)

| Read# | Chapter | code_figure | reprod. | Key findings |
|-------|---------|-------------|---------|--------------|
| 1 | 01-intro | 82 | 55 | refs resolve; king-analogy faithful; "tripled" prose vs ~1.56x figure; live SEC fetch + hard-coded UA `jfimbett@gmail.com`; stub demo, stale executed nb |
| 2 | 16-ai-ml | n/a | 80 | no figures (`.gitkeep`); `exercises.ipynb` real but live SEC EDGAR, no cache; `demo.ipynb` stub |
| 3 | 02-foundations | 45 | 50 | **6 prose pointers to demo.ipynb (a 583B stub)**; `fig_illustration` matches; `exercises.ipynb` real (22 cells) |
| 4 | 03-training | 87 | 80 | illustration figure reproducible, coefficients match caption; demo stub; EDGAR exercise cells unexecuted |
| 5 | 08-domain | 70 | 55 | figures `.gitkeep` only; demo stub; no regenerable artifact backs the chapter |
| 6 | 04-agents | 70 | 60 | figure matches notebook & runs; demo stub cited 3× as "complete implementation" |
| 7 | 09-nlp-sentiment | 78 | 76 | demo 2-cell stub; `exercises.ipynb` real but mislabels ~20-word toy list as Loughran–McDonald; net formula diverges from `eq:lm-sentiment` |
| 8 | 14-summarization | 90 | 78 | scored on tables/worked examples (no figures); demo 2-cell stub |
| 9 | 05-valuation | 86 | 62 | single figure accurate (Gordon-Growth spot-check ok); demo stub cited ~10×; FCF $98.8B (yfinance) vs $108.8B (EDGAR); **orphaned `valuation_example/` is the strongest runnable asset but uncited** |
| 10 | 06-credit | 88 | 70 | figure reproducible (AUROC 0.6837, KS 0.3476, Gini 0.3673 — identity verified); demo no-code stub; `exercises.ipynb` has `[Placeholder]` cell + mojibake/invalid UTF-8 |
| 11 | 10-portfolio | 84 | **35** | **worst reproducibility**: demo print-only stub; figures `.gitkeep`; none of mean-variance/BL/backtest/CVaR/GARCH demonstrated or regenerable |
| 12 | 11-regtech | 45 | 55 | **dangling `fig:ch11-rag-pipeline`**; demo stub implements none of RRF/AMI/XBRL; `exercises.ipynb` real (SEC EDGAR lab) |
| 13 | 12-xai | 80 | 65 | no figures (`.gitkeep`); demo 2-cell placeholder; methods (SHAP/LIME/IG) not demonstrated |
| 14 | 13-limitations | n/a | 60 | no figures; ECE worked example verified (0.115); display typo line 118 (`0.012`→`0.12`); demo 2-cell stub |
| 15 | 07-future | 55 | 58 | demo 1-cell `[Placeholder — fill in]` yet cited as "complete implementation"; real code in `exercises.ipynb` |
| 16 | 15-privacy | 91 | 70 | DP/FedAvg math verified vs Dwork–Roth & McMahan; `exercises.ipynb` real & good; demo stub; no figures |

## Reproducibility risks (book-wide)

| Risk | Where | Severity |
|------|-------|----------|
| All 16 `demo.ipynb` are stubs but cited as authoritative | every chapter | MAJOR |
| Live SEC/EDGAR fetch + hard-coded personal User-Agent | ch01 `gen_edgar_text_growth.py:42`; ch05 nb (`instructor@dauphine.eu`); ch11/ch16 exercises | MAJOR |
| ~1 GB GloVe download | ch01 `gen_king_analogy.py` | MAJOR |
| Live yfinance (news/financials), no seed/snapshot | ch01 `fig_illustration`; ch05 figure | MAJOR |
| Mojibake / `[Placeholder]` cells in executed exercise nbs | ch06, ch07, stale ch01 | MINOR |
| `code/run_illustrations.sh` covers only ch01–07 (7/16); `gen_*.py` not wired in | repo | MAJOR |
| Empty `code/src/__init__.py`, `code/tests/` | repo-wide | MINOR |

## Backlog (book-wide reproducibility effort — mostly not per-chapter edits)

1. Fill `demo.ipynb` for every chapter, **or** stop citing them as the implementation
   (point prose at `exercises.ipynb`). Highest-impact single action.
2. Define or remove `fig:ch11-rag-pipeline`; generate figures for ch08–16.
3. Parameterize the SEC User-Agent (env var / `--user-agent`); remove personal emails.
4. Vendor frozen data snapshots; add seeds; pin accessions.
5. Wire `gen_*.py` + ch08–16 generators into `run_illustrations.sh`.
6. Clean mojibake / placeholder cells; refresh stale executed notebooks.
