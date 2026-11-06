from pathlib import Path
import pandas as pd, numpy as np, json
V=Path('/mnt/data/sondes_research_workspace_ex7/versions/sondes_ex7_v001__2026-10-31/results/metrics')
O=Path('/mnt/data/EX7_V002_SUPPLEMENT')
mlp=pd.read_csv(V/'EX7_ORCHESTRA_ORG_MLP_GE4X_PER_SEED.csv')
assert mlp.seed.nunique()==5 and (mlp.MLP_P_total>0).all()
mlp=mlp[['seed','MLP_P_total','MLP_accuracy','MLP_log_loss','MLP_fit_seconds','MLP_checkpoint_bytes']].drop_duplicates('seed')
assert len(mlp)==5

def paired(df, group_col, name, time_col, pipeline_col=None):
    d=df.merge(mlp,on='seed',how='left',validate='many_to_one')
    d['ratio_MLP_over_candidate']=d.MLP_P_total/d.P_total
    d['accuracy_delta_pp']=(d.accuracy-d.MLP_accuracy)*100
    d['log_loss_delta_pct_vs_MLP']=(d.log_loss/d.MLP_log_loss-1)*100
    d['log_loss_delta_abs_vs_MLP']=d.log_loss-d.MLP_log_loss
    d['candidate_fit_or_pipeline_seconds']=d[pipeline_col] if pipeline_col else d[time_col]
    d['training_slowdown_vs_MLP']=d.candidate_fit_or_pipeline_seconds/d.MLP_fit_seconds
    d['comparator_scope']='same_seed EX7 Orchestra Org MLP-ge4x'
    d['test_opened']=False
    cols=[group_col,'seed','P_total','MLP_P_total','ratio_MLP_over_candidate','accuracy','MLP_accuracy','accuracy_delta_pp','log_loss','MLP_log_loss','log_loss_delta_abs_vs_MLP','log_loss_delta_pct_vs_MLP',time_col]
    if pipeline_col and pipeline_col!=time_col: cols.append(pipeline_col)
    cols += ['MLP_fit_seconds','candidate_fit_or_pipeline_seconds','training_slowdown_vs_MLP','comparator_scope','test_opened']
    return d, d[cols]

def agg(d,group_col):
    rows=[]
    for k,g in d.groupby(group_col,sort=True):
        rows.append({group_col:k,'n_seeds':len(g),'P_total_mean':g.P_total.mean(),'MLP_P_total_mean':g.MLP_P_total.mean(),'ratio_mean':g.ratio_MLP_over_candidate.mean(),'ratio_min':g.ratio_MLP_over_candidate.min(),'accuracy_mean':g.accuracy.mean(),'accuracy_sd':g.accuracy.std(ddof=1),'MLP_accuracy_mean':g.MLP_accuracy.mean(),'accuracy_delta_pp_mean':g.accuracy_delta_pp.mean(),'log_loss_mean':g.log_loss.mean(),'log_loss_sd':g.log_loss.std(ddof=1),'MLP_log_loss_mean':g.MLP_log_loss.mean(),'log_loss_delta_abs_mean':g.log_loss_delta_abs_vs_MLP.mean(),'log_loss_delta_pct_mean':g.log_loss_delta_pct_vs_MLP.mean(),'candidate_fit_or_pipeline_seconds_mean':g.candidate_fit_or_pipeline_seconds.mean(),'MLP_fit_seconds_mean':g.MLP_fit_seconds.mean(),'training_slowdown_mean':g.training_slowdown_vs_MLP.mean(),'all_ratios_ge4':bool((g.ratio_MLP_over_candidate>=4).all())})
    return pd.DataFrame(rows)

# Ablation runs: direct base training time, no OOF generation in this comparison.
a=pd.read_csv(V/'EX7_ORCHESTRA_ORG_ABLATIONS_PER_SEED.csv')
assert len(a)==30 and a.ablation.nunique()==6
ad,aper=paired(a,'ablation','ablation','fit_seconds')
aper.to_csv(O/'EX7_ORCHESTRA_ORG_ABLATIONS_MLP_COMPARISONS_PER_SEED.csv',index=False)
agg(ad,'ablation').to_csv(O/'EX7_ORCHESTRA_ORG_ABLATIONS_MLP_COMPARISONS_AGGREGATES.csv',index=False)

# Stage OOF: reconstruct whole production pipeline by adding OOF generation, base fit and corrector fit.
s=pd.read_csv(V/'EX7_ORCHESTRA_ORG_STAGE_OOF_PER_SEED.csv')
oof=pd.read_csv(V/'EX7_ORCHESTRA_ORG_OOF_PER_SEED.csv')
base=oof[oof.variant=='rbf_lite_1probe'][['seed','oof_generation_seconds','base_fit_seconds']].drop_duplicates('seed')
stage_timing=pd.read_csv(O/'EX7_ORCHESTRA_ORG_STAGE_OOF_EXTRACTION_TIMING.csv')[['seed','stage_oof_logits_extraction_seconds','max_abs_difference_vs_saved_stage_logits']]
s=s.merge(base,on='seed',how='left',validate='many_to_one').merge(stage_timing,on='seed',how='left',validate='many_to_one')
s['pipeline_seconds_reconstructed']=s.oof_generation_seconds+s.base_fit_seconds+s.stage_oof_logits_extraction_seconds+s.corrector_fit_seconds
sd,sper=paired(s,'variant','variant','corrector_fit_seconds','pipeline_seconds_reconstructed')
sper=sper.copy()
sper['oof_generation_seconds']=s.oof_generation_seconds
sper['base_fit_seconds']=s.base_fit_seconds
sper['stage_oof_logits_extraction_seconds']=s.stage_oof_logits_extraction_seconds
sper['stage_logits_parity_max_abs']=s.max_abs_difference_vs_saved_stage_logits
sper.to_csv(O/'EX7_ORCHESTRA_ORG_STAGE_OOF_MLP_COMPARISONS_PER_SEED.csv',index=False)
agg(sd,'variant').to_csv(O/'EX7_ORCHESTRA_ORG_STAGE_OOF_MLP_COMPARISONS_AGGREGATES.csv',index=False)

# Root recursive model, without OOF correction.
r=pd.read_csv(V/'EX7_ORCHESTRA_ORG_PER_SEED.csv')
r['variant']='recursive_org_base_only'
r['P_total']=r.P_total
r['fit_seconds']=r.fit_seconds
rd,rper=paired(r,'variant','variant','fit_seconds')
rper.to_csv(O/'EX7_ORCHESTRA_ORG_BASE_MLP_COMPARISONS_PER_SEED.csv',index=False)
agg(rd,'variant').to_csv(O/'EX7_ORCHESTRA_ORG_BASE_MLP_COMPARISONS_AGGREGATES.csv',index=False)

# combined machine-readable audit
summary={
 'ablations':{'rows':len(a),'arms':int(a.ablation.nunique()),'seeds_per_arm':a.groupby('ablation').seed.nunique().to_dict()},
 'stage_oof':{'rows':len(s),'arms':int(s.variant.nunique()),'seeds_per_arm':s.groupby('variant').seed.nunique().to_dict(),'oof_generation_in_pipeline':True,'stage_logits_extra_extraction_included':True,'stage_logits_extra_extraction_mean_seconds':float(stage_timing.stage_oof_logits_extraction_seconds.mean()),'stage_logits_parity_max_abs':float(stage_timing.max_abs_difference_vs_saved_stage_logits.max())},
 'recursive_base':{'rows':len(r),'seeds':int(r.seed.nunique())},
 'all_parameter_ratios_ge4':bool((ad.ratio_MLP_over_candidate>=4).all() and (sd.ratio_MLP_over_candidate>=4).all() and (rd.ratio_MLP_over_candidate>=4).all()),
 'test_opened':False,
 'notes':['No training was rerun; this script only pairs existing per-seed metrics with the same-seed EX7 MLP-ge4x comparator.','Ablation time compares direct model fit with MLP fit; stage-OOF pipeline time includes 3-fold OOF generation, base fit, the additional stage-logit extraction pass, and corrector fit. The stage-logit extra pass was timed by replaying existing fold checkpoints without retraining.','The recursive base-only comparison excludes any post-hoc OOF correction.']}
(O/'EX7_ORCHESTRA_ORG_ADDITIONAL_COMPARISONS_AUDIT.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
print('\nAblations aggregates:')
print(pd.read_csv(O/'EX7_ORCHESTRA_ORG_ABLATIONS_MLP_COMPARISONS_AGGREGATES.csv').to_string(index=False))
print('\nStage OOF aggregates:')
print(pd.read_csv(O/'EX7_ORCHESTRA_ORG_STAGE_OOF_MLP_COMPARISONS_AGGREGATES.csv').to_string(index=False))
print('\nRoot base aggregate:')
print(pd.read_csv(O/'EX7_ORCHESTRA_ORG_BASE_MLP_COMPARISONS_AGGREGATES.csv').to_string(index=False))
