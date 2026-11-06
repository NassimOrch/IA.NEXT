# Architecture ORDER80.4.7

Teacher LLM → 5 specialists → micro master → OIFL → final ORDER.

Specialists: loss, attention_surface, attention_focused, training, focus.

The final has empty initial memory and loads only acquired local artifacts after transfer. The live master and specialists are excluded from target execution.

Orchestration: prompt → think → rethink → act. Focus chooses an observation level before attention action when the task exposes Q/K observations.
