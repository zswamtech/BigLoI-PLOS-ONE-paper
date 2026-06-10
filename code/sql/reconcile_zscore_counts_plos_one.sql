-- Reconcile Z-score analyzed-contract and alert counts from the PLOS ONE
-- scientific data layer in Neon/Vercel.

SELECT
  run_id,
  analyzed_contracts,
  alerts_abs_z_ge_1_5,
  alerts_abs_z_ge_2_0,
  alerts_abs_z_ge_3_0
FROM plos_one.zscore_threshold_summary
ORDER BY run_id;

SELECT
  run_id,
  year,
  analyzed_contracts,
  alerts_abs_z_ge_1_5,
  alert_rate_pct
FROM plos_one.zscore_yearly_summary
ORDER BY run_id, year;

