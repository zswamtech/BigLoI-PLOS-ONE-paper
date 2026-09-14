# External publishing guide

**Status (2026-09-14):** the article is published in [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0350967) (DOI [10.1371/journal.pone.0350967](https://doi.org/10.1371/journal.pone.0350967)). The article-specific package is archived at Zenodo version DOI [10.5281/zenodo.22754602](https://doi.org/10.5281/zenodo.22754602) (concept DOI [10.5281/zenodo.19074137](https://doi.org/10.5281/zenodo.19074137)). The workflow below is retained as historical release procedure.

This package is prepared for external publication in one of two ways:

1. Preferred: dedicated public repository for the paper package.
2. Acceptable alternative: frozen public release archived from the main repository.

## Recommended path

The preferred path is a dedicated public repository because it gives editors and reviewers a smaller and clearer reproducibility package than the full BigLoI monorepo.

Suggested repository name:

- BigLoI-PLOS-ONE-paper

## What is already ready

- manuscript files are packaged;
- final TIFF figures are packaged;
- derived figure and table data are packaged;
- minimal regeneration and verification scripts are packaged;
- environment notes are packaged;
- citation metadata is packaged.

## Public-release items (completed)

The following items were outstanding during preparation and are now complete:

- public repository URL and Zenodo version DOI recorded (`10.5281/zenodo.22754602`; concept DOI `10.5281/zenodo.19074137`);
- English R2 manuscript freeze is the public scholarly text; PLOS ONE article DOI `10.1371/journal.pone.0350967`;
- public links verified (GitHub + Zenodo + PLOS ONE article);
- revision cover letter retained in the public archive (no confidential reviewer identities);
- public release archived in Zenodo.

## Dedicated repository workflow

1. Run the release-preparation script for the paper package.
2. Run the standalone staging script.
3. Create a new public GitHub repository.
4. Copy the staged package contents into that repository root.
5. Commit and push.
6. Create a GitHub release.
7. Archive that release in Zenodo.
8. Update manuscript and release metadata with the final public release URL and, if available, the Zenodo DOI.

## Main repository release workflow

1. Run the release-preparation script for the paper package.
2. Tag a frozen state in the main repository.
3. Create a GitHub release that clearly points to this paper package directory.
4. Archive the release in Zenodo.
5. Ensure the public release notes link directly to the package path and explain that this subdirectory is the article-specific reproducibility layer.

## Staging command

From the workspace root:

```bash
bash docs/publicacion_cientifica/paper_repository_plosone/code/scripts/stage_external_package.sh
```

This command:

- regenerates and verifies the paper package;
- creates a publish-ready standalone copy;
- prints the staging location and next manual steps.

## Recommended public-root contents

- README.md
- CITATION.cff
- manuscript/
- figures/
- data/
- code/
- statements/
- .gitignore

## Files to review before making the repository public

- statements/DATA_AVAILABILITY_STATEMENT.md
- statements/CODE_AVAILABILITY_STATEMENT.md
- CITATION.cff
- manuscript/Manuscript_main_submission.md
- manuscript/Cover_letter_submission.* if you decide not to expose editorial correspondence
