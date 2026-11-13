# SEO / GEO, Marketplace & Cross-Channel Weekly/Monthly Self-Serve Readout Mart (`P1` Extension)

Extends `paid-media-creative-testing-roas-engine` across **109,211 SHA-256 verified public campaign & direct-response records** (`64,000` Kevin Hillstrom multichannel assignments + `45,211` UCI Direct Marketing records) to materialize automated weekly and monthly stakeholder scorecards for **Power BI, Tableau, Looker, and Advanced Excel**.

## Verified Results

- **Combined Public Records:** `109,211` across **6 Digital Demand Channels** (`Paid Search`, `Email & Lifecycle CRM`, `SEO / GEO Organic`, `Paid Social`, `eCommerce Direct`, `Marketplaces & Syndication`) and **18 monthly channel cohorts**.
- **Settled Orders & Revenue:** `5,867` warehouse-settled orders (`$1,468,843.13` revenue on `$204,119.40` spend; **`7.20x` blended ROAS**).
- **GA4 & Adobe Analytics Order Reconciliation:** Reconciled platform-reported vs. warehouse-settled conversions to **`0.085%` (`< 0.1%`) variance**.
- **Governance & Testing:** Passed **`8/8 (100%)`** automated SQL parity gates and **`3/3`** unit tests (`rm -rf data/` clean cache ignored via `.gitignore`).

## Run Locally

```bash
python3 src/seo_geo_marketplace_readout.py
python3 tests/test_seo_geo_readout.py
```
