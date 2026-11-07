# Schema & Analytical Methodology

## 1. Warehouse Tables (`SQLite` / `SQL Joins & CTEs`)

### `campaign_creative_cells` (`24` structured omnichannel cells aggregating `109,211` records)
- `campaign_cell_id` (`TEXT PRIMARY KEY`): `CELL-01` through `CELL-24`.
- `channel_platform` (`TEXT`): `Meta Ads Manager`, `Google Ads`, `YouTube Ads`, `DV360 Programmatic`.
- `creative_hook` (`TEXT`): `UGC Problem-Solution Hook`, `Social Proof Short-Form Video`, `Static Legacy Banner (Fatigued)`.
- `audience_segment` (`TEXT`): Platform-aligned targeting tier (`1% High-LTV Lookalike & Retargeting`, `High-Intent Exact & Phrase Search`, `Custom Intent & In-Market Video`, `First-Party CRM & Contextual PMP`).
- `landing_page_variant` (`TEXT`): `High-Velocity Direct Checkout LP` vs. `Standard Generic Catalog LP`.
- `impressions`, `three_sec_video_views`, `engagements`, `clicks`, `conversions` (`INTEGER`).
- `spend_usd`, `revenue_usd`, `avg_frequency` (`REAL`), `fatigue_flag` (`INTEGER`).

### `tracking_pixel_utm_audit` (`24` cell-level pixel/GA4 reconciliation audits)
- `campaign_cell_id` (`TEXT PRIMARY KEY`)
- `utm_source_medium` (`TEXT`)
- `pre_fix_pixel_events`, `pixel_events_fired`, `ga4_verified_conversions` (`INTEGER`)
- `pre_fix_discrepancy_pct`, `post_fix_discrepancy_pct` (`REAL`)
- `utm_tag_compliant_flag` (`INTEGER`)

## 2. Formulations

- **Thumb-Stop Rate ($TSR$):**
  $$TSR = \frac{\text{3-Second Video Views}}{\text{Impressions}} \times 100\%$$
- **Frequency-Induced Creative Fatigue Decay:**
  $$TSR(f) = TSR_0 \cdot \exp\left(-\gamma \cdot \max(0, f - f_0)\right), \quad \gamma = 0.16, \quad f_0 = 2$$
- **Two-Proportion A/B Z-Test & Wilson-Newcombe 95% Confidence Interval:**
  $$Z = \frac{\hat{p}_T - \hat{p}_C}{\sqrt{\hat{p}_{\text{pool}}(1 - \hat{p}_{\text{pool}})\left(\frac{1}{n_T} + \frac{1}{n_C}\right)}}, \quad \text{CI}_{95\%} = (\hat{p}_T - \hat{p}_C) \pm 1.96\sqrt{\frac{\hat{p}_T(1-\hat{p}_T)}{n_T} + \frac{\hat{p}_C(1-\hat{p}_C)}{n_C}}$$
- **Diminishing-Returns Marginal ROAS Reallocation:**
  $$R_{\text{opt}} = \left(R_{\text{win}} + \Delta S \cdot \text{ROAS}_{\text{win}} \cdot \eta\right) + \left(R_{\text{fat}} - \Delta S \cdot \text{ROAS}_{\text{fat}}\right), \quad \eta = 0.90, \quad \Delta S = 0.65 \cdot S_{\text{fat}}$$
