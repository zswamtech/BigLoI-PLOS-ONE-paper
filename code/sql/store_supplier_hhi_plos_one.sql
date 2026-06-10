-- Store supplier-level Herfindahl-Hirschman Index results for the PLOS ONE
-- reconstructed SECOP API cohort in Neon/Vercel.

\set run_id 'plos_one_hhi_reconstructed_api_2026_06_05'

begin;

delete from plos_one.supplier_concentration_details
where run_id = :'run_id';

delete from plos_one.supplier_concentration_runs
where run_id = :'run_id';

with pharm as (
  select
    coalesce(nullif(trim(provider_name), ''), 'NO_ESPECIFICADO') as supplier,
    provider_document,
    contract_value_cop::numeric as value
  from plos_one.closed_2020_2025_contracts
),
totals as (
  select
    count(*) as total_contracts,
    count(distinct supplier) as total_suppliers,
    sum(value) as total_value
  from pharm
),
supplier_shares as (
  select
    supplier,
    max(provider_document) as provider_document,
    count(*) as supplier_contracts,
    sum(value) as supplier_value,
    sum(value) / (select total_value from totals) as share
  from pharm
  group by supplier
),
ranked as (
  select
    row_number() over (order by supplier_value desc, supplier) as supplier_rank,
    supplier,
    provider_document,
    supplier_contracts,
    supplier_value,
    share,
    sum(share) over (order by supplier_value desc, supplier) as cumulative_share
  from supplier_shares
),
top3 as (
  select greatest(1, ceil((select total_suppliers from totals) * 0.03)::bigint) as supplier_count
),
summary as (
  select
    (select total_contracts from totals) as total_contracts,
    (select total_suppliers from totals) as total_suppliers,
    (select total_value from totals) as total_value,
    sum(power(share, 2)) as hhi_0_1,
    sum(power(share, 2)) * 10000 as hhi_0_10000,
    max(share) as top_supplier_share,
    sum(share) filter (where supplier_rank <= 10) as top_10_share,
    (select supplier_count from top3) as top_3pct_supplier_count,
    sum(share) filter (where supplier_rank <= (select supplier_count from top3)) as top_3pct_share
  from ranked
)
insert into plos_one.supplier_concentration_runs (
  run_id,
  total_contracts,
  total_suppliers,
  total_value_cop,
  hhi_0_1,
  hhi_0_10000,
  top_supplier_share,
  top_10_share,
  top_3pct_supplier_count,
  top_3pct_share,
  status,
  notes,
  metadata
)
select
  :'run_id',
  total_contracts,
  total_suppliers,
  total_value,
  hhi_0_1,
  hhi_0_10000,
  top_supplier_share,
  top_10_share,
  top_3pct_supplier_count,
  top_3pct_share,
  'audit_reconstruction',
  'Calculated from the reconstructed SECOP API cohort in plos_one.closed_2020_2025_contracts. This run is an audit rebuild and does not yet replace the manuscript cohort count of 162,271.',
  jsonb_build_object(
    'source', 'datos.gov.co SECOP API rpmr-utcd',
    'cohort_label', 'reconstructed_api_cohort_2020_2025',
    'computed_at', '2026-06-05'
  )
from summary;

with pharm as (
  select
    coalesce(nullif(trim(provider_name), ''), 'NO_ESPECIFICADO') as supplier,
    provider_document,
    contract_value_cop::numeric as value
  from plos_one.closed_2020_2025_contracts
),
totals as (
  select sum(value) as total_value
  from pharm
),
supplier_shares as (
  select
    supplier,
    max(provider_document) as provider_document,
    count(*) as supplier_contracts,
    sum(value) as supplier_value,
    sum(value) / (select total_value from totals) as share
  from pharm
  group by supplier
),
ranked as (
  select
    row_number() over (order by supplier_value desc, supplier) as supplier_rank,
    supplier,
    provider_document,
    supplier_contracts,
    supplier_value,
    share,
    sum(share) over (order by supplier_value desc, supplier) as cumulative_share
  from supplier_shares
)
insert into plos_one.supplier_concentration_details (
  run_id,
  supplier_rank,
  provider_name,
  provider_document,
  supplier_contracts,
  supplier_value_cop,
  supplier_share,
  cumulative_share
)
select
  :'run_id',
  supplier_rank,
  supplier,
  provider_document,
  supplier_contracts,
  supplier_value,
  share,
  cumulative_share
from ranked;

commit;
