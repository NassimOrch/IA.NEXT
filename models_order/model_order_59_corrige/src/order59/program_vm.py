from __future__ import annotations
from .core import Program

class ProgramVM:
    VERSION="O59_PROGRAM_VM_1"
    def __init__(self, context): self.ctx=context
    def type_check(self, program:Program):
        allowed={"Observe","Probe","Predict","Compare","Sequence","Compose","Branch","Iterate","Verify","Retrieve","Store","Backtrack","Act","Select","Rank","Replan","Loop"}
        seen=set()
        def walk(node):
            if not isinstance(node,tuple) or not node:return True
            op=node[0]
            if op in seen and op in {"Observe","Probe","Predict","Retrieve","Store","Verify"}: return True
            if op not in allowed:return False
            seen.add(op)
            return all(walk(x) for x in node[1:] if isinstance(x,tuple))
        return bool(walk(program.ast))
    def run(self, program:Program):
        if not self.type_check(program): raise ValueError("program type/operation check failed")
        return self.eval_node(program.ast)
    def eval_node(self,node):
        if not isinstance(node,tuple): return node
        op=node[0]
        if op=="Observe": return self.ctx.get("observation")
        if op=="Probe":
            p=self.ctx.get("probe"); o=self.ctx.get("observation"); return p.apply(o) if p and o else None
        if op=="Predict":
            m=self.ctx.get("predictor"); o=self.ctx.get("observation"); a=self.ctx.get("action");
            if not (m and o is not None): return None
            pred=m.predict(o,a)
            return float(pred.confidence)
        if op=="Compare":
            a=self.eval_node(node[1]); b=self.eval_node(node[2]); return (a>b)-(a<b)
        if op=="Sequence":
            self.eval_node(node[1]); return self.eval_node(node[2])
        if op=="Compose":
            self.eval_node(node[1]); return self.eval_node(node[2])
        if op=="Branch":
            a=self.eval_node(node[1]); return self.eval_node(node[1] if a else node[2])
        if op=="Iterate":
            v=None
            for _ in range(int(node[2])): v=self.eval_node(node[1])
            return v
        if op=="Verify":
            vf=self.ctx.get("verify"); return bool(vf()) if vf else False
        if op=="Retrieve":
            mem=self.ctx.get("memory"); return mem.retrieve(limit=1)[0] if mem and mem.retrieve(limit=1) else None
        if op=="Store":
            mem=self.ctx.get("memory");
            return mem.add("program_state",{"stored":True}) if mem else None
        if op=="Backtrack": return self.ctx.get("fallback_signal",0.0)
        if op=="Act": return self.ctx.get("action_executor",lambda a:None)(self.ctx.get("action"))
        if op=="Select": return self.ctx.get("select_signal",self.ctx.get("action_feature",0.0))
        if op=="Rank": return self.ctx.get("rank_signal",self.ctx.get("action_feature",0.0))
        if op=="Replan": return self.ctx.get("replan_signal",self.ctx.get("action_feature",0.0))
        if op=="Loop": return self.eval_node(("Iterate",node[1],node[2]))
        raise ValueError(f"unknown program op {op}")
