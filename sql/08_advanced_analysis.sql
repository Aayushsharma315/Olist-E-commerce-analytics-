```sql
-- Olist E-Commerce Analytics Project
-- File: 08_advanced_analysis.sql

-- 1. Top 10 Customers by Total Spending
SELECT
    o.customer_id,
    ROUND(SUM(p.payment_value), 2) AS total_spending
FROM orders o
JOIN order_payments p
    ON o.order_id = p.order_id
GROUP BY o.customer_id
ORDER BY total_spending DESC
LIMIT 10;


-- 2. Rank Products by Revenue
SELECT
    product_id,
    total_revenue,
    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank
FROM (
    SELECT
        product_id,
        SUM(price) AS total_revenue
    FROM order_items
    GROUP BY product_id
) AS product_sales;


-- 3. Monthly Revenue Growth
WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(
            o.order_purchase_timestamp, '%Y-%m'
        ) AS sales_month,
        SUM(p.payment_value) AS revenue
    FROM orders o
    JOIN order_payments p
        ON o.order_id = p.order_id
    GROUP BY DATE_FORMAT(
        o.order_purchase_timestamp, '%Y-%m'
    )
),
previous_month AS (
    SELECT
        sales_month,
        revenue,
        LAG(revenue) OVER (
            ORDER BY sales_month
        ) AS previous_revenue
    FROM monthly_sales
)
SELECT
    sales_month,
    ROUND(revenue, 2) AS revenue,
    ROUND(previous_revenue, 2) AS previous_revenue,
    ROUND(
        (revenue - previous_revenue)
        / NULLIF(previous_revenue, 0) * 100,
        2
    ) AS growth_percentage
FROM previous_month
ORDER BY sales_month;


-- 4. Repeat Customer Rate
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
)
SELECT
    COUNT(*) AS total_buying_customers,
    SUM(
        CASE WHEN order_count > 1 THEN 1 ELSE 0 END
    ) AS repeat_customers,
    ROUND(
        100.0 * SUM(
            CASE WHEN order_count > 1 THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS repeat_customer_percentage
FROM customer_orders;


-- 5. Category Revenue Ranking
WITH category_sales AS (
    SELECT
        p.product_category_name,
        SUM(oi.price) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_category_name
)
SELECT
    product_category_name,
    ROUND(revenue, 2) AS revenue,
    DENSE_RANK() OVER (
        ORDER BY revenue DESC
    ) AS category_rank
FROM category_sales
ORDER BY category_rank;


-- 6. Average Order Value by Month
SELECT
    DATE_FORMAT(
        o.order_purchase_timestamp, '%Y-%m'
    ) AS sales_month,
    ROUND(
        SUM(p.payment_value)
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN order_payments p
    ON o.order_id = p.order_id
GROUP BY DATE_FORMAT(
    o.order_purchase_timestamp, '%Y-%m'
)
ORDER BY sales_month;
```

