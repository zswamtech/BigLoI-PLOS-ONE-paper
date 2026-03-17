# External publishing guide

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

## What still must be completed before public release

- confirm the final public release URL and, once available, the Zenodo DOI in manuscript and release metadata files;
- confirm which manuscript version will be public if the English version supersedes the current one;
- verify that all links are public and stable;
- decide whether the cover letter remains internal or is omitted from the public archive;
- archive the public release in Zenodo and record the DOI.

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
