-- TEST ONLY
-- Simulates a schema/data issue for the failure-handling workflow.

SELECT
    DATE(order_purchase_timestamp) AS report_date,
    ROUND(SUM(payment_value), 2) AS total_sales,
    COUNT(DISTINCT order_id) AS total_orders,

    -- Intentional error:
    -- payment_value does not have this column.
    SUM(payment_value_invalid) AS invalid_metric

FROM ecommerce_dashboard

WHERE DATE(order_purchase_timestamp) = %s

GROUP BY DATE(order_purchase_timestamp);