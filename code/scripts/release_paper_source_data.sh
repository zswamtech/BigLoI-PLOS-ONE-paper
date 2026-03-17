#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"

cd "$ROOT_DIR"

echo "[1/2] Regenerating frozen paper source-data files..."
bash docs/publicacion_cientifica/paper_repository_plosone/code/scripts/regenerate_source_data.sh

echo "[2/2] Verifying regenerated paper source-data files..."
bash docs/publicacion_cientifica/paper_repository_plosone/code/scripts/verify_source_data.sh

echo "Paper source-data release step completed successfully."