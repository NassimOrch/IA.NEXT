#!/usr/bin/env python3
from __future__ import annotations
import sys, pathlib, json, tempfile
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from o76 import MathEngine
from o76.integrity import scan_source

CASES=[
 ('ring',{'mode':'prove','variables':['x'],'target':'(x+1)^2=x^2+2*x+1'}),
 ('ideal',{'mode':'prove','variables':['x','y'],'assumptions':['x^2-2=0'],'target':'x^4-4=0'}),
 ('linear',{'mode':'solve','variables':['x','y'],'equations':['2*x+y=5','x-y=1']}),
 ('sturm',{'mode':'solve','variables':['x'],'equations':['x^4-5*x^2+4=0']}),
 ('logic_true',{'mode':'logic','target':'(p->q)&p->q'}),
 ('logic_false',{'mode':'logic','target':'p&!p'}),
 ('finite_true',{'mode':'prove','variables':['x'],'domains':{'x':{'min':0,'max':2}},'assumptions':['x=1'],'target':'x^2=1'}),
 ('finite_refuted',{'mode':'prove','variables':['x'],'domains':{'x':{'min':0,'max':2}},'target':'x=1'}),
 ('crt',{'mode':'congruences','congruences':[{'a':2,'modulus':3},{'a':3,'modulus':5}]}),
 ('dio',{'mode':'diophantine','variables':['x','y'],'equations':['6*x+9*y=15']}),
 ('pell',{'mode':'pell','definitions':{'D':2}}),
 ('matrix',{'mode':'matrix','matrix':[[1,2],[2,4]]}),
]

def main():
    failures=[]
    engcfg={'resources':{'time_s':30,'max_steps':50,'max_groebner_pairs':10000,'max_finite_cases':100000}}
    for name,data in CASES:
        r=MathEngine(engcfg).run(data)
        ok=r.get('status') in {'PROVEN','REFUTED'} and r.get('verification',{}).get('ok') is True
        if not ok: failures.append((name,r))
        print(f'{name}: {r.get("status")} {r.get("strategy")}')
    with tempfile.TemporaryDirectory() as td:
        p={'mode':'prove','variables':['x','y'],'assumptions':['x^2+y^2-1=0','x-y=0'],'target':'2*x^2-1=0'}
        c={'resources':{'time_s':30,'max_steps':1,'enabled_strategies':['GROEBNER_BUCHBERGER'],'max_groebner_pairs':1},'checkpoint':str(pathlib.Path(td)/'ckpt.json')}
        r1=MathEngine(c).run(p); c['resources']['max_groebner_pairs']=1000; r2=MathEngine(c).run(p)
        print(f'checkpoint_pause: {r1.get("status")}'); print(f'checkpoint_resume: {r2.get("status")}')
        if r1.get('status')!='UNRESOLVED' or r2.get('status')!='PROVEN': failures.append(('checkpoint_resume',r1,r2))
    hits=scan_source(str(ROOT/'src'))
    print(f'integrity_scan: {"PASS" if not hits else "FAIL"}')
    if hits: failures.append(('integrity',hits))
    print(f'selfcheck: {"PASS" if not failures else "FAIL"}')
    if failures:
        print(json.dumps(failures,ensure_ascii=False,indent=2,default=str)); return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
