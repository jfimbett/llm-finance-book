# Peer Review: "Training and Fine-Tuning Large Language Models"
## Chapter 3 — *Large Language Models in Finance*

**Reviewer:** Anonymous  
**Date:** 2026-05-31  
**Submission type:** Book chapter (academic monograph)  
**Verdict:** MAJOR_REVISION

---

## 1. Significance

The chapter addresses a topic of genuine and growing importance: how LLMs are
trained, adapted, and evaluated, with particular attention to financial
applications where domain adaptation, regulatory compliance, and bias mitigation
are first-order concerns. The scope is appropriate for the stated audience
(researchers, students, engineers, data scientists, quants), and the integration
of theoretical grounding (Chinchilla scaling laws, LoRA derivation, DPO
reparameterisation) with applied financial context (FinBERT, BloombergGPT, MiFID
II, SR 11-7) is a genuine contribution relative to existing NLP textbooks that
treat finance only superficially.

**Assessment: Strong.** The chapter covers territory not well-served by existing
monographs, and the governance and regulatory sections (Sections 3.5 on bias,
hallucination, and governance) are particularly valuable for practitioners.

---

## 2. Technical Correctness

Several errors require correction before the chapter can be published.

### 2.1 BLOCKER — Chinchilla example numerical error (ex:chinchilla-finance, lines 511-532)

The example states that at $C = 10^{23}$ FLOPs, the parametric Chinchilla formula
(Eq. eq:chinchilla-Nstar, with $\alpha=0.34$, $\beta=0.28$, $A=406.4$,
$B=410.7$) yields $N^* \approx 6.4 \times 10^9$ parameters and
$D^* \approx 2.6 \times 10^{12}$ tokens, giving ratio $D^*/N^* \approx 406$.

**This is arithmetically wrong.** Evaluating the theorem formula directly:

$$
N^*(10^{23}) = \left(\frac{0.34 \times 406.4}{0.28 \times 410.7 \times 6^{0.28}}\right)^{1/0.62}
               \times (10^{23})^{0.28/0.62}
             \approx 0.5987 \times 2.438 \times 10^{10} \approx 1.46 \times 10^{10}
$$

The correct values are $N^* \approx 1.46 \times 10^{10}$, 
$D^* = 10^{23}/(6 \times 1.46 \times 10^{10}) \approx 1.14 \times 10^{12}$,
and ratio $D^*/N^* \approx 78$. The stated $6.4 \times 10^9$ corresponds
to $C \approx 1.6 \times 10^{22}$, not $10^{23}$.

The error appears to have originated from an earlier draft using different
constants and was not recomputed when the theorem was corrected. **The example
must be recomputed from scratch.**

### 2.2 MAJOR — Inconsistency between parametric constants and the "20 tokens per parameter" rule (lines 479, 526-528)

The theorem states $D^*/N^* \approx 20$ (line 479, as an empirical approximation
at $C_0 = 10^{23}$ FLOPs). Section 2.2 also claims the "20 tokens per parameter"
rule is valid near $C \approx 10^{22}$–$10^{23}$ FLOPs (lines 526-527).

However, the parametric constants ($\alpha=0.34$, $\beta=0.28$) imply
$D^*/N^* \approx 78$ at $C=10^{23}$ and $\approx 63$ at $C=10^{22}$. The
ratio~20 result comes from the IsoFLOP estimation approach (Hoffmann et al.,
Approach 1), not from the parametric model (Approach 3) whose constants the
theorem uses.

**Fix required:** Clearly distinguish the two estimation approaches. Either
derive the ratio from the parametric constants (yielding $\approx 60$–$80$) or
attribute the "~20" rule to the IsoFLOP approach and note that both are
approximations to the same underlying phenomenon. Conflating the two will
confuse any reader who verifies the arithmetic.

### 2.3 MAJOR — Incorrect citation for BERT (line 412)

Line 412 reads: "MLM, used by BERT \cite{yang2020finbert} and its financial
variants." The citation `yang2020finbert` refers to FinBERT (Yang et al., 2020),
not to the original BERT model. BERT was introduced by Devlin, Chang, Lee, and
Toutanova (2018/2019) and requires its own citation (e.g., `devlin2018bert`).
Citing FinBERT for BERT misattributes the foundational model to the
domain-adaptation paper that builds on it.

### 2.4 MAJOR — BloombergGPT corpus size error (line 1078)

Line 1078 states BloombergGPT was "trained on a 363-billion-token corpus," but
the same paragraph (lines 1079-1082) correctly describes the corpus as having
two components: (i) 363B finance-specific tokens and (ii) approximately 345B
general tokens from The Pile. The total corpus is therefore approximately 708B
tokens. The mix weights (51%/49%) also confirm this: $363/(363+345) \approx 51\%$.
The opening sentence must be corrected to "approximately 708-billion-token corpus."

Additionally, Table tab:bloomberggpt-corpus lists The Pile at 343B while the
text says 345B — a minor 2B discrepancy that should be reconciled with the
original paper.

### 2.5 MINOR — Gradient checkpointing memory formula imprecise notation

The claim that gradient checkpointing reduces activation memory from
$O(L \cdot T \cdot d)$ to $O(\sqrt{L} \cdot T \cdot d)$ (line 626-627) is
correct for optimal checkpoint placement but implicitly assumes checkpointing
only at the layer granularity. The 33% FLOP overhead claim is standard and
defensible. No correction required, but a footnote clarifying the assumption
would improve precision.

---

## 3. Exposition Quality

**Strengths:**

- The context/deepdive/remark box structure is well-executed and creates natural
  reading rhythms for mixed audiences.
- The adaptation spectrum (Section 3.3) is clearly organised and the LoRA
  parameter-count example is pedagogically exemplary.
- The DPO derivation (lines 925-942) is compact and technically sound.
- The regulatory section (Section 3.5) integrates MiFID II, SR 11-7, and the
  EU AI Act in a way that will be valuable to practitioners and is difficult to
  find elsewhere in the LLM literature.
- The red-teaming subsection (Section 3.4.4) is concrete and actionable.

**Weaknesses:**

- The chapter lacks a closing synthesis paragraph. After the governance
  framework, the chapter simply ends. A one-paragraph conclusion drawing
  together the pre-training, fine-tuning, evaluation, and governance themes
  would improve the reader's sense of coherence.
- The evaluation section context box (lines 1188-1198) is very short (9 lines)
  and could be expanded to frame the evaluation landscape more substantively
  before the technical metrics are introduced.
- The sentence "The mechanism is not fully understood theoretically" (line 729,
  on in-context learning) is accurate but could usefully cite one or two
  theoretical papers (Xie et al., 2022; Akyürek et al., 2022) to orient the
  reader.

---

## 4. Exercise Quality

One illustration exercise (ex:ch03-illustration) is present, referencing a
notebook for the Chinchilla scaling law. Given the chapter's breadth (data
preprocessing, PEFT, RLHF, benchmarking, governance), the exercise set is
thin. Exercises on LoRA rank selection, MinHash deduplication, and benchmark
interpretation would strengthen the chapter's pedagogical value. (Note: the
review understands that exercises are generated by a separate workflow and are
not yet included.)

---

## 5. Summary

The chapter is well-conceived and covers important ground. Its integration of
technical depth with financial application and regulatory context is a genuine
contribution. However, three factual errors (the Chinchilla example calculation,
the BloombergGPT corpus size, and the BERT citation) and one conceptual
inconsistency (the "20 tokens per parameter" rule versus the parametric
constants) are serious enough to require revision before the chapter can be
released. These issues would be immediately visible to any reader who verifies
the arithmetic, and in a textbook context they risk undermining the reader's
trust in the entire numerical exposition.

**Verdict: MAJOR_REVISION**

Required changes:
1. Recompute ex:chinchilla-finance from the stated formula and constants.
2. Reconcile the "20 tokens per parameter" claim with the parametric model.
3. Correct BERT citation (line 412) to Devlin et al.
4. Correct BloombergGPT corpus size (line 1078) to ~708B tokens.
5. Add a closing synthesis paragraph.
