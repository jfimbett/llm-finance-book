# Undefined-Terms Audit
*Generated 2026-06-18 — 17 agents, 16 chapters + cross-chapter synthesis*

---

## Reading Order (from main.tex)

Ch01 → Ch16 → Ch02 → Ch03 → Ch08 → Ch04 → Ch09 → Ch14 → Ch05 → Ch06 → Ch10 → Ch11 → Ch12 → Ch13 → Ch07 → Ch15

This matters: a "forward reference" from Ch07 to a Ch03 concept is actually fine. The issues below are ordered by reading position.

---

## CRITICAL: Cross-Chapter Clusters (never defined anywhere, or defined too late)

### Cluster 1 — Mathematical primitives with no definition anywhere in the book

| Term | First formal use | Where defined |
|------|-----------------|---------------|
| **KL divergence** KL(p ∥ q) | Ch02 Definition 2.23 (line 2120); Ch03 eq:ppo-objective | **Never** |
| **N-gram** | Ch03 ROUGE eq (line 1318) | **Never** |
| **CAPM** (as benchmark return model) | Ch09 Definition 9.3 (line 411) | **Never** |
| **Cross-entropy loss** L_CE | Ch02 Definition 2.23 (line 2118) | Ch03 Definition 3.6 (perplexity) — but used in Ch02 *first* |
| **Softmax** | Ch01 Definition 1.11 (line 1690); Ch02 Definition 2.4 | Ch02 Definition 2.15 (Temperature-Scaled Softmax) — but used much earlier |

**Fix for KL:** Add one Definition block in Ch02 before Definition 2.23: `KL(p ∥ q) = Σ_i p_i log(p_i/q_i)`.  
**Fix for N-gram:** Add one sentence before the ROUGE equation in Ch03.  
**Fix for CAPM:** Add a Remark before Definition 9.3 with the beta formula.  
**Fix for cross-entropy / softmax:** Add inline definitions at first formal use in Ch01/Ch02.

---

### Cluster 2 — Cosine similarity used before first formal definition

Cosine similarity is used technically in **Ch02** (pos 3) and **Ch04** (pos 6) but only formally defined in **Ch05 Definition 5.9** (pos 9).

**Fix:** Add `cos(a,b) = aᵀb / (‖a‖ ‖b‖)` as a named equation in Ch02 at first technical use.

---

### Cluster 3 — Vocabulary V used in 5 Ch02 definitions before Token is defined

Definitions 2.2, 2.13, 2.15, 2.18, 2.19 all use vocabulary V before Definition 2.20 (Token, line 1756).

**One-line fix:** Ch16 (pos 2, reads immediately before Ch02) formally defines vocabulary V in Definition 16.4. Add a single sentence to the Ch02 chapter preamble: *"Throughout this chapter, V denotes the token vocabulary defined in Chapter 16, Definition 16.4."* This resolves all five issues at once.

---

### Cluster 4 — SHAP/Shapley used before cooperative-game foundations

- Ch06 (pos 10): Shapley sum formula + three axioms in a formal equation block
- Ch11 (pos 12): SHAP by name
- Ch12 (pos 13): **Definition 12.2** finally gives cooperative game + characteristic function + uniqueness

**Fix:** In Ch06, before the SHAP equation, add: *"SHAP values are the unique attribution satisfying efficiency, symmetry, and dummy axioms (see Chapter 12 for the formal game-theoretic derivation)."*

---

### Cluster 5 — Sharpe ratio and Precision/Recall used before their formal definitions

| Term | First use | Formally defined |
|------|-----------|-----------------|
| Sharpe ratio | Ch01 line 613 (economic significance criterion) | Ch13 eq:ch13-sharpe-ratio |
| Precision, Recall | Ch03 Definition 3.7 (Macro-F1, line 1298) | Ch09 eq:precision-recall |

**Fix for Sharpe:** Add a parenthetical formula in Ch01 at first use.  
**Fix for Precision/Recall:** Add a two-line inline definition immediately before Definition 3.7.

---

### Cluster 6 — Intra-chapter notation collisions with book-wide impact

| Chapter | Collision |
|---------|-----------|
| **Ch07** (pos 15) | Symbol `T` = finance task (Def 7.1) AND task set (Def 7.3) AND tool layer (Def 7.4) within 30 pages |
| **Ch10** (pos 11) | Symbol `α` = CVaR confidence level (line 717) AND ARCH coefficient (line 738); acknowledged but not fixed |

**Fix Ch07:** Rename the tool layer in Definition 7.4 to Γ or Λ_T.  
**Fix Ch10:** Rename the ARCH coefficient to φ₁ throughout the GARCH subsection.

---

### Secondary Cross-Chapter Issues

| Issue | Chapter | Fix |
|-------|---------|-----|
| BM25 defined in Ch02 but used in Ch11 and Ch07 without citing the definition | Ch11 (pos 12), Ch07 (pos 15) | Add `(Chapter 2, eq:bm25)` cross-reference |
| Rényi DP / Rényi divergence used in Ch15 proof sketch, never defined anywhere | Ch15 (pos 16) | Add inline definition or remove from proof sketch |
| NER used in Ch08 formal definition (pos 5) before Ch14's treatment (pos 8) | Ch08 | Expand acronym + add cross-reference |

---

## Per-Chapter High-Severity Issues

### Chapter 1 (reading pos 1) — 4 HIGH items in Definition 1.1 alone
The canonical example reported by the user:
- **Definition 1.1**: uses `vocabulary V`, `token`, `document d_t as finite sequence`, `finite sequences of tokens` — all defined only in **Definition 1.2** (line 677, 100 lines later).
- **Definition 1.12**: uses `d_model` without introduction (defined in prose after the definition).
- **Theorem 1.1**: uses matrix spectral norm `‖·‖₂` (never defined in Ch01).

**Quickest fix for Def 1.1:** Swap order — put Definition 1.2 (Corpus and Vocabulary) *before* Definition 1.1 (Textual Signal).

---

### Chapter 2 (reading pos 3)
- **Definition 2.1**: uses word embedding φ:V→ℝᵈ before any Ch02 definition of it (requires Ch01 cross-ref).
- **Definition 2.13**: uses vocabulary V before Definition 2.20 (Token) — 600 lines earlier (see Cluster 3).
- **Definition 2.23**: KL divergence and cross-entropy undefined (see Cluster 1).
- **KV-cache**: used in prose (line 1181), never defined.

---

### Chapter 3 (reading pos 4)
- **Definition 3.2** (MinHash): uses `k-shingle` and `min-wise independent family` without definition.
- **RLHF section**: Bradley-Terry model (line 941) and `policy π_θ` in RL sense (line 951) used without introduction.
- **KL divergence** in PPO/DPO objectives (see Cluster 1).
- **Precision/Recall** in Definition 3.7 (see Cluster 5).

---

### Chapter 4 (reading pos 6)
- **Definition 4.4**: outcome space Y and lesson space L undefined.
- **Definition 4.5**: vector database and ANN search used before Section 4.4.1 defines them.
- **Definition 4.11**: query space Q undefined.
- **Definition 4.15**: cryptographic hash H undefined.
- **Symbol δ reuse**: overlap tokens (Def 4.12) vs. routing function (Def 4.10).

---

### Chapter 5 (reading pos 9)
- **DCF equations** (lines 87–100): FCF_t used before Definition 5.2 (line 320).
- **WACC**: used throughout, never formally defined.
- **Proposition 5.1**: Modigliani-Miller framework invoked without introduction.
- **Definition 5.9**: `embedding` used in formal body without definition.

---

### Chapter 6 (reading pos 10)
- CAP curve used inside a proof without prior definition.
- AUROC used in Calibration section (Def 6.2) before it is defined in Section 6.5.
- Filtration F_t notation never defined.

---

### Chapter 7 (reading pos 15) — Symbol collision cluster
- Symbol `T` used for three distinct objects across Definitions 7.1, 7.3, 7.4.
- `non-trivial classifier` undefined in Proposition 7.1 (impossibility of fairness).
- `base rates Pr(Y=1|A=a)` informally used in Proposition 7.1.

---

### Chapter 8 (reading pos 5)
- `instruction-tuned` used in Definition 8.2 without definition.
- `NER` unexpanded in formal definition block (see cross-chapter issue).
- `catastrophic forgetting` used in Definition 8.3 before the term is explained.

---

### Chapter 9 (reading pos 7)
- CAPM inside Definition 9.3 (see Cluster 1).
- Krippendorff's alpha used in Example 9.2 before its definition in Section 9.5.3.
- SUE (Standardised Unexpected Earnings) used in formal regression without formula.

---

### Chapter 10 (reading pos 11)
- `cross-sectionally demeaned` score used in Definition 10.2 without defining the operation.
- GARCH(1,1) introduced without background.
- α notation collision (see Cluster 6).
- Broken cross-reference: exercise references `sec:ch10-execution` which does not exist (should be `sec:ch10-rl-order-execution`).

---

### Chapter 11 (reading pos 12)
- λ (decay rate) undefined inside Definition 11.4.
- e_i notation collision: binary offence vector (Def 11.4) vs. embedding vector (eq:xbrl-retrieval-score).
- k notation collision: top-k retrieval (line 178) vs. RRF smoothing constant (line 184).
- BM25 used without cross-reference (see secondary cross-chapter issues).

---

### Chapter 12 (reading pos 13)
- **KernelSHAP** used in Example 12.1 (line 254) before LIME Objective (Definition 12.3, line 318).
- kernel function π_x(z) used in formal LIME definition body without definition.
- `faithful` used inside Definition 12.5 body with a narrower meaning than Definition 12.4.
- Attention weights α_ij used without transformer cross-reference.

---

### Chapter 13 (reading pos 14)
- **PEFT** inside Definition 13.3 body without definition or cross-reference.
- σ reused: softmax/sigmoid in temperature scaling (line 209) vs. portfolio std dev (line 590).
- `outcome window` in Definition 13.2 body — notation replaced by `h` only in later Definition 13.3.

---

### Chapter 14 (reading pos 8)
- `token` used heavily in NER section without definition in chapter.
- `span representation h_{e_i}` in relation extraction equation never formally defined.
- `relation embedding r` in formal equation never introduced.
- NLI never defined despite being used for FactCC faithfulness checking.

---

### Chapter 15 (reading pos 16)
- `edit distance` used in Definition 15.1 without definition.
- `adjacent datasets` ambiguity in Definition 15.4 (add/remove vs. substitute).
- Rényi DP and Rényi divergence in Proposition 15.1 proof sketch — never defined (see cross-chapter issues).
- `moments accountant` never defined.

---

### Chapter 16 (reading pos 2)
- Vocabulary, tokens used in Remark 16.0 (learning objectives, line 4) before Definition 16.4 (line 205).
- Deep learning, LLMs used in Remark 16.1 (line 61) before their definitions.
- `input space X` and `output space Y` in Definition 16.3 never declared.
- `loss function ℓ` in Definition 16.3 never declared.
- `deep reinforcement learning` in Example 16.1 never defined.
- Softmax in Deep Dive block never defined in Ch16 (defined later in Ch02).

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Cross-chapter issues (6 major clusters + secondary) | ~15 |
| Per-chapter HIGH severity issues | ~85 |
| Per-chapter MEDIUM severity issues | ~70 |
| Per-chapter LOW severity issues | ~40 |

**Top priority (fix first):**
1. Swap Def 1.1 and Def 1.2 in Ch01 (the original reported issue)
2. Add KL divergence formal definition in Ch02 before Def 2.23
3. Add Ch02 preamble cross-reference to Ch16 Def 16.4 for vocabulary V (fixes 5 issues)
4. Add Precision/Recall inline definition before Ch03 Def 3.7
5. Fix notation collision in Ch07 (T → Γ for tool layer)
6. Fix notation collision in Ch10 (α_1 → φ_1 for ARCH coefficient)
