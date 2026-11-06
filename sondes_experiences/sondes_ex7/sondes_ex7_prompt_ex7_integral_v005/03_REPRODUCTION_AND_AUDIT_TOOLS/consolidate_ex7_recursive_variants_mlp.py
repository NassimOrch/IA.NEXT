#!/usr/bin/env python3
"""Append-only EX7 reprise: aggregate already completed runs with paired MLP controls.
No training is performed. Sources are read-only; outputs are new audit tables.
"""
from pathlib import Path
import json,csv,statistics,hashlib,sys,shutil
import numpy as np
V=Path('/mnt/data/sondes_research_workspace_ex7/versions/sondes_ex7_v001__2026-10-31')
OUT=Path('/mnt/data/EX7_V002_SUPPLEMENT'); OUT.mkdir(exist_ok=True)
RAW=V/'results/raw'; MET=V/'results/metrics'; EX6=V/'inputs/ex6_reference'
SEEDS=[1501,1607,1717,2029,3037]
def j(p): return json.loads(Path(p).read_text())
def writecsv(name,rows):
 if not rows: raise RuntimeError(f'no rows for {name}')
 fields=list(rows[0])
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def agg_num(vals): return statistics.mean(vals) if vals else None
def sd(vals): return statistics.stdev(vals) if len(vals)>1 else 0.0
# Structural compression variants paired to the family/seed EX6 MLP-ge4x comparator
struct_rows=[]
for family in ['emp_oof_corrector','orch_input_oof_corrector']:
 for seed in SEEDS:
  ref=j(EX6/'results_v3/raw'/f'{family}_seed{seed}_summary.json')
  mlp=ref['mlp_comparators']['ge4x']
  for variant in ['rbf_d1_k4','rbf_d2_k2','rbf_d1_k2','shared_centers_2heads','lowrank_context_r1','lowrank_context_r2']:
   tag=f'ex7_struct_{variant}_{family}_seed{seed}'
   r=j(RAW/f'{tag}_result.json'); v=r['validation']; P=int(r['P_total']); MP=int(mlp['counts']['P_total'])
   candidate_total=float(ref['oof_generation_seconds']+ref['base_fit_seconds']+ref['initialization_seconds']+r['corrector_fit_seconds'])
   mlp_total=float(mlp['pipeline_fit_seconds'])
   struct_rows.append({
    'family':family,'variant':variant,'seed':seed,
    'candidate_P_total':P,'MLP_ge4x_P_total':MP,'MLP_over_candidate_ratio':MP/P,
    'candidate_accuracy':v['accuracy'],'MLP_accuracy':mlp['validation']['accuracy'],'delta_accuracy_pp':100*(v['accuracy']-mlp['validation']['accuracy']),
    'candidate_log_loss':v['log_loss'],'MLP_log_loss':mlp['validation']['log_loss'],'relative_log_loss_change_pct':100*(v['log_loss']/mlp['validation']['log_loss']-1),
    'OOF_generation_seconds':ref['oof_generation_seconds'],'base_fit_seconds':ref['base_fit_seconds'],'initialization_seconds':ref['initialization_seconds'],
    'corrector_fit_seconds':r['corrector_fit_seconds'],'candidate_pipeline_seconds_including_initialization':candidate_total,
    'MLP_fit_pipeline_seconds':mlp_total,'training_slowdown_ratio':candidate_total/mlp_total,
    'candidate_checkpoint_bytes':r['checkpoint_bytes'],'MLP_checkpoint_bytes':mlp.get('checkpoint_bytes'),
    'candidate_checkpoint':r['checkpoint'],'MLP_comparator_source':'EX6 v003 paired per-seed summary, same Wisconsin split and seed',
    'test_opened':False})
# Aggregate structural table
struct_agg=[]
for family in ['emp_oof_corrector','orch_input_oof_corrector']:
 for variant in ['rbf_d1_k4','rbf_d2_k2','rbf_d1_k2','shared_centers_2heads','lowrank_context_r1','lowrank_context_r2']:
  rr=[r for r in struct_rows if r['family']==family and r['variant']==variant]
  def m(k): return statistics.mean(x[k] for x in rr)
  struct_agg.append({'family':family,'variant':variant,'n_seeds':len(rr),'candidate_P_total_mean':m('candidate_P_total'),'MLP_ge4x_P_total_mean':m('MLP_ge4x_P_total'),
   'ratio_mean':m('MLP_over_candidate_ratio'),'ratio_min':min(x['MLP_over_candidate_ratio'] for x in rr),
   'candidate_accuracy_mean':m('candidate_accuracy'),'MLP_accuracy_mean':m('MLP_accuracy'),'delta_accuracy_pp_mean':m('delta_accuracy_pp'),
   'candidate_log_loss_mean':m('candidate_log_loss'),'MLP_log_loss_mean':m('MLP_log_loss'),'relative_log_loss_change_pct_mean':m('relative_log_loss_change_pct'),
   'candidate_pipeline_seconds_mean':m('candidate_pipeline_seconds_including_initialization'),'MLP_fit_pipeline_seconds_mean':m('MLP_fit_pipeline_seconds'),
   'training_slowdown_ratio_mean':m('training_slowdown_ratio'),'candidate_checkpoint_bytes_mean':m('candidate_checkpoint_bytes'),
   'MLP_checkpoint_bytes_mean':None})
writecsv('EX7_STRUCTURAL_COMPRESSION_MLP_COMPARISONS_PER_SEED.csv',struct_rows)
writecsv('EX7_STRUCTURAL_COMPRESSION_MLP_COMPARISONS_AGGREGATES.csv',struct_agg)
# MLP rows used across Orchestra Org base/capacity arms when old MLP remains >=4x
mlp_rows=list(csv.DictReader((MET/'EX7_ORCHESTRA_ORG_MLP_GE4X_PER_SEED.csv').open()))
mlp_by_seed={int(x['seed']):x for x in mlp_rows}
if set(mlp_by_seed)!=set(SEEDS): raise RuntimeError('Org MLP per-seed comparator coverage mismatch')
cap_rows=[]
for variant in ['shallow_5x5','deep_9x5','latent_d2','centers_k4','latent_d2_centers_k4']:
 for seed in SEEDS:
  tag=f'orchestra_org_capacity_{variant}_seed{seed}'; r=j(RAW/f'{tag}_result.json'); fm=r.get('fresh_mlp_ge4x')
  if fm:
   MP=int(fm['P_total']); ma=float(fm['accuracy']); ml=float(fm['log_loss']); mt=float(fm['fit_seconds']); mb=int(fm['checkpoint_bytes']); mcp=fm['checkpoint']; source='fresh MLP-ge4x trained for this capacity/seed'
  else:
   mm=mlp_by_seed[seed]; MP=int(mm['MLP_P_total']); ma=float(mm['MLP_accuracy']); ml=float(mm['MLP_log_loss']); mt=float(mm['MLP_fit_seconds']); mb=int(mm['MLP_checkpoint_bytes']); mcp='results/models/orchestra_org_oof_rbf1_seed'+str(seed)+'_mlp_ge4x.pt'; source='reused EX7 paired MLP-ge4x: ratio rechecked >=4 for this candidate'
  P=int(r['counts']['P_total']); ratio=MP/P
  if ratio<4.0-1e-12: raise RuntimeError(f'MLP ratio below 4: {variant}/{seed}: {ratio}')
  v=r['validation']
  cap_rows.append({'variant':variant,'seed':seed,'n_layers':r['n_layers'],'latent_dimension':r['latent_dimension'],'centers_per_probe':r['centers_per_probe'],
   'candidate_P_total':P,'MLP_ge4x_P_total':MP,'MLP_over_candidate_ratio':ratio,
   'candidate_accuracy':v['accuracy'],'MLP_accuracy':ma,'delta_accuracy_pp':100*(v['accuracy']-ma),
   'candidate_log_loss':v['log_loss'],'MLP_log_loss':ml,'relative_log_loss_change_pct':100*(v['log_loss']/ml-1),
   'candidate_fit_seconds':r['fit_seconds'],'MLP_fit_seconds':mt,'training_slowdown_ratio':r['fit_seconds']/mt,
   'candidate_initialization_seconds':'NON_MESURE','MLP_initialization_seconds':'NON_MESURE',
   'candidate_checkpoint_bytes':r['checkpoint_bytes'],'MLP_checkpoint_bytes':mb,'MLP_comparator_source':source,
   'candidate_checkpoint':r['checkpoint'],'MLP_checkpoint':mcp,'test_opened':False})
cap_agg=[]
for variant in ['shallow_5x5','deep_9x5','latent_d2','centers_k4','latent_d2_centers_k4']:
 rr=[x for x in cap_rows if x['variant']==variant]
 def m(k): return statistics.mean(x[k] for x in rr)
 cap_agg.append({'variant':variant,'n_seeds':len(rr),'n_layers':rr[0]['n_layers'],'latent_dimension':rr[0]['latent_dimension'],'centers_per_probe':rr[0]['centers_per_probe'],
  'candidate_P_total_mean':m('candidate_P_total'),'MLP_ge4x_P_total_mean':m('MLP_ge4x_P_total'),'ratio_mean':m('MLP_over_candidate_ratio'),'ratio_min':min(x['MLP_over_candidate_ratio'] for x in rr),
  'candidate_accuracy_mean':m('candidate_accuracy'),'MLP_accuracy_mean':m('MLP_accuracy'),'delta_accuracy_pp_mean':m('delta_accuracy_pp'),
  'candidate_log_loss_mean':m('candidate_log_loss'),'MLP_log_loss_mean':m('MLP_log_loss'),'relative_log_loss_change_pct_mean':m('relative_log_loss_change_pct'),
  'candidate_fit_seconds_mean':m('candidate_fit_seconds'),'MLP_fit_seconds_mean':m('MLP_fit_seconds'),'training_slowdown_ratio_mean':m('training_slowdown_ratio'),
  'MLP_comparator_strategy':'fresh per-seed MLP for deep_9x5; otherwise reused paired MLP after verifying ratio >=4'})
writecsv('EX7_ORCHESTRA_ORG_CAPACITY_MLP_COMPARISONS_PER_SEED.csv',cap_rows)
writecsv('EX7_ORCHESTRA_ORG_CAPACITY_MLP_COMPARISONS_AGGREGATES.csv',cap_agg)
# Separate root seed rows from fold fits, fix the interpretation of legacy mixed table
root_rows=[]; fold_rows=[]
for seed in SEEDS:
 tag=f'orchestra_org_recursive_7x5_seed{seed}_cascade'; r=j(RAW/f'{tag}_result.json')
 root_rows.append({'seed':seed,'n_layers':r['n_layers'],'probes_per_layer':r['probes_per_layer'],'P_total':r['counts']['P_total'],'accuracy':r['validation']['accuracy'],'log_loss':r['validation']['log_loss'],'fit_seconds':r['fit_seconds'],'fit_epochs':r['fit_epochs'],'best_epoch':r['best_epoch'],'checkpoint':r['checkpoint'],'checkpoint_sha256':r['checkpoint_sha256'],'test_opened':False})
oofstatus=j(MET/'EX7_ORCHESTRA_ORG_OOF_STATUS.json')
for e in oofstatus['results']:
 for f in e['oof_folds']:
  fold_rows.append({'outer_seed':e['seed'],'fold':f['fold'],'fold_seed':f['fold_seed'],'n_outer_train':f['n_outer_train'],'n_oof':f['n_oof'],'n_inner_fit':f['n_inner_fit'],'n_inner_stop':f['n_inner_stop'],'fit_seconds':f['fit_seconds'],'predict_seconds':f['predict_seconds'],'checkpoint':f['checkpoint'],'checkpoint_sha256':f['checkpoint_sha256'],'oof_indices_sha256':f['oof_indices_sha256'],'test_opened':False})
writecsv('EX7_ORCHESTRA_ORG_ROOT_SEEDS_ONLY.csv',root_rows)
writecsv('EX7_ORCHESTRA_ORG_OOF_FOLD_MODELS_ONLY.csv',fold_rows)
# Corrector OOF (3-fold) all variants compared to the same paired MLP per seed
org_oof_rows=[]
for e in oofstatus['results']:
 mm=mlp_by_seed[int(e['seed'])]
 for v in e['variants']:
  P=v['counts']['P_total']; MP=int(mm['MLP_P_total']); q=v['validation']
  total=e['oof_generation_seconds']+e['base_fit_seconds_historical']+v['corrector_fit_seconds']
  org_oof_rows.append({'seed':e['seed'],'variant':v['variant'],'candidate_P_total':P,'MLP_ge4x_P_total':MP,'MLP_over_candidate_ratio':MP/P,
   'candidate_accuracy':q['accuracy'],'MLP_accuracy':float(mm['MLP_accuracy']),'delta_accuracy_pp':100*(q['accuracy']-float(mm['MLP_accuracy'])),
   'candidate_log_loss':q['log_loss'],'MLP_log_loss':float(mm['MLP_log_loss']),'relative_log_loss_change_pct':100*(q['log_loss']/float(mm['MLP_log_loss'])-1),
   'OOF_generation_seconds':e['oof_generation_seconds'],'base_fit_seconds':e['base_fit_seconds_historical'],'corrector_fit_seconds':v['corrector_fit_seconds'],
   'candidate_pipeline_seconds':total,'MLP_fit_seconds':float(mm['MLP_fit_seconds']),'training_slowdown_ratio':total/float(mm['MLP_fit_seconds']),'test_opened':False})
org_oof_agg=[]
for variant in ['temp_bias','linear_context','rbf_lite_1probe']:
 rr=[r for r in org_oof_rows if r['variant']==variant]
 def m(k):return statistics.mean(x[k] for x in rr)
 org_oof_agg.append({'variant':variant,'n_seeds':len(rr),'candidate_P_total_mean':m('candidate_P_total'),'MLP_ge4x_P_total_mean':m('MLP_ge4x_P_total'),'ratio_mean':m('MLP_over_candidate_ratio'),'ratio_min':min(x['MLP_over_candidate_ratio'] for x in rr),
  'candidate_accuracy_mean':m('candidate_accuracy'),'MLP_accuracy_mean':m('MLP_accuracy'),'delta_accuracy_pp_mean':m('delta_accuracy_pp'),'candidate_log_loss_mean':m('candidate_log_loss'),'MLP_log_loss_mean':m('MLP_log_loss'),
  'relative_log_loss_change_pct_mean':m('relative_log_loss_change_pct'),'candidate_pipeline_seconds_mean':m('candidate_pipeline_seconds'),'MLP_fit_seconds_mean':m('MLP_fit_seconds'),'training_slowdown_ratio_mean':m('training_slowdown_ratio')})
writecsv('EX7_ORCHESTRA_ORG_OOF_MLP_COMPARISONS_PER_SEED.csv',org_oof_rows)
writecsv('EX7_ORCHESTRA_ORG_OOF_MLP_COMPARISONS_AGGREGATES.csv',org_oof_agg)
# Copy the independent integrity audit
shutil.copy2('/mnt/data/EX7_RECURSIVE_VARIANTS_AUDIT.json',OUT/'EX7_RECURSIVE_VARIANTS_AUDIT.json')
# Small verification receipt with counts and input hashes
checks=json.load(open('/mnt/data/EX7_RECURSIVE_VARIANTS_AUDIT.json'))['checks']
receipt={'outputs':sorted(p.name for p in OUT.iterdir()),'recursive_root_runs':checks['recursive_root_seed_runs'],'recursive_oof_outer_seeds':checks['recursive_oof_seed_runs'],'recursive_fold_models':checks['recursive_oof_fold_models'],'capacity_runs':checks['capacity_runs'],'structural_runs':checks['structural_runs'],
 'all_mlp_parameter_ratios_ge4':all(float(r['MLP_over_candidate_ratio'])>=4 for r in struct_rows+cap_rows+org_oof_rows),
 'test_opened':False,'method':'Append-only, no training reruns; reaggregated already completed outputs paired by family/seed and validated checkpoint hashes/OOF indices.'}
(OUT/'EX7_V002_RECONSOLIDATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
