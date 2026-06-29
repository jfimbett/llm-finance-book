# REPETITION_MAP.md

> Single-source-of-truth (SSOT) assignments for concepts that recur across chapters.
> Goal (`RUBRIC.md` dim 6 `non_repetition`): each concept has **one** chapter that
> derives it; later chapters give a short reminder + `\Cref`, not a re-derivation.
> Keyed to reading order. **Status: 2026-06-20 audit + 2026-06-26 reorder/dedup pass.**
>
> **2026-06-26 updates (verified against live sources):**
> - All duplicate `\label`s from the 2026-06-20 collision list are now unique
>   (def:lstm, def:mlm, eq:cosine-sim, def:lora, eq:lora, def:rag, eq:multihead, def:calibration).
> - **SHAP/Shapley SSOT reassigned to ch12 (XAI), the dedicated chapter.** ch06's
>   `subsec:shap-credit` now keeps only the applied *efficiency* property
>   (`eq:shap-efficiency`) + the credit waterfall, and forward-refs the full derivation
>   to `def:shapley-value`/`eq:shapley-value` in `\Cref{ch:xai-explainability}`.
>   The old full re-derivation `eq:shap` in ch06 was removed.
> - Agentic primitives (agent/skill/hook) introduced once in ch04
>   `subsec:file-based-pattern` (concrete file format) and engineered, not re-derived, in
>   ch17 (`\Cref{ch:llm-agents}` bridge at chapter top).
> - Calibration: ch06 owns PD-calibration + Platt/TTC; ch13 owns the general
>   ECE/reliability criterion; both cross-reference each other (intentional split, not a
>   re-derivation).

## SSOT table (verified)

| Concept | Re-derived in (read#) | **Designated SSOT** | Later chapters should | Label collision (confirmed) |
|---------|------------------------|---------------------|------------------------|------------------------------|
| RNN / LSTM | #1 (ch01), #3 (ch02) | **#3 ch02** | ch01 → intuition `context` box + `\Cref` | `def:lstm` ch01:1584 ⇄ ch02:455; `eq:rnn-jacobian` ch01:1533 ⇄ ch02:402 |
| Attention / scaled dot-product / √d_k | #1 (ch01 full proof), #3 (ch02 full) | **#3 ch02** | ch01 → preview only + `\Cref` | `eq:multihead` ch01:1710 ⇄ ch02:854 |
| MLM objective | #1 (`def:mlm`), #4 (ch03) | **#3 ch02 owns; #4 reminds** | ch01 → `\Cref` | `def:mlm` ch01:1786 ⇄ ch03:389 |
| Cosine similarity | #1, #3, #9 | **#1 ch01** | ch02/ch05 → `\Cref` | `eq:cosine-sim` ch01:868 ⇄ ch02:2004 ⇄ ch05:926 (×3) |
| LoRA / PEFT | #3 (ch03), #5/#10 reuse, #10 re-derives | **#4 ch03** | ch02/ch06 → `\Cref`, no re-derivation | `def:lora` ch02:2184 ⇄ ch03:781; `eq:lora` ch02:2189 ⇄ ch03:786 ⇄ ch06:299 (×3). NOTE: ch02 & ch03 formulas **disagree** ($W_0+BA$ vs $W_0+\frac{\alpha}{r}BA$) — reconcile on the ch03 form |
| RAG | #3 (ch02 def), #6 (ch04 def), #15 (ch07 reuse) | **#6 ch04** | ch02 → `\Cref`; ch07 → reminder + `\Cref` | `def:rag` ch02:1972 ⇄ ch04:763 (two competing definitions: pipeline vs marginalization view) |
| ReAct loop | #6 (ch04), #9 (ch05) | **#6 ch04** | ch05 → reminder + `\Cref{ch:llm-agents}` (partly bridged) | — (ch04 `def:react-trajectory` is unique) |
| SHAP / Shapley attribution | #10 (ch06 full), #13 (ch12 full) | **#10 ch06** (earliest full derivation) | ch12 → `\Cref` + add forward-ref from ch06; ch11 already defers | — (no shared label, but full re-derivation) |
| Calibration (PD / ECE / reliability) | #10 (ch06 `def:calibration`), #14 (ch13 `def:ch13-perfect-calibration` + Platt/isotonic/ECE) | **#10 ch06** | ch13 → `\Cref`, drop the parallel definition | `def:calibration` ch06:382 ⇄ ch07:400 — **but these are DIFFERENT concepts** (ch06 PD-calibration vs ch07 fairness "calibration within group"); ch07 must **rename its label**, not merge |
| Backtesting / walk-forward | #11 (ch10) | **#11 ch10** | ch13 → `\Cref` | — (verified single-source: mean-variance/BL/CVaR all ch10-only) |
| GDPR (Arts 5/17/22) + MiFID II record-keeping | #12 (ch11), #16 (ch15) | **#12 ch11** | ch15 → `\Cref` | — (different bib keys `euaiact2024` vs `gdpr2016` — unify) |
| Open-weight models / quantisation (Llama/Mistral, GGUF, Ollama, QLoRA) | #16 (ch15), Appendix C | **Appendix C** (hands-on) | ch15 → `\Cref` | — |
| Sentiment lexicon (Loughran–McDonald) founding result | #1, #5 (ch08), #7 (ch09), #2 (ch16) | **#1 ch01** (motivation) | ch09/ch16 → `\Cref`, no re-narration | — |
| FinBERT / SEC-BERT / Financial PhraseBank | #5 (ch08), #7 (ch09) | **#5 ch08** | ch09 → trim to sentiment-specific delta + `\Cref` | — |
| Tetlock WSJ negativity example | #1, #7, #2 | **#1 ch01** | ch09/ch16 → brief recall + `\Cref` | — |

## Rules for converting a repetition into a reminder

1. Keep the **finance motivation** local (it is chapter-specific and not repetition).
2. Replace the *derivation/proof/definition* with: one or two sentences of intuition +
   `\Cref{ch:SSOT}` (or `\Cref{def:...}`/`\eqref{eq:...}`).
3. Remove the now-duplicate `\label` so cross-refs resolve to the SSOT only.
4. **Exception (calibration):** ch06 and ch07 share `def:calibration` for two *different*
   concepts — do NOT merge; rename ch07's fairness label (e.g. `def:fairness-calibration`).
5. Verify with `/audit-cross-refs` and a compile after each removal.

## Confirmed duplicate `\label`s (grep, 2026-06-20)

```
def:lstm          ch01:1584   ch02:455
eq:rnn-jacobian   ch01:1533   ch02:402
eq:multihead      ch01:1710   ch02:854
def:mlm           ch01:1786   ch03:389
eq:cosine-sim     ch01:868    ch02:2004   ch05:926
def:lora          ch02:2184   ch03:781
eq:lora           ch02:2189   ch03:786    ch06:299
def:rag           ch02:1972   ch04:763
def:calibration   ch06:382    ch07:400   (different concepts — rename, don't merge)
```

(Also expect `eq:lstm-{forget,input,candidate,cell,output,hidden}` collisions ch01⇄ch02
from the same RNN/LSTM duplication — confirm during the ch01/ch02 fix.)
