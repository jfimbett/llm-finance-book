# Constructive Review — Ch 04 LLM Agents and Finance Applications

Reading index 6 · slug `04-llm-agents` · file `book/chapters/04-llm-agents/chapter.tex` · audit date 2026-06-20.

This chapter is the designated single source of truth (SSOT) for AGENTS / ReAct / tool use in the book. Overall it is a strong, finance-first treatment with clean formal scaffolding. Below is the content worth protecting, tagged with the preservation vocabulary.

## KEEP_AS_SINGLE_SOURCE_OF_TRUTH

- **`def:autonomous-agent` (chapter.tex:64–70)** and **`def:pra-loop` (chapter.tex:92–109)** — the PRA loop `(\pi,\mu,\phi)` is the canonical agent definition for the whole book. Anchors every later chapter that uses "agent."
- **`def:react-trajectory` (chapter.tex:158–168)** and §`subsec:react` (chapter.tex:147–257) — ReAct is correctly owned here, grounded in `\citet{yao2022react}`, with the CoT-vs-ReAct program-synthesis framing (chapter.tex:184–199). This is the SSOT; later chapters should `\Cref{ch:llm-agents}` rather than re-derive (see BOOK_WIDE in editor-plan).
- **`def:tool` (chapter.tex:352–365)**, **`def:robust-tool` (chapter.tex:480–494)** — clean formalisation of tools and error-recovery contract.
- **`def:rag` (chapter.tex:762–779)** — the marginalization view of RAG (Eq. `eq:rag-marginal`) is the deeper treatment; keep, but resolve the duplicate-label collision with ch02 (see skeptical-review).

## GOOD_TECHNICAL_EXPLANATION

- **Memory taxonomy `def:memory-taxonomy` (chapter.tex:268–283)** — in-context / retrieval-augmented / long-term, each with latency and boundedness trade-offs. Precise and reusable. KEEP.
- **Hybrid search (chapter.tex:834–881)** — dense vs sparse, BM25, RRF with `k=60`, SPLADE, and the `\alpha` mixing equation `eq:hybrid-search`. Technically accurate and well-motivated by finance exact-match needs (CUSIP, "Article 7(1)(b) of MiFIR"). KEEP.
- **Chunking families `def:chunking` (chapter.tex:913–920)** plus the EDGAR-item hierarchical recipe (chapter.tex:922–926). GOOD_TECHNICAL_EXPLANATION.
- **RAGAS metrics `def:ragas` (chapter.tex:957–973)** — faithfulness / answer relevance / context precision / context recall, correctly decomposed. KEEP.
- **Audit trail `def:audit-trail` (chapter.tex:385–1394)** with the chained-hash tamper-evidence construction `H(payload || hash_{t-1})` and the SHA-256 clarification. GOOD_TECHNICAL_EXPLANATION.
- **Prompt-injection / confused-deputy / capability-based security treatment (chapter.tex:1411–1469)** — accurate security framing, `\citet{perez2022ignore}` and `\citet{greshake2023not}` correctly attributed to direct/indirect injection. KEEP.

## GOOD_BIG_PICTURE_EXPLANATION

- **Opening `context` box (chapter.tex:32–52)** — the portfolio-manager multi-document scenario motivates agents from a real finance problem before any formalism. Excellent finance-first framing. KEEP.
- Each section opens with a `context` box (Morgan Stanley live-yield example chapter.tex:321–330; 50,000-document research library chapter.tex:741–751; Mata v. Avianca governance hook chapter.tex:1271–1278). Strong concept_separation: `context` for the big picture, `deepdive` for internals.

## GOOD_FINANCE_EXAMPLE

- **`ex:react-filing` (chapter.tex:229–257)** — full ReAct trace for a Tesla 10-K liquidity query (EDGAR search → section retrieval → finish). Concrete and runnable in spirit. KEEP.
- **`ex:db-tools` (chapter.tex:438–452)** — semantic read-only tool suite (`get_financial_statement`, `compute_ratio`, `compare_peers`). KEEP.
- **`ex:multi-agent-research` (chapter.tex:706–725)** — five-agent equity-research pipeline. KEEP.
- **`ex:portfolio-qa` (chapter.tex:1160–1174)** — data-vintage caveat ("As of yesterday's close … please refresh after market close") is a genuinely valuable practitioner warning. GOOD_FINANCE_EXAMPLE.
- **`ex:earnings-output` (chapter.tex:1072–1087)** — explicitly fenced by the `Illustrative output` remark (chapter.tex:1068–1070) declaring all figures hypothetical. Honest handling of synthetic numbers. KEEP_BUT_CLARIFY only insofar as it depends on the missing notebook.
- **`rem:signal-staleness` (chapter.tex:1250–1261)** — adverse-selection / HFT half-life caveat for text signals. GOOD_FINANCE_EXAMPLE / KEEP.

## GOOD_FINANCE citation integration

- The chapter weaves in recent finance-specific agent papers well: `xiao2024tradingagents` (TradingAgents, chapter.tex:688–694), `an2024finverse` (FinVerse, 600+ APIs, chapter.tex:1025–1028), `wang2025finsage` and `zhang2024financebench` (FinanceBench gap, chapter.tex:1201–1209), `kim2024financial` (GPT-4 statement analysis, chapter.tex:1048–1053). These keep the techniques anchored to finance. KEEP (verify accuracy — see skeptical-review).

## Figure

- **`fig:ch04-illustration` (chapter.tex:985–996)** + `illustration` box (chapter.tex:998–1010) — TF-IDF cosine-similarity retrieval ranking. The figure-generating code in `code/notebooks/04-llm-agents/exercises.ipynb` (cells 1, 3) matches the caption exactly (5 tickers AAPL/MSFT/JPM/GS/BAC, RdYlGn colour, dashed mean line) and runs cleanly in `exercises_executed.ipynb`. KEEP.
