-- Índice: Filtragem Temporal
CREATE INDEX idx_sales_date ON main_table USING BRIN(Sale_Date)
/* Motivo: Consultas por intervalo de datas são frequentes e BRIN é eficiente para dados temporais ordenados */
