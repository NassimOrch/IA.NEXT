# CHANGELOG ORDER72 e1

## From e0 to e1

### Security / scientific integrity
- Public exact contract now rejects hidden object attributes, dynamic access, global hidden state and closures.
- Router feedback callback removed.
- Truth-bearing payload fields rejected.
- Exact objective integers are preserved without float coercion.

### Search
- Canonical action ordering under finite budgets.
- Adaptive beam width for delayed rewards.
- Public semantic outcome takes precedence over generic novelty only as open-search evidence.
- Deterministic-Markov plan reuse with per-step verification.

### Laboratory protocol
- DelayedBandit simulation now includes real history.
- TreeBandit simulation now conditions on selected root.
- Final stress campaign split into resource-bounded stages.

### Negative results preserved
- Random-only WM succeeds on current open families.
- Intentionally inverted WM succeeds on current open families.
- These results are interpreted as evidence that the present benchmark does not yet force learned WM competence.
