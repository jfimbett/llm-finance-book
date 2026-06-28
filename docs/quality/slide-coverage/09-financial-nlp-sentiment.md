# Slide Coverage: 09-financial-nlp-sentiment

Source: `book/chapters/09-financial-nlp-sentiment/chapter.tex`
Deck: `course/slides-html/09-financial-nlp-sentiment/index.html`

---

## Checklist

### Sections / subsections
- [x] §1 Text as Financial Data
- [x] §1.1 Sources: Social Media, News, Filings, Transcripts, Policy Documents
- [x] §1.2 Preprocessing: Tokenization, Normalization, Deduplication
- [x] §2 Sentiment Analysis Methods
- [x] §2.1 Lexicon-Based Methods: The Loughran–McDonald Wordlist
- [x] §2.2 Fine-Tuned Classifiers: FinBERT and SEC-BERT
- [x] §2.3 LLM Zero-Shot and Few-Shot Sentiment Classification
- [x] §3 Applications by Text Source
- [x] §3.1 Social Media: Twitter/X, Reddit WallStreetBets, StockTwits
- [x] §3.2 News and Wire Services
- [x] §3.3 Earnings Call Transcripts: Management Tone and Analyst Q&A
- [x] §3.4 SEC Filings: 10-K/10-Q Risk Factor Language and MD&A Readability
- [x] §3.5 Central Bank Communications: FOMC Minutes and ECB Decisions
- [x] §4 From Sentiment to Tradeable Signal
- [x] §4.1 Aggregation, Standardization, and Stationarity
- [x] §4.2 Event Studies: Earnings Surprises and FOMC Shocks
- [x] §4.3 Long-Horizon vs. Short-Horizon Predictability
- [x] §5 Practical Pipeline
- [x] §5.1 Data Collection: EDGAR, Twitter API, and News Vendors
- [x] §5.2 Inference at Scale: Batch vs. Streaming
- [x] §5.3 Evaluation: Krippendorff's Alpha, Precision, Recall, and F1

### Named models / methods / definitions
- [x] LM net-sentiment formula: S_LM(d) = (N_pos − N_neg) / N_words
- [x] Loughran–McDonald (LM) dictionary — word-list categories and sizes
- [x] Harvard General Inquirer (Stone 1966)
- [x] FinBERT classification head formula (softmax over [CLS] embedding)
- [x] SEC-BERT
- [x] Financial PhraseBank
- [x] GPT-4 zero-shot / few-shot classification
- [x] GPOMS psychometric tool (Bollen 2011 Twitter study)
- [x] Fog Index definition
- [x] Cumulative Abnormal Return (CAR) definition and formula
- [x] Predictive regression: CAR[1,60] = α + β₁·SUE + β₂·S̃
- [x] Cross-sectional z-score standardisation
- [x] Krippendorff's alpha (nominal and ordinal)
- [x] Precision, Recall, macro-F1
- [x] Sentiment inflation concept
- [x] MinHash / LSH deduplication (Jaccard threshold 0.6–0.8)
- [x] ADF / KPSS stationarity tests
- [x] ONNX / quantised models for streaming
- [x] Model distillation (110M → 33M, <5% accuracy loss)
- [x] Dynamic padding/batching; FP16/BF16 inference

### Key numbers
- [x] LM negative: 2,355 words
- [x] LM positive: 354 words
- [x] LM uncertainty: 297 words
- [x] LM litigious: 903 words
- [x] LM strong modal: 19 words
- [x] LM weak modal: 27 words
- [x] Financial PhraseBank: 4,840 sentences, 16 annotators
- [x] At 75% agreement: ~3,400 high-confidence sentences; inter-annotator agreement ~75–80%
- [x] Neutral ≈ half the Financial PhraseBank corpus
- [x] LM MD&A example: S_LM = (1−4)/35 ≈ −0.086
- [x] GI alternative: ≈ −0.17
- [x] Fog index: 12 = high-school; MD&A: 18–22
- [x] Krippendorff α ≥ 0.667 reliable; ≥ 0.800 high confidence
- [x] Financial benchmark alphas: 0.65–0.78
- [x] F1 illustrative range: 0.70–0.80 FinBERT vs. 0.60–0.65 lexicon
- [x] FinBERT: 110M parameters
- [x] LLM inference cost: ~$100–$500 per million short sentences (2024)
- [x] Few-shot optimal: 4–8 in-context examples
- [x] Fine-tuning: 3–5 epochs, η₀ = 2×10⁻⁵, batch 32, weight decay 0.01
- [x] NVIX back to 1890
- [x] Gilbazo 2025: 1.6M fund-family posts
- [x] A100 GPU: hundreds of docs/sec for 110M-param model
- [x] Distillation: 110M → 33M, <5% accuracy loss
- [x] Twitter/X cashtag filter, Jaccard dedup threshold 0.6–0.8
- [x] 10-K filed within 60–90 days of fiscal year-end; 10-Q within 40–45 days
- [x] FOMC 30-minute announcement window (Nakamura 2018)
- [x] Streaming latency target: <100 ms for FOMC

### Citations (Author, year)
- [x] Antweiler & Frank (2004) — social media orthogonal to institutional sources
- [x] Bollen et al. (2011) — Twitter mood → DJIA
- [x] Da et al. (2015) — Google Trends retail attention → price pressure/reversal
- [x] Tetlock (2007) — WSJ pessimism → price pressure
- [x] Tetlock et al. (2008) — firm-level neg. words → earnings and returns
- [x] Manela & Moreira (2017) — NVIX from WSJ text back to 1890
- [x] Larcker & Zakolyukina (2012) — deception cues in calls → restatements
- [x] Feldman et al. (2010) — Q&A responsiveness → post-announcement drift
- [x] Cohen et al. (2020) — "lazy prices": unchanged 10-K → underperformance
- [x] Loughran & McDonald (2011) — LM dictionary; 10-K filing-day returns
- [x] Schmeling & Wagner (2019) — ECB/Fed tone → equity returns
- [x] Hansen & McMahon (2018) — FOMC topic modelling → inflation outcomes
- [x] Xu & Babaian (2025) — FinBERT+GPT-4o ensemble on FOMC
- [x] Nakamura & Steinsson (2018) — high-frequency monetary policy surprises; information vs. policy effect
- [x] Araci (2019) — FinBERT
- [x] Huang et al. (2023) — FinBERT further pre-training
- [x] Loukas et al. (2022) — SEC-BERT
- [x] Malo et al. (2014) — Financial PhraseBank
- [x] Brown et al. (2020) — GPT-3 / zero-shot classification
- [x] Ko & Lee (2024) — GPT-4 zero-shot vs. FinBERT on PhraseBank, FiQA, earnings
- [x] Maia et al. (2018) — FiQA opinion task dataset
- [x] López-Lira & Tang (2023) — GPT headlines → next-day returns
- [x] Kirtac & Germano (2024) — OPT vs. LM dictionary on Sharpe
- [x] Fatemi & Hu (2023) — fine-tuned small LLMs; extra few-shot shots add no gain
- [x] Cookson & Niessner (2020) — StockTwits disagreement → volume and spreads
- [x] Gilbazo et al. (2025) — fund-family tweets → fund inflows
- [x] Cookson et al. (2026) — SVB social media → bank runs
- [x] Chen et al. (2022) — WSB/GameStop → gamma-hedging amplification
- [x] Ke et al. (2019) — supervised NLP features → cross-sectional returns
- [x] Engle et al. (2020) — climate-news index; hedge portfolio
- [x] Price et al. (2012) — management tone → post-call abnormal returns
- [x] Davis et al. (2015) — manager-specific tone component → future earnings
- [x] Cook & Kazinnik (2023) — local LLMs for earnings calls; privacy trade-off
- [x] Siano (2025) — LLM embeddings explain more return variation than dictionaries
- [x] Li (2008) — Fog Index → earnings quality / volatility
- [x] Lehavy et al. (2011) — less readable 10-K → fewer, less accurate analysts
- [x] Li (2010) — uncertain forward-looking language → lower earnings persistence
- [x] Krippendorff (1970) — agreement metric
- [x] Fama (1970) — event study framework
- [x] Chiu & Hung (2024) — LLaMA-2 + LLM summarisation of long 10-Ks
- [x] Lehner (2024) — LLMs rewrite filings to shift measured tone
- [x] Stone et al. (1966) — Harvard General Inquirer
- [x] Kearney & Loughran (2014) — survey: lexicon and early ML literature
- [x] Loughran & McDonald (2020) — authoritative survey: textual analysis in corporate finance

### Figure
- [x] fig_lm_lexicon.png — embedded on the LM lexicon / sentiment-dictionary slide in index.html
- [x] fig_lm_lexicon.png — embedded on the LM dictionary case study slide in practical.html

---

## Omissions

*(None — all items checked above after the P3 rewrite.)*
