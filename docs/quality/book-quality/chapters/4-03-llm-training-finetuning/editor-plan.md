# Editor Plan — Ch 03 (reading index 4): Training and Fine-Tuning

Audit only — no edits applied. Each item: target dimension · SSOT decision · action.

## MUST_FIX (block ≥90)

1. **Resolve `def:mlm` duplicate label.** (`notation_crossref`)
   - SSOT: ch01 `01-intro/chapter.tex:1786` is the *earlier* MLM definition in reading
     order (reading index 1). Ch03 `:388`–`:400` re-defines it with a richer mask-set
     formulation as a contrast to CLM.
   - Action: rename ch03's label to a unique key (e.g. `def:mlm-train` or
     `def:mlm-objective`) AND add `\Cref{def:mlm}` (ch01) at first mention so the reader
     is pointed to the SSOT, presenting ch03's box as "the training-objective view of"
     the already-defined MLM. Keep both equations but reconcile notation. Smallest viable
     fix: rename the ch03 label only. Do NOT delete ch03's CLM-vs-MLM contrast (it earns
     its place). Touch only `03-.../chapter.tex:389` (+ optional cross-ref line).

2. **Resolve `def:lora` + `eq:lora` duplicate labels AND formula mismatch.**
   (`notation_crossref`, `non_repetition`, `correctness`)
   - SSOT: ch02 `02-llm-foundations/chapter.tex:2184` introduces LoRA first (reading
     index 3); ch03 `:780`–`:794` is the fuller PEFT treatment with $\frac{\alpha}{r}$ scaling.
   - Action: rename ch03 labels to `def:lora-peft` / `eq:lora-scaled`. Reconcile the
     formula discrepancy: ch02 has $W=W_0+BA$ (no scaling), ch03 has $W=W_0+\frac{\alpha}{r}BA$.
     Add one sentence in ch03 noting it refines `\Cref{def:lora}` (ch02) by adding the
     $\alpha/r$ scaling factor, so the two are explicitly the same concept, not a
     contradiction. Designate ch03 as SSOT for the *full* PEFT comparison; ch02 keeps the
     first lightweight mention. Touch `03-.../chapter.tex:781,786`.

## SHOULD_FIX

3. **Replace `demo.ipynb` stub or remove it.** (`code_figure_correctness`, `reproducibility`)
   - Action: either fill `code/notebooks/03.../demo.ipynb` with the demonstration code its
     own markdown promises (tokenisation, CLM/MLM, Chinchilla calc, LoRA, eval) or delete
     it and point the chapter solely at `exercises.ipynb` (whose illustration cells are
     executed and match the figure). Do not ship a placeholder cell.

4. **Execute / document the EDGAR exercise cells.** (`reproducibility`)
   - Action: mark cells 6–13 of `exercises.ipynb` clearly as live-network exercises
     (non-deterministic; not part of the reproducible figure pipeline), or snapshot a
     cached EDGAR sample so they run offline deterministically. The illustration figure
     pipeline is already reproducible — preserve it.

5. **Add forward cross-ref for "catastrophic forgetting".** (`concept_ordering`)
   - Action: at first use (`:339`, `rem:replay`), add `\Cref{rem:adaptation-tax}` so the
     term is anchored to its fuller treatment (`:760`–`:768`). Minor.

## OPTIONAL

6. Split the very long `deepdive` block (`:707`–`:1008`, PEFT→RLHF→DPO→domain adaptation)
   into two boxes for skimmability. (`concept_separation`)
7. Add "(Press et al.)" to the ALiBi attribution (`:1130`–`:1132`). (`correctness`/NIT)

## DO_NOT_CHANGE (protect)

- The two-approach Chinchilla disambiguation (`:470`–`:476`, `:521`–`:525`, fig caption
  `:654`–`:667`) — correct and deliberately careful.
- The Chinchilla proof (`:479`–`:506`) and all hedged empirical figures
  ("for illustration", "vary with corpus, hardware, and seed", `:1005`, `:1042`, `:1335`).
- The `context`/`deepdive` separation architecture and the closing synthesis (`:1628`–`:1642`).
- All 33 `\cite` keys resolve and are non-duplicate — do not touch the `.bib` for this chapter.

## BOOK_WIDE_ITEMS

- **BW-1** `def:mlm` collision between ch01 (`01-intro:1786`) and ch03 (`03-...:389`).
  Target `notation_crossref`. SSOT = ch01 (earlier in reading order). Needs book-level
  dedup pass (`/audit-cross-refs`, `/book-quality-regression`).
- **BW-2** `def:lora` + `eq:lora` collision between ch02 (`02-...:2184`) and ch03
  (`03-...:781`), with mismatched formula. Target `notation_crossref` + `non_repetition`
  + `correctness`. SSOT = ch03 for full PEFT; ch02 keeps first mention. Reconcile $\alpha/r$.
- **BW-3** Confirm no further definition-label collisions for shared concepts
  (perplexity, BPE, MinHash appear only in ch03 — verified clean). Roll into the
  book-wide duplicate-label sweep.
