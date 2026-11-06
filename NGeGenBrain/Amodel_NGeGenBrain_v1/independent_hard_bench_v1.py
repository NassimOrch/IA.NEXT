from __future__ import annotations
import argparse, json, os, random, sqlite3, tempfile, threading, time, traceback, hashlib, platform
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path
from datetime import datetime, timezone
import sys

_parser=argparse.ArgumentParser(description='Same 15-case independent stress benchmark for NGeGenBrain V0 and V1')
_parser.add_argument('--model-root', required=True, help='Root of extracted model package (contains src/ngegenbrain)')
_parser.add_argument('--source-archive', required=True, help='Exact ZIP from which model-root was extracted')
_parser.add_argument('--output', required=True, help='Path for JSON results')
_parser.add_argument('--seed', type=int, default=20261027)
_ARGS=_parser.parse_args()
ROOT=Path(_ARGS.model_root).resolve()
SOURCE_ARCHIVE=Path(_ARGS.source_archive).resolve()
OUT=Path(_ARGS.output).resolve()
SEED=_ARGS.seed
STARTED_AT=datetime.now(timezone.utc).isoformat(timespec='seconds')
if not (ROOT/'src/ngegenbrain').is_dir():
    _parser.error(f'--model-root must be extracted model root with src/ngegenbrain: {ROOT}')
if not SOURCE_ARCHIVE.is_file():
    _parser.error(f'--source-archive does not exist: {SOURCE_ARCHIVE}')
os.environ['PYTHONPATH']=str(ROOT/'src')
sys.path.insert(0,str(ROOT/'src'))
from ngegenbrain.actions import ActionService
from ngegenbrain.store import Store
from ngegenbrain.engine import Engine
from ngegenbrain.operators import call_operator, OperatorError
from ngegenbrain.mesh import infer_mesh, verify_certificate
from ngegenbrain.world_model import WorldModelManager
from ngegenbrain.util import canonical_json

results=[]
def record(test_id, category, expected, observed, verdict, details=None, duration=None):
    results.append({'id':test_id,'category':category,'expected':expected,'observed':observed,'verdict':verdict,'details':details or {},'duration_seconds':duration})
def frac_out(v):
    if isinstance(v,dict) and set(v)=={'$rational'}: return Fraction(*v['$rational'])
    return Fraction(v)

# Fresh, isolated database per set; no demo facts or target answers loaded.
tmp=Path(tempfile.mkdtemp(prefix='ngegenbrain_independent_hard_'))
db=tmp/'bench.sqlite3'
svc=ActionService(db)
store=svc.store; engine=svc.engine

# 1. Deterministic property test for exact arithmetic against Python Fraction oracle.
rng=random.Random(SEED); arithmetic_checks=0; arithmetic_failures=[]
start=time.perf_counter()
for i in range(600):
    a=Fraction(rng.randint(-100000,100000),rng.randint(1,999))
    b=Fraction(rng.randint(-100000,100000),rng.randint(1,999))
    aa={'$rational':[a.numerator,a.denominator]}; bb={'$rational':[b.numerator,b.denominator]}
    for op, exp in [('add',a+b),('subtract',a-b),('multiply',a*b)]:
        got=frac_out(call_operator(op,[aa,bb])); arithmetic_checks+=1
        if got != exp: arithmetic_failures.append({'i':i,'op':op,'a':str(a),'b':str(b),'expected':str(exp),'got':str(got)})
    if b:
        got=frac_out(call_operator('divide',[aa,bb])); arithmetic_checks+=1
        if got != a/b: arithmetic_failures.append({'i':i,'op':'divide','a':str(a),'b':str(b),'expected':str(a/b),'got':str(got)})
record('ARITH-001','property-based exact arithmetic',f'{arithmetic_checks} exact matches',f'{arithmetic_checks-len(arithmetic_failures)} matches; {len(arithmetic_failures)} mismatches','PASS' if not arithmetic_failures else 'FAIL',{'seed':SEED,'generated_pairs':600,'failures':arithmetic_failures[:10]},time.perf_counter()-start)

# 2. Mesh closure on generated directed graph, compare to independent BFS oracle.
start=time.perf_counter()
N=12; edges=set()
for i in range(N):
    for j in range(N):
        if i!=j and rng.random()<0.12: edges.add((i,j))
for a,b in sorted(edges): store.add_fact(a,'edge',b,type_subject='Node',type_object='Node',status='observed')
rule={'id':'bench-transitive','version':'1.0.0','premises':[{'subject':{'var':'x'},'predicate':'edge','object':{'var':'y'}},{'subject':{'var':'y'},'predicate':'edge','object':{'var':'z'}}],'conclusions':[{'subject':{'var':'x'},'predicate':'edge','object':{'var':'z'},'type_subject':'Node','type_object':'Node'}]}
store.add_rule(rule)
infer=infer_mesh(store,max_rounds=32,max_new_facts=10000,rule_match_cap=20000)
# independent reachability oracle
adj={i:set() for i in range(N)}
for a,b in edges: adj[a].add(b)
reach=set(edges)
for k in range(N):
    for i in range(N):
        for j in range(N):
            if (i,k) in reach and (k,j) in reach: reach.add((i,j))
actual={(f['subject'],f['object']) for f in store.query_facts({'predicate':'edge'}) if isinstance(f['subject'],int) and isinstance(f['object'],int)}
missing=sorted(reach-actual); extra=sorted(actual-reach)
record('MESH-001','independent graph-closure oracle',f'all {len(reach)} reachable pairs; no extra pairs',f'{len(actual)} pairs; missing={len(missing)} extra={len(extra)}', 'PASS' if not missing and not extra else 'FAIL',{'nodes':N,'input_edges':len(edges),'closure_pairs':len(reach),'new_facts':infer['new_fact_count'],'status':infer['status'],'missing':missing[:25],'extra':extra[:25]},time.perf_counter()-start)

# 3. Typed fact identity: same SPO/context/status but different declared object type.
start=time.perf_counter(); typed_store=Store(tmp/'typed.sqlite3')
typed_store.add_fact('s','p',7,type_subject='Entity',type_object='Int',status='observed')
typed_store.add_fact('s','q',7,type_subject='Entity',type_object='String',status='derived')
typed_store.add_rule({'id':'typed-rule','version':'1','premises':[{'subject':'s','predicate':'p','object':7}], 'conclusions':[{'subject':'s','predicate':'q','object':7,'type_subject':'Entity','type_object':'Int'}]})
typed_out=infer_mesh(typed_store,max_rounds=4,max_new_facts=20)
q_facts=typed_store.query_facts({'subject':'s','predicate':'q','object':7})
found_int=any(f['type_object']=='Int' and f['epistemic_status']=='derived' for f in q_facts)
record('MESH-002','typed identity collision', 'typed derived fact with object type Int', {'new_facts':typed_out['new_fact_count'],'q_fact_types':[f['type_object'] for f in q_facts]},'PASS' if found_int else 'FAIL',{'rule': 'same SPO but target type differs','reproduced_defect':not found_int},time.perf_counter()-start)

# 4. World model evaluation must reject output-type-invalid transitions; model currently only type-checks predict(), not evaluate().
start=time.perf_counter(); wm_store=Store(tmp/'world.sqlite3'); wm_engine=Engine(wm_store)
# register primitive components so model AST uses the ordinary runtime
from ngegenbrain.contracts import builtin_catalog
for comp in builtin_catalog(): wm_store.put_component(comp)
wm=WorldModelManager(wm_store,wm_engine)
wm.register({'id':'bad-output-type','version':'1','state_type':'Any','action_type':'Any','output_type':'Int','transition_program':{'op':'Const','value':'target'},'activation_policy':{'min_samples':6,'min_gain':0.1,'z_score':1.0}})
holdout=[{'id':f'h{i}','state':i,'action':'noop','observed_next_state':'target'} for i in range(10)]
# independent baseline intentionally wrong, same protocol and same inputs
report=wm.evaluate('bad-output-type',holdout,baseline_program={'op':'Const','value':'baseline'})
activation=report['evaluation']['activation'] if 'evaluation' in report else report.get('activation')
model_enabled=(activation or {}).get('enabled')
record('WM-001','world-model output contract', 'reject output type violation and prevent activation', {'activation':activation,'model_exact_match_rate':(report.get('evaluation') or report).get('model_exact_match_rate'),'record_keys':list(report.keys())},'PASS' if model_enabled is not True else 'FAIL',{'model_output_type':'Int','actual_transition_output':'String','reproduced_defect':model_enabled is True},time.perf_counter()-start)

# 5. Non-finite resource budgets should not disable resource guards.
start=time.perf_counter(); eng=Engine(store)
large='x'*200_000
finite=eng.run({'op':'Id'},large,budget={'steps':100,'cpu':100,'memory':1024,'time':10,'io':100,'external':0})
nan=eng.run({'op':'Id'},large,budget={'steps':100,'cpu':float('nan'),'memory':float('nan'),'time':float('nan'),'io':float('nan'),'external':float('nan')})
record('BUDGET-001','non-finite budget validation','non-finite limits rejected or treated conservatively; 200KB value cannot pass 1KB memory cap',{'finite_status':finite.status,'nonfinite_status':nan.status,'nonfinite_reason':nan.reason},'PASS' if finite.status!='Success' and nan.status!='Success' else 'FAIL',{'reproduced_defect':nan.status=='Success'},time.perf_counter()-start)

# 6. Check custom component cost NaN validation.
from ngegenbrain.contracts import validate_component_definition
start=time.perf_counter()
try:
    d=validate_component_definition({'id':'nan-cost','version':'1','input_types':['Any'],'output_type':'Any','implementation':'constant','value':1,'resource_cost':{'cpu':float('nan')},'effects':[],'required_capabilities':[],'pure':True})
    accepted=True
except Exception as e:
    accepted=False; err=f'{type(e).__name__}: {e}'
record('BUDGET-002','component resource_cost validation','NaN resource cost rejected',{'accepted':accepted,'error':None if accepted else err},'FAIL' if accepted else 'PASS',{'reproduced_defect':accepted},time.perf_counter()-start)

# 7. Event-chain concurrent append test.
start=time.perf_counter(); conc_store=Store(tmp/'concurrent.sqlite3')
errs=[]
def add_events(worker):
    try:
        for j in range(25): conc_store.append_event({'kind':'stress_event','worker':worker,'index':j})
    except Exception as e: errs.append({'worker':worker,'error':repr(e)})
with ThreadPoolExecutor(max_workers=8) as pool: list(pool.map(add_events,range(8)))
chain=conc_store.verify_event_chain(); count=len(conc_store.list_events(1000))
record('TRACE-001','concurrent event append/hash chain','200 events and valid hash chain',{'visible_events':count,'chain':chain,'errors':errs},'PASS' if count==200 and chain['valid'] and not errs else 'FAIL',{'workers':8,'events_each':25},time.perf_counter()-start)

# 8. Memory payload corruption detection.
start=time.perf_counter(); mem_store=Store(tmp/'mem.sqlite3'); mem_store.store_memory('m1','test',{'x':[1,2,3]})
with sqlite3.connect(mem_store.path) as con:
    blob=con.execute('SELECT payload_blob FROM memory_objects WHERE id=?',('m1',)).fetchone()[0]
    corrupt=bytearray(blob); corrupt[-5]^=0x5A
    con.execute('UPDATE memory_objects SET payload_blob=? WHERE id=?',(bytes(corrupt),'m1'))
read=mem_store.get_memory('m1',include_payload=True)
record('MEM-001','memory corruption detection','payload_error present and no payload trusted',{'payload_error':read.get('payload_error'),'payload_returned': 'payload' in read},'PASS' if read.get('payload_error') else 'FAIL',{'payload_error':read.get('payload_error')},time.perf_counter()-start)

# 9. Invalid rule should be rejected before persistence, not accepted.
start=time.perf_counter(); rule_store=Store(tmp/'rules.sqlite3')
invalid_rules=[{}, {'id':'bad','premises':[],'conclusions':[{'subject':'x','predicate':'p','object':'y'}]}, {'id':'missing-pred','premises':[{'subject':'x','object':'y'}],'conclusions':[{'subject':'x','predicate':'q','object':'y'}]}]
accepted=[]
for i,r in enumerate(invalid_rules):
    try:
        from ngegenbrain.mesh import validate_rule
        validate_rule(r); rule_store.add_rule(r); accepted.append(i)
    except Exception: pass
record('MESH-003','invalid rule admission','all three structurally invalid rules rejected',{'accepted_indices':accepted,'persisted_count':len(rule_store.get_rules())},'PASS' if not accepted and not rule_store.get_rules() else 'FAIL',{'reproduced_defect':bool(accepted)},time.perf_counter()-start)

# 10. Certificate tampering with unchanged and changed hash / active premises.
start=time.perf_counter(); cert_store=Store(tmp/'cert.sqlite3')
cert_store.add_fact('A','edge','B',status='observed')
cert_store.add_rule({'id':'r1','version':'1','premises':[{'subject':{'var':'x'},'predicate':'edge','object':{'var':'y'}}],'conclusions':[{'subject':{'var':'x'},'predicate':'reachable','object':{'var':'y'}}]})
cert_out=infer_mesh(cert_store)
derived=next(f for f in cert_out['new_facts'] if f['predicate']=='reachable')
orig=derived['certificate']; good=verify_certificate(cert_store,orig)
from copy import deepcopy
bad=deepcopy(orig); bad['conclusion']['object']='C'; bad['conclusion_hash']=__import__('ngegenbrain.util',fromlist=['sha256_json']).sha256_json(bad['conclusion'])
forged=verify_certificate(cert_store,bad)
record('CERT-001','certificate re-derivation','valid cert accepted; altered conclusion rejected even with recalculated hash',{'valid_certificate':good,'forged_certificate':forged},'PASS' if good['valid'] and not forged['valid'] else 'FAIL',{},time.perf_counter()-start)

# 11. Type checks: bool is never integer; random values across declared primitive types.
start=time.perf_counter(); type_errors=[]
for val in [True,False,None,0,1,1.5,'1',[],{}, {'$rational':[1,2]}]:
    result=eng.run({'op':'Call','component':'identity','args':[{'var':'input'}]},val,budget=100)
    # identity takes Any: all canonical JSON values should succeed except noncanonical runtime-only values (none here).
    if result.status!='Success': type_errors.append({'value':repr(val),'status':result.status,'reason':result.reason})
record('TYPE-001','mixed JSON values and typed identity','all 10 JSON-shaped input forms supported by Any identity',{'checks':10,'errors':type_errors},'PASS' if not type_errors else 'FAIL',{},time.perf_counter()-start)

# 12. No arbitrary source execution path: payloads attempt Python expressions as strings; must be inert/rejected.
start=time.perf_counter(); payload='__import__("os").system("echo SHOULD_NOT_RUN")'
inert=eng.run({'op':'Const','value':payload},None,budget=100)
record('SEC-001','source-in-data boundary','string remains inert data and process does not execute it',{'status':inert.status,'value_equals_payload':inert.value==payload,'value':inert.value},'PASS' if inert.status=='Success' and inert.value==payload else 'FAIL',{},time.perf_counter()-start)

# 13. Recursion/depth resilience: deep AST must return typed failure rather than bubble exception.
start=time.perf_counter(); deep={'op':'Id'}
for _ in range(1200): deep={'op':'Seq','steps':[deep]}
try:
    deepres=eng.run(deep,None,budget=2000); observed={'returned':True,'status':deepres.status,'reason':deepres.reason,'details':deepres.details}
    verdict='PASS' if deepres.status in {'Partial','Rejected','Failed'} else 'FAIL'
except BaseException as e:
    observed={'returned':False,'exception':type(e).__name__,'message':str(e)}; verdict='FAIL'
record('ROBUST-001','deeply nested AST','bounded typed rejection/failure instead of uncaught runtime exception',observed,verdict,{},time.perf_counter()-start)

# 14. Context-filter correctness: context is a formal part of a fact, not an ignorable field.
start=time.perf_counter(); ctx_store=Store(tmp/'context.sqlite3')
ctx_store.add_fact('alice','member','team',context={'tenant':'alpha'})
ctx_store.add_fact('bob','member','team',context={'tenant':'beta'})
ctx_results=ctx_store.query_facts({'predicate':'member','context':{'tenant':'alpha'}})
record('MESH-005','context-scoped fact queries','only the fact in the requested context is returned',{'subjects':[f['subject'] for f in ctx_results],'count':len(ctx_results)},'PASS' if len(ctx_results)==1 and ctx_results[0]['subject']=='alice' else 'FAIL',{'reproduced_defect':not (len(ctx_results)==1 and ctx_results[0]['subject']=='alice')},time.perf_counter()-start)

# 15. Match cap must bound unsuccessful partial joins, not just completed matches.
from unittest.mock import patch
import ngegenbrain.mesh as mesh_module
start=time.perf_counter(); cap_store=Store(tmp/'cap.sqlite3')
for pred, count in (('p0',10),('p1',10),('p2',10)):
    for i in range(count): cap_store.add_fact(f'{pred}-{i}',pred,'v')
cap_store.add_rule({'id':'cap-no-join','version':'1.0.0','premises':[
    {'subject':{'var':'x'},'predicate':'p0','object':'v'},
    {'subject':{'var':'y'},'predicate':'p1','object':'v'},
    {'subject':{'var':'z'},'predicate':'p2','object':'v'},
    {'subject':'absent','predicate':'never','object':{'triple':[{'var':'x'},{'var':'y'},{'var':'z'}]}}],
    'conclusions':[{'subject':{'var':'x'},'predicate':'impossible','object':{'var':'z'}}]})
original=mesh_module._match_premise; visits={'count':0}
def counted(premise,fact,env):
    visits['count']+=1
    return original(premise,fact,env)
with patch.object(mesh_module,'_match_premise',counted):
    cap_out=infer_mesh(cap_store,max_rounds=1,max_new_facts=10,rule_match_cap=1)
record('MESH-006','bounded unsuccessful join exploration','no more than one fact-match attempt when cap=1',{'observed_match_calls':visits['count'],'reported_status':cap_out['status'],'rule_match_attempts':cap_out['rule_match_attempts']},'PASS' if visits['count']<=1 and cap_out['status']=='BUDGET_EXHAUSTED' else 'FAIL',{'reproduced_defect':visits['count']>1 or cap_out['status']!='BUDGET_EXHAUSTED'},time.perf_counter()-start)

ENDED_AT=datetime.now(timezone.utc).isoformat(timespec='seconds')
try:
    from ngegenbrain import MODEL_ID, __version__
    model_id=MODEL_ID; model_version=__version__
except Exception:
    model_id='unknown'; model_version='unknown'
summary={'schema':'NGeGenBrain.IndependentHardBenchmark/1','benchmark_id':'NG0-INDEP-HARD-20261027-01','model_id':model_id,'model_version':model_version,'model_root':str(ROOT),'source_archive':str(SOURCE_ARCHIVE),'source_sha256':hashlib.sha256(SOURCE_ARCHIVE.read_bytes()).hexdigest(),'harness_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seed':SEED,'run_started':STARTED_AT,'run_ended':ENDED_AT,'database_path':str(db),'test_count':len(results),'passed':sum(r['verdict']=='PASS' for r in results),'failed':sum(r['verdict']=='FAIL' for r in results),'tests':results,'environment':{'python':sys.version,'python_implementation':platform.python_implementation(),'platform':platform.platform(),'system':sys.platform}}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
print(json.dumps({'output':str(OUT),'model_id':summary['model_id'],'model_version':summary['model_version'],'source_sha256':summary['source_sha256'],'passed':summary['passed'],'failed':summary['failed'],'tests':[{'id':r['id'],'verdict':r['verdict'],'observed':r['observed']} for r in results]},ensure_ascii=False,indent=2,default=str))
