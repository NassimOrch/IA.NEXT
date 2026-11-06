# ORDER 63 — Generalist AI Research Release

Order 63 continues the verified Order 62 codebase rather than restarting from zero.

## Architecture

The release integrates the fingerprint/fiber/closure machinery, active representation acquisition, a structured deficit state, learned constraints, a semantic Transformer world model with an ensemble transition model, recursive counterfactual imagination, general reasoning program synthesis in a sandboxed VM, per-module micro-memory with an explicit typed memory bus, transfer/falsification, meta-control, verification, checkpointing, and conservative optimization infrastructure.

The final package ships with RS navigation **disabled by default** because the frozen O63 causal/paired evaluation did not establish a robust decision-level gain. The trained RS branch is distributed separately.

## Run

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python scripts/run_final.py --no-rs --time 15 --nodes 50000 --steps 16 --seed 630630
```

## RS branch

The RS branch is trained from `dataset_model_order_62_rs.json` using verified demonstration trajectories. The final evaluator does not need the dataset. The RS branch should be treated as an experimental navigation research branch, not as a proven solution to general reasoning.

## Integrity

Actions can be made opaque at evaluation time. The core contains no benchmark-specific answer table or domain-specific solution dispatch. The independent audit bundle contains hashes, commands, raw result summaries, source provenance, and the exact training/evaluation manifests.

## Scientific status

This is an experimental generalist architecture. It does not constitute a proof of universal AGI. The accompanying report deliberately retains FAIL, EXHAUSTED, NOT_VERIFIED, RESOURCE_BOUND and interruption statuses.
