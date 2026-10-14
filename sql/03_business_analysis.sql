```sql
-- Olist E-Commerce Analytics Project
-- File: 03_business_analysis.sql

-- 1. Total Orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;


-- 2. Total Revenue
SELECT
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM order_payments;


-- 3. Monthly Revenue
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
        AS order_month,
    ROUND(SUM(p.payment_value), 2) AS monthly_revenue
FROM orders o
JOIN order_payments p
    ON o.order_id = p.order_id
GROUP BY DATE_FORMAT(
    o.order_purchase_timestamp, '%Y-%m'
)
ORDER BY order_month;


-- 4. Order Status Analysis
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;


-- 5. Top 10 States by Customer Count
SELECT
    customer_state,
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM customers
GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;


-- 6. Average Order Value
SELECT
    ROUND(AVG(order_payment), 2) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(payment_value) AS order_payment
    FROM order_payments
    GROUP BY order_id
) AS order_totals;


-- 7. Top 10 Products by Revenue
SELECT
    oi.product_id,
    ROUND(SUM(oi.price), 2) AS product_revenue
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY oi.product_id
ORDER BY product_revenue DESC
LIMIT 10;
```

