#!/usr/bin/env python3
"""Check every regular payload file against FILE_MANIFEST_V005.csv."""
from pathlib import Path
import csv, hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
M=ROOT/"05_PROVENANCE"/"FILE_MANIFEST_V005.csv"
errors=[]; checked=0
with M.open(encoding="utf-8-sig",newline="") as f:
    for row in csv.DictReader(f):
        p=ROOT/row["path"]
        if not p.is_file(): errors.append("missing: "+row["path"]); continue
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        if h!=row["sha256"] or p.stat().st_size!=int(row["bytes"]): errors.append("mismatch: "+row["path"])
        checked+=1
print(json.dumps({"checked":checked,"errors":errors},indent=2))
sys.exit(1 if errors else 0)
