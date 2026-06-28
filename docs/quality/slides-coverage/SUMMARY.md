# Slides Coverage Audit Summary

> **✅ All findings resolved (commit `e83346f`).** The 3 minor gaps (ch02 ×2, ch09 ×1)
> were applied to the lesson decks and both decks pass `tools/validate.mjs`. No critical
> gaps were ever found. The per-chapter reports and the table below are retained as the
> historical audit record; the "Status" column reflects the current (resolved) state.

Audit of all 17 chapters: the `slides-coverage-auditor` agent compared each book
`chapter.tex` against its HTML **lesson** deck (`index.html`) and **practical** deck
(`practical.html`), from the perspective of a **slides-only student** (attends lectures and
studies slides, never opens the book). The book is allowed to go deeper; only *load-bearing*
gaps are flagged.

**Headline: the decks hold up well.** Every chapter is followable end to end from the slides
alone — **no CRITICAL gaps anywhere**. Only 3 minor under-explained items across 2 chapters.
The premise that "the slides have a lot less content" is true in raw volume (the book carries
proofs, derivations, and extended citations), but the slides — helped substantially by the
"under the hood" panels and the practical decks — do convey the load-bearing concepts.

| Chapter | Title                                    | Slides-only verdict                              | Critical | Minor | Status |
|---------|------------------------------------------|--------------------------------------------------|----------|-------|--------|
| ch01    | Introduction                             | can follow end to end                            |    0     |   0   | —      |
| ch02    | LLM Foundations                          | follows end to end; 2 governance/mitigation thin |    0     |   2   | ✅ resolved (`e83346f`) |
| ch03    | LLM Training and Fine-Tuning             | can follow end to end                            |    0     |   0   | —      |
| ch04    | LLM Agents                               | can follow end to end                            |    0     |   0   | —      |
| ch05    | Business Valuation                       | can follow end to end                            |    0     |   0   | —      |
| ch06    | Credit Risk                              | can follow end to end                            |    0     |   0   | —      |
| ch07    | Applications & Future                    | can follow end to end                            |    0     |   0   | —      |
| ch08    | Domain-Specific LLMs                     | can follow end to end                            |    0     |   0   | —      |
| ch09    | Financial NLP & Sentiment                | follows end to end; few-shot named not defined   |    0     |   1   | ✅ resolved (`e83346f`) |
| ch10    | Portfolio & Quant Trading                | can follow end to end                            |    0     |   0   | —      |
| ch11    | RegTech, Compliance & AML                | can follow end to end                            |    0     |   0   | —      |
| ch12    | XAI & Explainability                     | can follow end to end                            |    0     |   0   | —      |
| ch13    | LLM Limitations & Evaluation             | can follow end to end                            |    0     |   0   | —      |
| ch14    | Financial Text Summarization             | can follow end to end                            |    0     |   0   | —      |
| ch15    | Privacy & Local Models                   | can follow end to end                            |    0     |   0   | —      |
| ch16    | AI/ML in Finance (Text)                  | can follow end to end                            |    0     |   0   | —      |
| ch17    | Loops, Goals & Iterations                | can follow end to end                            |    0     |   0   | —      |

```
Total chapters audited: 17  (all have both lesson + practical decks)
Chapters with gaps:      2   (Critical: 0, Minor: 3 across all chapters) — all 3 resolved (e83346f)
Reports saved to: docs/quality/slides-coverage/
```

## Chapters Requiring Attention — ✅ all resolved (`e83346f`)

Ordered by severity (all minor — no chapter is below a usable standard). All items below
were applied to the lesson decks; both decks pass `tools/validate.mjs`.

### ch02 — LLM Foundations (0 critical, 2 minor) — ✅ resolved → [ch02-slides-coverage.md](ch02-slides-coverage.md)
*Slides-only student: follows end to end; only two secondary governance/mitigation items are thinner than the book.*
- **Prompted self-critique / Constitutional AI** — the deck shows 5 of the book's 6 hallucination defenses; the missing one is the only mitigation a closed-API practitioner can deploy without weights. Add one bullet to the defenses slide.
- **US / SEC fiduciary responsibility** — the responsible-use slide is EU-only (AI Act, GDPR); the book also develops who is *liable* for an AI output. Add one bullet for the industry/NA audience.

### ch09 — Financial NLP & Sentiment (0 critical, 1 minor) — ✅ resolved → [ch09-slides-coverage.md](ch09-slides-coverage.md)
*Slides-only student: follows end to end; few-shot classification is named but never explained.*
- **Few-shot (in-context) classification** — the slides define zero-shot, then use "few-shot" in a caveat as if already explained. The chapter treats it as a co-equal method. Add one fragment defining few-shot before the caveat lands. (Mitigant: in-context learning is introduced in the foundations chapters.)

## Well-Covered Chapters

ch01, ch03, ch04, ch05, ch06, ch07, ch08, ch10, ch11, ch12, ch13, ch14, ch15, ch16, ch17
(15 of 17) — slides convey all load-bearing concepts; remaining differences from the book are
appropriate book-only depth (proofs, derivations, secondary examples, exhaustive citations).

## Top cross-chapter patterns

- **The "under the hood" panels are doing real work.** Where the book carries the rigour
  (full self-attention math, KD/KL direction, Krippendorff derivation, CAR regression), the
  matching under-the-hood panel or the practical deck carries it too. This is the main reason
  coverage is so high and is worth preserving as decks evolve.
- **The thin spots are the "soft" sections, not the technical core.** All 3 minor gaps are in
  governance/regulatory framing (ch02 SEC/fiduciary) or a method named-but-not-defined
  (ch02 self-critique, ch09 few-shot) — never the mathematics or the central method. When
  trimming for slides, the technical spine has been protected and the policy/secondary-method
  edges are where the occasional concept slips off.
- **No chapter is missing its motivation or its main result** — every deck lands the finance
  application that makes the topic matter, which is the single most important thing for a
  slides-only student.
