#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON:-python3}"
"$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)' || { echo 'AAM O94.4 exige Python 3.11+.' >&2; exit 2; }
"$PYTHON_BIN" -c 'import tkinter' || { echo 'AAM O94.4 requiert Tk/Tcl pour l’interface graphique.' >&2; exit 3; }
export PYTHONPATH="$(pwd)${PYTHONPATH:+:$PYTHONPATH}"
"$PYTHON_BIN" -c 'import json; from pathlib import Path; from aam_o93.preflight import preflight; r=preflight(Path.cwd(), "launcher:posix-sh"); print(json.dumps(r, ensure_ascii=False)); raise SystemExit(0 if r.get("status") == "PASS_BOUNDED" else 20)' || { echo 'AAM O94.4 preflight blocked; inspect the JSON diagnostic above.' >&2; exit 20; }
exec "$PYTHON_BIN" -m aam_o93 ui
