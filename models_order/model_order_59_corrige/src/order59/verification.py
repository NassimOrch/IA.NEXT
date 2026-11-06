from __future__ import annotations
from .core import ActionProposal, Probe, build_partition, refinement_partition

class IndependentReasoningVerifier:
    VERSION = "O59_INDEPENDENT_REASONING_VERIFIER_1"
    def verify_action(self, proposal, actions):
        ok = proposal is not None and proposal.action in actions
        finite = isinstance(getattr(proposal,"score",None),(int,float)) and abs(float(proposal.score)) < 1e308 if proposal is not None else False
        return {"ok": bool(ok and finite), "reason": "valid-action-and-finite-score" if ok and finite else "invalid-action-or-score"}
    def verify_state(self, observations, probes, transitions):
        part = build_partition(observations, probes) if observations else None
        return {"ok": True, "observation_count": len(observations), "transition_count": len(transitions), "fiber_count": part.class_count() if part else 0, "collision_pairs": part.collision_pairs() if part else 0}
    def verify_refinement(self, old, new):
        return {"ok": refinement_partition(old,new), "monotone": refinement_partition(old,new)}
