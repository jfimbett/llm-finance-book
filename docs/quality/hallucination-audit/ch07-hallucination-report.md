# Hallucination Audit Report — Chapter 07: Other Applications in Finance and Future Trends

**Verdict:** HALLUCINATIONS FOUND (1 text, 0 code)

---

## Text Hallucinations

### H4 — Synthetic Real-World Examples

**Finding 1**
- **Location:** Section "Building Your Own Research Assistant," subsection `subsec:af-ra-openclaw` (paragraph beginning "OpenClaw (\url{https://openclaw.ai}) is an open-source framework...")
- **Quoted text:** "OpenClaw (\url{https://openclaw.ai}) is an open-source framework that resolves this tension architecturally: it runs entirely on the user's own hardware... OpenClaw accepts queries and returns responses through the messaging channels finance professionals already use---WhatsApp, Telegram, Slack, Discord, iMessage, and Signal."
- **Why flagged:** A named software product is presented as a real, existing open-source framework with a concrete verifiable URL (`openclaw.ai`) and a specific feature set (six named messaging integrations; Ollama/llama.cpp local inference; named cloud models). There is no `\cite{}` and no "for illustration"/"hypothetical" framing — it is asserted as factually existing. This is the structural pattern of invented specificity: a precise, checkable real-world claim with no source. (Note: the framework appears throughout the chapter, including a Learning Objective and an `\begin{example}` block, suggesting it may be the book's own bespoke/teaching framework; if so, it should be explicitly framed as a hypothetical/illustrative tool rather than asserted as an existing product at a live URL. The detector flags the pattern, not authorial intent.)
- **Recommended action:** Either add a citation/reference establishing OpenClaw as a real, locatable framework, or reframe it explicitly as an illustrative/hypothetical reference architecture (e.g., "a hypothetical local assistant we will call OpenClaw") and drop or qualify the live URL.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H4   | Sec. Research Assistant / `subsec:af-ra-openclaw` | MEDIUM |

**Severity guide:**
- HIGH: fabricated data attributed to a real entity with no disclaimer
- MEDIUM: uncited specific claim (named product + live URL + feature set) that could mislead a reader into treating an unverifiable framework as a real, locatable product
- LOW: undated "recent" claim or soft imprecision

**Notes on items deliberately NOT flagged:** the "roughly 80%" FinanceBench figure (`\cite{zhang2024financebench}`), the inverted-U context-length result (`\citet{BaloghDidisheim2025}`), the fairness impossibility result (`\citet{chouldechova2017fair}`), EU AI Act / GDPR Art. 22 / MiFID II / SR 11-7 / ECOA references (all carry `\cite{}` keys), the SR 11-7 quoted definition (cited), the benchmark figure caption (illustration block, cited to `xie2023pixiu`), the chain-of-thought DTI example (0.52 vs 0.45, clearly illustrative), the RRF constant k=60 (standard default), and Bloomberg/FactSet/Refinitiv/MSCI/EDGAR (real entities named generically without fabricated financials) — all fall under the "What NOT to Flag" rules.
