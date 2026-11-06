#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from order80.general_hierarchical import HierarchicalGeneralEngine

def main():
    ap=argparse.ArgumentParser(description='ORDER80.2.2 general hierarchical reference-guided solver')
    ap.add_argument('--task',required=True); ap.add_argument('--references',required=True); ap.add_argument('--output',default='run_output_o8022'); ap.add_argument('--memory',default=None); ap.add_argument('--duration',default='1h'); ap.add_argument('--no-web',action='store_true'); ap.add_argument('--max-depth',type=int,default=8); ap.add_argument('--max-children-per-node',type=int,default=3); args=ap.parse_args()
    ref=json.loads(Path(args.references).read_text(encoding='utf-8'))
    cfg=dict(ref.get('engine',{})); cfg.update({'duration':args.duration,'max_depth':args.max_depth,'max_children_per_node':args.max_children_per_node,'web_enabled_override':False if args.no_web else None})
    eng=HierarchicalGeneralEngine(args.task,args.references,args.output,args.memory,cfg)
    if args.no_web: eng.web.enabled=False
    r=eng.run(); print(json.dumps({k:r.get(k) for k in ('status','resolution_status','cycles','observation_rounds','node_attempts')},indent=2,ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
