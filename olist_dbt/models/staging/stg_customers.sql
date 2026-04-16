-- Staging model for customers
-- Renames columns for clarity
SELECT
    customer_id,
    customer_unique_id,
    customer_city       AS city,
    customer_state      AS state,
    customer_zip_code_prefix AS zip_code
FROM {{ source('public', 'customers') }}