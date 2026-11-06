from __future__ import annotations
from itertools import product
from .core import Program, stable_hash
OPS=("Observe","Probe","Refine","ConstructConstraint","Predict","Imagine","Compare","Select","Rank","Branch","Loop","Store","Retrieve","Act","Verify","Backtrack","Replan")
class ProgramSynthesizer:
    VERSION="O59_PROGRAM_SYNTH_2"
    def __init__(self,max_depth=4,max_programs=4000): self.max_depth=max_depth; self.max_programs=max_programs
    def enumerate(self):
        yield from self._trees(self.max_depth)
    def _trees(self,depth):
        atoms=[(x,) for x in ("Observe","Probe","Predict","Imagine","Compare","Select","Rank","Verify","Backtrack","Replan","Retrieve","Store")]
        for a in atoms: yield Program("p-"+stable_hash(a)[:12],a,"generic->generic",provenance={"synth":self.VERSION})
        if depth<=1:return
        child=[]
        for p in self._trees(depth-1):
            child.append(p);
            if len(child)>=24:break
        for a,b in product(child,child):
            for op in ("Compose","Branch","Sequence"):
                ast=(op,a.ast,b.ast)
                yield Program("p-"+stable_hash(ast)[:12],ast,"generic->generic",provenance={"synth":self.VERSION})
        for a in child[:24]: yield Program("p-"+stable_hash(("Loop",a.ast,2))[:12],("Loop",a.ast,2),"generic->generic",provenance={"synth":self.VERSION})
    def synthesize(self,evaluator,budget=300):
        best=None; tested=0; seen=set()
        for p in self.enumerate():
            if p.program_id in seen: continue
            seen.add(p.program_id); tested+=1
            if tested>budget:break
            score=float(evaluator(p))
            if best is None or score>best[0]: best=(score,p)
        return {"program":best[1],"score":best[0],"tested":tested} if best else None
