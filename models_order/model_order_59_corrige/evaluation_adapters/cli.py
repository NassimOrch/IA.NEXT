from __future__ import annotations
import argparse, json
import sys, pathlib
ROOT=pathlib.Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/'src'))
from order59 import Budget
from order59.agent import Order59Agent,AgentConfig
from evaluation_adapters.environments import HiddenPermutationEnv,SequenceEnv,MazeEnv,VisualPatternEnv,ChessEnv
FACTORIES={"hidden":HiddenPermutationEnv,"sequence":SequenceEnv,"maze":MazeEnv,"visual":VisualPatternEnv,"chess":ChessEnv}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('task',choices=FACTORIES); ap.add_argument('--time',type=float,default=5); ap.add_argument('--steps',type=int,default=80); args=ap.parse_args()
    env=FACTORIES[args.task](); agent=Order59Agent(AgentConfig(budget=Budget(time_s=args.time,max_steps=args.steps,max_branches=256)))
    print(json.dumps(agent.solve_episode(env),indent=2,default=str))
if __name__=='__main__': main()
