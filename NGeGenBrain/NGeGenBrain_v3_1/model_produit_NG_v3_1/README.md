# NG-Recomposed-TinyLM-v3_1 (preservation release)

This product composes the existing independent v3_0 byte-GRU language-generation path with a newly trained multi-view observation router. The v3_0 language-generation parameters and legacy output route are copied exactly and frozen. The additional observation router has 1,032 parameters and was trained on the English multi-view observation dataset derived from direct, recorded observations of the supplied SmolLM2 GGUF and TinyLLM PyTorch models. No teacher weights or teacher logits are copied into the student.

- Total parameters: 55,568
- Preserved legacy generation parameters: 54,536
- New observation-router parameters: 1,032
- Best checkpoint step selected from validation-window loss: 1700
- Final fresh held-out view classification: 9/32 (28.1%), with 8 classes and 4 documents per class; uniform chance is 12.5%
- Document-level validation classification: 2/16 (12.5%)
- Exact generation-logit identity check vs v3_0: True, max absolute delta 0.0

The observation router is a separate analytical path and does not alter generation logits. The fresh test result is small and exploratory; it is not evidence of robust view classification. This is a tiny causal language model, not a replacement for SmolLM2 or TinyLLM and not a claim of mechanistic equivalence to either source model.
