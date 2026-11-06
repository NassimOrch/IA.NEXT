from __future__ import annotations
class MetaController:
    VERSION="O59_META_1"
    def choose(self, deficit, context):
        vals=[]
        if deficit.Dobs>0: vals.append((deficit.Dobs,"PROBE"))
        if deficit.Dconstraint>0: vals.append((deficit.Dconstraint,"CONSTRAINT"))
        if deficit.Dcap>0: vals.append((deficit.Dcap,"SYNTHESIZE"))
        if deficit.Dtransfer>0: vals.append((deficit.Dtransfer,"TRANSFER"))
        if deficit.Dres>0: vals.append((deficit.Dres,"RESOURCE"))
        if deficit.Dsearch>0: vals.append((deficit.Dsearch,"IMAGINE"))
        vals.append((0.05,"SEARCH"))
        vals.append((0.04,"VERIFY"))
        return max(vals,key=lambda x:x[0])[1]
