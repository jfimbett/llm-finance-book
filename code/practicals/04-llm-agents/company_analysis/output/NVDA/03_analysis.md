# NVIDIA Corporation (NVDA) — Financial Analysis

*Fiscal year ends late January; "FY2026" = period ended 2026-01-25. All figures from `02_financials.json` and the FY2026 10-K (filed 2026-02-25) unless noted. No live market price is available, so valuation is framed qualitatively and on a per-share basis.*

## Executive Summary

NVIDIA closed FY2026 with **$215.9B in revenue (+65% YoY)** and **$120.1B in net income (+65%)**, having compounded revenue at a **68% CAGR** and net income at an **87% CAGR** over FY2022–FY2026 — a scale-up with virtually no precedent for a company of this size. The Data Center franchise ($193.7B, ~90% of revenue) and the CUDA software moat remain the engine, and the balance sheet is fortress-grade (net cash, ~0.05x debt/equity, $62.6B in cash and securities). The clear takeaways for a PM: (1) the fundamentals are exceptional and cash generation is real — **$96.7B free cash flow, 45% FCF margin**; (2) the two genuine watch-items are **gross-margin normalization** (71.1% in FY2026, down from 75.0%, partly from a $4.5B H20 charge and the Blackwell transition) and **extreme concentration** (one customer at 22% of revenue, top two at 36%, Data Center at ~90%); and (3) the **$95.2B of inventory purchase and supply/capacity commitments** is both a demand-confidence signal and the single largest obsolescence risk on a one-year product cadence. The debate is not the quality of the business but the durability of hyperscaler AI capex and how much of it is already priced in.

## 1. Business & Segment Performance

Revenue is now overwhelmingly Data Center (FY2026 end-market disclosure, $M):

| End market | FY2026 | FY2025 | YoY | % of FY26 rev |
|---|---|---|---|---|
| Data Center | 193,737 | 115,186 | +68% | 89.7% |
| — Compute | 162,361 | 102,196 | +59% | 75.2% |
| — Networking | 31,376 | 12,990 | +142% | 14.5% |
| Gaming | 16,042 | 11,350 | +41% | 7.4% |
| Professional Visualization | 3,191 | 1,878 | +70% | 1.5% |
| Automotive | 2,349 | 1,694 | +39% | 1.1% |
| OEM & Other | 619 | 389 | — | 0.3% |
| **Total** | **215,938** | **130,497** | **+65%** | 100% |

Two observations matter. First, **Networking grew +142%**, faster than Compute (+59%), validating the rack-scale / full-system strategy (NVLink, Spectrum-X, InfiniBand from Mellanox) — NVIDIA increasingly sells integrated AI factories, not chips, which deepens lock-in and lifts dollar content per deployment. Second, the non-DC segments, while healthy in growth terms, are now rounding error to the thesis: Gaming, ProViz and Automotive together are ~10% of revenue. The company is, for investment purposes, a Data Center accelerated-computing business with cyclical consumer/auto optionality attached.

## 2. Growth Trajectory & Sustainability

The trajectory is staggering but decelerating off a vast base: revenue growth ran +126% (FY2024), +114% (FY2025), and **+65% (FY2026)**. Deceleration at this scale is mathematically inevitable and not itself a red flag, but at NVIDIA's valuation the *second derivative* is what the market trades on. Sustainability rests on three legs the 10-K supports and three it cannot resolve:

- **Supportive:** a stated **one-year product cadence** (Hopper → Blackwell → Blackwell Ultra/GB300, shipping since Q2 FY2026 → **Rubin**, production in 2H FY2027 with a claimed ~10x cost-per-token reduction vs. Blackwell). This cadence is a genuine competitive weapon that resets the performance bar annually and pressures AMD and custom ASICs.
- **Unresolved:** the durability of hyperscaler capex; whether AI infrastructure ROI materializes for end customers; and the company's own caveat that **energy/power availability is a "complex, multi-year" constraint** that could "delay customer and partner deployments or reduce the scale" of AI adoption. Demand visibility beyond ~12 months is thin: remaining performance obligations on contracts >1 year are only **$2.3B** — NVIDIA's "backlog" lives in purchase commitments and informal allocation, not contracted RPO.

The honest read: growth is real and supply-led today, but forward sustainability is a judgment about a capex cycle, not a fact in the filings.

## 3. Margin Structure & Pricing Power

NVIDIA's margins are extraordinary for hardware and signal real pricing power and embedded software value:

| Metric | FY2023 | FY2024 | FY2025 | FY2026 |
|---|---|---|---|---|
| Gross margin | 56.9% | 72.7% | 75.0% | **71.1%** |
| Operating margin | 15.7% | 54.1% | 62.4% | **60.4%** |
| Net margin | 16.2% | 48.9% | 55.9% | **55.6%** |

A 60% *operating* margin on $216B of revenue is the headline of the entire analysis. But note the **gross-margin step-down from 75.0% to 71.1%**. Management attributes this to (a) the business-model shift from "Hopper HGX systems to Blackwell full-scale datacenter solutions" — selling more system/networking content dilutes percentage margin even as it grows gross profit dollars — and (b) the **$4.5B H20 charge**. Inventory and excess-commitment provisions were **$7.2B in FY2026 vs. $3.7B in FY2025**, a **2.6% unfavorable gross-margin hit** (2.3% prior year). This is the key margin debate: is ~71% the new floor for a richer-mix, system-level franchise, or the start of normalization as AMD/ASICs and hyperscaler in-housing erode pricing? The data cannot settle it; a break into the 60s without a clear mix explanation would be the signal to worry.

## 4. R&D, Cash Flow & Capital Returns

**R&D rose 43% to $18.5B**, funding the annual cadence and the moat. Notably, R&D *intensity fell* to **8.6% of revenue** (from 27.2% in FY2023) — revenue is simply outrunning a still-growing R&D base, the textbook signature of operating leverage rather than under-investment. Stock-based comp of $6.4B is large in absolute terms but only ~3% of revenue; diluted share count actually *fell* (25.35B → 24.51B split-adjusted) as buybacks more than offset SBC dilution.

Cash conversion is excellent. **Operating cash flow was $102.7B** (0.86x of net income), and **free cash flow was $96.7B (45% FCF margin)** against modest fabless capex of $6.0B. Capital returns are now substantial: **$40.1B of buybacks and $1.0B of dividends** in FY2026, with a fresh **$60B repurchase authorization (Aug 2025)** leaving **$58.5B outstanding**. The dividend ($0.04/sh) is a rounding error and not the story; buybacks are the return vehicle. One caveat from the cash-flow statement: investing outflows jumped to **$52.2B**, driven partly by **equity-investment purchases** (including a disclosed Intel common-stock stake and a Groq license) — NVIDIA is increasingly funding its own ecosystem/demand (Neocloud builders, AI labs), which is strategically rational but introduces circular-financing optics and mark-to-market volatility in "Other income."

## 5. Balance Sheet & Solvency

Effectively unlevered and cash-rich. FY2026: **$62.6B cash + marketable securities**, total long-term debt of just **$8.5B**, **debt/equity 0.05x**, equity of **$157.3B**, and **$22.6B net cash** (the metric understates strength — it excludes ~$22.3B of non-current equity stakes and non-current securities per the data notes). Solvency risk is negligible. Liquidity is comfortable: **current ratio 3.9x**. The watch-items are working-capital, not solvency: **receivables nearly doubled to $38.5B** and **inventory more than doubled to $21.4B** — both consistent with a demand-led ramp, but the AR build concentrates counterparty risk in a handful of large buyers, and the inventory build raises obsolescence exposure given annual product turns.

## 6. Valuation Framing (No Live Price)

Per-share fundamentals: **diluted EPS $4.90** (split-adjusted), up from $2.94, an 89% EPS CAGR FY2022–FY2026; **FCF/share ≈ $3.94** ($96.7B / 24.51B shares). Without a market price I cannot compute P/E or FCF yield, but the framing for a PM is: NVIDIA earns its premium *only* if growth persists. At a ~45% FCF margin and a net-cash balance sheet, the quality side of "growth-at-a-price" is unimpeachable; the risk is entirely on the durability and multiple side. The central tension is that decelerating-but-still-high growth (+65%) must be weighed against a multiple that historically prices in years of continued AI capex expansion — and against the concentration and policy risks below. Per-share value compounds further from buybacks shrinking the share count.

## 7. Risk Assessment

- **Customer concentration (high):** In FY2026, **one direct customer = 22% of revenue and a second = 14%** (top two = 36%), both Compute & Networking; additional indirect customers each >10%. The 10-K flags that one AI lab drives a "meaningful amount" of revenue via cloud customers. Loss or pullback of one buyer is materially impactful.
- **China / export controls (high, partly realized):** China (incl. Hong Kong) fell to **$19.7B / 9.1% of revenue (FY2026) from $25.0B / 19.2% (FY2025)**. The USG requires licenses for H20-class parts; NVIDIA took a **$4.5B H20 charge** and generated only **~$60M** of licensed H20 revenue, with USG reportedly expecting **15%+ of China-licensed revenue**. The filing states NVIDIA is "effectively foreclosed" from much of the China market, which is now being ceded to domestic competitors — a structural, not transient, headwind.
- **Hyperscaler in-sourcing & competition (medium-high):** The same concentrated buyers (Google TPU, Amazon Trainium, custom ASICs, plus AMD) are building alternatives. CUDA lock-in and the one-year cadence are the defenses; share erosion would show first in gross margin.
- **Inventory & purchase-commitment obsolescence (high):** **$95.2B of inventory-purchase and long-term supply/capacity obligations** against $21.4B of on-hand inventory — roughly 4.4x inventory. This is a confidence signal (NVIDIA prepays TSMC/CoWoS/HBM capacity), but on a one-year product cycle any demand air-pocket or node stumble converts commitments into write-downs. The auditor flagged inventory valuation as a **critical audit matter**.
- **Margin normalization (medium):** Already underway (75.0% → 71.1%); mix shift to systems plus provisions are the drivers. Bears should track whether 71% holds.
- **Supply/power constraints (medium):** Supply chain concentrated in Asia (mitigated modestly by US/Latin America expansion); energy availability cited as a multi-year limiter on customer deployment scale.

## 8. Outlook & Recommendation

**Constructive on the business, disciplined on the entry.** NVIDIA is a genuinely exceptional franchise — 60% operating margins, 45% FCF margin, net cash, a widening software/system moat, and an annual product cadence (Rubin in 2H FY2027) that competitors struggle to match. The financials show no signs of demand exhaustion: +65% revenue, +142% networking, and a $95.2B forward supply commitment all point to management betting on continued scale.

The case *against* complacency is equally concrete and lives in the same filing: revenue is ~90% one segment, 36% two customers, gross margin has already rolled over ~390bp, China has been structurally impaired, and the $95.2B of commitments is a double-edged sword that amplifies the downside if the hyperscaler capex cycle inflects. None of these are hypothetical — the H20 write-down and the China revenue decline are realized examples of the tail risks materializing.

For a portfolio manager: treat NVDA as a high-quality, high-beta expression of the AI-infrastructure capex cycle rather than a defensive compounder. The fundamentals justify a premium; the appropriate position size should reflect that the thesis is a *bet on the durability of customer capex*, with concentration and policy risk that can move fast. Key monitorables: sequential Data Center growth and forward guidance, gross margin holding ~71%+, China policy developments, the top-customer percentages in subsequent filings, and the inventory/purchase-commitment balance relative to realized demand. A sustained sequential Data Center deceleration *combined* with a sub-70% gross margin would be the signal to reduce.

---

### Data caveats (from `02_financials.json` notes and 10-K)
- Per-share/share series are split-adjusted to the post-June-2024 10:1 basis for comparability; FY2022 as-reported diluted EPS was $3.85.
- Revenue/cost/capex/marketable-securities series merge differing XBRL tags across years; figures are as-filed (latest values capture restatements).
- `net_cash_position` excludes ~$22.3B of non-current equity stakes and non-current securities, so it understates true balance-sheet strength.
- Valuation multiples (P/E, EV/EBITDA, FCF yield) are not computed — no live price feed; per-share metrics provided instead.
