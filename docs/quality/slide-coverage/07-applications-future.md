# Slide Coverage — Chapter 07: Other Applications in Finance and Future Trends

## Concept Checklist (from chapter.tex)

### Sections & Subsections
- [x] §1 LLM Applications Across Finance: A Survey
- [x] §1.1 Where We Have Been: Book map (17 chapters, Table 1)
- [x] §1.2 Remaining Application Areas
- [x] Portfolio management: natural-language mandates → quantitative optimisation
- [x] ESG screening from heterogeneous sustainability reports
- [x] Earnings-surprise prediction from calls (beats bag-of-words dictionaries)
- [x] López-Lira & Tang (2023) — earnings-call transcripts, return prediction
- [x] López-Lira (2025) — LLM agents in simulated markets; correlated strategies, systemic risk
- [x] Regulatory compliance: MiFID II suitability reports, SAR drafting
- [x] Insurance: underwriting risk extraction, claims triage, policy QA
- [x] Algorithmic trading: signal generation, strategy co-pilot, conversational OMS
- [x] §1.3 Choosing the Right LLM Architecture
- [x] Definition: three deployment patterns — zero-shot, RAG (Lewis et al., 2020), fine-tuning
- [x] FinanceBench (Zhang et al., 2024): frontier models answer ≈80% of financial QA correctly
- [x] Definition: four architecture families — encoder-only, decoder-only, enc-dec, agentic
- [x] Architecture selection table (7 task properties × 4 families)
- [x] Heuristics: latency & interpretability as tiebreakers

### Named Models/Benchmarks/Methods
- [x] FinBERT (encoder-only, finance-specialised)
- [x] BloombergGPT (domain-adapted)
- [x] GPT-4 (decoder-only, general-purpose)
- [x] LLaMA (decoder-only)
- [x] Mistral (decoder-only)
- [x] FinanceBench benchmark (Zhang et al., 2024)
- [x] FinQA benchmark (Chen et al., 2021) — numerical reasoning, exact-match accuracy
- [x] FPB benchmark (Malo et al., 2014) — three-class sentiment classification
- [x] FiQA-SA benchmark (Maia et al., 2018) — aspect-based sentiment (F1)
- [x] FinBench survey (Xie et al., 2023) — source for benchmark scores
- [x] fig_illustration.png — grouped bar chart embedded on benchmark slide

### §2 Automating Financial Workflows
- [x] Definition: financial workflow as a DAG W = (T, E)
- [x] Three automation patterns: sequential pipeline, event-triggered, orchestrator-worker
- [x] Earnings call pipeline (5-step sequential): retrieve → extract → compare → classify tone → draft
- [x] Regulatory filing monitor (event-triggered): EDGAR RSS feed → classify 8-K by type/materiality
- [x] Trade surveillance narrative (orchestrator-worker): flag → retrieve context → draft → human review
- [x] §2.3 Integration with existing financial infrastructure
- [x] Standard protocols: FIX (order routing), SWIFT (payments), XBRL (regulatory filings), BLPAPI (Bloomberg)
- [x] Tool wrappers: get_market_data(ticker, fields, start_date, end_date)
- [x] Temporal scale separation: LLMs at seconds-to-minutes, execution systems at microseconds
- [x] Audit surface: prompts + outputs must be logged, timestamped, attributable (MiFID II)

### §3 Building a Financial Research Assistant
- [x] Definition: A = (R, M, K, Λ, I) — retrieval, reader, memory, tools, interface
- [x] Hybrid retrieval: dense embeddings + BM25, reciprocal rank fusion k=60
- [x] RRF formula: s_RRF = 1/(k + r_dense) + 1/(k + r_sparse)
- [x] Semantic chunking: 10-K by SEC Items (1A, 7, 8) not fixed-size 512-token blocks
- [x] Embedding model selection: text-embedding-3-large, e5-mistral-7b; general vs. domain-specific
- [x] Source attribution: every claim must cite a retrieved passage
- [x] OpenClaw (openclaw.ai): 4 principles — privacy by default, meet users where they work, model flexibility, extensibility through skills
- [x] OpenClaw skills: /earnings AAPL, filing monitor, portfolio Q&A, macro digest
- [x] Production concerns: corpus freshness, hallucination mitigation, tiered routing (Balogh & Didisheim 2025 — inverted-U context length)
- [x] User feedback as quality signal (thumbs-up/down, reformulation as implicit signal)

### §4 Ethical Considerations and Bias Mitigation
- [x] Training-data bias (English-language, US-centric) — systematic pricing error
- [x] Historical discrimination encoded in data (lending records → reproduced patterns)
- [x] Feedback-loop bias (Soros reflexivity at faster timescale)
- [x] Anchoring bias (Tversky & Kahneman, 1974) — reproduced by LLMs
- [x] Definition: demographic parity
- [x] Definition: equalized odds
- [x] Definition: calibration within group
- [x] Proposition: fairness impossibility (Chouldechova, 2017) — cannot simultaneously satisfy all three when base rates differ
- [x] Mitigation: pre-processing (rebalancing, causal augmentation)
- [x] Mitigation: in-processing (adversarial debiasing, constrained optimisation)
- [x] Mitigation: post-processing (threshold adjustment)
- [x] Human-in-the-loop oversight (mandatory for high-stakes decisions)
- [x] EU AI Act (2024) — credit scoring as high-risk AI (Annex III)
- [x] ECOA / Fair Housing Act — adverse-action notice tension with LLM opacity
- [x] GDPR Article 22 — right not to be subject to purely automated decisions
- [x] MiFID II — record-keeping of LLM-generated outputs
- [x] FSB 2023 report — systemic risk concerns: concentration, herding, opacity
- [x] FSB 2024 report — AI amplifies third-party concentration risk, market correlations, financial disinformation

### §5 Deploying LLMs in Regulated Environments
- [x] SR 11-7 (Federal Reserve) definition: when an LLM = a model for regulatory purposes
- [x] SR 11-7 three lines of defence: Development, Independent Validation, Internal Audit
- [x] FAIR framework (Noguer, 2025) — LLM-specific failure modes: temporal inconsistencies, hallucination in numerical extraction, privacy leakage
- [x] SR 11-7 documentation checklist (7-item example): model description, intended use, performance report, sensitivity analysis, adversarial testing, monitoring plan, decommission plan
- [x] Adversarial testing: prompt injection, jailbreaking, distribution-shift tests
- [x] Explainability — post-hoc attribution (SHAP, attention saliency) vs. procedural transparency (chain-of-thought)
- [x] Chain-of-thought as auditable reasoning trace (Wei et al., 2022)
- [x] GDPR Article 22 — meaningful information about automated decision logic
- [x] MiFID II — prompt, model version, output, timestamp as first-class transactions
- [x] Monitoring: input distribution (KL divergence on prompt embeddings), output quality, operational (latency/cost/errors/refusals), fairness
- [x] Incident response: pre-defined severity tiers; low vs. high escalation pathways

### §6 Future Trends and Open Research Problems
- [x] Multimodal LLMs: text + images (charts) + audio (prosodic cues) + structured data
- [x] Long-context models: processing entire 10-K in one pass, linking Item 1A → Item 3 → Item 7
- [x] "Lost in the middle" phenomenon — recall degrades for passages far from context ends
- [x] Autonomous agents: quantitative research, trading strategy self-improvement
- [x] Systemic risk of autonomous agents (Bommasani et al., 2021; López-Lira, 2025)
- [x] Governance principle: informational / advisory / executive output categories
- [x] Open problem 1: calibrated uncertainty quantification (Chen et al., 2024) — token-level log-probabilities as principled uncertainty estimates
- [x] Open problem 2: cross-market comparables in thin markets — US-biased embeddings
- [x] Open problem 3: cross-lingual finance LLMs (J-GAAP, HGB, local GAAP) — no corpora/evaluation frameworks
- [x] Open problem 4: feedback loops & memorisation (Didisheim, 2025) — look-ahead bias worst at low frequencies for large models
- [x] Open problem 5: faithful chain-of-thought — "unfaithful reasoning" gap between stated and actual computation
- [x] Path forward (three disciplines): measure everything, document honestly, escalate appropriately
- [x] Note on model versions and reproducibility (claude-opus-4-5 etc.)

### Key Numbers & Citations
- [x] ≈80% — FinanceBench frontier model accuracy on first attempt (Zhang et al., 2024)
- [x] k = 60 — RRF smoothing constant
- [x] Inverted-U context length pattern — Balogh & Didisheim (2025)
- [x] damodaran2012investment — portfolio optimisation, qualitative + quantitative constraints
- [x] kolbel2020esg — ESG signals from sustainability reports
- [x] lopezdeprado2018advances — portfolio construction, NL mandate translation
- [x] mehrabi2021survey — bias in ML systems (cited for sources-of-bias and fairness metrics)
- [x] kearns2019ethical — fairness discussion

## Omissions

All concepts from chapter.tex are now covered in the lesson deck. No unchecked items remain under Omissions.
