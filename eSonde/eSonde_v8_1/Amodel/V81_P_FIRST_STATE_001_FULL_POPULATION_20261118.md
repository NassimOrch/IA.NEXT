# V81-P-FIRST-STATE-001 — Full-population P activation

- **Timestamp:** 2026-11-18T12:48:18+01:00
- **Status:** PASS_OPERATOR_ONLY

## Description
Exact first-state P activation for `Bonjour, comment vas-tu ?`, with all 1,000,000 original Obsiss rows processed exactly once.

## Architecture
Original v6 checkpoint, dimension 16; exact batched `F_h/F_p`; `E_C` state space retained; `E_O` remains separate. This mode produces the paired P published state and Q context without the graph-diffusion iterations.

## Pipeline
1. Verify the original checkpoint and statistics.
2. Load all 1,000,000 Obsiss rows read-only.
3. Tokenize the prompt.
4. Compute `F_h/F_p` across 123 batches of 8,192 rows.
5. Compute P and Q for every row.
6. Hash the complete outputs and verify row coverage.

## Command
```bash
PYTHONPATH=src OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
ESONDE_INDEX_WORKERS=3 python experiments/profile_full_population_first_state_P_20261118.py
```

## Results
- Model load: 2.129 s.
- P activation: 2.071 s.
- Total: 4.202 s measured from script start (5.50 s wall clock by `/usr/bin/time`).
- Population: 1,000,000; dimension: 16; 123 batches.
- Every row processed exactly once: PASS.
- Published SHA-256: `eec54aaefd800f72384117a7d3105b75c1c9a15448829b4b9ce07011b7428f54`.
- Q SHA-256: `c596c558156e2a46dc108c6ee7b70fafab4e9839acd7304573f1554f260a3abf`.
- Checkpoint SHA-256: `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`.
- Fixed-point/convergent status: **not claimed**.

## Interpretation
This confirms the first-state operator is computationally tractable over all one million rows in the observed environment. It does not measure a generated answer, semantic coherence, or generalisation.

## Consequences
- **Theoretical:** The P mapping and Q context are computed over the complete original population.
- **Conceptual:** First-state activation is a separate, explicitly named model variant from neighbour-diffusion convergence.
- **Operational:** It can be used symmetrically with first-state R for the next free-chat test; the convergent variant remains available for exact experimentation.

## Conclusion
PASS for the complete first-state operator only. No dialogue-quality conclusion follows.

## Model status
`RUNTIME_PROTOTYPE_UNDER_EVALUATION`.
