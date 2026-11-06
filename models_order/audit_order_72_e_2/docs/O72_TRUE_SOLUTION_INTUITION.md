# O72 - True Solution Intuition

The intuition module is a binary learned judge over explicit problem/solution pairs.

Formal interface:

`I(P, F(P), S, F(S)) -> (verdict, probability)`

where `P` is the observed problem, `F(P)` its deterministic canonical fingerprint, `S` is a candidate solution/state, and `F(S)` its fingerprint. The runtime verifies both fingerprints before inference. A `true` verdict means only that the learned judge predicts the candidate belongs to the positive class; it is never an external proof.

## Dataset label

For the deterministic symbolic training environments, a candidate successor is labeled true iff it attains the maximum public transition reward among all legal actions for the same problem; all ties are true. Every row stores:

- `probleme`
- `empreinte_probleme`
- `solution`
- `empreinte_solution`
- `verdict`

The runtime package does not contain the training JSONL files. They are kept in the audit package; the model checkpoint stores only training manifests and dataset hashes.

## Search integration

The judge is queried on bounded one-step candidate consequences before deeper search and on candidate consequences during expansion. `true` increases priority; `false` decreases priority. Neither verdict can hard-prune a candidate. The external verifier and, when available, the public objective remain independent.

A problem-only call cannot logically return a solution truth value without a candidate solution. The runtime therefore exposes no fake problem-only truth oracle. The pre-search stage constructs a bounded public candidate set first and then asks the true/false judge.
