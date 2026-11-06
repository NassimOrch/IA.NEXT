from __future__ import annotations
from collections import defaultdict
from .core import Observation,Probe,build_partition,stable_hash

class EAAttention:
    VERSION='O59_EA_ATTENTION_1'
    def __init__(self): self.history=[]
    def predictive_signature(self,obs,transitions,horizon=1):
        key=stable_hash(obs.value)[:16]; vals=[]
        for t in transitions:
            if stable_hash(t.obs_before.value)[:16]==key: vals.append(stable_hash(t.obs_after.value)[:16])
        return tuple(sorted(vals))
    def select(self,obs,probes,transitions):
        if not probes:return None
        base=build_partition([t.obs_before for t in transitions],[]).groups if transitions else {}
        scored=[]
        for p in probes:
            groups=defaultdict(list)
            for t in transitions:
                groups[stable_hash(p.apply(t.obs_before))].append(self.predictive_signature(t.obs_before,transitions))
            distinct=sum(len(set(v))>1 for v in groups.values())
            coverage=sum(1 for v in groups.values() if len(set(v))>1)
            score=distinct+0.01*coverage
            scored.append((score,-p.cost,-p.risk,p))
        return max(scored,key=lambda x:(x[0],x[1],x[2]))[3]
