# ORDER 63 component map

| Component | O63 implementation | Main file | Causal downstream use |
|---|---|---|---|
| Perception | multimodal generic encoder | src/order63/perception.py | observation, probe/representation |
| Fingerprints/fibres | partition/quotient/refinement | src/order63/geometry.py, representation.py | deficit, closure, meta |
| Deficit | structured deficit state | src/order63/agent.py | probes, constraints, RS, imagination |
| Constraints | generic primitives + promotion | src/order63/constraints.py | action filtering/scoring |
| Semantic world model | learned encoder/decoder + 3-member dynamics ensemble | src/order63/semantic_world_model.py | prediction, imagination, RS, memory |
| Semantic geometry | latent trajectory instrumentation | src/order63/semantic_world_model.py, rs_navigation.py | RS navigation |
| RS | multi-step trajectory progress navigator | src/order63/rs_navigation.py | action ranking/fusion |
| Imagination | hypothesis generation + rollouts | src/order63/imagination.py | candidate action scores, memory, RS |
| Program synthesis | neural proposal + compositional sandbox VM | src/order63/synthesis.py, program_vm.py | program signal/fusion |
| Micro-memory | per-module typed local memories | src/order63/micro_memory.py | contextual retrieval/fusion/learning |
| Memory bus | typed explicit propagation | src/order63/micro_memory.py | inter-module state transfer |
| Transfer | discovery + falsification | src/order63/transfer.py | deficit/representation/synthesis |
| Meta | learned strategy allocation | src/order63/meta.py | compute strategy |
| Verification | independent environment interface | src/order63/verification.py | admissibility/certification |
| Optimization | conservative generic optimizations | src/order63/optimizations.py | closure/research infrastructure |
| Checkpoint | full state and RNG capture | src/order63/checkpoint.py | restart/reproducibility |
| Audit | static/dynamic integrity | src/order63/audit.py | anti-cheat/integrity |
