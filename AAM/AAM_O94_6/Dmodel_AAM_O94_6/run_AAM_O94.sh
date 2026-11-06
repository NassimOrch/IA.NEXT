#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON:-python3}"
"$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)' || { echo 'AAM O94 exige Python 3.11+.' >&2; exit 2; }
exec "$PYTHON_BIN" -m aam_o93 ui
