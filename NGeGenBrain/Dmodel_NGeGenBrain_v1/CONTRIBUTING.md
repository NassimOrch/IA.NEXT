# Contribution guide

1. Read `formalism/theorie_programation_compositionnelle_NG_0.tex` and `theorie_programation_compositionnelle_3.tex` before modifying execution semantics.
2. Every new AST constructor or effect must define its types, operational behavior, error statuses, capabilities, budget charging, trace event, tests and source-map entry.
3. Keep the action ID in `src/ngegenbrain/actions.py::ACTION_DESCRIPTORS`; CLI, API and web must share the single registry.
4. Add positive and negative tests. A test result cannot be promoted into a universal theorem.
5. Run `scripts/run_tests.sh` (or the Windows test batch), requiring `ResourceWarning` as errors.
6. Update `NGeGenBrain_v1_mise_en_oevre.json`, `docs/FORMALISM_AUDIT.md`, checklists and changelog when behavior changes.
7. Keep secrets, live user databases, and machine-specific state out of commits. Do not introduce eval/exec of user-provided source.
8. Declare changes to contracts, schemas and saved checkpoints; provide explicit compatibility/migration behavior.
