-- Reconcile Z-score analyzed-contract and alert counts for the closed
-- 2020-2025 pharmaceutical procurement cohort.
--
-- This query assumes the table used by the BigLoI observatory:
-- observatorio_nacional.zscore_alertas_secop
--
-- Expected manuscript values currently under reconciliation:
--   analyzed contracts: 147,670
--   abs(zscore) >= 1.5 alerts: 690
--
-- Current Fig3 yearly source-data sum:
--   analyzed contracts: 147,020
--   abs(zscore) >= 1.5 alerts: 683

WITH closed_cohort AS (
  SELECT *
  FROM observatorio_nacional.zscore_alertas_secop
  WHERE fecha_firma >= DATE '2020-01-01'
    AND fecha_firma < DATE '2026-01-01'
)
SELECT
  COUNT(*) AS analyzed_contracts,
  COUNT(*) FILTER (WHERE ABS(zscore) >= 1.5) AS alerts_abs_z_ge_1_5,
  COUNT(*) FILTER (WHERE ABS(zscore) >= 2.0) AS alerts_abs_z_ge_2_0,
  COUNT(*) FILTER (WHERE ABS(zscore) >= 3.0) AS alerts_abs_z_ge_3_0
FROM closed_cohort;

-- Annual reconciliation for Fig3 source data.

WITH closed_cohort AS (
  SELECT *
  FROM observatorio_nacional.zscore_alertas_secop
  WHERE fecha_firma >= DATE '2020-01-01'
    AND fecha_firma < DATE '2026-01-01'
)
SELECT
  EXTRACT(YEAR FROM fecha_firma)::int AS year,
  COUNT(*) AS analyzed_contracts,
  COUNT(*) FILTER (WHERE ABS(zscore) >= 1.5) AS alerts_abs_z_ge_1_5,
  ROUND(
    100.0 * COUNT(*) FILTER (WHERE ABS(zscore) >= 1.5) / NULLIF(COUNT(*), 0),
    4
  ) AS alert_rate_pct
FROM closed_cohort
GROUP BY EXTRACT(YEAR FROM fecha_firma)
ORDER BY year;

