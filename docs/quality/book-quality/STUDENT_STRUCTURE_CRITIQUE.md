# STUDENT_STRUCTURE_CRITIQUE

_Re-evaluation after structural edits (prior run: 84/100 FAIL). Reading order and every
claim below were re-verified against the live sources on 2026-06-26._

Reading order (from `book/main.tex`, the only source of truth):

**Part I — Foundations of Large Language Models**
1. `ch:intro` (01-intro)
2. `ch:ai-ml-finance-text` (16-ai-ml-finance-text)
3. `ch:llm-foundations` (02-llm-foundations)
4. `ch:llm-training` (03-llm-training-finetuning)
5. `ch:domain-specific-llms` (08-domain-specific-llms)

**Part II — Agents, Tools, and Skills**
6. `ch:llm-agents` (04-llm-agents)

**Part III — Understanding Financial Text**
7. `ch:financial-nlp-sentiment` (09-financial-nlp-sentiment)
8. `ch:financial-text-summarization` (14-financial-text-summarization)

**Part IV — Quantitative Finance Applications**
9. `ch:business-valuation` (05-business-valuation)
10. `ch:credit-risk` (06-credit-risk)
11. `ch:portfolio-quant-trading` (10-portfolio-quant-trading)

**Part V — Trust, Governance, and Deployment**
12. `ch:regtech-compliance-aml` (11-regtech-compliance-aml)
13. `ch:xai-explainability` (12-xai-explainability)
14. `ch:llm-limitations-evaluation` (13-llm-limitations-evaluation)
15. `ch:privacy-local-models` (15-privacy-local-models)

**Part VI — Engineering Agentic Workflows and Outlook**
16. `ch:loops-goals-iterations` (17-loops-goals-iterations)
17. `ch:applications-future` (07-applications-future)

17 chapters, 6 parts. The `\part` arc is coherent: foundations → agentic tooling →
reading text → quantitative apps → governance/deployment → advanced agentic engineering +
outlook.

## Verification of the seven claimed edits (all PASS)

1. **6 `\part` divisions define order** — confirmed, `book/main.tex` lines 55–82. The
   header comment (lines 49–53) states the simple→advanced rationale.
2. **ch04 `subsec:file-based-pattern` with concrete artifacts** — confirmed,
   `04-llm-agents/chapter.tex` line 603. Contains a real agent `.md` *with YAML
   frontmatter* (lines 628–652), a skill `.md` *with YAML frontmatter* that calls another
   agent and another skill (lines 657–671), and a *hook JSON config* (lines 677–686).
   Forward `\Cref{ch:loops-goals-iterations}` at line 695, framed as "develop fully later."
3. **ch17 opens with a `\begin{context}` bridge** — confirmed,
   `17-loops-goals-iterations/chapter.tex` lines 32–47. It `\Cref`s `ch:llm-agents`,
   `def:skill`, `def:agent-hook`, and `subsec:file-based-pattern`, explicitly says "We do
   not re-derive those definitions here," and justifies the late placement (needs
   `ch:credit-risk` + Part V as ingredients).
4. **ch16 `sec:book-roadmap` rewritten to live 6-part order** — confirmed,
   `16-ai-ml-finance-text/chapter.tex` lines 663–718. Walks all six parts in live order,
   references `subsec:file-based-pattern` and `ch:loops-goals-iterations`.
5. **ch07 `tab:chapter-map` in live order incl. ch17, privacy before applications** —
   confirmed, `07-applications-future/chapter.tex` table lines 75–134; rows run
   intro → … → privacy (`ch:privacy-local-models`) → `ch:loops-goals-iterations` →
   `ch:applications-future`. The recap prose (lines 42–67) walks all six parts including
   ch17.
6. **ch06 SHAP trimmed to applied recall + forward-ref to ch12** — confirmed,
   `06-credit-risk/chapter.tex` lines 797–815: local conceptual recall + the efficiency
   property (`eq:shap-efficiency`) it actually uses, then "the full derivation is in the
   dedicated explainability chapter (`\Cref{def:shapley-value}` … in
   `\Cref{ch:xai-explainability}`)." The full derivation lives only in
   `12-xai-explainability/chapter.tex` (`def:shapley-value` line 210, `eq:shapley-value`).
7. **ch01 names cross-entropy at `eq:ar-objective`** — confirmed,
   `01-intro/chapter.tex` line 1651: "This negative log-likelihood is the
   *cross-entropy* loss…".

Integrity checks: **zero duplicate `\label`s** across all chapters; **exactly one**
`\begin{definition}[Shapley Value]` (ch12); cross-entropy is *named* at first use (ch01)
and *formalised once* (ch03, `eq:cross-entropy`), with later mentions being local
applications, not re-derivations.

## Scores
- D1 Concept ordering:        92/100  (weight 35%)
- D2 Progressive order:       93/100  (weight 25%)
- D3 Non-repetition:          95/100  (weight 20%)
- D4 Agentic tooling intro:   95/100  (weight 20%)
- OVERALL:                    93/100
- VERDICT: **PASS** (overall ≥90, no dimension <85, zero BLOCKERs)

OVERALL = 0.35·92 + 0.25·93 + 0.20·95 + 0.20·95 = 32.2 + 23.25 + 19.0 + 19.0 = **93.45 → 93**.

## BLOCKERS (use-before-introduction; must be zero to pass)
- **None.** The one cross-part forward dependency — SHAP used in read#10
  (`ch:credit-risk`) with its formal Shapley definition in read#13
  (`ch:xai-explainability`) — is no longer a blocker: ch06 supplies enough local context
  (name expansion, the average-marginal-contribution intuition, and the efficiency
  property `eq:shap-efficiency` it actually relies on) for the credit passage to stand on
  its own, and points forward with a `\Cref`. This is exactly the "forward `\Cref` + local
  context" pattern the rubric permits.

## MAJOR issues
- None.

## MINOR issues (watch items; none cost the PASS)
- **[m1] D1 — SHAP formal object still defined after first use.** The forward dependency
  in §1 above is acceptable but not ideal; the formal `def:shapley-value` (read#13) trails
  its first applied use (read#10). It reads fine, but a purist could prefer a one-line
  formal Shapley statement parked in ch06. Low priority — do not disturb the single-source
  property in ch12.
- **[m2] D2 — two end-of-book "capstone-flavoured" chapters.** ch17 calls itself a
  "methodology capstone" (line 30) while ch07 is the closing synthesis. The ordering is
  justified by ch17's context box (it needs Part IV/V material), and ch07 is genuinely the
  outlook/closing, so this is coherent — just note that two consecutive
  synthesis-toned chapters end the book. No action needed.
- **[m3] D2 — agentic tooling is intentionally two-tiered (basic in Part II, advanced in
  Part VI).** This is a deliberate, well-bridged design (ch04 introduces primitives + file
  format; ch17 composes them into loops without re-deriving). Flagged only so future edits
  preserve the "build-on, don't-repeat" relationship.

## What is already good (protect during edits)
- The `\part` structure in `main.tex` and its rationale comment — the spine of D2.
- ch04 `subsec:file-based-pattern`: the concrete agent/skill/hook file examples sitting in
  Part II *before* any finance chapter leans on them — the spine of D4. Do not move it
  later or strip the YAML frontmatter / JSON config.
- The ch17 `\begin{context}` bridge and its explicit "we do not re-derive" pledge —
  the spine of D3 for the agentic material.
- Single-source Shapley derivation in ch12 with ch06 doing applied recall — protect the
  no-duplicate-label, no-re-derivation state.
- The synchronized roadmap (ch16) and recap/table (ch07): all three now agree with
  `main.tex`. Any future reordering must update all three together.

## Prioritised fix list (highest leverage first)
The book PASSES; the items below are optional polish, not gates.
1. (Optional, m1) Add a one-line formal Shapley statement or an inline `$\phi_j$`
   definition in ch06 §`subsec:shap-credit` so the formal object is present at first use,
   keeping ch12 as the sole full derivation.
2. (Optional, m2) Soften ch17's "methodology capstone" framing (line 30) to avoid two
   capstone-toned chapters back to back, or have ch07 explicitly cast itself as the
   forward-looking coda rather than a second synthesis.
3. (Maintenance) Keep `main.tex`, ch16 roadmap, and ch07 chapter-map/recap in lockstep on
   any future reorder — they are now the three places that encode reading order in prose.
