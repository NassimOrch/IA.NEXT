from order59.agent import Order59Agent, AgentConfig
from order59.core import Budget, Observation
from evaluation_adapters.environments import SequenceEnv, ChessEnv

def test_imagination_engine_is_actually_invoked():
    a=Order59Agent(AgentConfig(budget=Budget(time_s=2,max_steps=1,max_branches=32),max_probe_trials=2,synth_budget=20))
    e=SequenceEnv(seed=5,length=6)
    r=a.solve_episode(e)
    assert a.imagination.calls > 0
    assert any(x.get('event')=='imagination_execution' for x in r['trace'])

def test_chess_candidate_generation_uses_only_action_alphabet():
    a=Order59Agent(AgentConfig(budget=Budget(time_s=2,max_steps=1,max_branches=32),max_probe_trials=1,synth_budget=10))
    e=ChessEnv(fen='7k/5Q2/7K/8/8/8/8/8 w - - 0 1')
    o=a.observe(e.reset())
    acts=a._generic_action_alternatives(o,e)
    assert len(acts)==32
    assert all(x in e.action_space() for x in acts)


def test_action_value_is_observation_conditioned():
    from evaluation_adapters.environments import ChessEnv
    a=Order59Agent(AgentConfig(budget=Budget(time_s=2,max_steps=1,max_branches=64),seed=65001,max_probe_trials=1,synth_budget=10))
    e1=ChessEnv(fen="7k/5Q2/7K/8/8/8/8/8 w - - 0 1")
    e2=ChessEnv(fen="6k1/5ppp/8/8/8/5Q2/6PP/6K1 w - - 0 1")
    o1=a.observe(e1.observe()); o2=a.observe(e2.observe())
    r1=a.action_neural.vector(a.perceiver.feature_vector(o1),'a1a2',observation=o1.value)
    r2=a.action_neural.vector(a.perceiver.feature_vector(o2),'a1a2',observation=o2.value)
    assert r1 != r2
    assert any(abs(x-y)>1e-12 for x,y in zip(r1,r2))


def test_program_vm_rank_does_not_read_reward_target():
    from order59.program_vm import ProgramVM
    from order59.core import Program
    p=Program('rank',('Rank',),'generic->generic')
    assert ProgramVM({'action_feature':0.2,'reward':1.0}).run(p) == ProgramVM({'action_feature':0.2,'reward':-1.0}).run(p)


def test_world_model_prediction_is_action_conditioned():
    from order59.prediction import PredictiveModel
    from order59.core import Observation,Transition
    m=PredictiveModel(); o=Observation({'x':0},'s'); a=Observation({'x':1},'s'); b=Observation({'x':9},'s')
    for i in range(8):
        act='A' if i%2==0 else 'B'
        nxt=a if act=='A' else b
        m.update(Transition(o,act,nxt,0.0,True,{}))
    pa=m.predict(o,'A'); pb=m.predict(o,'B')
    assert pa.state_features != pb.state_features


def test_capability_policy_effect_measurement_is_independent_of_truth():
    from order59.capabilities import CapabilityManager
    r=CapabilityManager().measure_policy_effect([0.0,1.0],[0.2,0.8])
    assert abs(r['mean_effect']) < 1e-12
    assert r['n']==2


def test_sequence_action_alphabet_does_not_depend_on_hidden_continuation():
    a=SequenceEnv(seed=22,length=10)
    b=SequenceEnv(seed=22,length=10)
    # Same observed prefix must imply the same public action alphabet regardless
    # of any hidden future rule. We replace only the hidden suffix.
    b.seq=b.seq[:3]+[999,1001,1003,1005,1007,1009,1011]
    a.reset(); b.reset()
    assert a.observe()==b.observe()
    assert a.action_space()==b.action_space()


def test_adversarial_chess_reply_uses_full_state_transition():
    from evaluation_adapters.environments import AdversarialChessEnv
    e=AdversarialChessEnv(fen="r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",max_agent_plies=1,seed=1)
    # White castles; the evaluator's internal transition must move the rook and
    # update castling rights before choosing the black reply.
    obs,reward,done,info=e.act('e1g1')
    assert e.board[7][6]=='K' and e.board[7][5]=='R'
    assert 'K' not in e.castle and 'Q' not in e.castle
    assert info.get('opponent_replied') in {True,False}
