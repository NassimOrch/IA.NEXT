from __future__ import annotations
from dataclasses import dataclass
import random
import numpy as np
import torch
from torch import nn
from .core import stable_hash

@dataclass
class NeuralProbeProposal:
    probe_id: str
    score: float
    model_version: str

class NeuralProbeController:
    """A real neural proposer; it never certifies truth and only ranks generic probes."""
    VERSION="O59_NEURAL_PROBE_CONTROLLER_1"
    def __init__(self, input_dim=96, seed=59059):
        torch.manual_seed(seed); random.seed(seed); np.random.seed(seed)
        self.net=nn.Sequential(nn.Linear(input_dim,64),nn.Tanh(),nn.Linear(64,32),nn.Tanh(),nn.Linear(32,1))
        self.opt=torch.optim.Adam(self.net.parameters(),lr=0.01)
        self.examples=[]
    def fit(self, feature_rows, targets, epochs=40):
        if not feature_rows:return
        X=torch.tensor(np.asarray(feature_rows,dtype=np.float32)); y=torch.tensor(np.asarray(targets,dtype=np.float32)).reshape(-1,1)
        for _ in range(epochs):
            pred=self.net(X); loss=((pred-y)**2).mean(); self.opt.zero_grad(); loss.backward(); self.opt.step()
        self.examples.extend((list(map(float,x)),float(t)) for x,t in zip(feature_rows,targets))
    def score(self, feature):
        with torch.no_grad(): return float(self.net(torch.tensor(np.asarray(feature,dtype=np.float32))).reshape(()))
    def propose(self, probe_features):
        scored=[NeuralProbeProposal(pid,self.score(feat),self.VERSION) for pid,feat in probe_features]
        return sorted(scored,key=lambda z:-z.score)


class NeuralActionController:
    """Observation-conditioned action scorer; it predicts feedback, never truth.
    The input is a generic observation feature vector concatenated with generic
    action-shape/hash features. No benchmark family or legal-move oracle is used.
    """
    VERSION="O59_NEURAL_ACTION_CONTROLLER_1"
    def __init__(self, obs_dim=96, action_dim=16, seed=59059):
        torch.manual_seed(seed+17); random.seed(seed+17); np.random.seed(seed+17)
        self.net=nn.Sequential(nn.Linear(obs_dim+action_dim,64),nn.Tanh(),nn.Linear(64,32),nn.Tanh(),nn.Linear(32,1))
        self.opt=torch.optim.Adam(self.net.parameters(),lr=0.005)
        self.examples=[]
    @staticmethod
    def action_vector(action,dim=16):
        s=str(action); vals=[len(s),sum(c.isalpha() for c in s),sum(c.isdigit() for c in s)]
        h=stable_hash(action)
        vals.extend(int(h[i:i+2],16)/255.0 for i in range(0,2*(dim-3),2))
        return (vals+[0.0]*dim)[:dim]
    def vector(self,obs_features,action,observation=None):
        base=list(map(float,obs_features[:96]))
        # Generic observation identity channels make conditioning explicit even
        # when two different observations share the same low-order structural
        # statistics. These channels are derived only from the raw observation,
        # never from benchmark labels, solutions, legal moves, or domain names.
        if observation is not None:
            h=stable_hash(str(observation))
            base=base[:88] + [int(h[i:i+2],16)/255.0 for i in range(0,16,2)]
        return base[:96]+self.action_vector(action)
    def fit(self,rows,targets,epochs=2):
        if not rows:return
        X=torch.tensor(np.asarray(rows,dtype=np.float32)); y=torch.tensor(np.asarray(targets,dtype=np.float32)).reshape(-1,1)
        for _ in range(epochs):
            pred=self.net(X); loss=((pred-y)**2).mean(); self.opt.zero_grad(); loss.backward(); self.opt.step()
        self.examples.extend((list(map(float,x)),float(t)) for x,t in zip(rows,targets))
    def score(self,row):
        with torch.no_grad(): return float(self.net(torch.tensor(np.asarray(row,dtype=np.float32))).reshape(()))
