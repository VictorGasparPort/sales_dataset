-- Particionamento: Segmentação por Região/Canal
CREATE TABLE main_table_partitioned PARTITION BY LIST (Region, Sales_Channel) (
    PARTITION north_online VALUES (('North', 'Online')),
    PARTITION south_retail VALUES (('South', 'Retail')),
    PARTITION others VALUES (DEFAULT)
);
/* Motivo: Acelera consultas regionais combinadas com tipo de canal */