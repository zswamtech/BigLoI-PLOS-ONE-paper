#!/usr/bin/env python3
"""Regenerate the frozen paper-specific source-data files.

This script writes the minimal figure/table CSV files included in the
article-specific reproducibility package. It intentionally targets the frozen
submission package rather than querying live APIs.

Invocation:
    python docs/publicacion_cientifica/paper_repository_plosone/code/scripts/generate_paper_source_data.py
"""

from __future__ import annotations

import csv
from pathlib import Path


PAPER_REPO = Path(__file__).resolve().parents[2]
DERIVED_DIR = PAPER_REPO / "data" / "derived"
FIGURES_DIR = DERIVED_DIR / "figures"
TABLES_DIR = DERIVED_DIR / "tables"
METADATA_DIR = DERIVED_DIR / "metadata"


FIG1_ROWS = [
    {"year": 2020, "contracts_indexed_bd": 35242, "value_thousand_million_cop": 3294.5, "value_billones_cop": 3.2945, "coverage_note": "Full year; contract-level veterinary exclusions applied"},
    {"year": 2021, "contracts_indexed_bd": 53723, "value_thousand_million_cop": 2846.1, "value_billones_cop": 2.8461, "coverage_note": "Full year; contract-level veterinary exclusions applied"},
    {"year": 2022, "contracts_indexed_bd": 30927, "value_thousand_million_cop": 2639.6, "value_billones_cop": 2.6396, "coverage_note": "Full year; contract-level veterinary exclusions applied"},
    {"year": 2023, "contracts_indexed_bd": 10648, "value_thousand_million_cop": 1527.9, "value_billones_cop": 1.5279, "coverage_note": "Full year; contract-level veterinary exclusions applied"},
    {"year": 2024, "contracts_indexed_bd": 9335, "value_thousand_million_cop": 1124.0, "value_billones_cop": 1.1240, "coverage_note": "Full year; contract-level veterinary exclusions applied"},
    {"year": 2025, "contracts_indexed_bd": 21955, "value_thousand_million_cop": 5496.8, "value_billones_cop": 5.4968, "coverage_note": "Full year; contract-level veterinary exclusions applied"},
]

FIG2_ROWS = [
    {"region": "Bogota D.C. combined", "contracts": 18020, "value_thousand_million_cop": 9607.0, "pct_total_national_value": 56.7},
    {"region": "Antioquia", "contracts": 47964, "value_thousand_million_cop": 1312.2, "pct_total_national_value": 7.8},
    {"region": "Valle del Cauca", "contracts": 5843, "value_thousand_million_cop": 696.5, "pct_total_national_value": 4.1},
    {"region": "Boyaca", "contracts": 9142, "value_thousand_million_cop": 623.6, "pct_total_national_value": 3.7},
    {"region": "Tolima", "contracts": 3773, "value_thousand_million_cop": 426.9, "pct_total_national_value": 2.5},
    {"region": "Santander", "contracts": 4278, "value_thousand_million_cop": 403.8, "pct_total_national_value": 2.4},
    {"region": "Huila", "contracts": 4177, "value_thousand_million_cop": 403.2, "pct_total_national_value": 2.4},
    {"region": "Cauca", "contracts": 2015, "value_thousand_million_cop": 389.6, "pct_total_national_value": 2.3},
    {"region": "Atlantico", "contracts": 5075, "value_thousand_million_cop": 348.8, "pct_total_national_value": 2.1},
]

FIG3_CATEGORY_ROWS = [
    {"category_label": "Analgesico", "contracts_analyzed": 42, "pct_with_alert": 9.52, "z_max": 4.22, "ratio_max_to_category_mean": 9.28},
    {"category_label": "Diabetes", "contracts_analyzed": 279, "pct_with_alert": 7.89, "z_max": 6.61, "ratio_max_to_category_mean": 15.52},
    {"category_label": "Antiviral", "contracts_analyzed": 37, "pct_with_alert": 5.41, "z_max": 4.83, "ratio_max_to_category_mean": 14.19},
    {"category_label": "Antibiotico", "contracts_analyzed": 217, "pct_with_alert": 3.23, "z_max": 8.89, "ratio_max_to_category_mean": 26.41},
    {"category_label": "Insumo medico", "contracts_analyzed": 2232, "pct_with_alert": 2.46, "z_max": 22.34, "ratio_max_to_category_mean": 88.69},
    {"category_label": "Oncologico", "contracts_analyzed": 400, "pct_with_alert": 0.75, "z_max": 19.27, "ratio_max_to_category_mean": 138.47},
]

FIG3_YEARLY_ROWS = [
    {"year": 2020, "contracts_analyzed": 35238, "contracts_with_alert": 120, "alert_rate_pct": 0.3405},
    {"year": 2021, "contracts_analyzed": 53718, "contracts_with_alert": 163, "alert_rate_pct": 0.3034},
    {"year": 2022, "contracts_analyzed": 30926, "contracts_with_alert": 126, "alert_rate_pct": 0.4074},
    {"year": 2023, "contracts_analyzed": 10648, "contracts_with_alert": 84, "alert_rate_pct": 0.7889},
    {"year": 2024, "contracts_analyzed": 9335, "contracts_with_alert": 83, "alert_rate_pct": 0.8891},
    {"year": 2025, "contracts_analyzed": 6729, "contracts_with_alert": 88, "alert_rate_pct": 1.3078},
]

FIG4_TOP10_ROWS = [
    {"rank": 1, "provider_label": "VECOL SA*", "pct_share_total_value": 5.6517, "cumulative_pct_share": 5.6517},
    {"rank": 2, "provider_label": "HOSMIL", "pct_share_total_value": 5.4679, "cumulative_pct_share": 11.1196},
    {"rank": 3, "provider_label": "ETICOS U.T. 2020", "pct_share_total_value": 3.5282, "cumulative_pct_share": 14.6478},
    {"rank": 4, "provider_label": "OPS/OMS Colombia", "pct_share_total_value": 2.6999, "cumulative_pct_share": 17.3476},
    {"rank": 5, "provider_label": "U. Antioquia", "pct_share_total_value": 2.6082, "cumulative_pct_share": 19.9558},
    {"rank": 6, "provider_label": "Agencia Atenea", "pct_share_total_value": 2.1051, "cumulative_pct_share": 22.0609},
    {"rank": 7, "provider_label": "DISCOLMETS SAS", "pct_share_total_value": 1.9139, "cumulative_pct_share": 23.9748},
    {"rank": 8, "provider_label": "U.T. MEDIPOL 14", "pct_share_total_value": 1.8528, "cumulative_pct_share": 25.8276},
    {"rank": 9, "provider_label": "POLPHARMA UT", "pct_share_total_value": 1.6017, "cumulative_pct_share": 27.4293},
    {"rank": 10, "provider_label": "U.T. MEDIPOL 15", "pct_share_total_value": 1.5785, "cumulative_pct_share": 29.0079},
]

FIG4_LORENZ_ROWS = [
    {"provider_share_pct": 0.0020, "cumulative_value_pct": 5.6517},
    {"provider_share_pct": 0.0060, "cumulative_value_pct": 14.6478},
    {"provider_share_pct": 0.0199, "cumulative_value_pct": 29.0079},
    {"provider_share_pct": 3.0005, "cumulative_value_pct": 85.8305},
    {"provider_share_pct": 10.0010, "cumulative_value_pct": 93.7105},
    {"provider_share_pct": 30.0010, "cumulative_value_pct": 97.7109},
    {"provider_share_pct": 50.0010, "cumulative_value_pct": 99.0718},
    {"provider_share_pct": 100.0, "cumulative_value_pct": 100.0},
]

FIG6_ROWS = [
    {"layer_number": 7, "layer_name": "Visualizacion", "primary_technology": "React / TypeScript", "function_or_scope": "Public observatory with time series maps and alerts"},
    {"layer_number": 6, "layer_name": "Contratos inteligentes", "primary_technology": "Solidity / Chainlink CRE / Sepolia", "function_or_scope": "Payment automation invoice NFTs and escrow release"},
    {"layer_number": 5, "layer_name": "Aprendizaje automatico", "primary_technology": "scikit-learn", "function_or_scope": "Demand prediction clustering and PCA modules"},
    {"layer_number": 4, "layer_name": "IA generativa (RAG)", "primary_technology": "Claude 3.5 Sonnet / GPT-4o / Pinecone", "function_or_scope": "Hybrid semantic plus TF-IDF retrieval over indexed documents"},
    {"layer_number": 3, "layer_name": "Procesamiento / API", "primary_technology": "FastAPI / Python / pandas", "function_or_scope": "Cleaning normalization classification and Z-score engine"},
    {"layer_number": 2, "layer_name": "Almacenamiento", "primary_technology": "PostgreSQL / Pinecone / MongoDB", "function_or_scope": "Relational vector and unstructured data storage"},
    {"layer_number": 1, "layer_name": "Recoleccion de datos", "primary_technology": "Socrata API / SECOP-II / INVIMA / SISMED", "function_or_scope": "Incremental ingestion of public pharmaceutical data"},
]

TABLE1_ROWS = [
    {"metric": "Total SECOP-II contracts (API universe)", "reported_value": "272814", "numeric_value": 272814, "unit": "contracts"},
    {"metric": "Pharmaceutical contracts after contract-level veterinary exclusions", "reported_value": "161830", "numeric_value": 161830, "unit": "contracts"},
    {"metric": "Total contracts in recovered local PostgreSQL source", "reported_value": "956157", "numeric_value": 956157, "unit": "contracts"},
    {"metric": "Total contracted value (corrected pharmaceutical cohort)", "reported_value": "16.93", "numeric_value": 16.93, "unit": "billones_cop"},
    {"metric": "Total contracted value (all sectors recovered local source)", "reported_value": "294.7", "numeric_value": 294.7, "unit": "billones_cop"},
    {"metric": "Total contracted value (API universe)", "reported_value": "42.00", "numeric_value": 42.00, "unit": "billones_cop"},
    {"metric": "Average value per positive-value pharmaceutical contract", "reported_value": "104.69", "numeric_value": 104.69, "unit": "millones_cop"},
    {"metric": "Unique normalized suppliers in corrected positive-value cohort", "reported_value": "50225", "numeric_value": 50225, "unit": "providers"},
    {"metric": "Regions covered", "reported_value": "36-37", "numeric_value": "", "unit": "regional_codes"},
    {"metric": "Period (pharmaceutical BD active years)", "reported_value": "2020 to 2025", "numeric_value": "", "unit": "period"},
    {"metric": "Period (monitored SECOP-II API)", "reported_value": "January 2015 onward", "numeric_value": "", "unit": "period"},
    {"metric": "Processed INVIMA records", "reported_value": "9838", "numeric_value": 9838, "unit": "records"},
    {"metric": "SISMED reference price records", "reported_value": "44038", "numeric_value": 44038, "unit": "records"},
    {"metric": "SISMED unique ATC codes", "reported_value": "1759", "numeric_value": 1759, "unit": "atc_codes"},
    {"metric": "SISMED reference period", "reported_value": "2017 to 2019", "numeric_value": "", "unit": "period"},
    {"metric": "Indexed vector RAG documents", "reported_value": "9336", "numeric_value": 9336, "unit": "documents"},
]

TABLE2_ROWS = [
    {"layer": "Recoleccion", "primary_technology": "Python / API Socrata", "main_function": "Ingesta incremental de SECOP-II INVIMA y SISMED"},
    {"layer": "Almacenamiento", "primary_technology": "PostgreSQL / Pinecone / MongoDB", "main_function": "Datos relacionales vectoriales y no estructurados"},
    {"layer": "Procesamiento", "primary_technology": "FastAPI / pandas", "main_function": "Limpieza normalizacion clasificacion ABC y motor Z-score"},
    {"layer": "IA generativa", "primary_technology": "Claude 3.5 Sonnet / GPT-4o", "main_function": "RAG con busqueda hibrida semantica y TF-IDF"},
    {"layer": "Aprendizaje automatico", "primary_technology": "scikit-learn", "main_function": "Prediccion de demanda k-means y PCA"},
    {"layer": "Contratos inteligentes", "primary_technology": "Solidity / Chainlink CRE / Sepolia", "main_function": "Automatizacion de pagos en 5 estados y NFT de facturas"},
    {"layer": "Visualizacion", "primary_technology": "React / TypeScript", "main_function": "Observatorio publico con series temporales mapas y alertas"},
]

SOURCE_FILE_MANIFEST_ROWS = [
    {"file_name": "Fig1_source_data.csv", "object_type": "figure", "underlies": "Fig 1", "source_basis": "Submission manuscript annual series plus frontend figure mapping", "notes": "Closed analytical cohort with complete calendar years 2020-2025"},
    {"file_name": "Fig2_source_data.csv", "object_type": "figure", "underlies": "Fig 2", "source_basis": "Submission manuscript geographic breakdown plus frontend figure mapping", "notes": "Bogota D.C. reported as combined SECOP codes"},
    {"file_name": "Fig3_category_source_data.csv", "object_type": "figure", "underlies": "Fig 3 panel A", "source_basis": "Submission manuscript category anomaly table plus frontend figure mapping", "notes": "Ordered in manuscript order"},
    {"file_name": "Fig3_yearly_source_data.csv", "object_type": "figure", "underlies": "Fig 3 panel B", "source_basis": "Submission manuscript yearly anomaly table plus frontend figure mapping", "notes": "Covers 2020 to 2025"},
    {"file_name": "Fig4_top10_source_data.csv", "object_type": "figure", "underlies": "Fig 4 provider bar chart", "source_basis": "Recovered original PostgreSQL snapshot; positive-value closed 2020-2025 cohort", "notes": "Contains top 10 provider shares and cumulative shares rounded for display"},
    {"file_name": "Fig4_lorenz_source_data.csv", "object_type": "figure", "underlies": "Fig 4 Lorenz curve", "source_basis": "Recovered original PostgreSQL snapshot; positive-value closed 2020-2025 cohort", "notes": "Control points used to reproduce the schematic Lorenz display"},
    {"file_name": "Fig5_notes.md", "object_type": "figure", "underlies": "Fig 5", "source_basis": "Conceptual source note anchored in manuscript sections 2.6 and 3.5 plus local evidence matrix", "notes": "No single numeric dataset"},
    {"file_name": "Fig6_components.csv", "object_type": "figure", "underlies": "Fig 6", "source_basis": "Submission manuscript Table 2 plus frontend architecture diagram", "notes": "Seven layers represented as machine-readable components"},
    {"file_name": "Table1_source_data.csv", "object_type": "table", "underlies": "Table 1", "source_basis": "Submission manuscript Table 1", "notes": "Machine-readable rendering of numbered table values"},
    {"file_name": "Table2_source_data.csv", "object_type": "table", "underlies": "Table 2", "source_basis": "Submission manuscript Table 2", "notes": "Machine-readable rendering of numbered table values"},
]

COLUMN_DICTIONARY_ROWS = [
    {"file_name": "Fig1_source_data.csv", "column_name": "year", "description": "Calendar year shown in the annual contracts figure", "unit_or_format": "YYYY"},
    {"file_name": "Fig1_source_data.csv", "column_name": "contracts_indexed_bd", "description": "Number of indexed pharmaceutical contracts in PostgreSQL", "unit_or_format": "contracts"},
    {"file_name": "Fig1_source_data.csv", "column_name": "value_thousand_million_cop", "description": "Annual contracted value expressed in thousand million COP", "unit_or_format": "thousand_million_cop"},
    {"file_name": "Fig1_source_data.csv", "column_name": "value_billones_cop", "description": "Annual contracted value expressed in billones COP", "unit_or_format": "billones_cop"},
    {"file_name": "Fig1_source_data.csv", "column_name": "coverage_note", "description": "Coverage qualifier for the reported year", "unit_or_format": "text"},
    {"file_name": "Fig2_source_data.csv", "column_name": "region", "description": "Department or combined regional code label", "unit_or_format": "text"},
    {"file_name": "Fig2_source_data.csv", "column_name": "contracts", "description": "Number of contracts in the region", "unit_or_format": "contracts"},
    {"file_name": "Fig2_source_data.csv", "column_name": "value_thousand_million_cop", "description": "Contracted value for the region", "unit_or_format": "thousand_million_cop"},
    {"file_name": "Fig2_source_data.csv", "column_name": "pct_total_national_value", "description": "Regional share of national contracted value", "unit_or_format": "percent"},
    {"file_name": "Fig3_category_source_data.csv", "column_name": "category_label", "description": "Therapeutic category label used in the figure", "unit_or_format": "text"},
    {"file_name": "Fig3_category_source_data.csv", "column_name": "contracts_analyzed", "description": "Number of contracts analyzed in the category", "unit_or_format": "contracts"},
    {"file_name": "Fig3_category_source_data.csv", "column_name": "pct_with_alert", "description": "Share of category contracts with abs(Z) greater than or equal to 1.5 sigma", "unit_or_format": "percent"},
    {"file_name": "Fig3_category_source_data.csv", "column_name": "z_max", "description": "Maximum observed Z-score in the category", "unit_or_format": "z_score"},
    {"file_name": "Fig3_category_source_data.csv", "column_name": "ratio_max_to_category_mean", "description": "Maximum contract-value ratio against the category mean", "unit_or_format": "times"},
    {"file_name": "Fig3_yearly_source_data.csv", "column_name": "year", "description": "Calendar year", "unit_or_format": "YYYY"},
    {"file_name": "Fig3_yearly_source_data.csv", "column_name": "contracts_analyzed", "description": "Number of contracts analyzed in the year", "unit_or_format": "contracts"},
    {"file_name": "Fig3_yearly_source_data.csv", "column_name": "contracts_with_alert", "description": "Contracts with abs(Z) greater than or equal to 1.5 sigma", "unit_or_format": "contracts"},
    {"file_name": "Fig3_yearly_source_data.csv", "column_name": "alert_rate_pct", "description": "Yearly alert rate", "unit_or_format": "percent"},
    {"file_name": "Fig4_top10_source_data.csv", "column_name": "rank", "description": "Provider rank by contracted value", "unit_or_format": "integer"},
    {"file_name": "Fig4_top10_source_data.csv", "column_name": "provider_label", "description": "Provider label used in the figure", "unit_or_format": "text"},
    {"file_name": "Fig4_top10_source_data.csv", "column_name": "pct_share_total_value", "description": "Share of total contracted value held by the provider", "unit_or_format": "percent"},
    {"file_name": "Fig4_top10_source_data.csv", "column_name": "cumulative_pct_share", "description": "Cumulative share through that provider rank", "unit_or_format": "percent"},
    {"file_name": "Fig4_lorenz_source_data.csv", "column_name": "provider_share_pct", "description": "Share of providers on the Lorenz X axis", "unit_or_format": "percent"},
    {"file_name": "Fig4_lorenz_source_data.csv", "column_name": "cumulative_value_pct", "description": "Cumulative share of contracted value on the Lorenz Y axis", "unit_or_format": "percent"},
    {"file_name": "Fig6_components.csv", "column_name": "layer_number", "description": "Layer order in the architecture stack", "unit_or_format": "integer"},
    {"file_name": "Fig6_components.csv", "column_name": "layer_name", "description": "Layer label", "unit_or_format": "text"},
    {"file_name": "Fig6_components.csv", "column_name": "primary_technology", "description": "Main technologies associated with the layer", "unit_or_format": "text"},
    {"file_name": "Fig6_components.csv", "column_name": "function_or_scope", "description": "Main function represented in the layer", "unit_or_format": "text"},
    {"file_name": "Table1_source_data.csv", "column_name": "metric", "description": "Table 1 metric label", "unit_or_format": "text"},
    {"file_name": "Table1_source_data.csv", "column_name": "reported_value", "description": "Literal value reported in the manuscript table", "unit_or_format": "text"},
    {"file_name": "Table1_source_data.csv", "column_name": "numeric_value", "description": "Numeric rendering when the value is single-valued", "unit_or_format": "number"},
    {"file_name": "Table1_source_data.csv", "column_name": "unit", "description": "Measurement or format descriptor", "unit_or_format": "text"},
    {"file_name": "Table2_source_data.csv", "column_name": "layer", "description": "Architecture layer label", "unit_or_format": "text"},
    {"file_name": "Table2_source_data.csv", "column_name": "primary_technology", "description": "Primary technology field reported in Table 2", "unit_or_format": "text"},
    {"file_name": "Table2_source_data.csv", "column_name": "main_function", "description": "Main function reported in Table 2", "unit_or_format": "text"},
]

FIG5_NOTE = """# Fig 5 source note

Figure 5 is a conceptual comparison figure and is therefore documented with a source note rather than a single numeric CSV.

Construction basis:

- Left column: institutional flow assembled from local Servicio Farmaceutico evidence on need identification, order preparation, supply, reception, registration, and control, plus a general administrative-financial segment for invoice filing, causation, treasury, and payment.
- Right column: prototype digital states validated in Sepolia testnet as a proof of concept.
- Current-cycle reference: 60 to 180 days, with a median institutional reference of 90 days.
- Prototype-cycle reference: approximately 30 hours.
- Financial scenario shown in the figure: corrected mean annual flow of COP 2.82 billones and corrected 2025 flow of COP 5.50 billones, financial cost of 2% monthly, and a theoretical reduction of the administrative digital cycle from 90 days to about 30 hours. The corresponding illustrative outputs are COP 167-325 billion/year.

Primary manuscript anchors:

- Methods section 2.6 for the interpretive scope of the comparison.
- Results section 3.5 for the prototype state times and projected savings scenario.

Primary implementation anchors:

- apps/frontend-web/src/pages/FigurasArticuloPage.tsx
- docs/publicacion_cientifica/matriz_consolidada_evidencia_empirica_local.md
"""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")


def main() -> None:
    output_map = {
        FIGURES_DIR / "Fig1_source_data.csv": FIG1_ROWS,
        FIGURES_DIR / "Fig2_source_data.csv": FIG2_ROWS,
        FIGURES_DIR / "Fig3_category_source_data.csv": FIG3_CATEGORY_ROWS,
        FIGURES_DIR / "Fig3_yearly_source_data.csv": FIG3_YEARLY_ROWS,
        FIGURES_DIR / "Fig4_top10_source_data.csv": FIG4_TOP10_ROWS,
        FIGURES_DIR / "Fig4_lorenz_source_data.csv": FIG4_LORENZ_ROWS,
        FIGURES_DIR / "Fig6_components.csv": FIG6_ROWS,
        TABLES_DIR / "Table1_source_data.csv": TABLE1_ROWS,
        TABLES_DIR / "Table2_source_data.csv": TABLE2_ROWS,
        METADATA_DIR / "source_file_manifest.csv": SOURCE_FILE_MANIFEST_ROWS,
        METADATA_DIR / "column_dictionary.csv": COLUMN_DICTIONARY_ROWS,
    }

    for path, rows in output_map.items():
        write_csv(path, rows)

    write_text(FIGURES_DIR / "Fig5_notes.md", FIG5_NOTE)

    generated = [str(path.relative_to(PAPER_REPO)) for path in output_map]
    generated.append(str((FIGURES_DIR / "Fig5_notes.md").relative_to(PAPER_REPO)))
    print("Generated paper source-data files:")
    for item in generated:
        print(f"- {item}")


if __name__ == "__main__":
    main()
