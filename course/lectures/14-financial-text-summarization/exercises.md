# Exercises — Lecture 14: Financial Text Summarization and Information Extraction

## Exercise 1 [B]
**Topic:** The Information Extraction Problem in Finance

Consider the following excerpt from a fictional 10-K filing:

> "As of December 31, 2024, Acme Corp. (NASDAQ: ACME) reported total revenues of $4.2 billion, a 12% increase year-over-year. The company's CEO, Jane Smith, noted that the North American segment accounted for approximately 60% of total revenues."

(a) Identify all named entities in this passage and classify each by type (e.g., organization, person, date, monetary figure, percentage).

(b) Explain the difference between an information extraction task and a summarization task. Which task would you apply to automatically populate a financial database from thousands of such filings, and why?

(c) Is the above text structured or unstructured? Justify your answer and describe what a structured representation of the same information might look like.

## Exercise 2 [I]
**Topic:** Financial Document Summarization

Using the Hugging Face `transformers` library, write a Python script that:

(a) Loads a pre-trained abstractive summarization model (e.g., `facebook/bart-large-cnn` or `google/pegasus-xsum`).

(b) Summarizes the following earnings call snippet (you may use the text verbatim as input):

> "Good morning, everyone. This is our third-quarter earnings call for fiscal year 2024. Our net income came in at $320 million, up 8% from the prior quarter, driven by strong performance in our asset management division. Operating expenses declined by 3% due to workforce optimization and technology-driven efficiencies. Looking ahead, we expect revenue growth in the range of 5 to 7 percent for the next fiscal year, contingent on stable interest rate conditions. We are also exploring strategic acquisitions in the European market to diversify our revenue streams."

(c) Print the summary and compute its ROUGE-1 and ROUGE-2 scores against a reference summary of your own writing using the `rouge-score` package.

(d) Discuss one limitation of applying general-domain summarization models to financial text, and suggest how fine-tuning on a dataset such as ECTSum could address it.

## Exercise 3 [A]
**Topic:** Evaluation and Benchmarks

Factual consistency is a critical evaluation dimension for financial NLP systems, since hallucinated numbers or fabricated entity relationships can have legal and reputational consequences.

(a) Describe the difference between ROUGE-based evaluation and factual consistency evaluation. Give a concrete example where a summary achieves a high ROUGE score but is factually inconsistent with the source document.

(b) Design a human evaluation rubric (with at least four criteria and a scoring scale) for assessing the quality of automatically generated summaries of SEC 10-K filings. Justify each criterion from a financial practitioner's perspective.

(c) Research and describe one automatic factual consistency metric beyond BERTScore (e.g., QAFactEval, DAE, SummaC, or FactCC). Explain how it works, what its main strengths are, and where it may fail on financial documents specifically.

(d) Propose an experimental design to benchmark three different LLM-based summarization pipelines on the ECTSum dataset. Specify the evaluation metrics you would use, the baseline you would compare against, and how you would handle the long-document problem for earnings call transcripts that exceed 4,000 tokens.
