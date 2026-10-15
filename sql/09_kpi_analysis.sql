```sql
-- Olist E-Commerce Analytics Project
-- File: 09_kpi_analysis.sql

-- 1. Total Orders
SELECT
    COUNT(*) AS total_orders
FROM orders;


-- 2. Total Unique Customers
SELECT
    COUNT(DISTINCT customer_unique_id)
        AS total_customers
FROM customers;


-- 3. Total Payment Value
SELECT
    ROUND(SUM(payment_value), 2)
        AS total_payment_value
FROM order_payments;


-- 4. Average Order Value
SELECT
    ROUND(
        SUM(order_payment) / COUNT(*), 2
    ) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(payment_value) AS order_payment
    FROM order_payments
    GROUP BY order_id
) AS order_totals;


-- 5. Delivered Orders
SELECT
    COUNT(*) AS delivered_orders
FROM orders
WHERE order_status = 'delivered';


-- 6. Order Delivery Rate
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN order_status = 'delivered'
                THEN 1 ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS delivery_rate_percentage
FROM orders;


-- 7. Average Review Score
SELECT
    ROUND(AVG(review_score), 2)
        AS average_review_score
FROM order_reviews;


-- 8. Total Sellers
SELECT
    COUNT(DISTINCT seller_id) AS total_sellers
FROM sellers;
```

