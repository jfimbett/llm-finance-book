# CITATION_DESCRIPTION_AUDIT.md

> Three-level citation audit: (1) BibTeX hygiene, (2) resolution, (3) description
> accuracy. Drives `RUBRIC.md` dims 9 (`citation_hygiene`) and 10 (`citation_accuracy`).
> Live bib = `book/bibliography.bib`. The two `bibliography_*.bib` files are stale and
> not loaded. **Status: VERIFIED across all 16 chapters (2026-06-20 full audit).**
> **The old `docs/quality/bibliography-audit.md` is stale — do not trust it.**

## 1. BibTeX hygiene

| Issue | Key / file | Severity | Action |
|-------|-----------|----------|--------|
| **Duplicate key** | `wei2022emergent` (bibliography.bib **:1727 & :3175**, confirmed) | BLOCKER | delete redundant block — build hazard |
| Stub entry | `xu2024stock` (author "and others", venue TBD) | MAJOR | complete or remove |
| Stub flag in entry | `shah2022flue` (`note = {Needs verification before final release}`, "and others", no venue) — cited ch08 | MAJOR | verify/replace |
| Stub flag in entry | `frattaroli2019`, `mukherjee2022ectsum` (`note = {Needs verification before final release}`) — cited ch14 | MAJOR | verify/replace |
| Placeholder entry | `shen2023nlp` (no venue, "Needs verification") — cited ch05 | MAJOR | verify/replace (ch05 T5) |
| Inline `[CHECK]`/`[CITE]` still live | `zhang2024financebench` (`% [CHECK]`), `fincen2020aml` (`% [CITE: verify…]`) | MAJOR | resolve flags |
| Metadata mismatch | `liu2018` keyed 2018 but `year = 2019` (RoBERTa); `ziemke2024temporal` author/year drift | MINOR | fix fields |
| Suspicious / likely-fabricated | `chen2025aml` — arXiv ID `2602.23373` decodes to Feb-2026 (future), inconsistent with `year=2025` (ch11) | MAJOR | `NEEDS_EXTERNAL_VERIFICATION`; likely remove |
| Possibly phantom | `kang2023hallucination` (ch13) | MINOR | `NEEDS_EXTERNAL_VERIFICATION` |
| Stale `.bib` files | `bibliography_bibertool.bib`, `bibliography_test.bib` (both present; not loaded) | MINOR | delete (human-confirmed) |
| ch16 citation-command drift | ch16 uses biblatex `\parencite/\textcite` vs `\citet/\citep` elsewhere | MINOR | unify macros |

## 2. Resolution

- **Per-chapter resolution is clean:** every chapter's cited keys resolve uniquely in
  the live `bibliography.bib` (verified per chapter: ch01 ~50, ch02 68, ch03 33, ch04 35,
  ch08 38, ch09 44, ch11 25, ch12 31, ch13 43, ch15 16, etc.). No cited-but-missing keys.
- Only `bibliography.bib` is loaded (`preamble.tex:141`).
- Full-book unresolved-`\cite` sweep deferred to `/book-quality-regression`.

## 3. Description accuracy — WRONG-PAPER findings (verified)

| Chapter:line | Key | Verdict | Detail |
|--------------|-----|---------|--------|
| ch05:645 | `frieder2023large` | **WRONG_PAPER** | entry = "LLMs and the ArXiv" (2302.00083); GPT-4 arithmetic-reliability claim belongs to "Mathematical Capabilities of ChatGPT" (2301.13867). (ch05 T4) |
| ch12:393 | `sundararajan2020shapley` | **WRONG_PAPER** | cited for Integrated Gradients, but that key is Sundararajan & Najmi 2020 "The Many Shapley Values"; IG is Sundararajan, Taly & Yan **2017** — correct ref absent from `.bib` |
| ch13:636 | `fama1970efficient` | **WRONG_PAPER** | cited for Fama–French 3-factor model; should be `fama1993common` (1970 paper is EMH) |
| ch15:136 | `touvron2023llama` | **WRONG_PAPER** | cites the original *LLaMA v1* paper for claims about *Llama 2/3/3.1* it does not cover |
| ch14:222,840 | `shah2023finer` | **LIKELY_MISATTRIBUTED** | "FINER-139" 139-tag XBRL benchmark is Loukas et al. 2022 (FiNER, ACL); `shah2023finer` is a different English/Greek FINER dataset |
| ch01:1728 | `ke2019predicting` | **MISDESCRIBED** | called "attention-based model"; it is a SESTM/topic-model paper (correct at ch01:1320). (ch01 T2) |

## 3b. Description accuracy — SUPPORTED (spot-checked, keep)

`vaswani2017attention`, `tetlock2007giving`, `loughran2011liability`, `hu2022lora`,
`wei2022chain`, `yao2022react`, `schick2023toolformer`, `LopezLiraTang2023`,
`mcmahan2017communication` / Dwork–Roth DP (ch15 math), `fama1970efficient` (ch01 EMH use — correct there).

## 4. Claims needing EXTERNAL verification (SSRN/arXiv working papers — cap citation_accuracy at 89)

Bunched by chapter — never assert until checked against the source:
- ch01: `hampole2025ai` (2%/14%), `wu2023bloomberggpt` token totals
- ch08: BloombergGPT 50B/708B/363B+345B, FinBERT F1s, FinQA/FinBen counts, RahimikiaDrinkall "50×"
- ch09: `KirtacGermano2024` Sharpe 3.05, `Siano2025` 3×/2×, FatemiHu2023, ChiuHung2024, Lehner2024, XuBabaian2025
- ch10: KirtacGermano2024 (74.4%), CoriatBenhamou2025 (HARLF 26%/Sharpe 1.2), MantshimuliMwamba2025, LopezLiraTang2023
- ch11: `chen2025aml` (+ 7 SSRN `@unpublished`)
- ch12: 8 SSRN/CFA descriptive claims
- ch13: `VidalSSRN2024` (59.4%), `kang2023hallucination` (15–30%), FinanceBench, `zhang2024financebench`
- ch07: NoguerFAIR2025, chen2024uncertainty, didisheim2025memory, BaloghDidisheim2025, FSB2024stability, LopezLira2025trade, FinanceBench "80%"
- ch15: descriptive claims verified except `touvron2023llama` (wrong paper, above)

> Section 3 is now fully populated by the per-chapter `citation-description-auditor`
> passes. Re-run `/audit-bibliography` for a fresh hygiene confirmation before release.
