# Exercises — Lecture 4: LLM Agents and Finance Applications

---

**Exercise 1 [B] — ReAct Agent for Financial Q\&A**

Using the OpenAI or Anthropic API, implement a minimal ReAct agent that answers factual questions about a provided earnings call transcript. The agent should have access to two tools: (1) a `search_transcript(query)` function that performs keyword search over the transcript, and (2) a `calculate(expression)` function that evaluates arithmetic expressions.

1. Run the agent on five questions of increasing complexity (e.g., revenue growth, margin comparison, year-over-year change).
2. Log and display each reasoning step and tool call.
3. Identify at least one case where the agent fails or produces an incorrect answer and propose a fix.

*(Covers Section 1: From Language Models to Agents)*

---

**Exercise 2 [I] — RAG Pipeline for SEC Filings**

Build a retrieval-augmented generation pipeline for answering questions about 10-K filings. Use the SEC EDGAR full-text search API to retrieve filings for at least five S\&P~500 companies. Your pipeline should:

1. Chunk documents using a sliding-window strategy with configurable chunk size and overlap.
2. Embed chunks with a sentence-transformer model and store them in a vector database (e.g., FAISS or ChromaDB).
3. Retrieve the top-$k$ chunks for a given question and pass them as context to a generative model.
4. Evaluate the pipeline on a set of 20 hand-labelled question–answer pairs using ROUGE-L and a faithfulness metric of your choice.
5. Ablate over chunk size ($\{256, 512, 1024\}$ tokens) and top-$k$ ($\{3, 5, 10\}$) and report how these affect answer quality.

*(Covers Sections 2 and 4: Tool Use and RAG)*

---

**Exercise 3 [A] — Multi-Agent Earnings Analyst**

Design and implement a multi-agent system that automatically produces a structured equity research note from a company's most recent earnings call transcript and 10-K filing. The system should consist of at least three specialised agents with distinct roles (e.g., data retrieval agent, financial analysis agent, report writing agent) coordinated by an orchestrator.

1. Define the inter-agent communication protocol and the tools available to each agent.
2. Generate research notes for three companies from different sectors.
3. Evaluate the notes on factual accuracy, completeness, and coherence using a rubric of your design. Have a domain expert (or a judge LLM) rate each note.
4. Identify failure modes specific to multi-agent coordination (e.g., conflicting tool outputs, context loss) and propose mitigation strategies.
5. Discuss the human-in-the-loop checkpoints you would add before this system could be deployed in a regulated asset management context.

*(Covers Sections 3, 5, and 6: Orchestration, Finance Applications, and Governance)*
