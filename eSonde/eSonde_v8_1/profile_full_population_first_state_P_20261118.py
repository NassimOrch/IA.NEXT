import os,sys,time,json,hashlib
from pathlib import Path
os.environ.setdefault('ESONDE_INDEX_WORKERS','3')
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Dmodel_eSonde_v8_1'/'src'))
from esonde_v6.model import load_model
from esonde_v7.activation import activate_text
root=Path('/mnt/data/esonde_audit/v8_1_work/Dmodel_eSonde_v8_1')
out=Path('/mnt/data/esonde_audit/v8_1_work/suivi_model_eSonde_v8_1/experiments/v81_first_state_P_bonjour_20261118')
out.mkdir(parents=True,exist_ok=True)
t0=time.perf_counter()
def mark(event,**kw): print(json.dumps({'event':event,'elapsed_seconds':round(time.perf_counter()-t0,3),**kw},ensure_ascii=False),flush=True)
mark('start',population=1000000,role='P',operator='exact_V6_first_state_Fh_Fp_batched')
t=time.perf_counter(); b=load_model(root/'models/eSonde_v6',n_obsiss=None,verify=True); mark('load_model_done',seconds=round(time.perf_counter()-t,3),n=b.weights.n_obsiss)
t=time.perf_counter(); o=activate_text(b,'Bonjour, comment vas-tu ?','P',out,keep_trace=False,active_count=b.weights.n_obsiss); mark('activate_P_first_state_done',seconds=round(time.perf_counter()-t,3),stats=o.stats)
rec={'status':'PASS','elapsed_seconds':round(time.perf_counter()-t0,3),'population':b.weights.n_obsiss,'operator':o.stats['operator'],'fixed_point_established':False,'q_context_sha256':o.stats['q_context_sha256'],'published_sha256':o.stats['published_sha256'],'stats':o.stats,'checkpoint_sha256':'8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4'}
(out/'result.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
