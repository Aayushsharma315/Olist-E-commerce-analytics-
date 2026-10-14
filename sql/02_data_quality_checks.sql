```sql
-- Olist E-Commerce Analytics Project
-- File: 02_data_quality_checks.sql

-- 1. Check total customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- 2. Check duplicate customer IDs
SELECT customer_id, COUNT(*) AS total
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- 3. Check missing customer IDs
SELECT COUNT(*) AS missing_customer_ids
FROM customers
WHERE customer_id IS NULL;

-- 4. Check total orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- 5. Check duplicate order IDs
SELECT order_id, COUNT(*) AS total
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 6. Check missing order dates
SELECT COUNT(*) AS missing_order_dates
FROM orders
WHERE order_purchase_timestamp IS NULL;

-- 7. Check order status distribution
SELECT order_status, COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- 8. Check negative payment values
SELECT *
FROM order_payments
WHERE payment_value < 0;

-- 9. Check negative product prices
SELECT *
FROM order_items
WHERE price < 0;

-- 10. Check missing product IDs
SELECT COUNT(*) AS missing_product_ids
FROM order_items
WHERE product_id IS NULL;
```

