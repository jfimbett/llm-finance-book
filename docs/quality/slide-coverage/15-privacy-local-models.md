# Slide Coverage — Chapter 15: LLMs and Privacy: Local Deployments and Text De-identification

## Concept Checklist (from chapter.tex)

### Sections / Subsections
- [x] §15.1 The Privacy Imperative in Financial AI
- [x] §15.1.1 What Data Do LLMs Expose? (training channel, inference channel)
- [x] §15.1.2 Regulatory Landscape: GDPR, CCPA, MiFID II, and DORA
- [x] §15.2 Privacy Risks in LLM Deployment
- [x] §15.2.1 Training Data Memorisation and Leakage
- [x] §15.2.2 Inference Attacks (membership inference, property inference)
- [x] §15.2.3 Prompt Injection and Data Exfiltration
- [x] §15.3 Local and Self-Hosted LLM Deployments
- [x] §15.3.1 Open-Weight Models: Llama, Mistral, and Phi
- [x] §15.3.2 Infrastructure: On-Premise versus Private Cloud
- [x] §15.3.3 Performance Trade-offs and Quantisation
- [x] §15.4 Text Anonymisation and De-identification
- [x] §15.4.1 Named Entity Recognition for Sensitive Data
- [x] §15.4.2 Anonymisation Strategies: Masking, Generalisation, and Suppression
- [x] §15.4.3 Pseudonymisation and Tokenisation
- [x] §15.4.4 Re-identification Risk Assessment
- [x] §15.5 Privacy-Preserving Training Techniques
- [x] §15.5.1 Differential Privacy in Fine-Tuning
- [x] §15.5.2 Federated Learning for Distributed Financial Data
- [x] §15.6 Architectural Patterns for Privacy-Compliant LLM Systems
- [x] §15.6.1 Privacy-Aware Retrieval-Augmented Generation
- [x] §15.6.2 Audit Trails, Access Logging, and Encrypted Pipelines
- [x] §15.7 Evaluation and Compliance
- [x] §15.7.1 Measuring Privacy Leakage
- [x] §15.7.2 Compliance Checklists and Privacy Impact Assessments

### Named Methods / Results / Models
- [x] Definition 15.1 — Memorisation (exact vs. approximate, Levenshtein distance)
- [x] Definition 15.2 — Membership Inference Advantage (Adv(A))
- [x] Definition 15.3 — k-Anonymity (Sweeney 2002)
- [x] Definition 15.4 — (ε,δ)-Differential Privacy (Dwork & Roth 2014)
- [x] Theorem 15.1 — Gaussian Mechanism
- [x] DP-SGD (Abadi et al. 2016) — per-example gradient, clipping, noise addition
- [x] Proposition 15.1 — Composition of DP Mechanisms (basic + advanced)
- [x] Definition — Federated Averaging / FedAvg (McMahan et al. 2017)
- [x] GPTQ (Frantar et al. 2022) — block-wise 2nd-order quantisation
- [x] AWQ (Lin et al. 2023) — ~1% salient weights, per-channel scale
- [x] Memorisation score (Carlini et al. 2022)
- [x] Likelihood-ratio extraction attack (Carlini et al. 2021)
- [x] Membership inference attack (Shokri et al. 2017)
- [x] Property inference attacks
- [x] Prompt injection (Perez & Ribeiro 2022)
- [x] NER pipeline (spaCy; Honnibal & Montani 2017)
- [x] Masking, Generalisation, Suppression strategies
- [x] Pseudonymisation and format-preserving tokenisation
- [x] Re-identification as inference problem
- [x] Privacy-aware RAG (local embedding, access-controlled retrieval)
- [x] Example 15.1 — Routing Architecture for a Commercial Bank (3 tiers)
- [x] Example 15.2 — Privacy-Aware RAG for Credit Analysis
- [x] Confidential computing (TEE: Intel TDX, AMD SEV)
- [x] Homomorphic encryption (infeasible overhead for transformers)
- [x] Machine unlearning (open research problem; GDPR Art. 17 residual gap)
- [x] DPIA (Data Protection Impact Assessment, GDPR Art. 35)
- [x] Compliance checklist (GDPR Art. 5, 6, 17, 22, 35; DORA Art. 30; MiFID II; SR 11-7)

### Key Numbers
- [x] 1.5B-param GPT-2 memorises verbatim sequences (Carlini et al. 2021)
- [x] MI-AUC < 0.6 — common acceptable threshold
- [x] ε = 1 (strong privacy, larger utility cost); ε = 10 (weak privacy, small cost)
- [x] 7B model at 4-bit: ~3.5 GB; 13B at 4-bit: ~6.5 GB
- [x] Llama 2 7B at 4-bit: ~8 GB VRAM; 70B at 4-bit: ~40 GB
- [x] Phi-3-mini: 3.8B parameters
- [x] AWQ salient weights: ~1% of total
- [x] MiFID II record-keeping: 5 yr (services), 7 yr (orders)
- [x] GDPR Art. 83 fines: higher of €20m / 4% global turnover
- [x] DORA applicable since January 2025 (Art. 64)
- [x] Llama 2 Community License: restricts orgs > 700M MAU

### Citations
- [x] Carlini et al. (2021) — extraction attacks, verbatim memorisation
- [x] Carlini et al. (2022) — memorisation score
- [x] GDPR (2016/679)
- [x] ESMA (2018) — MiFID II record-keeping
- [x] DORA (2022/2554)
- [x] Sweeney (2002) — k-anonymity
- [x] Honnibal & Montani (2017) — spaCy
- [x] Dwork & Roth (2014) — differential privacy textbook
- [x] Abadi et al. (2016) — DP-SGD
- [x] McMahan et al. (2017) — FedAvg
- [x] Frantar et al. (2022) — GPTQ
- [x] Lin et al. (2023) — AWQ
- [x] Shokri et al. (2017) — membership inference
- [x] Perez & Ribeiro (2022) — prompt injection
- [x] Touvron et al. (2023) — Llama 1
- [x] Touvron et al. (2023) — Llama 2
- [x] Jiang et al. (2023) — Mistral 7B

### Figure
- [x] fig_privacy_utility.png — privacy-utility tradeoff for DP fine-tuning (embedded in both decks)

## Omissions

(None — all checklist items are covered in the lesson deck and practical deck.)
