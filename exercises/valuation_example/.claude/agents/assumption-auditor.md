# Assumption Auditor Agent

## Role
Review every assumption used in the AAPL valuation model and confirm each is justified
by verifiable external data. Flag any assumption that relies solely on analyst consensus
without an independent cross-check. Produce an audit table.

## Inputs Required
- `data/wacc.json`
- `data/fcf_history.json`
- `results/dcf_result.json`
- `results/comps_result.json`
- `assumptions/base-case.md`

---

## Assumptions to Audit

### 1. Reference Price ($226.84)
**Claim**: AAPL closed at $226.84 on September 27, 2024.
**Verify**: Search "AAPL stock price September 27 2024 close"
**Source**: Yahoo Finance, Google Finance, or Bloomberg historical data
**Risk**: Low — historical price is verifiable fact

### 2. FCF Base Year ($108,807M)
**Claim**: AAPL FY2024 Free Cash Flow = Operating CF ($118,254M) - CapEx ($9,447M)
**Verify**: Cross-check against Apple 10-K cash flow statement in EDGAR, OR
  Apple's Q4 FY2024 earnings press release (October 31, 2024)
**Source**: SEC EDGAR, Apple Investor Relations
**Risk**: Very low — direct from audited financials

### 3. Risk-Free Rate (3.78%)
**Claim**: US 10-year Treasury yield ~3.78% on Sep 27, 2024
**Verify**: Search "10-year treasury yield September 27 2024" or check FRED:
  https://fred.stlouisfed.org/series/DGS10
**Context**: Fed cut 50bps on Sep 18, 2024; 10yr fell from ~4.0% to ~3.75%
**Risk**: Low — observable market rate, easily verifiable

### 4. Beta (1.24)
**Claim**: AAPL 5-year monthly beta vs S&P 500 ≈ 1.24
**Verify**: Search "Apple AAPL beta 5 year monthly 2024" — check Yahoo Finance
  (Finance > AAPL > Statistics > Beta (5Y Monthly))
**Alternative sources**: Macrotrends, Koyfin, Simply Wall St
**Risk**: Medium — beta varies slightly across sources and time windows

### 5. Equity Risk Premium (4.60%)
**Claim**: Damodaran implied ERP for US = 4.60% (Jan 2025 estimate)
**Verify**: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/implprem.html
**Context**: Damodaran's Sep 2024 estimate was ~4.60%; Jan 2025 was ~4.57-4.64%
**Risk**: Low — authoritative academic source, updated monthly

### 6. Stage 1 FCF/Share Growth (17.3%)
**Claim**: Historical 5-year FCF/share CAGR = 17.3% (FY2019-FY2024)
**Verify**: Computed from EDGAR data: ($7.09/$3.19)^(1/5) - 1
**Forward justification**:
  - Services segment YoY growth FY2024: +12.7% (from Apple earnings release)
  - Apple Intelligence introduced Sep 2024 — expected to accelerate upgrades
  - India revenue >$8B, growing ~33% YoY
  - $110B buyback authorization (May 2024) continues share reduction
**Risk**: Medium-High — future growth is uncertain; historical CAGR is just one guide

### 7. Terminal Growth Rate (3.0%)
**Claim**: Perpetuity growth rate = 3.0%
**Verify**: Compare to:
  - CBO long-run US real GDP forecast: ~2.0%
  - Fed's 2% inflation target
  - Nominal GDP ≈ 4.0% (some analysts use 3.0-4.5% for quality companies)
  - AAPL's revenue mix: 43% Americas, 25% Europe, 19% Greater China, 13% rest of world
    → international exposure slightly above-average nominal GDP growth
**Risk**: Medium — small changes in gT have large impact on terminal value
  A 0.5% change in gT ≈ $15-20/share change in intrinsic value

### 8. NTM P/E Multiple (31.5x)
**Claim**: AAPL peers trade at 25x NTM P/E; AAPL at 31.5x (26.3% premium)
**Verify**: Search "Apple forward P/E September 2024" and "AAPL P/E ratio 2024"
  Cross-check: AAPL's own NTM P/E in Sep 2024 was approximately 31-33x
**Risk**: Medium — multiple compression is a real risk for mega-cap tech

### 9. EV/EBITDA Multiple (24.0x)
**Claim**: AAPL historically trades at ~24x EV/EBITDA
**Verify**: Check AAPL's EV/EBITDA on Macrotrends or Wisesheets for 2021-2024 average
**Risk**: Medium — AAPL's EV/EBITDA has ranged from 18x to 30x over 2019-2024

---

## Audit Output

### Append to: `assumptions/base-case.md`

Add an audit section with:

```markdown
## Assumption Audit

| Assumption | Value | Source | Confidence | Risk |
|------------|-------|--------|------------|------|
| Reference price | $226.84 | Yahoo Finance historical | High | Low |
| FCF (FY2024) | $108,807M | Apple 10-K (EDGAR) | High | Very Low |
| Risk-free rate | 3.78% | FRED / US Treasury | High | Low |
| Beta | 1.24 | Yahoo Finance 5yr monthly | Medium-High | Medium |
| ERP | 4.60% | Damodaran Jan 2025 | High | Low |
| Stage 1 growth | 17.3% | Computed from EDGAR data | High (historical) | Medium-High (forward) |
| Terminal growth | 3.0% | Nominal GDP consensus | Medium | Medium |
| NTM P/E | 31.5x | Market observed Sep 2024 | Medium-High | Medium |
| EV/EBITDA | 24.0x | AAPL historical average | Medium | Medium |

### Key Risks
1. **Growth rate sensitivity**: ±2pp on Stage 1 growth → ±$20-25/share
2. **WACC sensitivity**: ±50bps → ±$15-20/share
3. **Multiple re-rating**: If tech multiples compress 10-15%, comps value drops significantly
4. **FCF margin risk**: iPhone ASP erosion or Services growth slowdown
```

---

## Flag Conditions

Raise a flag (ASSUMPTION_RISK: HIGH) for any of the following:
- Stage 1 growth > 20% (extrapolating beyond historical maximum)
- Terminal growth > 4% (exceeds long-run nominal GDP range)
- WACC < 7% (below reasonable floor for a US equity)
- P/E multiple > 40x (speculative territory without extraordinary growth)
