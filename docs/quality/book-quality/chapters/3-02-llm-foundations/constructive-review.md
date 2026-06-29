# Constructive Review — Chapter 3 (reading order) · `02-llm-foundations`

Audit date: 2026-06-20 · Scope: chapter · Auditor: constructive-reviewer
File: `book/chapters/02-llm-foundations/chapter.tex`

This chapter is the technical-and-practical spine of the book. It contains a large amount
of high-quality, release-grade material that the editor MUST protect. Tags follow the
RUBRIC §4 preservation vocabulary.

## KEEP_AS_SINGLE_SOURCE_OF_TRUTH

- **Scaled dot-product attention** — `chapter.tex:787-808` (Def `def:scaled-dot-product-attn`,
  eq `eq:scaled-dot-product`). Clean, correct, complete. This chapter is the *designated*
  SSOT for attention internals. KEEP — but see skeptical-review: ch01 currently re-derives
  the same content and collides on labels; the resolution is to thin ch01, not to move this.
- **√d_k variance normalisation** — `chapter.tex:818-827` (Prop `thm:sqrt-dk-scaling`,
  eq `eq:dot-product-var`). The Var = d_k result is correctly stated under the i.i.d.
  unit-variance assumption. KEEP_AS_SINGLE_SOURCE_OF_TRUTH.
- **Multi-head attention** — `chapter.tex:844-857` (Def `def:mha`, eq `eq:multihead`).
  Correct; original-Transformer constants (h=8, d_model=512, d_k=d_v=64) accurate. KEEP.
- **Causal mask** — `chapter.tex:829-838` (eq `eq:causal-mask`). Reused correctly later by
  CLM (`eq:clm-loss`, line 1055). KEEP.
- **Sinusoidal positional encoding + relative-position linearity proof** —
  `chapter.tex:889-943` (Def `def:positional-encoding`, Prop `thm:pe-relative`). The rotation
  matrix proof is correct and elegant. GOOD_TECHNICAL_EXPLANATION / KEEP.
- **LSTM cell-state / constant-error-carousel argument** — `chapter.tex:454-505`
  (Def `def:lstm`, eq `eq:lstm-cell`, eq `eq:lstm-cellgrad`). Correctly explains *why* the
  additive path mitigates (not eliminates) vanishing gradients, with the saturating-forget-gate
  caveat. KEEP — but ch01 holds colliding copies of these exact labels (skeptical-review BLOCKER).
- **Vanishing/exploding-gradient bound** — `chapter.tex:407-429` (Prop `thm:vanish-explode`,
  eq `eq:vanish-bound`). Bound and M_σ values (1/4 sigmoid, 1 tanh) correct. KEEP.

## KEEP_AS_SINGLE_SOURCE_OF_TRUTH (production internals)

- **Temperature-scaled softmax + entropy monotonicity** — `chapter.tex:1452-1486`
  (Def `def:temperature`). Correct; the τ→0 / τ=1 / τ→∞ limits are accurately characterised.
- **Top-k / nucleus (top-p) sampling** — `chapter.tex:1497-1531` (Def `def:topk`,
  `def:nucleus`). Correct, and the ρ-vs-p_i notation clash is explicitly disambiguated
  (line 1518). GOOD_TECHNICAL_EXPLANATION.
- **Knowledge distillation incl. forward-vs-reverse-KL remark** — `chapter.tex:2126-2163`
  (Def `def:kd`, Remark `rem:kd-kl-direction`). The τ² gradient-rescaling and mean-seeking
  argument are correct and unusually careful. KEEP.
- **LoRA / QLoRA** — `chapter.tex:2183-2207` (Def `def:lora`). The 4096×4096, r=16 →
  16.8M→131K (128×) arithmetic checks out. KEEP.
- **Constrained decoding validity mask** — `chapter.tex:1655-1675` (Def `def:validity-mask`).
  Pre-softmax −∞ masking explained correctly. KEEP.

## GOOD_FINANCE_EXAMPLE

- **Merger valuation: generative vs reasoning model** — `chapter.tex:1243-1272`
  (`ex:merger-valuation`). Concrete TechCo numbers, EV/EBITDA ≈ 13.5× is correct
  (4.2B / 310M). Excellent illustration of the reasoning-model value-add. KEEP.
- **FinBERT: two distinct models** — `chapter.tex:1084-1101` (`ex:finbert`). Valuable,
  correctly disambiguates Araci-2019 vs Huang-2023 FinBERT — a frequent literature confusion.
  GOOD_FINANCE_EXAMPLE / KEEP.
- **Cost worked example (10k transcripts, GPT-4o ≈ $410 vs Haiku ≈ $20)** —
  `chapter.tex:1910-1918`. Numbers tie back to Example `ex:bpe` (1.3 tok/word) and
  `eq:cost-model`. KEEP.
- **FinanceBench 81% failure stat** — `chapter.tex:2091-2096` (`zhang2024financebench`).
  Strong, sobering, well-integrated finance grounding for RAG limits. KEEP.
- **Hallucination example (D/E 1.8→0.8 inversion; fabricated PCAOB report)** —
  `chapter.tex:2303-2314` (`ex:hallucination`). Crisp intrinsic-vs-extrinsic contrast. KEEP.

## GOOD_BIG_PICTURE_EXPLANATION

- **`context`-box openers** on landscape (1154), sampling-finance (1569), structured-gen
  (1634), API (1756), RAG (1956), hallucinations (2261), limitations (2441). These narrative
  hooks are well-pitched for the mixed academic/industry audience and cleanly separated from
  the `deepdive` math. KEEP — exemplary use of the context/deepdive separation.
- **Sampling-strategy selection table** — `chapter.tex:1582-1617` (`tab:sampling-strategies`).
  Actionable per-task τ/sampling guidance. GOOD_FINANCE_EXAMPLE / KEEP.

## KEEP_BUT_CLARIFY

- **`illustration` env for positional encoding** — `chapter.tex:1136-1149`
  (`ex:ch02-illustration`) points to `exercises.ipynb` (22 cells, real, PE + cosine present).
  KEEP — wiring is good; just confirm figure regeneration path in the notebook header.

## Cross-reference integrity worth preserving

- Notation-inheritance remarks (`rem:ch2-notation` line 37; d_model note line 246) are a good
  practice — KEEP, but convert the hard-coded "Chapter~1" to `\Cref{ch:intro}` (see editor-plan).
