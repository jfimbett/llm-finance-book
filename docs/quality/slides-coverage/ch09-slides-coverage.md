# Slides Coverage Audit — Chapter 9: Financial NLP and Sentiment Analysis

**Verdict:** GAPS FOUND (0 critical, 1 minor)
**Slides-only student:** Can follow the chapter end to end — the lesson deck plus practical cover every load-bearing concept with intuition, worked examples, and formula panels; the one soft spot is that few-shot/in-context classification is named but never actually explained as a method.

---

## CRITICAL — load-bearing concepts a slides-only student would miss

None. Every learning objective is represented on the slides: the five sources and their four distinguishing axes, the three-step preprocessing pipeline (normalization, deduplication, temporal alignment), the three generations of methods (LM lexicon with formula + worked example, FinBERT/SEC-BERT with the classification-head panel, LLM zero-shot), all five source-specific applications with their canonical empirical findings, aggregation/z-standardization/stationarity, the event-study (CAR) and predictive-regression frameworks, Fog readability, batch/streaming inference, and evaluation via Krippendorff's alpha + macro-F1 + economic validity. The practical deck reinforces LM scoring, macro-F1-vs-accuracy, and the CAR regression with full worked solutions.

---

## MINOR — present but under-explained

### Finding 1 — Few-shot (in-context) classification
- **On the slides:** The lesson slide "LLMs classify with no training set at all" defines and illustrates only *zero-shot* (a prompt sketch and rationale). The word "few-shot" appears once, obliquely, in the next slide's Fatemi & Hu bullet ("extra few-shot examples beyond a small set add no accuracy"). The practical deck does not cover it.
- **What is thin:** The chapter (Sec 2.3, and a stated learning objective) treats few-shot as a co-equal method: *k* labelled in-context examples placed in the prompt, with 4–8 domain examples improving calibration and trading off against throughput. A slides-only student sees the term used as if already understood but is never shown what few-shot *is* in this setting or why one would add in-context examples — they only get the negative result that more examples don't help. (Mitigant: in-context learning was likely introduced in the foundations chapters, so a diligent attendee may carry it over.)
- **Suggested slide treatment:** One fragment on the zero-shot slide: "Few-shot = prepend *k* labelled examples (4–8) so the model learns the labelling convention in-context — no gradient update," then the Fatemi bullet lands as the natural caveat.

---

## OK-to-omit — book-only depth, correctly left off the slides

- The full FinBERT fine-tuning recipe (Example, Sec 4.3: spaCy sentence splitting, 75%-agreement subset, learning-rate/batch/weight-decay hyperparameters, F1 0.70–0.80 vs 0.60–0.65) — secondary worked depth; the practical's `yiyanghkust/finbert-tone` extension covers the operational gist.
- Exhaustive empirical citation chains within each source (e.g., Antweiler 2004, Da 2015, Manela full NVIX construction, Engle climate hedge) — the slides keep the load-bearing finding per source and push the rest to an appendix/frontiers slide.
- Detailed nominal-vs-ordinal Krippendorff derivation and the $d^2(c,c')$ coincidence metric — the lesson appendix carries the ordinal panel; the full derivation is reference depth.
- Vendor/API enumeration (RavenPack, GDELT, Pushshift, edgar package specifics) — appropriately compressed into the appendix collection slide.

---

## Coverage Summary Table

| Chapter concept (load-bearing) | Slides status | Tier |
|--------------------------------|---------------|------|
| Five text sources + four distinguishing axes | COVERED (table + per-source blocks) | — |
| Preprocessing: normalization / dedup / temporal alignment | COVERED (incl. underhood + look-ahead) | — |
| LM lexicon: net-sentiment formula + GI critique | COVERED (panel + figure) | — |
| Worked LM example (−0.086) | COVERED (lesson + practical P1) | — |
| FinBERT / SEC-BERT + [CLS] classification head | COVERED (underhood) | — |
| Financial PhraseBank + why neutral matters | COVERED | — |
| LLM zero-shot classification | COVERED (prompt sketch) | — |
| LLM few-shot / in-context examples | PARTIAL (named, not defined) | MINOR |
| Five source applications + canonical findings | COVERED (social slide + 4-source grid) | — |
| Fog index / readability | COVERED (underhood + Li/Lehavy) | — |
| Aggregation, z-standardization, stationarity, sentiment inflation | COVERED (lesson + practical recap) | — |
| Event study / CAR + predictive regression (SUE, β₂) | COVERED (underhood + practical P3) | — |
| Short- vs long-horizon predictability | COVERED (table) | — |
| Inference at scale: batch vs streaming | COVERED (appendix) | — |
| Krippendorff's alpha + precision/recall/macro-F1 + economic validity | COVERED (two eval slides + practical P2) | — |
