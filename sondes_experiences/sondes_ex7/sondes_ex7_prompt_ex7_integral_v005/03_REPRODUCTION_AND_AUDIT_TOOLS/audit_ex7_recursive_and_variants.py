import os, json, csv, hashlib, zipfile, math, statistics, sys
from pathlib import Path
import numpy as np
import torch
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import accuracy_score, log_loss
V=Path('/mnt/data/sondes_research_workspace_ex7/versions/sondes_ex7_v001__2026-10-31')
sys.path.insert(0,str(V/'inputs/ex6_reference'/'src'))
from ex6_common import calc_metrics
RAW=V/'results/raw'; MODELS=V/'results/models'; MET=V/'results/metrics'; EX6=V/'inputs/ex6_reference'
SEEDS=[1501,1607,1717,2029,3037]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def loadj(p): return json.loads(Path(p).read_text())
errors=[]; warnings=[]; checks={}
# Integrity core datasets
npz=np.load(EX6/'inputs/data_manifest/wisconsin_dev_only_v002.npz',allow_pickle=False)
checks['data_arrays']={k:{'shape':list(npz[k].shape),'dtype':str(npz[k].dtype),'finite':bool(np.isfinite(npz[k]).all()) if np.issubdtype(npz[k].dtype,np.number) else None} for k in npz.files}
X=np.asarray(npz['Xtr']); y=np.asarray(npz['ytr']); Xva=np.asarray(npz['Xva']); yva=np.asarray(npz['yva'])
checks['data_sha256']=sha(EX6/'inputs/data_manifest/wisconsin_dev_only_v002.npz')
# Recursive root training: separate root seeds vs OOF fold seeds
root_rows=[]; fold_rows=[]; loaded_ck=0
for seed in SEEDS:
 tag=f'orchestra_org_recursive_7x5_seed{seed}_cascade'
 rp=RAW/f'{tag}_result.json'; cp=MODELS/f'{tag}_checkpoint.pt'; pp=RAW/f'{tag}_predictions.json'
 if not (rp.exists() and cp.exists() and pp.exists()): errors.append(f'missing root Org seed artifacts {seed}'); continue
 r=loadj(rp); ck=torch.load(cp,map_location='cpu',weights_only=False); loaded_ck+=1
 if r.get('status')!='COMPLETE': errors.append(f'root seed {seed} status not complete')
 if r.get('n_layers')!=7 or r.get('probes_per_layer')!=5: errors.append(f'root seed {seed} topology mismatch')
 if r.get('checkpoint_sha256')!=sha(cp): errors.append(f'root seed {seed} checkpoint hash mismatch')
 if len(ck['model_state']['outer_logits'])!=7: errors.append(f'root seed {seed} missing outer coordination')
 # Verify saved output matches recorded validation metrics
 pred=loadj(pp); probs=np.asarray(pred['probabilities']); yy=np.asarray(pred['y_true'])
 if probs.shape!=(len(yva),2) or not np.isfinite(probs).all(): errors.append(f'root prediction shape/nonfinite {seed}')
 else:
  mm=calc_metrics(yy,probs); acc=mm['accuracy']; ll=mm['log_loss']
  if abs(acc-r['validation']['accuracy'])>1e-12 or abs(ll-r['validation']['log_loss'])>1e-9: errors.append(f'root metric/prediction mismatch {seed}')
 root_rows.append({'seed':seed,'P_total':r['counts']['P_total'],'accuracy':r['validation']['accuracy'],'log_loss':r['validation']['log_loss'],'fit_seconds':r['fit_seconds'],'epochs':r['fit_epochs'],'checkpoint':str(cp.relative_to(V)),'checkpoint_sha256':sha(cp)})
# Cross-fitting validation: 5 seeds x 3 folds, strict coverage/indices hash/ckpt hashes/Oof logits
OOF=loadj(MET/'EX7_ORCHESTRA_ORG_OOF_STATUS.json')
if OOF.get('n_completed')!=5 or OOF.get('expected')!=5: errors.append('Orchestra Org OOF status not 5/5')
oof_rows=[]; fold_index_rows=[]; corrector_loads=0
for entry in OOF['results']:
 seed=int(entry['seed']);
 if entry.get('status')!='COMPLETE' or len(entry.get('oof_folds',[]))!=3: errors.append(f'OOF incomplete seed {seed}')
 skf=StratifiedKFold(n_splits=3,shuffle=True,random_state=seed+5291)
 coverage=np.zeros(len(y),dtype=np.int8); fold_meta={f['fold']:f for f in entry['oof_folds']}
 for fi,(itr,ioof) in enumerate(skf.split(X,y)):
  coverage[ioof]+=1
  f=fold_meta.get(fi)
  if f is None: errors.append(f'missing fold metadata seed {seed} fold {fi}'); continue
  digest=hashlib.sha256(np.asarray(ioof,dtype=np.int64).tobytes()).hexdigest()
  if digest!=f['oof_indices_sha256']: errors.append(f'OOF index hash mismatch seed {seed} fold {fi}')
  if f['n_oof']!=len(ioof) or f['n_outer_train']!=len(itr): errors.append(f'fold size mismatch seed {seed} fold {fi}')
  fold_seed=int(f['fold_seed']); ifit,istop=train_test_split(np.arange(len(itr)),test_size=.20,random_state=fold_seed+7001,stratify=y[itr])
  if len(ifit)!=f['n_inner_fit'] or len(istop)!=f['n_inner_stop']: errors.append(f'inner split mismatch seed {seed} fold {fi}')
  fcp=V/f['checkpoint']
  if not fcp.exists() or sha(fcp)!=f['checkpoint_sha256']: errors.append(f'fold checkpoint hash/missing seed {seed} fold {fi}')
  else:
   c=torch.load(fcp,map_location='cpu',weights_only=False); loaded_ck+=1
   if len(c['model_state']['outer_logits'])!=7: errors.append(f'fold checkpoint outer gate missing {seed} fold {fi}')
  fold_rows.append({'outer_seed':seed,'fold':fi,'fold_seed':fold_seed,'n_outer_train':len(itr),'n_oof':len(ioof),'n_inner_fit':len(ifit),'n_inner_stop':len(istop),'fit_seconds':f['fit_seconds'],'predict_seconds':f['predict_seconds'],'checkpoint':str(fcp.relative_to(V)),'checkpoint_sha256':sha(fcp) if fcp.exists() else ''})
 if not np.all(coverage==1): errors.append(f'OOF coverage not exactly once for seed {seed}: {np.unique(coverage,return_counts=True)}')
 oofp=MODELS/f'orchestra_org_oof_seed{seed}_oof_logits.pt'
 if not oofp.exists(): errors.append(f'missing oof logits seed {seed}')
 else:
  oq=torch.load(oofp,map_location='cpu',weights_only=False); zz=np.asarray(oq['oof_train_logits'])
  if zz.shape!=(len(y),2) or not np.isfinite(zz).all(): errors.append(f'OOF logits shape/nonfinite seed {seed}')
  if len(oq.get('folds',[]))!=3: errors.append(f'OOF logits fold count seed {seed}')
 # corrector variants
 for v in entry.get('variants',[]):
  cp=V/v['checkpoint']; pp=V/v['predictions']
  if not cp.exists() or not pp.exists(): errors.append(f'missing corrector artifacts seed {seed} {v["variant"]}'); continue
  if sha(cp)!=v['checkpoint_sha256'] or sha(pp)!=v['predictions_sha256']: errors.append(f'corrector hash mismatch seed {seed} {v["variant"]}')
  q=torch.load(cp,map_location='cpu',weights_only=False); corrector_loads+=1
  pr=loadj(pp); prob=np.asarray(pr['probabilities']); yy=np.asarray(pr['y_true'])
  if prob.shape!=(len(yva),2) or not np.isfinite(prob).all(): errors.append(f'corrector probs shape/nonfinite seed {seed} {v["variant"]}')
  else:
   mm=calc_metrics(yy,prob); acc=mm['accuracy']; ll=mm['log_loss']
   if abs(acc-v['validation']['accuracy'])>1e-12 or abs(ll-v['validation']['log_loss'])>1e-9: errors.append(f'corrector metric mismatch seed {seed} {v["variant"]}')
   oof_rows.append({'seed':seed,'variant':v['variant'],'P_total':v['counts']['P_total'],'accuracy':acc,'log_loss':ll,'oof_generation_seconds':entry['oof_generation_seconds'],'base_fit_seconds':entry['base_fit_seconds_historical'],'corrector_fit_seconds':v['corrector_fit_seconds'],'pipeline_seconds':entry['oof_generation_seconds']+entry['base_fit_seconds_historical']+v['corrector_fit_seconds']})
# Capacity: check all expected raw+checkpoint and collect rows
capacity=[]; capmlp_loaded=0
variants=['shallow_5x5','deep_9x5','latent_d2','centers_k4','latent_d2_centers_k4']
for vn in variants:
 for seed in SEEDS:
  tag=f'orchestra_org_capacity_{vn}_seed{seed}'
  rp=RAW/f'{tag}_result.json'
  if not rp.exists(): errors.append(f'missing capacity run {vn}/{seed}'); continue
  r=loadj(rp); cp=V/r['checkpoint']
  if not cp.exists(): errors.append(f'missing capacity ckpt {vn}/{seed}'); continue
  c=torch.load(cp,map_location='cpu',weights_only=False); loaded_ck+=1
  if sha(cp)!=r.get('checkpoint_sha256'): errors.append(f'capacity checkpoint hash mismatch {vn}/{seed}')
  if r.get('capacity_variant')!=vn: errors.append(f'capacity variant metadata mismatch {vn}/{seed}')
  fm=r.get('fresh_mlp_ge4x')
  if fm:
   mcp=V/fm['checkpoint']
   if not mcp.exists(): errors.append(f'missing fresh mlp checkpoint {vn}/{seed}')
   else: torch.load(mcp,map_location='cpu',weights_only=False);capmlp_loaded+=1;loaded_ck+=1
  capacity.append({'seed':seed,'variant':vn,'P_total':r['counts']['P_total'],'accuracy':r['validation']['accuracy'],'log_loss':r['validation']['log_loss'],'fit_seconds':r['fit_seconds'],'fresh_mlp':fm,'existing_ratio':r.get('existing_org_mlp_ge4x_reusable_ratio'),'checkpoint':str(cp.relative_to(V)),'checkpoint_sha256':sha(cp)})
# Structural: 2 families x 6 variants x 5 seeds
struct=[]; structural_variants=['rbf_d1_k4','rbf_d2_k2','rbf_d1_k2','shared_centers_2heads','lowrank_context_r1','lowrank_context_r2']
for fam in ['emp_oof_corrector','orch_input_oof_corrector']:
 for vn in structural_variants:
  for seed in SEEDS:
   rp=RAW/f'ex7_struct_{vn}_{fam}_seed{seed}_result.json'
   if not rp.exists(): errors.append(f'missing structural run {fam}/{vn}/{seed}'); continue
   r=loadj(rp); cp=V/r['checkpoint']
   if not cp.exists(): errors.append(f'missing structural ckpt {fam}/{vn}/{seed}'); continue
   torch.load(cp,map_location='cpu',weights_only=False); loaded_ck+=1
   if sha(cp)!=hashlib.sha256(cp.read_bytes()).hexdigest(): errors.append(f'structural checksum internal failure {fam}/{vn}/{seed}')
   struct.append({'seed':seed,'family':fam,'variant':vn,'P_total':r['P_total'],'accuracy':r['validation']['accuracy'],'log_loss':r['validation']['log_loss'],'corrector_fit_seconds':r['corrector_fit_seconds'],'pipeline_seconds_reconstructed':r['pipeline_seconds_reconstructed'],'checkpoint_bytes':r['checkpoint_bytes'],'checkpoint':str(cp.relative_to(V)),'checkpoint_sha256':sha(cp)})
# Status matrix
checks.update({'recursive_root_seed_runs':len(root_rows),'recursive_oof_seed_runs':len([x for x in OOF['results'] if x['status']=='COMPLETE']),'recursive_oof_fold_models':len(fold_rows),'recursive_corrector_models_loaded':corrector_loads,'recursive_root_and_fold_checkpoints_loaded':loaded_ck,'capacity_runs':len(capacity),'capacity_fresh_mlps_loaded':capmlp_loaded,'structural_runs':len(struct),'oof_rows':len(oof_rows),'errors':errors,'warnings':warnings})
# Output audit bundle into /mnt/data for use by aggregator
out={'checks':checks,'root_rows':root_rows,'fold_rows':fold_rows,'oof_rows':oof_rows,'capacity_rows':capacity,'structural_rows':struct}
Path('/mnt/data/EX7_RECURSIVE_VARIANTS_AUDIT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps(checks,indent=2,ensure_ascii=False))
if errors: sys.exit(2)
