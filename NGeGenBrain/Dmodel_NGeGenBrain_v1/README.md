# NGeGenBrain_v1

NGeGenBrain_v1 is a local, standard-library-only Python implementation of a compositional runtime coupled to a stratified typed mesh, auditable execution traces, persistent memory, bounded synthesis, ASCRC scheduling, declarative chat intents, and conditional world-model evaluation. The project files have no PyPI dependencies; an interpreter is still required unless the optional Windows x64 embeddable-runtime bootstrap has been run.

**Repository status:** implementation release candidate with reproducible regression tests. Read `docs/REPORT_AUDIT_NGeGenBrain_v1.md` and `NGeGenBrain_v1_mise_en_oevre.json` for implementation scope, source-to-code traceability and evidence. The labels “tested” and “implemented” refer to the listed implementation and test scope; they are not a blanket mathematical proof of every possible execution.

## Design principles

- Programs are data: a validated JSON AST is interpreted by a controlled engine. User source strings are never passed to Python `eval`/`exec`.
- One action registry is shared by CLI, HTTP API and the web action explorer.
- Retrieval scores rank candidates; they are not truth certificates.
- Mesh derivations carry rule/premise/operator provenance and are independently rechecked against current stored premises and rules.
- Capabilities and budget gates are explicit. The local HTTP service binds to loopback only by default and rejects non-loopback binding.
- Predictions from a world model are always labelled `SIMULATED`; the model cannot promote its own prediction into an observation or proof.
- An ambiguous chat intent is not executed. Sensitive capabilities are never granted by the chat parser.
- The historical ASCR/AAM runtime source was not present. `ASCR-NG` is a documented reconstruction of the described retrieval role, not a claim of historical runtime equivalence. AAM is not an operational dependency.

## Requirements

- Python 3.11 or later is required for source execution. No third-party Python packages are required; the app uses the standard library and SQLite.
- - Windows x64: use the supplied `.bat` launchers. If no compatible Python is installed, run `powershell -NoProfile -ExecutionPolicy Bypass -File tools\bootstrap_python_windows.ps1` once; it downloads the official pinned embeddable package, verifies SHA-256 before extraction, and stores it under `%LOCALAPPDATA%\NGeGenBrain_v1\runtime`. This initial bootstrap needs Internet access. Linux/macOS: use an installed Python 3.11+ and the shell commands below.

## Start the web interface

Linux/macOS:

```sh
python3 ngbrain.py init
python3 ngbrain.py serve --host 127.0.0.1 --port 8765
```

Open <http://127.0.0.1:8765/>. Stop with `Ctrl+C`.

Windows: double-click `launch_NGeGenBrain_v1.bat`; it waits for a local HTTP 200 response before opening the browser. `run_web_NGeGenBrain_v1.bat` starts only the server. The persistent data directory is `%LOCALAPPDATA%\NGeGenBrain_v1\data`, not a temporary folder. Launchers prefer the embedded runtime when present, otherwise check `py -3` or `python` for Python 3.11+.

## CLI quick start

```sh
python3 ngbrain.py init
python3 ngbrain.py status
python3 ngbrain.py actions
python3 ngbrain.py verify
python3 ngbrain.py test
```

Run a program from a JSON AST file:

```sh
python3 ngbrain.py run --program examples/add.json --input null --capabilities '[]' --budget 1000
```

Run any registered action (same action registry as the web interface):

```sh
python3 ngbrain.py action mesh.fact.add --data '{"subject":"A","predicate":"edge","object":"B","status":"observed"}'
python3 ngbrain.py action mesh.infer --data '{}'
python3 ngbrain.py action mesh.fact.query --data '{"pattern":{"predicate":"edge"}}'
```

Use `python3 ngbrain.py actions` for the exact current action IDs and `python3 ngbrain.py action ACTION_ID --file payload.json` for complex requests. See `docs/USER_GUIDE.md` for every command family and UI equivalence.

## Data and privacy

By default, persistent state lives at `~/.ngegenbrain_v1/data/ngegenbrain.sqlite3`. Set `NGEGB_HOME` to select another persistent data directory, or use `--db PATH` to select a database for CLI operations. The server is local-only and does not call external services. A database can contain user-entered facts, messages, traces and program metadata: protect and back it up like any private project data.

## Tests and validation

```sh
python3 ngbrain.py test
```

Equivalent direct command from the repository root:

```sh
PYTHONWARNINGS=error::ResourceWarning PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The test suite uses isolated temporary databases. In the V1 release candidate, 65 unit/integration/adversarial tests passed with `ResourceWarning` promoted to errors. The separate audit archive contains the exact ZIP SHA-256 and clean-room benchmark receipt; a finite test suite is not a proof of universal correctness.

## Project layout

- `src/ngegenbrain/`: runtime, contracts, typed operators, mesh, storage, synthesis, ASCR-NG, ASCRC, world models, intents, CLI/API services.
- `web/`: local chatbot-shaped interface and reusable action explorer.
- `tests/`: unit, integration and adversarial regression tests.
- `formalism/`: original reference sources and the developed `theorie_programation_compositionnelle_3.tex` supplement.
- `docs/`: complete user guide, formalism audit, and release report.
- `NGeGenBrain_v1_mise_en_oevre.json`: requirement-by-requirement code and test map.
- The separate `suivi_model_NGeGenBrain_v1.zip` contains the canonical work paths, checklists, checkpoint, failure history, raw independent benchmark results and release receipts.

## License

The included `LICENSE` is a custom non-commercial license, not an OSI-approved open-source license. It permits personal, educational and non-commercial research use under its terms and prohibits commercial use without separate written permission. Review it before redistribution.
