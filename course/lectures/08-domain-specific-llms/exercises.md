# Exercises — Lecture 08: Domain-Specific Financial LLMs

## Exercise 1 [B]
**Topic:** Why Domain-Specific LLMs?

General-purpose LLMs such as GPT-4 are trained on broad internet corpora. Financial text, however, has distinctive properties that challenge such models.

(a) List three characteristics of financial language that distinguish it from general-purpose text, and explain why each characteristic creates difficulties for a model pre-trained on general web data.

(b) Give one concrete example of a financial NLP task (e.g., earnings call sentiment analysis) and describe a failure mode a general-purpose model might exhibit on that task.

## Exercise 2 [I]
**Topic:** Benchmark Comparisons

You have access to the Hugging Face `datasets` library. The `financial_phrasebank` dataset contains sentences from financial news labelled as positive, negative, or neutral.

(a) Load the dataset, fine-tune `ProsusAI/finbert` and `bert-base-uncased` on the training split, and evaluate both models on the test split using accuracy and macro-F1.

(b) Report your results in a table. For which label category does FinBERT show the largest improvement over BERT-base? Hypothesize why.

(c) Repeat the evaluation using only 10% of the training data. How does the data-efficiency comparison between the two models change?

## Exercise 3 [A]
**Topic:** Practical Deployment Considerations

A mid-sized asset manager wants to deploy a FinLLM to extract key financial metrics from 10-K filings in near-real-time. Their infrastructure team has flagged concerns about cost, latency, data sovereignty, and model licensing.

Design a hybrid deployment architecture that addresses these constraints. Your answer should:
- Specify which model(s) you would use and justify the choice based on licensing and performance
- Describe a routing strategy that sends simple extraction queries to a cheaper model and complex reasoning queries to a more capable one
- Estimate the cost and latency implications of your design relative to a single-model baseline
- Identify at least two regulatory considerations (e.g., GDPR, MiFID II model explainability) and explain how your architecture addresses them
