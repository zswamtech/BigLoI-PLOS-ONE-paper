-- Store supplier HHI for the recovered original PLOS ONE manuscript snapshot.

\set run_id 'plos_one_hhi_original_snapshot_2026_06_05'

begin;

delete from plos_one.supplier_concentration_details
where run_id = :'run_id';

delete from plos_one.supplier_concentration_runs
where run_id = :'run_id';

with pharm as (
  select
    coalesce(nullif(trim(razon_social), ''), 'NO_ESPECIFICADO') as supplier,
    valor_contrato::numeric as value
  from plos_one.original_closed_2020_2025_positive_value_contracts
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
  'recovered_original_snapshot',
  'Calculated from plos_one.original_closed_2020_2025_positive_value_contracts, recovered from local observatorio_nacional.contratos_secop. Year is defined by vigencia to match manuscript Fig. 1/Table 1.',
  jsonb_build_object(
    'source', 'local PostgreSQL observatorio_nacional.contratos_secop',
    'cohort_label', 'original_manuscript_snapshot_2020_2025',
    'year_field', 'vigencia',
    'computed_at', '2026-06-05'
  )
from summary;

with pharm as (
  select
    coalesce(nullif(trim(razon_social), ''), 'NO_ESPECIFICADO') as supplier,
    valor_contrato::numeric as value
  from plos_one.original_closed_2020_2025_positive_value_contracts
),
totals as (
  select sum(value) as total_value
  from pharm
),
supplier_shares as (
  select
    supplier,
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
  null,
  supplier_contracts,
  supplier_value,
  share,
  cumulative_share
from ranked;

commit;
