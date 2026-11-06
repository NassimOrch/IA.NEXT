from pathlib import Path
import json,tempfile,sys
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from order80.general_hierarchical import HierarchicalGeneralEngine

def w(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
with tempfile.TemporaryDirectory() as td:
    t=Path(td); docs=t/'docs'; docs.mkdir(); out=t/'out'; task=t/'task.json'; refs=t/'refs.json'
    w(task,json.dumps({'title':'hierarchy','problem':'Determine two independent aspects of a documented requirement.','objective':'produce an evidence-backed answer','required_terms':['alpha','beta'],'verification':{'mode':'documentary','min_unique_sources':1},'subproblems':['Determine the alpha aspect from references.','Determine the beta aspect from references.']}))
    w(docs/'a.md','Alpha aspect is documented here.\n\nGeneral background is provided.')
    w(docs/'b.md','Beta aspect is documented here.\n\nGeneral background is provided.')
    w(refs,json.dumps({'local':[str(docs)],'web':{'enabled':False},'engine':{'duration':'2s','local_batch':1,'rag_batch':1,'chunk_size':800,'idle_sleep_seconds':0.01,'max_children_per_node':2}}))
    e=HierarchicalGeneralEngine(task,refs,out,out/'memory.json',json.loads(refs.read_text())['engine']); r=e.run()
    ev=[json.loads(x) for x in (out/'events.jsonl').read_text().splitlines()]
    names=[x['event'] for x in ev]
    assert 'node_decomposed' in names
    assert 'root_retest_after_subproblem' in names
    assert 'peer_probes_after_subproblem' in names
    assert r['status'] in {'TIME_BUDGET_EXPIRED','UNRESOLVED','INTERRUPTED'}
print('ORDER80.2.2 SELF-TEST PASS')
