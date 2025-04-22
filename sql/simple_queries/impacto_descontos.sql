-- Query: Impacto de Descontos
SELECT
    Discount::INT AS discount_bucket,
    AVG(Quantity_Sold) AS avg_quantity,
    CORR(Discount, Quantity_Sold) AS quantity_corr,
    SUM(Sales_Amount) / SUM(Quantity_Sold) AS avg_revenue_per_unit
FROM main_table
GROUP BY 1
ORDER BY 1;
