-- Tabela: Performance de Representantes (Suporte a comissões)
CREATE TABLE sales_rep_performance (
    rep_name VARCHAR(50),
    month VARCHAR(7),
    total_sales NUMERIC,
    avg_discount NUMERIC,
    new_clients INT
);
/* Propósito: Calcular métricas-chave para bonificações */
INSERT INTO sales_rep_performance
SELECT
    Sales_Rep,
    TO_CHAR(Sale_Date, 'YYYY-MM'),
    SUM(Sales_Amount),
    AVG(Discount),
    COUNT(DISTINCT CASE WHEN Customer_Type = 'New' THEN Product_ID END)
FROM main_table
GROUP BY 1,2;
-- Combina múltiplas métricas em uma única fonte para RH