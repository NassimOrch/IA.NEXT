from __future__ import annotations
from .core import Capability, stable_hash

class CapabilityManager:
    VERSION="O59_CAPABILITIES_2"
    def candidate(self, program, domain_signature, evidence): return Capability("cap-"+stable_hash(program.ast)[:12],program,tuple(domain_signature),evidence)
    def measure_policy_effect(self, off_scores, on_scores):
        import numpy as np
        a=np.asarray(off_scores,dtype=float); b=np.asarray(on_scores,dtype=float)
        return {"mean_effect":float(np.mean(b-a)) if a.size and b.size else 0.0,"max_abs_effect":float(np.max(np.abs(b-a))) if a.size and b.size else 0.0,"n":int(min(a.size,b.size))}
    def promote_causal(self,cap,off,on):
        # Positive effect must not reduce correctness. For minimization, lower cost is positive.
        valid=bool(off.get("verified") and on.get("verified"))
        delta=float(off.get("cost",1e9)-on.get("cost",1e9))
        promoted=valid and delta>0
        return {"status":"PROMOTED" if promoted else "REJECTED","causal_delta":delta,"capability_id":cap.id}
