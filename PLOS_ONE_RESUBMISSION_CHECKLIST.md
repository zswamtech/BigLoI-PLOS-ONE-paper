# PLOS ONE Resubmission Checklist

Short operational checklist for the editorial resubmission package.

## Package status

**R2 freeze (2026-07-18 D7):** package ready after week deep-dive (D1–D5). Dry-run **47/47 PASS**. Track Changes regenerated vs EM R1 baseline (37 ins / 66 del). Abstract Results demoted PoC savings figures. See `docs/publicacion_cientifica/D7_FREEZE_R2.md`. Figures 1–6 unchanged (Fig4 Top 3% = 85.8%; veterinary correction 2026-07-11).

Canonical corrected figures: 161,830 contracts; 161,710 positive-value contracts; COP 16.93 trillion; 50,225 normalized suppliers; HHI 120.99; 146,594 Z-score-analyzable contracts; alert strata 664 / 508 / 295; 2025 Z-score funnel 21,955 → 6,729.

See also: `docs/publicacion_cientifica/PLOS_ONE_R2_UPLOAD_CHECKLIST.md` and `docs/publicacion_cientifica/Response_to_Reviewers_R2.md`.

## Files to upload to PLOS ONE

### 1. Main manuscript

- manuscript/Manuscript_main_submission.docx

### 2. Cover letter

- manuscript/Cover_letter_submission.pdf

Preferred editable alternative if needed by the platform:

- manuscript/Cover_letter_submission.docx

### 3. Figures as separate files

- figures/submission/Fig1.tif
- figures/submission/Fig2.tif
- figures/submission/Fig3.tif
- figures/submission/Fig4.tif
- figures/submission/Fig5.tif
- figures/submission/Fig6.tif

### 4. Supporting source-data files

- data/derived/figures/Fig1_source_data.csv
- data/derived/figures/Fig2_source_data.csv
- data/derived/figures/Fig3_category_source_data.csv
- data/derived/figures/Fig3_yearly_source_data.csv
- data/derived/figures/Fig4_lorenz_source_data.csv
- data/derived/figures/Fig4_top10_source_data.csv
- data/derived/tables/Table1_source_data.csv
- data/derived/tables/Table2_source_data.csv
- data/derived/metadata/column_dictionary.csv
- data/derived/metadata/source_file_manifest.csv

### 5. Corrected response and supporting information

- `docs/publicacion_cientifica/submission/PLOS_ONE_UPLOAD_CLEAN/Response_to_Reviewers.docx` (**R2 regenerated 2026-07-18**)
- `docs/publicacion_cientifica/submission/PLOS_ONE_UPLOAD_CLEAN/S1_Table.docx`

### 6. Revised manuscript with tracked changes

- `docs/publicacion_cientifica/submission/PLOS_ONE_UPLOAD_CLEAN/Revised_Manuscript_with_Track_Changes.docx`
- **Done (2026-07-18, cold-read):** regenerated vs **`Manuscript_EM_R1_BASELINE.docx`** (git `8e19d14`, byte-equivalent numbers to EM PDF `PONE-D-26-13579_R1.pdf`: 162,271 / 50,460 / 85.87 / 6,792). OOXML `w:ins`/`w:del` present. Working copy: `Manuscript_with_Track_Changes2.docx`. Optional: Word Compare GUI before upload.

## Internal checks before upload

- Confirm that manuscript/Manuscript_main_submission.docx is fully in English.
- Confirm that the manuscript title and all figure legends use the closed 2020-2025 cohort.
- Confirm that Fig1_source_data.csv and Table1_source_data.csv no longer include 2026 partial data.
- Confirm that CITATION.cff and manuscript/Cover_letter_submission.* no longer say 2020-2026.
- Confirm that the clean manuscript and Response to Reviewers contain 161,830 / 146,594 / 664 / 120.99 and do not contain the superseded 15.95-trillion supplier-level correction.
- Confirm that the tracked-changes DOCX was regenerated after the 2026-07-11 contract-level correction.
- Confirm that the Editorial Manager title, abstract, and ethics statement match the corrected manuscript.

## Do not upload unless explicitly requested

- manuscript/Manuscript_main_submission.md
- manuscript/Cover_letter_submission.md
- code/
- CITATION.cff
- PUBLISHING_EXTERNAL.md
- EDITORIAL_DELIVERY_FINAL_NOTE.md
- RELEASE_METADATA_TO_FILL.md
- RELEASE_HISTORY_SUMMARY.md