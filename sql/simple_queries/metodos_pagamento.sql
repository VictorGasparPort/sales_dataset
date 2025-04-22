-- Query: Eficácia de Métodos de Pagamento
SELECT
    Payment_Method,
    AVG(Sales_Amount) AS avg_transaction,
    SUM(Sales_Amount) * 0.02 AS processing_cost_estimate,
    COUNT(*) FILTER (WHERE Discount > 0) AS discounted_transactions
FROM main_table
GROUP BY 1
ORDER BY 2 DESC;
