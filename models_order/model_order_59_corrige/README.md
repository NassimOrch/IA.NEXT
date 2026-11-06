# ORDER 59.0.2 — Theory of Fingerprints

The executable agent starts from raw observations exposed by the environment protocol. It constructs observations, probes, fingerprints and fibres; measures observational deficits; performs active probing; induces constraints from interaction evidence; predicts transitions; generates and executes counterfactual hypotheses; synthesizes typed reasoning programs inside a sandbox; stores and retrieves episodic/semantic memory; discovers transfer correspondences structurally; and uses a meta-controller to choose the next reasoning resource.

No benchmark solution table is shipped. The deployable core under src/order59 contains no benchmark classes, benchmark dispatch, chess rules or task-specific action generators. Evaluation environments are isolated under evaluation_adapters/ and are never imported by the core.

## Reproduction

```bash
python -m pip install -e . --no-build-isolation
PYTHONPATH=src:. pytest -q
python -m evaluation_adapters.cli hidden --time 1 --steps 12
python -m evaluation_adapters.cli sequence --time 1 --steps 8
python -m evaluation_adapters.cli maze --time 1 --steps 16
python -m evaluation_adapters.cli visual --time 1 --steps 8
python -m evaluation_adapters.cli chess --time 1 --steps 2
```

Scientific claims are restricted to the evidence archived with O59.

The delivered implementation also contains hard-audit integrity corrections documented in `docs/HARD_AUDIT_V0.md`. These corrections include global time-budget enforcement, action-conditioned prediction, action-specific imagination use, reward-independent synthesis evaluation, chess legality fixes, and generic observation-conditioned neural action scoring.
