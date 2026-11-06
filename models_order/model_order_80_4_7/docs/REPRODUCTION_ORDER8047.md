# Reproduction — ORDER80.4.7

Extract model, micro and LLM packages under the same parent directory. Run the LLM verifier first, then `model_order_8_0_4_7/pipeline/reproduce_order_8_0_4_7.sh`.

The script reconstructs specialists from teacher traces, creates the specialist observation stream, trains the master only on specialist outputs, acquires the master through the OIFL subprocess interface, rebuilds the router, and runs the release tests.

Strict acquisition path does not train specialists on the raw corpus. The new dataset is reserved for post-acquisition evaluation/training experiments.

The final reproduction script resolves the sibling packages from the parent of `model_order_8_0_4_7`, so the four archives must be extracted side-by-side under one release root. This path was tested from a fresh extraction.
