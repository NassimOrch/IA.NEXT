from __future__ import annotations
from .core import Observation, Probe, canonical, stable_hash
import math

class GenericPerceiver:
    VERSION="O59_PERCEIVER_1"
    def encode(self, raw, modality=None):
        if modality is None:
            modality = self._infer_modality(raw)
        return Observation(canonical(raw), modality, source="environment", id=stable_hash(canonical(raw))[:16])
    def _infer_modality(self, x):
        try:
            from PIL import Image
            if isinstance(x,Image.Image): return "image"
        except Exception: pass
        if isinstance(x,str): return "text"
        if isinstance(x,(int,float,list,tuple,dict)): return "structured"
        try:
            import numpy as np
            if isinstance(x,np.ndarray): return "numeric_or_image"
        except Exception: pass
        return "opaque"

    def feature_vector(self, obs:Observation, limit=96):
        x=obs.value; vals=[]
        def walk(v, depth=0):
            if len(vals)>=limit or depth>4:return
            if isinstance(v,bool): vals.append(float(v)); return
            if isinstance(v,(int,float)) and math.isfinite(float(v)): vals.append(float(v)); return
            if isinstance(v,str):
                vals.extend([float(len(v)), float(sum(ch.isalpha() for ch in v)), float(sum(ch.isdigit() for ch in v))])
                for n in (1,2,3):
                    vals.extend([int(stable_hash(v[i:i+n])[:8],16)%1000/1000.0 for i in range(max(0,min(len(v)-n+1,8)))])
                return
            if isinstance(v,dict):
                vals.append(float(len(v)))
                for k in sorted(v,key=str)[:16]:
                    vals.append(int(stable_hash(str(k))[:8],16)%1000/1000.0); walk(v[k],depth+1)
                return
            if isinstance(v,(list,tuple)):
                vals.append(float(len(v)))
                for z in list(v)[:16]: walk(z,depth+1)
                return
            try:
                a=v.tolist(); walk(a,depth+1); return
            except Exception: return
        walk(x)
        while len(vals)<limit: vals.append(0.0)
        return vals[:limit]

class GenericProbeFactory:
    VERSION="O59_PROBE_FACTORY_1"
    def candidates(self, obs:Observation):
        ps=[Probe("type","generic",transform="type"), Probe("len","generic",transform="len"), Probe("hash8","generic",transform="hash:8")]
        x=obs.value
        if isinstance(x,dict):
            for k in sorted(x,key=str)[:32]:
                base=str(k)
                ps += [Probe("key="+base,"field",(k,),"identity"), Probe("keytype="+base,"field",(k,),"type"), Probe("keylen="+base,"field",(k,),"len"), Probe("keysign="+base,"field",(k,),"sign"), Probe("keybucket="+base,"field",(k,),"bucket")]
                v=x.get(k)
                if isinstance(v,(dict,list,tuple)):
                    for nk in (sorted(v,key=str)[:8] if isinstance(v,dict) else range(min(8,len(v)))):
                        ps.append(Probe("path="+base+":"+str(nk),"field",(k,nk),"identity"))
        elif isinstance(x,(list,tuple)):
            for i in range(min(16,len(x))): ps += [Probe(f"idx={i}","index",(i,),"identity"), Probe(f"idxlen={i}","index",(i,),"len")]
        elif isinstance(x,str):
            ps += [Probe("alpha_count","text",transform="len",provenance={"derived":"generic"})]
        return ps
