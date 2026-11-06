# NG-Recomposed-TinyLM-v3_1 (preservation release)

This model composes the existing independent v3_0 byte-GRU language-generation path with a newly trained multi-view observation router. The language model parameters, legacy route and adapters are copied exactly from v3_0 and frozen. The additional view router receives both recurrent context representations and direct byte embeddings and is trained on the English multi-view observation dataset.

- Total parameters: 55568
- Preserved legacy generation parameters: 54536
- New observation-router parameters: 1032
- Best step (validation only): 1700
- Held-out view classification: 4/16 (25.0%)
- Exact generation-logit identity check vs v3_0: True, max absolute delta 0.0

The classifier affects observation output only and does not perturb generation logits. This is intentional because the alternative joint-finetuned student degraded the common held-out bits-per-byte test. The model remains a tiny LM and does not claim equivalence to SmolLM2 or TinyLLM.
