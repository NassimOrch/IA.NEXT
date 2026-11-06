from order59.core import Observation,Probe,build_partition,is_sufficient,factorize,pair_thresholds,minimum_double_ok,relaxation,Constraint
from order59.geometry import ThresholdGeometry,CirculationEngine,ReflectionEngine

def test_factorization_and_insufficiency():
    obs=[Observation({'x':0,'y':0},'s'),Observation({'x':0,'y':1},'s'),Observation({'x':1,'y':0},'s')]
    px=Probe('x','field',('x',)); py=Probe('y','field',('y',))
    target=[0,1,2]
    ok,_,_=is_sufficient(obs,target,[px,py]); assert ok
    m,w=factorize(obs,[px,py],target); assert w is None and len(m)==3
    ok,w,_=is_sufficient(obs,[0,1,0],[px]); assert not ok and w is not None

def test_refinement_never_merges_and_thresholds():
    obs=[Observation({'a':1,'b':0},'s'),Observation({'a':1,'b':1},'s'),Observation({'a':2,'b':1},'s')]
    pa=Probe('a','field',('a',)); pb=Probe('b','field',('b',))
    p1=build_partition(obs,[pa]); p2=build_partition(obs,[pa,pb]);
    assert all(set(v).issubset(set(next(kv for kv in p1.groups.values() if v[0] in kv))) for v in p2.groups.values())
    th=pair_thresholds(obs,[pa,pb]); assert minimum_double_ok(th,3)
    g=ThresholdGeometry(obs,[pa,pb]); assert g.verify()['minimum_double']

def test_constraint_relax_uses_both_inputs():
    c1=Constraint('c1',('x',),'p',lambda s:s.get('x')==1)
    c2=Constraint('c2',('x',),'q',lambda s:s.get('x')==2)
    r=relaxation(c1,c2)
    assert r.holds({'x':1}) and r.holds({'x':2}) and not r.holds({'x':3})

def test_circulation_and_reflection():
    from order59.core import Regime
    r1=Regime('a',('p',),0); r2=Regime('b',('p','q'),1)
    t=CirculationEngine().compatible(r1,r2,{'p':'p'}); assert t.compatible
    ref=ReflectionEngine().reflect({'probes':['p'],'fiber_count':2,'collision_pairs':1})
    assert ref['idempotent'] and ref['fiber_count']==2
