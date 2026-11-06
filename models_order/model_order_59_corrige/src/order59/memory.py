from __future__ import annotations
from dataclasses import dataclass,asdict
import json,time
from .core import stable_hash

@dataclass
class MemoryItem:
    kind:str; payload:dict; fingerprint:str; status:str="active"; version:int=1; timestamp:float=time.time(); provenance:dict=None

class MemorySystem:
    VERSION="O59_MEMORY_1"
    def __init__(self,max_items=10000): self.items=[]; self.max_items=max_items
    def add(self,kind,payload,fingerprint=None,provenance=None):
        r=MemoryItem(kind,payload,fingerprint or stable_hash(payload),"active",1,time.time(),provenance or {}); self.items.append(r); self.items=self.items[-self.max_items:]; return r
    def retrieve(self,kind=None,query=None,limit=20):
        out=[x for x in reversed(self.items) if (kind is None or x.kind==kind) and x.status=="active"]
        if query is not None: out=[x for x in out if query in json.dumps(x.payload,sort_keys=True,default=str)]
        return out[:limit]
    def invalidate(self,fingerprint,reason):
        for r in reversed(self.items):
            if r.fingerprint==fingerprint and r.status=="active": r.status="INVALIDATED"; r.provenance=(r.provenance or {})|{"reason":reason}; return r
        return None
    def replace(self,fingerprint,payload,evidence):
        old=self.invalidate(fingerprint,"replacement")
        return self.add("semantic",payload,fingerprint=fingerprint,provenance={"replaced":old.fingerprint if old else None,"evidence":evidence})
