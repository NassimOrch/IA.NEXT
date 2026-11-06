# Workspace EX5 — état consolidé v001–v007 (30 octobre 2026)

EX5 est une campagne versionnée prolongeant EX4 : RETRO/Adam, proportions fixes-adaptatives, correcteur alterné A↔B, micro-MIXA hiérarchique question/réponse, résidus OOF, optimisation du partage encodeur/centres, PCA question-only, transfert Wine/Digits et profilage CPU. Les artefacts historiques, registres bruts, checkpoints et prédictions sont conservés ; les tableaux sont dérivés.

## Conclusion scientifique

Aucune candidate ne démontre simultanément la non-infériorité prédictive pré-enregistrée et la conformité à chacune des dimensions obligatoires mesurées de la règle rouge. Les 437 comparaisons physiques MLP ge4x auditées respectent `P_MLP_total / P_sonde_total >= 4` (minimum 4,000735×). L'OOF est entièrement livré et audité, mais plus lent en entraînement et en latence batch 1 que son MLP ge4x. La règle rouge globale n'est donc pas satisfaite.

## Versions expérimentales

- v001 : RETRO/factoriel, proportions, OOF résiduel et premières topologies Q/A.
- v002 : sémantiques Adam/gel et alternance A↔B.
- v003 : transfert Wine/Digits, gel test et bootstrap apparié.
- v004 : ablations hiérarchiques questions/réponses.
- v005 : partage d'encodeur/centres et optimisation micro-MIXA.
- v006 : PCA question-only, MLP appariés et vectorisation.
- v007 : profilage TorchScript/Numba sans réentraînement ; parité stricte contrôlée.

## OOF — artefacts complets

La famille `TWO_LEVEL_OOF_RESIDUAL` comprend 25 modèles fold (5 folds × 5 graines), 25 états de reprise avec Adam, 25 marqueurs, cinq caches OOF, dix composites finaux (tête fixe/adaptative × cinq graines), dix états de reprise de la tête, dix fichiers de métriques, dix prédictions, et 20 liens MLP matched/ge4x. L'audit spécifique recense 162 artefacts sans manque et vérifie les partitions, les prédictions OOF, la réinférence composite et les métriques (écart maximal 0). Le forward n'accepte que X. Voir `deliverables/oof_artifact_manifest_ex5.csv`, `oof_artifact_audit_ex5.json` et `rapport_oof_mlp_appariement_ex5.md`.

## Nomenclature sans ambiguïté

- `MIXA` (`MIXA_GENERAL`) : famille générale adaptative + banque fixe + mélange appris.
- `micro-MIXA` (`MICRO_MIXA`) : instanciation compacte explorée dans EX4/EX5.
- `MiXA` et `micro-MiXA` : alias de casse uniquement, pas de modèle supplémentaire.
- `mixa_micro_d4_k8` : alias historique de micro-MIXA ; la valeur de 528 coefficients des débris demeure non vérifiable.

Voir `deliverables/NOMENCLATURE_EX5.md`, `nomenclature_registry_ex5.json`, `INDEX_VARIANTS_EX5.md` et `catalogue_campagnes_ex5.csv`.

## Intégrité et limites

Le dernier audit complet couvre 3 951 fichiers non-cache : 1 865 JSON valides, 1 720 lignes JSONL dans 53 fichiers et 60 CSV rectangulaires. Aucun défaut de parsing/forme, aucun hash prompt divergent, aucun lien symbolique sortant. Les audits des versions contrôlent 1 313 références checkpoint, 1 162 références canoniques de prédiction, 826 recalculs et 437 liens ge4x sans divergence/ratio inférieur à 4. Les doublons et pointeurs remplacés sont conservés et documentés.

Banknote/MAGIC sont bloqués par l'échec DNS du runtime ; VRAM et énergie ne sont pas mesurables (CPU-only) ; les MACs complets d'entraînement et une télémétrie RSS uniforme restent non mesurés. EX5 n'est donc pas déclaré complet au sens de la réussite scientifique globale.

## Documents de référence

- `deliverables/rapport_reprise_finale_ex5.md`
- `deliverables/rapport_executif_ex5.md` et `rapport_technique_ex5.md`
- `deliverables/rapport_retro_adam_ex5.md`
- `deliverables/rapport_micro_mixa_ex5.md`
- `deliverables/rapport_alternance_hierarchie_ex5.md`
- `deliverables/rapport_oof_mlp_appariement_ex5.md`
- `deliverables/rapport_generalisation_ex5.md` et `rapport_ressources_ex5.md`
- `deliverables/matrice_conformite_ex5.md`
- `deliverables/audit_integrite_ex5.md` et manifestes SHA-256

Prompt actif : `inputs/prompt_ex5.json` (v1.1), SHA-256 `88f67fc34bf34c5ca0817da42a057ed71dfb092cfb33720be5532da96bab3291`. La version 1.0 et les prompts de référence sont conservés.
