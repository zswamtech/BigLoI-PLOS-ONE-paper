# BigLoI — PLOS ONE reproducibility package

Article-specific package for:

**Computational surveillance of Colombian public pharmaceutical procurement using public administrative data: a reproducible analysis of a closed 2020–2025 cohort**

- Manuscript ID: **PONE-D-26-13579R2** (under peer review at [PLOS ONE](https://journals.plos.org/plosone/))
- Author: Andrés Soto · ORCID [0009-0004-8001-5372](https://orcid.org/0009-0004-8001-5372)
- Archive: [https://doi.org/10.5281/zenodo.19074137](https://doi.org/10.5281/zenodo.19074137)

## Canonical R2 cohort (contract-level veterinary correction)

| Metric | Value |
| --- | ---: |
| Corrected closed cohort (2020–2025) | **161,830** contracts |
| Positive-value / normalized suppliers | **161,710** / **50,225** |
| Top 3% supplier value share | **85.83%** (figure annotation 85.8%) |
| HHI (0–10,000) | **120.99** |
| Z-score denominator / alerts \|Z\|≥1.5 | **146,594** / **664** |
| 2025 indexed → Z-score eligible | **21,955 → 6,729** (`NO_ESPECIFICADO` = 15,226) |

Source → corrected: 162,271 candidate contracts − 441 explicit veterinary/agricultural exclusions.

## Structure

- `manuscript/` — submission Markdown/DOCX (and cover letter)
- `figures/` — masters (PNG) and submission TIFFs (Fig1–Fig6)
- `data/derived/` — figure/table CSVs, metadata, and `corrections/veterinary_exclusion/` audit artifacts
- `code/` — minimal regeneration/verification scripts
- `statements/` — data/code availability text for journal forms

## Reproduce (minimal)

```bash
# verify packaged source tables
python code/scripts/verify_paper_source_data.py

# regenerate English figure masters from packaged CSVs (optional)
python code/scripts/render_english_figures.py
```

See `code/README.md` and `PUBLISHING_EXTERNAL.md` for environment notes and release workflow.

## Citation

Prefer citing the manuscript once published. Until then, cite this package via the Zenodo DOI above (`CITATION.cff`).

## Scope note

Statistical alerts are exploratory prioritization signals, not evidence of corruption or fraud. The Sepolia smart-contract module is a simulated technical proof of concept only.
