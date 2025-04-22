-- Índice: Vendas de Alto Valor
CREATE INDEX idx_high_value_sales ON main_table (Sales_Amount)
WHERE Sales_Amount > 5000;
/* Motivo: Isola 20% das transações que geram 80% da receita (Princípio de Pareto) */