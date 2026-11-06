# Rapport de phase P3 — RAG sémantique multi-espaces O93_0

**Identifiant :** O930-P3-RAPPORT-001  
**État :** `COMPLETE_LOCAL_TESTED_BOUNDED`  
**Date d’enregistrement :** 2026-10-13  
**Périmètre :** code source O93_0 dans cette version, tests locaux et corpus synthétique de contrôle. Ce statut ne vaut pas acceptation globale du modèle, validation sémantique universelle, ni validation des interfaces externes.

## 1. Description

La phase construit un RAG fondé sur l’observation multi-sondes et des espaces sémantiques dérivés des morceaux observés. Chaque transformation produit un espace distinct contenant provenance, contextes de token, rôles itoken/vtoken, proximité/distance et poids. Un agrégat final est consultable par un lecteur multi-sondes qui utilise ces poids et restitue les sources. La recherche lexicale héritée demeure accessible comme voie distincte explicitement choisie.

La sélection facultative du nombre d’espaces évalue des préfixes après construction des représentations, avec des requêtes de validation et des hashes de sources pertinentes. Les étiquettes de validation ne sont pas injectées lors de la construction des vecteurs. La sélection respecte `min_spaces`; le jeu final d’évaluation doit être tenu à l’écart de celui de sélection.

## 2. Architecture

`O93Observer` et le stockage des morceaux observés avec SHA-256 → `aam_o93/semantic_rag.py::SemanticRAG.rebuild` → vues de sondes et espaces candidats → vecteurs contextuels et rôles itoken/vtoken → distances mesurées → agrégation des poids → lecteur `SemanticRAG.search` → résultats sourcés et journal d’opération. `aam_o93/runtime.py` branche l’ingestion au RAG sémantique par défaut dans la politique observation-first. Le CLI expose reconstruction, listing, inspection, suppression, nettoyage, évaluation et recherche.

Les transformations P3 du portefeuille actuel sont `sequence_context`, `mirror_order`, `lexical_order`, `parity_mirror`, `frequency_context` et `cyclic_mirror`. Ce sont des vues de travail testées, pas une preuve d’exhaustivité de toutes les modalités.

## 3. Pipeline complet

1. Valider le préflight, les documents normatifs, les checklists et les deux registres d’erreurs.
2. Charger les morceaux observés, vérifier leur contenu et leur provenance, et préserver les hashes de source.
3. Appliquer séparément les transformations de sondes et calculer les contextes de token par espace.
4. Classer les tokens selon leur stabilité relative en itoken/vtoken et mesurer la proximité ; pour les vecteurs valides, `d = 1 - s`.
5. Calculer les contributions de poids par espace puis agréger les espaces dans un index final versionné.
6. Évaluer le gain marginal, les changements de rôles et de poids et le statut d’arrêt ; une stabilité heuristique ne vaut pas preuve de généralisation.
7. Si le jeu de sélection est fourni, évaluer les préfixes après construction sur `MRR` puis `Hit@k` avec un départage par coût / nombre d’espaces et respecter le plancher configuré.
8. Écrire le final de façon transactionnelle avec traçabilité et sauvegarde de génération précédente.
9. Faire passer les requêtes par les vues de contexte, le lecteur pondéré, la citation des sources et les ablations disponibles.
10. Inspecter, supprimer ou nettoyer les espaces intermédiaires par actions explicites ; le reçu de nettoyage reste conservé et l’espace final reste interrogeable.

## 4. Commandes d’exécution

Les commandes reproductibles principales sont :

```bash
python -m unittest discover -s tests -p 'test_p3_semantic_rag.py' -v
python -m unittest discover -s tests -p 'test_p5_knowledge.py' -v
python -m unittest discover -s tests -p 'test_p7_integrated.py' -v
python -m unittest discover -s tests -v
python -m aam_o93 rag-rebuild --selection-cases validation.jsonl --selection-top-k 5
python -m aam_o93 rag-spaces
python -m aam_o93 semantic-search "sample query"
python -m aam_o93 rag-evaluate test-final.jsonl --ablation
```

Le smoke CLI final a été réalisé avec un workspace temporaire créé pour cette expérience ; il n’a pas remplacé les corpus de production ou les sources d’origine. Les détails des résultats sont dans `logs/O930_P3_min_space_cli_smoke.txt`. La suite complète est archivée dans `logs/O930_P3_post_selection_full_regression.txt`.

## 5. Environnement, jeux et identité des sources

- Archive source d’origine : `sources_AAM_17.zip` ; SHA-256 `add72728952cd4ec83b6994a02d28022339fbbed29835d40c01b8f26bca60c38`.
- Test : `tests/test_p3_semantic_rag.py` ; jeux de contrôle réduits et synthétiques ; aucune métrique de test final industriel n’est revendiquée.
- Les journaux de compilation et de rendu sont conservés sous `logs/O930_P3_*` ; PDF de formalise : 16 pages ; PDF du laboratoire : 13 pages ; 29 pages rendues et inspectées visuellement.
- Préflight P3 : `logs/O930_P3_preflight_close_visual_report.json` (les hashes de docs sont ceux de la version préflightée avant enregistrement final du rapport).

## 6. Résultats bruts

| Mesure | Résultat consigné | Référence |
|---|---:|---|
| Tests ciblés RAG sémantique | 12/12 réussis | `logs/O930_P3_min_space_targeted.txt` |
| Tests ciblés connaissance + intégration avec RAG | 24/24 réussis au total (12 + 6 + 6) | `logs/O930_P3_validation_selection_targeted.txt` |
| Régression locale complète après le correctif `min_spaces` | 130/130 réussis, 0 échec | `logs/O930_P3_post_selection_full_regression.txt` |
| Smoke CLI : espaces sélectionnés | 3 (`min_spaces=3`) | `logs/O930_P3_min_space_cli_smoke.txt` |
| Smoke CLI : catalogue | 7 entrées (6 espaces candidats et l’agrégat final) | idem |
| Smoke CLI : résultats de recherche | 2 | idem |
| Compilations LaTeX | 2 passes par document | `logs/O930_P3_formalism_final_pass1.txt`, `logs/O930_P3_formalism_final_pass2.txt`, `logs/O930_P3_laboratory_final_pass1.txt`, `logs/O930_P3_laboratory_final_pass2.txt` |
| Inspection visuelle | Pages représentatives vues, aucune coupure/débordement visible | `evidence/final_render_formalisme/`, `evidence/final_render_laboratoire/` |

Le test d’ablation et de provenance est couvert par `test_retrieval_evaluation_is_postbuild_and_reports_metrics`, ainsi que par `SemanticRAG.evaluate_ablation` et les tests d’inspection/suppression/cleanup. Les résultats chiffrés de pertinence sur un corpus réel indépendant restent `NOT_RUN`.

## 7. Interprétation des résultats

Les résultats montrent que les contrats locaux testés du pipeline multi-espace fonctionnent dans les cas contrôlés : provenance, espaces distincts, rôles, distances, poids, recherche citée, sélection de préfixe tenue à l’écart, reconstruction, inspection, nettoyage et conservation du final. L’ancienne recherche lexicale n’est pas supprimée ; elle est séparée du parcours sémantique par défaut.

Le premier smoke CLI a révélé un défaut réel : le sélecteur pouvait choisir un seul espace malgré un minimum configuré à trois. Le défaut a été enregistré comme `O930-RAG-012`, corrigé, puis testé ; le smoke final sélectionne trois espaces. La trace du nettoyage, qui n’était initialement conservée qu’en mémoire, a aussi été corrigée sous `O930-RAG-011`.

Les tests et résultats synthétiques ne permettent pas d’inférer une qualité universelle, une reproduction parfaite dans tout domaine, ni une généralisation sur de grands corpus. Une évaluation finale indépendante, avec un jeu séparé du jeu de sélection, demeure nécessaire.

## 8. Conséquences : théoriques, conceptuelles, opérationnelles

- **Théoriques :** les statuts itoken/vtoken et les poids sont empiriques, dépendants du corpus, des sondes et de la politique de calcul ; ils ne sont pas des invariants universels préinjectés.
- **Conceptuelles :** le final est une représentation consultable et reconstruisible de l’observation du corpus. Il n’est ni une preuve de vérité des passages, ni à lui seul une compétence de recherche ou de réponse.
- **Opérationnelles :** les hashes de source, les journaux, sauvegardes, reçus de nettoyage, tests d’ablation et paramètres de sélection rendent les versions auditées. La sélection doit être suivie d’un test indépendant ; les états non testés restent explicites.

## 9. Erreurs, limites et résolution

- `O930-RAG-011` — reçu de nettoyage non persisté au départ : corrigé, retest ciblé réussi.
- `O930-RAG-012` — plancher `min_spaces` ignoré au départ : corrigé, 12/12 tests RAG et smoke CLI réussi.
- `O930-TEX-001` — caractère UTF-8 dans un listing LaTeX : la chaîne d’exemple a été remplacée par une chaîne ASCII ; recompilations réussies.
- `O930-ENC-001` — lecteur de logs présumant UTF-8 : audit refait sur les octets bruts ; aucune compilation n’avait échoué dans cette étape.
- `O930-AUDIT-002` — un script d’inspection supposait que `registre_prouves.json["phases"]` était une liste alors que c’est un dictionnaire : lecteur corrigé, nouvelle lecture réussie. C’est une erreur d’outil d’audit, pas un échec du modèle.
- Limites restantes : corpus de mesure synthétique et étroit ; test de généralisation indépendant à grande échelle `NOT_RUN`; l’interface complète relève de P6; compétences et orchestration complète relèvent de P4/P8; Internet réel, capteurs physiques et Windows natif restent soumis aux gates d’environnement P10.

## 10. Conclusion

P3 est clos uniquement pour la portée locale définie par les critères et les tests archivés. Le système fournit désormais un RAG sémantique multi-espaces avec poids et lecture pondérée, ainsi qu’un cycle d’inspection et de reconstruction éprouvé localement. La phase suivante autorisée est P4, qui devra valider l’acquisition, la composition et le routage des compétences sans présumer de leurs résultats.

## 11. Statut du modèle

**Statut P3 : `COMPLETE_LOCAL_TESTED_BOUNDED`.**  
**Statut global O93_0 : incomplet — P4 en cours ensuite ; P5 à P10 non clos.**  
Aucune réussite future n’est prédite, aucun échec futur n’est programmé et aucune généralisation non mesurée n’est revendiquée.
