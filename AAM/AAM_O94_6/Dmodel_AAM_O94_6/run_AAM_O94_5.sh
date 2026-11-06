#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
PYTHON_BIN="${AAM_PYTHON:-python3}"
"$PYTHON_BIN" scripts/preflight_o945.py
exec "$PYTHON_BIN" -m aam_o93 ui
