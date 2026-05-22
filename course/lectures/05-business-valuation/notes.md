# Lecture 5: LLMs for Business Valuation

## Learning Objectives

By the end of this lecture, students should be able to:

1. Define business valuation and situate the income, market, and asset approaches within financial theory.
2. Build an automated pipeline that retrieves, parses, and structures SEC EDGAR filings using LLM-assisted extraction.
3. Derive FCFF and FCFE from raw financial statements and implement the computation programmatically.
4. Design and evaluate prompt-based cash-flow forecasting strategies using chain-of-thought reasoning, with MAPE, RMSE, and directional accuracy metrics.
5. Explain why LLMs require external tools for reliable arithmetic and implement a ReAct agent that routes calculations to a code interpreter.
6. Construct bull, base, and bear valuation scenarios and orchestrate a Monte Carlo simulation over WACC and growth-rate distributions.
7. Apply embedding-based and prompt-based methods to identify peer companies, and combine them in a hybrid pipeline.
8. Assemble an end-to-end valuation agent, estimate first-order error propagation, and apply best practices for production deployment.

---

## 1. The Business Valuation Problem

### What Is Business Valuation?

A private equity firm identifies a mid-cap software company as an acquisition target. Before the partners can table a bid, they must answer a deceptively simple question: *what is this company worth?* The answer depends on future cash flows not yet realised, on discount rates derived from noisy market data, and on comparisons with peers that are never quite identical to the target. Every assumption is defensible; every assumption is contestable.

**Business valuation** is the process of determining the economic value of an ownership interest in a firm or specific set of its assets. Formally, it maps observable and projected financial variables—cash flows, discount rates, growth rates—into a scalar value $V \in \mathbb{R}_+$ that a rational, fully informed market participant would assign to the claim.

Valuation arises across diverse professional contexts:
- **M&A**: buyer and seller commission independent analyses; the spread between their estimates defines the zone of possible agreement.
- **IPOs**: investment banks produce valuation ranges to price new shares, balancing the issuer's desire for a high price against the underwriters' need for a successful book-building.
- **Portfolio management**: a widening gap between model value and market price generates a trade signal at long/short equity funds.
- **Financial reporting**: IFRS 13 and ASC 820 classify fair-value measurements at Level 1 (quoted prices), Level 2 (observable inputs), and Level 3 (unobservable inputs). Level 3 assets require a documented valuation model subject to auditor scrutiny.

### Three Valuation Frameworks

**Income approach** — values a firm by the present value of economic benefits it will generate. The canonical implementation is the discounted cash flow (DCF) model. Let $\text{FCF}_t$ be free cash flow in period $t$, $n$ the forecast horizon, and WACC the weighted-average cost of capital:

$$V = \sum_{t=1}^{n} \frac{\text{FCF}_t}{(1+\text{WACC})^t} + \frac{TV}{(1+\text{WACC})^n}$$

Under the Gordon Growth Model (constant perpetual growth rate $g < \text{WACC}$ after period $n$):

$$TV = \frac{\text{FCF}_{n+1}}{\text{WACC} - g}$$

**Sensitivity**: a 100-basis-point change in either WACC or $g$ typically alters the terminal value by 20–40% for a firm with moderate growth. This is why scenario analysis is indispensable.

**Market approach** — values a firm by reference to prices at which comparable businesses have traded. The most common implementation uses trading multiples (EV/EBITDA, P/E, P/Book) observed for a peer group and applied to the target's financial metrics. Simple and market-grounded; the challenge is finding genuinely comparable peers—a task where LLMs and embedding methods excel.

**Asset approach** — values a firm by the fair value of its assets minus liabilities:

$$V_{\text{NAV}} = \sum_i FV(\text{Asset}_i) - \sum_j FV(\text{Liability}_j)$$

Best suited to asset-intensive firms or as a floor valuation cross-check.

In practice, a rigorous analysis triangulates all three approaches and presents a valuation *range* rather than a point estimate.

### How LLMs Transform Each Step

A standard DCF valuation has six analytical steps: (1) collect and clean financial data, (2) compute historical free cash flows, (3) forecast future cash flows, (4) estimate the discount rate, (5) calculate terminal value, (6) stress-test through scenario analysis. Each step has traditionally required skilled human labour or specialised software. LLMs, augmented with tools and organised into agents, can now automate or substantially accelerate every one.

---

## 2. Extracting Financial Data with LLMs and Agents

### The SEC EDGAR Ecosystem

The SEC requires every public US company to submit standardised periodic reports to EDGAR (Electronic Data Gathering, Analysis, and Retrieval). For valuation, the critical filing types are:

- **Form 10-K**: Annual report with audited financial statements (income statement, balance sheet, cash flow statement), MD&A, and footnote disclosures. The canonical source of historical financial data.
- **Form 10-Q**: Quarterly unaudited interim statements. Three are filed each fiscal year.
- **Form 8-K**: Current report filed within 4 business days of any material event (earnings release, merger agreement, CEO departure, credit-rating change).
- **Form DEF 14A**: Proxy statement with executive compensation tables and board composition—inputs to corporate governance adjustments in valuation.

EDGAR exposes two programmatic interfaces:
- **Submissions API**: `https://data.sec.gov/submissions/CIK{cik}.json` — returns filing metadata (accession numbers, dates, form types) for a given CIK.
- **Full-text search**: `https://efts.sec.gov/LATEST/search-index?q="goodwill impairment"&forms=10-K` — queries across content of all filings.

Since 2009, the SEC requires XBRL tagging: each reported figure maps to a concept in the US-GAAP or IFRS taxonomy. In principle this makes extraction straightforward. In practice, filers exercise discretion in tag choice, use non-standard extension elements for firm-specific line items, and sometimes apply the taxonomy inconsistently. **LLMs fill this gap** by parsing residual HTML and plain-text content that XBRL misses.

### Building the Extraction Pipeline

The pipeline follows three steps: (1) resolve a ticker to a CIK using the EDGAR company tickers file, (2) fetch the filing index to locate the primary document, (3) download the HTML for parsing.

Key engineering constraints:
- The SEC requires a `User-Agent` header identifying the requesting party; omitting it causes throttling or blocking.
- Rate limit is approximately 10 requests/second; use exponential backoff for large-scale workflows.
- Accession numbers follow `XXXXXXXXXX-YY-ZZZZZZ`; strip hyphens to get the directory path in the `/Archives/` URL tree.

### Parsing Financial Tables with LLMs

A raw 10-K is an HTML file exceeding 200 pages. Financial statements occupy perhaps 10 pages but are embedded in legal boilerplate, footnotes, and risk-factor disclosures. Classical rule-based approaches—searching for header strings and extracting rows by HTML tags—work for consistent formats but fail on the long tail of non-standard layouts, merged cells, multi-level headers, and footnote references within cells.

**LLMs handle this variation** because they understand the semantics of content, not merely its structure.

Recommended pattern:
1. Extract raw HTML of each candidate table using BeautifulSoup.
2. Convert to compact plain-text preserving column headers and indentation, stripping HTML tags.
3. Send to an LLM with a structured extraction prompt requesting a specific JSON schema (income statement, balance sheet, or cash flow statement).

Requesting JSON directly—rather than free-form text—reduces post-processing effort and enables automatic schema validation. Modern LLMs with JSON mode virtually eliminate format violations. Without forced JSON, adding "Respond only with valid JSON. Do not include markdown code fences" and retrying on `json.loads` failure achieves near-perfect reliability.

**Key design principle**: use XBRL as the primary source and LLM extraction as a cross-check or gap-filler. The SEC's `companyfacts` API at `https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json` returns every tagged data point across all filings in one JSON response.

### Structuring Extracted Data

The minimum data model for DCF valuation requires 3–5 years of historical data per statement, with a consistent mapping from filing-specific line-item names to a canonical schema. A production schema includes: company identifier (ticker and CIK), fiscal period end date, **filing date** (critical to avoid look-ahead bias in backtests), and a dictionary of standardised financial quantities with units and provenance.

Common normalisation issues: currency-unit mismatch (thousands vs. millions), fiscal-year offset (not all fiscal years end December 31), and restatements (refiled 10-Ks supersede originals). The extracted data object should carry a `restatement_flag` and the provenance of each figure (XBRL tag or LLM extraction with model name and date) for auditing.

---

## 3. Computing Cash Flows

### Free Cash Flow Definitions

The foundation of the income approach is free cash flow. Two canonical definitions (Damodaran, 2012):

**Free Cash Flow to the Firm (FCFF)** — after-tax operating cash flow available to all capital providers (debt and equity) after funding net investment:

$$\text{FCFF}_t = \text{EBIT}_t \times (1 - \tau) + \text{DA}_t - \text{CapEx}_t - \Delta\text{NWC}_t$$

where $\tau$ is the marginal corporate tax rate, DA is depreciation and amortisation, CapEx is capital expenditure (net of asset disposals), and $\Delta\text{NWC}_t$ is the change in net working capital (current assets excluding cash minus current liabilities excluding short-term debt).

**Free Cash Flow to Equity (FCFE)** — residual cash flow available to common shareholders after meeting all obligations including debt service:

$$\text{FCFE}_t = \text{NI}_t + \text{DA}_t - \text{CapEx}_t - \Delta\text{NWC}_t + \text{NB}_t$$

where NI is net income and NB is net new borrowing (debt issued minus debt repaid).

**Relationship between FCFF and FCFE** (under Modigliani-Miller with corporate taxes):

$$\text{FCFE}_t = \text{FCFF}_t - \text{InterestExp}_t \times (1-\tau) + \text{NB}_t$$

*Proof sketch*: from the FCFF formula, note that $\text{NI}_t = [\text{EBIT}_t - \text{InterestExp}_t](1-\tau)$, so FCFF rewrites in terms of NI. Substituting into the FCFE definition and rearranging yields the result.

**Which to use?** FCFF is discounted at WACC to yield enterprise value; FCFE is discounted at the cost of equity to yield equity value directly. When leverage is stable, both give the same equity value. When capital structure is changing materially, FCFF is more robust because WACC can be held constant while FCFE requires adjustments to the cost of equity as leverage changes.

### Worked Example

A hypothetical software company (USD millions):
- EBIT: 840, DA: 310, CapEx: 180, NWC (current): 620, NWC (prior): 540, $\tau = 21\%$

$$\Delta\text{NWC} = 620 - 540 = 80$$
$$\text{FCFF} = 840 \times (1-0.21) + 310 - 180 - 80 = 663.6 + 310 - 180 - 80 = 713.6 \text{ M}$$

With WACC = 9%, five-year growth at 8%, terminal growth rate 3%: enterprise value ≈ $15.2B (roughly 3.6× trailing revenue, consistent with high-quality software-sector medians for firms with strong near-term growth).

### Handling Missing Data and Non-Recurring Items

Financial statements frequently contain items that distort FCFF if treated naively:

1. **One-time items** — restructuring charges, litigation settlements, impairment write-downs. They distort EBIT in the reporting period but do not reflect recurring earning power. Remove from base EBIT used for forecasting.
2. **Capitalised operating leases** — brought onto the balance sheet under IFRS 16 and ASC 842, creating a mismatch between reported EBIT, depreciation, and cash flows that must be carefully reconciled.
3. **Acquired intangible amortisation** — from purchase accounting. Often excluded by analysts calculating "adjusted EBIT" or "cash EBIT."

LLMs flag these issues from MD&A and footnote text. A structured prompt instructs the model to identify non-recurring items, returning a JSON array with description, amount, affected line item, and confidence (High / Medium / Low).

Human-in-the-loop design: high-confidence items are automatically stripped from EBIT; medium-confidence items are flagged for analyst review; low-confidence items pass through unchanged. The normalised EBIT is:

$$\text{EBIT}^* = \text{EBIT} + \sum_{k \in \mathcal{K}} a_k$$

where $\mathcal{K}$ is the set of identified non-recurring expense items and $a_k > 0$ is the pre-tax amount of item $k$ (adding back an expense that should be excluded from recurring income).

---

## 4. Forecasting Cash Flows with LLMs

### Classical Baselines

The simplest forecasting model is the **random walk with drift**:

$$\text{FCF}_{t+1} = \mu + \text{FCF}_t + \varepsilon_{t+1}, \quad \varepsilon_{t+1} \sim \mathcal{N}(0, \sigma^2)$$

More elaborate specifications allow for mean reversion toward a long-run level $\bar{\text{FCF}}$:

$$\text{FCF}_{t+1} - \bar{\text{FCF}} = \phi(\text{FCF}_t - \bar{\text{FCF}}) + \varepsilon_{t+1}$$

where $|\phi| < 1$ is the speed of mean reversion. Empirical estimates of $\phi$ for earnings are typically 0.5–0.7: substantial persistence but non-trivial mean reversion (Fama, 2000).

The key limitation of pure time-series models: they rely exclusively on historical values. They ignore qualitative information in management guidance, industry trends, and macroeconomic conditions that analysts routinely incorporate. LLMs, trained on corpora including financial disclosures, analyst reports, and economic news, can incorporate this qualitative dimension.

### Chain-of-Thought Forecasting

Wei et al. (2022) introduced **chain-of-thought (CoT) prompting**, which elicits intermediate reasoning steps before the final answer. For financial forecasting, CoT is particularly valuable: it forces the model to articulate the causal mechanisms driving its projection, making the output auditable and reducing pattern-matching confabulation.

A well-designed CoT forecasting prompt structures the reasoning in four stages:
1. **Macroeconomic context** — how do interest rates, GDP growth, and inflation affect this company's revenue and margins?
2. **Industry dynamics** — key drivers and headwinds over the next three years (competitive dynamics, technology disruption, regulatory changes).
3. **Firm-specific factors** — competitive position, strategic initiatives, margin trajectory, and CapEx plans as disclosed in the MD&A.
4. **Synthesis and projection** — point estimate plus upside (90th percentile) and downside (10th percentile) for each year, with two-sentence justification per year.

Separating reasoning from numerical output enables downstream validation. If the reasoning contains an internally inconsistent claim—for example, projecting 20% revenue growth while noting a highly competitive market with stable pricing—an automated consistency-checker flags it before the numbers propagate into the DCF model.

### Few-Shot vs. Fine-Tuning

Two adaptation strategies exist:

**Few-shot prompting**: 3–10 examples of historical (company, context, forecast) triples are prepended to the prompt. Advantages: deployment flexibility (no training infrastructure), zero marginal cost per new company, ability to update examples without retraining. Disadvantage: poorly chosen examples anchor the model to the wrong regime. Including examples with diverse macro environments and industry types reduces forecast variance.

**Fine-tuning**: trains model weights on labelled (filing, subsequent cash flow realisation) pairs, internalising domain-specific patterns—e.g., the empirical relationship between specific MD&A language and subsequent earnings surprises. Lopez-Lira & Tang (2023) show LLM signals from financial text predict subsequent stock returns even without fine-tuning, implying that strong general-purpose models already encode substantial domain knowledge. Fine-tuning is most beneficial for highly specialised tasks or when calibrated uncertainty estimates are needed.

**Practical hybrid**: parameter-efficient fine-tuning (PEFT) via LoRA trains only a small fraction of parameters, dramatically reducing compute requirements while achieving performance competitive with full fine-tuning on domain-specific tasks.

### Evaluation Metrics

Forecast evaluation requires both magnitude accuracy and directional accuracy.

**Mean Absolute Percentage Error (MAPE)**:
$$\text{MAPE} = \frac{1}{n}\sum_{t=1}^{n} \frac{|y_t - \hat{y}_t|}{|y_t|} \times 100$$

**Root Mean Squared Error (RMSE)**:
$$\text{RMSE} = \sqrt{\frac{1}{n}\sum_{t=1}^{n}(y_t - \hat{y}_t)^2}$$

**Directional Accuracy (DA)**:
$$\text{DA} = \frac{1}{n}\sum_{t=1}^{n} \mathbf{1}\left[\text{sign}(y_t - y_{t-1}) = \text{sign}(\hat{y}_t - y_{t-1})\right]$$

Practical caveats:
- MAPE is undefined or misleading when $y_t \approx 0$ or $y_t < 0$.
- RMSE is sensitive to outliers and depends on company size, complicating cross-company comparisons.
- DA is scale-invariant and directly relevant to investment decisions: correctly identifying whether FCF will grow or shrink next year captures trading alpha even if the magnitude is imprecise.

A complete evaluation reports all three and compares them against the random-walk baseline and, where available, sell-side analyst consensus estimates.

---

## 5. Tool-Augmented Agents for Financial Math

### Why LLMs Cannot Be Trusted for Arithmetic

LLMs are next-token predictors. The correct answer to $47{,}382 \times 631$ is determined by a deterministic algorithm, not statistical patterns. While transformers approximate simple arithmetic through training exposure, reliability degrades rapidly with complexity. GPT-4 achieves near-perfect accuracy on single-digit multiplication but makes non-trivial errors on multi-step financial calculations involving chained operations, unit conversions, and percentage changes.

For business valuation this is serious. A five-year DCF model involves roughly 15–20 distinct arithmetic operations, each conditional on prior results. **Errors compound**: an incorrectly applied tax rate in the FCFF formula propagates through every subsequent calculation. The solution is architectural: remove arithmetic from the LLM's responsibility entirely and route it to a deterministic computational tool.

### The Code Interpreter Pattern

The **code interpreter** pattern allows an LLM to generate executable code, submit it to a sandboxed Python interpreter, receive the output, and incorporate it into its reasoning. Toolformer (Schick et al., 2023) demonstrated that models can learn to decide *when* to call external tools by observing how tool use reduces prediction loss.

Advantages of generating Python over in-context arithmetic:
- **Accuracy**: the Python interpreter is deterministic.
- **Auditability**: the generated code is an artefact a human reviewer can inspect to verify the correct formula, correct inputs, and correct units. The code is itself a deliverable.

The execution function wraps `subprocess.run` with a timeout, returning `{stdout, stderr, success}`. It never raises exceptions—errors return as structured observations. This is critical: the agent must receive errors as observations and generate recovery actions, not encounter Python exceptions that halt the loop.

### ReAct Pattern Applied to DCF

A ReAct loop for DCF valuation:

- **Thought 1**: I need to compute FCFF with EBIT=840M, DA=310M, CapEx=180M, ΔNWC=80M, τ=0.21. I will use `python_executor` for correctness.
- **Action 1**: `python_executor(code="fcff = 840*(1-0.21)+310-180-80; print(f'FCFF = {fcff:.1f} M')")`
- **Observation 1**: `FCFF = 713.6 M`
- **Thought 2**: FCFF is 713.6M. Now compute the full 5-year DCF with g=8% explicit, g=3% terminal, WACC=9%.
- **Action 2**: `python_executor(code=<DCF code using numpy>)`
- **Observation 2**: `Enterprise Value = 13346.7 M`
- **Thought 3**: Enterprise value is approximately $13.3B. I can now report this result with full provenance.

The agent formulates calculations and interprets results. The Python interpreter handles computation.

### Four Distinctive LLM Failure Modes

Even with tool augmentation, four failure modes require explicit guardrails:

1. **Phantom tickers and fabricated companies**: all tickers must be validated against an authoritative source (EDGAR company search API or securities master file) before use.

2. **Invented financial ratios**: models confabulate plausible-looking numbers not corresponding to any filed data. Replace "trust but verify" with "do not trust until verified." Every financial figure must trace to a specific EDGAR filing or verified market data source.

3. **Misapplied formulas**: syntactically correct code implementing the wrong formula (e.g., FCFE when FCFF was requested, missing the tax shield on interest). Code review or automated formula-level testing against known benchmark cases is necessary in production.

4. **Stale knowledge**: LLMs have a knowledge cutoff date. Financial data, tax rates, and accounting standards change. Any retrieval-augmented system must always use EDGAR-retrieved information in preference to parametric knowledge for factual claims about specific companies.

---

## 6. Scenario Analysis and Monte Carlo

### Bull, Base, and Bear Cases

A single-point DCF estimate is misleading—inputs are uncertain. Professional practice uses **scenario analysis**: a small number of internally consistent input sets representing different outcomes.

- **Bull case**: approximately the 90th percentile—favourable macro, strong competitive execution, above-consensus growth.
- **Base case**: the 50th percentile—the analyst's best estimate of the most likely trajectory.
- **Bear case**: the 10th percentile—adverse macro, margin compression, or competitive deterioration.

Each scenario specifies a complete, internally consistent set: revenue growth rates for each explicit year, EBIT margins, CapEx intensity, NWC ratios, and terminal growth rate. **Internal consistency is critical**: a model simultaneously assuming 25% revenue growth, 35% EBIT margins, and 1% terminal growth is contradictory—rapid growth firms rarely decelerate to near-zero growth abruptly.

LLMs add value at this stage for **narrative coherence checking**: given proposed scenario inputs, the model assesses whether the numbers are consistent with the described business environment and flags contradictions. This is where LLMs excel—qualitative judgment applied to a defined set of inputs—not numerical computation.

### Monte Carlo DCF

Scenario analysis with three discrete cases does not characterise the full distribution of enterprise value. Monte Carlo generates this distribution by sampling from parametric distributions over key inputs.

Let $\text{WACC} \sim \mathcal{N}(\mu_W, \sigma_W^2)$ and $g \sim \mathcal{N}(\mu_g, \sigma_g^2)$ (truncated so $g < \text{WACC}$). For $M$ simulation paths:

$$V^{(m)} = \sum_{t=1}^{n} \frac{\text{FCF}_t^{(m)}}{(1+\text{WACC}^{(m)})^t} + \frac{\text{FCF}_{n+1}^{(m)}}{(\text{WACC}^{(m)} - g^{(m)})(1+\text{WACC}^{(m)})^n}$$

The empirical distribution $\{V^{(m)}\}_{m=1}^M$ yields mean, median, standard deviation, and percentile-based confidence intervals.

Typical parameterisation: $\mu_W = 0.09$, $\sigma_W = 0.015$, $\mu_g = 0.03$, $\sigma_g = 0.01$. With $M = 10{,}000$ draws, the simulation runs in under one second on a modern laptop—practical to re-run after every revision to model inputs.

An agent orchestrates this by calling the `monte_carlo_dcf` tool and then generating a plain-language investment narrative identifying key risk factors driving the downside and framing upside drivers. This narrative synthesis is where LLMs genuinely augment analyst productivity.

---

## 7. Comparable Selection Using LLMs

### Traditional Approaches and Their Pitfalls

The market approach requires a peer group sufficiently similar to the target to make multiple-based comparisons meaningful. Traditional filtering applies: (1) industry classification (SIC, GICS, NAICS codes), (2) size (0.3–3.0× target revenue or market cap), (3) geographic and regulatory constraints.

Three documented pitfalls:
1. **Code obsolescence**: SIC codes were last revised in 1987. A cloud computing company and a 1990s software distributor may share the same SIC code.
2. **Diversified conglomerates**: a manufacturing SIC company may derive most revenue from financial services—its multiples are not informative peers for a pure-play manufacturer.
3. **Cyclical timing**: firms in the same sector at different cycle stages exhibit very different multiples; including a temporarily distressed firm depresses the median and undervalues the target.

### Prompt-Based Comparable Identification

LLMs identify peers from a natural-language description of the target's business model, without rigid classification codes. A zero-shot prompt describes the target and requests comparable firms, structured as a JSON array (company name, ticker, exchange, similarity rationale, similarity score 1–5).

The instruction "Do NOT invent tickers or company names" is necessary but not sufficient. Hallucinated comparables occur with non-trivial frequency. A mandatory validation step—checking every returned ticker against a securities master—is non-negotiable in production. Few-shot prompts including 3–5 examples from historical analyst reports markedly reduce the hallucination rate by anchoring the model to real firm names.

### Embedding-Based Comparable Selection

The limitation of prompt-based selection: it relies on the model's parametric memory, which may be stale or incomplete for smaller companies.

**Embedding-based approach**: embed the MD&A section of the 10-K for all companies in a universe (MD&A is the most semantically rich source—it describes in management's own words the products, markets, competitive position, and strategy). Index them in a FAISS vector database. For a target, retrieve the top-$k$ most similar companies by cosine similarity:

$$\text{sim}(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$$

FAISS's `IndexFlatIP` with L2-normalised vectors computes inner product as cosine similarity. Empirical studies show embedding-based peers outperform SIC-code-based peers: the comparable set has lower interquartile range of EV/EBITDA multiples and valuations from embedding-based comparables exhibit lower absolute deviation from subsequent transaction prices.

### Hybrid Pipeline

Both methods have complementary weaknesses: prompt-based leverages broad world knowledge but hallucinates; embedding-based is grounded but may return companies textually similar for wrong reasons.

**Hybrid pipeline** (two stages):
1. **Candidate generation**: embedding index returns the top 30 candidates by cosine similarity.
2. **LLM filtering**: the model receives candidates alongside brief company descriptions and applies qualitative judgment—removing firms that are geographically incomparable, in demonstrably different competitive positions, or subject to idiosyncratic events (pending acquisition, bankruptcy protection). The filtered 8–12 comparables proceed to multiple analysis.

The two-stage design confines the LLM to tasks where it excels (qualitative business-model reasoning) and avoids tasks where it is unreliable (recalling whether a specific ticker exists).

---

## 8. End-to-End Pipeline, Error Propagation, and Best Practices

### Integrated 10-Step Pipeline

The ten-step data flow:
1. **EDGAR Retrieval**: resolve ticker to CIK; download most recent 10-K plus four prior years.
2. **LLM Extraction**: parse income statement, balance sheet, cash flow statement into structured JSON; flag non-recurring items via MD&A analysis.
3. **XBRL Cross-check**: reconcile with XBRL tags; prefer XBRL for unambiguous tagged items.
4. **FCF Computation**: apply FCFF formula to normalised financials; produce historical time series.
5. **Forecasting**: apply CoT prompt to generate base, upside, and downside FCF paths.
6. **Terminal Value**: compute under Gordon Growth assumptions for each scenario.
7. **Comparable Selection**: run the hybrid pipeline; compute current-year multiples for each peer.
8. **DCF and Comparables Valuation**: compute DCF enterprise value and equity value; compute comparables-based equity value.
9. **Monte Carlo**: simulate EV distribution under parameter uncertainty.
10. **Report Generation**: synthesise into a structured valuation summary with narrative commentary.

Each step produces a structured artefact passed to the next, creating an auditable data lineage. Pydantic data contracts between pipeline stages prevent silent failures from propagating.

### Agent Orchestration

The pipeline above implemented as a monolithic script is brittle: a failure in step 6 requires rerunning all prior steps. A robust design uses an **orchestrator agent** dispatching to specialist sub-agents: `edgar_agent`, `fcf_agent`, `forecast_agent`, `comps_agent`, and `dcf_agent`. Each specialist reports back with its output and any flags (e.g., "data gap in 2021 CapEx"). The orchestrator aggregates, handles exceptions, and escalates to humans when a specialist signals low confidence.

Key advantages: specialists can be independently tested and replaced; specialists with no dependencies run in parallel (comparable selection does not depend on the FCF forecast); the orchestrator maintains a shared valuation state dictionary with full provenance for the final output.

### Error Propagation Analysis

A critical concern in multi-step pipelines: mistakes in early stages compound downstream. Let $V = V(\text{FCF}, g, \text{WACC})$ denote the DCF value. Suppose extraction produces FCF with error $\varepsilon_1$ and the forecasting stage introduces a bias in terminal growth of $\varepsilon_2$. The induced error in enterprise value is approximately:

$$\Delta V \approx \frac{\partial V}{\partial \text{FCF}} \varepsilon_1 + \frac{\partial V}{\partial g} \varepsilon_2$$

For the Gordon Growth perpetuity component:

$$\frac{\partial V}{\partial \text{FCF}_n} = \frac{1+g}{\text{WACC} - g}, \qquad \frac{\partial V}{\partial g} = \frac{\text{FCF}_n(1+\text{WACC})}{(\text{WACC}-g)^2}$$

Both partial derivatives are large when $g \approx \text{WACC}$. With $\text{WACC} = 0.09$ and $g = 0.03$:
- A 1% relative error in FCF → approximately 1% error in enterprise value.
- A 100-basis-point error in terminal growth → approximately 15–18% error in enterprise value.

**This quantifies why Monte Carlo is not optional**: the terminal growth rate assumption dominates valuation uncertainty.

### Case Study: Mid-Cap SaaS Company

A mid-cap US cloud software company (illustrative composite):
- Revenue (TTM): $4.2B, +12% YoY; EBIT margin: 20%; D&A: $310M; CapEx: $180M
- Net debt: $800M; shares outstanding: 280M

Pipeline output: two non-recurring items flagged ($45M restructuring, $30M acquired intangible amortisation). After normalisation: EBIT = $915M, FCFF = $789M.

CoT forecasting base-case FCFs: Year 1–5 = $868M, $947M, $1,025M, $1,100M, $1,170M.

With WACC = 9%, terminal growth = 3%: **DCF enterprise value = $17.0B** → equity value = $16.2B → $57.9/share.

Embedding-based pipeline identifies 9 peers with median EV/EBITDA of 24.5×. Applying to EBITDA of $1.22B: **comparables-based EV = $29.9B** — a substantial premium, consistent with the sector trading at elevated growth multiples.

Monte Carlo (10,000 draws, $\sigma_W = 1.5\%$, $\sigma_g = 1\%$): EV mean = $17.2B, 10th–90th percentile range = $12.5B–$24.1B.

### Best Practices for Production Deployment

1. **Always verify against XBRL**: LLM extraction is a complement, not a sole source. Any figure conflicting with the XBRL tag is flagged for human review.

2. **Use a code interpreter for all arithmetic**: no financial calculation—however simple—should be performed by in-context LLM reasoning. The generated code documents exactly what was computed.

3. **Run Monte Carlo**: a point-estimate DCF is a misleading representation of value. Communicate the percentile range alongside the central estimate.

4. **Implement mandatory hallucination guards**: validate every ticker against a securities register; trace every financial figure to a specific EDGAR accession number; suppress unverifiable claims from final output.

5. **Always require human review before publication**: LLMs are a powerful analytical assistant, not an autonomous decision-maker. Final valuation reports must be reviewed by a qualified analyst who takes responsibility for the figures.

These principles are consistent with FSB (2023) guidance on AI in finance, which emphasises human accountability, model transparency, and robust back-testing as prerequisites for responsible deployment of ML systems in investment processes.

---

## Summary and Connections

This lecture developed a complete framework for LLM-assisted business valuation: EDGAR data extraction, FCFF/FCFE computation, CoT forecasting, tool-augmented arithmetic (ReAct + code interpreter), scenario analysis (Monte Carlo), comparable selection (embedding + LLM hybrid), and end-to-end pipeline orchestration.

The key quantitative insight is the error propagation analysis: a 100-bps error in terminal growth propagates into a 15–18% valuation error, quantifying why Monte Carlo simulation and scenario analysis are not optional—they are the mechanism for communicating irreducible uncertainty in any forward-looking valuation.

Chapter 6 applies related techniques to credit risk assessment—where the same data extraction and forecasting tools operate under different target variables (probability of default, loss given default) and stricter regulatory constraints on model transparency.
