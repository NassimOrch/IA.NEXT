from __future__ import annotations
from collections import defaultdict
from .core import stable_hash
class CanonicalLatent:
    VERSION='O59_CANONICAL_LATENT_1'
    def __init__(self): self.cells={}; self.edges=set(); self.reflections=[]
    def add(self, fingerprint, payload):
        k=stable_hash(fingerprint)[:16]; self.cells.setdefault(k,[]).append(payload); return k
    def connect(self,a,b,reason): self.edges.add((a,b,reason))
    def quotient(self): return {k:len(v) for k,v in self.cells.items()}
    def reflect(self):
        state={'cells':len(self.cells),'edges':len(self.edges)}; self.reflections.append(state); return state
