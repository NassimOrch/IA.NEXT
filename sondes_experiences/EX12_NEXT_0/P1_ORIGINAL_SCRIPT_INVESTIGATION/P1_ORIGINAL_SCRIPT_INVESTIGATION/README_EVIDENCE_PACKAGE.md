# Evidence package — P1_RUN_001 / P1_RUN_002 source provenance

This package preserves result artifacts, metadata, registries, later canonical scripts, the forensic audit script and the signed declarative investigation report.

## Key finding

The result CSV/JSON artifacts for P1_RUN_001 and P1_RUN_002 exist and their stored timing aggregates recompute from raw measurements. The exact original producer scripts and contemporaneous producer hashes were not found in the accessible environment. The reusable, hash-linked scripts for P1_RUN_003/P1_RUN_004 were created after the first two result sets and are not represented as their originals.

## Layout

- `evidence/P1_RUN_001_FAILED/`: failed prototype result files and failure note.
- `evidence/P1_RUN_001_ROOT_DUPLICATE/`: byte-identical duplicate result artifacts found at P1 root.
- `evidence/P1_RUN_002/`: provisional result files and end-to-end comparison limitation note.
- `evidence/CANONICAL_RUN_003_004_SOURCES/`: later scripts, hashes and run-specific metadata; not original RUN_001/002 sources.
- `evidence/GOVERNANCE_AND_EXISTING_REPORTS/`: run registry, phase gate and P1 report materials.
- `evidence/ENVIRONMENT_AND_AUDIT/`: repeatable forensic audit source and machine-readable output.
- `P1_SOURCE_CHRONOLOGY.csv`: chronology table used in the report.
- `P1_ORIGINAL_SCRIPT_FORENSIC_REPORT.md/.pdf`: signed declarative report.

## Reproduction

Run the audit script from the EX12 workspace's pinned Python environment, or from the path recorded in the JSON report. The script independently checks artifact existence, hashes, raw-to-summary recomputation, available script timestamps, `.pyc` headers, and accessible environment history locations. It does not claim to regenerate the original P1 producer code.

## Limits

The container is `uid=0(root)` but cannot inspect inaccessible host overlay layers or host audit logs. The report therefore states a code-retention/provenance gap and does not infer sabotage, theft or an intentional deletion from missing files alone.
