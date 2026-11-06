# Workspace EX4 — sondes adaptatives compactes contre MLP

**Date de gel/livraison :** 30 octobre 2026  
**Dernière version :** `sondes_ex4_v009__2026-10-30`  
**État :** développement Wisconsin + récupération micro-MIXA + un transfert Iris exploratoire achevé ; succès global non démontré.

## Objectif
Trouver une sonde ayant au plus 25 % des coefficients numériques persistants d'un MLP compétitif (P_MLP/P_sonde ≥ 4), sans infériorité en accuracy et log-loss, et avec des coûts inférieurs ou égaux. Paramètres fixes, entraînables et prétraitement partagé sont distingués.

## Conclusion scientifique
Les sondes compactes satisfont le ratio de paramètres mais ne battent pas simultanément les MLP en accuracy, log-loss et ressources. Sur Wisconsin, aucune des 12 familles v006 ne satisfait l'ensemble des conditions. Sur Iris, quatre candidates (adaptatif et trois micro-MIXA) ont été évaluées sur cinq initialisations ; accuracy parfois égale au MLP mais log-loss et latence moins bonnes. L'objectif n'est pas atteint.

## Résultats et livrables
- `prompt_ex4.json` : copie révisée de `prompt_ex3.json`, complétée par la piste micro-MIXA.
- `deliverables/debrit_0_reconstruction.md` : extraction des idées et limites des débris.
- `deliverables/rapport_executif_ex4.md`, `rapport_technique_ex4.md` : conclusions et protocole détaillés.
- `deliverables/rapport_micro_mixa_ex4.md` : hybride micro-MIXA et ablations.
- `deliverables/rapport_transfert_externe_iris.md` : transfert et limites d'isolation.
- `deliverables/AUDIT_V007_MIXED_REGISTRY.md` : séparation du registre mélangeant deux campagnes.
- `deliverables/tableau_conformite_ex4.md` : conformité exigence par exigence.
- `versions/` : v001–v009, scripts, logs, données, prédictions brutes, tables, états modèles, audits et checksums.

## État des preuves
- v005 et v006 : tests d'intégrité PASS, Wisconsin historique.
- v007 : registre brut de 95 lignes mélangeant 70 initiales + 25 add-on ; test historique non filtré échoue par comptage ; audits filtrés séparés passés.
- v008 : récupération micro-MIXA Wisconsin PASS, sans réentraînement, ratios ≥4x.
- v009 : transfert Iris PASS audit technique, 20 sondes, 40 MLP, 60 métriques test, aucun réglage après test. Réserve explicite : loader Iris matérialise le dataset complet et la stratification lit les labels ; pas d'isolation mémoire stricte.

## Non achevé / obstacles
- Workspace/code/checkpoints EX3 et jeux bruts cités dans les débris absents de l'archive.
- Banknote Authentication et MAGIC Gamma Telescope indisponibles au téléchargement à cause de la résolution DNS/réseau de l'environnement.
- Pas de confirmation multi-domaines vierge, pas d'IC de non-infériorité, pas de mesures hardware complètes des FLOPs/MAC, VRAM, énergie ou coût total de recherche.
- Cinq seeds signifient cinq initialisations, pas cinq jeux indépendants.

## Vérifications rapides
```bash
cd versions/sondes_ex4_v006__2026-10-30 && python tests/test_ex4_integrity.py
cd ../sondes_ex4_v008__2026-10-30 && python scripts/audit_micro_mixa_recovery.py
cd ../sondes_ex4_v009__2026-10-30 && python scripts/audit_iris_transfer.py
```

## Continuité finale et intégrité
Le rapport de continuité final est disponible dans `deliverables/rapport_continuite_finale_ex4.md` et le catalogue des artefacts dans `deliverables/manifest_livrables.md`. Lors de la reprise, les copies de `prompt_ex4.json` ont toutes été relues comme JSON et vérifiées identiques (SHA-256 `39471af7dabb7ad80a6379b6c2d2cc53a41d8a35af6369c344b82bd1546b36d4`). Les derniers tests v005, v006, v008 et v009 passent. Le test global historique v007 échoue toujours de façon attendue sur le comptage (95 entrées au lieu de 70) ; les audits filtrés sont la référence pour ce registre mixte. Les journaux et preuves de ces exécutions figurent dans `checksums/`.

**Conclusion ferme :** objectif de réduction des paramètres atteint, mais objectif conjoint performance + ressources non atteint. La campagne reste partielle au sens strict du prompt faute de datasets Banknote/MAGIC récupérables, d'énergie/VRAM mesurées et de démonstration statistique formelle de non-infériorité.
