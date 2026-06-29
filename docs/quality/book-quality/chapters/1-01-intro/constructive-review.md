# Constructive Review — 1 01-intro

Reading index **1** (first chapter in `book/main.tex`). Audience: mixed academic +
industry finance (TOPIC.md). This is the book's opening chapter, so much of its content
is the canonical *first* introduction of concepts that recur downstream — making SSOT
discipline especially important here.

## Strengths to preserve

- **[KEEP_AS_SINGLE_SOURCE_OF_TRUTH] §1 `sec:ai-jobs-tasks` (lines 34–161)** — the
  task-based-automation framing (Autor; Acemoglu–Restrepo; Hampole et al.; Felten et al.)
  applied to a finance professor's task bundle is the book's economic thesis for *why a
  finance professional should care about LLMs at all*. No other chapter sets this up.
  The three Hampole findings (≈2% per s.d.; ≈14% at near-complete exposure; reallocation
  insulation, lines 74–87) are concrete and well-attributed. Keep verbatim.

- **[GOOD_BIG_PICTURE_EXPLANATION] §1.2 `sec:tasks-finance` (lines 127–145)** — the
  "compound advantage / AI is infrastructure that makes scarce professional time go
  further" passage, with three role-specific vignettes (equity analyst, compliance
  officer, quant researcher), is the clearest motivation in the book and exactly
  audience-appropriate. The "three papers simultaneously" professor example (130–135)
  lands the abstraction.

- **[KEEP / GOOD_BIG_PICTURE_EXPLANATION] §2 `sec:history` (lines 167–368)** — the
  history of financial textual analysis (Tetlock 2006 narrative cold-open →
  General Inquirer/Harvard IV-4 → Loughran–McDonald → LDA → Word2Vec/GloVe → LSTM →
  attention/BERT → FinBERT) is a strong, citation-dense spine. The Loughran–McDonald
  "tax/liability/depreciation are not negative in the financial register" explanation
  (lines 237–250) is the single best motivation of *domain-specific* NLP in the book.

- **[KEEP_AS_SINGLE_SOURCE_OF_TRUTH] §3.2 `def:textual-signal` + `eq:signal-predictability`
  + `eq:linear-factor` + `rem:identification` (lines 572–651)** — the formal
  $f:\mathcal{D}\to\mathbb{R}^k$ signal definition, the $\mathrm{Cov}(s_t,r_{t+1})\neq0$
  predictability condition, the linear factor model, and the four-part identification
  remark (reverse causality, confounding, multiple testing, misspecification) constitute
  the book's analytical backbone. The text explicitly frames the whole book as "an
  investigation of the best choice of $f$" (656–658). Later chapters should `\ref` this,
  not redefine it.

- **[GOOD_TECHNICAL_EXPLANATION] §6 `thm:vanishing-gradient` + proof + numeric
  (lines 1521–1610)** — the spectral-norm vanishing-gradient bound
  $\|\partial h_T/\partial h_k\|\le(\alpha\|W_h\|)^{T-k}$, its clean sub-multiplicativity
  proof, the $0.95^{500}\approx5\times10^{-12}$ "10-K opening paragraph is numerically
  zero" illustration, and the additive cell-state explanation of how the LSTM circumvents
  it (1605–1610) form a self-contained, re-derivable, finance-anchored derivation. Strong.

## Other strengths worth protecting

- **[GOOD_FINANCE_EXAMPLE] `ex:tfidf-example` (lines 888–1014)** — the fully worked TF-IDF
  computation on three finance sentences, including the two cosine-similarity numbers
  (0.213, 0.106), is independently re-derivable and exactly the kind of concrete worked
  example the rubric rewards. Protect the arithmetic.
- **[GOOD_FINANCE_EXAMPLE] `ex:risk-neighbours` / `tab:risk-neighbours` (lines 1362–1386)**
  — general vs. 10-K nearest-neighbours of *risk* (danger/threat vs. uncertainty/exposure/
  volatility) crisply motivates finance-domain embeddings.
- **[GOOD_TECHNICAL_EXPLANATION] Word2Vec SGNS derivation incl. NEG gradients
  (lines 1143–1231)** — softmax objective → negative-sampling loss → both gradient
  expressions with the "push positive closer, push negatives away" interpretation. Clean.
- **[KEEP_AS_SINGLE_SOURCE_OF_TRUTH] `def:corpus-vocab`, `def:bow`, `def:one-hot`,
  `def:tf`, `def:idf`, `def:tfidf` (§4)** — the classical-representation notation
  ($\mathcal{C}$, $\mathcal{V}$, $V$, $\mathbf{x}(d)$, term/document frequency). The
  deepdive intro explicitly states this notation is "used throughout the book" (672–673).
  This is the canonical home; downstream chapters should inherit, not redefine.
- **[KEEP] `prop:sqrt-dk` + proof (lines 1662–1685)** — the $\mathrm{Var}(s)=d_k$
  derivation is correct and self-contained (see SSOT note below on division of labour
  with ch02).
- **[GOOD_FINANCE_EXAMPLE] `rem:eu-ai-act` + `rem:sec-guidance` (lines 2084–2108)** — the
  EU AI Act risk-tier and SEC predictive-data-analytics summaries are concrete, correctly
  scoped to finance use-cases, and rarely covered this well in technical texts.
- **[KEEP] `rem:this-book-ai` (lines 147–159)** — the "this book was written using the
  tools it describes" reflexive remark is a memorable, honest pedagogical device that
  reinforces the task-based thesis.

## Dimensions already strong (do not over-edit)

- **`finance_orientation` (≈92):** every technique is introduced from a finance problem —
  TF-IDF from 10-K word dominance, embeddings from *risk* polysemy, RNN/LSTM from hedging
  clauses spanning a 10-K, attention from RNN failure on long filings. Finance-first
  throughout; not bolted on.
- **`finance_examples` (≈90):** worked TF-IDF (re-derivable), risk-neighbours table, EDGAR
  growth figure, API-cost worked example ($250 vs $15 per million headlines), context-
  window vs document-length table. Grounded and act-on-able.
- **`correctness` (≈90, math layer):** the vanishing-gradient bound, $\sqrt{d_k}$ variance
  proof, TF-IDF arithmetic, and SGNS gradients are all independently re-derivable. (Costs/
  pricing are appropriately hedged as illustrative — see protect note.)
- **`pedagogy` (≈90):** 9 explicit Learning Objectives map 1:1 onto sections; consistent
  `context` (big-picture) vs `deepdive` (under-the-hood) separation; the §"Looking Ahead"
  bridge (2113–2159) explicitly forward-references later chapters.
- **`concept_separation` (≈90):** disciplined use of `context` for motivation and
  `deepdive` for derivations is exactly what RUBRIC dimension 2 asks for.

## Single-source-of-truth candidates

- **Task-based AI/labour economics** — defined best here (§1). Owns it book-wide.
- **Textual-signal formalism** (`def:textual-signal`, predictability, identification) —
  best here (§3.2); later empirical chapters should `\ref` rather than re-derive.
- **Classical text representations** (BoW / one-hot / TF-IDF notation, §4) — canonical
  home; deepdive says so explicitly.
- **Vanishing gradient / LSTM** (§6) — owned here; ch02's "RNNs to Attention" (§ around
  line 341) should `\ref` this rather than re-derive the bound.
- **Attention / Transformers — SSOT belongs to ch02, NOT ch01.** Ch01 §7
  (`sec:attention`, lines 1615–1736) gives a *preview*: scaled dot-product attention
  (`def:attention`), the $\sqrt{d_k}$ variance proposition, and multi-head attention.
  Ch02 (reading index 3, `02-llm-foundations`) owns the *full* treatment — positional
  encoding (sinusoidal), encoder/decoder layers, causal masking, KV-cache, full
  architecture diagram (verified: ch02 lines 616–1136). **Recommendation:** ch02 is the
  single source of truth for the Transformer; ch01 should keep its compact preview but
  (i) the chapter already signals this correctly at lines 2128–2133 ("derived from first
  principles in §… of that chapter"), so preserve that bridge; (ii) the duplicated
  `def:attention`/$\sqrt{d_k}$ proof across ch01 and ch02 is *intentional preview vs.
  full-derivation* overlap — keep both but ensure ch02 `\Cref`s back to ch01's preview (or
  vice versa) so it reads as deliberate, not re-derived. Do **not** delete ch01's preview:
  it is needed in reading order (ch01 precedes ch02) to make the history section's
  attention paragraph (340–348) land.

## Protect-from-edit zones

- **Lines 34–161 (§1 task-based framework)** — the book's economic thesis; do not trim the
  Hampole/Felten findings or the reallocation mechanism when editing unrelated prose.
- **Lines 888–1014 (`ex:tfidf-example`)** — every number is load-bearing and cross-checked
  (tf, idf, tfidf tables, two cosine sims). An "unrelated" edit must not perturb the
  arithmetic.
- **Lines 1521–1610 (vanishing-gradient theorem, proof, numeric, LSTM resolution)** —
  self-contained derivation; the $0.95^{500}$ figure ties to the theorem.
- **Lines 1662–1685 (`prop:sqrt-dk` + proof)** — keep consistent with ch02's version.
- **Lines 1922–1954 + `rem` at 1944 / 1956 (API cost table and hedges)** — the pricing is
  explicitly framed as illustrative "2024" list prices with a verify-before-deploy caveat
  (`rem` lines 1944–1946) and the worked example says "at the illustrative prices."
  This is the correct way to handle volatile pricing — do **not** "fix" the numbers or
  strip the hedges; that framing is what keeps the table honest.
- **Lines 572–658 (`def:textual-signal` … "best choice of $f$")** — the analytical spine;
  the closing framing sentence anchors the whole book's narrative.

## One-paragraph assessment

The spine of this chapter is a three-part argument that must survive intact: (1) an
**economic thesis** — LLMs matter for finance because professions are task bundles and AI
reallocates effort toward high-comparative-advantage work (§1); (2) a **historical and
empirical motivation** — text carries priced-and-unpriced information, established from
Tetlock through Loughran–McDonald and formalised as the textual-signal
$f:\mathcal{D}\to\mathbb{R}^k$ with its identification caveats (§2–3); and (3) a
**technical ladder** — classical representations → embeddings → RNN/LSTM and the
vanishing-gradient bound → attention preview → model families → APIs → limitations
(§4–10). The chapter's deepest, most re-derivable assets are the textual-signal
formalism, the worked TF-IDF example, and the vanishing-gradient theorem; its most
distinctive non-technical assets are the task-based framing and the regulatory remarks.
The one cross-chapter discipline to enforce is attention/Transformer ownership: ch01
holds a deliberate *preview*, ch02 holds the *single source of truth*; the existing
forward-reference at §"Looking Ahead" already encodes this correctly and should be
protected rather than edited away.
