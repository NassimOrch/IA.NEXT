# API contract — eSonde

## Common data types

- `Token`: `surface`, `normalized`, `start`, `end`, `kind`, `document_id`. Les offsets `start/end` sont des indices de points de code Python dans le texte d’origine, non des offsets UTF-8 en octets.
- `ProbeResponse`: `family`, `distribution: dict[str,float]`, `support: int`, `distance: float|null`, `entropy: float|null`, `diagnostics: list[str]`, `provenance: list[dict]`, `active: bool`.
- `Prediction`: `distribution`, `top_tokens`, `family_responses`, `coordinator_weights`, `diagnostics`, `copy_attribution`.
- `GenerationResult`: `text`, `tokens`, `seed`, `strategy`, `trace`, `stop_reason`.
- `TrainingReport`: corpus manifest, counts by family, calibration status, elapsed time, skipped/rejected records and integrity hashes.

## Methods

```python
Tokenizer.tokenize(text: str, document_id: str = "inline") -> list[Token]
ProbeModel.train(train_documents, config=None, validation_documents=None, batch_id="initial-train") -> TrainingReport
ProbeModel.update(documents, batch_id: str) -> TrainingReport
ProbeModel.remove_batch(batch_id: str) -> dict
ProbeModel.calibrate(validation_documents) -> dict
ProbeModel.predict_next(text: str, top_k: int = 10) -> Prediction
ProbeModel.generate(prompt: str, max_tokens: int = 64, strategy: str = "greedy", seed: int = 0) -> GenerationResult
ProbeModel.score(documents) -> dict
ProbeModel.retrieve(query: str, top_k: int = 5) -> list[dict]
ProbeModel.find_relations(left=None, relation=None, right=None, top_k=20) -> list[dict]
ProbeModel.coreference_candidates(text: str, top_k=20) -> list[dict]
ProbeModel.inspect(family: str, key: str | None = None) -> dict
ProbeModel.audit() -> dict
ProbeModel.save(path) -> dict
ProbeModel.load(path) -> ProbeModel
```

The concrete API may add optional keyword arguments without breaking these defaults. It must not change the data semantics. Invalid family names, negative budgets, invalid probability parameters, corrupted model states and unreadable corpus paths raise explicit typed exceptions. Public CLI code translates them to stable non-zero exit codes.

## API invariants

1. Training reads only train documents for probes and base counts.
2. Validation is used only for calibration/hyperparameter selection; `calibrate()` never modifies probe tables and replaces only the validation manifest and COORD weights.
3. `score()` is read-only and cannot update probe tables or COORD weights; it reports bounded-context truncation in `context_window`.
4. Retrieval outputs carry source/document/offset attribution.
5. SEM relation records are induced only from observed completed clause prefixes and retain the source evidence; the extraction is candidate-level, not a verified parser.
6. DISC coreference results are ranked surface-mention/alias candidates (`resolved=false`), never forced single antecedents.
7. `remove_batch()` replays all retained source batches exactly, including rebuilding RETR; it refuses legacy checkpoints without a complete retained-text ledger rather than approximating decrements.
8. Checkpoints from newly trained models retain UTF-8 training/validation texts for exact retraction; protect them as sensitive corpus-bearing files.
9. `max_context=0` disables the additional global cap; each probe still uses its own configured local window. Positive caps surface `TRUNCATED_CONTEXT` and the number of discarded prefix items in prediction/score reports.
10. `save()` never deletes or partially overwrites a previous valid model.
11. `load()` validates minimum schema, payload digest, exact-file sidecar and tokenizer compatibility before exposing a model object.
12. `inspect()` is read-only and emits enough information to reproduce the support decision.
13. `generate()` is reproducible for greedy decoding or a fixed seed.
14. No public API calls a neural model or imports a neural framework.
15. GUI and CLI use the same `ProbeModel` implementation.
