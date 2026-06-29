# Slide Coverage Checklist — Chapter 05: LLMs for Business Valuation

Generated from `book/chapters/05-business-valuation/chapter.tex`.

---

## Sections and Subsections

- [x] §1 Introduction to Business Valuation (`sec:bv-intro`)
  - [x] §1.1 What Is Business Valuation? (`subsec:bv-intro-definition`)
  - [x] §1.2 Key Valuation Methodologies (`subsec:bv-intro-methodologies`)
  - [x] §1.3 Chapter Roadmap: How LLMs Transform Each Step (`subsec:bv-intro-roadmap`)
- [x] §2 Extracting Financial Data with LLMs and Agents (`sec:bv-extraction`)
  - [x] §2.1 The SEC EDGAR Ecosystem and Structured Filings (`subsec:bv-extraction-edgar`)
  - [x] §2.2 Building an Automated EDGAR Extraction Pipeline (`subsec:bv-extraction-pipeline`)
  - [x] §2.3 Parsing Financial Tables and Statements with LLMs (`subsec:bv-extraction-parsing`)
  - [x] §2.4 Structuring Extracted Data for Downstream Computation (`subsec:bv-extraction-structuring`)
- [x] §3 Computing Cash Flows (`sec:bv-cashflows`)
  - [x] §3.1 Free Cash Flow: Definitions and Formulas (`subsec:bv-cashflows-definitions`)
  - [x] §3.2 Programmatic Computation from Extracted Data (`subsec:bv-cashflows-computation`)
  - [x] §3.3 Handling Missing Data and Normalisation with LLM Assistance (`subsec:bv-cashflows-missing`)
- [x] §4 Forecasting Cash Flows with LLMs (`sec:bv-forecasting`)
  - [x] §4.1 Time-Series Perspectives on Financial Forecasting (`subsec:bv-forecasting-timeseries`)
  - [x] §4.2 Prompt-Based Forecasting: Chain-of-Thought Approaches (`subsec:bv-forecasting-cot`)
  - [x] §4.3 Fine-Tuning vs. Few-Shot Approaches (`subsec:bv-forecasting-finetuning`)
  - [x] §4.4 Evaluating Forecast Quality (`subsec:bv-forecasting-evaluation`)
- [x] §5 Tool-Augmented Agents for Financial Math (`sec:bv-tools`)
  - [x] §5.1 Why LLMs Alone Struggle with Arithmetic (`subsec:bv-tools-limitations`)
  - [x] §5.2 Code Interpreter and Calculator Tools (`subsec:bv-tools-code-interpreter`)
  - [x] §5.3 ReAct and Tool-Use Patterns (`subsec:bv-tools-react`)
  - [x] §5.4 Hallucinations and Limitations in Numerical Reasoning (`subsec:bv-tools-hallucinations`)
- [x] §6 Scenario Analysis with LLMs (`sec:bv-scenarios`)
  - [x] §6.1 Bull, Base, and Bear Case Construction (`subsec:bv-scenarios-cases`)
  - [x] §6.2 Monte Carlo Simulation Orchestrated by Agents (`subsec:bv-scenarios-montecarlo`)
  - [x] §6.3 Sensitivity Analysis and Narrative Generation (`subsec:bv-scenarios-sensitivity`)
- [x] §7 Comparable Selection Using LLMs (`sec:bv-comparables`)
  - [x] §7.1 Traditional Comparable Selection: Criteria and Pitfalls (`subsec:bv-comparables-traditional`)
  - [x] §7.2 Prompt-Based Comparable Identification (`subsec:bv-comparables-prompts`)
  - [x] §7.3 Embedding-Based Approaches (`subsec:bv-comparables-embeddings`)
  - [x] §7.4 Hybrid Methods (`subsec:bv-comparables-hybrid`)
- [x] §8 End-to-End Valuation Pipeline (`sec:bv-pipeline`)
  - [x] §8.1 Integrating Extraction, Forecasting, and Comparables (`subsec:bv-pipeline-integration`)
  - [x] §8.2 Agent Orchestration for Multi-Step Valuation (`subsec:bv-pipeline-orchestration`)
  - [x] §8.3 Case Study: Full Pipeline on a Public Company (`subsec:bv-pipeline-casestudy`)
  - [x] Remark: AAPL companion exercise (`rem:valuation-companion`)
- [x] §9 Efficiency and Accuracy in LLM-Assisted Valuation (`sec:bv-efficiency`)
  - [x] §9.1 Benchmarking LLM Valuations Against Analyst Estimates (`subsec:bv-efficiency-benchmarking`)
  - [x] §9.2 Cost, Latency, and Token Efficiency (`subsec:bv-efficiency-cost`)
  - [x] §9.3 Error Propagation in Multi-Step Agent Workflows (`subsec:bv-efficiency-errors`)
  - [x] §9.4 Best Practices and Deployment Considerations (`subsec:bv-efficiency-bestpractices`)

---

## Named Methods, Models, and Results

- [x] Definition: Business Valuation (`def:business-valuation`) — V ∈ ℝ₊
- [x] DCF enterprise value formula (`eq:dcf`)
- [x] Terminal value / Gordon Growth Model (`eq:terminal-value`)
- [x] 100-bps change in WACC or g → 20–40% terminal-value change
- [x] Definition: WACC and CAPM (`def:wacc`, `eq:wacc`, `eq:capm`)
- [x] Market approach: trading multiples (EV/EBITDA, P/E, P/Book)
- [x] Asset approach: net asset value (`eq:nav`)
- [x] IFRS 13 / ASC 820 fair-value hierarchy (Level 1 / 2 / 3)
- [x] XBRL standard (SEC since 2009)
- [x] SEC EDGAR APIs: submissions API, full-text search, companyfacts XBRL API
- [x] Form types: 10-K, 10-Q, 8-K, DEF 14A
- [x] Rate limit: ~10 requests per second
- [x] Accession number format: XXXXXXXXXX-YY-ZZZZZZ
- [x] BeautifulSoup → compact plain-text → JSON extraction pattern
- [x] XBRL as ground truth / cross-check (Remark: xbrl-groundtruth)
- [x] Financial data model: company identifier, fiscal period end, filing date (look-ahead bias), restatement_flag, provenance
- [x] Currency-unit mismatch (thousands vs. millions), fiscal-year offset, restatements
- [x] Definition: FCFF (`def:fcff`, `eq:fcff`)
- [x] Definition: FCFE (`def:fcfe`, `eq:fcfe`)
- [x] Proposition: FCFF–FCFE relationship (`prop:fcff-fcfe-relation`, `eq:fcff-fcfe`) — Modigliani–Miller with taxes
- [x] Example: FCFF computation — hypothetical software company (Revenue 4,200; EBIT 840; D&A 310; CapEx 180; NWC 620/540; τ 21%) → FCFF = 713.6 M; EV ≈ $15.2B ≈ 3.6× trailing revenue
- [x] One-time items, capitalised operating leases (IFRS 16, ASC 842), acquired intangible amortisation
- [x] Normalisation prompt — JSON with description, amount, line_item, confidence
- [x] Human-in-the-loop: high-confidence auto-strip; medium-confidence flag; low-confidence pass through
- [x] Adjusted EBIT formula: EBIT* = EBIT + Σ a_k
- [x] Random walk with drift (`eq:rw-fcf`)
- [x] Mean-reverting FCF model (`eq:mean-reversion`), φ ≈ 0.5–0.7 for earnings
- [x] Chain-of-thought (CoT) prompting — Wei et al. (2022)
- [x] Four-stage CoT: macro → industry → firm → synthesis
- [x] Few-shot: 3–10 examples; diverse macro/industry types reduce forecast variance
- [x] Fine-tuning: historical (filing, realisation) dataset; captures domain patterns
- [x] LoRA / PEFT — Hu et al. (2022); small fraction of parameters trained
- [x] LLM signals without fine-tuning carry return-predictive information — López-Lira and Tang (2023)
- [x] Definition: MAPE (`def:mape`, `eq:mape`)
- [x] Definition: RMSE (`def:rmse`, `eq:rmse`)
- [x] Definition: Directional Accuracy (`def:da`, `eq:da`)
- [x] GPT-4 arithmetic reliability degrades on multi-step financial calculations — Frieder et al. (2023)
- [x] 5-year DCF involves ~15–20 chained arithmetic operations
- [x] Toolformer — Schick et al. (2023): models learn when to call tools
- [x] ReAct (Reason + Act) — Yao et al. (2022): Thought / Action / Observation loop
- [x] Four hallucination failure modes: phantom tickers, invented ratios, misapplied formulas, stale knowledge
- [x] Definition: Valuation Scenarios — bull (P90), base (P50), bear (P10)
- [x] Internal consistency requirement; contradictory scenario: 25% revenue growth + 1% terminal growth
- [x] LLMs for narrative coherence checking
- [x] Definition: Monte Carlo DCF (`def:monte-carlo-dcf`, `eq:monte-carlo-ev`)
- [x] Typical parameters: μ_WACC = 0.09, σ_WACC = 0.015, μ_g = 0.03, σ_g = 0.01; M = 10,000; runtime < 1 s
- [x] Sensitivity table: WACC × terminal growth → enterprise value
- [x] Figure: DCF sensitivity heatmap for AAPL (`fig:ch05-illustration`) — `fig_illustration.png`
- [x] AAPL FY2024 free cash flow: $108.8B from 10-K; $98.8B from yfinance API (vendor discrepancy)
- [x] Traditional comparable selection: SIC (last revised 1987), GICS, NAICS; size filter 0.3–3.0× revenue/market cap
- [x] Three pitfalls: code obsolescence, diversified conglomerates, cyclical timing
- [x] Prompt-based peers: zero-shot; mandatory ticker validation; few-shot reduces hallucination rate
- [x] Embedding function φ: D → ℝ^d; cosine similarity for peer retrieval
- [x] MD&A as semantically rich source; tighter IQR of EV/EBITDA vs. SIC-code sets
- [x] Two-stage hybrid: top-30 embedding candidates → LLM filter → 8–12 comparables
- [x] 10-step pipeline (EDGAR retrieval through report generation)
- [x] Pydantic / schema validators for data contracts
- [x] Orchestrator + five specialists: edgar_agent, fcf_agent, forecast_agent, comps_agent, dcf_agent
- [x] Parallel execution: comparable selection independent of FCF forecast
- [x] Case study SaaS firm: Revenue $4.2B +12%, EBIT 20%, D&A $310M, CapEx $180M, net debt $800M, 280M shares
- [x] Non-recurring: $45M restructuring + $30M acquired intangible amortisation
- [x] After normalisation: EBIT $915M, FCFF $789M (τ = 21%)
- [x] FCF projections (base / upside / bear) years 1–5
- [x] DCF EV $17.0B; equity $16.2B; $57.9/share
- [x] 9 embedding-based peers; median EV/EBITDA 24.5×; EBITDA $1.22B; comparables EV $29.9B
- [x] Monte Carlo (10,000 draws): mean $17.2B, P10–P90 $12.5B–$24.1B
- [x] AAPL remark: r_f = 3.78%, β = 1.24, ERP = 4.23% → r_E ≈ 9.0%; after-tax cost of debt 2.2%; WACC ≈ 8.84%
- [x] AAPL two-stage DCF → ~$225/share; EV/EBITDA cross-check → ~$217/share; triangulation $221.04/share within 2.6% of $226.84
- [x] MAVE metric: mean absolute valuation error
- [x] Coverage rates: >90% large-cap, >75% smaller companies
- [x] Token counts: 10-K ≈ 50,000 tokens; extraction context 3,000–8,000; forecasting 1,000–2,000
- [x] 6 LLM calls; ~$1–$5/company (2024 frontier-model pricing); 3,000 companies quarterly → ~$3,000–$15,000/quarter
- [x] Error propagation formula (`eq:error-propagation`): ΔV ≈ (∂V/∂FCF)ε₁ + (∂V/∂g)ε₂
- [x] ∂V/∂FCF_n = (1+g)/(WACC−g); ∂V/∂g = FCF_n(1+WACC)/(WACC−g)²
- [x] 1% FCF error → 1% EV error; 100-bps g error → ~15–18% EV error
- [x] Five best practices: XBRL first, code interpreter, Monte Carlo, hallucination guards, human review
- [x] FSB (2023) governance: human accountability, model transparency, robust back-testing

---

## Key Citations

- [x] (Damodaran, 2012) — `damodaran2012investment`
- [x] (Berk, 2020) — `berk2020corporate`
- [x] (IASB, 2011) — `iasb2011ifrs13` (IFRS 13 fair value)
- [x] (SEC, 2009) — `sec2009xbrl` (XBRL mandate)
- [x] (Koller et al., 2020) — `koller2020valuation` (acquired intangible amortisation)
- [x] (Ball and Brown, 1972) — `ball1972earnings` (random walk)
- [x] (Fama and French, 2000) — `fama2000forecasting` (mean reversion, φ ≈ 0.5–0.7)
- [x] (Lewellen, 2010) — `lewellen2010empirical` (analyst consensus)
- [x] (Wei et al., 2022) — `wei2022chain` (chain-of-thought)
- [x] (Brown et al., 2020) — `brown2020language` (few-shot, diverse examples)
- [x] (López-Lira and Tang, 2023) — `LopezLiraTang2023` (LLM signals without fine-tuning)
- [x] (Hu et al., 2022) — `hu2022lora` (LoRA / PEFT)
- [x] (Zhang et al., 2024) — `zhang2024financebench` (FinanceBench benchmark)
- [x] (Frieder et al., 2023) — `frieder2023mathematical` (GPT-4 arithmetic reliability)
- [x] (Schick et al., 2023) — `schick2023toolformer` (Toolformer)
- [x] (Yao et al., 2022) — `yao2022react` (ReAct)
- [x] (FSB, 2023) — `fsb2023ai` (AI governance in finance)

---

## Omissions

*(All items listed above are covered in the revised lesson deck. No unchecked items remain.)*
