#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON:-python3}"
"$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)' || { echo 'AAM O94.1 exige Python 3.11+.' >&2; exit 2; }
"$PYTHON_BIN" -c 'import tkinter' || { echo 'AAM O94.1 requiert Tk/Tcl pour l’interface graphique.' >&2; exit 3; }
export PYTHONPATH="$(pwd)${PYTHONPATH:+:$PYTHONPATH}"
exec "$PYTHON_BIN" -m aam_o93 ui
