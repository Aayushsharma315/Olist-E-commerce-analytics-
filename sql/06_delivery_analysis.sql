```sql
-- Olist E-Commerce Analytics Project
-- File: 06_delivery_analysis.sql

-- 1. Average Delivery Time in Days
SELECT
    ROUND(
        AVG(
            DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp
            )
        ), 2
    ) AS avg_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;


-- 2. Orders Delivered Late
SELECT
    COUNT(*) AS late_deliveries
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL
  AND order_delivered_customer_date >
      order_estimated_delivery_date;


-- 3. On-Time vs Late Deliveries
SELECT
    CASE
        WHEN order_delivered_customer_date <=
             order_estimated_delivery_date
        THEN 'On Time'
        ELSE 'Late'
    END AS delivery_status,
    COUNT(*) AS total_orders
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL
GROUP BY delivery_status;


-- 4. Average Estimated Delivery Time
SELECT
    ROUND(
        AVG(
            DATEDIFF(
                order_estimated_delivery_date,
                order_purchase_timestamp
            )
        ), 2
    ) AS avg_estimated_days
FROM orders
WHERE order_estimated_delivery_date IS NOT NULL;


-- 5. Delivery Delay by Customer State
SELECT
    c.customer_state,
    ROUND(
        AVG(
            DATEDIFF(
                o.order_delivered_customer_date,
                o.order_estimated_delivery_date
            )
        ), 2
    ) AS avg_delay_days
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY avg_delay_days DESC;


-- 6. Orders Still Not Delivered
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
WHERE order_status NOT IN ('delivered', 'canceled')
GROUP BY order_status
ORDER BY total_orders DESC;
```

