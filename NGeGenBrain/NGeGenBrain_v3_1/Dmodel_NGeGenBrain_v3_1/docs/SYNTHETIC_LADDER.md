# Synthetic architecture ladder (SYNTH-001…008)

The ladder in `nggegenbrain_v3.adapters.synthetic` separates **instrumentation evidence** from **reconstruction evidence**. Each seeded model can be passed as an instrumentable adapter or wrapped by `QueryOnlyAdapter`. Random parameters are reproducible by seed.

| Level | Fixture | Main purpose | Executed checks in this release |
|---|---|---|---|
| SYNTH-001 | Linear network | numeric input/output observation | forward, capture, intervention, black-box query |
| SYNTH-002 | ReLU parity circuit | boolean mechanism and blind finite reconstruction | forward, capture, intervention; separate XOR reconstruction on full 4-bit domain |
| SYNTH-003 | Interaction MLP | nonlinear input interactions | forward, capture, intervention, black-box query |
| SYNTH-004 | Distributed feature network | distributed hidden representations | forward, capture, intervention, black-box query |
| SYNTH-005 | Competing pathways | two branches and learned gate | forward, capture, intervention, black-box query |
| SYNTH-006 | Hierarchical MLP | nested stages | forward, capture, intervention, black-box query |
| SYNTH-007 | Tiny Transformer encoder | transformer instrumentation | forward, capture, intervention, black-box query |
| SYNTH-008 | Tiny causal Transformer | autoregressive token generation | forward, capture, intervention, deterministic generation and seeded sampling |

The official smoke run is stored in `benchmarks/results/20261027_official/synthetic_ladder_smoke.json`. This fixture suite is not itself proof that the discovery engine reconstructs all eight models. The only reconstruction claim in this release is the explicitly bounded independent symbolic reconstruction of SYNTH-PARITY-4 in the declared affine-XOR hypothesis class. The causal Transformer uses random initialization and is not a pretrained LLM.

## Local usage

```python
from nggegenbrain_v3.adapters.synthetic import create_synthetic_level, run_synthetic_ladder_smoke

fixture = create_synthetic_level(7, seed=20261027, black_box=False)
adapter = fixture["adapter"]
output, activations = adapter.capture(fixture["sample_input"])

summary = run_synthetic_ladder_smoke(seed=20261027)
```
