from __future__ import annotations
from itertools import permutations
from .core import Transport, Regime, stable_hash

class TransferDiscovery:
    VERSION="O59_TRANSFER_DISCOVERY_1"
    def discover(self, source_features:dict, target_features:dict):
        # Structural discovery: match by invariant signatures, not names of benchmark families.
        mapping={}
        used=set()
        src=sorted(source_features.items(), key=lambda x:(str(x[1]),x[0]))
        tgt=sorted(target_features.items(), key=lambda x:(str(x[1]),x[0]))
        for sk,sv in src:
            candidates=[tk for tk,tv in tgt if tv==sv and tk not in used]
            if candidates: mapping[sk]=candidates[0]; used.add(candidates[0])
        score=len(mapping)/max(1,len(src)); return mapping,score
    def certify(self, mapping, source_runs, target_runner):
        if not mapping:return {"status":"REJECTED","reason":"no discovered correspondence"}
        checks=[]
        for x in source_runs[:4]: checks.append(bool(target_runner(x,mapping)))
        ok=sum(checks)>=max(1,len(checks)-1)
        return {"status":"VERIFIED" if ok else "REJECTED","checks":checks,"mapping":mapping}
