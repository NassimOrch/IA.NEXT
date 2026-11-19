#!/usr/bin/env python3
"""Build TRAIN-only language priors for eSonde v8 chat.

The language identifier is trained only from the latest USER turn in each
available dialogue context, not from assistant history. Response-start and
response-vocabulary counts remain role-conditioned on the paired assistant
response. Only aggregate token counts are stored; no raw conversation is saved.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import hashlib, json, re
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Dmodel_eSonde_v8'/'src'))
from esonde_v6.features import tokenize, FEATURE_VERSION
TRAIN=ROOT/'derived'/'OASST1_chat'/'train.jsonl'
MANIFEST=ROOT/'derived'/'OASST1_chat'/'dataset_manifest.json'
PROFILE=ROOT/'Dmodel_eSonde_v8'/'models'/'eSonde_v8'/'dialogue_profiles.json'
OUT=ROOT/'Dmodel_eSonde_v8'/'models'/'eSonde_v8'/'response_language_priors.json'
ROLE=re.compile(r'(?m)(?:^|\n)(USER|ASSISTANT):\s*')
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def latest_user_turn(text):
    text=str(text or '')
    matches=list(ROLE.finditer(text))
    if not matches: return text, False
    for i in range(len(matches)-1,-1,-1):
        if matches[i].group(1)=='USER':
            start=matches[i].end(); end=matches[i+1].start() if i+1<len(matches) else len(text)
            return text[start:end].strip(), True
    return text, False
def main():
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    meta=manifest['derived_splits']['train']
    if sha(TRAIN)!=meta['sha256'] or TRAIN.stat().st_size!=meta['bytes']:
        raise SystemExit('TRAIN split hash/size mismatch')
    langs=defaultdict(lambda:{'examples':0,'last_user_unigrams':Counter(),
        'response_unigrams':Counter(),'response_starts':Counter(),
        'last_user_token_count':0,'response_token_count':0})
    global_starts=Counter(); global_last_user=Counter(); rows=usable=parsed=0
    for line in TRAIN.open(encoding='utf-8'):
        r=json.loads(line); rows+=1
        if r.get('source_split')!='train': raise ValueError('non-TRAIN data encountered')
        context=str(r.get('context','')); response=str(r.get('response',''))
        if not context.strip() or not response.strip(): continue
        user_text, parsed_role=latest_user_turn(context); parsed+=int(parsed_role)
        ctx=[t for t in tokenize(user_text) if t!='<empty>']
        rsp=[t for t in tokenize(response) if t!='<empty>']
        if not rsp: continue
        lang=str(r.get('lang') or 'und'); b=langs[lang]
        b['examples']+=1; usable+=1
        b['last_user_unigrams'].update(ctx); global_last_user.update(ctx)
        b['response_unigrams'].update(rsp); b['response_starts'][rsp[0]]+=1
        b['last_user_token_count']+=len(ctx); b['response_token_count']+=len(rsp)
        global_starts[rsp[0]]+=1
    profile=json.loads(PROFILE.read_text(encoding='utf-8'))['profiles']['everyday_dialogue']
    stored=profile['response_starts']
    mismatch={k:{'derived':global_starts.get(k,0),'profile':v} for k,v in stored.items() if global_starts.get(k,0)!=int(v)}
    if mismatch: raise SystemExit(f'response-start count mismatch: {list(mismatch.items())[:5]}')
    payload={'schema':'esonde.v8.oasst1_language_priors.v2','dataset':'OpenAssistant/oasst1',
      'revision':manifest['revision'],'source_split':'derived_train_only',
      'source_train_jsonl_sha256':meta['sha256'],'source_train_manifest_sha256':sha(MANIFEST),
      'tokenizer_feature_version':FEATURE_VERSION,'training_examples':usable,
      'language_evidence_field':'latest_USER_turn_only','latest_user_turns_parsed':parsed,
      'global_last_user_token_count':sum(global_last_user.values()),
      'global_last_user_unigrams':dict(sorted(global_last_user.items())),
      'languages':{},'aggregate_response_starts_crosscheck':{'profile_top256_matches':True,
      'profile_top256_count':len(stored),'derived_total_start_count':sum(global_starts.values())},
      'neural_components':[],'raw_prompt_response_storage':False,
      'purpose':'prompt-only language identification; language-conditioned proposal vocabulary and assistant response-start priors'}
    for lang,b in sorted(langs.items()):
        payload['languages'][lang]={'examples':b['examples'],
          'last_user_token_count':b['last_user_token_count'],
          'last_user_unigrams':dict(sorted(b['last_user_unigrams'].items())),
          'response_token_count':b['response_token_count'],
          'response_unigrams':dict(sorted(b['response_unigrams'].items())),
          'response_starts':dict(sorted(b['response_starts'].items(),key=lambda x:(-x[1],x[0])))}
    tmp=OUT.with_suffix('.json.tmp'); tmp.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8'); tmp.replace(OUT)
    print(json.dumps({'status':'BUILT','output':str(OUT),'bytes':OUT.stat().st_size,'sha256':sha(OUT),
      'train_rows':rows,'usable_examples':usable,'latest_user_turns_parsed':parsed,
      'languages':{l:{'examples':v['examples'],'last_user_vocab':len(v['last_user_unigrams']),
      'response_vocab':len(v['response_unigrams']),'starts':v['response_starts'].most_common(8)} for l,v in sorted(langs.items())},
      'aggregate_response_starts_match':True},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
