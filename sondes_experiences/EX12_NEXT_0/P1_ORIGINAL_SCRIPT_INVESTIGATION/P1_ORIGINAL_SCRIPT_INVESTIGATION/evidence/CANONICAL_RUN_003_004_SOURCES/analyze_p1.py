#!/usr/bin/env python3
"""Recompute and compare EX12 P1 raw CPU microbenchmarks; no model training."""
from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd

ROOT=Path('/mnt/data/EX12_NEXT_0')
BASE=ROOT/'08_benchmarks'/'P1'
RUNS=['P1_RUN_003','P1_RUN_004']

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

recomp=[]; pairwise=[]; center=[]; run_summaries={}
for rn in RUNS:
    rp=BASE/rn
    s=pd.read_csv(rp/'P1_BENCHMARK_SUMMARY.csv')
    raw=pd.read_csv(rp/'P1_BENCHMARK_RAW.csv')
    tests=json.loads((rp/'P1_NUMERICAL_TESTS.json').read_text())
    groups=raw.groupby(['kernel','batch','centers','latent_dim'],sort=False)
    bad=[]
    for key,g in groups:
        m=s[(s.kernel==key[0])&(s.batch==key[1])&(s.centers==key[2])&(s.latent_dim==key[3])]
        ok=len(m)==1 and len(g)==40
        diffs={}
        if len(m)==1:
            vals=g.latency_ms.to_numpy(dtype=np.float64)
            calc={'p50_ms':float(np.quantile(vals,.5)), 'p95_ms':float(np.quantile(vals,.95)),
                  'p99_ms':float(np.quantile(vals,.99)), 'mean_ms':float(np.mean(vals)),
                  'std_ms':float(np.std(vals,ddof=0))}
            for c,v in calc.items(): diffs[c]=abs(float(m.iloc[0][c])-v)
            ok=ok and all(v<=1e-9 for v in diffs.values())
        if not ok: bad.append({'key':list(key),'raw_n':len(g),'summary_rows':len(m),'diffs':diffs})
        recomp.append({'run_id':rn,'kernel':key[0],'batch':key[1],'centers':key[2],'latent_dim':key[3],
                       'raw_n':len(g),'summary_recomputed_exactly':ok,'max_abs_aggregate_diff':max(diffs.values()) if diffs else None})
    # Matched comparisons on same batch/K/D shape.
    def cmp(a,b,label,metric='p50_ms'):
        x=s[s.kernel==a]; y=s[s.kernel==b]
        m=x.merge(y,on=['batch','centers','latent_dim'],suffixes=('_a','_b'))
        if m.empty: return
        ratios=m[f'{metric}_a'].to_numpy()/m[f'{metric}_b'].to_numpy()
        pairwise.append({'run_id':rn,'comparison':label,'metric':metric,'n_pairs':len(ratios),
                         'median_ratio_a_over_b':float(np.median(ratios)),
                         'q25_ratio':float(np.quantile(ratios,.25)), 'q75_ratio':float(np.quantile(ratios,.75)),
                         'n_a_faster':int((ratios<1).sum()),'n_equal_or_slower':int((ratios>=1).sum()),
                         'min_ratio':float(ratios.min()),'max_ratio':float(ratios.max())})
    cmp('distance_vectorized_broadcast','distance_reference_loop','distance_broadcast_vs_reference')
    cmp('distance_vectorized_identity64','distance_reference_loop','distance_identity64_vs_reference')
    cmp('full_hc_vectorized_broadcast','full_hc_reference','full_hc_broadcast_vs_reference')
    cmp('full_hc_identity64','full_hc_reference','full_hc_identity64_vs_reference')
    for q in [2,4,8,16]:
        kn=f'topq_rbf_pipeline_q{q}'
        if (s.kernel==kn).any(): cmp(kn,'dense_rbf_pipeline_distance_activation_readout',f'{kn}_vs_dense_full_pipeline')
    cmp('low_rank_modulation','affine_plus_rbf_readout','isolated_lowrank_vs_affine_rbf_readout')
    cmp('message_passing_3_rounds','full_hc_vectorized_broadcast','isolated_3round_message_vs_full_hc')
    c=pd.read_csv(rp/'P1_CENTER_INIT.csv')
    for method,g in c.groupby('method'):
        center.append({'run_id':rn,'method':method,'n_configs':len(g),'median_p50_ms':float(g.p50_ms.median()),
                       'median_p95_ms':float(g.p95_ms.median()),'min_p50_ms':float(g.p50_ms.min()),
                       'max_p50_ms':float(g.p50_ms.max()),'max_p95_ms':float(g.p95_ms.max()),
                       'all_train_only':bool(g.train_only.all()),'total_init_reps':int(g.runs.sum())})
    meta=json.loads((rp/'P1_BENCHMARK_METADATA.json').read_text())
    failed=[t for t in tests['tests'] if not t.get('pass',t.get('allclose',True))]
    run_summaries[rn]={'status':meta['status'],'seed':meta['seed'],'summary_rows':len(s),'raw_samples':len(raw),
                       'raw_groups':len(recomp)//len(RUNS) if False else len(groups),'bad_raw_aggregate_groups':len(bad),
                       'numerical_tests':len(tests['tests']),'numerical_test_failures':len(failed),
                       'max_output_error':tests['max_output_error'],'max_gradient_error':tests['max_gradient_error'],
                       'raw_sha256':sha(rp/'P1_BENCHMARK_RAW.csv'),'summary_sha256':sha(rp/'P1_BENCHMARK_SUMMARY.csv'),
                       'metadata_sha256':sha(rp/'P1_BENCHMARK_METADATA.json')}
    if bad: run_summaries[rn]['bad_examples']=bad[:5]

# Cross-run reproducibility in matched p50 timings (not a claim of identical wall-clock performance).
s3=pd.read_csv(BASE/'P1_RUN_003'/'P1_BENCHMARK_SUMMARY.csv')
s4=pd.read_csv(BASE/'P1_RUN_004'/'P1_BENCHMARK_SUMMARY.csv')
repeat=[]
for kernel in sorted(set(s3.kernel)&set(s4.kernel)):
    a=s3[s3.kernel==kernel]; b=s4[s4.kernel==kernel]
    m=a.merge(b,on=['batch','centers','latent_dim'],suffixes=('_run003','_run004'))
    if len(m):
        r=m.p50_ms_run004.to_numpy()/m.p50_ms_run003.to_numpy()
        repeat.append({'kernel':kernel,'n_pairs':len(r),'run004_over_run003_median':float(np.median(r)),
                       'q10':float(np.quantile(r,.1)),'q90':float(np.quantile(r,.9))})

pd.DataFrame(recomp).to_csv(BASE/'P1_RAW_TO_SUMMARY_AUDIT.csv',index=False)
pd.DataFrame(pairwise).to_csv(BASE/'P1_PAIRED_KERNEL_COMPARISONS.csv',index=False)
pd.DataFrame(center).to_csv(BASE/'P1_CENTER_INIT_COMPARISON.csv',index=False)
pd.DataFrame(repeat).to_csv(BASE/'P1_CROSS_RUN_REPEATABILITY.csv',index=False)
result={'experiment':'EX12_NEXT_0','phase':'P1','runs':run_summaries,
        'raw_aggregate_groups_checked':len(recomp),'raw_aggregate_groups_failed':sum(not x['summary_recomputed_exactly'] for x in recomp),
        'paired_comparisons':len(pairwise),'center_init_summaries':len(center),
        'cross_run_kernel_families':len(repeat),
        'limits':['CPU only; no CUDA/VRAM or calibrated power meter. Process RSS and structural tensor-byte estimates are not per-model peak memory or physical memory traffic.',
                  'Microbenchmarks do not measure training convergence or predictive accuracy.'],
        'artifacts':['P1_RAW_TO_SUMMARY_AUDIT.csv','P1_PAIRED_KERNEL_COMPARISONS.csv','P1_CENTER_INIT_COMPARISON.csv','P1_CROSS_RUN_REPEATABILITY.csv']}
(BASE/'P1_RECOMPUTATION_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
