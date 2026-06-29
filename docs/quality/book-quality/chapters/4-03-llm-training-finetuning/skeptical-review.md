# Skeptical Review — Ch 03 (reading index 4): Training and Fine-Tuning

Format: `SEVERITY · dimension_key · file:line — issue`. Scope tag: local vs book-wide.
File: `book/chapters/03-llm-training-finetuning/chapter.tex` unless noted.

## BLOCKER

- `BLOCKER · notation_crossref · chapter.tex:389 — DUPLICATE LABEL def:mlm.`
  (book-wide / cross-chapter) `def:mlm` is also defined in
  `book/chapters/01-intro/chapter.tex:1786` ("Masked Language Modelling Objective",
  numbered 1.27). Ch03's is numbered 4.8. LaTeX `\label` collision: any `\ref{def:mlm}`
  is ambiguous and `pdflatex` emits "multiply-defined labels". Confirmed via `.aux`
  (`01-intro/chapter.aux:130` and `03.../chapter.aux:34`). Currently nothing `\ref`s it,
  which masks the breakage, but it is a hard label collision and a BLOCKER for
  notation_crossref. Ch03 should rename to e.g. `def:mlm-objective-train` OR (preferred
  per non_repetition) drop the re-definition and `\Cref` the ch01 SSOT — but note ch01
  precedes ch03 in reading order, so the *ch01* definition is the earlier one.

- `BLOCKER · notation_crossref · chapter.tex:781 — DUPLICATE LABEL def:lora.`
  (book-wide / cross-chapter) `def:lora` is also defined in
  `book/chapters/02-llm-foundations/chapter.tex:2184` ("Low-Rank Adaptation (LoRA)",
  with `eq:lora` there too). Ch02 (reading index 3) gives a shorter LoRA definition;
  ch03 (`:780`–`:794`) gives the fuller scaled $\frac{\alpha}{r}BA$ version. Both carry
  `\label{def:lora}` AND `\label{eq:lora}` → double collision. The two definitions even
  DISAGREE: ch02 uses $W = W_0 + BA$ (no scaling), ch03 uses $W = W_0 + \frac{\alpha}{r}BA$.
  BLOCKER for notation_crossref; also a non_repetition / correctness concern (same concept
  defined twice with different formulas, neither cross-referencing the other).

## MAJOR

- `MAJOR · code_figure_correctness · code/notebooks/03.../demo.ipynb — STUB.`
  (local / code-figure) `demo.ipynb` is a single markdown cell ending
  "[Placeholder — fill in with demonstration code when drafting the chapter]". It is an
  empty placeholder. The *real* illustration code lives in `exercises.ipynb`, which is
  fine, but the demo notebook is a stub and lowers reproducibility/code coverage.

- `MAJOR · reproducibility · code/notebooks/03.../exercises.ipynb cells 6–13 — unexecuted, network-dependent.`
  (local / code-figure) The SEC EDGAR data-lab exercises (`requests` to EDGAR) are not
  executed in `exercises_executed.ipynb` (which only contains the 6 illustration cells).
  They are non-deterministic (live EDGAR fetch) and unvalidated. The illustration figure
  cells (1, 3) ARE executed with outputs and the coefficients match the caption, so the
  figure itself is reproducible; the EDGAR exercises are not.

## MINOR

- `MINOR · completeness · chapter.tex:336–345 — replay-buffer remark forward-references
  "catastrophic forgetting" before it is formally introduced` (it is named again at
  `:756`/`:763` in `rem:adaptation-tax`). (local) Concept is used at `:339` and defined
  in passing; a one-line forward `\Cref` to `rem:adaptation-tax` would tidy ordering.

- `MINOR · citation_accuracy · chapter.tex:454–477 — Chinchilla constants
  ($E{=}1.69, A{=}406.4, B{=}410.7, \alpha{=}0.34, \beta{=}0.28$) and the derived
  $D^*/N^*\approx78$` (citation). Constants match the widely reported Hoffmann et al.
  (2022) parametric fit and the arithmetic is internally re-derivable
  ($N^*\approx1.46\times10^{10}$, $D^*\approx1.14\times10^{12}$ checks out), but the
  exact published-table values and the 78 ratio cannot be verified against the paper
  from local resources → `NEEDS_EXTERNAL_VERIFICATION`. Caps citation_accuracy at 89.

- `MINOR · citation_accuracy · chapter.tex:103–132 — GPT-3 corpus table` (citation).
  Token counts (CC 410B, WebText2 19B, Books1 12B, Books2 55B, Wikipedia 3B) and the
  60/22/8/8/2 sampling weights are the commonly cited Brown et al. (2020) figures and
  are self-consistent, but unverifiable locally → `NEEDS_EXTERNAL_VERIFICATION`.

- `MINOR · citation_accuracy · chapter.tex:1042 — FinBERT 88.5% vs BERT 80.7% on FPB`
  and `:1085`–`:1090` BloombergGPT 708B/363B/345B token split and 51/49 weights, and
  `:1335` FinQA human 91% / neural 68–75%. (citation) Plausible, hedged where uncertain,
  but exact figures unverifiable locally → `NEEDS_EXTERNAL_VERIFICATION`.

- `MINOR · correctness · chapter.tex:1130–1132 — "BloombergGPT adopts architectural
  choices from the BLOOM model family — specifically ALiBi"` (local). Minor naming
  nuance: ALiBi originates from Press et al. (2022), adopted by BLOOM; phrasing is
  defensible ("adopts … from the BLOOM family … rather than building on BLOOM weights")
  but a reader could read it as ALiBi being a BLOOM invention. NIT-adjacent; leave or
  add "(Press et al.)".

## NIT

- `NIT · concept_separation · chapter.tex:354,694,707,1015,1193,1218,1312,1423 — box
  granularity.` Several `deepdive`/`context` boxes span 100+ lines and wrap multiple
  subsections. The separation is real and good, but a few very long `deepdive` blocks
  (e.g. `:707`–`:1008`) mix PEFT, instruction tuning, RLHF, DPO, and domain adaptation
  under one box; consider splitting for skimmability. Does not block ≥90.

- `NIT · pedagogy · chapter.tex:285,291 — inline definitions of "$k$-shingle" and
  "min-wise independent family"` are correct but dense; fine for the mixed audience.

## Cross-chapter / book-wide summary
1. `def:mlm` collision ch01:1786 ↔ ch03:389 — BLOCKER.
2. `def:lora`/`eq:lora` collision ch02:2184 ↔ ch03:781, with *disagreeing* formulas — BLOCKER.
3. Section-level labels (`sec:finetuning`, `sec:evaluation`, `sec:safety`,
   `sec:pretraining`) are NOT collided book-wide (verified) — clean.
