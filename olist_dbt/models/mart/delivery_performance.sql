-- Delivery performance by state
SELECT
    c.state,
    COUNT(*)                                    AS total_orders,
    ROUND(AVG(o.delivery_days)::numeric, 1)     AS avg_delivery_days,
    MAX(o.delivery_days)                        AS max_delivery_days,
    MIN(o.delivery_days)                        AS min_delivery_days
FROM {{ ref('stg_orders') }} o
LEFT JOIN {{ ref('stg_customers') }} c ON o.customer_id = c.customer_id
GROUP BY c.state
ORDER BY total_orders DESC