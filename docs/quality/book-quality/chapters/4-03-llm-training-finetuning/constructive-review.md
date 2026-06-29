# Constructive Review — Ch 03 (reading index 4): Training and Fine-Tuning

Scope: `book/chapters/03-llm-training-finetuning/chapter.tex` (1646 lines). Audit only.

This chapter is the natural single source of truth for the training/fine-tuning/
LoRA/RLHF/scaling/evaluation/governance stack of the book. The treatment is strong,
quantitatively grounded, and consistently finance-first. Below: what to preserve.

## KEEP_AS_SINGLE_SOURCE_OF_TRUTH

- **Chinchilla scaling laws + proof** (`:454`–`:506`, `thm:chinchilla`). Full derivation
  from `C=6ND` constraint with FOC, fitted constants, and the careful disambiguation
  between the parametric (Approach 3) ratio ~78 and the IsoFLOP "20 tokens/param"
  (Approach 1) heuristic (`:470`–`:476`). This is the book's SSOT for scaling; the
  honesty about the two-approach discrepancy is exemplary. `KEEP_AS_SINGLE_SOURCE_OF_TRUTH`.
- **RLHF three-stage pipeline** (`:900`–`:937`): SFT → Bradley-Terry reward model
  (`eq:reward-model`) → PPO with KL penalty (`eq:ppo-objective`). Policy/environment
  framing inline-defined. SSOT for RLHF. `KEEP_AS_SINGLE_SOURCE_OF_TRUTH`.
- **DPO derivation** (`:939`–`:961`, `eq:dpo-reward`→`eq:dpo`): partition-function
  cancellation explained correctly. SSOT for DPO. `KEEP_AS_SINGLE_SOURCE_OF_TRUTH`.
- **PEFT family** (`:771`–`:865`): LoRA (`def:lora`), prefix tuning, adapters, with the
  `rem:peft-comparison` trade-off box. SSOT for the *full* PEFT comparison (ch02 has a
  shorter LoRA definition — see skeptical review for the collision). `KEEP_AS_SINGLE_SOURCE_OF_TRUTH`.
- **Perplexity / cross-entropy** (`:1228`–`:1261`, `def:perplexity`) and **Macro-F1 /
  ROUGE** (`:1272`–`:1308`). Clean, correct metric definitions. SSOT for evaluation metrics.

## GOOD_TECHNICAL_EXPLANATION

- ZeRO stages 1/2/3 with byte-accounting (`:574`–`:594`); the explicit
  "16 bytes/param = 4+4+8" baseline makes the memory reductions concrete and correct.
- Distributed-training memory motivation (`:542`–`:547`): 7B model → 112 GB under fp32
  Adam, derived line by line. Excellent setup for why parallelism is needed.
- Mixed precision / loss scaling / gradient checkpointing $O(L)\to O(\sqrt L)$ (`:603`–`:634`),
  with a precise footnote on the optimal-checkpoint assumption.
- BPE (`def:bpe`) and MinHash/Jaccard (`def:minhash`, `eq:minhash`) with the unbiased-
  estimator variance $J(1-J)/m$ (`:296`–`:303`). Correct and well-pitched.

## GOOD_FINANCE_EXAMPLE

- `ex:chinchilla-finance` (`:508`–`:529`): applies the scaling law to a concrete
  $10^{23}$ FLOPs financial-LLM budget and reasons about the 100B-token data
  constraint. Reader can act on it. `GOOD_FINANCE_EXAMPLE`.
- `ex:lora-sentiment` (`:808`–`:821`): LoRA param-count arithmetic for a 7B LLaMA
  (8.39M trainable, 0.12%), with a 90-min-vs-40-hr cost contrast. `GOOD_FINANCE_EXAMPLE`.
- `ex:two-stage-adaptation` (`:992`–`:1006`): DAPT → Financial PhraseBank fine-tuning
  with explicit, honestly hedged accuracy figures ("exact figures vary…", `:1005`).
- BloombergGPT corpus table `tab:bloomberggpt-corpus` (`:1095`) and the
  under-training-vs-Chinchilla tension discussion (`:1113`–`:1121`). `GOOD_FINANCE_EXAMPLE`.
- FinGPT-under-$300 / FinLLaMA / InvestLM / PIXIU-FinMA citations woven into the data
  and instruction-tuning narrative (`:165`–`:168`, `:890`–`:898`, `:1178`–`:1184`).

## GOOD_BIG_PICTURE_EXPLANATION

- Opening `context` on "every capability is a function of what it has read" (`:31`–`:53`)
  and the four-stage pipeline framing. `GOOD_BIG_PICTURE_EXPLANATION`.
- The Chinchilla `deepdive` narrative opening (`:354`–`:366`) — story-driven motivation.
- Closing synthesis paragraph (`:1628`–`:1642`): ties pre-training → fine-tuning →
  evaluation → governance into one dependency chain. `KEEP`.
- The `context`/`deepdive` box architecture is used deliberately throughout: each
  section pairs a big-picture `context` opener with an under-the-hood `deepdive`.
  This is the model the rubric wants for concept_separation. `KEEP`.

## Finance orientation

Finance-first framing is consistent: temporal/look-ahead bias (`rem:temporal-alignment`),
survivorship/temporal/geographic/analyst-consensus bias (`:1446`–`:1472`), MiFID II
Article 37 research independence (`:1433`, `:1537`), SR 11-7, SEC Rule 17a-4, EU AI Act
Annex III (`rem:eu-ai-act`). Real out-of-sample finance evidence: López-Lira & Tang
Sharpe-decay (`:1407`–`:1414`) and Balogh-Didisheim inverted-U information overload
(`:962`–`:967`). `GOOD_FINANCE_EXAMPLE`.

## DO_NOT_CHANGE

- The two-approach Chinchilla hedging (`:470`–`:476`, `:521`–`:525`, fig caption `:654`–`:667`).
  It is correct and unusually careful — do not "simplify" it into the 20:1 heuristic.
- All hedged empirical figures ("for illustration", "typical … range", "vary with corpus,
  hardware, and seed"). These are responsible and rubric-aligned.
