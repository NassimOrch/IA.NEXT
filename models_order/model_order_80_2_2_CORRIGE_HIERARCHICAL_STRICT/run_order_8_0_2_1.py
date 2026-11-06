#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from order80.general_engine import GeneralResearchEngine

def main():
    ap=argparse.ArgumentParser(description='ORDER80.2.1 general reference-guided research engine')
    ap.add_argument('--task',required=True,help='JSON task with problem/objective and optional required_terms')
    ap.add_argument('--references',required=True,help='JSON reference manifest: local paths + web URLs/allowlist')
    ap.add_argument('--output',default='run_output_o8021')
    ap.add_argument('--memory',default=None)
    ap.add_argument('--duration',default='1h',help='e.g. 30m, 1h, 24h, 1week, forever')
    ap.add_argument('--no-web',action='store_true')
    ap.add_argument('--local-batch',type=int,default=4); ap.add_argument('--rag-batch',type=int,default=6); ap.add_argument('--chunk-size',type=int,default=5000)
    args=ap.parse_args()
    ref=json.loads(Path(args.references).read_text(encoding='utf-8'))
    if args.no_web: ref.setdefault('web',{})['enabled']=False
    # Reference manifest is immutable input for this run; task remains separate.
    tmp=Path(args.references)
    cfg=dict(ref.get('engine',{})); cfg.update({'duration':args.duration,'local_batch':args.local_batch,'rag_batch':args.rag_batch,'chunk_size':args.chunk_size})
    eng=GeneralResearchEngine(args.task,tmp,args.output,args.memory,cfg)
    if args.no_web: eng.web.enabled=False
    result=eng.run()
    print(json.dumps({k:result.get(k) for k in ('status','resolution_status','cycles','observation_rounds')},indent=2,ensure_ascii=False))
    return 0
if __name__=='__main__': raise SystemExit(main())
