-- Calculate supplier-level Herfindahl-Hirschman Index from the PLOS ONE
-- scientific data layer in Neon/Vercel.

WITH pharm AS (
  SELECT
    COALESCE(NULLIF(TRIM(provider_name), ''), 'NO_ESPECIFICADO') AS supplier,
    provider_document,
    contract_value_cop::numeric AS value
  FROM plos_one.closed_2020_2025_contracts
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
    max(provider_document) AS provider_document,
    COUNT(*) AS supplier_contracts,
    SUM(value) AS supplier_value,
    SUM(value) / (SELECT total_value FROM totals) AS share
  FROM pharm
  GROUP BY supplier
),
ranked AS (
  SELECT
    row_number() over (order by supplier_value desc, supplier) AS supplier_rank,
    supplier,
    provider_document,
    supplier_contracts,
    supplier_value,
    share,
    sum(share) over (order by supplier_value desc, supplier) AS cumulative_share
  FROM supplier_shares
),
top3 AS (
  SELECT greatest(1, ceil((SELECT total_suppliers FROM totals) * 0.03)::bigint) AS supplier_count
),
summary AS (
  SELECT
    (SELECT total_contracts FROM totals) AS total_contracts,
    (SELECT total_suppliers FROM totals) AS total_suppliers,
    (SELECT total_value FROM totals) AS total_value,
    SUM(POWER(share, 2)) AS hhi_0_1,
    SUM(POWER(share, 2)) * 10000 AS hhi_0_10000,
    MAX(share) AS top_supplier_share,
    SUM(share) FILTER (WHERE supplier_rank <= 10) AS top_10_share,
    (SELECT supplier_count FROM top3) AS top_3pct_supplier_count,
    SUM(share) FILTER (WHERE supplier_rank <= (SELECT supplier_count FROM top3)) AS top_3pct_share
  FROM ranked
)
SELECT *
FROM summary;

