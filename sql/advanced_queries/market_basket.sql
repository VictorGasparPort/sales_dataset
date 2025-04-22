-- Query: Associação de Produtos (Market Basket)
SELECT 
    product_pair,
    support_count,
    confidence,
    lift_ratio
FROM (
    SELECT
        p1.Product_Category AS product1,
        p2.Product_Category AS product2,
        COUNT(*) AS support_count,
        COUNT(*) * 1.0 / total_transactions AS support,
        COUNT(*) * 1.0 / p1_count AS confidence,
        (COUNT(*) * 1.0 / total_transactions) / 
            ((p1_count * 1.0 / total_transactions) * (p2_count * 1.0 / total_transactions)) AS lift_ratio
    FROM main_table p1
    JOIN main_table p2 ON p1.Sale_Date = p2.Sale_Date 
        AND p1.Product_ID < p2.Product_ID
    CROSS JOIN (SELECT COUNT(DISTINCT Sale_Date) AS total_transactions FROM main_table) t
    GROUP BY 1,2,total_transactions,p1_count,p2_count
) combos
WHERE lift_ratio > 1 AND support_count > 10;