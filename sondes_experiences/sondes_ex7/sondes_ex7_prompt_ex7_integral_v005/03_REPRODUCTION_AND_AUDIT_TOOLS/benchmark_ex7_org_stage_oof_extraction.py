from pathlib import Path
import os,sys,time,json,hashlib,csv
import numpy as np, torch
from sklearn.model_selection import StratifiedKFold,train_test_split
V=Path('/mnt/data/sondes_research_workspace_ex7/versions/sondes_ex7_v001__2026-10-31')
os.environ['EX7_EX6_REFERENCE']=str(V/'inputs'/'ex6_reference')
sys.path.insert(0,str(V/'src'))
from run_orchestra_org_recursive import OrchestraOrg,CONFIGS,load_data,tensor_x,MODELS,RAW

torch.set_num_threads(1); torch.set_num_interop_threads(1)
data=load_data(); X=np.asarray(data['Xtr'],np.float32); y=np.asarray(data['ytr'],np.int64)
rows=[]
for seed in [1501,1607,1717,2029,3037]:
    saved=np.load(RAW/f'orchestra_org_oof_seed{seed}_stage_logits.npz',allow_pickle=False)['oof_stage_logits']
    allout=np.zeros_like(saved); skf=StratifiedKFold(n_splits=3,shuffle=True,random_state=seed+5291)
    t_all=time.perf_counter(); breakdown=[]; fold_ids=[]
    for fi,(itr,ioof) in enumerate(skf.split(X,y)):
        t0=time.perf_counter(); fold_seed=100000+seed*10+fi
        ifit,istop=train_test_split(np.arange(len(itr)),test_size=.20,random_state=fold_seed+7001,stratify=y[itr])
        Xfit=X[itr][ifit]
        model=OrchestraOrg(Xfit,CONFIGS,fold_seed,cascade=True)
        t_construct=time.perf_counter()-t0
        ckpath=MODELS/f'orchestra_org_recursive_7x5_seed{fold_seed}_cascade_checkpoint.pt'
        t1=time.perf_counter(); ck=torch.load(ckpath,map_location='cpu',weights_only=False); model.load_state_dict(ck['model_state']); model.eval()
        t_load=time.perf_counter()-t1
        t2=time.perf_counter()
        with torch.no_grad():
            _,hs=model.layer_inputs(tensor_x(X[ioof]),vectorized=True)
            logits=np.stack([h.cpu().numpy() for h in hs],axis=1)
        t_inf=time.perf_counter()-t2
        allout[ioof]=logits; fold_ids.extend(ioof.tolist())
        breakdown.append({'fold':fi,'n_oof':int(len(ioof)),'construct_seconds':t_construct,'load_seconds':t_load,'forward_seconds':t_inf,'fold_total_seconds':t_construct+t_load+t_inf})
    total=time.perf_counter()-t_all
    diff=float(np.max(np.abs(allout-saved)))
    if diff>1e-6: raise RuntimeError(f'seed {seed} stage-logit parity error {diff}')
    rows.append({'seed':seed,'n_folds':3,'n_train':len(y),'stage_oof_logits_extraction_seconds':total,
                 'construct_seconds_sum':sum(x['construct_seconds'] for x in breakdown),'checkpoint_load_seconds_sum':sum(x['load_seconds'] for x in breakdown),
                 'forward_seconds_sum':sum(x['forward_seconds'] for x in breakdown),'max_abs_difference_vs_saved_stage_logits':diff,
                 'saved_stage_logits_sha256':hashlib.sha256(saved.tobytes()).hexdigest(),'recomputed_stage_logits_sha256':hashlib.sha256(allout.tobytes()).hexdigest(),
                 'folds':json.dumps(breakdown,separators=(',',':')),'test_opened':False})
    print('TIMED_STAGE_OOF',seed,round(total,4),'sec','parity',diff,flush=True)
# persist in both top and V2 eventually
out=Path('/mnt/data/EX7_V002_SUPPLEMENT/EX7_ORCHESTRA_ORG_STAGE_OOF_EXTRACTION_TIMING.csv')
with out.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('MEAN_STAGE_EXTRACTION_SECONDS',sum(r['stage_oof_logits_extraction_seconds'] for r in rows)/len(rows))
