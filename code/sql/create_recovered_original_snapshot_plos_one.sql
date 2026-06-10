-- Recovered original BigLoI/PLOS ONE analytical snapshot.
--
-- Purpose:
--   Preserve the local PostgreSQL source that reproduces the manuscript
--   Fig. 1/Table 1 closed cohort exactly when year is defined by `vigencia`.
--
-- Source:
--   local observatorio_nacional.contratos_secop
--   local observatorio_nacional.zscore_alertas_secop

create schema if not exists plos_one;

create table if not exists plos_one.contratos_secop_original_snapshot (
  id integer,
  numero_contrato text,
  descripcion_objeto text,
  valor_contrato bigint,
  fecha_firma date,
  razon_social text,
  departamento text,
  municipio text,
  duracion_meses integer,
  vigencia integer,
  es_farmaceutico boolean,
  categoria text,
  created_at timestamp,
  updated_at timestamp,
  fecha_ingesta timestamp,
  recovered_at timestamptz not null default now(),
  source_label text not null default 'local_postgres_observatorio_nacional_recovered_2026_06_05'
);

create index if not exists plos_one_original_snapshot_vigencia_idx
  on plos_one.contratos_secop_original_snapshot(vigencia);

create index if not exists plos_one_original_snapshot_farma_idx
  on plos_one.contratos_secop_original_snapshot(es_farmaceutico);

create index if not exists plos_one_original_snapshot_supplier_idx
  on plos_one.contratos_secop_original_snapshot(razon_social);

create index if not exists plos_one_original_snapshot_contract_idx
  on plos_one.contratos_secop_original_snapshot(numero_contrato);

create table if not exists plos_one.zscore_alertas_secop_original_snapshot (
  id integer,
  numero_contrato text,
  valor_contrato bigint,
  fecha date,
  anno integer,
  departamento text,
  razon_social text,
  atc text,
  descripcion_atc text,
  sismed_precio_ref numeric,
  sismed_stddev numeric,
  precio_unitario_contrato numeric,
  zscore numeric,
  ratio_vs_sismed numeric,
  sismed_n_muestras bigint,
  nivel_alerta text,
  tipo_anomalia text,
  recovered_at timestamptz not null default now(),
  source_label text not null default 'local_postgres_observatorio_nacional_recovered_2026_06_05'
);

create index if not exists plos_one_zscore_original_anno_idx
  on plos_one.zscore_alertas_secop_original_snapshot(anno);

create index if not exists plos_one_zscore_original_zscore_idx
  on plos_one.zscore_alertas_secop_original_snapshot(abs(zscore) desc);

create index if not exists plos_one_zscore_original_contract_idx
  on plos_one.zscore_alertas_secop_original_snapshot(numero_contrato);

create or replace view plos_one.original_closed_2020_2025_contracts as
select *
from plos_one.contratos_secop_original_snapshot
where es_farmaceutico = true
  and vigencia between 2020 and 2025;

create or replace view plos_one.original_closed_2020_2025_positive_value_contracts as
select *
from plos_one.original_closed_2020_2025_contracts
where valor_contrato is not null
  and valor_contrato > 0;

create or replace view plos_one.original_zscore_yearly_summary as
select
  anno as year,
  count(*) as alert_rows,
  count(*) filter (where abs(zscore) >= 1.5) as alerts_abs_z_ge_1_5,
  count(*) filter (where abs(zscore) >= 2.0) as alerts_abs_z_ge_2_0,
  count(*) filter (where abs(zscore) >= 3.0) as alerts_abs_z_ge_3_0
from plos_one.zscore_alertas_secop_original_snapshot
where anno between 2020 and 2025
group by anno;
