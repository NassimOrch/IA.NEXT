# eSonde v2 — Language Model with Explicit Probes

**Source and licensing notice:** This work is distributed under the source-code license available at [https://github.com/NassimOrch/IA.NEXT/].

**Final project files:** The final and complete files for this work are available in the **Releases** section.

**Runtime version:** 0.2.0  
**Project:** `eSond_v2`  
**Target architecture:** explicit and sparse probes; no neurons, no dense layers, no MLP, no dense learned embeddings, and no neural Q/K/V.  
**Interfaces:** Python CLI and Tkinter GUI.

## 1. Overview

eSonde v2 is an experimental general-purpose language-model prototype built around families of explicit probes. The runtime combines the responses of the SEQ, SKIP_REL, MORPH, SEM, DISC, and RETR families through a COORD coordinator. It provides training, updating, calibration, exact batch removal, prediction, continuation generation, scoring, attributed retrieval, extraction of composed A–relation–B relations, coreference/alias candidates, inspection, and auditing.

The model state is serialized as canonical JSON with a SHA-256 hash of the payload, an exact file hash, and a `.sha256` sidecar. No `pickle` is used. Generation and scoring reuse the same runtime as the graphical interface.

This repository contains the mathematical formalism, implementation, schemas, tests, demonstration corpora, an example checkpoint, reports, and validation logs. The original user-provided source archives are kept outside the release packages and are not copied into the runtime.

## 2. Scientific status — mandatory reading

Passing software tests does not establish general linguistic quality, superiority over MLPs/LLMs, or equivalence to a commercial model. Conversely, a weak result on a small corpus does not make it possible to draw conclusions about the full potential of the approach. Measured results are retained without artificial correction and must be reassessed using broader P5 protocols.

Two checkpoints are distinguished. `models/esonde_v2_demo_checkpoint.json` is the historical P3 state (older history format, with no complete text registry; it does not support exact batch removal). `models/esonde_v2_p6_demo_checkpoint.json` is the delivered v0.2.0 checkpoint: it was trained on this project's examples and then updated with the `p6-demo-update` batch. It retains the training/validation/batch texts in order to demonstrate exact removal. Neither checkpoint contains weights imported from the historical archives, nor is either a general-purpose pretrained model. The `demo_train`, `demo_validation`, and `demo_test` sets are workflow examples, not representative research benchmarks.

## 3. Requirements and installation

- **Python 3.10+.**
- CLI: Python standard library only; no pip runtime dependencies.
- GUI: Tkinter/Tcl-Tk must be available in the Python installation. On some Linux distributions, the `python3-tk` component is optional.
- No network connection is required by the runtime.

Run directly from the extracted directory:

```bash
python run_esonde.py --help
python run_esonde_gui.py
```

Shortcuts: `run_esonde_cli.sh` / `run_esonde_gui.sh` (Linux/macOS) and `run_esonde_cli.bat` / `run_esonde_gui.bat` (Windows).

Optional installation in a Python environment:

```bash
python -m pip install .
esonde --help
esonde-gui
```

Optional installation requires an appropriate Python build environment; it is not necessary for direct execution. This release is a standalone application directory with no third-party Python libraries, but it does not bundle a multi-OS Python interpreter. A standalone native executable must be built and tested separately for each OS/architecture.

## 4. Quick start — CLI

```bash
# Quick demo using the supplied corpus
python run_esonde.py demo --output models/quick_demo.json

# Controlled training with a versioned config and separate splits
python run_esonde.py train \
  --corpus examples/demo_train \
  --validation examples/demo_validation \
  --config examples/training_config.json \
  --output models/my_model.json

# Generation
python run_esonde.py generate --model models/my_model.json \
  --prompt "Science" --max-tokens 24 --strategy greedy

# Evaluation on a separate test set
python run_esonde.py score --model models/my_model.json \
  --corpus examples/demo_test --top-k 5 --output results/my_score.json

# Retrieval, inspection, and audit
python run_esonde.py retrieve --model models/my_model.json --query "energy and memory" --top-k 5
python run_esonde.py inspect --model models/my_model.json --family SEM --output results/sem_inspection.json
python run_esonde.py audit --model models/my_model.json --output results/model_audit.json
python run_esonde.py info --model models/my_model.json
```

The subcommands are: `train`, `update`, `remove-batch`, `calibrate`, `generate`, `score`, `retrieve`, `relations`, `coref`, `inspect`, `audit`, `info`, `demo`.

## 5. Quick start — graphical interface

```bash
python run_esonde_gui.py
```

The `models/esonde_v2_p6_demo_checkpoint.json` checkpoint, which retains a removable batch registry, is loaded by default. The four tabs cover:

1. **Training / update**: training, demo, adding/removing batches, and recalibration.
2. **Generation**: prompt, number of tokens, and greedy/sample strategy.
3. **Evaluation / retrieval**: test scoring and context search.
4. **Inspection / audit**: families, COORD, A–relation–B relations, candidate aliases/coreferences, and audit.

Long-running operations execute in a worker thread and do not block the GUI thread. Results and errors appear in the log at the bottom of the window. Details are provided in `docs/GUI_GUIDE.md`.

## 6. Formats, data separation, and integrity

The runtime reads UTF-8 text files (`.txt`, `.text`, `.md`, `.rst`, `.csv`, `.tsv`, `.jsonl` when enumerating a directory). Explicitly specified paths are read as UTF-8 text. Empty files are ignored.

The training, validation, and test corpora must be disjoint both by identifier AND by SHA-256 hash. Renaming a document does not make its content independent. Training uses only the training split; validation is used for COORD calibration; `score` is read-only.

After each save, keep the JSON file and its `.sha256` sidecar together. Do not edit JSON weights by hand, and do not recreate the sidecar for a file whose integrity is unknown. Keep previous checkpoints before running `update`.

## 7. Full documentation

- `formalism/formalisme_eSond_v2.tex`: end-to-end mathematical formalism.
- `docs/IMPLEMENTATION_SPEC_V2.md`: implementation specification.
- `docs/API_CONTRACT.md`: API and invariants.
- `docs/CLI_GUIDE.md`: CLI command and error reference.
- `docs/GUI_GUIDE.md`: complete graphical-interface guide.
- `docs/GUIDE_UTILISATION_CLI_GUI.md`: combined user workflows.
- `docs/PROTOCOL_EXPERIMENTAL_VALIDATION.md`: scientific validation protocol.
- `docs/P3_GATE_REPORT.md` and `docs/P4_GATE_REPORT.md`: CLI and GUI reports.
- `docs/P5_GATE_REPORT.md` and `docs/P6_GATE_REPORT.md`: P5/P6 experimental results and audit.
- `docs/REPORT_TEMPLATE.md`: standardized report template.
- `schemas/`: versioned JSON schemas.
- `tests/`: unit tests and CLI/GUI workflows.

## 8. Local tests

From the extracted directory:

```bash
python -m compileall -q src/esonde tests
PYTHONPATH=src python -m unittest discover -s tests -p 'test_core_p2.py' -v
PYTHONPATH=src python -m unittest discover -s tests -p 'test_cli_p3.py' -v
```

For GUI tests in a headless environment, Xvfb is required if no graphical server is available:

```bash
xvfb-run -a env PYTHONPATH=src python -m unittest discover -s tests -p 'test_gui_p4.py' -v
PYTHONPATH=src python -m unittest discover -s tests -p 'test_p6_advanced.py' -v

# Full suite (Xvfb only if no graphical session is available)
xvfb-run -a env PYTHONPATH=src python -m unittest discover -s tests -v
```

## 9. CLI exit codes

- `0`: command completed.
- `2`: invalid arguments, paths, data, configuration, or state.
- `3`: static audit detected a purity violation.

Errors are written to `stderr`; they are not converted into successful results.

## 10. Project structure

```text
formalism/       LaTeX formalism
src/esonde/      pure-probe runtime, API, serialization, CLI, and GUI
schemas/         state and family schemas
examples/        neutral demonstration corpora and config
models/          example checkpoint and hash
scripts/         validation/audit tools
results/         versioned results and logs
logs/            test and compilation output
checks*          project checklists and errors
```

## 11. Explicit operational limitations

The distribution contains the code and an example checkpoint, but no Python interpreter bundled for all systems. The GUI depends on Tkinter being available. The engine does not download corpora or an external tokenizer, and it does not include a third-party pretrained model. Observed quality limitations are reported in the reports and are not concealed; they must be examined under a broader protocol before any performance claims are made.

## 12. License and use

See `LICENSE.txt`. The examples are included for technical testing purposes. Before any real-world use, verify the rights to the corpora and back up the models and metadata.

## 13. P5 validation — results and status

Phase P5 is closed with documented limitations. The benchmark covers 36 documents (20 training, 8 validation, 8 test) in English, French, Arabic, and Spanish. Across 286 test targets, eSonde obtains a log-loss of 17.8791, perplexity of 58.18 M, top-1 accuracy of 8.39%, and top-5 accuracy of 20.98%. The overall perplexity comparison is not fair at this stage: 58.39% of the targets are OOV, and the baselines use different OOV policies. The post-hoc diagnostic limited to the 119 known targets is reported without replacing the original benchmark.

The complete suite passes twice (22/22 tests on each run). The block-level tests pass at 14/14 (core), 5/5 (CLI), and 3/3 (GUI). Generation with a fixed seed is reproducible; however, the tested example mixes several languages, and open lexical generation has not been demonstrated. The complete report in the project format is `docs/P5_GATE_REPORT.md`, including data, ablations, interpretation, resources, and chronology caveats. The machine-readable summary is `results/p5_validation_summary.json`.

The separate instrumented retraining run, whose canonical state exactly matches the reference checkpoint apart from `model_id`, `created_at`, and the integrity envelope, measured 21.83 s and a maximum RSS of 249,240 KiB. This figure is specific to the current environment.

## 14. P6 extensions: relational semantics, mentions, and reversibility

Runtime v0.2.0 adds to SEM the induction of composed A–relation–B relational patterns from observed clause partitions (A: 1–2 tokens, relation: 1–3, B: 1–2). These structures remain empirical candidates, with provenance; they are not certified syntactic analyses or proof of human-like understanding.

DISC retains surface mentions beginning with a capital letter (1–4 tokens) and ranks aliases/antecedent candidates by weighted overlap. The output indicates `resolved=false`: no arbitrary automatic resolution is imposed. Pronoun coverage is not claimed.

The new commands are:

```bash
python run_esonde.py relations --model models/esonde_v2_p6_demo_checkpoint.json --left "cats" --relation "eat"
python run_esonde.py coref --model models/esonde_v2_p6_demo_checkpoint.json --text "Alice returned."
python run_esonde.py remove-batch --model models/esonde_v2_p6_demo_checkpoint.json --batch-id p6-demo-update
```

Checkpoints created with v0.2.0 store the UTF-8 training and validation texts so that the counters, graphs, mentions, and RETR reservoir can be reconstructed exactly after a batch is removed. This means that the model JSON contains the corpus: protect it, and do not share it without checking rights/confidentiality. Historical models without a complete registry reject exact removal rather than simulate an approximate operation.

`max_context: 0` disables the additional global cap; the local windows specific to each family remain configurable, and their effective costs must be measured. The default value remains 512.

## 15. P6 runtime status

P6 adds candidate composed SEM relations, DISC mentions/aliases, exact batch removal by replay for recent checkpoints, the `max_context: 0` option, and explicit truncation diagnostics. The current version passes 33 integrated tests under Xvfb; the AST audit covers 20 Python runtime files with no findings, and the formalism has passed two recent compilations. These software checks do not validate complete pronominal coreference, a syntactic parser, open-vocabulary generation, or general-purpose semantics comparable to an LLM. The P5 benchmark retains its caveats (286 targets, 58.39% OOV, non-equivalent overall OOV comparability, and the formal JSON registry being written after the initial measurements). See `docs/P6_GATE_REPORT.md` for the complete report.

## 13. eSond v2 deliverables

The project distribution is organized into three archives:

- `Dmodel_eSond_v2.zip`: application, runtime sources, models/checkpoints, examples, schemas, CLI/GUI documentation, and tests.
- `Amodel_eSond_v2.zip`: source audit and experiments, P0–P6 reports, results, logs, validation scripts, tests, and attestations.
- `suivi_model_eSond_v2.zip` (possibly split into volumes): checklists, paths, evidence ledger, history, incidents, and the `sav_eSond_v2` backup.

The original user-provided sources and their raw extractions are not included in any archive. SHA-256 hashes of the member files are recorded in `PACKAGE_SHA256SUMS.txt` inside each package; archive and volume checksums are provided alongside the ZIP files. Consult `docs/P7_GATE_REPORT.md` in the audit package and `P7_RELEASE_VERIFICATION.json` in the tracking package.

The final and complete project files are available in the **Releases** section.

