# Lecture 7: Other Applications in Finance and Future Trends

## Learning Objectives

By the end of this lecture, students should be able to:

1. Map the landscape of LLM applications across finance — portfolio management, regulatory compliance, insurance, and algorithmic trading — and connect them to techniques developed in earlier chapters.
2. Apply a structured decision framework to select among zero-shot prompting, retrieval-augmented generation, and fine-tuning for a given finance task.
3. Model a financial workflow as a directed acyclic graph and implement the three canonical automation patterns.
4. Design an LLM-powered research assistant incorporating hybrid retrieval, persistent memory, and tool use.
5. Identify and measure the principal sources of bias in LLM-based finance systems, apply the three canonical fairness metrics, and interpret the fairness impossibility theorem.
6. Apply the SR 11-7 model risk management framework to LLM deployments, including documentation, validation, and monitoring.
7. Articulate the obligations arising from the EU AI Act, GDPR, and MiFID II for LLM-based financial products.
8. Evaluate the frontier of multimodal and autonomous LLM capabilities and identify the five open research problems most likely to shape finance AI over the next decade.

---

## 1. LLM Applications Across Finance: A Survey

### Where We Have Been

This is the concluding chapter of the book. Looking back at the full arc is worthwhile before moving forward.

The book has developed its argument across six interconnected themes: text fundamentals and sentiment analysis (Chapter 1), the modern LLM landscape — transformers, pre-training, RLHF (Chapter 2), fine-tuning for finance-specific tasks (Chapter 3), LLM agents with tool use and multi-step reasoning (Chapter 4), business valuation via agent-assisted DCF and comparables selection (Chapter 5), and credit risk — fine-tuning, constrained generation, fairness, and regulatory compliance (Chapter 6).

Reading across these chapters, a clear progression emerges: early chapters used lightweight representations applicable to large corpora with modest compute; later chapters required generative and agent-based models capable of nuanced multi-step reasoning; this final chapter addresses the cross-cutting concerns of deployment, governance, and frontier capability that arise once LLMs are embedded in production financial systems.

### Remaining Application Areas

Several high-value finance domains appear in the book without full treatment.

**Portfolio Management**: LLMs contribute at multiple levels. Natural-language portfolio specification translates a qualitative mandate ("long quality momentum in US large-caps while hedging out market beta") into quantitative optimisation inputs. ESG screening extracts structured signals from heterogeneous sustainability reports and proxy statements that resist tabularisation. Earnings surprise prediction from conference call transcripts — one of the most studied applications — exploits management tone, topic emphasis, and directness of responses to analyst questions; López-Lira and Tang (2023) show LLMs trained on earnings call transcripts consistently outperform bag-of-words sentiment dictionaries. López-Lira (2025) further constructs a simulated stock market with heterogeneous LLM agents (value investors, momentum traders, market makers) and shows the resulting price dynamics exhibit features observed in real markets — including episodic bubbles — while revealing systemic risks when many agents share similar training data.

**Regulatory Compliance**: MiFID II suitability report generation requires synthesising a client's risk profile, an instrument's characteristics, and a regulatory template into a personalised, defensible narrative. AML Suspicious Activity Report drafting — transforming complex transaction patterns into plain-language narratives — has been shown to improve consistency and reduce analyst time per report.

**Insurance**: Underwriting extracts structured risk factors from unstructured files (inspection reports, medical records, claims histories). Claims triage determines the priority, complexity, and likely settlement cost of incoming claims. Policy question-answering, where an LLM serves as an accessible interface to insurance contracts' complex conditional logic, has seen rapid commercial adoption.

**Algorithmic Trading**: LLMs process news, social media, regulatory announcements, and corporate filings to produce sentiment and event indicators that complement price-based signals. They translate strategy hypotheses into testable code, explain backtest behaviour, and suggest risk controls. At the execution level, conversational interfaces to order management systems allow traders to adjust parameters without context-switching.

### Choosing the Right LLM Architecture

**Three canonical deployment patterns**:

*Zero-shot prompting* applies a general-purpose model $M$ directly: $\hat{y} = M(\text{prompt}(x))$. No task-specific training or retrieval. The FinanceBench benchmark shows frontier models answer ~80% of financial QA questions correctly on the first attempt — a high bar for more elaborate systems to clear.

*Retrieval-Augmented Generation* augments the prompt with retrieved context: $\hat{y} = M(\text{prompt}(x, \mathcal{R}(x, \mathcal{D})))$, where $\mathcal{R}$ is a retrieval function over document corpus $\mathcal{D}$. Prefer RAG when the task requires grounding in specific, updatable documents — current regulatory texts, recent filings, live prices.

*Fine-tuning* adapts model parameters on task-specific labelled data: $\hat{y} = M_\theta(x)$. Justified when output format is highly structured and consistency across thousands of calls matters more than generality.

**Four architecture families** relevant to finance NLP:
- *Encoder-only* (BERT, FinBERT): bidirectional; strong for classification, embeddings, real-time low-latency tasks; weak for generation.
- *Decoder-only* (GPT-4, LLaMA): autoregressive; dominant for general-purpose financial NLP; weak for real-time constraints.
- *Encoder-decoder* (T5, BART): sequence-to-sequence; strong for summarisation and structured extraction.
- *Agentic system* (ReAct + tools): appropriate when task completion requires retrieving or manipulating external state across multiple steps.

When the two selection axes give conflicting signals, latency and interpretability requirements are the tiebreakers: real-time, high-stakes applications default to the simplest, most auditable approach.

---

## 2. Automating Financial Workflows

### Workflow Automation Patterns

A financial workflow is a sequence of processing steps that transforms raw inputs (market data, regulatory filings, client communications, trade records) into actionable outputs (reports, alerts, recommendations, compliance records). The defining characteristic is the presence of dependencies between steps.

**Financial Workflow as a DAG**: A financial workflow is a directed acyclic graph $W = (T, E)$ where $T = \{t_1, \ldots, t_n\}$ is a finite set of tasks ($t_i : \mathcal{X}_i \to \mathcal{Y}_i$) and $E \subseteq T \times T$ contains dependency edges: $(t_i, t_j) \in E$ if and only if $t_j$ requires an output of $t_i$. An execution of $W$ is a topological ordering of $T$ consistent with $E$.

Three automation patterns map onto this structure:

**Sequential pipeline**: executes tasks in a fixed linear order $t_1 \to t_2 \to \cdots \to t_n$. Appropriate when tasks are inherently ordered, failures cascade, and the workflow is invoked batch-wise. Example: a nightly process that fetches earnings transcripts, extracts forward guidance, compares against analyst consensus, and distributes an analyst briefing.

**Event-triggered**: a monitor process watches an event stream and fires a workflow when a condition is satisfied. The monitor is often LLM-powered, classifying incoming events and routing them to the appropriate handler. The natural architecture for regulatory filing monitors and compliance surveillance tools where the trigger is semantic rather than syntactic.

**Orchestrator-worker**: separates coordination from execution. A central orchestrator decomposes a high-level goal into sub-tasks and dispatches them to specialised workers, collecting and synthesising their outputs. Best suited to tasks requiring parallel information gathering, expert specialisation, and adaptive replanning when early results change the downstream strategy.

### Finance Workflow Examples

**Earnings call processing pipeline** (sequential, 5 tasks): (1) retrieve transcript; (2) extract structured forward guidance (revenue, margin, capex) as JSON; (3) compare against analyst consensus; (4) classify management tone (constructive/cautious/evasive); (5) draft analyst briefing. Executes within minutes of a call ending — compressing what traditionally required several hours of analyst time.

**Regulatory filing monitor** (event-triggered): an RSS feed poller classifies each new SEC 8-K by type and issuer, routes it to the appropriate team with a summary, and determines whether the event is material for any company on the firm's watchlist — a non-trivial semantic judgment, since materiality depends on the recipient's exposure.

**Trade surveillance narrative** (orchestrator-worker): when a rule-based system flags an unusual order pattern, an LLM retrieves relevant news and social media from the preceding hours, searches internal communications for context, and drafts a structured narrative. The analyst provides the regulatory judgment; the LLM handles information aggregation.

### Integrating with Existing Infrastructure

**Data level**: financial infrastructure relies on standardised protocols (FIX for order routing, SWIFT for payments, XBRL for regulatory filings). LLMs interact via tool wrappers — Python functions that translate natural-language requests into well-formed API calls. The LLM never sees the raw wire protocol.

**Compute level**: the appropriate integration pattern is *asynchronous*. LLMs operate on aggregated, lower-frequency signals (seconds to minutes); execution systems operate at microseconds to milliseconds. This clean temporal separation is a structural feature, not a limitation.

**Governance level**: every LLM call should be treated as a first-class transaction generating a record including the model version, the full prompt, the output, and any tool calls — potentially subject to MiFID II record-keeping requirements.

---

## 3. Building Your Own Research Assistant

### Architecture

A financial research assistant $\mathcal{A} = (\mathcal{R}, \mathcal{M}, \mathcal{K}, \mathcal{T}, \mathcal{I})$ consists of five components: retrieval engine $\mathcal{R}$ (ranked passages from corpus $\mathcal{D}$), LLM reader $\mathcal{M}$ (synthesises response from query and retrieved passages), persistent memory $\mathcal{K}$ (user preferences, portfolio context, conversation history), tool layer $\mathcal{T}$ (market data APIs, filing databases, calculators), and interface layer $\mathcal{I}$ (natural language, voice, tables, visualisations).

The retrieval engine is the component most often underspecified in prototypes and most consequential in production. Semantic search alone fails on numerical queries and on queries requiring exact term matching (regulatory article numbers, accounting standards identifiers). A production retriever must combine dense retrieval with sparse retrieval (BM25) in a hybrid pipeline.

### RAG Implementation Details

**Chunking strategy**: naive fixed-size chunking fragments tables, disrupts cross-references, and splits financial statements in ways that destroy their meaning. The appropriate strategy for 10-K documents is semantic chunking that respects SEC Item boundaries (Item 1A Risk Factors, Item 7 MD&A, Item 8 Financial Statements). Tables are extracted as structured objects and indexed separately.

**Hybrid retrieval via Reciprocal Rank Fusion**: given a query $q$, compute dense similarity $s_{\text{dense}}(q, d_i) = \cos(\mathbf{e}_q, \mathbf{e}_{d_i})$ and sparse relevance $s_{\text{sparse}}(q, d_i)$ from BM25. Combine:
$$s_{\text{RRF}}(q, d_i) = \frac{1}{k + r_{\text{dense}}(d_i)} + \frac{1}{k + r_{\text{sparse}}(d_i)}$$
where $r_{\text{dense}}$ and $r_{\text{sparse}}$ are the ranks of passage $d_i$ under each retriever and $k = 60$ is a smoothing constant. Parameter-free and robust to different score scales.

**Source attribution**: every claim must be attributable to a retrieved passage. Claims not supported by retrieved context should be flagged as model-generated inference, not retrieved fact. In regulated contexts, source attribution is the mechanism by which outputs can be audited.

### OpenClaw

OpenClaw is an open-source framework resolving the tension between capability and data security: it runs entirely on the user's own hardware, so financial data never leaves the machine. Four design principles: *privacy by default* (all processing local), *meet users where they work* (queries via WhatsApp, Telegram, Slack, Signal), *model flexibility* (cloud models for maximum capability; locally-hosted open-weight models for data sensitivity), and *extensibility through skills* (Python functions with descriptive docstrings become callable tools).

Key skills: earnings alert (ticker → guidance summary relative to consensus), filing monitor (scheduled digest of new SEC filings from watchlist), portfolio Q&A (natural-language questions about positions in a local CSV), macro digest (morning briefing from central bank speeches, overnight moves, data releases).

### Production Challenges

**Freshness vs. accuracy**: maintain corpus freshness with a continuous ingestion pipeline and document versioning — a superseding 10-K must replace, not coexist with, the prior year's filing.

**Hallucination mitigation**: enforce source attribution at the system level; validate numerical claims against structured data sources; flag unverifiable claims from the output.

**Context management**: Balogh and Didisheim (2025) show LLM predictive accuracy follows an inverted U-shaped pattern as a function of context length — excessive context degrades performance, mirroring cognitive limitations in human analysts. Larger models mitigate but do not eliminate the degradation.

---

## 4. Ethical Considerations and Bias Mitigation

### Sources of Bias

**Training data bias**: frontier LLMs are trained predominantly on English-language, US-centric financial content. When applied to financial analysis in non-English-speaking jurisdictions, they systematically underestimate risks and misread institutional context — a source of systematic pricing error, not merely a fairness concern.

**Historical discrimination encoded in data**: an LLM trained on historical lending records reproduces the discriminatory patterns present in those records. A bank with a history of racially discriminatory mortgage denials will, if its historical decisions form training data, produce a model associating neighbourhood demographic proxies with elevated credit risk. This is not a failure of the LLM; it faithfully reproduces the signal in the training data.

**Feedback loop bias**: when a model's output influences asset prices, those prices enter future training data, reinforcing the model's priors — analogous to Soros's reflexivity but at faster timescales. When many participants deploy similar LLM-based strategies, feedback loops can amplify volatility and reduce price efficiency.

**Anchoring bias**: LLMs weight salient numerical anchors disproportionately. An LLM that has processed an earnings call reporting dramatically higher-than-expected revenue will anchor on that number; structural trends with more persistent cash flow implications may receive insufficient weight. This is a cognitive bias documented by Tversky and Kahneman (1974) that LLMs, trained on human-generated text, reproduce reliably.

### Fairness Metrics and the Impossibility Theorem

**Demographic parity**: $\Pr(\hat{Y} = 1 \mid A = a) = \Pr(\hat{Y} = 1 \mid A = b)$ for all values $a, b$ of sensitive attribute $A$.

**Equalized odds**: $\Pr(\hat{Y} = 1 \mid Y = y, A = a) = \Pr(\hat{Y} = 1 \mid Y = y, A = b)$ for $y \in \{0, 1\}$. Both TPR and FPR equal across groups.

**Calibration within group**: $\Pr(Y = 1 \mid \hat{P} = p, A = a) = p$ for all $p$. Predicted probabilities equally reliable across groups.

**Impossibility theorem** (Chouldechova, 2017): when base rates differ across groups, a non-trivial classifier cannot simultaneously satisfy demographic parity, equalized odds, and calibration within group. Specifically, demographic parity and calibration within group are mutually incompatible whenever base rates differ.

This is a policy choice, not a technical limitation. Choosing which fairness criterion to satisfy is a decision that must be made explicitly and justified to regulators.

### Mitigation Strategies

**Pre-processing**: data rebalancing; causal data augmentation (vary protected attributes while holding other features fixed, creating counterfactual examples). Reduces bias at some cost to majority-group predictive accuracy.

**In-processing**: adversarial debiasing trains a classifier to be predictive while a simultaneously trained adversary cannot recover the sensitive attribute from the model's intermediate representations. Requires sensitive attribute annotations in training data.

**Post-processing**: threshold adjustment selects decision thresholds satisfying the desired fairness criterion on a held-out calibration set. Applicable to black-box APIs; comes at the cost of accepting different error rates for different groups.

**Human oversight**: mandatory for high-stakes decisions regardless of which technical mitigation is applied.

### Regulatory Landscape

**EU AI Act (2024)**: credit scoring and life insurance risk assessment are classified as *high-risk* AI systems requiring conformity assessment before market entry, mandatory registration, ongoing monitoring, and meaningful human oversight.

**FSB (2024)**: documents AI's capacity to amplify third-party concentration risk, increase market correlations through algorithmic herding, and generate financial disinformation. Calls on authorities to develop AI-powered supervisory tools.

---

## 5. Deploying LLMs in Regulated Environments

### SR 11-7 Three Lines of Defence

SR 11-7 (2011): when an LLM produces quantitative estimates feeding into material business decisions, it constitutes a model regardless of its internal architecture.

**First line — development and ownership**: document purpose, scope, data inputs, architecture (foundation model choice, fine-tuning), known limitations, intended and prohibited use cases, performance metrics. For LLMs, documenting known limitations is challenging because the failure mode space is not fully characterised. Document observed failure modes from red-teaming explicitly, even if the list is acknowledged to be incomplete.

**Second line — independent validation**: adversarial testing includes prompt injection attacks, jailbreaking, and distribution shift tests. The FAIR framework (Noguer, 2025) addresses LLM-specific failure modes: temporal data inconsistencies, hallucination in numerical extraction, and privacy leakage.

**Third line — internal audit**: periodically assesses whether documentation is maintained, validation is genuinely independent, findings are tracked to resolution, and usage has drifted beyond validated scope.

### Explainability

**Procedural transparency** (chain-of-thought): the intermediate reasoning steps constitute an auditable trace. This is a natural-language reconstruction of the model's reasoning — not an explanation of the neural network's internal computation — but it provides a basis for auditing consistency with outcomes and institutional policy.

**Post-hoc attribution** (SHAP, attention saliency): adaptable for LLMs that produce numerical outputs from structured features.

Regulators have indicated that "we use a large language model" does not constitute meaningful information under GDPR Articles 13 and 14.

### Privacy (GDPR and MiFID II)

**GDPR Article 22**: right to human review of automated decisions with legal or significant effects; meaningful information about the logic involved required.

**MiFID II**: LLM-generated investment recommendations and market analyses must be logged with sufficient detail to reconstruct the decision: the prompt, model version, output, and time of generation.

**Practical implication**: on-premise or private-cloud deployment is strongly preferred for any application processing personal financial data or generating client-specific recommendations.

### Incident Response

Four monitoring signal classes: input distribution (KL divergence between prompt embeddings detects distributional shift), output quality (accuracy on sampled outputs where ground truth is available), operational (latency, cost, error rates, refusal rates), fairness (periodic re-runs of the bias evaluation framework).

**Severity classification**: pre-define before incidents occur. A hallucination in a low-stakes summarisation task triggers standard review; a hallucinated financial figure in a credit decision triggers immediate escalation, potential reversal of affected decisions, regulatory notification if required, and root-cause investigation.

---

## 6. Future Trends and Open Research Problems

### Multimodal LLMs

Current models process text. The financial data that matters most for investment decisions is not purely textual: earnings presentations contain charts; annual reports embed tables; earnings calls carry prosodic cues (hesitation, confidence, urgency) lost in transcription. Multimodal LLMs jointly encoding text, images, audio, and structured data represent a qualitative expansion of the capability frontier.

**Long-context models**: as context windows expand to hundreds of thousands of tokens, an entire 10-K can be processed in a single forward pass — linking observations across sections without losing context between chunks. The challenge: the "lost in the middle" phenomenon — recall accuracy degrades for passages far from either end of a long context. The optimal architecture combines long-context reasoning for intra-document tasks with retrieval for multi-document synthesis.

### Autonomous Financial Agents

Multi-agent systems that can write new tools, form hypotheses, design experiments, and revise their own strategies in response to outcomes represent a fundamentally different class of technology.

The governance principle: distinguish *informational* outputs (analysis and recommendations), *advisory* outputs (proposed actions for human approval), and *executive* outputs (acts on the financial system directly). Mature practice confines executive autonomy to well-defined, pre-approved action spaces with hard limits, and treats any action outside that space as requiring explicit human authorisation.

### Five Open Research Problems

1. **Calibrated uncertainty quantification** for LLM-generated forecasts. Conformal prediction can provide distribution-free coverage guarantees; Chen et al. (2024) show that token-level log-probability distributions provide principled uncertainty estimates outperforming post-hoc sampling methods on financial QA tasks.

2. **Robust comparable company selection in thin markets**. Embedding-based similarity measures trained on US financial text are systematically biased toward US market characteristics. Cross-market comparables selection requires embedding spaces invariant to market-level characteristics.

3. **Cross-lingual finance LLMs** for non-English regulatory filings. Current multilingual models perform substantially worse on filings in Japanese, German, French, Portuguese, and Chinese. Building or adapting finance LLMs for these environments requires corpora not currently publicly available.

4. **Detecting and mitigating feedback loops and memorisation**. Didisheim and López-Lira (2025) formalise the LLM's "predictable memory" — look-ahead bias from training corpora, most severe at low frequencies and for large models trained on broad corpora. Developing credible identification strategies for feedback-loop-induced inflation in apparent forecast performance is an open problem.

5. **Formal verification of chain-of-thought financial reasoning**. There is no guarantee that the stated reasoning in a chain-of-thought is the actual computation that produced the output — "unfaithful reasoning." Developing methods to verify consistency between stated reasoning and output, and to detect when the stated reasoning could not have produced the conclusion, has direct regulatory relevance.

### The Path Forward

Three disciplines separate successful deployments from failures:
1. **Measure everything**: retrieval quality, output faithfulness, fairness metrics, distributional drift. What is not measured cannot be managed.
2. **Document honestly**: purpose, limitations, known failure conditions, and the human oversight structure. Documentation is the mechanism by which institutional knowledge survives model updates and team turnover.
3. **Escalate appropriately**: build human review into every consequential decision workflow as a genuine check — not a legal formality — that the reviewer is empowered to override.

The field is young enough that researchers and practitioners reading this chapter will shape its norms, its standards, and its failures as much as its successes.
