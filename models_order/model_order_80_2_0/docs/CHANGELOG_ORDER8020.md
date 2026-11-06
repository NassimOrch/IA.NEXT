# Changelog ORDER80.2.0

## 8.0.2.0

### Added

- persistent wall-clock budget (`1h`, `24h`, `1week`, `forever`, compound forms);
- cooperative budget checks inside proof synthesis;
- outer long-running discovery cycles;
- dynamic refresh of local formal and documentary RAG sources;
- monitored RAG inbox and explicit `rag_more_data_requested` events;
- persistent checkpoint file;
- query-family diversification and web search de-duplication;
- `news/` archive for every newly verified demonstration;
- standalone `self_test_order8020.py`.

### Preserved

- ORDER80.2 proof kernel and recursive subproblem logic;
- persistent verified-proof memory;
- documentary/web separation from logical premises;
- strict novelty fingerprinting;
- no target-specific solution code.

### Non-goals

ORDER80.2.0 does not infer the truth or falsity of an unresolved target from timeout, stagnation, missing sources, or interrupted execution.
