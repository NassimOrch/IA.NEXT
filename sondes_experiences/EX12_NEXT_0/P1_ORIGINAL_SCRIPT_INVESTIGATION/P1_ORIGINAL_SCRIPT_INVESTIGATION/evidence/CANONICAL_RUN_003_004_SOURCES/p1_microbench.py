#!/usr/bin/env python3
"""EX12 P1: CPU-only kernel/initialization microbenchmarks; no model training."""
from __future__ import annotations
import csv, json, random, statistics, sys, time, os
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import psutil
import torch
from sklearn.cluster import KMeans
from hc_kernels import (squared_distances_reference, squared_distances_vectorized,
                        squared_distances_vectorized_identity64, gaussian_activations,
                        normalize_activations, affine_rbf_readout,
                        low_rank_modulation, hc_forward, ThreeRoundMessagePassing)

ROOT=Path('/mnt/data/EX12_NEXT_0')
OUT=ROOT/'08_benchmarks'/'P1'/'P1_RUN_003'
OUT.mkdir(parents=True,exist_ok=False)
SEED=120402; BATCHES=[1,16,64,256]; CENTERS=[8,16,32]; DIMS=[4,8,16]
WARMUPS=5; SAMPLES=40; torch.set_num_threads(1)
try: torch.set_num_interop_threads(1)
except RuntimeError: pass

def pctl(x,q): return float(np.quantile(np.asarray(x,dtype=np.float64),q))
def bench(name,fn,shape,bytes_est):
    t=time.perf_counter_ns(); fn(); cold=(time.perf_counter_ns()-t)/1e6
    for _ in range(WARMUPS): fn()
    xs=[]
    for _ in range(SAMPLES):
        t=time.perf_counter_ns(); fn(); xs.append((time.perf_counter_ns()-t)/1e6)
    return {'kernel':name,**shape,'cold_ms':cold,'p50_ms':pctl(xs,.5),'p95_ms':pctl(xs,.95),'p99_ms':pctl(xs,.99),
            'mean_ms':float(statistics.mean(xs)),'std_ms':float(statistics.pstdev(xs)),
            'throughput_samples_s':float(shape['batch']/(pctl(xs,.5)/1000)),
            'n_samples':SAMPLES,'n_warmup':WARMUPS,'structural_output_bytes_est':int(bytes_est)},xs

def dense_rbf_pipeline(z,c,p,w):
    d2=squared_distances_vectorized(z,c,p); phi=torch.exp(-.5*d2)
    return (phi*w.unsqueeze(0)).sum(-1)

def sparse_rbf_pipeline(z,c,p,w,q):
    d2=squared_distances_vectorized(z,c,p); phi=torch.exp(-.5*d2)
    vals,idx=torch.topk(phi,q,dim=-1); selected_w=w[idx]
    return (vals*selected_w).sum(-1)

def farthest_point_centers(X,k):
    # Deterministic train-only farthest-point selection; first point is farthest from train mean.
    mean=X.mean(0); first=int(((X-mean)**2).sum(1).argmax())
    chosen=[first]; mind=((X-X[first])**2).sum(1)
    for _ in range(1,k):
        ix=int(mind.argmax()); chosen.append(ix); d=((X-X[ix])**2).sum(1); mind=torch.minimum(mind,d)
    return X[chosen]

def sobol_anchors(X,k,d):
    lo=X.min(0).values; hi=X.max(0).values
    unit=torch.quasirandom.SobolEngine(dimension=d,scramble=False).draw(k)
    return lo+(hi-lo)*unit

def center_init_bench():
    rows=[]
    for d in DIMS:
      X=torch.randn(630,d)
      for k in CENTERS:
       methods=[('kmeans_train_only',lambda:KMeans(n_clusters=k,n_init=5,random_state=SEED,algorithm='lloyd').fit(X.numpy()).cluster_centers_),
                ('farthest_train_only',lambda:farthest_point_centers(X,k)),
                ('sobol_train_bounds',lambda:sobol_anchors(X,k,d))]
       for name,fn in methods:
        xs=[]
        for r in range(7):
          t=time.perf_counter_ns(); out=fn(); xs.append((time.perf_counter_ns()-t)/1e6)
          if hasattr(out,'shape') and tuple(out.shape)!=(k,d): raise RuntimeError(f'{name} bad shape {out.shape}')
        rows.append({'method':name,'n_train':630,'centers':k,'latent_dim':d,'p50_ms':pctl(xs,.5),'p95_ms':pctl(xs,.95),'runs':7,'train_only':True})
    return rows

def main():
    torch.manual_seed(SEED); np.random.seed(SEED); rng=random.Random(SEED)
    proc=psutil.Process(os.getpid()); rss0=proc.memory_info().rss
    summary=[]; raw=[]; tests=[]
    cases=[(b,k,d) for k in CENTERS for d in DIMS for b in BATCHES]
    rng.shuffle(cases)
    for b,k,d in cases:
      z=torch.randn(b,d); c=torch.randn(k,d); p=torch.nn.functional.softplus(torch.randn(k,d))+.2
      dref=squared_distances_reference(z,c,p); db=squared_distances_vectorized(z,c,p); di=squared_distances_vectorized_identity64(z,c,p)
      tests.append({'test':'distance_ref_vs_broadcast','batch':b,'centers':k,'latent_dim':d,'max_abs':float((dref-db).abs().max()),'allclose':bool(torch.allclose(dref,db,atol=1e-6,rtol=1e-6))})
      tests.append({'test':'distance_ref_vs_identity64','batch':b,'centers':k,'latent_dim':d,'max_abs':float((dref-di).abs().max()),'allclose':bool(torch.allclose(dref,di,atol=1e-6,rtol=1e-6))})
      phi=torch.exp(-.5*db); w=torch.randn(k); qvals=sorted(set([min(2,k),min(4,k),min(8,k),k]))
      shapes={'batch':b,'centers':k,'latent_dim':d}
      aw=torch.randn(d,1); ab=torch.randn(1); rw=torch.randn(k,1); rb=torch.randn(1)
      fp=torch.randn(k,d+7); rel=z[:,None,:]-c[None,:,:]; dist=torch.sqrt(db.clamp_min(1e-12))
      msg=ThreeRoundMessagePassing(d,k,d+7,hidden=16,rounds=3,seed=SEED+k+d)
      rank=4; emb=torch.randn(k,rank)*.1; U=torch.randn(d,rank)*.1; aa=torch.zeros(rank); Wc=torch.randn(d,rank)*.1; ws=torch.randn(rank)*.1; wg=torch.randn(rank)*.1
      fns=[
        ('distance_reference_loop',lambda:squared_distances_reference(z,c,p),b*k*4),
        ('distance_vectorized_broadcast',lambda:squared_distances_vectorized(z,c,p),b*k*4),
        ('distance_vectorized_identity64',lambda:squared_distances_vectorized_identity64(z,c,p),b*k*4),
        ('gaussian_activation',lambda:gaussian_activations(db),b*k*4),
        ('activation_normalization',lambda:normalize_activations(phi),b*k*4),
        ('dense_rbf_readout_only',lambda:(phi*w.unsqueeze(0)).sum(-1),b*4),
        ('dense_rbf_pipeline_distance_activation_readout',lambda:dense_rbf_pipeline(z,c,p,w),b*k*8),
        ('affine_plus_rbf_readout',lambda:affine_rbf_readout(z,phi,aw,ab,rw,rb),b*4),
        ('low_rank_modulation',lambda:low_rank_modulation(z,emb,U,aa,Wc,ws,wg,.1,.1,.1),b*k*(d+2)*4),
        ('full_hc_reference',lambda:hc_forward(z,torch.eye(d),torch.zeros(d),c,p,torch.ones(d),torch.zeros(1),rw,rb,method='reference'),b*k*4),
        ('full_hc_vectorized_broadcast',lambda:hc_forward(z,torch.eye(d),torch.zeros(d),c,p,torch.ones(d),torch.zeros(1),rw,rb,method='vectorized'),b*k*4),
        ('full_hc_identity64',lambda:hc_forward(z,torch.eye(d),torch.zeros(d),c,p,torch.ones(d),torch.zeros(1),rw,rb,method='identity64'),b*k*4),
        ('message_passing_3_rounds',lambda:msg(rel,dist,phi,fp),b*k*k*8+b*k*16*4)
      ]
      for q in qvals:
        fns.append((f'topq_rbf_pipeline_q{q}',lambda q=q:sparse_rbf_pipeline(z,c,p,w,q),b*q*12))
      rng.shuffle(fns)
      for name,fn,mem in fns:
        row,xs=bench(name,fn,shapes,mem); summary.append(row)
        raw.extend({'kernel':name,**shapes,'sample_index':i,'latency_ms':v} for i,v in enumerate(xs))
      # top-q == dense when q=K, strict check.
      td=sparse_rbf_pipeline(z,c,p,w,k); dd=dense_rbf_pipeline(z,c,p,w)
      tests.append({'test':'topq_equals_dense_when_q_equals_K','batch':b,'centers':k,'latent_dim':d,'max_abs':float((td-dd).abs().max()),'pass':bool(torch.allclose(td,dd,atol=1e-6,rtol=1e-6))})

    # Full HC forward and gradients: reference loop vs broadcast vectorization, 15 cases.
    out_err=0.; grad_err=0.; grad_count=0
    for sd in [11,29,47]:
      torch.manual_seed(sd)
      for b,k,d in [(1,8,4),(16,16,8),(64,32,16),(256,8,16),(64,16,4)]:
        base=[torch.randn(b,d),torch.randn(d,d)*.3,torch.randn(d)*.1,torch.randn(k,d),torch.nn.functional.softplus(torch.randn(k,d))+.2,torch.randn(d,1)*.2,torch.randn(1)*.1,torch.randn(k,1)*.2,torch.randn(1)*.1]
        outs=[]; grads=[]
        for meth in ['reference','vectorized']:
          args=[x.clone().detach().requires_grad_(True) for x in base]
          o=hc_forward(*args,method=meth); loss=o.square().mean()+.17*o.mean(); g=torch.autograd.grad(loss,args)
          outs.append(o.detach()); grads.append([gg.detach() for gg in g])
        oe=float((outs[0]-outs[1]).abs().max()); ge=max(float((a-bb).abs().max()) for a,bb in zip(grads[0],grads[1]))
        out_err=max(out_err,oe); grad_err=max(grad_err,ge); grad_count+=1
        tests.append({'test':'full_forward_gradient_equivalence','seed':sd,'batch':b,'centers':k,'latent_dim':d,'output_max_abs':oe,'gradient_max_abs':ge,'pass':oe<=1e-6 and ge<=1e-6})

    # B4 message passing output contract.
    for b,k,d in [(1,8,4),(16,16,8),(64,32,16)]:
      z=torch.randn(b,d); c=torch.randn(k,d); p=torch.ones(k,d); dd=squared_distances_vectorized(z,c,p); phi=torch.exp(-.5*dd)
      rel=z[:,None,:]-c[None,:,:]; dist=torch.sqrt(dd.clamp_min(1e-12)); fp=torch.randn(k,d+7)
      out=ThreeRoundMessagePassing(d,k,d+7,seed=SEED)(rel,dist,phi,fp)
      tests.append({'test':'message_passing_shape_finite','batch':b,'centers':k,'latent_dim':d,'pass':out.shape==(b,k,16) and bool(torch.isfinite(out).all())})

    init_rows=center_init_bench()
    for fname,rows in [('P1_BENCHMARK_SUMMARY.csv',summary),('P1_BENCHMARK_RAW.csv',raw),('P1_CENTER_INIT.csv',init_rows)]:
      with (OUT/fname).open('w',newline='') as f:
        wcsv=csv.DictWriter(f,fieldnames=list(rows[0])); wcsv.writeheader(); wcsv.writerows(rows)
    (OUT/'P1_NUMERICAL_TESTS.json').write_text(json.dumps({'max_output_error':out_err,'max_gradient_error':grad_err,'gradient_cases':grad_count,'tests':tests},indent=2)+'\n')
    failures=[t for t in tests if not t.get('pass',t.get('allclose',False))]
    rss1=proc.memory_info().rss
    meta={'experiment':'EX12_NEXT_0','phase':'P1','run_id':'P1_RUN_003','status':'PASS' if not failures else 'FAIL',
      'created_at_utc':datetime.now(timezone.utc).isoformat(),'mode':'CPU_ONLY_NO_TRAINING','seed':SEED,
      'batches':BATCHES,'center_counts':CENTERS,'latent_dims':DIMS,'warmups':WARMUPS,'timed_samples_per_kernel':SAMPLES,
      'torch_threads':torch.get_num_threads(),'rss_baseline_bytes':rss0,'rss_final_bytes':rss1,
      'equivalence':{'max_output_error':out_err,'max_gradient_error':grad_err,'tol':1e-6,'gradient_cases':grad_count},
      'summary_rows':len(summary),'raw_samples':len(raw),'center_init_rows':len(init_rows),'tests':len(tests),'failures':len(failures),
      'limits':['CPU-only; CUDA/VRAM and reliable energy meter unavailable. RSS is process-level; structural byte estimates are not hardware memory-traffic counters.','Top-q comparisons include distance+activation+selection+gather+readout, paired against dense distance+activation+readout.'],
      'files':['P1_BENCHMARK_SUMMARY.csv','P1_BENCHMARK_RAW.csv','P1_CENTER_INIT.csv','P1_NUMERICAL_TESTS.json']}
    (OUT/'P1_BENCHMARK_METADATA.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta,indent=2))
    return 0 if meta['status']=='PASS' else 3

if __name__=='__main__': raise SystemExit(main())
