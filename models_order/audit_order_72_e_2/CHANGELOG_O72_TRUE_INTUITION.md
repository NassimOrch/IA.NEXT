# O72 true solution intuition v1.1

- Replaced the previous search-prior intuition with a binary solution judge.
- Explicit dataset schema: problem, problem fingerprint, solution, solution fingerprint, verdict.
- Added exact fingerprint consistency gate.
- Integrated verdict into search ordering only; no hard pruning and no truth certification.
- Added pre-search bounded candidate queries.
- Removed training JSONL from runtime package; full corpus moved to audit package.
- Added deterministic train/validation/test contracts and family-OOD diagnostic.
