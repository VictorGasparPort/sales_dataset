-- Query: Análise de Tendência com Janela Móvel
WITH SalesTrend AS (
    SELECT
        Sale_Date,
        Region,
        SUM(Sales_Amount) AS daily_sales,
        AVG(SUM(Sales_Amount)) OVER (
            PARTITION BY Region 
            ORDER BY Sale_Date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS weekly_avg
    FROM main_table
    GROUP BY 1,2
)
/* Propósito: Identificar padrões sazonais e anomalias */
SELECT 
    *,
    (daily_sales - weekly_avg) / weekly_avg * 100 AS deviation_percent,
    CASE 
        WHEN daily_sales > 1.5 * weekly_avg THEN 'Pico'
        WHEN daily_sales < 0.5 * weekly_avg THEN 'Vale'
        ELSE 'Normal'
    END AS sales_status
FROM SalesTrend;