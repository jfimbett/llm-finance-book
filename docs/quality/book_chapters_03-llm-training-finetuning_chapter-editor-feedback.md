# Editor Feedback: Chapter 3 — Training and Fine-Tuning Large Language Models

**Source:** Peer review (2026-05-31)  
**Verdict:** MAJOR_REVISION  
**Revision Round:** 1

---

## BLOCKERs

- [x] **BLOCKER-1** — Chinchilla example numerical error (`ex:chinchilla-finance`, ~lines 511-532)
  - **Problem:** States N*(1e23) ≈ 6.4e9 and D* ≈ 2.6e12 with ratio D*/N* ≈ 406. Correct values from the stated formula and constants (α=0.34, β=0.28, A=406.4, B=410.7) are N* ≈ 1.46e10, D* ≈ 1.14e12, ratio ≈ 78.
  - **Fix:** Recompute the entire example from scratch using the formula in `eq:chinchilla-Nstar`. Replace all stated numbers.

---

## MAJORs

- [x] **MAJOR-1** — "20 tokens per parameter" rule inconsistent with parametric constants (~lines 479, 526-528)
  - **Problem:** The theorem states D*/N* ≈ 20, but the parametric constants (α=0.34, β=0.28) imply D*/N* ≈ 78 at C=1e23 and ≈ 63 at C=1e22. The "~20" rule comes from the IsoFLOP approach (Approach 1), not the parametric model (Approach 3).
  - **Fix:** Distinguish the two estimation approaches. Either derive the ratio from the parametric constants (≈60–80) or attribute "~20" to the IsoFLOP approach with a note that both approximate the same phenomenon.

- [x] **MAJOR-2** — Incorrect BERT citation (line 412)
  - **Problem:** "MLM, used by BERT \cite{yang2020finbert}" — `yang2020finbert` is FinBERT (Yang et al., 2020), not the original BERT paper.
  - **Fix:** Replace `\cite{yang2020finbert}` with `\cite{devlin2018bert}` (Devlin, Chang, Lee, Toutanova 2018/2019) at line 412. If the key `devlin2018bert` is not in the bibliography, add it.

- [x] **MAJOR-3** — BloombergGPT corpus size error (~line 1078)
  - **Problem:** "trained on a 363-billion-token corpus" — this omits the ~345B general tokens from The Pile. Total is ~708B tokens (51% finance / 49% general).
  - **Fix:** Change to "approximately 708-billion-token corpus" and reconcile the Pile figure in Table `tab:bloomberggpt-corpus` (text says 345B, table says 343B — use the paper's figure).

---

## MINORs

- [x] **MINOR-1** — Missing closing synthesis paragraph
  - **Problem:** Chapter ends abruptly after the governance framework with no conclusion.
  - **Fix:** Add a one-paragraph conclusion drawing together pre-training, fine-tuning, evaluation, and governance themes.

- [x] **MINOR-2** — Evaluation section context box too short (~lines 1188-1198)
  - **Problem:** The context box is only 9 lines and does not adequately frame the evaluation landscape.
  - **Fix:** Expand the context box to 15–20 lines with more substantive framing of the evaluation landscape before the technical metrics.

- [x] **MINOR-3** — In-context learning sentence lacks citations (~line 729)
  - **Problem:** "The mechanism is not fully understood theoretically" — accurate but would benefit from 1–2 theoretical citations.
  - **Fix:** Cite Xie et al. (2022) and/or Akyürek et al. (2022) for theoretical perspectives on ICL.

- [x] **MINOR-4** — Gradient checkpointing notation footnote

---

## Revision Round 2 (2026-06-01 — from full-review critique + peer review)

### BLOCKERs

- [x] **BLOCKER-2** — FinBERT vocabulary modification claim is false (`subsec:finbert`, ~line 1034)
  - **Problem:** "modified the BERT vocabulary to include financial terms" — Yang et al. (2020) FinBERT uses the original BERT-large WordPiece vocabulary unchanged; only weight updates, not vocabulary expansion.
  - **Fix:** Remove the vocabulary modification sentence or rephrase to note only weight updates occur.

- [x] **BLOCKER-3** — Financial PhraseBank misattributed (`subsec:domain-adaptation`, ~line 995)
  - **Problem:** `\cite{yang2020finbert}` cited as the source of Financial PhraseBank — dataset was created by Malo et al. (2014), not Yang et al.
  - **Fix:** Add `malo2014financial` bibliography entry; replace the cite key.

- [x] **BLOCKER-4** — GPT-3 "57% training time" contradicts table (`subsec:text-corpora`, ~lines 106–108)
  - **Problem:** Text says Common Crawl = "60% of training tokens but only 57% of training time" — table directly below shows 60% sampling weight, contradicting 57%.
  - **Fix:** Remove the 57% figure and the false distinction; state "60% sampling weight" consistent with the table.

### MAJORs

- [x] **MAJOR-4** — Chinchilla figure-caption exponents inconsistent with theorem constants (`fig:ch03-illustration`)
  - **Problem:** Figure caption uses $N^* = 0.1192 C^{0.4937}$ (IsoFLOP/Approach 1) while theorem uses parametric constants implying exponent ≈ 0.452. No explanation given.
  - **Fix:** Add a sentence noting the figure uses the IsoFLOP power-law fit (Approach 1) from Hoffmann et al. and that it differs from the parametric (Approach 3) result used in the theorem.

- [x] **MAJOR-5** — ZeRO memory reduction factors stated without assumptions (~lines 585–595)
  - **Problem:** "4× memory reduction" (ZeRO-1) and "8× reduction" (ZeRO-2) stated without derivation or assumptions (Adam, fp32, large K).
  - **Fix:** Qualify as "up to 4×" and "up to 8×" and note they apply under Adam with fp32 master weights for large K.

- [x] **MAJOR-6** — PPO objective sign convention (eq:ppo-objective, ~lines 918–924)
  - **Problem:** `\mathcal{L}` notation implies minimization but the equation as written is a quantity to maximize.
  - **Fix:** Rename to `\mathcal{J}_{\mathrm{PPO}}` and state it is maximized, or negate and note it is minimized.

- [x] **MAJOR-7** — "Bloomberg estimates...0.5%" uncited (~lines 139–142)
  - **Problem:** Precise quantitative claim attributed to Bloomberg with no citation.
  - **Fix:** Cite `wu2023bloomberggpt` or rephrase as an order-of-magnitude estimate without attribution.

- [x] **MAJOR-8** — GPT-4 "1.8T parameters" stated as fact without qualification (ex:ch03-illustration, ~line 673)
  - **Problem:** Unverified figure from informal sources presented as ground truth.
  - **Fix:** Add qualifier: "widely-cited but unconfirmed estimate of ~1.8T parameters."

### MINORs

- [x] **MINOR-5** — GPT-3 table sampling weights sum to 101% (tab:gpt3-corpus)
  - **Fix:** Adjust one weight (e.g., Common Crawl 60%→59%) or add footnote noting rounding.

- [x] **MINOR-6** — LoRA missing scaling factor α/r in definition and forward pass (~lines 769, 786)
  - **Fix:** Add `(α/r)` scaling to eq:lora and the forward-pass line; mention α as a second hyperparameter.

- [x] **MINOR-7** — ROUGE formula double-summation notation ambiguous (eq:rouge, ~line 1293)
  - **Fix:** Replace with single-summation standard form summing over n-grams directly.

- [x] **MINOR-8** — "BloombergGPT architecture uses the BLOOM architecture" misleading (~line 1130)
  - **Fix:** Rephrase to "BloombergGPT adopts ALiBi positional encodings from the BLOOM model family."
  - **Problem:** The O(√L · T · d) formula assumes checkpointing only at layer granularity — not stated.
  - **Fix:** Add a brief footnote clarifying that the √L bound assumes optimal checkpoint placement at layer granularity.
