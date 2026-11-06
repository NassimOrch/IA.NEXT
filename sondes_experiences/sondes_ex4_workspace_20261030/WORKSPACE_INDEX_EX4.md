# WORKSPACE_INDEX_EX4

| Version | Statut | Contenu / correction | Limite / note |
|---|---|---|---|
| v001 | ABANDONED | Premier micro-benchmark | Pipeline de prétraitement non strict, fixed-only à corriger |
| v002 | ABANDONED | Contrôleur adaptation simple | Déclencheur inopérant et sélection de données après transformation |
| v003 | ABANDONED | Patience adaptation et géométries | Experts dormants préalloués et comptés |
| v004 | ABANDONED | Loader train/val/adapt et contrôles immédiat/linéaire/RETRO | Comptage capacité/scaler incomplet |
| v005 | COMPLETED (intermédiaire) | Croissance dynamique réellement instanciée, 60 sondes/85 MLP/120 paires | Scaler commun omis du P_total |
| v006 | COMPLETED (développement) | Comptage scaler corrigé, 60 sondes/135 MLP/120 paires | Wisconsin historique ; pas mesures ressources complètes |
| v007 | MIXED REGISTRY / QUARANTINED | 70 lignes initiales + 25 add-on micro-MIXA | Test global historique échoue sur comptage 95 vs 70 ; utiliser uniquement audits filtrés |
| v008 | PASS (audit de récupération) | 25 runs micro-MIXA récupérés, 30 MLP, 50 paires | Wisconsin historique ; métadonnée adaptation source corrigée séparément |
| v009 | COMPLETED (transfert exploratoire) | Iris : 20 sondes, 40 MLP, test descriptif, audit d'intégrité PASS | n_test=30 ; API charge complet ; pas d'isolation mémoire stricte ; training time de 5 checkpoints adaptatifs ND |

## Livrables principaux
- `prompt_ex4.json` et copies synchronisées dans `inputs/` / versions pertinentes.
- `deliverables/debrit_0_reconstruction.md`
- `deliverables/rapport_executif_ex4.md`
- `deliverables/rapport_technique_ex4.md`
- `deliverables/rapport_micro_mixa_ex4.md`
- `deliverables/rapport_transfert_externe_iris.md`
- `deliverables/AUDIT_V007_MIXED_REGISTRY.md`
- `deliverables/tableau_conformite_ex4.md`

## Artefacts bruts / audits
- v006 : `results/raw/`, `results/processed/`, `tests/test_ex4_integrity.py`.
- v008 : récupération micro-MIXA filtrée et `ex4_micro_mixa_recovery_audit.json`.
- v009 : snapshots Iris, checkpoints, `ex4_iris_freeze_manifest.json`, `ex4_iris_integrity_audit.json`, script d'audit et comparaisons appariées.

## Continuité finale
- `deliverables/rapport_continuite_finale_ex4.md` : reprise, conformité, état d'intégrité et obstacles.
- `deliverables/manifest_livrables.md` : catalogue de livraison.
- `checksums/final_test_status.txt` : statut des tests rejoués lors de la reprise (v005/v006/v008/v009 PASS ; test global v007 FAIL attendu sur registre mélangé).
