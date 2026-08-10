-- ============================================================
-- E-Commerce Sales & Customer Analytics
-- SQL Analysis
-- ============================================================
-- Purpose:
--   Exploratory and business analysis used to support the
--   Power BI E-Commerce Sales & Customer Analytics dashboard.
--
-- Database: MySQL
-- ============================================================

-- ============================================================
-- 1. DATA EXPLORATION
-- ============================================================

-- Preview the main tables
SELECT * FROM `retail_analytics orders` LIMIT 10;
SELECT * FROM `retail_analytics ecommerce` LIMIT 10;

-- Check row counts
SELECT COUNT(*) AS order_rows
FROM `retail_analytics orders`;

SELECT COUNT(*) AS ecommerce_rows
FROM `retail_analytics ecommerce`;

-- ============================================================
-- 2. ORDER VOLUME
-- ============================================================

-- Total number of unique orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM `retail_analytics orders`;

-- Orders by month
SELECT
    DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS order_month,
    COUNT(DISTINCT order_id) AS total_orders
FROM `retail_analytics orders`
GROUP BY DATE_FORMAT(order_purchase_timestamp, '%Y-%m')
ORDER BY order_month;


-- ============================================================
-- 3. SALES ANALYSIS
-- ============================================================

-- Total sales / payment value
SELECT
    ROUND(SUM(payment_value), 2) AS total_sales
FROM `retail_analytics ecommerce`;

-- Average order value
SELECT
    ROUND(
        SUM(payment_value) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM `retail_analytics ecommerce`;

-- Monthly sales
SELECT
    DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS order_month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_sales,
    ROUND(AVG(payment_value), 2) AS average_order_value
FROM `retail_analytics ecommerce`
GROUP BY DATE_FORMAT(order_purchase_timestamp, '%Y-%m')
ORDER BY order_month;


-- ============================================================
-- 4. PRODUCT CATEGORY ANALYSIS
-- ============================================================

-- Sales by product category
SELECT
    product_category,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_sales
FROM `retail_analytics ecommerce`
GROUP BY product_category
ORDER BY total_sales DESC;

-- Orders by product category
SELECT
    product_category,
    COUNT(DISTINCT order_id) AS total_orders
FROM `retail_analytics ecommerce`
GROUP BY product_category
ORDER BY total_orders DESC;

-- Average order value by product category
SELECT
    product_category,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(payment_value) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM `retail_analytics ecommerce`
GROUP BY product_category
ORDER BY average_order_value DESC;

-- Top 15 categories by sales
SELECT
    product_category,
    ROUND(SUM(payment_value), 2) AS total_sales
FROM `retail_analytics ecommerce`
GROUP BY product_category
ORDER BY total_sales DESC
LIMIT 15;

-- Top 15 categories by orders
SELECT
    product_category,
    COUNT(DISTINCT order_id) AS total_orders
FROM `retail_analytics ecommerce`
GROUP BY product_category
ORDER BY total_orders DESC
LIMIT 15;


-- ============================================================
-- 5. GEOGRAPHIC / STATE ANALYSIS
-- ============================================================

-- Orders by customer state
SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS total_orders
FROM `retail_analytics ecommerce`
GROUP BY customer_state
ORDER BY total_orders DESC;

-- Sales by customer state
SELECT
    customer_state,
    ROUND(SUM(payment_value), 2) AS total_sales
FROM `retail_analytics ecommerce`
GROUP BY customer_state
ORDER BY total_sales DESC;

-- Average delivery time by state
SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(delivery_days), 2) AS average_delivery_days
FROM `retail_analytics orders`
GROUP BY customer_state
ORDER BY average_delivery_days DESC;


-- ============================================================
-- 6. DELIVERY PERFORMANCE
-- ============================================================

-- Overall average delivery days
SELECT
    ROUND(AVG(delivery_days), 2) AS average_delivery_days
FROM `retail_analytics orders`;

-- Delivery performance based on delivery delay
SELECT
    CASE
        WHEN delivery_delay_days <= 0 THEN 'On Time'
        ELSE 'Late'
    END AS delivery_status,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        COUNT(DISTINCT order_id) * 100.0 /
        (SELECT COUNT(DISTINCT order_id)
         FROM `retail_analytics orders`),
        2
    ) AS percentage_of_orders
FROM `retail_analytics orders`
GROUP BY
    CASE
        WHEN delivery_delay_days <= 0 THEN 'On Time'
        ELSE 'Late'
    END
ORDER BY total_orders DESC;

-- Delivery performance by state
SELECT
    customer_state,
    CASE
        WHEN delivery_delay_days <= 0 THEN 'On Time'
        ELSE 'Late'
    END AS delivery_status,
    COUNT(DISTINCT order_id) AS total_orders
FROM `retail_analytics orders`
GROUP BY
    customer_state,
    CASE
        WHEN delivery_delay_days <= 0 THEN 'On Time'
        ELSE 'Late'
    END
ORDER BY customer_state, total_orders DESC;

-- Longest delivery times
SELECT
    order_id,
    customer_state,
    delivery_days,
    delivery_delay_days
FROM `retail_analytics orders`
ORDER BY delivery_days DESC
LIMIT 10;


-- ============================================================
-- 7. PAYMENT METHOD ANALYSIS
-- ============================================================

-- Revenue by payment method
SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_payment_value
FROM `retail_analytics ecommerce`
WHERE payment_type IS NOT NULL
GROUP BY payment_type
ORDER BY total_payment_value DESC;

-- Orders by payment method
SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS total_orders
FROM `retail_analytics ecommerce`
WHERE payment_type IS NOT NULL
GROUP BY payment_type
ORDER BY total_orders DESC;

-- Payment method share
SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        COUNT(DISTINCT order_id) * 100.0 /
        (SELECT COUNT(DISTINCT order_id)
         FROM `retail_analytics ecommerce`
         WHERE payment_type IS NOT NULL),
        2
    ) AS order_share_percentage
FROM `retail_analytics ecommerce`
WHERE payment_type IS NOT NULL
GROUP BY payment_type
ORDER BY total_orders DESC;


-- ============================================================
-- 8. MONTHLY SALES / ORDER TREND
-- ============================================================

SELECT
    DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS order_month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_sales
FROM `retail_analytics ecommerce`
GROUP BY DATE_FORMAT(order_purchase_timestamp, '%Y-%m')
ORDER BY order_month ASC;


-- ============================================================
-- 9. SUMMARY KPIs
-- ============================================================

SELECT
    ROUND(SUM(payment_value), 2) AS total_sales,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(payment_value) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM `retail_analytics ecommerce`;

SELECT
    ROUND(AVG(delivery_days), 2) AS average_delivery_days,
    COUNT(DISTINCT order_id) AS total_orders
FROM `retail_analytics orders`;


-- ============================================================
-- END OF ANALYSIS
-- ============================================================