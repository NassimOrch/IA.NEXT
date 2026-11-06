# Trace des cellules d'expérimentation EX6

Ce fichier conserve le texte source interactif disponible dans l'historique de la session pour les cellules sélectionnées qui définissent les modèles, exécutent les runs, recalculent les métriques ou construisent les scripts autonomes. Il s'agit d'une trace descriptive, pas d'un notebook entièrement reproductible : plusieurs cellules utilisent des variables et chemins définis dans les cellules précédentes.

Important : les scripts autonomes empaquetés dans `src/` ont été sauvegardés après les résultats initiaux. Leurs hashes ne sont donc pas présentés comme des hashes d'exécution. Cette campagne ne dispose pas d'un code SHA par run au temps exact du calcul.


---

## Cellule In[69]

```python
import torch.nn as nn
configs=[
    (5,0,'equal'), # adaptive
    (0,5,'equal'), # fixed
    (3,2,'equal'),
    (3,2,'global'),
    (3,2,'input'),
    (4,1,'global'),
    (1,4,'input')
]
class EmplicaStack(nn.Module):
    def __init__(self,Xtr,seed=1501,configs=configs,outer=False):
        super().__init__()
        self.layers=nn.ModuleList()
        self.outer=outer
        self.layer_gain=nn.Parameter(torch.zeros(len(configs))) if outer else None
        h_input=np.asarray(Xtr,dtype=np.float32)
        z_prev=torch.zeros((len(Xtr),2),dtype=torch.float32)
        for li,(na,nf,gate) in enumerate(configs):
            xin=h_input if li==0 else np.concatenate([h_input,z_prev.detach().numpy()],axis=1).astype(np.float32)
            layer=rmp.MicroMIXA(xin,seed+10000+li*97,na,nf,2,d=4,k=8,gate=gate)
            self.layers.append(layer)
            with torch.no_grad():
                delta=layer(ec.tensor_x(xin))
                if outer:
                    # outer global layer gate initialized with gain 0.5
                    gain=torch.sigmoid(self.layer_gain[li]).detach()
                    z_prev=z_prev+gain*delta
                else:
                    z_prev=z_prev+delta
    def forward(self,x):
        z=torch.zeros((len(x),2),dtype=x.dtype,device=x.device)
        for li,layer in enumerate(self.layers):
            hin=x if li==0 else torch.cat([x,z],dim=1)
            delta=layer(hin)
            if self.outer:
                gain=torch.sigmoid(self.layer_gain[li])
                z=z+gain*delta
            else:
                z=z+delta
        return z

emp_simple=EmplicaStack(Xtr,seed=seed,outer=False)
emp_orch=EmplicaStack(Xtr,seed=seed,outer=True)
cnt_simple=ec.count_parameters_complete(emp_simple,scaler_params=60)
cnt_orch=ec.count_parameters_complete(emp_orch,scaler_params=60)
print("simple",cnt_simple, "orchestra",cnt_orch)
print("number experts",sum(na+nf for na,nf,g in configs),"layers",len(configs))
```

---

## Cellule In[70]

```python
print(inspect.getsource(ec.load_wisconsin_dev))
```

---

## Cellule In[71]

```python
# Run one development seed for Emplica simple (35 probes, 7 layers); no test access.
emp_run_dir=Path(V1)/"results"/"raw"/"emplica_simple_seed1501"
emp_model_dir=Path(V1)/"results"/"models"/"emplica_simple_seed1501"
emp_run_dir.mkdir(parents=True,exist_ok=True); emp_model_dir.mkdir(parents=True,exist_ok=True)
ec.seed_all(seed)
opt_emp=torch.optim.Adam(emp_simple.parameters(),lr=ec.BASE_LR,weight_decay=ec.WD)
t_emp0=time.perf_counter()
emp_res,emp_prob,emp_state,emp_opt_state=rmp.fit_resumable(
    emp_simple,Xtr,data['ytr'],Xva,data['yva'],ec.BASE_LR,opt_emp,emp_model_dir/"resume_emplica_simple.pt"
)
emp_total_time=time.perf_counter()-t_emp0
emp_counts=ec.count_parameters_complete(emp_simple,scaler_params=60)
emp_lat=ec.profile_latency(emp_simple,Xva)
torch.save({"model_state":emp_state,"optimizer_state":emp_opt_state,"extra":{"P_counts":emp_counts,"configs":configs,"seed":seed}},emp_model_dir/"emplica_simple.pt")
with open(emp_run_dir/"predictions.json","w") as f: json.dump({"y_true":data['yva'].tolist(),"probabilities":emp_prob.tolist(),"test_partition_accessed":False},f)
print(json.dumps({"counts":emp_counts,"validation":emp_res['validation'],"epochs":emp_res['epochs_run'],"best_epoch":emp_res['best_epoch'],"fit_wall_s":emp_res['fit_wall_seconds'],"outer_call_wall_s":emp_total_time,"latency":emp_lat},indent=2))
```

---

## Cellule In[72]

```python
emp_ptotal=emp_counts['P_total']
emp_mlp_rows={}
for kind in ["matched","ge4x"]:
    h,pmlp,ratio=ec.make_mlp_width(Xtr.shape[1],2,emp_ptotal,matched=(kind=="matched"))
    ec.seed_all(seed+19000+emp_ptotal+(0 if kind=="matched" else 1))
    m=ec.MLP(Xtr.shape[1],2,h)
    opt=torch.optim.Adam(m.parameters(),lr=ec.MLP_LR,weight_decay=ec.WD)
    result,prob,state_m,optstate=rmp.fit_resumable(m,Xtr,data['ytr'],Xva,data['yva'],ec.MLP_LR,opt,emp_model_dir/f"resume_mlp_{kind}.pt")
    latency=ec.profile_latency(m,Xva)
    cnt=ec.count_parameters_complete(m,scaler_params=60)
    emp_mlp_rows[kind]={
        "hidden":h,"P_counts":cnt,"ratio_vs_emplica":cnt["P_total"]/emp_ptotal,
        "validation":result["validation"],"epochs_run":result["epochs_run"],
        "best_epoch":result["best_epoch"],"train_wall_seconds":result["fit_wall_seconds"],
        "latency":latency,"rss_peak_delta_bytes":result.get("rss_peak_delta_bytes")
    }
    torch.save({"model_state":state_m,"model_config":{"hidden":h},"extra":emp_mlp_rows[kind]},emp_model_dir/f"mlp_{kind}.pt")
    with open(emp_run_dir/f"mlp_{kind}_pred.json","w") as f:
        json.dump({"y_true":data['yva'].tolist(),"probabilities":prob.tolist(),"test_partition_accessed":False},f)
print(json.dumps(emp_mlp_rows,indent=2))
```

---

## Cellule In[73]

```python
# Train one Orchestra pilot: same 7x5 heterogeneous stack + external scalar layer gates.
orch_run_dir=Path(V1)/"results"/"raw"/"emplica_orchestra_seed1501"
orch_model_dir=Path(V1)/"results"/"models"/"emplica_orchestra_seed1501"
orch_run_dir.mkdir(parents=True,exist_ok=True); orch_model_dir.mkdir(parents=True,exist_ok=True)
ec.seed_all(seed)
opt_orch=torch.optim.Adam(emp_orch.parameters(),lr=ec.BASE_LR,weight_decay=ec.WD)
t_orch0=time.perf_counter()
orch_res,orch_prob,orch_state,orch_opt_state=rmp.fit_resumable(
    emp_orch,Xtr,data['ytr'],Xva,data['yva'],ec.BASE_LR,opt_orch,orch_model_dir/"resume_orchestra.pt"
)
orch_total_time=time.perf_counter()-t_orch0
orch_counts=ec.count_parameters_complete(emp_orch,scaler_params=60)
orch_lat=ec.profile_latency(emp_orch,Xva)
torch.save({"model_state":orch_state,"optimizer_state":orch_opt_state,"extra":{"P_counts":orch_counts,"configs":configs,"seed":seed,"outer_gate":"learned sigmoid gain per layer"}},orch_model_dir/"emplica_orchestra.pt")
with open(orch_run_dir/"predictions.json","w") as f: json.dump({"y_true":data['yva'].tolist(),"probabilities":orch_prob.tolist(),"test_partition_accessed":False},f)
print(json.dumps({"counts":orch_counts,"validation":orch_res['validation'],"epochs":orch_res['epochs_run'],"best_epoch":orch_res['best_epoch'],"fit_wall_s":orch_res['fit_wall_seconds'],"outer_call_wall_s":orch_total_time,"latency":orch_lat,"outer_gains":torch.sigmoid(emp_orch.layer_gain).detach().numpy().tolist()},indent=2))
```

---

## Cellule In[74]

```python
# Orchestra matched/ge4x comparators for the exact Orchestra P_total.
orch_ptotal=orch_counts['P_total']
orch_mlp_rows={}
for kind in ["matched","ge4x"]:
    h,pmlp,ratio=ec.make_mlp_width(Xtr.shape[1],2,orch_ptotal,matched=(kind=="matched"))
    ec.seed_all(seed+19000+orch_ptotal+(0 if kind=="matched" else 1))
    m=ec.MLP(Xtr.shape[1],2,h)
    opt=torch.optim.Adam(m.parameters(),lr=ec.MLP_LR,weight_decay=ec.WD)
    result,prob,state_m,optstate=rmp.fit_resumable(m,Xtr,data['ytr'],Xva,data['yva'],ec.MLP_LR,opt,orch_model_dir/f"resume_mlp_{kind}.pt")
    latency=ec.profile_latency(m,Xva)
    cnt=ec.count_parameters_complete(m,scaler_params=60)
    orch_mlp_rows[kind]={
        "hidden":h,"P_counts":cnt,"ratio_vs_orchestra":cnt["P_total"]/orch_ptotal,
        "validation":result["validation"],"epochs_run":result["epochs_run"],
        "best_epoch":result["best_epoch"],"train_wall_seconds":result["fit_wall_seconds"],
        "latency":latency,"rss_peak_delta_bytes":result.get("rss_peak_delta_bytes")
    }
    torch.save({"model_state":state_m,"model_config":{"hidden":h},"extra":orch_mlp_rows[kind]},orch_model_dir/f"mlp_{kind}.pt")
    with open(orch_run_dir/f"mlp_{kind}_pred.json","w") as f:
        json.dump({"y_true":data['yva'].tolist(),"probabilities":prob.tolist(),"test_partition_accessed":False},f)
print(json.dumps(orch_mlp_rows,indent=2))
```

---

## Cellule In[75]

```python
def train_layered_seed(s0, outer, pdir, rdir):
    pdir=Path(pdir); rdir=Path(rdir); pdir.mkdir(parents=True,exist_ok=True); rdir.mkdir(parents=True,exist_ok=True)
    ec.seed_all(s0)
    model=EmplicaStack(Xtr,seed=s0,outer=outer)
    model_tag="emplica_orchestra" if outer else "emplica_simple"
    opt=torch.optim.Adam(model.parameters(),lr=ec.BASE_LR,weight_decay=ec.WD)
    res,prob,state0,optstate=rmp.fit_resumable(model,Xtr,data['ytr'],Xva,data['yva'],ec.BASE_LR,opt,pdir/f"resume_{model_tag}.pt")
    counts=ec.count_parameters_complete(model,scaler_params=60)
    lat=ec.profile_latency(model,Xva)
    torch.save({"model_state":state0,"optimizer_state":optstate,"extra":{"P_counts":counts,"configs":configs,"seed":s0,"outer":outer}},pdir/f"{model_tag}.pt")
    with open(rdir/"predictions.json","w") as f: json.dump({"y_true":data['yva'].tolist(),"probabilities":prob.tolist(),"test_partition_accessed":False},f)
    comparator={}
    for kind in ["matched","ge4x"]:
        h,_,_=ec.make_mlp_width(Xtr.shape[1],2,counts['P_total'],matched=(kind=="matched"))
        ec.seed_all(s0+19000+counts['P_total']+(0 if kind=="matched" else 1))
        m=ec.MLP(Xtr.shape[1],2,h)
        optm=torch.optim.Adam(m.parameters(),lr=ec.MLP_LR,weight_decay=ec.WD)
        resm,pm,sm,om=rmp.fit_resumable(m,Xtr,data['ytr'],Xva,data['yva'],ec.MLP_LR,optm,pdir/f"resume_mlp_{kind}.pt")
        latm=ec.profile_latency(m,Xva)
        cntm=ec.count_parameters_complete(m,scaler_params=60)
        comparator[kind]={"hidden":h,"P_counts":cntm,"ratio_vs_candidate":cntm["P_total"]/counts["P_total"],
                          "validation":resm["validation"],"epochs_run":resm["epochs_run"],"best_epoch":resm["best_epoch"],
                          "train_wall_seconds":resm["fit_wall_seconds"],"latency":latm,
                          "rss_peak_delta_bytes":resm.get("rss_peak_delta_bytes")}
        torch.save({"model_state":sm,"extra":comparator[kind]},pdir/f"mlp_{kind}.pt")
        with open(rdir/f"mlp_{kind}_pred.json","w") as f:
            json.dump({"y_true":data['yva'].tolist(),"probabilities":pm.tolist(),"test_partition_accessed":False},f)
    output={"seed":s0,"model_tag":model_tag,"outer":outer,"P_counts":counts,
            "validation":res["validation"],"epochs_run":res["epochs_run"],"best_epoch":res["best_epoch"],
            "train_wall_seconds":res["fit_wall_seconds"],"latency":lat,"comparators":comparator}
    with open(rdir/"summary.json","w") as f: json.dump(output,f,indent=2)
    return output

additional_layered_runs=[]
for s0 in [1607,1717,2029,3037]:
    for outer in [False,True]:
        tag="emplica_orchestra" if outer else "emplica_simple"
        pdir=Path(V1)/"results"/"models"/f"{tag}_seed{s0}"
        rdir=Path(V1)/"results"/"raw"/f"{tag}_seed{s0}"
        result0=train_layered_seed(s0,outer,pdir,rdir)
        additional_layered_runs.append(result0)
        print(tag,s0,"acc",result0["validation"]["accuracy"],"ll",result0["validation"]["log_loss"],
              "train",result0["train_wall_seconds"],"p50",result0["latency"]["latency_batch1_median_ms"])
```

---

## Cellule In[76]

```python
replica_runs=[]
for s0 in [1501,1607,1717,2029,3037]:
    ck0=torch.load(v1+f'/results/models/TWOLEVEL_OOF_RESIDUAL_ADAPTIVE_seed{s0}.pt',map_location='cpu',weights_only=False)
    st=ck0['model_state']
    oof0=np.load(v1+f'/results/raw/oof_base_seed{s0}.npz')
    Xaug0=np.concatenate([Xtr,oof0['oof_logits']],axis=1).astype(np.float32)
    bs=[]
    for i in range(5):
        mi=ec.AdaptiveRBF(Xtr,4,8,s0+701+i,2)
        mi.load_state_dict({k[len(f'bases.{i}.'):]:v for k,v in st.items() if k.startswith(f'bases.{i}.')})
        mi.eval(); bs.append(mi)
    hd=OOFHead(Xaug0,s0+1801)
    hd.head.load_state_dict({k[len('head.head.'):]:v for k,v in st.items() if k.startswith('head.head.')})
    hd.eval()
    model0=OOFBaseSystem(bs,hd).eval()
    replica0=copy.deepcopy(model0).eval()
    for pp in replica0.parameters(): pp.requires_grad_(False)
    def split_one(x,model=model0): # closures default bind
        with torch.no_grad(): return torch.stack([model.bases[i](x) for i in [0,1,2]],0).mean(0)
    def split_two(x,model=replica0):
        with torch.no_grad(): return torch.stack([model.bases[i](x) for i in [3,4]],0).mean(0)
    def split_serial(x,one=split_one,two=split_two,head_mod=hd):
        z=(3/5)*one(x)+(2/5)*two(x)
        return head_mod(x,z)
    pool0=concurrent.futures.ThreadPoolExecutor(max_workers=2)
    def split_parallel(x,one=split_one,two=split_two,head_mod=hd,pool=pool0):
        f1=pool.submit(one,x); f2=pool.submit(two,x)
        z=(3/5)*f1.result()+(2/5)*f2.result()
        return head_mod(x,z)
    with torch.no_grad():
        base_logits=model0(ec.tensor_x(Xva))
        replica_logits=split_serial(ec.tensor_x(Xva))
    parity=float(torch.max(torch.abs(base_logits-replica_logits)))
    probs=torch.softmax(replica_logits,dim=1).numpy()
    predfile=v1+f'/results/raw/TWOLEVEL_OOF_RESIDUAL_ADAPTIVE_seed{s0}_pred.json'
    saved=json.load(open(predfile))
    p_diff=float(np.max(np.abs(np.asarray(saved['probabilities'])-probs)))
    metrics=ec.calc_metrics(data['yva'],probs)
    # Bench serial and true parallel split, same number of measurements as original benchmark
    ben0={"serial":bench(split_serial,Xva),"parallel":bench(split_parallel,Xva)}
    pool0.shutdown()
    p_model=sum(p.numel() for p in model0.parameters())
    p_rep=2*p_model+60
    row0=json.load(open(v1+f'/results/raw/TWOLEVEL_OOF_RESIDUAL_ADAPTIVE_seed{s0}.json'))
    # candidate-specific MLP baselines at the doubled replica parameter budget
    rep_mlp={}
    for kind in ["matched","ge4x"]:
        h,_,_=ec.make_mlp_width(Xtr.shape[1],2,p_rep,matched=(kind=="matched"))
        ec.seed_all(s0+19000+p_rep+(0 if kind=="matched" else 1))
        mm=ec.MLP(Xtr.shape[1],2,h)
        oo=torch.optim.Adam(mm.parameters(),lr=ec.MLP_LR,weight_decay=ec.WD)
        pr,mprob,mstate,mopt=rmp.fit_resumable(mm,Xtr,data['ytr'],Xva,data['yva'],ec.MLP_LR,oo,
                                                Path(V1)/"results"/"models"/f"replica_seed{s0}"/f"resume_mlp_{kind}.pt")
        mlat=ec.profile_latency(mm,Xva)
        mcnt=ec.count_parameters_complete(mm,scaler_params=60)
        rep_mlp[kind]={"hidden":h,"P_counts":mcnt,"ratio_vs_replica":mcnt['P_total']/p_rep,
                       "validation":pr['validation'],"epochs_run":pr['epochs_run'],"best_epoch":pr['best_epoch'],
                       "train_wall_seconds":pr['fit_wall_seconds'],"latency":mlat,
                       "rss_peak_delta_bytes":pr.get('rss_peak_delta_bytes')}
        mdir=Path(V1)/"results"/"models"/f"replica_seed{s0}"; mdir.mkdir(parents=True,exist_ok=True)
        torch.save({"model_state":mstate,"extra":rep_mlp[kind]},mdir/f"mlp_{kind}.pt")
    rep_row={"seed":s0,"source_validation":row0['validation'],"replica_validation":metrics,
             "P_base_total":p_model,"P_replica_total":p_rep,"ratio_legacy_mlp_ge4x_to_replica":4649/p_rep,
             "exact_output_max_logit_diff":parity,"archived_prediction_max_prob_diff":p_diff,
             "benchmark":ben0,"mlp_comparators":rep_mlp,"source_train_wall_seconds":row0['train_wall_seconds_total'],
             "replica_training_time":"NOT_MEASURED (inference-only frozen replica pilot)"}
    rdir=Path(V1)/"results"/"raw"/f"replica_seed{s0}"; rdir.mkdir(parents=True,exist_ok=True)
    with open(rdir/"summary.json","w") as f: json.dump(rep_row,f,indent=2)
    with open(rdir/"predictions.json","w") as f: json.dump({"y_true":data['yva'].tolist(),"probabilities":probs.tolist(),"test_partition_accessed":False},f)
    replica_runs.append(rep_row)
    print(s0,"parity",parity,"metrics",metrics["accuracy"],metrics["log_loss"],
          "serial b1",ben0["serial"]["1"]["p50_ms"],"parallel b1",ben0["parallel"]["1"]["p50_ms"],
          "mlp ge4x",rep_mlp["ge4x"]["P_counts"]["P_total"])
```

---

## Cellule In[77]

```python
def orch_intermediates(model, x):
    with torch.no_grad():
        z=torch.zeros((len(x),2),dtype=x.dtype,device=x.device)
        outs=[]
        for li,layer in enumerate(model.layers):
            hin=x if li==0 else torch.cat([x,z],dim=1)
            delta=layer(hin)
            gain=torch.sigmoid(model.layer_gain[li])
            z=z+gain*delta
            outs.append(z.clone())
    return outs
xv=ec.tensor_x(Xva)
orch_outs=orch_intermediates(emp_orch,xv)
exit_scan={}
for thr in [0.70,0.80,0.90,0.95,0.98,0.99]:
    final=[]; used=[]
    for j in range(len(data['yva'])):
        chosen=None
        for li,zli in enumerate(orch_outs, start=1):
            p=torch.softmax(zli[j:j+1],dim=1)
            if float(p.max())>=thr or li==len(orch_outs):
                chosen=zli[j:j+1]; used.append(li); break
        final.append(chosen)
    zz=torch.cat(final,dim=0)
    exit_scan[str(thr)]={"metrics":ec.calc_metrics(data['yva'],torch.softmax(zz,dim=1).numpy()),
                         "mean_layers":float(np.mean(used)),
                         "exit_counts":{str(i):int(used.count(i)) for i in range(1,8)}}
print(json.dumps(exit_scan,indent=2))
```

---

## Cellule In[78]

```python
# save first-seed detailed summaries from already-run models
def write_seed1501_summary(tag, counts, res, latency, train_wall, mlp_rows, rdir, configs, extras=None):
    out={"seed":1501,"candidate":tag,"configs":configs,"P_counts":counts,"validation":res["validation"],
         "epochs_run":res["epochs_run"],"best_epoch":res["best_epoch"],"train_wall_seconds":res["fit_wall_seconds"],
         "outer_wall_seconds":train_wall,"latency":latency,"comparators":mlp_rows}
    if extras: out["extras"]=extras
    with open(Path(rdir)/"summary.json","w") as f: json.dump(out,f,indent=2)
    return out
emp1501=write_seed1501_summary("emplica_simple",emp_counts,emp_res,emp_lat,emp_total_time,emp_mlp_rows,emp_run_dir,configs)
orch1501=write_seed1501_summary("emplica_orchestra",orch_counts,orch_res,orch_lat,orch_total_time,orch_mlp_rows,orch_run_dir,configs,{"outer_gains":torch.sigmoid(emp_orch.layer_gain).detach().numpy().tolist()})
# Proper batch early-exit implementation
def orch_early_exit(x, threshold):
    with torch.no_grad():
        n=len(x); z_full=torch.zeros((n,2),dtype=x.dtype,device=x.device)
        active=torch.arange(n,device=x.device)
        for li,layer in enumerate(emp_orch.layers):
            if active.numel()==0: break
            xa=x[active]; za=z_full[active]
            hin=xa if li==0 else torch.cat([xa,za],dim=1)
            dz=layer(hin); znew=za+torch.sigmoid(emp_orch.layer_gain[li])*dz
            z_full[active]=znew
            conf=torch.softmax(znew,dim=1).max(dim=1).values
            if li==len(emp_orch.layers)-1:
                active=active[:0]
            else:
                active=active[conf<threshold]
        return z_full
exit_bench={}
for thr in [0.90,0.98,0.99]:
    exit_bench[str(thr)]=bench(lambda x,t=thr: orch_early_exit(x,t),Xva,reps=100)
single_layer_fn=lambda x: emp_orch.layers[0](x)*torch.sigmoid(emp_orch.layer_gain[0])
print("early exit bench",json.dumps(exit_bench,indent=2))
# Layerwise metrics
layer_metrics={}
for li,zli in enumerate(orch_outs,1):
    layer_metrics[str(li)]=ec.calc_metrics(data['yva'],torch.softmax(zli,dim=1).numpy())
print("layer metrics",json.dumps(layer_metrics,indent=2))
```

---

## Cellule In[79]

```python
def gather_layered(tag):
    vals=[]
    for s0 in [1501,1607,1717,2029,3037]:
        p=Path(V1)/"results"/"raw"/f"{tag}_seed{s0}"/"summary.json"
        if p.exists(): rr=json.load(open(p))
        elif s0==1501:
            rr=emp1501 if tag=="emplica_simple" else orch1501
        else: continue
        vals.append(rr)
    return vals
def meanstd(xs):
    return {"mean":float(np.mean(xs)),"std_pop":float(np.std(xs)),"min":float(np.min(xs)),"max":float(np.max(xs))}
layered_agg={}
for tag in ["emplica_simple","emplica_orchestra"]:
    vals=gather_layered(tag)
    d={}
    for k in ["accuracy","log_loss"]:
        d[k]=meanstd([v["validation"][k] for v in vals])
    d["training_time_s"]=meanstd([v["train_wall_seconds"] for v in vals])
    d["latency_batch1_p50_ms"]=meanstd([v["latency"]["latency_batch1_median_ms"] for v in vals])
    d["latency_batch1_p95_ms"]=meanstd([v["latency"]["latency_batch1_p95_ms"] for v in vals])
    d["P_total"]=meanstd([v["P_counts"]["P_total"] for v in vals])
    for kind in ["matched","ge4x"]:
        d[f"mlp_{kind}_accuracy"]=meanstd([v["comparators"][kind]["validation"]["accuracy"] for v in vals])
        d[f"mlp_{kind}_log_loss"]=meanstd([v["comparators"][kind]["validation"]["log_loss"] for v in vals])
        d[f"mlp_{kind}_train_s"]=meanstd([v["comparators"][kind]["train_wall_seconds"] for v in vals])
        d[f"mlp_{kind}_batch1_p50_ms"]=meanstd([v["comparators"][kind]["latency"]["latency_batch1_median_ms"] for v in vals])
        d[f"mlp_{kind}_P_total"]=meanstd([v["comparators"][kind]["P_counts"]["P_total"] for v in vals])
    layered_agg[tag]=d
print(json.dumps(layered_agg,indent=2))
```

---

## Cellule In[80]

```python
rep_agg={
"accuracy":meanstd([x["replica_validation"]["accuracy"] for x in replica_runs]),
"log_loss":meanstd([x["replica_validation"]["log_loss"] for x in replica_runs]),
"serial_b1_p50_ms":meanstd([x["benchmark"]["serial"]["1"]["p50_ms"] for x in replica_runs]),
"serial_b1_p95_ms":meanstd([x["benchmark"]["serial"]["1"]["p95_ms"] for x in replica_runs]),
"parallel_b1_p50_ms":meanstd([x["benchmark"]["parallel"]["1"]["p50_ms"] for x in replica_runs]),
"parallel_b1_p95_ms":meanstd([x["benchmark"]["parallel"]["1"]["p95_ms"] for x in replica_runs]),
"source_training_s":meanstd([x["source_train_wall_seconds"] for x in replica_runs]),
"mlp_ge4x_accuracy":meanstd([x["mlp_comparators"]["ge4x"]["validation"]["accuracy"] for x in replica_runs]),
"mlp_ge4x_log_loss":meanstd([x["mlp_comparators"]["ge4x"]["validation"]["log_loss"] for x in replica_runs]),
"mlp_ge4x_training_s":meanstd([x["mlp_comparators"]["ge4x"]["train_wall_seconds"] for x in replica_runs]),
"mlp_ge4x_latency_b1":meanstd([x["mlp_comparators"]["ge4x"]["latency"]["latency_batch1_median_ms"] for x in replica_runs])
}
print(json.dumps(rep_agg,indent=2))
```

---

## Cellule In[85]

```python
replica_base_bench=[]
for s0 in [1501,1607,1717,2029,3037]:
    ck0=torch.load(v1+f'/results/models/TWOLEVEL_OOF_RESIDUAL_ADAPTIVE_seed{s0}.pt',map_location='cpu',weights_only=False)
    st=ck0['model_state']; oc=np.load(v1+f'/results/raw/oof_base_seed{s0}.npz')
    xaug0=np.concatenate([Xtr,oc['oof_logits']],axis=1).astype(np.float32)
    bbs=[]
    for i in range(5):
        mm=ec.AdaptiveRBF(Xtr,4,8,s0+701+i,2)
        mm.load_state_dict({k[len(f'bases.{i}.'):]:v for k,v in st.items() if k.startswith(f'bases.{i}.')})
        bbs.append(mm.eval())
    hh=OOFHead(xaug0,s0+1801)
    hh.head.load_state_dict({k[len('head.head.'):]:v for k,v in st.items() if k.startswith('head.head.')})
    sys0=OOFBaseSystem(bbs,hh).eval()
    b=bench(sys0,Xva,reps=100)
    replica_base_bench.append({"seed":s0,"baseline":b,"serial":next(x for x in replica_runs if x['seed']==s0)['benchmark']['serial'],
                               "parallel":next(x for x in replica_runs if x['seed']==s0)['benchmark']['parallel']})
    print(s0,"baseline",b["1"]["p50_ms"],"serial",replica_base_bench[-1]["serial"]["1"]["p50_ms"])
```

---

## Cellule In[86]

```python
base_mean=meanstd([x["baseline"]["1"]["p50_ms"] for x in replica_base_bench])
serial_mean=meanstd([x["serial"]["1"]["p50_ms"] for x in replica_base_bench])
parallel_mean=meanstd([x["parallel"]["1"]["p50_ms"] for x in replica_base_bench])
base_mean,serial_mean,parallel_mean
```

---

## Cellule In[87]

```python
# Preserve the exact input prompts and source documents.
ex3_bytes=outer.read('last_sources/prompt_ex3.json')
with open(Path(V1)/"inputs"/"prompt_ex3.json","wb") as f: f.write(ex3_bytes)
# copy theory and observation sources
theory_dir=Path(V1)/"inputs"/"reference_theory"
theory_dir.mkdir(parents=True,exist_ok=True)
theory_sources=[
    ("/mnt/data/extracted_global/FORMALISME_ADAPTATION_GLOBALE.tex","FORMALISME_ADAPTATION_GLOBALE.tex"),
    ("/mnt/data/extracted_global/source_copies/DDD_Base_theorie_des_empreintes_complete_order_5.tex","DDD_Base_theorie_des_empreintes_complete_order_5.tex"),
    ("/mnt/data/extracted_global/source_copies/NGeGenBrain_observation_formalisme_full_0.tex","NGeGenBrain_observation_formalisme_full_0.tex"),
    ("/mnt/data/extracted_global/source_copies/etude_et_formalisme_sonde_adaptative_1.tex","etude_et_formalisme_sonde_adaptative_1.tex")
]
for src,name in theory_sources:
    shutil.copy2(src,theory_dir/name)
# include debris as historical, low-priority source
debris=outer.read('last_sources/debrit_0.txt')
histdir=Path(V1)/"inputs"/"historical"; histdir.mkdir(parents=True,exist_ok=True)
with open(histdir/"debrit_0.txt","wb") as f:f.write(debris)
# copy split ledger for reproducibility and create data_manifest path expected by patched common
ledger_src=base4+"/versions/sondes_ex4_v006__2026-10-30/data_manifest/ex4_reference_partition_ledger_v009.csv"
print("ledger exists",os.path.exists(ledger_src))
ledger_dest=Path(V1)/"inputs"/"data_manifest"/"ex4_reference_partition_ledger_v009.csv"
ledger_dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(ledger_src,ledger_dest)
# copy reference source scripts immutably
refcode=Path(V1)/"inputs"/"reference_code"; refcode.mkdir(parents=True,exist_ok=True)
for src,name in [
    (common_path,"ex5_common.py"),
    (mixapath,"run_mixa_proportions.py"),
    (srcfile,"run_twolevel_oof_residual.py")
]:
    shutil.copy2(src,refcode/name)
# patch a local EX6 copy of the common module to use the local read-only partition ledger
new_common=common_txt.replace(
    "EX4 = Path('/mnt/data/sondes_research_workspace_ex4')\nV006 = next((EX4/'versions').glob('*v006*'))\nV008 = next((EX4/'versions').glob('*v008*'))",
    "EX4 = Path(os.environ.get('EX4_WORKSPACE', str(Path(__file__).resolve().parents[1] / 'inputs' / 'ex4_workspace_reference')))\nV006 = Path(__file__).resolve().parents[1] / 'inputs'\nV008 = V006"
)
assert "V006 = Path(__file__).resolve().parents[1] / 'inputs'" in new_common
with open(Path(V1)/"src"/"ex6_common.py","w",encoding="utf-8") as f:f.write(new_common)
new_mixa=sm.replace("from ex5_common import *","from ex6_common import *")
with open(Path(V1)/"src"/"ex6_mixa_engine.py","w",encoding="utf-8") as f:f.write(new_mixa)
print("copied sources and patched local EX6 helper")
```

---

## Cellule In[88]

```python
outer=zipfile.ZipFile('/mnt/data/last_sources.zip')
# Preserve the exact input prompts and source documents.
ex3_bytes=outer.read('last_sources/prompt_ex3.json')
with open(Path(V1)/"inputs"/"prompt_ex3.json","wb") as f: f.write(ex3_bytes)
theory_dir=Path(V1)/"inputs"/"reference_theory"
theory_dir.mkdir(parents=True,exist_ok=True)
theory_sources=[
    ("/mnt/data/extracted_global/FORMALISME_ADAPTATION_GLOBALE.tex","FORMALISME_ADAPTATION_GLOBALE.tex"),
    ("/mnt/data/extracted_global/source_copies/DDD_Base_theorie_des_empreintes_complete_order_5.tex","DDD_Base_theorie_des_empreintes_complete_order_5.tex"),
    ("/mnt/data/extracted_global/source_copies/NGeGenBrain_observation_formalisme_full_0.tex","NGeGenBrain_observation_formalisme_full_0.tex"),
    ("/mnt/data/extracted_global/source_copies/etude_et_formalisme_sonde_adaptative_1.tex","etude_et_formalisme_sonde_adaptative_1.tex")
]
for src,name in theory_sources: shutil.copy2(src,theory_dir/name)
debris=outer.read('last_sources/debrit_0.txt')
histdir=Path(V1)/"inputs"/"historical"; histdir.mkdir(parents=True,exist_ok=True)
with open(histdir/"debrit_0.txt","wb") as f:f.write(debris)
ledger_src=base4+"/versions/sondes_ex4_v006__2026-10-30/data_manifest/ex4_reference_partition_ledger_v009.csv"
print("ledger exists",os.path.exists(ledger_src))
ledger_dest=Path(V1)/"inputs"/"data_manifest"/"ex4_reference_partition_ledger_v009.csv"
ledger_dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ledger_src,ledger_dest)
refcode=Path(V1)/"inputs"/"reference_code"; refcode.mkdir(parents=True,exist_ok=True)
for src,name in [(common_path,"ex5_common.py"),(mixapath,"run_mixa_proportions.py"),(srcfile,"run_twolevel_oof_residual.py")]:
    shutil.copy2(src,refcode/name)
new_common=common_txt.replace(
    "EX4 = Path('/mnt/data/sondes_research_workspace_ex4')\nV006 = next((EX4/'versions').glob('*v006*'))\nV008 = next((EX4/'versions').glob('*v008*'))",
    "EX4 = Path(os.environ.get('EX4_WORKSPACE', str(Path(__file__).resolve().parents[1] / 'inputs' / 'ex4_workspace_reference')))\nV006 = Path(__file__).resolve().parents[1] / 'inputs'\nV008 = V006"
)
assert "V006 = Path(__file__).resolve().parents[1] / 'inputs'" in new_common
with open(Path(V1)/"src"/"ex6_common.py","w",encoding="utf-8") as f:f.write(new_common)
new_mixa=sm.replace("from ex5_common import *","from ex6_common import *")
with open(Path(V1)/"src"/"ex6_mixa_engine.py","w",encoding="utf-8") as f:f.write(new_mixa)
print("copied sources and patched local EX6 helper")
```

---

## Cellule In[89]

```python
emp_script = r'''#!/usr/bin/env python3
"""EX6 Emplica pilot: 7 layers x 5 probes, heterogeneous and outer-gated variants."""
from __future__ import annotations
import argparse, json, time, copy
from pathlib import Path
import numpy as np
import torch
from torch import nn
from ex6_common import *
from ex6_mixa_engine import MicroMIXA, fit_resumable

CONFIGS = [
    (5,0,"equal"),  # adaptive-only
    (0,5,"equal"),  # fixed-only
    (3,2,"equal"),  # MIXA equal
    (3,2,"global"), # MIXA global gate
    (3,2,"input"),  # MIXA input-conditioned gate
    (4,1,"global"), # adaptive-dominant
    (1,4,"input"),  # fixed-dominant
]
SEEDS = [1501,1607,1717,2029,3037]

class EmplicaStack(nn.Module):
    def __init__(self, Xtr, seed=1501, configs=CONFIGS, outer=False):
        super().__init__()
        self.layers = nn.ModuleList()
        self.outer = bool(outer)
        self.layer_gain = nn.Parameter(torch.zeros(len(configs))) if outer else None
        x_np = np.asarray(Xtr, dtype=np.float32)
        z_prev = torch.zeros((len(x_np),2), dtype=torch.float32)
        # Train-only initialization of each layer's RBF basis. Later layers see
        # X plus the preceding layer's initial logits, never labels.
        for li,(na,nf,gate) in enumerate(configs):
            xin = x_np if li == 0 else np.concatenate([x_np,z_prev.detach().numpy()],axis=1).astype(np.float32)
            layer = MicroMIXA(xin, seed+10000+li*97, na, nf, 2, d=4, k=8, gate=gate)
            self.layers.append(layer)
            with torch.no_grad():
                delta = layer(tensor_x(xin))
                gain = torch.sigmoid(self.layer_gain[li]).detach() if outer else 1.0
                z_prev = z_prev + gain*delta

    def forward(self, x):
        z = torch.zeros((len(x),2), dtype=x.dtype, device=x.device)
        for li,layer in enumerate(self.layers):
            hin = x if li == 0 else torch.cat([x,z],dim=1)
            delta = layer(hin)
            gain = torch.sigmoid(self.layer_gain[li]) if self.outer else 1.0
            z = z + gain*delta
        return z

def run_one(seed: int, outer: bool):
    data = load_wisconsin_dev()  # train/validation/adaptation only; historical development split
    tag = "emplica_orchestra" if outer else "emplica_simple"
    run_id = f"{tag}_seed{seed}"
    raw_dir = VROOT/"results"/"raw"/run_id
    model_dir = VROOT/"results"/"models"/run_id
    raw_dir.mkdir(parents=True,exist_ok=True); model_dir.mkdir(parents=True,exist_ok=True)
    summary_path = raw_dir/"summary.json"
    if summary_path.exists():
        raise FileExistsError(f"{summary_path} already exists; use a new run ID/version, do not overwrite")
    seed_all(seed)
    model = EmplicaStack(data["Xtr"],seed=seed,outer=outer)
    optimizer = torch.optim.Adam(model.parameters(),lr=BASE_LR,weight_decay=WD)
    result,probs,state,optstate = fit_resumable(
        model,data["Xtr"],data["ytr"],data["Xva"],data["yva"],BASE_LR,optimizer,
        model_dir/"resume_probe.pt"
    )
    counts = count_parameters_complete(model,scaler_params=SHARED_SCALER_PARAMS)
    lat = profile_latency(model,data["Xva"])
    torch.save({"model_state":state,"optimizer_state":optstate,
                "config":{"seed":seed,"outer":outer,"configs":CONFIGS,"P_counts":counts}},
               model_dir/"candidate.pt")
    with (raw_dir/"predictions.json").open("w",encoding="utf8") as f:
        json.dump({"y_true":data["yva"].tolist(),"probabilities":probs.tolist(),
                   "test_partition_accessed":False,"split":"historically exposed Wisconsin development"},f)
    comparators={}
    for kind in ("matched","ge4x"):
        hidden,_,_ = make_mlp_width(data["Xtr"].shape[1],2,counts["P_total"],
                                    scaler_params=SHARED_SCALER_PARAMS,matched=(kind=="matched"))
        seed_all(seed+19000+counts["P_total"]+(0 if kind=="matched" else 1))
        mlp = MLP(data["Xtr"].shape[1],2,hidden)
        opt_mlp = torch.optim.Adam(mlp.parameters(),lr=MLP_LR,weight_decay=WD)
        r_mlp,p_mlp,s_mlp,o_mlp = fit_resumable(
            mlp,data["Xtr"],data["ytr"],data["Xva"],data["yva"],MLP_LR,opt_mlp,
            model_dir/f"resume_mlp_{kind}.pt"
        )
        c_mlp = count_parameters_complete(mlp,scaler_params=SHARED_SCALER_PARAMS)
        comparators[kind] = {
            "hidden":hidden,"P_counts":c_mlp,"ratio_vs_candidate":c_mlp["P_total"]/counts["P_total"],
            "validation":r_mlp["validation"],"epochs_run":r_mlp["epochs_run"],
            "best_epoch":r_mlp["best_epoch"],"train_wall_seconds":r_mlp["fit_wall_seconds"],
            "latency":profile_latency(mlp,data["Xva"]),
            "rss_peak_delta_bytes":r_mlp.get("rss_peak_delta_bytes")
        }
        torch.save({"model_state":s_mlp,"config":{"hidden":hidden,"P_counts":c_mlp}},
                   model_dir/f"mlp_{kind}.pt")
        with (raw_dir/f"mlp_{kind}_predictions.json").open("w",encoding="utf8") as f:
            json.dump({"y_true":data["yva"].tolist(),"probabilities":p_mlp.tolist(),
                       "test_partition_accessed":False},f)
    row = {
        "run_id":run_id,"seed":seed,"architecture":tag,"outer_global_gates":outer,
        "layer_configs":CONFIGS,"n_layers":len(CONFIGS),"probes_per_layer":[na+nf for na,nf,_ in CONFIGS],
        "P_counts":counts,"validation":result["validation"],
        "epochs_run":result["epochs_run"],"best_epoch":result["best_epoch"],
        "train_wall_seconds":result["fit_wall_seconds"],"latency":lat,
        "rss_peak_delta_bytes":result.get("rss_peak_delta_bytes"),
        "comparators":comparators,"test_partition_accessed":False,
        "dataset_status":"historically exposed development only; no confirmatory claim"
    }
    with summary_path.open("w",encoding="utf8") as f: json.dump(row,f,ensure_ascii=False,indent=2)
    append_jsonl(VROOT/"results"/"raw"/"emplica_runs.jsonl",row)
    return row

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seeds",nargs="+",type=int,default=SEEDS)
    ap.add_argument("--architectures",nargs="+",choices=["simple","orchestra"],default=["simple","orchestra"])
    args=ap.parse_args()
    for seed in args.seeds:
        for arch in args.architectures:
            row=run_one(seed,arch=="orchestra")
            print(row["run_id"],row["validation"],row["P_counts"]["P_total"],flush=True)

if __name__=="__main__":
    main()
'''
with open(Path(V1)/"src"/"run_emplica_pilot.py","w",encoding="utf-8") as f: f.write(emp_script)
print("emplica script saved")
```

---

## Cellule In[90]

```python
rep_script = r'''#!/usr/bin/env python3
"""EX6 Replica inference pilot: frozen exact clone, fold-computation partition."""
from __future__ import annotations
import os, json, time, copy, argparse, concurrent.futures
from pathlib import Path
import numpy as np
import torch
from torch import nn
from ex6_common import *
from ex6_mixa_engine import fit_resumable

SEEDS=[1501,1607,1717,2029,3037]
EX5_V001=Path(os.environ.get(
    "EX5_V001_DIR",
    "/mnt/data/sondes_research_workspace_ex5/versions/sondes_ex5_v001__2026-10-30"
))

class OOFHead(nn.Module):
    def __init__(self,Xaug,seed):
        super().__init__()
        self.nin=Xaug.shape[1]-2
        self.head=AdaptiveRBF(Xaug,4,8,seed,2)
    def forward(self,x,z):
        return z+self.head(torch.cat([x,z],dim=1))

class OOFBaseSystem(nn.Module):
    def __init__(self,bases,head):
        super().__init__()
        self.bases=nn.ModuleList(bases)
        self.head=head
    def forward(self,x):
        z=torch.stack([m(x) for m in self.bases],dim=0).mean(0)
        return self.head(x,z)

def build_source(seed,data):
    checkpoint=EX5_V001/"results"/"models"/f"TWOLEVEL_OOF_RESIDUAL_ADAPTIVE_seed{seed}.pt"
    cache=EX5_V001/"results"/"raw"/f"oof_base_seed{seed}.npz"
    predfile=EX5_V001/"results"/"raw"/f"TWOLEVEL_OOF_RESIDUAL_ADAPTIVE_seed{seed}_pred.json"
    if not (checkpoint.exists() and cache.exists() and predfile.exists()):
        raise FileNotFoundError(f"missing immutable EX5 OOF artifact for seed {seed}")
    ck=torch.load(checkpoint,map_location="cpu",weights_only=False)
    state=ck["model_state"]
    oof=np.load(cache)
    Xaug=np.concatenate([data["Xtr"],oof["oof_logits"]],axis=1).astype(np.float32)
    bases=[]
    for i in range(5):
        model=AdaptiveRBF(data["Xtr"],4,8,seed+701+i,2)
        model.load_state_dict({k[len(f"bases.{i}."):]:v for k,v in state.items()
                               if k.startswith(f"bases.{i}.")})
        model.eval(); bases.append(model)
    head=OOFHead(Xaug,seed+1801)
    head.head.load_state_dict({k[len("head.head."):]:v for k,v in state.items()
                               if k.startswith("head.head.")})
    head.eval()
    source=OOFBaseSystem(bases,head).eval()
    archived=json.load(open(predfile,encoding="utf8"))
    return source,archived,ck

def run_one(seed):
    data=load_wisconsin_dev()
    run_id=f"replica_seed{seed}"
    raw_dir=VROOT/"results"/"raw"/run_id
    model_dir=VROOT/"results"/"models"/run_id
    raw_dir.mkdir(parents=True,exist_ok=True); model_dir.mkdir(parents=True,exist_ok=True)
    summary_path=raw_dir/"summary.json"
    if summary_path.exists():
        raise FileExistsError(f"{summary_path} already exists; use a new version/run ID")
    source,archived,ck=build_source(seed,data)
    tclone=time.perf_counter()
    replica=copy.deepcopy(source).eval()
    clone_seconds=time.perf_counter()-tclone
    for p in replica.parameters(): p.requires_grad_(False)
    def f_primary(x):
        with torch.no_grad():
            return torch.stack([source.bases[i](x) for i in [0,1,2]],dim=0).mean(0)
    def f_replica(x):
        with torch.no_grad():
            return torch.stack([replica.bases[i](x) for i in [3,4]],dim=0).mean(0)
    def serial_split(x):
        z=(3.0/5.0)*f_primary(x)+(2.0/5.0)*f_replica(x)
        return source.head(x,z)
    pool=concurrent.futures.ThreadPoolExecutor(max_workers=2)
    def parallel_split(x):
        a=pool.submit(f_primary,x); b=pool.submit(f_replica,x)
        z=(3.0/5.0)*a.result()+(2.0/5.0)*b.result()
        return source.head(x,z)
    xv=tensor_x(data["Xva"])
    with torch.no_grad():
        source_logits=source(xv)
        replica_logits=serial_split(xv)
        parallel_logits=parallel_split(xv)
    probs=torch.softmax(replica_logits,dim=1).numpy()
    parallel_probs=torch.softmax(parallel_logits,dim=1).numpy()
    source_prob=np.asarray(archived["probabilities"])
    parity=float(torch.max(torch.abs(source_logits-replica_logits)).item())
    archived_diff=float(np.max(np.abs(source_prob-probs)))
    parallel_diff=float(np.max(np.abs(source_prob-parallel_probs)))
    metrics=calc_metrics(data["yva"],probs)
    parallel_metrics=calc_metrics(data["yva"],parallel_probs)
    serial_latency=profile_latency(source,data["Xva"],forward_fn=serial_split)
    parallel_latency=profile_latency(source,data["Xva"],forward_fn=parallel_split)
    pool.shutdown()
    p_one=sum(p.numel() for p in source.parameters())
    pbase=sum(p.numel() for m in source.bases for p in m.parameters())
    phead=sum(p.numel() for p in source.head.parameters())
    ptotal=2*p_one+SHARED_SCALER_PARAMS
    pdormant=(2*182)+ (3*182)+phead  # unused fold copies + unused replica head (d=4,k=8)
    counts={"P_train":2*p_one,"P_fixed_and_buffers_in_model":0,
            "P_preprocessor":SHARED_SCALER_PARAMS,"P_total":ptotal,
            "P_active_train_estimate":p_one,"P_dormant_train_estimate":pdormant,
            "P_replica_copy_trainable_flags_false":sum(p.numel() for p in replica.parameters() if not p.requires_grad)}
    source_row=json.load(open(EX5_V001/"results"/"raw"/
                              f"TWOLEVEL_OOF_RESIDUAL_ADAPTIVE_seed{seed}.json",encoding="utf8"))
    comparator={}
    for kind in ("matched","ge4x"):
        hidden,_,_=make_mlp_width(data["Xtr"].shape[1],2,ptotal,
                                  scaler_params=SHARED_SCALER_PARAMS,matched=(kind=="matched"))
        seed_all(seed+19000+ptotal+(0 if kind=="matched" else 1))
        mlp=MLP(data["Xtr"].shape[1],2,hidden)
        opt=torch.optim.Adam(mlp.parameters(),lr=MLP_LR,weight_decay=WD)
        r,p,s,o=fit_resumable(mlp,data["Xtr"],data["ytr"],data["Xva"],data["yva"],
                              MLP_LR,opt,model_dir/f"resume_mlp_{kind}.pt")
        comparator[kind]={"hidden":hidden,"P_counts":count_parameters_complete(mlp,scaler_params=SHARED_SCALER_PARAMS),
                          "validation":r["validation"],"epochs_run":r["epochs_run"],
                          "best_epoch":r["best_epoch"],"train_wall_seconds":r["fit_wall_seconds"],
                          "latency":profile_latency(mlp,data["Xva"])}
        torch.save({"model_state":s,"extra":comparator[kind]},model_dir/f"mlp_{kind}.pt")
    torch.save({"primary_state":source.state_dict(),"frozen_replica_state":replica.state_dict(),
                "extra":{"P_counts":counts,"replica_train_wall_seconds":"NOT_MEASURED"}},
               model_dir/"replica_pair.pt")
    row={"run_id":run_id,"seed":seed,"architecture":"frozen exact clone; primary folds 0-2, replica folds 3-4",
         "P_counts":counts,"source_validation":source_row["validation"],"replica_validation":metrics,
         "parallel_validation":parallel_metrics,"max_logit_parity":parity,
         "max_probability_diff_vs_archived":archived_diff,"max_parallel_probability_diff":parallel_diff,
         "clone_seconds":clone_seconds,"source_train_wall_seconds":source_row["train_wall_seconds_total"],
         "replica_training_time":"NOT MEASURED (inference-only; replica has no optimizer/step)",
         "serial_latency":serial_latency,"parallel_latency":parallel_latency,
         "mlp_comparators":comparator,"test_partition_accessed":False,
         "dataset_status":"historically exposed Wisconsin development only"}
    with summary_path.open("w",encoding="utf8") as f: json.dump(row,f,ensure_ascii=False,indent=2)
    with (raw_dir/"predictions.json").open("w",encoding="utf8") as f:
        json.dump({"y_true":data["yva"].tolist(),"probabilities":probs.tolist(),
                   "test_partition_accessed":False},f)
    append_jsonl(VROOT/"results"/"raw"/"replica_runs.jsonl",row)
    return row

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seeds",nargs="+",type=int,default=SEEDS)
    args=ap.parse_args()
    for seed in args.seeds:
        row=run_one(seed)
        print(row["run_id"],row["replica_validation"],row["P_counts"],flush=True)

if __name__=="__main__":
    main()
'''
with open(Path(V1)/"src"/"run_replica_pilot.py","w",encoding="utf-8") as f:f.write(rep_script)
print("replica script saved")
```

---

## Cellule In[91]

```python
sys.path.insert(0,str(Path(V1)/"src"))
import importlib
# Import through the new, packaged EX6 copies rather than the historical in-memory imports.
if "ex6_common" in sys.modules: del sys.modules["ex6_common"]
if "ex6_mixa_engine" in sys.modules: del sys.modules["ex6_mixa_engine"]
ex6c=importlib.import_module("ex6_common")
ex6m=importlib.import_module("ex6_mixa_engine")
dtest=ex6c.load_wisconsin_dev()
print("VROOT",ex6c.VROOT)
print("split",dtest["split_sizes"],"Xtr exact",np.array_equal(dtest["Xtr"],data["Xtr"]))
print("Emplica engine",ex6m.MicroMIXA,"fit",ex6m.fit_resumable)
```

---

## Cellule In[92]

```python
for scriptname in ["run_emplica_pilot.py","run_replica_pilot.py"]:
    path=Path(V1)/"src"/scriptname
    compile(path.read_text(encoding="utf-8"),str(path),"exec")
    print("syntax OK",scriptname)
```

---

## Cellule In[93]

```python
homo_configs=[(3,2,'global')]*7
homo_runs=[]
for s0 in [1501,1607,1717,2029,3037]:
    rdir=Path(V1)/"results"/"raw"/f"orchestra_homo_global_seed{s0}"
    pdir=Path(V1)/"results"/"models"/f"orchestra_homo_global_seed{s0}"
    rdir.mkdir(parents=True,exist_ok=True); pdir.mkdir(parents=True,exist_ok=True)
    ec.seed_all(s0)
    model=EmplicaStack(Xtr,seed=s0,configs=homo_configs,outer=True)
    opt=torch.optim.Adam(model.parameters(),lr=ec.BASE_LR,weight_decay=ec.WD)
    res,prob,stateh,opth=rmp.fit_resumable(model,Xtr,data['ytr'],Xva,data['yva'],ec.BASE_LR,opt,pdir/"resume_probe.pt")
    cnt=ec.count_parameters_complete(model,scaler_params=60)
    lat=ec.profile_latency(model,Xva)
    torch.save({"model_state":stateh,"optimizer_state":opth,"extra":{"P_counts":cnt,"configs":homo_configs}},pdir/"candidate.pt")
    with open(rdir/"predictions.json","w") as f:json.dump({"y_true":data['yva'].tolist(),"probabilities":prob.tolist(),"test_partition_accessed":False},f)
    cmp={}
    for kind in ['matched','ge4x']:
        h,_,_=ec.make_mlp_width(30,2,cnt['P_total'],matched=(kind=='matched'))
        ec.seed_all(s0+19000+cnt['P_total']+(0 if kind=='matched' else 1))
        mm=ec.MLP(30,2,h); optm=torch.optim.Adam(mm.parameters(),lr=ec.MLP_LR,weight_decay=ec.WD)
        mr,mp,ms,mo=rmp.fit_resumable(mm,Xtr,data['ytr'],Xva,data['yva'],ec.MLP_LR,optm,pdir/f"resume_mlp_{kind}.pt")
        mcnt=ec.count_parameters_complete(mm,scaler_params=60)
        cmp[kind]={"hidden":h,"P_counts":mcnt,"ratio":mcnt["P_total"]/cnt["P_total"],
                   "validation":mr["validation"],"train_wall_seconds":mr["fit_wall_seconds"],
                   "epochs_run":mr["epochs_run"],"best_epoch":mr["best_epoch"],
                   "latency":ec.profile_latency(mm,Xva)}
        torch.save({"model_state":ms,"extra":cmp[kind]},pdir/f"mlp_{kind}.pt")
    row={"seed":s0,"architecture":"ORCH_HOMO_GLOBAL_MIXA","configs":homo_configs,
         "P_counts":cnt,"validation":res["validation"],"train_wall_seconds":res["fit_wall_seconds"],
         "epochs_run":res["epochs_run"],"best_epoch":res["best_epoch"],"latency":lat,"comparators":cmp,
         "test_partition_accessed":False,"dataset_status":"historically exposed development only"}
    with open(rdir/"summary.json","w") as f:json.dump(row,f,indent=2)
    append_jsonl(Path(V1)/"results"/"raw"/"orchestra_homogeneous_runs.jsonl",row)
    homo_runs.append(row)
    print(s0,row["validation"],"P",cnt["P_total"],"p50",lat["latency_batch1_median_ms"])
```

---

## Cellule In[94]

```python
homo_runs=[]
seed1501_homo_path=Path(V1)/"results"/"raw"/"orchestra_homo_global_seed1501"/"summary.json"
print("seed1501 complete",seed1501_homo_path.exists())
if seed1501_homo_path.exists():
    rr=json.load(open(seed1501_homo_path)); homo_runs.append(rr)
    ex6c.append_jsonl(Path(V1)/"results"/"raw"/"orchestra_homogeneous_runs.jsonl",rr)
```

---

## Cellule In[95]

```python
for s0 in [1607,1717,2029,3037]:
    rdir=Path(V1)/"results"/"raw"/f"orchestra_homo_global_seed{s0}"
    pdir=Path(V1)/"results"/"models"/f"orchestra_homo_global_seed{s0}"
    rdir.mkdir(parents=True,exist_ok=True); pdir.mkdir(parents=True,exist_ok=True)
    ec.seed_all(s0)
    model=EmplicaStack(Xtr,seed=s0,configs=homo_configs,outer=True)
    opt=torch.optim.Adam(model.parameters(),lr=ec.BASE_LR,weight_decay=ec.WD)
    res,prob,stateh,opth=rmp.fit_resumable(model,Xtr,data['ytr'],Xva,data['yva'],ec.BASE_LR,opt,pdir/"resume_probe.pt")
    cnt=ec.count_parameters_complete(model,scaler_params=60)
    lat=ec.profile_latency(model,Xva)
    torch.save({"model_state":stateh,"optimizer_state":opth,"extra":{"P_counts":cnt,"configs":homo_configs}},pdir/"candidate.pt")
    with open(rdir/"predictions.json","w") as f:json.dump({"y_true":data['yva'].tolist(),"probabilities":prob.tolist(),"test_partition_accessed":False},f)
    cmp={}
    for kind in ['matched','ge4x']:
        h,_,_=ec.make_mlp_width(30,2,cnt['P_total'],matched=(kind=='matched'))
        ec.seed_all(s0+19000+cnt['P_total']+(0 if kind=='matched' else 1))
        mm=ec.MLP(30,2,h); optm=torch.optim.Adam(mm.parameters(),lr=ec.MLP_LR,weight_decay=ec.WD)
        mr,mp,ms,mo=rmp.fit_resumable(mm,Xtr,data['ytr'],Xva,data['yva'],ec.MLP_LR,optm,pdir/f"resume_mlp_{kind}.pt")
        mcnt=ec.count_parameters_complete(mm,scaler_params=60)
        cmp[kind]={"hidden":h,"P_counts":mcnt,"ratio":mcnt["P_total"]/cnt["P_total"],
                   "validation":mr["validation"],"train_wall_seconds":mr["fit_wall_seconds"],
                   "epochs_run":mr["epochs_run"],"best_epoch":mr["best_epoch"],
                   "latency":ec.profile_latency(mm,Xva)}
        torch.save({"model_state":ms,"extra":cmp[kind]},pdir/f"mlp_{kind}.pt")
    row={"seed":s0,"architecture":"ORCH_HOMO_GLOBAL_MIXA","configs":homo_configs,
         "P_counts":cnt,"validation":res["validation"],"train_wall_seconds":res["fit_wall_seconds"],
         "epochs_run":res["epochs_run"],"best_epoch":res["best_epoch"],"latency":lat,"comparators":cmp,
         "test_partition_accessed":False,"dataset_status":"historically exposed development only"}
    with open(rdir/"summary.json","w") as f:json.dump(row,f,indent=2)
    ex6c.append_jsonl(Path(V1)/"results"/"raw"/"orchestra_homogeneous_runs.jsonl",row)
    homo_runs.append(row)
    print(s0,row["validation"],"P",cnt["P_total"],"p50",lat["latency_batch1_median_ms"])
```

---

## Cellule In[96]

```python
homo_agg={}
for key in ["accuracy","log_loss"]:
    homo_agg[key]=meanstd([x["validation"][key] for x in homo_runs])
for key,func in [
    ("train_s",lambda x:x["train_wall_seconds"]),
    ("batch1_p50_ms",lambda x:x["latency"]["latency_batch1_median_ms"]),
    ("batch1_p95_ms",lambda x:x["latency"]["latency_batch1_p95_ms"]),
    ("P_total",lambda x:x["P_counts"]["P_total"])
]:
    homo_agg[key]=meanstd([func(x) for x in homo_runs])
for kind in ["matched","ge4x"]:
    for key,func in [
        ("accuracy",lambda x:x["validation"]["accuracy"]),
        ("log_loss",lambda x:x["validation"]["log_loss"]),
        ("train_s",lambda x:x["train_wall_seconds"]),
        ("batch1_p50_ms",lambda x:x["latency"]["latency_batch1_median_ms"]),
        ("P_total",lambda x:x["P_counts"]["P_total"])
    ]:
        homo_agg[f"mlp_{kind}_{key}"]=meanstd([func(x["comparators"][kind]) for x in homo_runs])
print(json.dumps(homo_agg,indent=2))
```

---

## Cellule In[97]

```python
# Complete missing prediction artefacts for Replica comparators and homogeneous Orchestra.
audit_recalc=[]
for seed0 in [1501,1607,1717,2029,3037]:
    # Replica MLP comparators
    rdir=Path(V1)/"results"/"raw"/f"replica_seed{seed0}"
    mdir=Path(V1)/"results"/"models"/f"replica_seed{seed0}"
    for kind in ["matched","ge4x"]:
        mo=torch.load(mdir/f"mlp_{kind}.pt",map_location="cpu",weights_only=False)
        h=int(mo["extra"]["hidden"])
        mm=ec.MLP(30,2,h); mm.load_state_dict(mo["model_state"]); mm.eval()
        with torch.no_grad(): pp=torch.softmax(mm(ec.tensor_x(Xva)),dim=1).numpy()
        pm=ec.calc_metrics(data["yva"],pp)
        with open(rdir/f"mlp_{kind}_predictions.json","w") as f:
            json.dump({"y_true":data["yva"].tolist(),"probabilities":pp.tolist(),"test_partition_accessed":False},f)
        exp=mo["extra"]["validation"]
        audit_recalc.append({"type":"replica","seed":seed0,"kind":kind,
                             "max_metric_abs_diff":max(abs(pm[k]-exp[k]) for k in ["accuracy","log_loss"]),
                             "metrics":pm})
    # Homogeneous Orchestra candidate and MLP comparators
    rdir=Path(V1)/"results"/"raw"/f"orchestra_homo_global_seed{seed0}"
    mdir=Path(V1)/"results"/"models"/f"orchestra_homo_global_seed{seed0}"
    hp=torch.load(mdir/"candidate.pt",map_location="cpu",weights_only=False)
    ec.seed_all(seed0)
    model=EmplicaStack(Xtr,seed=seed0,configs=homo_configs,outer=True)
    model.load_state_dict(hp["model_state"]); model.eval()
    with torch.no_grad(): pp=torch.softmax(model(ec.tensor_x(Xva)),dim=1).numpy()
    with open(rdir/"predictions.json","w") as f:
        json.dump({"y_true":data["yva"].tolist(),"probabilities":pp.tolist(),"test_partition_accessed":False},f)
    exp=json.load(open(rdir/"summary.json"))["validation"]
    pm=ec.calc_metrics(data["yva"],pp)
    audit_recalc.append({"type":"orchestra_homo","seed":seed0,"kind":"probe",
                         "max_metric_abs_diff":max(abs(pm[k]-exp[k]) for k in ["accuracy","log_loss"]),
                         "metrics":pm})
    for kind in ["matched","ge4x"]:
        mo=torch.load(mdir/f"mlp_{kind}.pt",map_location="cpu",weights_only=False)
        h=int(mo["extra"]["hidden"])
        mm=ec.MLP(30,2,h); mm.load_state_dict(mo["model_state"]); mm.eval()
        with torch.no_grad(): pp=torch.softmax(mm(ec.tensor_x(Xva)),dim=1).numpy()
        pm=ec.calc_metrics(data["yva"],pp)
        with open(rdir/f"mlp_{kind}_predictions.json","w") as f:
            json.dump({"y_true":data["yva"].tolist(),"probabilities":pp.tolist(),"test_partition_accessed":False},f)
        exp=mo["extra"]["validation"]
        audit_recalc.append({"type":"orchestra_homo","seed":seed0,"kind":kind,
                             "max_metric_abs_diff":max(abs(pm[k]-exp[k]) for k in ["accuracy","log_loss"]),
                             "metrics":pm})
max(a["max_metric_abs_diff"] for a in audit_recalc),len(audit_recalc)
```

---

## Cellule In[98]

```python
def sha256_path(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def sha256_member(zf,name):
    h=hashlib.sha256()
    with zf.open(name) as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b""): h.update(chunk)
    return h.hexdigest()
archive_hash=sha256_path('/mnt/data/last_sources.zip')
prompt_paths={
    "prompt_ex3.json":str(Path(V1)/"inputs"/"prompt_ex3.json"),
    "prompt_ex4.json":str(Path(V1)/"inputs"/"prompt_ex4.json"),
    "prompt_ex5.json":str(Path(V1)/"inputs"/"prompt_ex5.json"),
    "prompt_ex6.json":str(Path(V1)/"prompt_ex6.json")
}
prompt_hashes={k:{"path":v,"sha256":sha256_path(v),"bytes":os.path.getsize(v)} for k,v in prompt_paths.items()}
print("archive sha",archive_hash)
print(json.dumps(prompt_hashes,indent=2))
```
