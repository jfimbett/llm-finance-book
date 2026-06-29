# Constructive Review — Ch. 13 (read #14) LLM Limitations and Rigorous Evaluation

Scope: `book/chapters/13-llm-limitations-evaluation/chapter.tex`. Audit only.

This is one of the strongest chapters in the book on a per-section basis: it is
finance-first, methodologically rigorous, and densely (and accurately) cited. The
content below is correct and worth protecting.

## Keep as single source of truth

- **KEEP_AS_SINGLE_SOURCE_OF_TRUTH** — Temporal leakage / contamination taxonomy,
  `sec:ch13-temporal-leakage` (lines 244–412). The three-channel memorisation taxonomy
  (direct, indirect via outcome narratives, statistical bias; lines 272–285), the
  contamination-resistant temporal split (`def:ch13-temporal-split`, lines 348–360),
  and the contamination-audit worked example (`ex:ch13-contamination-audit`, lines
  390–412) are the book's authoritative treatment of look-ahead bias for LLMs. No other
  chapter covers this; this is genuinely novel material.

- **KEEP_AS_SINGLE_SOURCE_OF_TRUTH** — Hallucination taxonomy for finance,
  `sec:ch13-hallucination-financial-contexts` (lines 742–877): fabricated citations,
  incorrect numerical facts, phantom companies/executives, anachronistic facts (lines
  755–789). The grounding strategies (RAG, retrieval verification, tool use,
  self-consistency; lines 791–845) and benchmarks (FinanceBench, FinQA; lines 847–877)
  are well-organised and correctly cited.

- **KEEP_BUT_CLARIFY / KEEP_AS_SINGLE_SOURCE_OF_TRUTH (with caveat)** — Calibration
  section `sec:ch13-calibration-overconfidence` (lines 22–241). The ECE/MCE machinery
  (eqs. `eq:ch13-ece`, `eq:ch13-mce`), the RLHF/token-vs-claim/distribution-shift
  decomposition of LLM overconfidence (lines 144–164), and the recalibration menu are
  excellent. **Caveat:** ch06 (`def:calibration`) already defines perfect calibration,
  reliability diagrams, Platt scaling, isotonic regression, and ECE — and ch06 is read
  FIRST (position 10 vs 14). See skeptical/editor reports: this section should be the
  declared SSOT and ch06 should cross-reference it, OR this section should defer to ch06.
  Either way the duplication must be reconciled, not left as two parallel definitions.

## Good technical explanations

- **GOOD_TECHNICAL_EXPLANATION** — Token-level vs claim-level confidence (lines 151–157):
  precise, non-obvious, and exactly the kind of under-the-hood point the audience needs.
- **GOOD_TECHNICAL_EXPLANATION** — Walk-forward / expanding-window / purge period with
  `def:ch13-walk-forward` (lines 642–682). Cleanly ties the purge gap back to
  `def:ch13-temporal-split`.
- **GOOD_BIG_PICTURE_EXPLANATION** — EMH / Grossman-Stiglitz framing of the information
  barrier (lines 429–472), including the three channels where LLMs may still add value.
  This is the correct economic frame and stops the chapter from being naive techno-optimism.

## Good finance examples

- **GOOD_FINANCE_EXAMPLE** — `ex:ch13-ece-credit` (lines 91–128): worked ECE on a credit
  classifier; arithmetic verified (ECE = 0.115, bins sum to 1000). One display typo only
  (see skeptical report, line 118).
- **GOOD_FINANCE_EXAMPLE** — `ex:ch13-contamination-audit` (lines 390–412): 13-gram
  membership check + anonymisation ablation dropping accuracy 62%→54%. Concrete,
  reproducible-in-spirit, and lands the chapter's central methodological lesson.
- **GOOD_FINANCE_EXAMPLE** — Trading-grade evaluation checklist (lines 730–739) and the
  transaction-cost / capacity / drawdown formulas (`eq:ch13-transaction-cost`,
  `eq:ch13-max-drawdown`): actionable, finance-grounded.

## Citation strengths

- The SSRN finance-evaluation literature is unusually well integrated and current:
  `LopezLiraTang2023`, `LopezLiraTangZhu2025`, `RahimikiaDrinkall2024`,
  `GaoJiangYan2025`, `ChenGreenGulenZhou2024`, `VidalSSRN2024` all resolve and are
  described in a way consistent with their titles. This is a model for the rest of the book.

## Pedagogy

- **KEEP** — Learning objectives (lines 4–19) are specific and measurable; the Summary
  (lines 880–928) maps one-to-one onto the five sections; Further Reading (lines 931–976)
  is curated, not padded. Strong scaffolding for the mixed academic/industry audience.
