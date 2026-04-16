SELECT  
    COUNT(*)                        AS total_de_transacciones, 
    ROUND(AVG(amount)::numeric, 1)  AS media_del_importe, 
    ROUND(SUM(amount):: numeric, 2) AS total_del_importe,
    payment_type                    AS tipo_de_pago
FROM {{ ref('stg_payments') }}
GROUP BY payment_type
ORDER BY total_del_importe DESC