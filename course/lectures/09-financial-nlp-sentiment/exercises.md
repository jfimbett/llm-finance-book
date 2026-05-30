# Exercises — Lecture 09: Financial NLP and Sentiment Analysis

## Exercise 1 [B]
**Topic:** Sentiment Analysis Methods

The Loughran-McDonald (LM) wordlist was constructed specifically for financial documents and differs substantially from general-purpose sentiment lexicons such as the Harvard General Inquirer. Explain why a word like "liability" is classified as negative in the LM dictionary but would be neutral or even positive in a general English sentiment lexicon. Give two additional examples of financial terms whose sentiment polarity differs between the LM wordlist and a general-purpose lexicon, and explain the economic reasoning behind each classification.

## Exercise 2 [I]
**Topic:** Applications by Text Source — Earnings Call Transcripts

Download a publicly available earnings call transcript for a large-cap firm of your choice (e.g., from the SEC EDGAR full-text search system or a financial data API). Using the `transformers` library and the `ProsusAI/finbert` model, classify each sentence in the transcript as positive, negative, or neutral. Compute the following aggregate statistics: (a) the fraction of positive, negative, and neutral sentences in the management prepared remarks section versus the analyst Q&A section, and (b) the difference in average sentiment score between the two sections. Discuss whether the patterns you observe are consistent with the hypothesis that management tone is more optimistic than analyst responses.

## Exercise 3 [A]
**Topic:** Practical Pipeline — Evaluation and Signal Construction

Design and implement an evaluation framework for a financial sentiment classifier applied to FOMC meeting minutes. Your framework should: (a) construct a labeled dataset by sampling 200 sentences from FOMC minutes spanning at least five years and obtaining two independent human ratings per sentence using the positive/neutral/negative scheme, (b) compute Krippendorff alpha to assess inter-annotator agreement, (c) train or fine-tune a transformer-based classifier on the annotated data and report precision, recall, and F1 by class, and (d) assess whether the classifier's aggregate document-level sentiment score Granger-causes changes in the 2-year Treasury yield in the two trading days following each FOMC release. Discuss the main threats to validity in each step of the pipeline and propose one mitigation for each.
