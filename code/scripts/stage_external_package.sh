#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
PACKAGE_DIR="$ROOT_DIR/docs/publicacion_cientifica/paper_repository_plosone"
STAGING_ROOT="$ROOT_DIR/docs/publicacion_cientifica/publish_ready"
STAGING_DIR="$STAGING_ROOT/BigLoI-PLOS-ONE-paper"
OVERWRITE="${1:-}"

cd "$ROOT_DIR"

echo "[1/3] Preparing frozen paper package..."
bash docs/publicacion_cientifica/paper_repository_plosone/code/scripts/release_paper_source_data.sh

echo "[2/3] Creating standalone staging directory..."
mkdir -p "$STAGING_ROOT"

if [[ -d "$STAGING_DIR" ]] && [[ -n "$(find "$STAGING_DIR" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]]; then
	if [[ "$OVERWRITE" != "--overwrite" ]]; then
		echo "Staging directory already exists and is not empty: $STAGING_DIR"
		echo "Re-run with --overwrite to replace it explicitly."
		exit 1
	fi
	rm -rf "$STAGING_DIR"
fi

mkdir -p "$STAGING_DIR"

cp -R "$PACKAGE_DIR"/. "$STAGING_DIR"/

echo "[3/3] Standalone package staged successfully."
echo "Staging directory: $STAGING_DIR"
echo "Next steps:"
echo "- review final public-release URL and DOI fields in statements and metadata"
echo "- decide whether to keep or remove cover letter files before public release"
echo "- push the staged contents to a dedicated public repository or use them for an archived release"