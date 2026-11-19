#!/usr/bin/env python3
"""Evaluate latest-user-turn language routing; threshold/window tuning on VALIDATION only."""
from __future__ import annotations
import argparse, hashlib, json, math, re, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Dmodel_eSonde_v8'/'src'))
from esonde_v6.features import tokenize
ROLE=re.compile(r'(?m)(?:^|\n)(USER|ASSISTANT):\s*')
PRIORS=ROOT/'Dmodel_eSonde_v8/models/eSonde_v8/response_language_priors.json'
VALID=ROOT/'derived/OASST1_chat/validation.jsonl';TEST=ROOT/'derived/OASST1_chat/test.jsonl'
def latest_user(text):
 t=str(text or '');m=list(ROLE.finditer(t))
 if not m:return t
 for i in range(len(m)-1,-1,-1):
  if m[i].group(1)=='USER':return t[m[i].end():(m[i+1].start() if i+1<len(m) else len(t))].strip()
 return t
def read_rows(path):
 out=[]
 for line in path.open(encoding='utf-8'):
  r=json.loads(line)
  if r.get('source_split') not in ('validation','test'):raise ValueError('split mismatch')
  r['_latest_user']=latest_user(r['context']);out.append(r)
 return out
def script_hint(text):
 # Script evidence is a direct Unicode property, not an embedding or learned model.
 if any('\u3040'<=c<='\u30ff' for c in text):return 'ja'
 if any('\uac00'<=c<='\ud7af' for c in text):return 'ko'
 if any('\u0e00'<=c<='\u0e7f' for c in text):return 'th'
 if any('\u0600'<=c<='\u06ff' for c in text):return 'ar'
 if any('\u0900'<=c<='\u097f' for c in text):return 'hi'
 if any('\u0400'<=c<='\u052f' for c in text):return None # distinguish ru/uk by TRAIN lexical counts
 han=any('\u4e00'<=c<='\u9fff' for c in text)
 if han:return 'zh'
 return None
def raw_prediction(priors,text,window=None,use_script=True,alpha=.5):
 all_toks=[t for t in tokenize(text) if len(t)>1 and any(c.isalpha() for c in t)]
 toks=all_toks[:window] if window else all_toks
 if not toks:return {'best':'global','margin':0.,'coverage':0.,'n_tokens':0,'script_hint':None}
 if use_script:
  hint=script_hint(text)
  if hint and hint in priors['languages']:
   return {'best':hint,'margin':999.,'coverage':1.,'n_tokens':len(toks),'script_hint':hint}
 tc=Counter(toks);gu=priors['global_last_user_unigrams'];gt=max(1,int(priors['global_last_user_token_count']));v=max(1,len(gu));gd=gt+alpha*(v+1);scores={}
 for lang,b in priors['languages'].items():
  uni=b['last_user_unigrams'];den=max(1,int(b['last_user_token_count']))+alpha*(v+1);ll=0.;matched=0
  for t,f in tc.items():
   c=int(uni.get(t,0));gc=int(gu.get(t,0));matched+=f if c else 0
   ll+=f*math.log(((c+alpha)/den)/((gc+alpha)/gd))
  scores[lang]={'score':ll/len(toks),'coverage':matched/len(toks)}
 order=sorted(scores,key=lambda l:(scores[l]['score'],l),reverse=True);best=order[0];second=order[1]
 return {'best':best,'margin':scores[best]['score']-scores[second]['score'],'coverage':scores[best]['coverage'],'n_tokens':len(toks),'script_hint':None}
def score_rows(rows,priors,window,use_script):
 out=[]
 for r in rows:
  out.append({'gold':r['lang'],'context_hash':hashlib.sha256(r['_latest_user'].encode()).hexdigest(),**raw_prediction(priors,r['_latest_user'],window,use_script)})
 return out
def dedup(rows):
 out={};conf=0
 for x in rows:
  old=out.get(x['context_hash'])
  if old:
   if old['gold']!=x['gold']:conf+=1
  else:out[x['context_hash']]=x
 return list(out.values()),conf
def summarize(rows,th):
 cm=defaultdict(Counter);routed=correct=0
 for x in rows:
  pred=x['best'] if x['n_tokens']>=th['min_tokens'] and x['coverage']>=th['min_coverage'] and x['margin']>=th['min_margin'] else 'global'
  cm[x['gold']][pred]+=1
  if pred!='global':routed+=1;correct+=int(pred==x['gold'])
 return {'examples':len(rows),'routed':routed,'coverage':routed/len(rows) if rows else 0.,'selective_accuracy':correct/routed if routed else 0.,'correctly_routed_fraction_all':correct/len(rows) if rows else 0.,'confusion':{k:dict(v) for k,v in cm.items()}}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['grid','fixed'],default='grid');ap.add_argument('--out',type=Path,default=ROOT/'Amodel_eSonde_v8/experiments/results/oasst1_language_route_latest_user_20261117.json');a=ap.parse_args()
 priors=json.loads(PRIORS.read_text());vr=read_rows(VALID);tr=read_rows(TEST);grid=[]
 if a.mode=='grid':
  for win in (4,8,12,16,24,32,None):
   for script in (False,True):
    v,_=dedup(score_rows(vr,priors,win,script))
    for nt in (1,2,3):
     for cov in (.05,.10,.20,.25,.35):
      for margin in (0.,.005,.015,.03,.06):
       th={'min_tokens':nt,'min_coverage':cov,'min_margin':margin};sm=summarize(v,th)
       if sm['coverage']>=.30:grid.append({'window':win,'script_override':script,'thresholds':th,'validation_unique':sm})
  grid.sort(key=lambda z:(z['validation_unique']['correctly_routed_fraction_all'],z['validation_unique']['selective_accuracy'],z['validation_unique']['coverage']),reverse=True)
  best=grid[0] if grid else None
  payload={'schema':'esonde.v8.latest_user_language_route_eval.v2','selection':'max correct-route fraction on unique VALIDATION contexts; tie-break selective accuracy and coverage','grid_top':grid[:25],'eligible_variants':len(grid),'best':best,'test_threshold_selection':'not used'}
 else:
  win=24;script=True;th={'min_tokens':1,'min_coverage':.05,'min_margin':.03}
  v,vc=dedup(score_rows(vr,priors,win,script));t,tc=dedup(score_rows(tr,priors,win,script))
  payload={'schema':'esonde.v8.latest_user_language_route_eval.v2','frozen_window_tokens':win,'script_override':script,'thresholds_frozen':th,'validation_unique':summarize(v,th),'test_unique':summarize(t,th),'validation_unique_contexts':len(v),'test_unique_contexts':len(t),'duplicate_label_conflicts_validation':vc,'duplicate_label_conflicts_test':tc}
 payload['priors_sha256']=hashlib.sha256(PRIORS.read_bytes()).hexdigest();payload['source_split_contract']='TRAIN language counts only; latest USER turn; validation tunes; TEST is held out'
 a.out.parent.mkdir(parents=True,exist_ok=True);tmp=a.out.with_suffix('.tmp');tmp.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n');tmp.replace(a.out)
 if a.mode=='grid':print(json.dumps({'output':str(a.out),'eligible_variants':len(grid),'best':{'window':best['window'],'script_override':best['script_override'],'thresholds':best['thresholds'],'metrics':{k:best['validation_unique'][k] for k in ('examples','coverage','selective_accuracy','correctly_routed_fraction_all')}} if best else None},ensure_ascii=False))
 else:print(json.dumps({'output':str(a.out),'validation':{k:payload['validation_unique'][k] for k in ('examples','coverage','selective_accuracy','correctly_routed_fraction_all')},'test':{k:payload['test_unique'][k] for k in ('examples','coverage','selective_accuracy','correctly_routed_fraction_all')}},ensure_ascii=False))
if __name__=='__main__':main()
