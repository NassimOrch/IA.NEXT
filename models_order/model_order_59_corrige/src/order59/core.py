from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict, Counter
from itertools import combinations
from typing import Any, Callable, Mapping, Sequence
import hashlib, json, math, time


def stable_hash(x: Any) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, default=str, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


class Status(str, Enum):
    PASS="PASS"; FAIL="FAIL"; VERIFIED="VERIFIED"; NOT_VERIFIED="NOT_VERIFIED"; UNKNOWN="UNKNOWN"
    RESOURCE_BOUND="RESOURCE_BOUND"; INVALID_INPUT="INVALID_INPUT"; NOT_APPLICABLE="NOT_APPLICABLE"; PARTIAL="PARTIAL"


@dataclass(frozen=True)
class Budget:
    time_s: float = 15.0
    max_steps: int = 1200
    max_nodes: int = 50000
    max_branches: int = 64
    max_memory: int = 10000


@dataclass(frozen=True)
class Observation:
    value: Any
    modality: str
    timestamp: float = field(default_factory=time.time)
    source: str = "environment"
    id: str = ""
    def as_dict(self):
        return {"value": self.value, "modality": self.modality, "timestamp": self.timestamp, "source": self.source, "id": self.id}


@dataclass(frozen=True)
class Probe:
    id: str
    kind: str
    path: tuple[Any, ...] = ()
    transform: str = "identity"
    cost: float = 1.0
    risk: float = 0.0
    provenance: dict = field(default_factory=dict)

    def apply(self, obs: Observation) -> Any:
        x = obs.value
        try:
            for p in self.path: x = x[p] if isinstance(x, (dict,list,tuple)) else getattr(x, p)
        except Exception:
            return None
        if self.transform == "identity": return canonical(x)
        if self.transform == "type": return type(x).__name__
        if self.transform == "len":
            try: return len(x)
            except Exception: return None
        if self.transform == "bucket":
            try:
                v=float(x); return int(math.floor(v*10.0))/10.0
            except Exception: return None
        if self.transform == "sign":
            try:
                v=float(x); return -1 if v<0 else (1 if v>0 else 0)
            except Exception: return None
        if self.transform.startswith("hash:"): return stable_hash(canonical(x))[:int(self.transform.split(":",1)[1])]
        return canonical(x)


def canonical(x: Any):
    if isinstance(x, dict): return {str(k): canonical(v) for k,v in sorted(x.items(), key=lambda kv:str(kv[0]))}
    if isinstance(x, (list, tuple)): return [canonical(v) for v in x]
    if hasattr(x, "tolist"):
        try: return canonical(x.tolist())
        except Exception: pass
    if isinstance(x, (int,float,str,bool)) or x is None: return x
    return str(x)


def freeze(x: Any) -> str:
    """Deterministic exact serialization used for hashable quotient keys."""
    return json.dumps(canonical(x), sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


@dataclass
class Fingerprint:
    probe_ids: tuple[str,...]
    key: tuple[Any,...]
    provenance: list[dict] = field(default_factory=list)


@dataclass
class Partition:
    groups: dict[tuple[Any,...], list[int]]
    def collision_pairs(self):
        return sum(n*(n-1)//2 for n in (len(v) for v in self.groups.values()))
    def class_count(self): return len(self.groups)


def build_partition(observations: Sequence[Observation], probes: Sequence[Probe]) -> Partition:
    g=defaultdict(list)
    for i,o in enumerate(observations): g[tuple(freeze(p.apply(o)) for p in probes)].append(i)
    return Partition(dict(g))


def is_sufficient(observations, target_values, probes):
    part=build_partition(observations,probes); witness=None
    for idxs in part.groups.values():
        vals={freeze(target_values[i]) for i in idxs}
        if len(vals)>1:
            witness=(idxs[0],idxs[1]); return False,witness,part
    return True,witness,part


def factorize(observations, probes, target_values):
    ok,witness,part=is_sufficient(observations,target_values,probes)
    if not ok: return None, witness
    mapping={}
    for idxs in part.groups.values(): mapping[tuple(freeze(probes[j].apply(observations[idxs[0]])) for j in range(len(probes)))] = canonical(target_values[idxs[0]])
    return mapping,None


def refinement_partition(part_old: Partition, part_new: Partition, observations=None) -> bool:
    # Every new cell must be contained in one old cell.
    old_by_item={i:k for k,vs in part_old.groups.items() for i in vs}
    for new_vs in part_new.groups.values():
        olds={old_by_item[i] for i in new_vs}
        if len(olds)>1: return False
    return True


def closure(observations: Sequence[Observation], probes: Sequence[Probe], candidates: Sequence[Probe]) -> set[str]:
    base=build_partition(observations, probes)
    out=set(p.id for p in probes)
    for c in candidates:
        if c.id in out: continue
        pc=build_partition(observations, list(probes)+[c])
        if pc.groups == base.groups: out.add(c.id)
    return out


def pair_thresholds(observations: Sequence[Observation], ordered_probes: Sequence[Probe]) -> dict[tuple[int,int], int]:
    out={}
    for i,j in combinations(range(len(observations)),2):
        k=0
        for p in ordered_probes:
            if p.apply(observations[i]) != p.apply(observations[j]): break
            k+=1
        out[(i,j)]=k
    return out


def minimum_double_ok(th: Mapping[tuple[int,int], float], n:int) -> bool:
    def t(i,j): return th[tuple(sorted((i,j)))]
    for i,j,k in combinations(range(n),3):
        if t(i,k)+1e-12 < min(t(i,j),t(j,k)): return False
    return True


def ultrametric_from_thresholds(th):
    return lambda i,j: 0.0 if i==j else math.exp(-float(th[tuple(sorted((i,j)))]))


@dataclass
class Constraint:
    id: str
    scope: tuple[str,...]
    relation: str
    predicate: Callable[[Mapping[str,Any]], bool]
    confidence: float = 0.5
    provenance: dict = field(default_factory=dict)
    status: str = "candidate"
    version: int = 1

    def holds(self,state):
        try: return bool(self.predicate(state))
        except Exception: return True


def conjunction(c1: Constraint,c2: Constraint)->Constraint:
    return Constraint("and:"+c1.id+":"+c2.id, tuple(dict.fromkeys(c1.scope+c2.scope)), "and", lambda s: c1.holds(s) and c2.holds(s), min(c1.confidence,c2.confidence), {"parents":[c1.id,c2.id]})

def disjunction(c1: Constraint,c2: Constraint)->Constraint:
    return Constraint("or:"+c1.id+":"+c2.id, tuple(dict.fromkeys(c1.scope+c2.scope)), "or", lambda s: c1.holds(s) or c2.holds(s), min(c1.confidence,c2.confidence), {"parents":[c1.id,c2.id]})

def refinement(c: Constraint, stronger: Constraint)->Constraint:
    return conjunction(c,stronger)

def relaxation(c: Constraint, weaker: Constraint)->Constraint:
    # Correct O55/O56 behavior: both inputs participate in the disjunctive relaxation.
    return disjunction(c,weaker)


@dataclass
class Deficit:
    Dobs: float = 0.0
    Dcap: float = 0.0
    Dres: float = 0.0
    Dsearch: float = 0.0
    Dtransfer: float = 0.0
    Dconstraint: float = 0.0
    reason: tuple[str,...] = ()
    def vector(self): return (self.Dobs,self.Dcap,self.Dres,self.Dsearch,self.Dtransfer,self.Dconstraint)
    def norm(self): return math.sqrt(sum(x*x for x in self.vector()))

    def delta(self, other):
        return tuple(a-b for a,b in zip(self.vector(), other.vector()))


@dataclass
class Hypothesis:
    id: str
    kind: str
    payload: dict
    parent: str | None = None
    score: float = 0.0
    status: str = "candidate"
    provenance: dict = field(default_factory=dict)


@dataclass
class ActionProposal:
    action: Any
    score: float
    program_id: str | None = None
    hypothesis_id: str | None = None
    reason: str = ""


@dataclass
class Transition:
    obs_before: Observation
    action: Any
    obs_after: Observation
    reward: float | None
    accepted: bool | None
    metadata: dict = field(default_factory=dict)


@dataclass
class Program:
    program_id: str
    ast: tuple
    type_signature: str
    preconditions: tuple[str,...] = ()
    effects: tuple[str,...] = ()
    provenance: dict = field(default_factory=dict)
    cost: float = 1.0
    confidence: float = 0.0
    status: str = "candidate"


@dataclass
class Capability:
    id: str
    program: Program
    domain_signature: tuple[Any,...]
    evidence: dict
    status: str = "candidate"


@dataclass
class Regime:
    context_id: str
    probe_ids: tuple[str,...]
    level: int


@dataclass
class Transport:
    source: Regime
    target: Regime
    mapping: dict[str,str]
    compatible: bool
    provenance: dict = field(default_factory=dict)

@dataclass
class WorldPrediction:
    state_features: tuple[float,...]
    confidence: float
    support: list[dict]
    horizon: int


class Clock:
    def __init__(self,budget:Budget): self.start=time.perf_counter(); self.budget=budget
    def ok(self): return time.perf_counter()-self.start <= self.budget.time_s
    def runtime(self): return time.perf_counter()-self.start
