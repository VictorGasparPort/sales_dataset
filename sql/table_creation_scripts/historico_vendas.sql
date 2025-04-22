-- Tabela: Histórico Diário de Vendas (Agregação para relatórios rápidos)
CREATE TABLE daily_sales_summary AS
/* Propósito: Otimizar consultas recorrentes de análise diária */
SELECT
    Sale_Date,
    Product_Category,
    Region,
    SUM(Sales_Amount) AS total_sales,
    AVG(Unit_Price - Unit_Cost) AS avg_margin,
    COUNT(DISTINCT Product_ID) AS unique_products
FROM main_table
GROUP BY 1,2,3;
-- Permite análise rápida de desempenho sem reprocessar dados brutos
