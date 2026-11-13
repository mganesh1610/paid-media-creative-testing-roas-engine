-- =============================================================================
-- Automated Weekly & Monthly Self-Serve Performance Readout Views
-- Channels: Paid Search, Email, SEO/GEO, Paid Social, eCommerce & Marketplaces
-- =============================================================================

DROP VIEW IF EXISTS vw_weekly_monthly_channel_readout;
CREATE VIEW vw_weekly_monthly_channel_readout AS
WITH unified_events AS (
    SELECT
        reporting_month,
        reporting_week,
        channel_name,
        audience_tier,
        sessions,
        leads,
        platform_reported_orders,
        warehouse_settled_orders,
        media_spend_usd,
        settled_revenue_usd,
        net_new_customer_orders
    FROM omnichannel_readout_staging
)
SELECT
    reporting_month,
    channel_name,
    SUM(sessions) AS total_sessions,
    SUM(leads) AS total_leads,
    SUM(platform_reported_orders) AS platform_orders,
    SUM(warehouse_settled_orders) AS settled_orders,
    SUM(net_new_customer_orders) AS net_new_orders,
    ROUND(SUM(media_spend_usd), 2) AS spend_usd,
    ROUND(SUM(settled_revenue_usd), 2) AS revenue_usd,
    ROUND(SUM(settled_revenue_usd) / NULLIF(SUM(media_spend_usd), 0), 3) AS blended_roas,
    ROUND(
        ABS(SUM(platform_reported_orders) - SUM(warehouse_settled_orders)) * 100.0
        / NULLIF(SUM(warehouse_settled_orders), 0),
        2
    ) AS tracking_discrepancy_pct
FROM unified_events
GROUP BY reporting_month, channel_name
ORDER BY reporting_month, revenue_usd DESC;
