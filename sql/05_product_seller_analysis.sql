```sql
-- Olist E-Commerce Analytics Project
-- File: 05_product_seller_analysis.sql

-- 1. Top 10 Products by Sales Revenue
SELECT
    product_id,
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 10;


-- 2. Top 10 Sellers by Revenue
SELECT
    seller_id,
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items
GROUP BY seller_id
ORDER BY total_revenue DESC
LIMIT 10;


-- 3. Top 10 Sellers by Number of Items Sold
SELECT
    seller_id,
    COUNT(*) AS items_sold
FROM order_items
GROUP BY seller_id
ORDER BY items_sold DESC
LIMIT 10;


-- 4. Average Product Price
SELECT
    ROUND(AVG(price), 2) AS average_product_price
FROM order_items;


-- 5. Product Category Performance
SELECT
    p.product_category_name,
    COUNT(oi.order_id) AS total_items_sold,
    ROUND(SUM(oi.price), 2) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;


-- 6. Seller Count by State
SELECT
    seller_state,
    COUNT(DISTINCT seller_id) AS total_sellers
FROM sellers
GROUP BY seller_state
ORDER BY total_sellers DESC;


-- 7. Average Revenue per Seller
SELECT
    ROUND(AVG(seller_revenue), 2) AS avg_revenue_per_seller
FROM (
    SELECT
        seller_id,
        SUM(price) AS seller_revenue
    FROM order_items
    GROUP BY seller_id
) AS seller_sales;
```

