# P6 — Note de provenance des scripts

Aucun des scripts principaux de P6 requis pour réexécuter les phases n’est actuellement absent : les fichiers v1, v2, v3 (`run_p6_ablation_v1.py`, `run_p6_ablation_v2.py`, `run_p6_ablation.py`), la réanalyse de similarité (`reanalyze_p6_error_similarity.py`) et l’analyse inter-graines (`analyze_p6_crossseed_roles.py`) sont présents. Leurs SHA-256 sont consignés dans `P6_INTEGRITY_AUDIT.json`.

Il existe néanmoins une lacune de traçabilité pour les 123 enregistrements SUCCESS issus de la première version : leur enregistrement terminal ne contient ni `attempt_id` ni `script_sha256`. Le fichier source v1 a été récupéré et hashé après le démarrage des premières exécutions. Il est donc disponible pour inspection et reproduction, mais les métadonnées append-only ne prouvent pas cryptographiquement que chaque run historique a été lancé avec exactement ces octets. Les 25 enregistrements v2 et 172 enregistrements v3 comportent un hash de script.

Cette situation ne permet pas d’affirmer que les scripts ont été supprimés, volés ou sabotés. Elle impose seulement une réserve de provenance sur les 123 premiers runs. Les données, checkpoints, résultats et scripts actuellement présents sont conservés ; aucune lacune n’a été masquée.
