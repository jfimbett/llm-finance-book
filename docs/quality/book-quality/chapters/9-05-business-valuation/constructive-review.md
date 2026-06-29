# Constructive Review — 9 05-business-valuation

*Target:* `book/chapters/05-business-valuation/chapter.tex` (reading index 9).
*Audience:* mixed academic + industry finance.
*Reviewer:* constructive-reviewer (preserve-good-content pass; not a defect hunt).

This chapter is one of the strongest applied chapters in the book. It carries the
canonical DCF/FCFF formalism, a clean ReAct loop description, a fully worked SaaS
case study, and a figure that is correctly hedged as illustrative. The dominant
risk during remediation is that a generic editor "tidies" the load-bearing
formalism (the FCFF/FCFE proposition, the error-propagation derivation) or strips
the careful illustrative-data caveats and reintroduces overclaiming. Protect those.

## Strengths to preserve

### DCF / FCFF formalism (single source of truth)
- `KEEP_AS_SINGLE_SOURCE_OF_TRUTH` §1.2 / eq.~\eqref{eq:dcf}, \eqref{eq:terminal-value} (lines 81–105) — the DCF enterprise-value equation, Gordon-Growth terminal value, and inline WACC definition `\mathrm{WACC}=w_E r_E + w_D r_D(1-\tau)` are stated cleanly and completely. This is the book's definitive DCF statement; later chapters (credit-risk, portfolio, applications) should `\eqref{eq:dcf}`/`\eqref{eq:terminal-value}` rather than re-derive. The "100-bp change alters TV by 20–40%" sensitivity hook (lines 102–105) correctly motivates §scenarios.
- `KEEP_AS_SINGLE_SOURCE_OF_TRUTH` / `GOOD_TECHNICAL_EXPLANATION` §3.1 Def~\ref{def:fcff}, Def~\ref{def:fcfe}, Prop~\ref{prop:fcff-fcfe-relation} (lines 320–368) — FCFF and FCFE defined precisely with every symbol named (τ, DA, CapEx, ΔNWC, NI, NB), and the FCFF↔FCFE relationship is stated as a proposition with a short, correct, independently re-derivable proof via `NI = (EBIT − Interest)(1−τ)`. This is the cleanest free-cash-flow treatment in the book and should be the referenced source. The added MM-with-taxes parenthetical (line 355) is a good clarifying gloss — keep.
- `KEEP` §3.1 closing paragraph on FCFF-vs-FCFE choice (lines 370–376) — correct, nuanced statement of when WACC-discounted FCFF is more robust than FCFE under changing leverage. Do not compress.

### Worked numeric examples (finance examples)
- `GOOD_FINANCE_EXAMPLE` §3.1 Example~\ref{ex:fcff-example} (lines 378–406) — the illustrative tech-firm FCFF walk-through (ΔNWC = 80, FCFF = 663.6 + 310 − 180 − 80 = 713.6M) is arithmetically correct and ties straight back to Def~\ref{def:fcff}. The ~\$15.2B EV / 3.6× revenue sanity check is well-hedged ("hypothetical", "consistent with software-sector medians"). Protect the arithmetic — an editor must not "round" these numbers and break the chain.
- `GOOD_FINANCE_EXAMPLE` §7.3 SaaS case study, Case Study (lines 1043–1091) — the composite mid-cap SaaS valuation is the chapter's keystone integration example: stylised profile → two flagged non-recurring items (\$45M restructuring, \$30M intangible step-up) → normalised EBIT \$915M, FCFF \$789M → base/upside/bear FCF table → \$17.0B base DCF, \$57.9/share → 9 comps at 24.5× EV/EBITDA → \$29.9B comps EV → Monte Carlo mean \$17.2B, P10–P90 \$12.5B–\$24.1B. It exercises *every* prior section and is explicitly labelled illustrative/composite (lines 1046–1048). KEEP verbatim, including the DCF-vs-comps divergence commentary (lines 1085–1090), which models honest valuation triangulation. Protect-from-edit.

### ReAct / tool-use
- `KEEP` / `GOOD_TECHNICAL_EXPLANATION` §4.3 ReAct, lines 678–697 — the Thought/Action/Observation three-phase loop with concrete tool names (`python_executor`, `edgar_search`, `calculator`) and the "agent formulates; interpreter computes" framing is the clearest short statement of tool-use in this chapter. Correctly attributed to `\citet{yao2022react}`. KEEP.
- `KEEP` / `GOOD_BIG_PICTURE_EXPLANATION` §4.1 "Why LLMs alone struggle with arithmetic" (lines 633–653) — the next-token-vs-deterministic-algorithm argument and the error-compounding motivation ("15–20 chained ops; an incorrect tax rate propagates") give the architectural *reason* tool augmentation is non-optional. This is the conceptual spine that justifies the entire §4. KEEP.
- `KEEP` §4.4 hallucination catalogue (lines 699–727) — phantom tickers, invented ratios, misapplied formulas, stale knowledge, each with a concrete mitigation ("do not trust until verified", mandatory ticker validation). Finance-grounded and actionable. KEEP.

### Figure / sensitivity heatmap
- `KEEP` Figure~\ref{fig:ch05-illustration} + Illustration~\ref{ex:ch05-illustration} (lines 825–856) — the AAPL DCF sensitivity heatmap. The figure file `figures/fig_illustration.pdf` exists. The caption is *exemplary*: it gives the exact formula `EV = FCF(1+g)/(WACC−g)`, the colour encoding, the qualitative finding (non-linear blow-up near the low-WACC/high-g corner), and — critically — hedges the data ("approximate FY2024 FCF; values are illustrative and depend on the filing date; see companion notebook for live computation via `yfinance`"). The companion Illustration extends the grid and backs out the implied discount rate from market cap. KEEP both the figure reference and the hedging language verbatim; do not let an editor strip the "illustrative" caveats.

### Other strong content (do not over-edit)
- `KEEP` Learning Objectives remark (lines 4–25) — eight specific, verb-led, individually assessable objectives mapped 1:1 to the eight sections. Strong pedagogical scaffold.
- `KEEP` §2 EDGAR ecosystem (lines 175–221) — accurate filing-type taxonomy (10-K/10-Q/8-K/DEF 14A), correct submissions/full-text/companyfacts API endpoints and CIK format, correct XBRL-since-2009 framing with the honest "filers exercise tag discretion → LLM fills the residual" caveat. Reliable reference material.
- `KEEP` §3.3 normalisation (lines 422–471) — one-time items / IFRS-16-ASC-842 leases / acquired-intangible amortisation, with the `lst:nonrecurring-prompt` listing and the High/Medium/Low confidence human-in-the-loop routing. The `EBIT* = EBIT + Σ a_k` formalisation (line 470) is a clean touch.
- `KEEP` §6 comparable selection (lines 869–969) — SIC-obsolescence-since-1987, conglomerate, and cyclical-timing pitfalls; Cosine-similarity Def~\ref{def:cosine-similarity}; and the two-stage hybrid (embedding candidate-gen → LLM filter) that "confines the LLM to where it excels and avoids where it is unreliable". Coherent, finance-first.
- `KEEP` / `GOOD_TECHNICAL_EXPLANATION` §8.3 error propagation (lines 1146–1183) — first-order Taylor expansion of DCF value with explicit ∂V/∂FCF and ∂V/∂g, and the worked sensitivity (1% FCF error → ~1% EV error; 100-bp g error → ~15–18% EV error), cross-checked against the exact discrete change (~16%). Quantitatively justifies the whole Monte-Carlo emphasis. Re-derivable; protect.

## Dimensions already strong (do not over-edit)
- `correctness` (~90–94) — FCFF/FCFE proof, FCFF arithmetic (713.6M), error-propagation derivative, and Gordon-Growth sensitivity all independently re-derivable; claims are precise and explicitly hedged where illustrative.
- `finance_orientation` (~92) — every technique is introduced from a valuation decision problem (M&A bid, IPO pricing, long/short signal, IFRS-13/ASC-820 Level-3 fair value); ML is never bolted on.
- `finance_examples` (~92) — the FCFF example and SaaS case study are grounded, integrated end-to-end, and tied to the companion notebooks.
- `concept_separation` (~90) — disciplined use of `context` (intro, extraction, pipeline) for big-picture and `deepdive` (cash flows, forecasting, tools, scenarios, efficiency) for under-the-hood; reader can follow either layer.
- `completeness` (~90) — WACC defined, terminal value derived, both FCF measures defined, evaluation metrics (MAPE/RMSE/DA) defined, caveats (illustrative data, hallucination guards, human review) present.
- `pedagogy` (~90) — objectives→sections mapping, per-section deepdive preambles stating what the reader will be able to do, smooth difficulty curve from definitions to integrated pipeline.
- `code_figure_correctness` (~90) — heatmap figure exists, caption matches the stated formula and finding, and is correctly flagged illustrative.

## Single-source-of-truth candidates
- **DCF enterprise value + Gordon-Growth terminal value** — defined best here at eq.~\eqref{eq:dcf}/\eqref{eq:terminal-value} (§1.2). Later chapters should `\eqref` these.
- **FCFF / FCFE and their relationship** — defined best here at Def~\ref{def:fcff}, Def~\ref{def:fcfe}, Prop~\ref{prop:fcff-fcfe-relation} (§3.1). Any later cash-flow discussion should `\ref` here, not re-derive.
- **MAPE / RMSE / Directional Accuracy** — Def~\ref{def:mape}/\ref{def:rmse}/\ref{def:da} (§5.4) are clean, general forecast-evaluation definitions; portfolio/trading and limitations-evaluation chapters can `\ref` these rather than restate.
- **Cosine similarity** — Def~\ref{def:cosine-similarity} (§6.3) is a tidy general definition; embedding-using chapters may reference it (note: foundational chapters may already own this concept — defer to earliest reading-order home if one exists).
- **ReAct loop (Thought/Action/Observation)** — well stated here (§4.3); if Ch.~`ch:llm-agents` (read #6, earlier) is the canonical home, this should `\ref` there. Either way, keep only one source of truth; this version is good enough to be it if the agents chapter's is weaker.

## Protect-from-edit zones
- Lines 320–406 (FCFF/FCFE definitions, Prop + proof, worked Example) — the formal spine; any arithmetic or symbol edit risks breaking re-derivability.
- Lines 1043–1091 (SaaS case study) — the integrating example; the numeric chain must stay internally consistent and the "illustrative/composite" disclaimers (lines 1046–1048) must survive.
- Lines 825–856 (AAPL heatmap figure + Illustration) — keep the formula, the qualitative finding, and especially the illustrative-data / `yfinance` caveats; do not let a rewrite reintroduce a hard factual AAPL valuation claim.
- Lines 1146–1183 (error-propagation derivation) — the ∂V/∂g derivative and the ~15–18% vs ~16% cross-check are load-bearing and exact; protect.
- Lines 1127, 1140–1144 (coverage/MAVE/cost/latency) — these are *deliberately* hedged ("rough illustration", "broadly comparable", "verify current rates", "on the order of"). Preserve the hedging; an editor must not convert these into hard numbers.

## One-paragraph assessment
The spine of this chapter is the disciplined fusion of *rigorous valuation theory*
(DCF, FCFF/FCFE with proof, Gordon-Growth terminal value, first-order error
propagation) with a *production LLM workflow* (EDGAR extraction → normalisation →
CoT forecasting → ReAct-routed arithmetic → Monte Carlo → hybrid comparables →
orchestrated pipeline), tied together by a single end-to-end SaaS case study and an
honestly-captioned AAPL sensitivity heatmap. Its distinguishing virtue is epistemic
honesty: illustrative numbers are labelled illustrative, arithmetic is offloaded to
a deterministic interpreter for a clearly-argued architectural reason, and
hallucination guards plus mandatory human review are stated as non-negotiable. That
combination of mathematical correctness, finance-first motivation, and well-hedged
claims is exactly what must survive remediation; edits should be surgical and stay
out of the formalism, the case study, the heatmap caveats, and the error-propagation
derivation.
