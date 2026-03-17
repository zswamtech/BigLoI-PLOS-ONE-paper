# Minimal reproduction scripts

This directory contains the smallest script layer required to regenerate the paper-specific derived source-data files.

Current scripts:

- generate_paper_source_data.py: regenerates the frozen figure and table CSV files, plus the minimal metadata files and the conceptual note for Fig 5.
- regenerate_source_data.sh: shell wrapper that runs the Python generator from the workspace root.
- verify_paper_source_data.py: verifies that all expected outputs exist and that CSV headers match the frozen paper package specification.
- verify_source_data.sh: shell wrapper that runs the verification script from the workspace root.
- release_paper_source_data.sh: runs regeneration and verification together as a single release-preparation step for the frozen paper package.
- stage_external_package.sh: creates a publish-ready standalone copy of the paper package for a dedicated repository or archived release workflow.

Input basis:

- frozen submission manuscript values;
- frozen figure definitions used in the article package;
- conceptual note for Fig 5 derived from the manuscript and local evidence synthesis.

Primary outputs:

- data/derived/figures/*.csv
- data/derived/tables/*.csv
- data/derived/metadata/*.csv
- data/derived/figures/Fig5_notes.md

Exact invocation:

```bash
python docs/publicacion_cientifica/paper_repository_plosone/code/scripts/generate_paper_source_data.py
```

Or:

```bash
bash docs/publicacion_cientifica/paper_repository_plosone/code/scripts/regenerate_source_data.sh
```

Release-preparation command:

```bash
bash docs/publicacion_cientifica/paper_repository_plosone/code/scripts/release_paper_source_data.sh
```

Standalone staging command:

```bash
bash docs/publicacion_cientifica/paper_repository_plosone/code/scripts/stage_external_package.sh
```

Verification command:

```bash
python docs/publicacion_cientifica/paper_repository_plosone/code/scripts/verify_paper_source_data.py
```

Or:

```bash
bash docs/publicacion_cientifica/paper_repository_plosone/code/scripts/verify_source_data.sh
```

These scripts intentionally regenerate the frozen paper package, not a live export from changing APIs.
