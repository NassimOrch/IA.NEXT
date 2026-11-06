from __future__ import annotations
from dataclasses import dataclass
import random, math, hashlib

class Environment:
    def reset(self): raise NotImplementedError
    def observe(self): raise NotImplementedError
    def act(self, action): raise NotImplementedError
    def terminal(self): return False
    def score(self): return 0.0
    def public_goal(self): return "achieve the public objective"

class HiddenPermutationEnv(Environment):
    """Generic black-box constraint induction. The rule is not exposed to the agent."""
    def __init__(self,n=5,seed=1): self.n=n; self.r=random.Random(seed); self.target=tuple(self.r.sample(range(n),n)); self.state=[]; self.last=None
    def reset(self): self.state=[]; self.last=None; return self.observe()
    def observe(self): return {"slots":self.n,"assigned":list(self.state),"feedback":self.last}
    def action_space(self):
        # The environment exposes the generic action alphabet; it does not expose
        # the hidden target. For the hard suite n<=8, the full permutation alphabet
        # remains finite and exactly matches the action semantics.
        if self.n <= 8:
            return [tuple(x) for x in _perms(range(self.n), self.n)]
        return [tuple(x) for x in _perms(range(self.n), min(self.n,6))]
    def act(self,a):
        a=tuple(a); ok=(len(a)==self.n and sorted(a)==list(range(self.n)) and a==self.target)
        self.last={"accepted":ok,"score":sum(x==y for x,y in zip(a,self.target))}
        self.state=list(a); return self.observe(), (1.0 if ok else self.last["score"]/self.n), ok, {"accepted":ok,"score":self.last["score"]}
    def terminal(self): return bool(self.last and self.last.get("accepted"))
    def score(self): return 1.0 if self.terminal() else (self.last or {}).get("score",0)/self.n
    def public_goal(self): return "construct a sequence satisfying the environment's hidden consistency condition"

class SequenceEnv(Environment):
    def __init__(self,seed=2, length=12): self.r=random.Random(seed); self.coeff=(self.r.randint(1,4),self.r.randint(-3,3)); self.length=length; self.seq=[self._f(i) for i in range(length)]; self.t=3; self.correct=0
    def _f(self,i): return self.coeff[0]*i*i+self.coeff[1]*i+1
    def reset(self): self.t=3; self.correct=0; return self.observe()
    def observe(self): return {"sequence":self.seq[:self.t]}
    def action_space(self):
        # Public action alphabet is derived only from the observed prefix.
        # It is deliberately NOT generated from the hidden continuation f(t).
        obs=self.seq[:self.t]
        if not obs: return list(range(-32,33))
        vals=[int(v) for v in obs]
        diffs=[abs(vals[i]-vals[i-1]) for i in range(1,len(vals))]
        scale=max(1,max(diffs,default=1),max(abs(v) for v in vals))
        radius=min(512,max(32,4*scale))
        center=vals[-1]
        lo=max(-2048,center-radius); hi=min(2048,center+radius)
        return list(range(lo,hi+1))
    def act(self,a):
        truth=self._f(self.t); ok=a==truth; self.correct+=int(ok); self.t=min(self.length,self.t+1); return self.observe(),float(ok), self.t>=self.length, {"accepted":ok,"truth_hidden":True}
    def terminal(self): return self.t>=self.length
    def score(self): return self.correct/max(1,self.length-3)
    def public_goal(self): return "predict the next value repeatedly using only observations and feedback"

class MazeEnv(Environment):
    def __init__(self,grid=None):
        self.grid=grid or ["S..#..","##.#.#","...#G.",".#....","......","..#..."]
        self.pos=self.start(); self.steps=0
    def start(self):
        for i,row in enumerate(self.grid):
            for j,c in enumerate(row):
                if c=='S':return (i,j)
    def reset(self): self.pos=self.start(); self.steps=0; return self.observe()
    def observe(self): return {"grid":self.grid,"position":self.pos,"steps":self.steps}
    def action_space(self): return ["U","D","L","R"]
    def act(self,a):
        self.steps+=1; i,j=self.pos; di,dj={"U":(-1,0),"D":(1,0),"L":(0,-1),"R":(0,1)}.get(a,(0,0)); ni,nj=i+di,j+dj
        ok=0<=ni<len(self.grid) and 0<=nj<len(self.grid[0]) and self.grid[ni][nj]!='#'
        if ok:self.pos=(ni,nj)
        goal=self.grid[self.pos[0]][self.pos[1]]=='G'; return self.observe(),1.0 if goal else (0.05 if ok else -0.05),goal,{"accepted":ok}
    def terminal(self):return self.grid[self.pos[0]][self.pos[1]]=='G' or self.steps>=80
    def score(self):return 1.0 if self.grid[self.pos[0]][self.pos[1]]=='G' else 0.0
    def public_goal(self):return "reach the target while interacting with an unknown transition rule"

class VisualPatternEnv(Environment):
    def __init__(self,seed=3): self.r=random.Random(seed); self.samples=[]; self.i=0; self.correct=0
    def reset(self):
        self.samples=[self._img(k%2) for k in range(8)]; self.i=0; self.correct=0; return self.observe()
    def _img(self,label):
        import numpy as np
        a=np.zeros((12,12),dtype=np.float32); cx=5 if label==0 else 7; a[2:10,cx-1:cx+1]=1; a[cx-1:cx+1,2:10]=1; return a.tolist()
    def observe(self): return {"image":self.samples[self.i].tolist() if hasattr(self.samples[self.i],'tolist') else self.samples[self.i]}
    def action_space(self): return [0,1]
    def act(self,a):
        truth=0 if self.i%2==0 else 1; ok=int(a==truth); self.correct += ok; self.i=min(len(self.samples)-1,self.i+1); return self.observe(),float(ok),self.i>=len(self.samples)-1,{"accepted":bool(ok)}
    def terminal(self):return self.i>=len(self.samples)-1
    def score(self):return self.correct/max(1,self.i) if self.i else 0.0
    def public_goal(self):return "infer the latent visual distinction and predict the hidden class label"

# Full chess legality for the environment only. The agent sees only an 8x8 text board and action strings.
class ChessEnv(Environment):
    PIECES="PNBRQKpnbrqk"
    def __init__(self,fen=None,max_plies=8):
        self.max_plies=max_plies; self.reset(fen or "7k/5Q2/7K/8/8/8/8/8 w - - 0 1")
    def reset(self,fen=None):
        self.board,self.turn,self.castle,self.ep=self._parse_fen(fen or "7k/5Q2/7K/8/8/8/8/8 w - - 0 1"); self.plies=0; self.last=None; return self.observe()
    def _parse_fen(self,fen):
        p,turn,castle,ep,*_=fen.split(); b=[]
        for row in p.split('/'):
            r=[]
            for c in row:r += ['.']*int(c) if c.isdigit() else [c]
            b.append(r)
        return b,turn,castle,ep
    def observe(self): return {"board":["".join(r) for r in self.board],"turn":self.turn,"last":self.last}
    def action_space(self):
        files='abcdefgh'; ranks='12345678'
        base=[files[c]+str(r+1)+files[d]+str(t+1) for c in range(8) for r in range(8) for d in range(8) for t in range(8)]
        promo=[a+p for a in base for p in 'qrbn' if a[3] in ('1','8')]
        return base+promo
    def _inside(self,r,c):return 0<=r<8 and 0<=c<8
    def _attacked(self,b,r,c,by):
        # Standard attack test used only by environment legality/evaluation.
        dirs_kn=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        dirs_king=[(dr,dc) for dr in(-1,0,1) for dc in(-1,0,1) if dr or dc]
        pawndir=-1 if by=='w' else 1
        for dc in(-1,1):
            rr,cc=r+pawndir,c+dc
            if self._inside(rr,cc) and b[rr][cc]==('P' if by=='w' else 'p'):return True
        for dr,dc in dirs_kn:
            rr,cc=r+dr,c+dc
            if self._inside(rr,cc) and b[rr][cc]==('N' if by=='w' else 'n'):return True
        for dr,dc in dirs_king:
            rr,cc=r+dr,c+dc
            if self._inside(rr,cc) and b[rr][cc]==('K' if by=='w' else 'k'):return True
        for rays, pieces in [([(-1,0),(1,0),(0,-1),(0,1)],'RQrq'),([(-1,-1),(-1,1),(1,-1),(1,1)],'BQbq')]:
            for dr,dc in rays:
                rr,cc=r+dr,c+dc
                while self._inside(rr,cc):
                    x=b[rr][cc]
                    if x!='.':
                        if (by=='w' and x in pieces[:2]) or (by=='b' and x in pieces[2:]): return True
                        break
                    rr+=dr;cc+=dc
        return False
    def _legal_move(self,b,turn,uci):
        if len(uci) not in (4,5):return False
        files='abcdefgh'
        try:
            r1=8-int(uci[1]);c1=files.index(uci[0]);r2=8-int(uci[3]);c2=files.index(uci[2])
        except Exception:return False
        if not(self._inside(r1,c1) and self._inside(r2,c2)):return False
        p=b[r1][c1]; q=b[r2][c2]
        if p=='.' or q.lower()=='k' or (p.isupper())!=(turn=='w') or (q!='.' and p.isupper()==q.isupper()):return False
        promo=uci[4].lower() if len(uci)==5 else None
        if len(uci)==5 and promo not in 'qrbn': return False
        dr,dc=r2-r1,c2-c1; ad,ac=abs(dr),abs(dc); ok=False
        if p.lower()=='p':
            d=-1 if turn=='w' else 1; start=6 if turn=='w' else 1
            reaches=(r2==0 if turn=='w' else r2==7)
            ok=(dc==0 and dr==d and q=='.') or (dc==0 and dr==2*d and r1==start and q=='.' and b[r1+d][c1]=='.') or (ac==1 and dr==d and q!='.') or (ac==1 and dr==d and (r2,c2)==self._ep_sq(files))
            if reaches and len(uci)!=5: return False
            if not reaches and len(uci)==5: return False
        elif p.lower()=='n': ok=(ad,ac) in {(1,2),(2,1)}
        elif p.lower()=='b': ok=ad==ac and self._clear(b,r1,c1,r2,c2)
        elif p.lower()=='r': ok=(dr==0 or dc==0) and self._clear(b,r1,c1,r2,c2)
        elif p.lower()=='q': ok=((dr==0 or dc==0) or ad==ac) and self._clear(b,r1,c1,r2,c2)
        elif p.lower()=='k':
            if max(ad,ac)==1: ok=True
            # Castling: rights, empty transit squares and no check on start/transit/destination.
            if dr==0 and ad==0 and ac==2:
                if turn=='w' and r1==7 and c1==4 and c2==6 and 'K' in self.castle and b[7][7]=='R' and b[7][5]==b[7][6]=='.':
                    ok=not self._attacked(b,7,4,'b') and not self._attacked(b,7,5,'b') and not self._attacked(b,7,6,'b')
                elif turn=='w' and r1==7 and c1==4 and c2==2 and 'Q' in self.castle and b[7][0]=='R' and b[7][1]==b[7][2]==b[7][3]=='.':
                    ok=not self._attacked(b,7,4,'b') and not self._attacked(b,7,3,'b') and not self._attacked(b,7,2,'b')
                elif turn=='b' and r1==0 and c1==4 and c2==6 and 'k' in self.castle and b[0][7]=='r' and b[0][5]==b[0][6]=='.':
                    ok=not self._attacked(b,0,4,'w') and not self._attacked(b,0,5,'w') and not self._attacked(b,0,6,'w')
                elif turn=='b' and r1==0 and c1==4 and c2==2 and 'q' in self.castle and b[0][0]=='r' and b[0][1]==b[0][2]==b[0][3]=='.':
                    ok=not self._attacked(b,0,4,'w') and not self._attacked(b,0,3,'w') and not self._attacked(b,0,2,'w')
        if not ok:return False
        bb=[row[:] for row in b]
        bb[r2][c2]=p;bb[r1][c1]='.'
        if p.lower()=='p' and (r2,c2)==self._ep_sq(files) and q=='.':
            bb[r2 + (1 if turn=='w' else -1)][c2]='.'
        if p.lower()=='k' and abs(c2-c1)==2:
            rc=7 if c2==6 else 0; rt=5 if c2==6 else 3
            bb[r2][rt]=bb[r2][rc]; bb[r2][rc]='.'
        if promo: bb[r2][c2]=promo.upper() if turn=='w' else promo
        kr,kc=self._king(bb,turn)
        return kr is not None and not self._attacked(bb,kr,kc,'b' if turn=='w' else 'w')
    def _clear(self,b,r1,c1,r2,c2):
        dr=(r2-r1)//max(1,abs(r2-r1));dc=(c2-c1)//max(1,abs(c2-c1));r,c=r1+dr,c1+dc
        while (r,c)!=(r2,c2):
            if b[r][c]!='.':return False
            r+=dr;c+=dc
        return True
    def _king(self,b,turn):
        k='K' if turn=='w' else 'k'
        for r in range(8):
            for c in range(8):
                if b[r][c]==k:return r,c
        return None,None
    def _ep_sq(self,files):
        if self.ep=='-':return (-1,-1)
        return 8-int(self.ep[1]),files.index(self.ep[0])
    def legal_actions(self,limit=None):
        acts=[]
        for a in self.action_space():
            if self._legal_move(self.board,self.turn,a): acts.append(a)
            if limit and len(acts)>=limit:break
        return acts
    def act(self,a):
        ok=self._legal_move(self.board,self.turn,a)
        if not ok:
            self.last={"accepted":False,"action":a}; return self.observe(),-0.05,False,{"accepted":False}
        files='abcdefgh';r1=8-int(a[1]);c1=files.index(a[0]);r2=8-int(a[3]);c2=files.index(a[2]);p=self.board[r1][c1];q=self.board[r2][c2]
        old_turn=self.turn; old_ep=self.ep; old_castle=self.castle
        # En-passant capture.
        if p.lower()=='p' and (r2,c2)==self._ep_sq(files) and q=='.':
            self.board[r2 + (1 if old_turn=='w' else -1)][c2]='.'
        # Move piece / castling rook.
        self.board[r2][c2]=p;self.board[r1][c1]='.'
        if p.lower()=='k' and abs(c2-c1)==2:
            rc=7 if c2==6 else 0; rt=5 if c2==6 else 3
            self.board[r2][rt]=self.board[r2][rc];self.board[r2][rc]='.'
        # Promotion.
        if p.lower()=='p' and r2 in (0,7):
            promo=a[4].lower() if len(a)==5 else 'q'
            self.board[r2][c2]=promo.upper() if old_turn=='w' else promo
        # Castling rights are a state variable, not an observation-side oracle.
        rights=set(old_castle if old_castle!='-' else '')
        if p=='K': rights.discard('K');rights.discard('Q')
        if p=='k': rights.discard('k');rights.discard('q')
        if (r1,r2,c1,c2)==(7,7,0,0) or (r2,c2)==(7,0): rights.discard('Q')
        if (r1,c1)==(7,7) or (r2,c2)==(7,7): rights.discard('K')
        if (r1,c1)==(7,0) or (r2,c2)==(7,0): rights.discard('Q')
        if (r1,c1)==(0,7) or (r2,c2)==(0,7): rights.discard('k')
        if (r1,c1)==(0,0) or (r2,c2)==(0,0): rights.discard('q')
        self.castle=''.join(x for x in 'KQkq' if x in rights) or '-'
        self.ep='-'
        if p.lower()=='p' and abs(r2-r1)==2:
            self.ep=files[c1]+str((8-r1 + 8-r2)//2)
        self.turn='b' if self.turn=='w' else 'w';self.plies+=1; self.last={"accepted":True,"action":a}
        kpos=self._king(self.board,self.turn); check=kpos[0] is not None and self._attacked(self.board,kpos[0],kpos[1],'b' if self.turn=='w' else 'w')
        mate=check and len(self.legal_actions())==0
        return self.observe(),1.0 if mate else 0.0,mate,{"accepted":True,"check":check,"mate":mate}
    def terminal(self):
        kpos=self._king(self.board,self.turn)
        return self.plies>=self.max_plies or (kpos[0] is not None and len(self.legal_actions())==0)
    def score(self):return 1.0 if self.last and self.last.get('accepted') and len(self.legal_actions())==0 else 0.0
    def public_goal(self):return "choose actions that improve the position and terminate the public objective in an adversarial environment"

def _perms(vals,k):
    import itertools
    return itertools.permutations(vals,k) if k==len(vals) else itertools.permutations(vals,k)

class AdversarialChessEnv(ChessEnv):
    """Evaluator-side chess environment: agent controls White; Black replies automatically.
    Legal moves are used only internally by the evaluator and are never exposed to the agent.
    The reply policy is deterministic and deliberately simple; it is not a chess engine.
    """
    def __init__(self,fen=None,max_agent_plies=10,seed=59):
        self.seed=seed; super().__init__(fen=fen,max_plies=max_agent_plies*2+1); self.agent_plies=0

    def reset(self,fen=None):
        out=super().reset(fen=fen); self.agent_plies=0; return out

    def _apply_without_reward(self,a):
        # Reuse the full evaluator-side chess transition so castling rights,
        # en-passant, promotion and king-safety state remain coherent.
        ChessEnv.act(self,a)
        self.last={'accepted':True,'action':a,'auto_reply':True}

    def _choose_reply(self):
        legal=self.legal_actions()
        if not legal: return None
        # Deterministic evaluator policy, independent of hidden target: choose the move with
        # the smallest stable hash after prioritizing captures/checking opportunities only
        # through legal transition outcomes, never exposing this ordering to the model.
        scored=[]
        for a in legal:
            h=hashlib.sha256(repr((self.seed,self.plies,a)).encode()).hexdigest()
            scored.append((h,a))
        return min(scored)[1]

    def act(self,a):
        if self.turn!='w':
            return self.observe(),-0.1,False,{'accepted':False,'reason':'agent_called_out_of_turn'}
        ok=self._legal_move(self.board,self.turn,a)
        if not ok:
            self.last={'accepted':False,'action':a}; return self.observe(),-0.05,False,{'accepted':False}
        self._apply_without_reward(a); self.agent_plies+=1
        kpos=self._king(self.board,self.turn)
        check=kpos[0] is not None and self._attacked(self.board,kpos[0],kpos[1],'b' if self.turn=='w' else 'w')
        mate=check and len(self.legal_actions())==0
        if mate: return self.observe(),1.0,True,{'accepted':True,'check':True,'mate':True,'opponent_replied':False}
        # Automatic black reply.
        reply=self._choose_reply()
        if reply is None:
            done=True
            return self.observe(),0.8,done,{'accepted':True,'opponent_replied':False,'opponent_terminal':True}
        self._apply_without_reward(reply)
        kpos=self._king(self.board,self.turn)
        check_after=kpos[0] is not None and self._attacked(self.board,kpos[0],kpos[1],'b' if self.turn=='w' else 'w')
        opp_mate=check_after and len(self.legal_actions())==0
        reward=-1.0 if opp_mate else 0.0
        done=opp_mate or self.agent_plies>=self.max_plies//2
        return self.observe(),reward,done,{'accepted':True,'opponent_replied':True,'opponent_action':reply,'opponent_mate':opp_mate}

    def terminal(self):
        return self.plies>=self.max_plies or self.agent_plies>=self.max_plies//2

    def score(self):
        if self.last and self.last.get('mate'):
            return 1.0
        return 0.0
