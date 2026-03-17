#!/usr/bin/env python3
"""Verify the frozen paper-specific source-data package.

Checks performed:
1. All expected output files exist.
2. CSV files have the exact expected headers.
3. CSV files contain at least one data row.
4. The conceptual note for Fig 5 exists and starts with the expected heading.

Invocation:
    python docs/publicacion_cientifica/paper_repository_plosone/code/scripts/verify_paper_source_data.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path


PAPER_REPO = Path(__file__).resolve().parents[2]

EXPECTED_CSV_HEADERS = {
    "data/derived/figures/Fig1_source_data.csv": [
        "year",
        "contracts_indexed_bd",
        "value_thousand_million_cop",
        "value_billones_cop",
        "coverage_note",
    ],
    "data/derived/figures/Fig2_source_data.csv": [
        "region",
        "contracts",
        "value_thousand_million_cop",
        "pct_total_national_value",
    ],
    "data/derived/figures/Fig3_category_source_data.csv": [
        "category_label",
        "contracts_analyzed",
        "pct_with_alert",
        "z_max",
        "ratio_max_to_category_mean",
    ],
    "data/derived/figures/Fig3_yearly_source_data.csv": [
        "year",
        "contracts_analyzed",
        "contracts_with_alert",
        "alert_rate_pct",
    ],
    "data/derived/figures/Fig4_top10_source_data.csv": [
        "rank",
        "provider_label",
        "pct_share_total_value",
        "cumulative_pct_share",
    ],
    "data/derived/figures/Fig4_lorenz_source_data.csv": [
        "provider_share_pct",
        "cumulative_value_pct",
    ],
    "data/derived/figures/Fig6_components.csv": [
        "layer_number",
        "layer_name",
        "primary_technology",
        "function_or_scope",
    ],
    "data/derived/tables/Table1_source_data.csv": [
        "metric",
        "reported_value",
        "numeric_value",
        "unit",
    ],
    "data/derived/tables/Table2_source_data.csv": [
        "layer",
        "primary_technology",
        "main_function",
    ],
    "data/derived/metadata/source_file_manifest.csv": [
        "file_name",
        "object_type",
        "underlies",
        "source_basis",
        "notes",
    ],
    "data/derived/metadata/column_dictionary.csv": [
        "file_name",
        "column_name",
        "description",
        "unit_or_format",
    ],
}

EXPECTED_TEXT_FILES = {
    "data/derived/figures/Fig5_notes.md": "# Fig 5 source note",
}


def verify_csv(relative_path: str, expected_header: list[str]) -> list[str]:
    errors: list[str] = []
    path = PAPER_REPO / relative_path

    if not path.exists():
        return [f"Missing file: {relative_path}"]

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            return [f"Empty CSV file: {relative_path}"]

        if header != expected_header:
            errors.append(
                f"Header mismatch in {relative_path}: expected {expected_header}, found {header}"
            )

        try:
            first_row = next(reader)
        except StopIteration:
            first_row = None

        if first_row is None:
            errors.append(f"CSV has no data rows: {relative_path}")

    return errors


def verify_text_file(relative_path: str, expected_first_line: str) -> list[str]:
    path = PAPER_REPO / relative_path

    if not path.exists():
        return [f"Missing file: {relative_path}"]

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return [f"Text file is empty: {relative_path}"]

    first_line = content.splitlines()[0] if content.splitlines() else ""
    if first_line != expected_first_line:
        return [
            f"First line mismatch in {relative_path}: expected {expected_first_line!r}, found {first_line!r}"
        ]

    return []


def main() -> int:
    errors: list[str] = []

    for relative_path, expected_header in EXPECTED_CSV_HEADERS.items():
        errors.extend(verify_csv(relative_path, expected_header))

    for relative_path, expected_first_line in EXPECTED_TEXT_FILES.items():
        errors.extend(verify_text_file(relative_path, expected_first_line))

    if errors:
        print("Paper source-data verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Paper source-data verification passed.")
    print(f"Verified CSV files: {len(EXPECTED_CSV_HEADERS)}")
    print(f"Verified text files: {len(EXPECTED_TEXT_FILES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())