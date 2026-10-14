```sql
-- Olist E-Commerce Analytics Project
-- File: 07_payment_analysis.sql

-- 1. Payment Type Distribution
SELECT
    payment_type,
    COUNT(*) AS total_payments,
    ROUND(SUM(payment_value), 2) AS total_payment_value
FROM order_payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;


-- 2. Average Payment Value
SELECT
    ROUND(AVG(payment_value), 2) AS avg_payment_value
FROM order_payments;


-- 3. Installment Distribution
SELECT
    payment_installments,
    COUNT(*) AS total_transactions
FROM order_payments
GROUP BY payment_installments
ORDER BY payment_installments;


-- 4. Revenue by Payment Type
SELECT
    payment_type,
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM order_payments
GROUP BY payment_type
ORDER BY total_revenue DESC;


-- 5. Average Order Payment
SELECT
    ROUND(AVG(order_total), 2) AS avg_order_payment
FROM (
    SELECT
        order_id,
        SUM(payment_value) AS order_total
    FROM order_payments
    GROUP BY order_id
) AS order_payments_summary;


-- 6. Orders with Multiple Payment Records
SELECT
    order_id,
    COUNT(*) AS payment_records
FROM order_payments
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY payment_records DESC;


-- 7. Payment Value by Installment Count
SELECT
    payment_installments,
    ROUND(SUM(payment_value), 2) AS total_payment_value
FROM order_payments
GROUP BY payment_installments
ORDER BY total_payment_value DESC;
```

