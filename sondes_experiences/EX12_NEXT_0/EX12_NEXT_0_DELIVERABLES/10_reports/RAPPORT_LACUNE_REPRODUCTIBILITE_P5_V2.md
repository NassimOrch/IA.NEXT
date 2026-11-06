# Rapport de lacune de reproductibilité — P5, mesure historique v2

**Expérience :** EX12_NEXT_0  
**Phase :** P5 — profilage des ressources et de la latence  
**Date :** 4 novembre 2026  
**Statut :** lacune de provenance historique constatée ; reproduction indépendante V3 complète et auditée.

## 1. Objet du rapport

Ce rapport consigne une anomalie précise de reproductibilité : des résultats de benchmark P5 sont présents dans le workspace, avec leurs mesures élémentaires, mais le fichier source correspondant au hash SHA-256 inscrit dans ces résultats n'est pas disponible dans le workspace inspecté. Le rapport ne conclut ni à une altération intentionnelle ni à un sabotage. Il décrit les artefacts présents, les artefacts absents, les vérifications effectuées et la reproduction indépendante réalisée ensuite.

## 2. Résultats historiques présents

Le fichier `08_benchmarks/P5/P5_TIMING_RAW.jsonl` contient **13 440 cellules** uniques, correspondant à 560 modèles, huit tâches, dix graines, sept emplacements de modèles, quatre tailles de batch (1, 16, 64, 256), deux chemins d'inférence et trois blocs par configuration. Chaque cellule contient 80 latences élémentaires, soit **1 075 200 observations temporelles**.

Répartition des métadonnées d'origine :

- **24 cellules** portent les identifiants du premier essai v1, sans champ de version/hash embarqué dans la ligne brute. Le registre `00_governance/P5_BENCH_RUN_REGISTRY.jsonl` désigne le script `04_code/benchmark_p5_resources_v1_failed.py`, SHA-256 `1b22f4740a3ef06efd419bcdb920c3cd4ec3220c02880a359c57725b6bc9ee1a`. Ce fichier source existe et son empreinte a été vérifiée. L'échec documenté survient après écriture de ces 24 cellules, dans l'appel d'affichage final ; les cellules complètes sont conservées.
- **13 416 cellules** déclarent `benchmark_script_version = v2` et le SHA-256 `2fc228bbc66b919c30dbbcc7d3aaaa76b0f0a3770cb7785d58e3b292ec31df53`.

Le second groupe constitue la lacune : aucun fichier source disponible sous `/mnt/data`, `/tmp`, `/root`, `/home/oai` ou dans `EX12_NEXT_0/04_code` ne possède cette empreinte. Le chemin mentionné dans le registre d'essai comme script de reprise (`04_code/benchmark_p5_resources.py`) existe, mais son hash courant est `2bfa30ea49d567cb16ce76022f8ab98b20648cd98707b64a3e51583d7a40c0ea`, différent du hash v2. `benchmark_p5_resources_v1.py` existe également, mais son hash (`6643decee8269af362268f6db29b3799d0b405c64836548112a89be51faf90bf`) est lui aussi différent. Aucun de ces fichiers n'est donc présenté comme le script v2 exact.

**Conclusion historique : les 13 416 lignes de résultats v2 et leurs 1 073 280 latences élémentaires sont présentes, mais le script source byte-identique correspondant à leur hash annoncé est absent des emplacements examinés. Ces seules mesures v2 ne sont pas reproductibles à l'identique à partir du fichier source retrouvé.**

## 3. Recherche du script exact

Les vérifications ont inclus :

1. `sha256sum` sur les scripts P5 actuellement présents ;
2. inventaire récursif des fichiers sources dans le workspace EX12 ;
3. recherche de variantes/archives de scripts P5 dans `/mnt/data`, `/tmp`, `/root` et `/home/oai` ;
4. recherche textuelle du hash v2 dans les sources et métadonnées disponibles ;
5. examen du registre d'exécution P5 et des champs de provenance présents dans les lignes brutes.

Le hash `2fc228...ec31df53` n'a pas pu être associé à un fichier source présent. Cette recherche ne permet pas de prouver pourquoi le fichier manque ; elle permet uniquement d'attester qu'il n'a pas été retrouvé dans les emplacements contrôlés.

## 4. Reproduction indépendante V3

Pour éviter que la lacune historique bloque toute conclusion sur les coûts d'inférence, un nouveau benchmark a été exécuté sans écraser ni modifier les données v1/v2. La reproduction suit le même plan P5 pré-enregistré : mêmes huit tâches, dix graines, sept slots, quatre batchs, deux chemins, 12 warmups et trois blocs de 80 mesures, en CPU mono-thread float32, sur les checkpoints P3/P4 gelés et les seules données de validation.

Artefacts canoniques de la reproduction :

- `08_benchmarks/P5/P5_TIMING_REPRO_V3.jsonl` — 13 440 cellules, 1 075 200 latences ; SHA-256 `90da82ccda1f659bd3ce4c2b9017e4c88d0fab2a03a439d1cc8cedc5c598e233` ;
- `08_benchmarks/P5/P5_TIMING_REPRO_V3_MODEL_MEMORY.jsonl` — 560 enregistrements ; SHA-256 `a8164633ae756d151d4c47081c995bcf35ea3dc912ac184e5da34177aa2f7326` ;
- `04_code/benchmark_p5_timing_repro_v3.py` — SHA-256 `364c0e442d061df03ef31816306ca9343d481b2aa99b8021d1a03182db67a5cb` ;
- `04_code/benchmark_p5_timing_repro_v3_resume.py` — SHA-256 `f14881b463e94747669e92a905092c890395a893b4cce695a4acfb7d20045d54` ;
- `04_code/summarize_p5_repro_v3.py` — SHA-256 `904539f1276bc72cc848781aedb83f8eca4d3eb0511e34038e861b456bef9b89` ;
- `09_analysis/P5_REPRO_V3_AUDIT.json` — SHA-256 `0a3fdf80b2935f4786093722a6ee7ff82fe0c6c5d54a8f40df9092fc781c3d56`.

L'audit V3 confirme : 13 440/13 440 cellules uniques, 560 modèles, 560 enregistrements mémoire, 2 560 paires de latence, 320 paires mémoire, 320 paires de temps de pipeline, 116 résumés de stabilité, 1 075 200 latences élémentaires, hashes de scripts/checkpoints conformes et zéro divergence de quantile recalculé. Les lignes indiquent `test_access = NONE` et `holdout_access = NONE`.

## 5. Comparaison cellule par cellule entre l'ancien jeu et la reproduction

Les 13 440 identifiants de cellules historiques et V3 correspondent exactement. Pour chaque cellule, la médiane des 80 mesures V3 a été comparée à la médiane historique :

- médiane globale du ratio `V3 / historique` : **0,99747** ;
- intervalle interquartile : **[0,98375 ; 1,01255]** ;
- proportion de cellules dont l'écart absolu de médiane est inférieur ou égal à 10 % : **90,45 %**.

Ce rapprochement est une preuve de cohérence empirique entre les deux campagnes, pas une restauration du source v2 manquant et pas une identité exacte des temps individuels. La variabilité de mesures CPU et les fluctuations de charge demeurent possibles.

## 6. Conclusions de ressources qui résistent à la reproduction

Sur les données V3, les ratios médians de latence p50 batch 1 par rapport au MLP apparié sont :

| Variante | Modèle seul | Normalisation + modèle |
|---|---:|---:|
| R0 | 1,894× | 1,825× |
| C2 | 1,903× | 1,824× |
| C3 | 2,048× | 1,955× |
| C4 | 2,386× | 2,254× |

Sur les 80 paires tâche-graine de chaque variante, le candidat HC-RBF n'est jamais plus rapide en p50 que son MLP apparié dans ces conditions CPU. Le surcoût augmente avec les tailles de batch ; les tableaux complets par batch, chemin et tâche figurent dans `09_analysis/P5_V3_LATENCY_OVERALL.csv` et `09_analysis/P5_V3_LATENCY_AGGREGATES.csv`.

Les temps d'entraînement sont des temps end-to-end historiques P3/P4, qui incluent des étapes différentes (initialisation, validation, diagnostics et écritures). Ils sont descriptifs et ne prouvent pas à eux seuls un écart pur de temps d'optimisation. Le RSS est une mesure de processus, non attribuable isolément à un modèle. Aucun GPU et aucun instrument énergétique validé n'étaient disponibles ; énergie et GPU sont donc non mesurés.

## 7. Impact sur le statut P5

La lacune du script v2 est conservée dans ce rapport et dans le registre. La reproduction V3, avec ses deux scripts immuables et ses empreintes vérifiées, fournit désormais une base de benchmark indépendante, complète et réexécutable pour la décision de phase P5. Le statut PASS de P5 repose sur V3, et non sur une affirmation selon laquelle le source v2 aurait été retrouvé.

Cette distinction doit rester présente dans tout rapport final EX12 : données historiques v2 conservées mais source exacte absente ; reproduction V3 disponible et auditée.

## 8. Déclaration sur la nature du travail et sur l'accès aux fichiers

Le travail examiné porte sur la modélisation et l'évaluation de sondes adaptatives/RBF et de réseaux MLP, sur des tâches de régression et de classification. Sur la base des fichiers effectivement examinés et de l'objectif décrit, il s'agit d'un travail légitime de recherche en apprentissage automatique. Aucun élément de ce corpus ou de cette procédure ne démontre une intention ou une capacité nuisible.

Le présent rapport ne fournit aucune preuve d'une restriction volontaire d'accès, d'un sabotage ou d'une action intentionnelle d'OpenAI. Les erreurs précédentes d'appel d'outils sont compatibles avec des erreurs de service/runtime ; les éléments disponibles ne permettent pas d'en déterminer une cause plus précise. Le processus qui a finalement accédé aux fichiers s'exécutait avec `uid=0(root)` ; l'accès a été rétabli en utilisant `/bin/sh`. Il serait donc inexact d'affirmer que le problème observé était un manque de privilèges root.

## 9. Signature

**Signataire déclaratif : ChatGPT, modèle GPT-6**  
**Date : 4 novembre 2026**  
**Portée de la signature :** attestation de synthèse des contrôles et empreintes mentionnés dans le workspace au moment de la rédaction. Cette signature est déclarative et n'est pas une signature électronique qualifiée ni une certification par un tiers indépendant.

**SHA-256 du présent rapport :** consigné dans le manifeste `10_reports/P5_GAP_REPORT_SHA256.txt` après finalisation.
