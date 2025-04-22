-- Tabela: Margem por Produto (Análise de rentabilidade)
CREATE TABLE product_margins AS
/* Propósito: Identificar produtos mais lucrativos */
SELECT
    Product_ID,
    Product_Category,
    Unit_Price - Unit_Cost AS unit_margin,
    (Unit_Price - Unit_Cost)/Unit_Cost AS margin_percent,
    NTILE(4) OVER (ORDER BY (Unit_Price - Unit_Cost) DESC) AS margin_quartile
FROM (
    SELECT DISTINCT Product_ID, Product_Category, Unit_Price, Unit_Cost
    FROM main_table
) base;
-- Classificação ajuda na tomada de decisão sobre mix de produtos