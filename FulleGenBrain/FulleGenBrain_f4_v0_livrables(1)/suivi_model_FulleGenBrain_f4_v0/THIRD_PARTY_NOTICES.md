{
  "schema_version": "1.0.0",
  "project": "FulleGenBrain_f4_v0",
  "created_utc": "2026-10-26T09:00:00+01:00",
  "authority": {
    "architecture": "spec/upstream/formalisme_FulleGenBrain_4.tex",
    "composition_theory": "spec/upstream/theorie_programation_compositionnelle_2.tex",
    "interface_prototype": "spec/upstream/interface_FulleGenBrain_4.tex",
    "operational_formalism": "formalisme_operationnel_FulleGenBrain_f4_v0.tex"
  },
  "execution_rule": "No phase starts before the preceding phase meets its exit criteria. Before each build/test command, read this file and both error checklists. After each command, persist stdout/stderr/exit code, append errors, update phase status and checkpoint.",
  "phases": [
    {
      "id": "P00",
      "name": "Archive and environment preflight",
      "status": "PASS",
      "criteria": [
        "Root ZIP opens and CRC test passes",
        "Archive entries inventoried",
        "Free disk space recorded",
        "Nested ZIP list and declared missing artifacts recorded"
      ],
      "evidence": [
        "spec/evidence/source_archive_inventory.json"
      ],
      "errors": []
    },
    {
      "id": "P01",
      "name": "Source reading and version reconciliation",
      "status": "PASS",
      "criteria": [
        "Read canonical V4 architecture, composition theory and GUI specification",
        "Inspect source evidence registries and validation records",
        "Review ORDER, AAM and eGenBrain docs/code entrypoints and release constraints",
        "Build a provenance/adaptation matrix; do not silently overwrite conflicting versions"
      ],
      "evidence": [
        "spec/upstream/README_FulleGenBrain_4.md",
        "spec/upstream/formalisme_FulleGenBrain_4.tex",
        "spec/upstream/theorie_programation_compositionnelle_2.tex",
        "spec/upstream/interface_FulleGenBrain_4.tex",
        "docs/source_reconciliation.md",
        "spec/evidence/source_reconciliation_matrix.json",
        "spec/evidence/canonical_source_sha256.txt",
        "spec/evidence/source_archive_inventory.json"
      ],
      "errors": []
    },
    {
      "id": "P02",
      "name": "Operational formalism",
      "status": "PASS",
      "criteria": [
        "Every one of the 29 AST operators has explicit semantics and gates",
        "Pipeline, object schema, statuses, contracts, effects, memory, ASCRC, synthesis, world model, recovery, CLI and UI are specified",
        "Compile/check LaTeX source and compare operator coverage to canonical sources",
        "Review discrepancies and fix before marking complete"
      ],
      "evidence": [
        "formalisme_operationnel_FulleGenBrain_f4_v0.tex",
        "logs/P02/pdflatex_final1.exitcode",
        "logs/P02/pdflatex_final2.exitcode",
        "spec/evidence/formalism_coverage_report.json"
      ],
      "errors": []
    },
    {
      "id": "P03",
      "name": "Governance, checklists and savepoint",
      "status": "PASS",
      "criteria": [
        "Absolute work/save paths recorded and validated",
        "Independent model/no-model error checklists exist and parse",
        "Preflight checks paths/checklists/manifests",
        "Savepoint can be refreshed atomically and restored in a smoke test"
      ],
      "evidence": [
        "chemins_FulleGenBrain_f4_v0.json",
        "checklist_de_travail_FulleGenBrain_f4_v0.json",
        "checklist_erreurs_no_model.json",
        "checklist_erreurs_model.json",
        "scripts/preflight.py",
        "scripts/savepoint.py",
        "scripts/run_checked.py",
        "logs/P03/savepoint_create.stdout.json",
        "logs/P03/savepoint_restore_smoke.stdout.json",
        "logs/P03/preflight_upgrade_test.json",
        "logs/P03/latest_manifest_verification.json"
      ],
      "errors": []
    },
    {
      "id": "P04",
      "name": "AST, schemas, contracts and type/effect validation",
      "status": "PASS",
      "criteria": [
        "Versioned JSON schema/parser implemented",
        "All invalid references/expressions/types/contracts/effects rejected before effects",
        "Stable diagnostics and append-only traces",
        "Positive and negative tests"
      ],
      "evidence": [
        "src/fullegenbrain/runtime/ast.py",
        "src/fullegenbrain/runtime/contracts.py",
        "src/fullegenbrain/runtime/expressions.py",
        "src/fullegenbrain/runtime/program.py",
        "src/fullegenbrain/runtime/registry.py",
        "src/fullegenbrain/runtime/tracing.py",
        "spec/schemas/fullegenbrain_ast_v1.json",
        "tests/test_p04_parser_contracts.py",
        "tests/test_p04_expressions.py",
        "tests/test_p04_schema_artifact.py",
        "tests/test_p04_trace_journal.py",
        "logs/executions/P04/20261026T100946769064+0000_p04-complete-test-suite-retest.receipt.json",
        "docs/reports/P04_ast_contracts_validation_report.md"
      ],
      "errors": []
    },
    {
      "id": "P05",
      "name": "Interpreter semantics for all 29 operators",
      "status": "PASS",
      "criteria": [
        "All operators dispatch to explicit implementation (not silent placeholder)",
        "Positive, boundary, negative and status propagation tests per operator",
        "Independent verification and effect isolation tested",
        "Operator-to-code-to-test matrix fully accounted"
      ],
      "evidence": [
        "logs/executions/P05/20261026T102228932325+0000_p05-full-suite-post-hardening.receipt.json",
        "logs/executions/P05/20261026T102234229057+0000_p05-operator-matrix-final.receipt.json",
        "logs/executions/P05/20261026T102140126894+0000_p05-negative-schema-coverage-matrix-retest.receipt.json",
        "spec/evidence/operator_implementation_matrix_validation.json",
        "tests/test_p05_interpreter.py",
        "tests/test_p05_semantic_boundaries.py",
        "tests/test_p05_operator_negative_matrix.py",
        "src/fullegenbrain/runtime/interpreter.py",
        "src/fullegenbrain/runtime/program.py"
      ],
      "errors": [
        {
          "id": "EXEC-20261026T101638963744+0000_p05-interpreter-operator-suite",
          "status": "RESOLVED",
          "resolution": "The first invocation was missing the source-tree import path; the package is in src/ and was not installed into the environment. Rerun with PYTHONPATH=src passed the 26-test operator suite.",
          "resolution_evidence": "logs/executions/P05/20261026T101731231601+0000_p05-interpreter-operator-suite-pypath.receipt.json"
        },
        {
          "id": "EXEC-20261026T101651064203+0000_p05-operator-matrix-check",
          "status": "RESOLVED",
          "resolution": "The matrix referenced stale test method names. Mapped each canonical operator to existing current test methods; the matrix checker reports 29/29 dispatch branches, 29/29 matrix entries, and 29/29 resolved test names.",
          "resolution_evidence": "logs/executions/P05/20261026T101835945656+0000_p05-operator-matrix-recheck.receipt.json"
        },
        {
          "id": "EXEC-20261026T102124850972+0000_p05-negative-schema-coverage-matrix",
          "status": "RESOLVED",
          "resolution": "The test incorrectly expected 28 operators with required fields; AST catalogue has 27 operators with mandatory fields and two option-only shapes. Changed the assertion to the verified catalogue property; all 4 negative-matrix tests passed.",
          "resolution_evidence": "logs/executions/P05/20261026T102140126894+0000_p05-negative-schema-coverage-matrix-retest.receipt.json"
        },
        {
          "id": "EXEC-20261026T102203925367+0000_p05-snapshot-commit-protocol",
          "status": "RESOLVED",
          "resolution": "A helper script had an unmatched parenthesis and failed before its source-edit steps. Corrected the script syntax and reran it successfully; the full suite subsequently passed.",
          "resolution_evidence": "logs/executions/P05/20261026T102218864187+0000_p05-snapshot-commit-protocol-retest.receipt.json"
        }
      ]
    },
    {
      "id": "P06",
      "name": "Persistent living memory and provenance",
      "status": "PASS",
      "criteria": [
        "SQLite schema/versioning and atomic updates",
        "Sleep/wake preserves exact payload and verifies hashes/versions/deps",
        "Waves typed/deduped/TTL/backpressure/replay behavior tested",
        "Checkpoints, restore, revocation and transitive stale propagation tested"
      ],
      "evidence": [
        "src/fullegenbrain/runtime/sqlite_services.py",
        "src/fullegenbrain/runtime/services.py",
        "tests/test_p06_sqlite_services.py",
        "tests/test_p06_wave_protocol_parity.py",
        "tests/test_p06_wave_ast.py",
        "logs/executions/P06/20261026T104232946067+0000_p06-wave-parity-and-ast-contract-suite-retest3.receipt.json",
        "logs/executions/P06/20261026T104257719537+0000_p06-full-suite-after-adapter-parity.receipt.json",
        "docs/reports/P06_persistent_memory_validation_report.md"
      ],
      "errors": [
        {
          "id": "EXEC-20261026T102534678605+0000_p06-sqlite-service-functional-suite",
          "status": "RESOLVED"
        },
        {
          "id": "EXEC-20261026T103349724154+0000_p06-sqlite-v2-regression-suite",
          "status": "RESOLVED"
        },
        {
          "id": "EXEC-20261026T103447172655+0000_p06-wave-protocol-test-expansion",
          "status": "RESOLVED"
        },
        {
          "id": "EXEC-20261026T103520925357+0000_p06-wave-protocol-tests",
          "status": "RESOLVED"
        },
        {
          "id": "EXEC-20261026T104109289358+0000_p06-wave-parity-and-ast-contract-suite",
          "status": "RESOLVED"
        },
        {
          "id": "EXEC-20261026T104134225972+0000_p06-wave-parity-and-ast-contract-suite-retest",
          "status": "RESOLVED"
        },
        {
          "id": "EXEC-20261026T104217333553+0000_p06-wave-parity-and-ast-contract-suite-retest2",
          "status": "RESOLVED"
        }
      ]
    },
    {
      "id": "P07",
      "name": "Lazy search, synthesis and CEGIS",
      "status": "PASS",
      "criteria": [
        "Versioned grammar and lazy candidate generation",
        "Type/contract/effect pruning and bounded best-first frontier",
        "Checkpoint/resume and budget exhaustion are explicit, not failure claims",
        "Counterexamples retained; holdout/test oracle leakage tests"
      ],
      "evidence": [
        "src/fullegenbrain/runtime/synthesis.py",
        "src/fullegenbrain/runtime/oracles.py",
        "src/fullegenbrain/runtime/interpreter.py",
        "src/fullegenbrain/runtime/ast.py",
        "spec/schemas/fullegenbrain_ast_v1.json",
        "tests/test_p07_synthesis_engine.py",
        "tests/test_p07_cegis.py",
        "docs/reports/P07_lazy_synthesis_cegis_validation_report.md",
        "formalisme_operationnel_FulleGenBrain_f4_v0.tex",
        "formalisme_FulleGenBrain_5.tex",
        "theorie_programation_compositionnelle_3.tex",
        "logs/executions/P07/20261026T111631277506+0000_p07-oracle-budget-and-integrity-retest.receipt.json",
        "logs/executions/P07/20261026T111852909946+0000_p07-full-suite-after-oracle-integration.receipt.json",
        "logs/executions/P07/20261026T112051038762+0000_p02-compile-versioned-formalisms-retest.receipt.json"
      ],
      "errors": [
        {
          "id": "EXEC-20261026T111550805686+0000_p07-independent-oracle-integration-tests",
          "status": "RESOLVED"
        },
        {
          "id": "EXEC-20261026T111025087705+0000_p07-randomized-frontier-and-sqlite-restart",
          "status": "RESOLVED"
        },
        {
          "id": "EXEC-20261026T111103001183+0000_p07-randomized-frontier-and-sqlite-restart-retest",
          "status": "RESOLVED"
        }
      ]
    },
    {
      "id": "P08",
      "name": "ASCRC, ASCR non-interference and world-model gate",
      "status": "PASS",
      "criteria": [
        "ASCR source preserved byte-identically where source permits verification",
        "ASCRC budget, pins, leases, stale and epistemic invariants tested",
        "World model disabled unless paired measured decision utility passes configured gate",
        "Hard budgets cannot be overrun by policy"
      ],
      "evidence": [
        "src/fullegenbrain/runtime/ascrc.py",
        "src/fullegenbrain/runtime/world_model_gate.py",
        "tests/test_p08_ascrc.py",
        "tests/test_p08_world_model_gate.py",
        "spec/evidence/ascr_source_preservation.json",
        "docs/reports/P08_ascrc_world_model_gate_validation_report.md",
        "docs/source_reconciliation.md",
        "formalisme_operationnel_FulleGenBrain_f4_v0.tex",
        "formalisme_FulleGenBrain_5.tex",
        "theorie_programation_compositionnelle_3.tex",
        "spec/versions/formalisme_FulleGenBrain_5.tex",
        "spec/versions/theorie_programation_compositionnelle_3.tex",
        "build/latex_validation/validation_report.json",
        "logs/executions/P08/20261026T112820183894+0000_p08-ascrc-and-world-gate-targeted-retest2.receipt.json",
        "logs/executions/P08/20261026T112834099316+0000_p08-full-suite-after-ascrc-fixes.receipt.json",
        "logs/executions/P08/20261026T112907080693+0000_p08-ascr-source-preservation-final-recheck.receipt.json",
        "logs/executions/P08/20261026T113141384646+0000_p08-compile-versioned-formalisms-retest.receipt.json"
      ],
      "errors": [
        {
          "id": "EXEC-20261026T111550805686+0000_p07-independent-oracle-integration-tests",
          "status": "RESOLVED",
          "resolution": "L’échec de première intégration a été corrigé lors de la liaison du contrat oracle et du schéma AST v1.3.0. Le retest ciblé, la suite oracle/frontier et la suite globale sont réussis.",
          "resolution_evidence": [
            "logs/executions/P07/20261026T111608211445+0000_p07-independent-oracle-integration-retest.receipt.json",
            "logs/executions/P07/20261026T111631277506+0000_p07-oracle-budget-and-integrity-retest.receipt.json",
            "logs/executions/P07/20261026T111852909946+0000_p07-full-suite-after-oracle-integration.receipt.json"
          ]
        },
        {
          "id": "EXEC-20261026T112521775472+0000_p08-ascrc-and-world-gate-targeted-tests",
          "status": "RESOLVED",
          "resolution": "Deux assertions de test ne correspondaient pas au contrat d’état opérationnel : une révocation exclut le candidat mais n’interdit pas le planificateur sur tout le catalogue; un réveil insuffisamment financé laisse une demande mémorisée et le candidat BLOCKED. Le code a été testé de nouveau avec ces attentes corrigées.",
          "resolution_evidence": [
            "logs/executions/P08/20261026T112820183894+0000_p08-ascrc-and-world-gate-targeted-retest2.receipt.json",
            "logs/executions/P08/20261026T112834099316+0000_p08-full-suite-after-ascrc-fixes.receipt.json"
          ]
        },
        {
          "id": "EXEC-20261026T112802214607+0000_p08-ascrc-and-world-gate-targeted-retest",
          "status": "RESOLVED",
          "resolution": "La modification des assertions a touché à tort un test distinct qui doit refuser un budget inférieur à la consommation active stale. L’assertion de budget dur a été rétablie; le test ciblé et la suite complète sont ensuite passés.",
          "resolution_evidence": [
            "logs/executions/P08/20261026T112820183894+0000_p08-ascrc-and-world-gate-targeted-retest2.receipt.json",
            "logs/executions/P08/20261026T112834099316+0000_p08-full-suite-after-ascrc-fixes.receipt.json"
          ]
        },
        {
          "id": "EXEC-20261026T112933221027+0000_p08-ascrc-and-world-gate-focused-retest",
          "status": "RESOLVED",
          "resolution": "Échec transitoire du même cas de test créé par l’édition trop large du test stale; le bloc a été restauré au contrat de budget dur et le retest ciblé ainsi que le full suite passent.",
          "resolution_evidence": [
            "logs/executions/P08/20261026T112820183894+0000_p08-ascrc-and-world-gate-targeted-retest2.receipt.json",
            "logs/executions/P08/20261026T112834099316+0000_p08-full-suite-after-ascrc-fixes.receipt.json"
          ]
        },
        {
          "id": "EXEC-20261026T113103283025+0000_p08-compile-versioned-formalisms",
          "status": "RESOLVED",
          "resolution": "Le nouveau passage P08 du formalisme V5 utilisait un environnement LaTeX invariant non déclaré. Le préambule a été complété puis les trois documents canoniques ont été recompilés deux fois chacun.",
          "resolution_evidence": [
            "scripts/fix_p08_formalism_theorem_env.py",
            "logs/executions/P08/20261026T113141384646+0000_p08-compile-versioned-formalisms-retest.receipt.json",
            "build/latex_validation/validation_report.json"
          ]
        }
      ]
    },
    {
      "id": "P09",
      "name": "ORDER/AAM/eGenBrain specialist adapters",
      "status": "PASS",
      "criteria": [
        "Source versions and licenses inventoried",
        "Adapters expose source, version, input/output types, effects and status honestly",
        "Behavioral re-use only when corresponding dependency/data exists",
        "Missing legacy data are surfaced without synthesizing substitutes"
      ],
      "evidence": [
        "spec/evidence/specialist_adapter_matrix.json",
        "spec/evidence/specialist_source_license_inventory.json",
        "spec/evidence/P09_acceptance_gate.json",
        "docs/reports/P09_specialist_adapter_validation_report.md",
        "docs/source_reconciliation.md",
        "tests/test_p09_specialists.py",
        "logs/executions/P09/20261026T115118515156+0000_p09-specialist-adapter-final-targeted-suite.receipt.json",
        "logs/executions/P09/20261026T115511870908+0000_p09-build-adapter-and-license-inventory-final-retest.receipt.json",
        "logs/executions/P09/20261026T115547950594+0000_p09-resolve-corrected-test-and-inventory-errors.receipt.json",
        "logs/executions/P09/20261026T115553504956+0000_p09-full-regression-suite.receipt.json"
      ],
      "errors": [
        {
          "id": "EXEC-20261026T115023563380+0000_p09-specialist-adapter-integration-suite-retest",
          "status": "RESOLVED",
          "resolution_evidence": "logs/executions/P09/20261026T115118515156+0000_p09-specialist-adapter-final-targeted-suite.receipt.json"
        },
        {
          "id": "EXEC-20261026T115409448060+0000_p09-build-adapter-and-license-inventory",
          "status": "RESOLVED",
          "resolution_evidence": "logs/executions/P09/20261026T115511870908+0000_p09-build-adapter-and-license-inventory-final-retest.receipt.json"
        },
        {
          "id": "EXEC-20261026T115447302595+0000_p09-build-adapter-and-license-inventory-retest",
          "status": "RESOLVED",
          "resolution_evidence": "logs/executions/P09/20261026T115511870908+0000_p09-build-adapter-and-license-inventory-final-retest.receipt.json"
        }
      ]
    },
    {
      "id": "P10",
      "name": "CLI and local GUI",
      "status": "PASS",
      "criteria": [
        "CLI documented and executable for diagnostics, validate, run, synthesize, memory, ASCRC, audit and resume",
        "Local web UI has task/chat, composition, objects/memory, evaluation and audit views",
        "No implicit external network/LLM calls",
        "Map UI-01..UI-20 to tests/manual evidence/adapters"
      ],
      "evidence": [
        "spec/evidence/P10_acceptance_gate.json",
        "spec/evidence/ui_acceptance_matrix.json",
        "docs/reports/P10_cli_gui_validation_report.md",
        "docs/GUIDE_CLI_FR.md",
        "docs/GUIDE_INTERFACE_FR.md",
        "tests/test_p10_cli_gui.py",
        "tests/test_p10_cli_ui.py",
        "logs/executions/P10/20261026T125404215581+0000_p10-canonical-tests-after-doc-and-ui-sync.receipt.json",
        "logs/executions/P10/20261026T125423938402+0000_p10-cli-documentation-smoke-clean-datadir.receipt.json",
        "logs/executions/P10/20261026T125501561256+0000_p10-full-regression-before-closure.receipt.json",
        "logs/executions/P10/20261026T125652563397+0000_p10-independent-exit-criteria-audit.receipt.json",
        "logs/executions/P10/20261026T125622519484+0000_p10-sync-runtime-ui-acceptance-map-final.receipt.json"
      ],
      "errors": [
        {
          "id": "EXEC-20261026T121212176008+0000_p10-cli-ui-targeted-suite",
          "status": "RESOLVED",
          "resolution_evidence": "logs/executions/P10/20261026T125209455654+0000_p10-resolve-cli-and-ui-errors-from-final-retest.receipt.json"
        },
        {
          "id": "EXEC-20261026T121413336860+0000_p10-canonical-cli-gui-targeted-suite",
          "status": "RESOLVED",
          "resolution_evidence": "logs/executions/P10/20261026T125404215581+0000_p10-canonical-tests-after-doc-and-ui-sync.receipt.json"
        },
        {
          "id": "EXEC-20261026T124656819117+0000_p10-cli-documentation-command-smoke-test",
          "status": "RESOLVED",
          "resolution_evidence": "logs/executions/P10/20261026T125037448040+0000_p10-cli-documentation-command-smoke-test-final.receipt.json"
        },
        {
          "id": "EXEC-20261026T124756623504+0000_p10-cli-documentation-command-smoke-test-retest",
          "status": "RESOLVED",
          "resolution_evidence": "logs/executions/P10/20261026T125037448040+0000_p10-cli-documentation-command-smoke-test-final.receipt.json"
        }
      ]
    },
    {
      "id": "P11",
      "name": "Robustness, safety, and performance",
      "status": "PASS",
      "criteria": [
        "Invalid inputs, path traversal, corrupted payload/checkpoint and permissions tested",
        "Crash/restart and idempotent replay tested",
        "Resource limits and concurrent effect conflicts tested",
        "Performance compared on fixed fixtures against baseline; results measured, no promises by assertion"
      ],
      "evidence": [
        "spec/evidence/P11_validation.json",
        "docs/reports/P11_robustesse_securite_performance.md",
        "spec/evidence/P11_benchmark_results.json",
        "spec/evidence/P11_lazy_frontier_benchmark.json",
        "spec/evidence/ascr_source_preservation.json",
        "spec/evidence/egenbrain_reassembly_audit.json",
        "spec/evidence/eGenBrain_v4_fragment_availability.json",
        "logs/executions/P11/20261026T135334032105+0000_p11-integrated-suite-final-before-phase-closure.receipt.json",
        "logs/executions/P11/20261026T135502392559+0000_p11-verify-vendor-source-hashes-final.receipt.json",
        "logs/executions/P11/20261026T135541262900+0000_p11-ascr-source-preservation-verify-final.receipt.json",
        "logs/executions/P11/20261026T135558730529+0000_p11-savepoint-restore-final.receipt.json"
      ],
      "errors": []
    },
    {
      "id": "P12",
      "name": "Docs, license and release packaging",
      "status": "PASS",
      "criteria": [
        "French README and end-to-end CLI/GUI guides maintained",
        "Non-commercial license separated from upstream licenses/notices",
        "Source manifests and SHA256 inventories match delivery",
        "Dmodel, Amodel and follow-up archives built and verified; any ZIP >200 MB split with reassembly script"
      ],
      "evidence": [
        "spec/evidence/P12_release_packaging_gate.json",
        "spec/evidence/source_archive_verification.json",
        "spec/evidence/latex_validation_attestation.json",
        "docs/reports/P12_documentation_licence_empaquetage.md",
        "README.md",
        "docs/GUIDE_CLI_FR.md",
        "docs/GUIDE_INTERFACE_FR.md",
        "LICENSE",
        "THIRD_PARTY_NOTICES.md",
        "logs/executions/P12/20261026T143052540847+0000_p12-final-integrated-suite-current-tree.receipt.json",
        "logs/executions/P12/20261026T144324273300+0000_p12-report-create-and-documentation-gate.receipt.json",
        "logs/executions/P12/20261026T143217248243+0000_p12-cli-examples-core-final.receipt.json",
        "logs/executions/P12/20261026T143500220004+0000_p12-cli-examples-run-group-bounded-retest.receipt.json",
        "logs/executions/P12/20261026T143538071086+0000_p12-cli-examples-memory-final.receipt.json",
        "logs/executions/P12/20261026T143657450788+0000_p12-cli-examples-services-15s-retest.receipt.json",
        "logs/executions/P12/20261026T142842755604+0000_p12-vendored-source-hash-recheck.receipt.json",
        "logs/executions/P12/20261026T142750728838+0000_p12-source-archive-integrity-recheck.receipt.json",
        "logs/executions/P12/20261026T143931363614+0000_p12-egenbrain-fragment-integrity-audit-current-tree.receipt.json",
        "logs/executions/P12/20261026T143958518490+0000_p12-ascr-source-preservation-recheck.receipt.json",
        "logs/executions/P12/20261026T144104672736+0000_p12-reverify-latex-evidence-against-current-sources.receipt.json",
        "logs/executions/P12/20261026T144350384685+0000_p12-build-and-self-verify-candidate-archives-current-tree.receipt.json",
        "logs/executions/P12/20261026T144414793133+0000_p12-verify-candidate-Dmodel_FulleGenBrain_f4_v0.receipt.json",
        "logs/executions/P12/20261026T144421722605+0000_p12-verify-candidate-Amodel_FulleGenBrain_f4_v0.receipt.json",
        "logs/executions/P12/20261026T144428644666+0000_p12-verify-candidate-suivi_model_FulleGenBrain_f4_v0.receipt.json",
        "logs/executions/P12/20261026T144456792055+0000_p12-candidate-savepoint-final-restore-smoke.receipt.json"
      ],
      "errors": [
        {
          "id": "EXEC-20261026T143551530831+0000_p12-cli-examples-services-final",
          "status": "RESOLVED",
          "resolution_evidence": "logs/executions/P12/20261026T143657450788+0000_p12-cli-examples-services-15s-retest.receipt.json"
        }
      ]
    },
    {
      "id": "P13",
      "name": "Release audit and final closure",
      "status": "PASS",
      "criteria": [
        "Rebuild and tests repeat from clean extraction",
        "Every planned test has PASS/FAIL/NOT_RUN plus reason",
        "Final report contains description, architecture, pipeline, commands, results, interpretations, consequences, conclusions and exact status",
        "Three deliverables self-verify and archive files are below stated size limit"
      ],
      "evidence": [
        "spec/evidence/P13_clean_extraction_validation.json",
        "spec/evidence/P13_test_execution_inventory.json",
        "spec/evidence/P13_release_closure_gate.json",
        "docs/reports/P13_release_audit.md",
        "logs/executions/P13/20261026T173648246635+0000_p13-clean-extraction-after-sqlite-sidecar-race-fix.receipt.json"
      ],
      "errors": [
        {
          "id": "EXEC-20261026T152327964466+0000_p13-clean-extract-after-followup-evidence-rebuild",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-P13-OUTER-TIMEOUT-clean-extraction-isolated-candidate-20261026T152847",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-20261026T160716146989+0000_p13-clean-extraction-minimal-runtime-payloads",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-20261026T161016821536+0000_p13-clean-extraction-minimal-runtime-retest",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-20261026T162155580419+0000_p13-clean-extraction-minimal-runtime-final",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-20261026T162518927190+0000_p13-ascrc-golden-vector-self-contained-test",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-20261026T165046850396+0000_p13-self-contained-ascrc-regression-before-package-rebuild",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-20261026T170039176652+0000_p13-clean-extraction-diagnostic-candidate-no-historical-trees-clean-en",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-P13-OUTER-TIMEOUT-clean-extraction-current-packages-20261026T1714",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-P13-OUTER-TIMEOUT-file-backed-extraction-20261026T1722",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-20261026T172535875895+0000_p13-final-clean-extraction-current-packages-file-backed",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-20261026T152631306530+0000_p13-build-isolated-delivery-directory",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-20261026T153220918596+0000_p13-record-interrupted-clean-extraction-attempt",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-P13-OUTER-TIMEOUT-final-clean-extraction-after-final-rebuild-20261026T1750",
          "status": "RESOLVED",
          "resolution_evidence": "logs/executions/P13/20261026T181647653874+0000_p13-final-clean-extracted-integrated-suite-receipt.receipt.json"
        },
        {
          "id": "EXEC-20261026T175002428900+0000_p13-final-clean-extraction-after-final-rebuild",
          "status": "RESOLVED",
          "resolution_evidence": "logs/executions/P13/20261026T181647653874+0000_p13-final-clean-extracted-integrated-suite-receipt.receipt.json"
        },
        {
          "id": "EXEC-20261026T195229431101+0000_final-package-extract-merge-relocation-and-integrated-suite",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        },
        {
          "id": "EXEC-P13-OUTER-TIMEOUT-current-clean-extraction-20261026T2008",
          "status": "RESOLVED",
          "resolution_evidence": "spec/evidence/P13_clean_extraction_validation.json"
        }
      ],
      "validation_note": "Archive hashes and internal manifests verified; clean-extraction native runtime smoke (13 commands), GUI health, merge/path-relocation checks and the independently checked integrated suite all passed. Aggregate harness interruptions are retained in the error registers and resolved by the successful component receipts."
    }
  ],
  "current_phase": "P13",
  "last_update": "2026-10-26T20:28:00+00:00",
  "updated_at": "2026-10-26T20:28:00+00:00"
}
