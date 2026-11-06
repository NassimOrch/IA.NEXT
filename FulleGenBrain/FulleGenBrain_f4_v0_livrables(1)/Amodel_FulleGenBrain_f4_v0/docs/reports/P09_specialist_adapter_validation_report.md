# P09 — ORDER/AAM/eGenBrain specialist adapters: validation report

**Status:** PASS for the phase criteria below, on the exact sources and tests recorded here. This is not a claim of universal behavioral equivalence to every historical model.

## 1. Description

P09 adds explicit, versioned adapter boundaries for selected executable ORDER, AAM and eGenBrain source bundles. Each call records the source/version, canonical input hash, source-bundle hash where available, command, exit code, timeout/output-limit state, stdout/stderr hashes, duration and output hash. Source operations are selected by named adapter IDs; import does not automatically execute a specialist or enable network access.

## 2. Architecture

The adapter registry contains four executable or partially executable entries and three non-executable historical entries: `aam.o82_0`, `order.o76.math`, `order.80_2_2.hierarchical`, `egenbrain.v4.mesh`, `aam.o82_2`, `aam.o94_6`, and `order.80_4_7`. ORDER 80.2.0 is retained in the source/license inventory as a historical reference, not activated by default. Audit/comparison-only descriptors deliberately have no callable input/output schema because no runtime contract was established for those artifacts.

Executables are launched with an argument vector and `shell=False`, a sanitized environment, isolated per-run directory, timeout, aggregate output cap, and JSON-only input/output. Network is disabled by default; `allow_network=True` is refused because no reviewed network capability is registered. Input validation takes place before subprocess creation. A source timeout or `UNRESOLVED` status is not interpreted as proof of impossibility.

## 3. Pipeline complet

1. Resolve the declared source root and required-file contract.
2. Describe adapter version/status/source hash/effects/capabilities and missing files.
3. Validate operation name, exact JSON shape, input byte bound and path constraints.
4. Reject audit-only, missing-source, blocked, or unregistered operations explicitly.
5. Create a unique run directory and durable `request.json` with canonical input SHA-256.
6. Launch only the registered local entrypoint with a sanitized environment and bounded process capture.
7. Parse one JSON result, map source state without strengthening its epistemic claim, hash output and record a receipt.
8. Preserve diagnostics, original failures and source gaps in the audit tree.

## 4. Commandes d’exécution

From the project root:

```sh
python3 scripts/preflight.py --read-only-check
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_p09_specialists.py' -v
PYTHONPATH=src python3 scripts/build_p09_evidence.py
PYTHONPATH=src python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

The release-grade checked commands and their exact argument vectors, outputs, hashes, return codes and snapshot results are preserved in `logs/executions/P09/` and listed in `spec/evidence/P09_acceptance_gate.json`.

## 5. Résultats

- P09 targeted adapter suite: **15 tests passed**.
- Full integrated regression suite at P09 closure: **213 tests passed**, exit code 0, with `ResourceWarning` treated as an error.
- Adapter registry: **7 descriptors**; source/license inventory: **8 source artifacts**.
- Network-default assertion: pass (no adapter has implicit network capability).
- Source-gap assertion: pass; the missing eGenBrain v4 `.chunks/eGenBrain_v4.sqlite3.part02` is listed in the adapter descriptor and inventory.
- Input path traversal and absolute path cases are rejected as `INVALID` before a run/process is created.
- Output receipts bind adapter/source/version/status to input/source/output hashes; AAM O82.0 doctor/run and the selected ORDER/eGenBrain mesh paths are exercised in the targeted suite.

## 6. Interprétation des résultats

The tests establish adapter-boundary behavior for the fixtures and runtime versions present in the work tree. They do not show that all algorithms in the historical packages are equivalent to FulleGenBrain, that every source operation is integrated, or that the legacy eGenBrain MG database is complete. `COMPARISON_ONLY`, `AUDIT_ONLY`, and `PARTIAL` are intentionally retained rather than upgraded from an inference or guessed dependency.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

### Theoretical

An external specialist is a typed, effect-bearing component with a version, capability set and provenance. An unavailable source is not silently replaced by an assumed equivalent; the result is a typed block/unresolved state.

### Conceptual

The integrated model retains the distinction between source observation, candidate solution, verified proof and non-resolution. Preferences and successful process exits do not automatically become proof claims.

### Operational

The registry is inspectable without execution; invocation is explicit, offline by default and bounded. Missing files and uncertain upstream license terms are machine-readable. New project-authored code is covered separately by the project non-commercial license; upstream rights remain governed by their actual terms, which are not presumed granted by this audit.

## 8. Conclusions

**P09 PASS.** P00–P09 meet their recorded phase criteria. The native runtime is not dependent on eGenBrain's inherited MG database. AAM O94.6 remains audit-only because the supplied artifact does not provide a verified executable Dmodel. The eGenBrain mesh adapter is usable only for its implemented typed-mesh operations while the inherited MG remains blocked until the complete part set and integrity checks are available. P10 (CLI and local GUI) is the next authorized phase.

## 9. Statut du modèle

**P09 : PASS selon les critères et reçus de phase cités dans ce rapport.** Cette indication ne constitue pas une preuve de correction universelle.
