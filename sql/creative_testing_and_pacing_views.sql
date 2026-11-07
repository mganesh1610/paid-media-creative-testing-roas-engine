-- ============================================================================
-- Omnichannel Paid Media Creative Iteration, A/B Testing & ROAS Optimization
-- Analytical SQL Views (SQL Joins & CTEs)
-- ============================================================================

WITH channel_creative_rollup AS (
    SELECT
        c.channel_platform,
        c.creative_hook,
        c.audience_segment,
        c.landing_page_variant,
        COUNT(DISTINCT c.campaign_cell_id) AS active_cells,
        SUM(c.impressions) AS total_impressions,
        SUM(c.three_sec_video_views) AS total_thumb_stops,
        SUM(c.engagements) AS total_engagements,
        SUM(c.clicks) AS total_clicks,
        SUM(c.conversions) AS platform_conversions,
        SUM(c.spend_usd) AS total_spend_usd,
        SUM(c.revenue_usd) AS total_revenue_usd,
        ROUND(100.0 * SUM(c.three_sec_video_views) / NULLIF(SUM(c.impressions), 0), 2) AS thumb_stop_rate_pct,
        ROUND(100.0 * SUM(c.engagements) / NULLIF(SUM(c.impressions), 0), 2) AS engagement_rate_pct,
        ROUND(100.0 * SUM(c.clicks) / NULLIF(SUM(c.impressions), 0), 2) AS ctr_pct,
        ROUND(100.0 * SUM(c.conversions) / NULLIF(SUM(c.clicks), 0), 2) AS cvr_pct,
        ROUND(SUM(c.spend_usd) / NULLIF(SUM(c.conversions), 0), 2) AS cpa_usd,
        ROUND(SUM(c.revenue_usd) / NULLIF(SUM(c.spend_usd), 0), 2) AS roas_ratio
    FROM campaign_creative_cells c
    GROUP BY
        c.channel_platform,
        c.creative_hook,
        c.audience_segment,
        c.landing_page_variant
),
ga4_pixel_reconciliation AS (
    SELECT
        t.campaign_cell_id,
        t.utm_source_medium,
        t.pixel_events_fired,
        t.ga4_verified_conversions,
        t.utm_tag_compliant_flag,
        ROUND(
            100.0 * ABS(t.pixel_events_fired - t.ga4_verified_conversions)
            / NULLIF(t.pixel_events_fired, 0),
            2
        ) AS discrepancy_pct
    FROM tracking_pixel_utm_audit t
)
SELECT
    r.channel_platform,
    r.creative_hook,
    r.audience_segment,
    r.landing_page_variant,
    r.total_impressions,
    r.thumb_stop_rate_pct,
    r.ctr_pct,
    r.cvr_pct,
    r.cpa_usd,
    r.roas_ratio,
     ROUND(AVG(g.discrepancy_pct), 2) AS avg_pixel_ga4_discrepancy_pct
FROM channel_creative_rollup r
INNER JOIN campaign_creative_cells c
    ON r.channel_platform = c.channel_platform
   AND r.creative_hook = c.creative_hook
   AND r.audience_segment = c.audience_segment
   AND r.landing_page_variant = c.landing_page_variant
INNER JOIN ga4_pixel_reconciliation g
    ON c.campaign_cell_id = g.campaign_cell_id
GROUP BY
    r.channel_platform,
    r.creative_hook,
    r.audience_segment,
    r.landing_page_variant
ORDER BY r.roas_ratio DESC;
