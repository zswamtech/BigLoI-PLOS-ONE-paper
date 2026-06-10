-- Calculate supplier-level Herfindahl-Hirschman Index for the closed
-- 2020-2025 pharmaceutical procurement cohort.
--
-- Scale:
--   hhi_0_1     = SUM(supplier_share^2)
--   hhi_0_10000 = SUM(supplier_share^2) * 10000
--
-- This query assumes the PostgreSQL table used by the BigLoI observatory:
-- observatorio_nacional.contratos_secop.

WITH pharm AS (
  SELECT
    COALESCE(NULLIF(TRIM(razon_social), ''), 'NO_ESPECIFICADO') AS supplier,
    valor_contrato::numeric AS value
  FROM observatorio_nacional.contratos_secop
  WHERE es_farmaceutico = true
    AND valor_contrato IS NOT NULL
    AND valor_contrato::numeric > 0
    AND fecha_firma >= DATE '2020-01-01'
    AND fecha_firma < DATE '2026-01-01'
),
totals AS (
  SELECT
    COUNT(*) AS total_contracts,
    COUNT(DISTINCT supplier) AS total_suppliers,
    SUM(value) AS total_value
  FROM pharm
),
supplier_shares AS (
  SELECT
    supplier,
    COUNT(*) AS supplier_contracts,
    SUM(value) AS supplier_value,
    SUM(value) / (SELECT total_value FROM totals) AS share
  FROM pharm
  GROUP BY supplier
)
SELECT
  (SELECT total_contracts FROM totals) AS total_contracts,
  (SELECT total_suppliers FROM totals) AS total_suppliers,
  (SELECT total_value FROM totals) AS total_value,
  SUM(POWER(share, 2)) AS hhi_0_1,
  SUM(POWER(share, 2)) * 10000 AS hhi_0_10000,
  MAX(share) AS top_supplier_share,
  SUM(CASE WHEN supplier_value IS NOT NULL THEN 1 ELSE 0 END) AS suppliers_with_value
FROM supplier_shares;

