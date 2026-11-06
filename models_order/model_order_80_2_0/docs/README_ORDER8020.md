# ORDER80.2.0 — Persistent Long-Running Adaptive Observation

Version: **8.0.2.0**  
Base: **ORDER80.2 / proof kernel ORDER80.2-PROOF-KERNEL**

## 1. Objective

ORDER80.2.0 keeps the ORDER80.2 proof system running until a configured wall-clock budget expires, the user interrupts it, or the proof kernel verifies a complete certificate.

The target shipped by default is the structured Riemann Hypothesis task. No Riemann proof, solution certificate, or target-specific solver is embedded in executable source.

## 2. Long-running loop

```text
problem
→ observe
→ synthesize
→ fail
→ observe more
→ synthesize
→ …
→ decompose
→ subproblem
   → observe
   → synthesize
   → fail
   → observe more
   → …
   → decompose again
→ local proof verified
→ memory update
→ root retest
→ peer-probe other unresolved nodes
→ continue
```

After the current search tree has been exhausted without a root certificate, the controller starts another **discovery cycle**. It does not blindly repeat the same proof search: a new solver pass requires a changed formal/memory knowledge signature.

## 3. Time budget

Examples:

```bash
python3 run_order_8_0_2_0.py --duration 1h
python3 run_order_8_0_2_0.py --duration 24h
python3 run_order_8_0_2_0.py --duration 1week
python3 run_order_8_0_2_0.py --duration forever
```

Compound values such as `1h30m` are accepted. `0` is a valid immediate-expiry budget.

A long search is interrupted cooperatively at synthesis checkpoints; partial state is saved.

## 4. Anti-stagnation invariant

The controller tracks:

- formal theorem certificate fingerprints;
- memory certificate fingerprints;
- research chunk hashes;
- web URL and chunk hashes;
- web search query history.

The proof synthesizer is not rerun solely because time passed. Formal/memory knowledge must change first. Documentary/web observations may continue independently because they broaden future discovery, but identical content is not counted as a new observation.

## 5. Local RAG replenishment

The engine watches:

```text
<output>/rag_inbox/documents/
<output>/rag_inbox/formal/
```

When currently indexed sources are exhausted, the model writes a request under:

```text
<output>/rag_requests/
```

and continues polling while the budget remains. Newly added or changed files are indexed during the run.

Formal JSON units are only activated after independent ORDER80.2 kernel verification.

## 6. Web expansion

The web observer supports:

- explicit reference URLs;
- URLs discovered inside already observed local documentary chunks;
- configurable search engines;
- allowlisted domains;
- unique search-query tracking;
- URL/page/chunk hashing;
- link expansion.

Additional time therefore permits new query families rather than fetching the same URL repeatedly.

Web pages remain documentary evidence. Downloading a page never makes it a logical axiom. Only independently verified formal certificates can enter the proof search.

## 7. Persistent novelty archive

Every certificate that is newly verified by the kernel and admitted into persistent memory is copied to:

```text
<output>/news/<sequence>_<proof_fingerprint>/
```

with:

```text
proof.json
demonstration.txt
metadata.json
```

`demonstration.txt` is rendered from the actual `Proof` object produced by the synthesizer. No external reconstruction is performed by the controller.

## 8. Result statuses

`VERIFIED_COMPLETE` means a complete certificate for the formalized target passed the kernel.

`TIME_BUDGET_EXPIRED` means the configured wall-clock budget elapsed without a verified complete certificate.

`INTERRUPTED` means the user interrupted the process and the current state was checkpointed.

These statuses describe the concrete execution only; they do not infer mathematical possibility, impossibility, truth or falsity beyond a certificate that was actually produced and verified.
