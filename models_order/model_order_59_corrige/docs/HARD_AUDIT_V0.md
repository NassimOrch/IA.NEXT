# ORDER 59.0.2 — Hard audit V0 final

This audit records the verified corrective release. It does not claim general intelligence.

## Final status
- package version: 0.59.2 / runtime: 59.0.2
- tests: 24 passed
- compileall: PASS
- filtered core coverage: 87% line coverage
- core/evaluation separation: PASS
- static forbidden-call/import audit across deployable core and evaluation adapters: PASS
- generic interface suite outside the repository: 3/3 PASS
- hard multi-family suite: 8/8 executed, all PARTIAL
- chess hard 2-step suite: 5/5 executed, all PARTIAL
- chess hard 10-step suite: 5/5 executed as independent shards, all PARTIAL

## Hard chess budget
The long chess shards used 60 s wall budget per position, 10 agent steps, 100000 internal evaluation-node budget, 4096 candidate branches and 400 synthesis candidates. Each position was run independently to preserve checkpointability. The model received no legal-move list; the evaluator retained legality checks internally.

## Integrity corrections
The release corrects occurrence-vs-hash history, active-probe reuse, closure execution, interaction-derived constraints, independent action verification, global time/node budgeting, action-conditioned prediction, action-specific imagination, reward-independent synthesis evaluation, observation-conditioned neural scoring, evidence-based transfer deficit, core/adaptor separation, package versioning, chess adapter legality for promotion/castling/en-passant, adversarial state-transition consistency, sequence action-alphabet leakage, and release documentation consistency.

## Genericity
No benchmark class or benchmark dispatch is present under `src/order59`. Evaluation environments are external adapters. The sequence adapter no longer derives its public action alphabet from the hidden continuation; it uses only a generic range derived from the observed prefix. A separate generic-interface harness constructed three previously unseen environment classes outside the model repository; all three reached PASS in the tested finite episodes. This is interface evidence only, not proof of general intelligence.

## Interpretation
The hard campaigns remain predominantly PARTIAL. Resource exhaustion is represented explicitly when it occurs, and launcher interruptions are not recoded as model failures. The release therefore provides causal instrumentation and integrity improvements, but does not establish open-ended reasoning, universal program synthesis, universal world modelling, general transfer, or competitive chess strength.
