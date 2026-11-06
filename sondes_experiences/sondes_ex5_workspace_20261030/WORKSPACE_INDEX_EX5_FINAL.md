# Index final du workspace EX5 — v001 à v007

| Dossier | Rôle et contenu |
|---|---|
| `inputs/` | prompt actif v1.1, SHA-256, révision 1.0 préservée, prompts EX3/EX4 de référence et manifeste des sources |
| `versions/sondes_ex5_v001__2026-10-30/` | RETRO/factoriel, proportions, OOF, hiérarchie, folds, checkpoints, états Adam, prédictions et MLP |
| `versions/sondes_ex5_v002__2026-10-30/` | politiques Adam/gel et alternance A↔B |
| `versions/sondes_ex5_v003__2026-10-30/` | transfert Wine/Digits, pré-enregistrement, gel avant test, prédictions et bootstrap |
| `versions/sondes_ex5_v004__2026-10-30/` | ablations hiérarchiques Q/A |
| `versions/sondes_ex5_v005__2026-10-30/` | partage encodeur/centres micro-MIXA |
| `versions/sondes_ex5_v006__2026-10-30/` | PCA question-only, comparateurs et vectorisation |
| `versions/sondes_ex5_v007__2026-10-30/` | profils TorchScript/Numba et tests de parité CPU |
| `scripts/` | audit global, audit OOF, catalogue des variantes, audit workspace final |
| `tests/` | liaison MLP OOF, vérification intégrale des artefacts OOF |
| `deliverables/` | rapports, matrice de conformité, catalogues, prédictions/mappings OOF, audits, hashes et commandes de reproduction |

## Sources d'autorité

Les JSONL sous `versions/*/results/raw/`, les checkpoints `results/models/`, les manifestes de partitions et prédictions sont les sources d'autorité. Les agrégats CSV/JSON et rapports sont dérivés. Aucun doublon ni pointeur historique n'a été effacé pour rendre un test artificiellement vert.

## OOF complet

Voir `deliverables/oof_artifact_manifest_ex5.csv` (162 entrées), `oof_artifact_audit_ex5.json`, `oof_mlp_comparison_links.csv`, `oof_validation_metrics_audit.csv`, `rapport_oof_mlp_appariement_ex5.md`, ainsi que le script `scripts/audit_oof_artifacts_ex5.py` et le test `tests/test_oof_artifacts_complete.py`.

## Nomenclature

`MIXA` = famille générique ; `micro-MIXA` = reconstruction compacte ; `MiXA`/`micro-MiXA` = alias de casse ; `mixa_micro_d4_k8` = alias historique non autonome. Aucun quatrième modèle n'est créé pour la seule variation de casse.

## Intégrité finale

Consulter `deliverables/audit_integrite_workspace_final.json` et `deliverables/sha256_manifest_workspace_final.csv`. Le dernier scan : 3 951 fichiers non-cache, 1 865 JSON, 1 720 lignes JSONL, 60 CSV rectangulaires, prompt externe/interne identique au SHA attendu et aucun lien symbolique sortant.
