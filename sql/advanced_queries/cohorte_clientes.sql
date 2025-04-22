-- Query: Análise de Cohorte de Clientes
SELECT
    cohort_month,
    customer_type,
    months_since_first_purchase,
    retention_rate,
    CLTV
FROM (
    SELECT
        TO_CHAR(first_purchase, 'YYYY-MM') AS cohort_month,
        Customer_Type,
        EXTRACT(MONTH FROM AGE(Sale_Date, first_purchase)) AS months_since_first_purchase,
        COUNT(DISTINCT m.Product_ID) * 1.0 / COUNT(DISTINCT cohort_users) AS retention_rate,
        SUM(Sales_Amount) / COUNT(DISTINCT m.Product_ID) AS CLTV
    FROM main_table m
    JOIN (
        SELECT 
            Product_ID, 
            MIN(Sale_Date) AS first_purchase,
            ARRAY_AGG(DISTINCT Product_ID) AS cohort_users
        FROM main_table
        GROUP BY Product_ID
    ) cohort ON m.Product_ID = ANY(cohort.cohort_users)
    GROUP BY 1,2,3
) analysis
WHERE months_since_first_purchase <= 12;