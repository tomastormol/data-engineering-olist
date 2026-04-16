-- Staging model for payments
-- Filters out invalid payment types
SELECT
    order_id,
    payment_type,
    payment_installments    AS installments,
    payment_value           AS amount
FROM {{ source('public', 'payments') }}
WHERE payment_type != 'not_defined'