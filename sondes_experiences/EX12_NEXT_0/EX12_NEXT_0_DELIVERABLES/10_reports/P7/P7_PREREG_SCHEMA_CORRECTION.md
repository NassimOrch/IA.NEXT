# P7 pre-registration schema correction

The first P7 preregistration file was serialized as a JSON list containing one object. The complete original list is preserved as `03_design/P7/P7_PREREGISTRATION_V1_0_1_WRAPPED.json`. The canonical `03_design/P7/P7_PREREGISTRATION.json` is now the same object represented directly as a JSON object. This is a serialization/schema correction only; no split, seed, task, model slot, metric, threshold, quota, stopping rule, or test-access rule was relaxed. The only added explanatory field records that C3 remains a predeclared structural control, while R0/C2/C4 were prioritized at P2.

The exact hashes and change record are in `03_design/P7/P7_PREREG_SCHEMA_CHANGE.json`.
