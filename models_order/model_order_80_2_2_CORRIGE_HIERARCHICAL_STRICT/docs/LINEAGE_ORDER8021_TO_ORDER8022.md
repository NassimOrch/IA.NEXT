# Lignée ORDER80.2.1 → ORDER80.2.2

Base directe : `model_order_8_0_2_1.zip`.

Diagnostic : le chemin généraliste O80.2.1 n’utilisait pas le moteur hiérarchique formel qui contenait déjà `decompose`/`peer_probe`. Le second diagnostic était sémantique : le vérificateur général pouvait renvoyer `EVIDENCE_SYNTHESIS_VERIFIED` sur des tâches demandant une résolution complète.

Correction : nouveau `run_order_8_0_2_2.py` + `HierarchicalGeneralEngine`, séparation `DOCUMENTED_INSIGHT`/résolution complète, tests et audit associés.
