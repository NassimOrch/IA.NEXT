from __future__ import annotations
from itertools import combinations, product
from .core import Constraint, conjunction, disjunction, relaxation, stable_hash

class ConstraintInducer:
    VERSION="O59_CONSTRAINT_INDUCER_1"
    def __init__(self): self.history=[]
    def induce_from_assignments(self, variables, observations):
        # Generic candidates: distinctness and value stability. No problem family is referenced.
        cons=[]
        rows=[o for o in observations if isinstance(o,dict)]
        for a,b in combinations(variables,2):
            vals_a=[r.get(a) for r in rows if a in r and b in r]; vals_b=[r.get(b) for r in rows if a in r and b in r]
            if vals_a and vals_b and all(x!=y for x,y in zip(vals_a,vals_b)):
                cons.append(Constraint(f"neq:{a}:{b}",(a,b),"neq",lambda s,a=a,b=b: s.get(a)!=s.get(b),0.6,{"source":"induced"}))
        self.history.extend(cons); return cons
    def induce_from_interactions(self, transitions):
        # Accepted/rejected actions yield generic action-compatibility hypotheses.
        grouped={}
        for t in transitions:
            k=stable_hash(t.obs_before.value)[:16]
            grouped.setdefault(k,[]).append(t)
        out=[]
        for k,ts in grouped.items():
            rejected={str(t.action) for t in ts if t.accepted is False}
            accepted={str(t.action) for t in ts if t.accepted is True}
            if rejected and accepted:
                out.append(Constraint(f"action-compat:{k}",(),"interaction",lambda s: True,0.5,{"rejected":sorted(rejected)[:8]}))
        self.history.extend(out); return out

__all__=["ConstraintInducer","conjunction","disjunction","relaxation"]
