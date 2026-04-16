-- Staging model for orders
-- Selects only delivered orders and renames columns for clarity
SELECT
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp    AS purchased_at,
    order_approved_at           AS approved_at,
    order_delivered_customer_date AS delivered_at,
    order_estimated_delivery_date AS estimated_delivery_at,
    delivery_days
FROM {{ source('public', 'orders') }}
WHERE order_status = 'delivered'