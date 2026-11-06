from __future__ import annotations
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict, field
from .core import Observation, Probe, Deficit, Transition, stable_hash, Clock, Budget, ActionProposal, Fingerprint, build_partition, Regime
from .perception import GenericPerceiver, GenericProbeFactory
from .neural import NeuralProbeController, NeuralActionController
from .prediction import PredictiveModel
from .constraints import ConstraintInducer
from .imagination import ImaginationEngine
from .synthesis import ProgramSynthesizer
from .memory import MemorySystem
from .capabilities import CapabilityManager
from .transfer import TransferDiscovery
from .meta import MetaController
from .attention import EAAttention
from .latent import CanonicalLatent
from .program_vm import ProgramVM
from .verification import IndependentReasoningVerifier
from .geometry import ThresholdGeometry, ClosureEngine, CirculationEngine
import math, time, random

@dataclass
class AgentConfig:
    budget: Budget=field(default_factory=Budget)
    max_probe_candidates:int=32
    max_probe_trials:int=12
    imagination_depth:int=3
    synth_budget:int=250
    seed:int=59059
    use_probes:bool=True
    use_imagination:bool=True
    use_synthesis:bool=True
    use_memory:bool=True
    use_world_model:bool=True
    use_neural:bool=True
    use_constraints:bool=True

class Order59Agent:
    VERSION="ORDER59_AGENT_1"
    def __init__(self,config=None):
        self.config=config or AgentConfig(); random.seed(self.config.seed)
        self.perceiver=GenericPerceiver(); self.probe_factory=GenericProbeFactory(); self.neural=NeuralProbeController(seed=self.config.seed); self.action_neural=NeuralActionController(seed=self.config.seed)
        self.predictor=PredictiveModel(); self.constraints=ConstraintInducer(); self.imagination=ImaginationEngine(self.config.imagination_depth)
        self.synth=ProgramSynthesizer(max_depth=3); self.memory=MemorySystem(); self.capabilities=CapabilityManager(); self.transfer=TransferDiscovery(); self.meta=MetaController(); self.attention=EAAttention(); self.latent=CanonicalLatent(); self.verifier=IndependentReasoningVerifier(); self.circulation=CirculationEngine(); self.closure=ClosureEngine(); self.reset()
    def reset(self):
        self.history=[]; self.transitions=[]; self.observations=[]; self.probes=[]; self.trace=[]; self.learned_constraints=[]; self.programs=[]; self.fibers=[]; self.current_repr=[]; self.stats=Counter(); self.start=None; self._adaptive_branch_limit=None
    def observe(self,raw):
        o=self.perceiver.encode(raw); self.observations.append(o); return o
    def _fingerprint(self,obs,probes): return tuple(stable_hash(p.apply(obs)) for p in probes)
    def _estimate_deficit(self,obs,action_space):
        D=Deficit(); reasons=[]
        # Observation deficit: collisions in past that produced different observed futures.
        groups=defaultdict(list)
        for i,t in enumerate(self.history): groups[self._fingerprint(t.obs_before,self.probes)].append(i)
        bad=0; pairs=0
        for ids in groups.values():
            for i in range(len(ids)):
                for j in range(i+1,len(ids)):
                    fi=self._future_sig(ids[i]); fj=self._future_sig(ids[j]); pairs+=1
                    if fi!=fj: bad+=1
        D.Dobs=bad/max(1,pairs)
        if D.Dobs>0: reasons.append('colliding observations have divergent observed consequences')
        # Constraint deficit emerges when interaction feedback is inconsistent with current learned candidates.
        D.Dconstraint=0.5 if self.config.use_constraints and any(t.accepted is False for t in self.transitions[-8:]) and not self.learned_constraints else 0.0
        # Search deficit from repeated rejected/visited actions.
        rej=sum(1 for t in self.transitions[-32:] if t.accepted is False)
        D.Dsearch=rej/max(1,min(16,len(action_space)))
        # Resource deficit is measured only from actual consumption.
        elapsed=time.perf_counter()-self.start if self.start else 0
        D.Dres=max(0.0, elapsed/self.config.budget.time_s-0.8)
        # Capability and transfer deficit are questions, not impossibility claims.
        D.Dcap=0.25 if len(self.transitions)>=4 and not self.programs else 0.0
        # Transfer deficit is evidence-driven. The existence of a memory item alone
        # is not a deficit; a deficit appears only after a remembered structure is
        # actually compared with the current observation and the discovered mapping
        # is insufficient.
        D.Dtransfer=0.0
        if self.config.use_memory:
            for item in self.memory.retrieve(kind='program',limit=8):
                src=item.payload.get('feature_signature') if isinstance(item.payload,dict) else None
                if not src: continue
                target=self.perceiver.feature_vector(obs)[:8]
                _,score=self.transfer.discover(
                    {f's{i}':v for i,v in enumerate(src)},
                    {f't{i}':v for i,v in enumerate(target)}
                )
                if score < 0.5: D.Dtransfer=max(D.Dtransfer,1.0-score)
        D.reason=tuple(reasons)
        return D
    def _future_sig(self,index):
        if index>=len(self.history): return None
        if index<0 or index>=len(self.history): return None
        t=self.history[index]
        return (stable_hash(t.obs_after.value)[:16], t.accepted, round(float(t.reward or 0),3))
    def _learn_probe_bank(self,obs):
        generic=self.probe_factory.candidates(obs)
        # Retain any previously discovered probes and exact deduplication.
        byid={p.id:p for p in self.probes};
        for p in generic: byid.setdefault(p.id,p)
        self.probes=list(byid.values())[:128]
        return self.probes
    def _active_probe(self, obs):
        cands=self._learn_probe_bank(obs)
        if not self.config.use_probes or not self.history or len(self.history)<2:return None
        scored=[]
        for p in cands:
            if p.id in {q.id for q in self.current_repr}:continue
            g=defaultdict(list)
            start=max(0,len(self.history)-64)
            for idx,t in enumerate(self.history[start:], start): g[stable_hash(p.apply(t.obs_before))].append(idx)
            splits=sum(1 for v in g.values() if len(v)>1)
            # information gain relative to current collisions using consequence diversity, no direct labels
            entropy_before=self._entropy([self._future_sig(i) for i in range(len(self.history))])
            entropy_after=0.0; total=len(self.history)
            for ids in g.values(): entropy_after += len(ids)/total*self._entropy([self._future_sig(i) for i in ids])
            gain=max(0.0,entropy_before-entropy_after)
            scored.append((gain/(p.cost+p.risk+1e-9),gain,splits,p))
        if not scored:return None
        # Neural proposer participates by reranking candidates using learned consequence data.
        feats=[]
        for _,gain,_,p in scored[:32]:
            vec=self.perceiver.feature_vector(obs)[:96]; feats.append((p.id,vec))
        nnrank=self.neural.propose(feats) if self.config.use_neural else []
        nnscore={x.probe_id:x.score for x in nnrank}
        scored.sort(key=lambda x:(x[0]+0.05*nnscore.get(x[3].id,0.0),x[1],x[2]),reverse=True)
        attention_cands=[p for p in cands if p.id not in {q.id for q in self.current_repr}]
        chosen=(max(scored,key=lambda x:(x[0],x[1],x[2]))[3] if scored else None)
        if self.transitions and attention_cands:
            att=self.attention.select(obs,attention_cands,self.transitions)
            att_row=next((row for row in scored if row[3].id==getattr(att,'id',None)),None)
            if att_row is not None and att_row[0] >= (chosen and next((row[0] for row in scored if row[3].id==chosen.id),-1)):
                chosen=att
        if chosen is not None:
            self.stats['probe_candidate_scores'] += len(scored)
        self.current_repr.append(chosen); self.stats['probe_calls']+=1; self.trace.append({'event':'active_probe','probe':chosen.id,'gain':scored[0][1],'utility':scored[0][0],'neural_score':nnscore.get(chosen.id,0.0)}); return chosen
    @staticmethod
    def _entropy(xs):
        c=Counter(map(str,xs)); n=sum(c.values()) or 1
        return -sum((v/n)*math.log((v/n)+1e-12,2) for v in c.values())
    def _representation_step(self,obs):
        if not self.current_repr:self._learn_probe_bank(obs); self.current_repr=[self.probes[0]] if self.probes else []
        for _ in range(min(self.config.max_probe_trials,max(0,len(self.observations)//2))):
            if not self.config.use_probes: break
            p=self._active_probe(obs)
            if not p:break
        part=build_partition(self.observations,self.current_repr) if self.current_repr else None
        self.fibers.append(part)
        geom=ThresholdGeometry(self.observations,self.current_repr) if self.current_repr else None
        geom_check=geom.verify() if geom and len(self.observations)>=3 else {'minimum_double':True,'pairs':0}
        closure_candidates=self.closure.reduce(self.observations,self.current_repr,self.probes) if self.current_repr else []
        self.stats['closure_candidates'] += len(closure_candidates)
        lkey=self.latent.add(tuple(p.id for p in self.current_repr),{'fiber_count':part.class_count() if part else 0}); refl=self.latent.reflect();
        self.trace.append({'event':'representation','probes':[p.id for p in self.current_repr],'fiber_count':part.class_count() if part else 0,'collision_pairs':part.collision_pairs() if part else 0,'latent_cell':lkey,'reflection':refl,'threshold_geometry':geom_check,'closure_probe_ids':[p.id for p in closure_candidates]})
        return part
    def _induce_constraints(self):
        # No hidden family/type is passed. Candidate relations arise solely from observed dictionaries and interactions.
        dict_rows=[]
        for o in self.observations[-32:]:
            if isinstance(o.value,dict) and isinstance(o.value.get('assignment'),dict): dict_rows.append(o.value['assignment'])
        if dict_rows:
            self.learned_constraints=self.constraints.induce_from_assignments(sorted({k for r in dict_rows for k in r}),dict_rows)
        interaction_constraints=self.constraints.induce_from_interactions(self.transitions[-64:])
        if interaction_constraints: self.learned_constraints.extend(interaction_constraints)
        if self.learned_constraints:self.stats['constraints_learned']+=len(self.learned_constraints)
    def _program_score(self,program):
        # A program is accepted only when it produces a numeric, non-constant signal
        # that correlates with observed rewards on held-out transitions. Mere AST
        # validity or a non-empty return value is never sufficient.
        if len(self.transitions) < 6:
            return -1.0
        vals=[]; ys=[]
        probe=self.current_repr[-1] if self.current_repr else (self.probes[0] if self.probes else None)
        n=len(self.transitions); split=max(3,int(n*0.6)); eval_transitions=self.transitions[split:]
        if len(eval_transitions)<3: eval_transitions=self.transitions[-3:]
        for t in eval_transitions:
            action_feature=(int(stable_hash(t.action)[:8],16)%100000)/100000.0
            ctx={'observation':t.obs_before,'action':t.action,'predictor':self.predictor,'memory':self.memory,
                 'action_score':0.0,'action_feature':action_feature,'rank_signal':action_feature,'select_signal':action_feature,
                 'probe':probe,'verify':lambda: False,'fallback_signal':0.0,'replan_signal':action_feature}
            try:
                v=ProgramVM(ctx).run(program)
                if not isinstance(v,(int,float)) or isinstance(v,bool):
                    return -1.0
                vals.append(float(v)); ys.append(float(t.reward or 0.0))
            except Exception:
                return -1.0
        if len(vals)<3 or max(vals)-min(vals)<1e-9:
            return -0.5 - 0.001*len(repr(program.ast))
        import numpy as np
        corr=float(np.corrcoef(np.asarray(vals),np.asarray(ys))[0,1]) if len(set(vals))>1 and len(set(ys))>1 else 0.0
        complexity=0.002*len(repr(program.ast))
        return corr-complexity

    def _program_policy_effect(self, program, enabled):
        if not self.observations: return 0.0
        obs=self.observations[-1]; vals=[]
        for a in [stable_hash(('a',i))[:8] for i in range(8)]:
            ctx={'observation':obs,'action':a,'predictor':self.predictor,'memory':self.memory,'action_score':0.0,'action_feature':(int(stable_hash(a)[:8],16)%100000)/100000.0,'rank_signal':0.0,'select_signal':0.0,'probe':self.current_repr[-1] if self.current_repr else None,'verify':lambda:False,'fallback_signal':0.0,'replan_signal':0.0}
            if enabled:
                try:
                    v=ProgramVM(ctx).run(program); vals.append(float(v) if isinstance(v,(int,float)) and not isinstance(v,bool) else 0.0)
                except Exception: vals.append(0.0)
            else: vals.append(0.0)
        return sum(vals)/max(1,len(vals))

    def _synthesize(self):
        if not self.config.use_synthesis: return None
        cached=self.memory.retrieve('program',limit=1) if self.config.use_memory else []
        if cached:
            p=ProgramVM({}).ctx if False else cached[0].payload.get('program_obj')
            if p is not None:
                self.programs.append(p); self.trace.append({'event':'program_retrieval','program':p.program_id}); return p
        out=self.synth.synthesize(self._program_score,self.config.synth_budget)
        if out and float(out.get('score',-1.0)) > 0.05:
            p=out['program'];p.status='tested';p.confidence=max(0.0,min(1.0,float(out['score']))) ; self.programs.append(p);
            if self.config.use_memory: self.memory.add('program',{'program_obj':p,'program_id':p.program_id,'feature_signature':self.perceiver.feature_vector(self.observations[-1])[:8] if self.observations else []},provenance={'source':'causal-synthesis'});
            self.trace.append({'event':'program_synthesis','program':p.program_id,'score':out['score'],'tested':out['tested'],'accepted':True}); self.stats['programs_synthesized']+=1
            return p
        if out:
            self.trace.append({'event':'program_synthesis','program':out['program'].program_id,'score':out['score'],'tested':out['tested'],'accepted':False})
            self.stats['programs_rejected']+=1
        return None
    def _generic_action_features(self, obs, action, predicted=None):
        s=str(action)
        return {'length':len(s),'hash':int(stable_hash(action)[:8],16)%1000/1000.0,'digit_count':sum(c.isdigit() for c in s),'letter_count':sum(c.isalpha() for c in s),'pred_conf':predicted.confidence if predicted else 0.0}
    def _generic_action_alternatives(self, obs, env):
        # The model receives only the generic action alphabet exposed by the environment.
        # No task-specific generator, heuristic, legal-move list or benchmark family is consulted.
        actions=list(env.action_space())
        if not actions:
            return []
        # Deterministic diversity-preserving sampling when the action alphabet exceeds the budget.
        limit=self._adaptive_branch_limit or self.config.budget.max_branches
        if len(actions) <= limit:
            return actions
        ranked=sorted(actions, key=lambda a: stable_hash((obs.id, repr(a))))
        return ranked[:limit]

    def _empirical_action_value(self, obs, action):
        # Task-agnostic feedback model: reuse an action only when its observed
        # fingerprint context matches the present observation. No target or
        # domain label is stored in the rule.
        if not self.transitions: return 0.0
        key=stable_hash(obs.value)[:16]
        vals=[]
        for t in self.transitions[-128:]:
            if stable_hash(t.obs_before.value)[:16]==key and str(t.action)==str(action) and t.reward is not None:
                vals.append(float(t.reward))
        return sum(vals)/len(vals) if vals else 0.0

    def _transfer_from_memory(self,obs):
        if not self.config.use_memory: return None
        programs=self.memory.retrieve(kind='program',limit=8)
        if not programs: return None
        target=self.perceiver.feature_vector(obs)[:8]
        for item in programs:
            src=item.payload.get('feature_signature')
            if not src: continue
            mapping,score=self.transfer.discover({f's{i}':v for i,v in enumerate(src)},{f't{i}':v for i,v in enumerate(target)})
            source_reg=Regime('memory-source',tuple(f's{i}' for i in range(len(src))),0)
            target_reg=Regime('current-target',tuple(f't{i}' for i in range(len(target))),1)
            transport=self.circulation.compatible(source_reg,target_reg,mapping)
            if mapping and score>=0.5 and transport.compatible:
                p=item.payload.get('program_obj')
                if p is not None and p.program_id not in {q.program_id for q in self.programs}:
                    self.programs.append(p)
                    self.trace.append({'event':'transfer_discovery','score':score,'mapping':mapping,'program':p.program_id})
                    return p
        self.trace.append({'event':'transfer_discovery','score':0.0,'mapping':{}})
        return None

    def _choose_action(self,env,obs):
        actions=self._generic_action_alternatives(obs,env)
        if not actions:return None
        # Avoid direct semantic/legal oracle: action_space is the generic environment action alphabet; legality is learned through act().
        actions=actions[:min(len(actions),self.config.budget.max_branches)]
        hypotheses=self.imagination.hypotheses({'step':len(self.transitions)}) if self.config.use_imagination else []
        # Each hypothesis is genuinely simulated through the world model and contributes an
        # action-specific score. We do not add a common constant to every candidate.
        candidates=[]
        evaluated=0
        for a in actions:
            if self.stats.get('action_evaluations',0) + evaluated >= self.config.budget.max_nodes:
                self.stats['resource_bound'] += 1
                break
            evaluated += 1
            pred=self.predictor.predict(obs,a,horizon=1) if self.config.use_world_model else None
            generic=self._generic_action_features(obs,a,pred)
            novelty=0.0 if any(str(t.action)==str(a) for t in self.transitions[-64:]) else 0.2
            neural_action_score=self.action_neural.score(self.action_neural.vector(self.perceiver.feature_vector(obs),a,observation=obs.value)) if self.config.use_neural else 0.0
            score=0.0
            if self.config.use_memory:
                oh=stable_hash(obs.value)[:16]
                past=self.memory.retrieve(kind='episode_step',query=oh,limit=8)
                for item in past:
                    if str(item.payload.get('action'))==str(a): score += 0.15
            score += 0.3*generic['pred_conf']+0.2*generic['hash']+0.15*generic['digit_count']+novelty+0.75*self._empirical_action_value(obs,a) + 0.25*neural_action_score
            if self.config.use_constraints and self.learned_constraints:
                state={'observation':obs.value,'action':a,'__action__':a}
                violations=sum(1 for c in self.learned_constraints if not c.holds(state))
                if violations: score -= 0.4*violations/max(1,len(self.learned_constraints))
            # No benchmark/domain-specific score is injected here. All action valuation is
            # derived from generic prediction, interaction feedback, novelty, neural proposal,
            # imagination and synthesized-program outputs.
            if self.programs:
                ctx={'observation':obs,'action':a,'predictor':self.predictor,'memory':self.memory,'action_score':score}
                pv=ProgramVM(ctx).run(self.programs[-1])
                if isinstance(pv,(int,float)): score += 0.12*float(pv)
                self.stats['program_effect_evaluations']+=1
            candidates.append(ActionProposal(a,score,program_id=self.programs[-1].program_id if self.programs else None))
        self.stats['action_evaluations'] += evaluated
        # Hypotheses are selected from actual internal counterfactual simulations.
        base=self._estimate_deficit(obs,actions)
        sim_rows=[]
        imagination_bonus=defaultdict(float)
        # Evaluate a bounded but diverse subset of candidate actions to keep the causal
        # mechanism computationally explicit without allowing it to dominate the whole budget.
        ordered=sorted(candidates,key=lambda c:c.score,reverse=True)
        imag_actions=[]
        seen_actions=set()
        for c in ordered[:32]:
            if c.action not in seen_actions: imag_actions.append(c.action); seen_actions.add(c.action)
        # Add deterministic diversity points from the remainder.
        stride=max(1,len(candidates)//32)
        for idx in range(0,len(candidates),stride):
            a=candidates[idx].action
            if a not in seen_actions and len(imag_actions)<64:
                imag_actions.append(a); seen_actions.add(a)
        def simulate(h,state,acts):
            hp=h.payload if isinstance(h.payload,dict) else {}
            chosen=acts[:max(1,min(len(acts),int(hp.get('length',1))))] if acts else []
            preds=self.predictor.multi_step(state,chosen) if (chosen and self.config.use_world_model) else []
            conf=sum(p.confidence for p in preds)/max(1,len(preds))
            return {'predicted_steps':len(preds),'simulation_confidence':conf,'actions':[repr(a) for a in chosen]}
        for h in hypotheses:
            h_best=None
            for act in imag_actions:
                result=self.imagination.simulate(h,simulate,obs,[act]) if self.config.use_imagination else None
                if result is not None:
                    utility=float(result.get('simulation_confidence',0.0))
                    imagination_bonus[stable_hash(act)]+=0.08*utility
                    h_best=(utility,act,result) if h_best is None or utility>h_best[0] else h_best
            if h_best:
                score,act,res=h_best; h.score=score; sim_rows.append((score,h,act,res))
        best_h=max(sim_rows,key=lambda x:x[0],default=None)
        if best_h:
            _,h,act,res=best_h
            self.trace.append({'event':'imagination_execution','selected':h.id,'hypothesis':h.kind,'action':repr(act),'base_deficit':base.vector(),'best_hypothesis_utility':float(h.score),**res})
            for c in candidates:
                c.hypothesis_id=h.id
                c.score += imagination_bonus.get(stable_hash(c.action),0.0)
        ordered=sorted(candidates,key=lambda c:c.score,reverse=True)
        for cand in ordered:
            check=self.verifier.verify_action(cand,actions)
            self.trace.append({'event':'independent_verification','action':repr(cand.action),'ok':check['ok'],'reason':check['reason']})
            if check['ok']: return cand
        return None
    def solve_episode(self,env):
        self.reset(); self.start=time.perf_counter(); raw=env.reset(); obs=self.observe(raw); self._representation_step(obs); self._induce_constraints()
        self.stats['action_evaluations']=0; self.stats['resource_bound']=0
        terminal=False
        for step in range(self.config.budget.max_steps):
            if time.perf_counter()-self.start > self.config.budget.time_s:
                self.stats['resource_bound']+=1; break
            D=self._estimate_deficit(obs, list(env.action_space()))
            mode=self.meta.choose(D,{'steps':step})
            self.trace.append({'event':'meta','decision':mode,'deficit':D.vector()})
            if mode=='PROBE': self._representation_step(obs)
            if mode=='CONSTRAINT': self._induce_constraints()
            if mode=='TRANSFER': self._transfer_from_memory(obs)
            if mode=='RESOURCE':
                ratio=max(0.2,min(1.0,1.0-D.Dres))
                self._adaptive_branch_limit=max(4,int(self.config.budget.max_branches*ratio))
                self.trace.append({'event':'resource_replan','branch_limit':self._adaptive_branch_limit})
            if mode=='VERIFY':
                vr=self.verifier.verify_state(self.observations,self.current_repr,self.transitions)
                self.trace.append({'event':'verify_state','result':vr})
            if (mode=='SYNTHESIZE' or (step>=3 and not self.programs)) and self.config.use_synthesis:self._synthesize()
            if mode=='IMAGINE': self.imagination.hypotheses({'step':step})
            proposal=self._choose_action(env,obs)
            if proposal is None: return {'status':StatusLike('UNKNOWN'),'score':env.score(),'trace':self.trace}
            before=obs; action=proposal.action; raw2,reward,terminal,info=env.act(action); obs2=self.observe(raw2); accepted = info.get("accepted") if isinstance(info,dict) else None
            tr=Transition(before,action,obs2,float(reward) if reward is not None else None,accepted,{'step':step,'mode':mode}); self.transitions.append(tr); self.predictor.update(tr); self.history.append(tr); self.memory.add('episode_step',{'step':step,'action':str(action),'reward':reward,'deficit':D.vector()},provenance={'agent':self.VERSION})
            if self.config.use_neural:
                self.action_neural.fit([self.action_neural.vector(self.perceiver.feature_vector(before),action,observation=before.value)],[float(reward or 0.0)],epochs=1)
            self._induce_constraints()
            if step >= 1 and step % 2 == 1:
                self._representation_step(obs)
            # Online learning of neural probe quality from consequence novelty.
            if self.config.use_neural and step % 4 == 0:
                fv=self.perceiver.feature_vector(before); target=min(1.0,max(0.0,(float(reward)+1)/2)); self.neural.fit([fv],[target],epochs=1)
            if terminal:
                break
        status='PASS' if env.score()>=0.999 else ('RESOURCE_BOUND' if self.stats['resource_bound'] else 'PARTIAL')
        return {'status':status,'score':env.score(),'steps':len(self.transitions),'trace':self.trace,'metrics':dict(self.stats),'memory_items':len(self.memory.items),'fibers':[(p.class_count(),p.collision_pairs()) for p in self.fibers],'programs':[asdict(p) for p in self.programs]}

class StatusLike:
    def __init__(self,x): self.value=x
