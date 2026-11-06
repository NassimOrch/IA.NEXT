from __future__ import annotations
from dataclasses import dataclass
from .core import Hypothesis, Deficit, stable_hash, ActionProposal

class ImaginationEngine:
    VERSION="O59_IMAGINATION_1"
    def __init__(self, max_depth=4, width=16): self.max_depth=max_depth; self.width=width; self.calls=0
    def hypotheses(self, context):
        hs=[]
        for kind,payload in [
            ("probe",{"mode":"more_observation"}),
            ("constraint",{"mode":"test_invariant"}),
            ("program",{"mode":"compose_known_ops"}),
            ("action_sequence",{"length":2}),
            ("representation","mode=change_resolution"),
        ]:
            hs.append(Hypothesis(stable_hash((kind,payload,context.get('step',0)))[:12],kind,payload,provenance={"engine":self.VERSION}))
        return hs[:self.width]
    def simulate(self, hypothesis:Hypothesis, simulator, state, actions):
        self.calls+=1
        result=simulator(hypothesis,state,actions)
        return result
    def select(self, candidates, scorer):
        scored=[]
        for h in candidates:
            s=float(scorer(h)); h.score=s; scored.append(h)
        return max(scored,key=lambda h:h.score,default=None)
