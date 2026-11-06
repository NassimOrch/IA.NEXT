from order59.agent import Order59Agent,AgentConfig
from order59.core import Budget
from evaluation_adapters.environments import HiddenPermutationEnv,SequenceEnv,MazeEnv,VisualPatternEnv

def run(env):
    a=Order59Agent(AgentConfig(budget=Budget(time_s=3,max_steps=50,max_nodes=10000,max_branches=256),max_probe_trials=4,synth_budget=80))
    return a.solve_episode(env)

def test_hidden_and_sequence_pipeline():
    rh=run(HiddenPermutationEnv(n=4,seed=4)); rs=run(SequenceEnv(seed=2,length=8))
    assert rh['steps']>0 and rs['steps']>0
    assert any(x.get('event')=='representation' for x in rh['trace'])
    assert any(x.get('event')=='imagination_execution' for x in rs['trace'])

def test_maze_and_visual_execute():
    rm=run(MazeEnv()); rv=run(VisualPatternEnv())
    assert rm['steps']>0 and rv['steps']>0
