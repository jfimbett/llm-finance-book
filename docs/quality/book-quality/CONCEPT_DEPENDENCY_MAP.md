# CONCEPT_DEPENDENCY_MAP.md

> Concept introduction/definition map keyed to **`main.tex` reading order**.
>
> **Current reading order (2026-06-26 reorder into 6 \part divisions):**
> `01 → 16 → 02 → 03 → 08` (Part I Foundations) `→ 04` (Part II Agents/Tools/Skills)
> `→ 09 → 14` (Part III Financial Text) `→ 05 → 06 → 10` (Part IV Quant Apps)
> `→ 11 → 12 → 13 → 15` (Part V Trust/Governance) `→ 17 → 07` (Part VI Engineering & Outlook).
>
> Reorder changes vs. the 2026-06-20 order: ch07 (synthesis) moved to last; ch15 before
> ch17; ch11 leads Part V; ch17 (loops/goals/iterations) now sits **after** its credit-risk
> (#10), regulation (#12), and evaluation (#14) prerequisites. Agentic primitives are now
> introduced concretely (file format) in ch04 `subsec:file-based-pattern` and engineered in
> ch17. The table below uses the OLD reading indices for the historical audit; re-verify
> "used before defined" flags against the current order before acting on them.
> **Status: table verified 2026-06-20; order header updated 2026-06-26.**

| Concept | First used (read#) | First properly defined (read#) | Used before defined? | SSOT / Notes |
|---------|--------------------|--------------------------------|----------------------|--------------|
| AI/ML/DL hierarchy | #2 (ch16) | #2 (ch16) | No | ch16 is de-facto overview |
| NLP / text-as-data | #1 (ch01) | #2/#7 | Borderline | introduced ch01, deepened later |
| Tokens / tokenization | #1 (ch01) | #3 (ch02) | Minor | BPE/SentencePiece in ch03/ch08 |
| Embeddings | #1 (ch01) | #1–#3 | No | re-defined again ch05 (redundant) |
| Cosine similarity | #1 (ch01) | #1 (ch01) | No | **SSOT = #1; redefined #3,#9 w/ colliding `eq:cosine-sim`** |
| Attention | #1 (ch01 preview) | #3 (ch02, full) | No | **SSOT = #3 (ch02); ch01 should be intuition-only** |
| Transformers | #1 (ch01) | #3 (ch02) | No | SSOT = #3 |
| RNN / LSTM | #1 (ch01, full) | #1 and #3 | No | **Duplicated #1⇄#3; SSOT = #3; `def:lstm` collides** |
| Vanishing gradient / √d_k proof | #1 (ch01) | #1 and #3 | No | **Duplicated proofs #1⇄#3; SSOT = #3** |
| Pretraining (CLM/MLM) | #1 (ch01 `def:mlm`) | #3 (ch02) | Minor | **`def:mlm` collision ch01⇄ch03** |
| softmax | #1 (ch01:1167) | #1 (ch01:1652, inline) | **Yes (local)** | used ~480 lines before definition |
| cross-entropy | #1 (ch01 losses) | never named in ch01 | **Yes** | AR/MLM losses are cross-entropy but unnamed |
| KL divergence | #4 (RLHF/DPO) | late | Borderline | name at first use |
| Scaling laws (Chinchilla) | #4 (ch03) | #4 (ch03) | No | — |
| Fine-tuning / PEFT / LoRA | #3 (ch02 mention), #4 (ch03) | #4 (ch03) | No | **re-derived #10 (ch06); SSOT = #4; `eq:lora` ×3** |
| Instruction tuning / RLHF / DPO | #4 (ch03) | #4 (ch03) | No | ch03 confirmed SSOT |
| Domain LLMs (BloombergGPT/FinBERT) | #5 (ch08) | #5 (ch08) | No | **SSOT = #5; ch09 re-narrates FinBERT** |
| Agents / tool use / ReAct | #6 (ch04) | #6 (ch04) | No | **re-introduced #9 (ch05); SSOT = #6** |
| RAG | #3 (ch02 def), #6 (ch04 def) | #6 (ch04) | Minor | **Defined twice #3⇄#6 (`def:rag` collision); SSOT = #6; reused #15** |
| Sentiment analysis | #1/#2 | #7 (ch09) | No | founding results SSOT = #1; method SSOT = #7 |
| Summarization metrics (ROUGE/BERTScore) | #8 (ch14) | #8 (ch14) | No | **SSOT = #8; ch13 should `\Cref`** |
| CAPM | #7 (ch09:411, inline) | **never properly** | **Yes** | needed for WACC at #9; define a SSOT |
| Valuation / DCF / WACC | #9 (ch05) | #9 (ch05) | **WACC never derived** | orphaned `valuation_example/` supplies CAPM r_E≈9.48%, WACC≈9.27% |
| Credit risk (Merton/reduced-form) | #10 (ch06) | #10 (ch06) | No | self-contained |
| AUROC / KS / Gini | #10 (ch06:379) | #10 (ch06, later) | No (forward-pointer present) | **self-contained in ch06; NOT SSOT'd in ch13** |
| Calibration (ECE/reliability) | #10 (ch06) | #10 (ch06 `def:calibration`) | No | **SSOT = #10; ch13 re-defines (`def:ch13-perfect-calibration`); ch07 reuses label for a different concept** |
| Asset pricing / mean-variance / BL / CVaR | #11 (ch10) | #11 (ch10) | No | **verified single-source (not in ch05/ch06/ch13)** |
| Regulatory (EU AI Act, SR 11-7, GDPR, MiFID) | #1 (scattered) | #12 (ch11) | Scattered | **GDPR/MiFID re-introduced #16 (ch15); SSOT = #12** |
| Explainability / SHAP | #10 (ch06, full) | #10 (ch06) | No | **SSOT = #10; ch12 (#13) re-derives in full; ch11 defers** |
| Integrated Gradients | #13 (ch12) | #13 (ch12) | No | cited to WRONG paper (`sundararajan2020shapley`) — see citation audit |
| Hallucination taxonomy | #1 (mention) | #14 (ch13) | Borderline | early mention, late rigor |
| Privacy / DP / de-identification | #16 (ch15) | #16 (ch15) | No | last chapter; math verified vs Dwork–Roth |

## Priority use-before-definition flags (verified)

1. **WACC/CAPM** — used in ch05 (#9) 36+ times but never derived; CAPM only an inline
   stray at ch09:411 (#7), never referenced. **Highest-leverage ordering gap.**
2. **cross-entropy / softmax** — used in ch01 before being named/defined (local).
3. **Calibration owner conflict** — ch06 (#10) owns it; ch13 (#14, intended SSOT)
   re-defines it; ch07 (#15) reuses `def:calibration` for a *different* fairness concept.
4. **Roadmap drift** — ch02 `tab:roadmap` (line 2563) and ch07 `tab:chapter-map` (56–82)
   describe a stale, pre-reorder chapter structure that contradicts `main.tex`.

## Resolved / non-issues found by the full audit (previously suspected)

- **AUROC is NOT used before definition** — ch06 defines it internally with a forward-pointer.
- **Backtesting is single-source in ch10** — not duplicated in ch13.
- **Mean-variance/Black–Litterman/CVaR** are single-source in ch10.
