from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from .core import Regime,Transport,Probe,Observation,build_partition,stable_hash,minimum_double_ok,ultrametric_from_thresholds,Constraint

class ThresholdGeometry:
    VERSION="O59_THRESHOLD_GEOMETRY_1"
    def __init__(self,observations,ordered_probes): self.observations=observations; self.probes=ordered_probes
    def pair_thresholds(self):
        from .core import pair_thresholds
        return pair_thresholds(self.observations,self.probes)
    def measure(self):
        th=self.pair_thresholds(); counts=defaultdict(int)
        for v in th.values():counts[v]+=1
        n=max(1,len(th)); return {k:v/n for k,v in sorted(counts.items())}
    def curve(self,t):
        th=self.pair_thresholds(); return sum(1 for v in th.values() if t>v)/max(1,len(th))
    def verify(self):
        th=self.pair_thresholds(); return {"minimum_double":minimum_double_ok(th,len(self.observations)),"pairs":len(th)}
    def ultrametric(self):
        return ultrametric_from_thresholds(self.pair_thresholds())

class ClosureEngine:
    VERSION="O59_CLOSURE_1"
    def reduce(self,obs,probes,candidates):
        from .core import closure
        ids=closure(obs,probes,candidates); return [p for p in candidates if p.id in ids]

class CirculationEngine:
    VERSION="O59_CIRCULATION_1"
    def compatible(self,source:Regime,target:Regime,mapping):
        ok=all(mapping.get(x)==x or x in target.probe_ids for x in source.probe_ids)
        return Transport(source,target,mapping,bool(ok),{"engine":self.VERSION})
    def compose(self,t1:Transport,t2:Transport):
        if not(t1.compatible and t2.compatible): return Transport(t1.source,t2.target,{},False,{"reason":"incompatible"})
        m={k:t2.mapping.get(v,v) for k,v in t1.mapping.items()}; return Transport(t1.source,t2.target,m,True,{"parents":[t1.provenance,t2.provenance]})

class ReflectionEngine:
    VERSION="O59_REFLECTION_1"
    def reflect(self,representation_state):
        # Meta-observation is an executable transformation over the current observation regime.
        return {"probe_count":len(representation_state.get("probes",[])),"fiber_count":representation_state.get("fiber_count",0),"collision_pairs":representation_state.get("collision_pairs",0),"hash":stable_hash(representation_state),"idempotent":True}
