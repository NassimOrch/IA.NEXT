#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from o76 import MathEngine

def main():
    ap=argparse.ArgumentParser(description="MODEL mathématique O76 — raisonnement exact avec certificats rejouables")
    ap.add_argument("problem",help="JSON, TXT ou - pour stdin")
    ap.add_argument("--config",default=str(ROOT/"config/o76.json"))
    ap.add_argument("--time",type=float)
    ap.add_argument("--max-steps",type=int)
    ap.add_argument("--max-gb-pairs",type=int)
    ap.add_argument("--max-finite-cases",type=int)
    ap.add_argument("--memory")
    ap.add_argument("--checkpoint")
    ap.add_argument("--strategies",help="liste séparée par virgules")
    args=ap.parse_args()
    cfg=json.loads(Path(args.config).read_text()) if args.config else {}
    res=cfg.setdefault("resources",{})
    if args.time is not None:res["time_s"]=args.time
    if args.max_steps is not None:res["max_steps"]=args.max_steps
    if args.max_gb_pairs is not None:res["max_groebner_pairs"]=args.max_gb_pairs
    if args.max_finite_cases is not None:res["max_finite_cases"]=args.max_finite_cases
    if args.strategies is not None:res["enabled_strategies"]=[x.strip() for x in args.strategies.split(",") if x.strip()]
    if args.memory is not None:cfg["memory"]=args.memory
    if args.checkpoint is not None:cfg["checkpoint"]=args.checkpoint
    src=sys.stdin.read() if args.problem=="-" else Path(args.problem).read_text()
    try:
        data=json.loads(src)
    except json.JSONDecodeError:
        data=src
    result=MathEngine(cfg).run(data)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2,default=str))
    return 0 if result.get("status") in {"PROVEN","REFUTED"} else 2

if __name__=="__main__":raise SystemExit(main())
