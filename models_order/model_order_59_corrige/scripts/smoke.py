from order59.agent import Order59Agent, AgentConfig
from order59.core import Budget
from order59.environments import SequenceEnv
cfg=AgentConfig(budget=Budget(time_s=0.4,max_steps=6,max_branches=16),seed=59059)
print(Order59Agent(cfg).solve_episode(SequenceEnv(seed=59059,length=7)))
