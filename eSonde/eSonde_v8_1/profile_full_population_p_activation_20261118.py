import os,sys,time,json,hashlib,traceback
from pathlib import Path
os.environ['ESONDE_INDEX_PROGRESS']='1'
os.environ.setdefault('ESONDE_INDEX_WORKERS','3')
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Dmodel_eSonde_v8_1'/'src'))
from esonde_v6.model import load_model
from esonde_v7.activation import activate_convergent_text
root=Path('/mnt/data/esonde_audit/v8_1_work/Dmodel_eSonde_v8_1')
out=Path('/mnt/data/esonde_audit/v8_1_work/suivi_model_eSonde_v8_1/experiments/v81_stage_profile_bonjour_20261118')
out.mkdir(parents=True,exist_ok=True)
start=time.perf_counter()
def mark(event,**kw):
 rec={'event':event,'elapsed_seconds':round(time.perf_counter()-start,3),**kw}
 print(json.dumps(rec,ensure_ascii=False),flush=True)
mark('start',population=1000000,role='P',prompt='Bonjour, comment vas-tu ?',checkpoint_sha256='8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4')
try:
 t=time.perf_counter(); bundle=load_model(root/'models/eSonde_v6',n_obsiss=None,verify=True); mark('load_model_done',seconds=round(time.perf_counter()-t,3),n=bundle.weights.n_obsiss)
 t=time.perf_counter(); obs=activate_convergent_text(bundle,'Bonjour, comment vas-tu ?','P',out,active_count=bundle.weights.n_obsiss,keep_trace=False); mark('activate_P_done',seconds=round(time.perf_counter()-t,3),stats=obs.stats)
 rec={'status':'PASS','elapsed_seconds':round(time.perf_counter()-start,3),'stats':obs.stats}
 (out/'result.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
except Exception as e:
 mark('exception',type=type(e).__name__,error=str(e)); traceback.print_exc()
 raise
