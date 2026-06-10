-- PLOS ONE scientific data layer for BigLoI.
-- Target: Neon/Postgres provisioned from Vercel Marketplace.
--
-- Purpose:
--   Keep the PLOS ONE analytical cohort separate from the public
--   operational observatory tables.

create schema if not exists plos_one;

create table if not exists plos_one.source_manifests (
  id bigserial primary key,
  source_key text not null unique,
  source_system text not null,
  source_uri text,
  source_period text,
  capture_started_at timestamptz,
  capture_finished_at timestamptz,
  content_hash text,
  row_count bigint,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists plos_one.contratos_secop (
  id bigserial primary key,
  source_key text references plos_one.source_manifests(source_key),
  source_record_id text,
  contract_uid text not null,
  contract_number text,
  entity_name text,
  entity_document text,
  department text,
  municipality text,
  regional_code text,
  provider_name text,
  provider_document text,
  contract_object text,
  contract_value_cop numeric(20, 2),
  signing_date date,
  publication_date date,
  therapeutic_category text,
  is_pharmaceutical boolean not null default true,
  inclusion_terms text[] not null default '{}',
  exclusion_terms text[] not null default '{}',
  raw_payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(contract_uid)
);

create index if not exists plos_one_contratos_secop_signing_date_idx
  on plos_one.contratos_secop(signing_date);

create index if not exists plos_one_contratos_secop_provider_idx
  on plos_one.contratos_secop(provider_name);

create index if not exists plos_one_contratos_secop_value_idx
  on plos_one.contratos_secop(contract_value_cop desc);

create index if not exists plos_one_contratos_secop_category_idx
  on plos_one.contratos_secop(therapeutic_category);

create table if not exists plos_one.zscore_alertas_secop (
  id bigserial primary key,
  contract_uid text not null references plos_one.contratos_secop(contract_uid) on delete cascade,
  signing_date date,
  therapeutic_category text,
  contract_value_cop numeric(20, 2),
  category_mean_cop numeric(20, 2),
  category_stddev_cop numeric(20, 2),
  zscore double precision,
  abs_zscore double precision generated always as (abs(zscore)) stored,
  alert_level text generated always as (
    case
      when abs(zscore) >= 3.0 then 'critical'
      when abs(zscore) >= 2.0 then 'high'
      when abs(zscore) >= 1.5 then 'moderate'
      else 'normal'
    end
  ) stored,
  run_id text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(contract_uid, run_id)
);

create index if not exists plos_one_zscore_alertas_run_idx
  on plos_one.zscore_alertas_secop(run_id);

create index if not exists plos_one_zscore_alertas_abs_idx
  on plos_one.zscore_alertas_secop(abs_zscore desc);

create index if not exists plos_one_zscore_alertas_year_idx
  on plos_one.zscore_alertas_secop(signing_date);

create table if not exists plos_one.reconciliation_runs (
  id bigserial primary key,
  run_id text not null unique,
  run_type text not null,
  cohort_start_date date not null default date '2020-01-01',
  cohort_end_date date not null default date '2026-01-01',
  manuscript_analyzed_contracts bigint,
  manuscript_alerts_abs_z_ge_1_5 bigint,
  computed_analyzed_contracts bigint,
  computed_alerts_abs_z_ge_1_5 bigint,
  computed_alerts_abs_z_ge_2_0 bigint,
  computed_alerts_abs_z_ge_3_0 bigint,
  status text not null default 'draft',
  notes text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists plos_one.supplier_concentration_runs (
  id bigserial primary key,
  run_id text not null unique,
  cohort_start_date date not null default date '2020-01-01',
  cohort_end_date date not null default date '2026-01-01',
  total_contracts bigint,
  total_suppliers bigint,
  total_value_cop numeric(24, 2),
  hhi_0_1 numeric(18, 10),
  hhi_0_10000 numeric(18, 4),
  top_supplier_share numeric(18, 10),
  top_10_share numeric(18, 10),
  top_3pct_supplier_count bigint,
  top_3pct_share numeric(18, 10),
  status text not null default 'draft',
  notes text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists plos_one.supplier_concentration_details (
  id bigserial primary key,
  run_id text not null references plos_one.supplier_concentration_runs(run_id) on delete cascade,
  supplier_rank bigint not null,
  provider_name text not null,
  provider_document text,
  supplier_contracts bigint,
  supplier_value_cop numeric(24, 2),
  supplier_share numeric(18, 10),
  cumulative_share numeric(18, 10),
  created_at timestamptz not null default now(),
  unique(run_id, supplier_rank)
);

create index if not exists plos_one_supplier_concentration_details_run_idx
  on plos_one.supplier_concentration_details(run_id);

create index if not exists plos_one_supplier_concentration_details_share_idx
  on plos_one.supplier_concentration_details(run_id, supplier_share desc);

create or replace view plos_one.closed_2020_2025_contracts as
select *
from plos_one.contratos_secop
where is_pharmaceutical = true
  and contract_value_cop is not null
  and contract_value_cop > 0
  and signing_date >= date '2020-01-01'
  and signing_date < date '2026-01-01';

create or replace view plos_one.zscore_threshold_summary as
select
  run_id,
  count(*) as analyzed_contracts,
  count(*) filter (where abs_zscore >= 1.5) as alerts_abs_z_ge_1_5,
  count(*) filter (where abs_zscore >= 2.0) as alerts_abs_z_ge_2_0,
  count(*) filter (where abs_zscore >= 3.0) as alerts_abs_z_ge_3_0
from plos_one.zscore_alertas_secop
where signing_date >= date '2020-01-01'
  and signing_date < date '2026-01-01'
group by run_id;

create or replace view plos_one.zscore_yearly_summary as
select
  run_id,
  extract(year from signing_date)::int as year,
  count(*) as analyzed_contracts,
  count(*) filter (where abs_zscore >= 1.5) as alerts_abs_z_ge_1_5,
  round(100.0 * count(*) filter (where abs_zscore >= 1.5) / nullif(count(*), 0), 4) as alert_rate_pct
from plos_one.zscore_alertas_secop
where signing_date >= date '2020-01-01'
  and signing_date < date '2026-01-01'
group by run_id, extract(year from signing_date);

