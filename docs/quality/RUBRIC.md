# RUBRIC.md — Book-Quality Rubric (0–100, ≥90 = release)

> Canonical scoring rubric for the **multi-agent book-quality goal system** of
> *Large Language Models in Finance*. This rubric supersedes the legacy 5-dimension
> 0–10 `scorer` rubric **for book-quality audits only**. The legacy scorer and its
> commit gate (`quality_threshold: 8` in `TOPIC.md`) remain in force for ordinary
> `/score-content` saves; this file governs `/audit-book-quality`,
> `/audit-chapter-quality`, `/iterate-book-quality`, and `/book-quality-regression`.

---

## 0. Ground rules

1. **Reading order is the ground truth.** Every ordering, progression, repetition,
   and use-before-definition judgement uses the `\include{...}` order in
   `book/main.tex`, **not** the numeric folder names. Current reading order:

   ```
   01 → 16 → 02 → 03 → 08 → 04 → 09 → 14 → 05 → 06 → 10 → 11 → 12 → 13 → 07 → 15
   ```

   Reading-index ↔ file map (kept in sync with `main.tex`):

   | Read # | File | Title |
   |--------|------|-------|
   | 1 | `01-intro` | Introduction |
   | 2 | `16-ai-ml-finance-text` | AI, ML, and Text in Finance |
   | 3 | `02-llm-foundations` | LLMs: Architecture and Practice |
   | 4 | `03-llm-training-finetuning` | Training and Fine-Tuning |
   | 5 | `08-domain-specific-llms` | Domain-Specific Financial LLMs |
   | 6 | `04-llm-agents` | LLM Agents and Finance Applications |
   | 7 | `09-financial-nlp-sentiment` | Financial NLP and Sentiment |
   | 8 | `14-financial-text-summarization` | Financial Text Summarization |
   | 9 | `05-business-valuation` | LLMs for Business Valuation |
   | 10 | `06-credit-risk` | LLMs for Credit Risk Analysis |
   | 11 | `10-portfolio-quant-trading` | Portfolio Optimization & Quant Trading |
   | 12 | `11-regtech-compliance-aml` | RegTech, Compliance, AML |
   | 13 | `12-xai-explainability` | Explainability and Interpretability |
   | 14 | `13-llm-limitations-evaluation` | LLM Limitations & Evaluation |
   | 15 | `07-applications-future` | Other Applications & Future Trends |
   | 16 | `15-privacy-local-models` | Privacy, Local Models, De-identification |

   Appendices A–F follow, in `main.tex` order.

2. **Score band semantics.**

   ```
   0–49   failing        — wrong, broken, or absent
   50–69  weak           — present but unreliable
   70–79  acceptable draft
   80–89  good but NOT release-ready
   90–94  release-quality   ← target floor
   95–100 excellent (rare)
   ```

3. **A chapter does not earn 90 merely for being readable.** A 90 on any dimension
   requires the *positive evidence* listed in that dimension's "≥90 requires" row —
   not just the absence of complaints.

4. **Preserve good content.** Reviewers must mark what is correct and worth keeping.
   The editor must protect `KEEP`-tagged content. Edits are targeted and minimal.

5. **No invention.** If a citation/claim cannot be verified locally, mark it
   `NEEDS_EXTERNAL_VERIFICATION`. Never fabricate paper details, statistics, or data.

---

## 1. The 14 dimensions

Each dimension is scored 0–100 per chapter and (where meaningful) at book level.
Keys in this table are the canonical JSON keys used in every `score.json`.

| # | Key | Dimension | ≥90 requires | Primary auditor(s) |
|---|-----|-----------|--------------|--------------------|
| 1 | `correctness` | Correctness of explanations | Every claim correct & precise; no overclaiming; no H-class hallucination; math re-derivable | math-checker, fact-checker, hallucination-detector, skeptical-reviewer |
| 2 | `concept_separation` | Big-picture vs under-the-hood separation | Intuition and internals clearly delineated (e.g. `context`/`deepdive` boxes); reader can follow either layer alone | structure-reviewer, skeptical-reviewer |
| 3 | `code_figure_correctness` | Code/figure correctness | Code runs (or is clearly runnable); figures match the prose claim; no contradiction between figure and text | code-figure-auditor, code-reviewer |
| 4 | `concept_ordering` | Concept introduction & ordering | Every concept defined before use **in reading order**; zero use-before-definition | concept-ordering-auditor |
| 5 | `progressive_learning` | Progressive learning path | Chapter builds on prior chapters; smooth difficulty curve; explicit bridges | concept-ordering-auditor, pedagogy-reviewer |
| 6 | `non_repetition` | Lack of unnecessary repetition | Overlap is intentional and cross-referenced, not re-derived; one source of truth per concept | concept-ordering-auditor, skeptical-reviewer |
| 7 | `finance_orientation` | Finance orientation | Finance-first framing; techniques motivated by finance problems, not bolted on | finance-auditor |
| 8 | `finance_examples` | Finance example quality & integration | Realistic, grounded, integrated (not orphaned); reader can act on them | finance-auditor |
| 9 | `citation_hygiene` | BibTeX correctness & cleanliness | All keys resolve; no dupes/stubs; required fields present; no stale `.bib` confusion | citation-description-auditor, audit-bibliography |
| 10 | `citation_accuracy` | Accuracy of paper descriptions | Described result matches the cited source; right paper for the proposition | citation-description-auditor, fact-checker |
| 11 | `completeness` | No missing bridge concepts/warnings/definitions/caveats | No critical concept, caveat, definition, or bridge missing | skeptical-reviewer, structure-reviewer |
| 12 | `notation_crossref` | Notation, labels, cross-references | All `\ref`/`\cite` resolve; consistent notation; no label collisions; no hard-coded "Chapter N" prose refs | cross-ref-checker, consistency-checker |
| 13 | `reproducibility` | Reproducibility of code/notebooks/figures | Figures regenerable; deterministic or clearly documented; notebooks real, not stubs | code-figure-auditor |
| 14 | `pedagogy` | Pedagogical clarity for the audience | Audience-appropriate; objectives clear; difficulty curve sound; terms defined for the mixed academic/industry reader | pedagogy-reviewer, accessibility-reviewer, constructive-reviewer |

### Dimension detail (anchors)

For each dimension, score against these anchors. "Evidence" must cite file + line/section.

- **`correctness` (1).** 0 = factually wrong claims or fabricated stats. 50 = mostly
  right but imprecise. 90 = all claims correct, precise, no overclaiming, no
  hallucinations, math independently re-derivable. 100 = every assertion sourced and
  exact.
- **`concept_separation` (2).** 0 = intuition and internals mixed indiscriminately.
  50 = some signposting. 90 = big-picture and technical layers clearly delineated
  (use `context` for the bigger picture, `deepdive` for under-the-hood). 100 = reader
  can read either layer standalone.
- **`code_figure_correctness` (3).** 0 = code wrong or figure contradicts prose. 50 =
  runs but unvalidated. 90 = runs deterministically (or documented as illustrative)
  and figures provably match claims. 100 = reproducible from seed and tested. If a
  chapter has no code/figures, score on the correctness of any tables/worked numeric
  examples; if truly none apply, set `score: null` and `pass: true` with evidence
  `"N/A — no code or figures"`.
- **`concept_ordering` (4).** 0 = concepts used before defined. 90 = every concept
  defined before first use in reading order; zero forward-dependency. 100 = optimal
  pedagogical order.
- **`progressive_learning` (5).** 0 = no build-up. 90 = each chapter builds on prior
  with a smooth curve and explicit bridges. 100 = deliberate, signposted progression.
- **`non_repetition` (6).** 0 = same material re-derived verbatim across chapters.
  90 = overlap is intentional and cross-referenced via `\ref`/`\Cref`, not re-derived;
  one designated single source of truth per concept. 100 = zero redundant derivation.
- **`finance_orientation` (7).** 0 = generic ML with finance bolted on. 90 =
  finance-first framing; each technique tied to a real finance use case. 100 = every
  concept motivated by a financial decision problem.
- **`finance_examples` (8).** 0 = toy/fabricated. 90 = realistic, grounded,
  integrated (cf. wiring in `exercises/valuation_example/`), reader can run them.
  100 = backed by data/exercises the reader can reproduce.
- **`citation_hygiene` (9).** 0 = missing/malformed/duplicate keys. 90 = all keys
  resolve, no dupes/stubs, fields complete. 100 = clean + DOIs verified.
- **`citation_accuracy` (10).** 0 = misattributes results. 90 = described result
  matches source exactly; correct paper for each proposition. 100 = verified against
  the paper. Unverifiable-locally → `NEEDS_EXTERNAL_VERIFICATION` (caps at 89).
- **`completeness` (11).** 0 = major gaps (e.g. WACC never derived). 90 = no critical
  concept/warning/definition/bridge missing. 100 = comprehensive incl. caveats.
- **`notation_crossref` (12).** 0 = undefined refs or label collisions. 90 = all refs
  resolve, consistent notation, no collisions, no hard-coded chapter-number prose.
  100 = uniform symbols book-wide.
- **`reproducibility` (13).** 0 = figures unregenerable / notebooks are placeholders.
  90 = figures regenerable and documented; notebooks real. 100 = seeded, snapshotted,
  notebook-execution validated. N/A handling as in dimension 3.
- **`pedagogy` (14).** 0 = inaccessible to the audience. 90 = objectives clear,
  difficulty curve sound, terms defined for the mixed academic/industry reader.
  100 = exemplary scaffolding.

---

## 2. Pass conditions

- **Chapter pass:** `pass: true` **iff** every applicable dimension ≥ 90 (a dimension
  set to `null` for N/A does not block).
- **Book pass:** true **iff** all of:
  1. every chapter passes;
  2. every book-level dimension ≥ 90;
  3. the book compiles (`scripts/build-book.sh` clean);
  4. no broken `\ref`/`\eqref`;
  5. no unresolved `\cite` keys;
  6. no known duplicate labels (e.g. `def:calibration`);
  7. no stale critical audit reports (STATUS.md / bibliography-audit re-run fresh).

---

## 3. Severity vocabulary (skeptical reviewer)

`BLOCKER` (must fix before scoring can pass) · `MAJOR` (significantly lowers a
dimension) · `MINOR` (polish) · `NIT` (optional). Each issue is tagged with its
dimension key (above) and its scope: `local` · `cross-chapter-ordering` ·
`book-repetition` · `citation` · `code-figure` · `finance-example`.

## 4. Preservation vocabulary (constructive reviewer)

`KEEP` · `KEEP_BUT_MOVE` · `KEEP_BUT_CLARIFY` · `KEEP_AS_SINGLE_SOURCE_OF_TRUTH` ·
`GOOD_FINANCE_EXAMPLE` · `GOOD_TECHNICAL_EXPLANATION` · `GOOD_BIG_PICTURE_EXPLANATION`.

## 5. Available LaTeX environments (do not invent new ones)

From `book/preamble.tex`: `context` (bigger picture), `deepdive` (under the hood),
`definition`, `example`, `illustration`, `remark`, `theorem`/`lemma`/`proposition`/
`corollary`. There is **no** dedicated `warning`/`takeaway` box — use `remark` or a
`context` box for caveats/takeaways. Concept separation should reuse `context` vs
`deepdive`. Cross-references use `\ref`/`\Cref{ch:...}` — never hard-coded chapter
numbers.
