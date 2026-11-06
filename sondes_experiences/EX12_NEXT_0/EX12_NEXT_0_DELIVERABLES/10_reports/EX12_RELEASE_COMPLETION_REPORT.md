# EX12_NEXT_0 — rapport de clôture et de livraison

**Date :** 4 novembre 2026  
**Workspace :** `/mnt/data/EX12_NEXT_0`  
**Prompt exécuté :** `prompt_ex12.json` (v1.0.1, changement limité à l'équité `P_trainable ±1%`, original v1.0.0 conservé et hashé).  
**Rapport directeur :** `rapport_prigramme_expermentale_EX12_NEXT_0.tex`.

## 1. État des phases

Le protocole présent dans `prompt_ex12.json` contient huit phases séquentielles, P0 à P7. Il ne contient pas de phases P8–P10 ; P7 est la phase terminale qui inclut verrouillage, scoring, audit et livraison. Les portes P0–P7 sont PASS. `00_governance/PHASE_STATUS.json` est synchronisé sur `COMPLETE`.

| Phase | Objet | État | Preuve principale |
|---|---|---|---|
| P0 | Audit sources/prompts, décisions et préinscription | PASS | `00_governance/phase_gate.json`, `P0_COMPLETION_REPORT.md` |
| P1 | Benchmarks kernels et équivalence numérique | PASS | `00_governance/P1_phase_gate.json`, `P1_BENCHMARK_REPORT.md` |
| P2 | Criblage exploratoire contrôlé | PASS | `P2_PHASE_GATE.json`, registres original/retry et `P2_EXPLORATORY_REPORT.md` |
| P3 | Tâches, données fraîches et généralisation exploratoire | PASS | `P3_phase_gate.json`, `P3_GENERALIZATION_REPORT.md` |
| P4 | Matching MLP par paramètres entraînables | PASS | `P4_phase_gate.json`, `P4_MLP_FAIRNESS_REPORT.md` |
| P5 | Qualité et mesures de ressources | PASS | `P5_phase_gate.json`, `P5_RESOURCE_REPORT_V3.md` |
| P6 | Ablations, diversité et stabilité | PASS | `P6_phase_gate.json`, `P6_FALSIFICATION_REPORT.md` |
| P7 | Gel, tests confirmatoires, scoring et audit | PASS | `P7_phase_gate.json`, audit P7 et rapport confirmatoire |

Le gate P7 valide l'intégrité et la complétude de la campagne ; il ne signifie pas que HC-RBF a gagné scientifiquement.

## 2. Résultats confirmatoires P7

- 640 entraînements confirmatoires réussis : 4 tâches primaires × 20 graines × 8 slots.
- 640 modèles scorés et 2 560 évaluations modèle×régime.
- 80 jeux de test et 640 arrays, générés après gel ; 1 280 comparaisons appariées par graine/régime.
- 16 contrastes primaires d'interpolation ; 11/16 passent la non-infériorité avec marge +0,02 après correction ; 7/16 différences sont significatives après correction de Holm bilatérale.
- Extrapolation nettement défavorable : différence NMAE moyenne candidat−MLP +0,20559 sur les 16 contrastes de tâche×variante. La frontière est favorable dans 15/16 contrastes ; le shift varie selon la tâche.
- L'audit indépendant `04_code/audit_analyze_p7_test.py` exécuté via l'environnement verrouillé a passé 11/11 contrôles, zéro divergence de métriques, 640 modèles, 2 560 lignes métriques et 1 280 paires.

Le rapport détaillé et les données par graine se trouvent dans `10_reports/P7/` et `09_analysis/P7/`.

## 3. Résultat sur les objectifs de recherche

| Critère | Verdict observé |
|---|---|
| Qualité prédictive vs MLP | Mixte et dépendante de la fonction ; pas de victoire générale. |
| Paramètres à égalité | Matching `P_trainable ±1%` vérifié, 320 paires P4 et 320 paires P7. L'ancien objectif GE4X est retiré. |
| Latence et ressources | Échec de l'objectif prioritaire sur CPU : les quatre variantes HC-RBF ont une latence p50 batch 1 supérieure au MLP apparié ; ratios full-path p50 environ 1,82 à 2,25 fois. |
| Temps d'entraînement | Les médianes sont supérieures au MLP ; les mesures end-to-end P5 incluent prétraitement, validation, diagnostics et écritures. |
| Généralisation | Frontière souvent favorable ; extrapolation défavorable sur trois des quatre tâches ; shift hétérogène. |

Le verdict général est **mixte sur la qualité, négatif pour l'objectif prioritaire vitesse/ressources, et insuffisant pour revendiquer un remplacement général du MLP**. Les conclusions sont limitées aux tâches, données, graines et conditions mesurées.

## 4. Variantes et reproduction

`09_analysis/VARIANT_IMPLEMENTATION_EXPERIMENT_MAP.csv` inventorie les variantes et contrôles par phase. Il distingue explicitement les éléments réellement implémentés/testés de ceux différés. C5 et C6 sont `DEFERRED_NOT_IMPLEMENTED` ; ils ne sont pas présentés comme expérimentés. G1/G2 et C1 restent des contrôles exploratoires P2 et ne sont pas promus dans la confirmation P7.

- `05_configs/CONFIG_CATALOG.csv` : 1 460 configurations persistées, avec chemin et hash.
- `07_checkpoints/CHECKPOINT_CATALOG.csv` : 1 360 checkpoints persistés, avec chemin et hash.
- `04_code/SCRIPT_INVENTORY.json` : 58 scripts sources Python inventoriés avec SHA-256.
- `11_reproducibility/REPRODUCTION_GUIDE.md` et `reproduce.sh` : contrôles reproductibles sans entraînement ni nouveau scoring.

## 5. Lacunes de reproductibilité — déclaration consolidée

Les résultats historiques P1_RUN_001/P1_RUN_002 sont présents, mais leurs scripts sources exacts ne le sont pas. Les 13 416 cellules P5 V2 historiques sont présentes, mais le script V2 correspondant au hash enregistré n'a pas été retrouvé ; V3 fournit une reproduction indépendante, complète et hashée. Enfin, 123 terminal records P6 v1 n'ont pas le hash du script dans leur ligne terminale, même si la source v1 est actuellement présente. Ces lacunes et leurs limites sont détaillées dans `EX12_REPRODUCIBILITY_GAPS_SIGNED.md/.pdf` et dans les rapports propres à chaque phase.

Ces écarts ne démontrent pas un sabotage, un vol ou une manipulation intentionnelle. Les artefacts documentent des limites de provenance ; aucune cause intentionnelle n'est établie.

## 6. Contrôle de périmètre du paquet

La livraison est construite exclusivement depuis `EX12_NEXT_0/`. Elle contient les données fraîches EX12, les splits, scripts, configs, checkpoints, registres, logs, prédictions, métriques, benchmarks, audits, rapports, manifestes et instructions de reproduction. Elle exclut `last_sources_3.zip`, `last_sources_3/`, les archives/workspaces/datasets/checkpoints/logs/sauvegardes EX3–EX11, les caches Python/tests et les aperçus de rendu temporaires. Les rapports peuvent citer les noms des campagnes historiques à des fins de provenance, sans inclure leurs artefacts de données.

Le rapport directeur `.tex` est copié byte-identique dans le répertoire de gouvernance ; le chemin et l’empreinte SHA-256 source/copie sont enregistrés dans le manifeste. Le contrôle final de livraison `12_release/P7_DELIVERY_GATE.json` passe 23/23 vérifications. Le manifeste final et les sommes de contrôle sont `12_release/DELIVERABLES_MANIFEST.json` et `12_release/SHA256SUMS`. Le fichier livré est `/mnt/data/EX12_NEXT_0_DELIVERABLES.zip`; son CRC ZIP est vérifié avant livraison.

## 7. Signature et portée

**Rédacteur déclaratif :** ChatGPT, modèle GPT-6, assistant OpenAI.  
**Date :** 4 novembre 2026.  
Cette signature atteste la rédaction du présent rapport sur la base des fichiers et contrôles mentionnés ; ce n'est ni une signature numérique certifiée ni une expertise judiciaire indépendante.
