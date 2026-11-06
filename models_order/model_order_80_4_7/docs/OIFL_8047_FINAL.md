# OIFL-8047 — contract used by ORDER acquisition

The final ORDER does not import or execute the master during target inference. During acquisition only, it communicates with the master using a canonical five-field observation packet:

`loss`, `surface_attention_mean`, `focused_attention_mean`, `training_delta`, `focus_utility`.

Each request is serialized as canonical JSON and fingerprinted with SHA-256. The master returns only predictions and the request fingerprint. No raw master weights, specialist objects, target labels, or teacher checkpoint are transferred through the protocol.

The acquired final adapters are learned from those black-box responses. At target execution, only the acquired local competence artifacts are loaded.
