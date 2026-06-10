#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../../../.." && pwd)"

if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
else
  PYTHON_BIN="python3"
fi

cd "$ROOT_DIR"
"$PYTHON_BIN" docs/publicacion_cientifica/publish_ready/BigLoI-PLOS-ONE-paper/code/scripts/simulate_inventory_soc.py "$@"