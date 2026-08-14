-- ============================================================
-- Daily Sales Report
-- ============================================================
-- Returns daily sales KPIs for a supplied reporting date.
-- The Python automation will later provide the date.
-- ============================================================

SELECT
    DATE(order_purchase_timestamp) AS report_date,

    ROUND(SUM(payment_value), 2) AS total_sales,

    COUNT(DISTINCT order_id) AS total_orders,

    ROUND(
        SUM(payment_value) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value

FROM ecommerce_dashboard

WHERE DATE(order_purchase_timestamp) = %s

GROUP BY DATE(order_purchase_timestamp);