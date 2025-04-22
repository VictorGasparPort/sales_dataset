-- Query: Vendas por Região/Categoria
SELECT
    Region,
    Product_Category,
    SUM(Sales_Amount) AS total_sales,
    RANK() OVER (PARTITION BY Region ORDER BY SUM(Sales_Amount) DESC) AS rank
FROM main_table
GROUP BY 1,2
ORDER BY 1,3 DESC;
