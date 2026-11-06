from __future__ import annotations
from collections import defaultdict, Counter
from .core import Observation, Transition, WorldPrediction, stable_hash
import numpy as np

class PredictiveModel:
    VERSION="O59_PREDICTIVE_MODEL_1"
    def __init__(self):
        self.table=defaultdict(Counter); self.samples=[]; self.weights=None
    def _state_vec(self,obs):
        # generic state vector; it contains no benchmark label or target
        s=str(obs.value)
        base=[len(s),sum(c.isdigit() for c in s),sum(c.isalpha() for c in s)]
        base += [int(stable_hash(s[i:i+2])[:8],16)%1000/1000 for i in range(min(len(s),45))]
        return np.asarray(base+[0.0]*64,dtype=np.float32)[:48]

    def _action_vec(self,action):
        s=str(action); h=stable_hash(action)
        base=[len(s),sum(c.isdigit() for c in s),sum(c.isalpha() for c in s)]
        base += [int(h[i:i+2],16)/255.0 for i in range(0,16,2)]
        return np.asarray(base,dtype=np.float32)[:16]

    def _vec(self,obs,action=None):
        if action is None: return np.pad(self._state_vec(obs),(0,16)).astype(np.float32)[:64]
        return np.concatenate([self._state_vec(obs),self._action_vec(action)]).astype(np.float32)
    def update(self,tr:Transition):
        k=(stable_hash(tr.obs_before.value)[:16],stable_hash(tr.action)[:24])
        nxt=stable_hash(tr.obs_after.value)
        self.table[k][nxt]+=1; self.samples.append((self._vec(tr.obs_before,tr.action),stable_hash(tr.action),self._state_vec(tr.obs_after)))
        if len(self.samples)>=8:self._fit()
    def _fit(self):
        X=np.stack([x for x,_,_ in self.samples[-512:]]); Y=np.stack([y for _,_,y in self.samples[-512:]])
        self.weights=np.linalg.lstsq(np.c_[X,np.ones(len(X))],Y,rcond=None)[0]
    def predict(self,obs,action,horizon=1):
        k=(stable_hash(obs.value)[:16],stable_hash(action)[:24]); c=self.table.get(k)
        support=[]
        if c:
            tot=sum(c.values()); support=[{"hash":h,"prob":n/tot} for h,n in c.most_common()]
        vec=self._vec(obs,action)
        if self.weights is not None:
            nxt=(np.c_[vec.reshape(1,-1),np.ones(1)]@self.weights).reshape(-1)
            conf=min(0.99,0.1+0.01*len(self.samples))
        else: nxt=vec; conf=0.0
        return WorldPrediction(tuple(map(float,nxt[:64])),conf,support,horizon)
    def error(self,pred:WorldPrediction, obs_after):
        if pred.support:
            h=stable_hash(obs_after.value); return 0.0 if any(s['hash']==h for s in pred.support) else 1.0
        return min(2.0,float(np.mean((np.asarray(pred.state_features)-self._state_vec(obs_after))**2)))
    def multi_step(self,obs,actions):
        from .core import Observation
        cur=obs; out=[]
        for i,a in enumerate(actions,1):
            pred=self.predict(cur,a,i); out.append(pred)
            # Continue imagination in latent observation space using the predicted state.
            cur=Observation({"latent_state":list(pred.state_features)},"latent",source="world_model")
        return out
