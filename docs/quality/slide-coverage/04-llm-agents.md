# Slide Coverage Checklist — Chapter 04: LLM Agents and Finance Applications

Generated from `book/chapters/04-llm-agents/chapter.tex`.

---

## Sections and Subsections

- [x] §1 From Language Models to Agents (`sec:lm-to-agents`)
- [x] §1.1 The Perceive–Reason–Act Cycle (`subsec:pra-cycle`)
- [x] §1.2 ReAct, Chain-of-Thought, and Planning Loops (`subsec:react`)
- [x] §1.3 Memory: In-Context, External Retrieval, and Long-Term Stores (`subsec:agent-memory`)
- [x] §2 Tool Use and Function Calling (`sec:tool-use`)
- [x] §2.1 The Tool Use Paradigm: Structured Outputs and API Calls (`subsec:tool-paradigm`)
- [x] §2.2 Building Custom Tools: Calculators, Databases, Web Search (`subsec:custom-tools`)
- [x] §2.3 Tool Selection, Reliability, and Error Recovery (`subsec:tool-reliability`)
- [x] §3 Skills, Hooks, and Workflow Orchestration (`sec:orchestration`)
- [x] §3.1 Skills as Modular Agent Capabilities (`subsec:skills`)
- [x] §3.2 Hooks: Event-Driven Agent Behaviours (`subsec:hooks`)
- [x] §3.3 The File-Based Pattern: Agents, Skills, and Hooks as Markdown Artifacts (`subsec:file-based-pattern`)
- [x] §3.4 Orchestration Frameworks: LangChain, LlamaIndex, and AutoGen (`subsec:frameworks`)
- [x] §3.5 Multi-Agent Systems and Role Delegation (`subsec:multi-agent`)
- [x] §4 Retrieval-Augmented Generation in Finance (`sec:rag-finance`)
- [x] §4.1 Vector Databases and Embedding Retrieval (`subsec:vector-db`)
- [x] §4.2 Hybrid Search: Dense and Sparse Retrieval Combined (`subsec:hybrid-search`)
- [x] §4.3 Chunking Strategies for Long Financial Documents (`subsec:chunking`)
- [x] §4.4 RAG Evaluation: Faithfulness, Relevance, and Grounding (`subsec:rag-eval`)
- [x] §5 Finance-Specific Agent Applications (`sec:finance-apps`)
- [x] §5.1 Earnings Call Analysis and Summarisation Pipelines (`subsec:earnings-analysis`)
- [x] §5.2 Automated Financial Report Generation (`subsec:report-generation`)
- [x] §5.3 Portfolio Construction and Research Assistants (`subsec:portfolio-agents`)
- [x] §5.4 Regulatory Filing Search and Q&A Agents (`subsec:filing-search`)
- [x] §5.5 Algorithmic Trading Signals from Text (`subsec:trading-signals`)
- [x] §6 Deployment, Safety, and Governance (`sec:agent-governance`)
- [x] §6.1 Latency, Cost, and Reliability in Production (`subsec:production`)
- [x] §6.2 Human-in-the-Loop Design Patterns (`subsec:hitl`)
- [x] §6.3 Audit Trails and Explainability for Compliance (`subsec:audit`)
- [x] §6.4 Prompt Injection and Adversarial Robustness (`subsec:adversarial`)

---

## Named Definitions, Methods, and Models

- [x] Autonomous Agent (`def:autonomous-agent`)
- [x] Perceive–Reason–Act (PRA) Loop (`def:pra-loop`) — triple (π, μ, φ)
- [x] ReAct trajectory (`def:react-trajectory`) — (Yao et al., 2022)
- [x] Chain-of-Thought (CoT) prompting — (Wei et al., 2022)
- [x] Tree-of-Thought (ToT) — (Yao et al., 2023)
- [x] Reflexion loop (`def:reflexion-loop`) — (Shinn et al., 2023)
- [x] Agent Memory Taxonomy (`def:memory-taxonomy`) — in-context / retrieval-augmented / long-term
- [x] Tool (`def:tool`) — triple (name, schema, f)
- [x] Toolformer — (Schick et al., 2023)
- [x] Gorilla — (Patil et al., 2023)
- [x] Robust Tool Calling (`def:robust-tool`)
- [x] Skill (`def:skill`) — parameterised sub-workflow
- [x] Agent Hook (`def:agent-hook`) — (event, handler) pair
- [x] File-based pattern — agents/skills/hooks as plain-text markdown under version control
- [x] LangChain — (langchain2022)
- [x] LlamaIndex — (llamaindex2022)
- [x] AutoGen — (Wu et al., 2023)
- [x] Multi-Agent System (`def:multi-agent`) — (AG, C, δ)
- [x] Hierarchical delegation pattern — (Park et al., 2023)
- [x] TradingAgents — (Xiao et al., 2024)
- [x] Crypto AI agents survey — (Ante et al., 2024)
- [x] Retrieval-Augmented Generation — probabilistic marginalisation view — (Lewis et al., 2020)
- [x] FAISS (Facebook AI Similarity Search) — (Johnson et al., 2019)
- [x] HNSW (hierarchical navigable small worlds)
- [x] Commercial vector databases (Pinecone, Weaviate, Chroma, Qdrant)
- [x] BM25 sparse retrieval — (Robertson et al., 2009)
- [x] Hybrid score formula (α · cosine + (1−α) · BM25)
- [x] Reciprocal Rank Fusion (RRF) — k=60 constant
- [x] SPLADE / learned sparse retrieval
- [x] Chunking strategy (`def:chunking`) — fixed-size, semantic, hierarchical
- [x] RAGAS metrics (`def:ragas`) — (Es et al., 2023)
- [x] FinVerse — (An et al., 2024)
- [x] Earnings analysis pipeline (5 stages: ingest, segment, extract, sentiment, synthesise)
- [x] Larcker et al. (2012) — linguistic features of earnings calls predict abnormal returns
- [x] Kogan et al. (2009) — textual features predict risk
- [x] LopezLira & Tang (2023) — zero-shot GPT-4 sentiment predicts returns
- [x] Kim et al. (2024) — GPT-4 on anonymised financials beats human analysts
- [x] FinGPT — (Yang et al., 2023)
- [x] BloombergGPT — (Wu et al., 2023)
- [x] Automated report generation pipeline — fact-grounding discipline
- [x] MiFID II substantiation requirements for algorithmic research
- [x] Portfolio Q&A tool library (`get_factor_exposures`, `compute_tracking_error`, etc.)
- [x] Data-vintage transparency for portfolio agents
- [x] Citation-enforcement wrapper for filing Q&A
- [x] FinanceBench — (Zhang et al., 2024)
- [x] FinSage — multi-aspect RAG — (Wang et al., 2025)
- [x] Tetlock (2007) — trading signals from text
- [x] Signal staleness / adverse selection (10–60s latency, half-life calibration)
- [x] Latency Budget (`def:latency-budget`)
- [x] Model tiering (small-fast vs. large-slow)
- [x] Circuit breakers / defensive architecture
- [x] HITL patterns: pre-execution, checkpoint review, post-hoc audit
- [x] Ouyang et al. (2022) — RLHF alignment
- [x] Audit Trail (`def:audit-trail`) — hash-chained records
- [x] MiFID II Article 16 record-keeping / SEC Rule 17a-4
- [x] Confused deputy problem
- [x] Capability-based security
- [x] Prompt injection — (Perez et al., 2022); indirect injection — (Greshake et al., 2023)
- [x] Defences: input sanitisation, privilege separation, invariant monitoring, dual-key
- [x] EU AI Act (2024) — high-risk classification for financial AI
- [x] SEC proposed rules on AI in investment advisers (2023)
- [x] Mata v. Avianca case — hallucinated citations in legal brief
- [x] Kurshan et al. (2024) — model-risk frameworks inadequate for LLM agents

---

## Key Numbers

- [x] 128,000-token context ≈ 100 pages for GPT-4-class models
- [x] FAISS IVF-HNSW: under 10 ms query speed, above 95% recall for top-10 (up to ~1M vectors)
- [x] RAGAS faithfulness threshold: 0.80–0.90 (commonly ~0.85) → human review
- [x] Apple 2023 10-K (170 pages): ~15 item chunks, ~300 paragraph chunks, 20–30 table chunks
- [x] Hierarchical RAG recall: 85–95% on manually labelled 10-K evaluation sets
- [x] 5-agent research system: ~4 minutes vs 2 days for a human analyst team
- [x] Earnings analysis pipeline latency: 3.2 minutes for a 90-minute transcript
- [x] Tesla EDGAR accession 0001318605-24-000004, filed 2024-01-26 (ReAct example)
- [x] Apple Q4 2023: revenue guidance $89–90B vs consensus $90.7B; Services +16% YoY
- [x] Deflection score 0.72 (high) for China exposure in Apple earnings example
- [x] Signal latency: 10–60 seconds for cloud inference
- [x] LLM generation: 50–70% of latency budget
- [x] Portfolio Q&A: tech sector 28.4% vs benchmark 27.8%, 60bps overweight
- [x] k=60 RRF constant
- [x] 512 tokens max chunk size, 64-token overlap (recommended for 10-K items)

---

## Citations (all rendered as Author, year)

- [x] Wang et al. (2023) — survey
- [x] Yao et al. (2022) — ReAct
- [x] Wei et al. (2022) — chain-of-thought
- [x] Yao et al. (2023) — Tree-of-Thought
- [x] Shinn et al. (2023) — Reflexion
- [x] Schick et al. (2023) — Toolformer
- [x] Patil et al. (2023) — Gorilla
- [x] LangChain (2022)
- [x] LlamaIndex (2022)
- [x] Wu et al. (2023) — AutoGen
- [x] Park et al. (2023) — generative agents
- [x] Xiao et al. (2024) — TradingAgents
- [x] Ante et al. (2024) — crypto AI agents
- [x] Lewis et al. (2020) — RAG
- [x] Gao et al. (2024) — RAG survey
- [x] Johnson et al. (2019) — FAISS
- [x] Robertson et al. (2009) — BM25
- [x] Es et al. (2023) — RAGAS
- [x] An et al. (2024) — FinVerse
- [x] Larcker et al. (2012)
- [x] Kogan et al. (2009)
- [x] Ko et al. (2024)
- [x] LopezLira & Tang (2023)
- [x] Kim et al. (2024)
- [x] Yang et al. (2023) — FinGPT
- [x] Wu et al. (2023) — BloombergGPT
- [x] Tetlock (2007)
- [x] Zhang et al. (2024) — FinanceBench
- [x] Wang et al. (2025) — FinSage
- [x] Ouyang et al. (2022) — RLHF
- [x] ESMA (2018) — MiFID II Article 16
- [x] Perez et al. (2022) — prompt injection
- [x] Greshake et al. (2023) — indirect injection
- [x] Kurshan et al. (2024) — agentic regulator

---

## Omissions

All checklist items above were identified as gaps versus the original deck and have been addressed in the rewrite. The following were **missing** from the original deck and are now covered:

- [x] File-based pattern (§3.3) — agents/skills/hooks as plain-text markdown artifacts
- [x] Toolformer (Schick et al., 2023) and Gorilla (Patil et al., 2023) — tool-calling model training
- [x] Portfolio Construction and Research Assistants (§5.3) — portfolio Q&A, data-vintage transparency
- [x] Algorithmic Trading Signals from Text (§5.5) — Tetlock (2007), signal staleness/adverse selection
- [x] Latency, Cost, and Reliability in Production (§6.1) — latency budget, model tiering, circuit breakers
- [x] Regulatory perspective — EU AI Act (2024), SEC rules (2023), Mata v. Avianca, Kurshan et al. (2024)
- [x] Vector database details — FAISS, HNSW, commercial VDBs (§4.1)
- [x] SPLADE / learned sparse retrieval — appendix
- [x] FinVerse (An et al., 2024), TradingAgents (Xiao et al., 2024), Ante et al. (2024)
- [x] FinanceBench (Zhang et al., 2024), FinSage (Wang et al., 2025)
- [x] Signal staleness / adverse selection remark
- [x] Figure `diagram.svg` embedded in both decks
- [x] Badge fixed in both decks (removed "MBA-friendly")
- [x] RAGAS faithfulness threshold 0.80–0.90 range (was only 0.85 in original)
- [x] Ouyang et al. (2022) — RLHF alignment (mentioned in HITL section)
- [x] Confused deputy problem and capability-based security
