# Rapport de phase P5 — Autonomie, mémoires et causalité

**Version :** AAM O93_0, statut `COMPLETE_LOCAL_TESTED_BOUNDED` après validation des cinq gates locales et contrôle documentaire final.  
**Date de vérification :** 2026-10-13.  
**Portée :** exécution locale sous environnement Linux de travail, espaces temporaires pour tests ; pas d’acceptation physique/externe.

## 1. Description

La phase P5 relie l’autonomie persistante, la priorité de la demande utilisateur, les mémoires, les relations causales, la récompense/punition, le focus et l’adaptation temporaire des poids sémantiques. L’autonomie démarre à l’initialisation normale de l’interface ; l’arrêt est explicite. À l’arrivée d’une requête, le runtime ferme la frontière de cycle autonome avant le travail utilisateur, puis reprend la boucle après l’achèvement/échec tracé de la tâche.

## 2. Architecture

- `aam_o93/autonomy.py` : cadence, pause à frontière durable, verrou de cycle, focus et événement causal d’action.
- `aam_o93/runtime.py` : arbitrage de requête, orchestration d’actions autonomes, inventaire complet des mémoires, sélection du focus, causalité des résultats et feedback.
- `aam_o93/memory.py` : journal d’audit chaîné et mémoire de raisonnement séparée ; désactiver le détail de raisonnement ne désactive pas l’audit minimal.
- `aam_o93/observer.py` : observation des valeurs/fichiers à la même interface d’observation que les sources externes.
- `aam_o93/semantic_rag.py` : ajustement temporaire du poids des tokens pour une recherche, sans altérer l’espace final persistant.
- `tests/test_p5_autonomy_o930.py`, `tests/test_p6_autonomy.py`, `tests/test_p5_knowledge.py`, `tests/test_p3_semantic_rag.py` : tests ciblés.

## 3. Pipeline complet exécuté

1. L’application construit le runtime, puis demande le démarrage idempotent de l’autonomie.
2. L’autonomie produit une observation d’état et une liste d’actions locales possibles ; les accès réseau/capteurs ne sont pas autorisés par défaut.
3. L’inventaire parcourt toutes les catégories mémoires prévues sans plafond artificiel de 100 fichiers, calcule les hashes et signale les erreurs d’accès.
4. Les contenus nouveaux/modifiés passent dans une file d’observation incrémentale. Les fichiers stables sont observés par `O93Observer`; les journaux JSONL append-only sont traités par nouvelles lignes/événements. Le focus fait passer les catégories choisies devant les autres et permet un lot plus profond.
5. L’arrivée d’une requête met l’autonomie en pause au prochain point de synchronisation. L’événement de priorité relie le hash de requête ; `task.started`, `task.completed` et `task.causal_outcome` relient les hashes parents.
6. Le résultat d’une tâche n’est pas déclaré vrai parce qu’il a été noté positivement. La note influence la priorité de travail ; la relecture d’un trajet satisfait reste `NEEDS_INDEPENDENT_VERIFICATION`.
7. La modulation temporaire RAG n’est possible que si le réglage persistant de l’utilisateur l’autorise. Elle est limitée à la requête ; les hashes de l’espace final avant/après doivent être identiques.
8. Les écritures, les résultats, les erreurs, la file d’observation et les événements de causalité sont conservés dans les artefacts de test.

## 4. Commandes d’exécution

Commande de phase utilisée pour la non-régression ciblée :

```text
python scripts/o930_phase_exec.py P5 targeted_p5_acceptance_after_memory_observer_retest -- python -m unittest tests.test_p6_autonomy tests.test_p5_autonomy_o930 tests.test_p5_knowledge tests.test_p3_semantic_rag -v
```

Commande de phase utilisée pour la régression globale :

```text
python scripts/o930_phase_exec.py P5 full_regression_after_memory_observer -- python -m unittest discover -s tests -v
```

Le lanceur de phase relit les deux documents normatifs, la checklist de phase et les deux checklists d’erreurs avant l’exécution ; il archive commande, sorties, code retour et erreurs.

## 5. Résultats bruts vérifiables

- Acceptation ciblée P5/autonomie/RAG : **34 tests, 34 réussis, 0 échec** — `logs/O930_P5_targeted_p5_acceptance_after_memory_observer_retest_result.json` et les fichiers stdout/stderr associés.
- Régression globale : **154 tests, 154 réussis, 0 échec, 23,153 s** — `logs/O930_P5_full_regression_after_memory_observer_result.json` et les fichiers stdout/stderr associés.
- Le test de mémoire crée **107 fichiers** de contenu, constate que tous sont inventoriés (`truncated=false`), observe par lots jusqu’à `pending=0`, modifie un fichier pour provoquer une nouvelle observation et vérifie que le texte sentinelle n’est pas persisté dans l’index.
- Le test causal vérifie trois parents d’événement pour le résultat de tâche : priorité de requête, démarrage de tâche, achèvement de tâche ; la chaîne d’audit reste vérifiable.
- Le test de pondération temporaire vérifie l’opt-in, refuse le contournement par appel quand l’option est désactivée, refuse un token inconnu et constate que le hash de l’espace final ne change pas.

- Retest causal autonomie/mémoires P5-P6 : **16/16 PASS** — `logs/O930_P5_causal_memory_gate_tests_retest3_result.json`.
- Revue contractuelle des relations causales : **16/16 PASS** — `logs/O930_P5_autonomy_causality_contract_review_final_result.json`.
- Régression complète finale : **154/154 PASS, zéro échec** — `logs/O930_P5_full_regression_after_explicit_causal_gates_result.json`.
- Recompilation documentaire : formalisme **18 pages**, laboratoire **19 pages**, deux passes par document ; les rendus complets et leur inspection sont consignés dans `logs/O930_P5_render_formalisme_after_final_polish_result.json`, `logs/O930_P5_render_laboratoire_closure_status_retest_final_result.json` et `evidence/P5_pdf_visual_review.json`.
- Compilation/rendu de référence antérieur, réussite vérifiée (18 pages formalisme, 19 laboratoire) : `logs/O930_P5_compile_and_render_p5_documents_final_retest_result.json` ; son compte rendu n’est pas substitué aux compilations/rendus finaux listés ci-dessus.
## 6. Interprétation des résultats

Les essais démontrent le comportement logiciel local spécifié pour les scénarios testés : pause/reprise à frontière de cycle, liens causaux vérifiables, priorisation par feedback sans substitution aux preuves, focus persistant et observation incrémentale des mémoires. Les tests sont des preuves de contrat/exécution contrôlée, non la preuve d’une compétence générale parfaite sur tout domaine.

## 7. Conséquences

### Théoriques

La boucle autonome et les observations de mémoire deviennent des événements reliés causalement. L’empreinte d’un contenu observé, sa provenance, son état de décodage et ses empreintes sémantiques restent distincts de l’interprétation métier de son contenu.

### Conceptuelles

La récompense est un signal de préférence et d’ordre de travail, non une vérité injectée. Le focus modifie la cadence et l’ordre d’inspection, non les règles de preuve. L’index des observations mémoires stocke provenance, hashes, statuts et résumé de l’observation ; le contenu brut n’est pas recopié dans cet index.

### Opérationnelles

L’inventaire est complet pour les racines configurées et signale les erreurs ; la file est incrémentale, persistante et reprenable. Les fichiers multimodaux ou binaires dont le décodeur n’est pas disponible restent marqués `PARTIAL`/`NOT_DECODED`, sans faux succès. Les journaux append-only sont traités par nouveaux événements.

## 8. Erreurs, limites et environnements non testés

- Le lancement normal est exercé via un constructeur d’interface Tk simulé ; cette livraison n’est pas une qualification native interactive sous Windows.
- Aucun capteur ou appareil physique n’a été ouvert ; aucun accès Internet n’a été utilisé. Les fournisseurs réseau/capteurs restent soumis à permissions explicites.
- Les tests utilisent des espaces de travail temporaires et des données contrôlées. Ils ne prouvent pas la performance générale, la perfection universelle de reproduction, ni la généralisation à des domaines inédits.
- Les fichiers encodés ou binaires dont le décodeur manque sont explicitement incomplets ; l’observation de structure/empreinte n’est pas une compréhension sémantique garantie.
- Les incidents d’audit/outillage des tentatives précédentes restent dans les journaux ; ils sont résolus uniquement à partir des relances réussies et ne sont pas effacés.

## 9. Conclusion

**P5 est clôturée dans une portée locale testée et bornée, après contrôle des cinq gates, des journaux, des documents compilés et des rendus inspectés. Aucun statut global de complétude n’est revendiqué ; P6 (intégration UI complète) reste non commencée jusqu’à la transition formelle.

## 10. Statut du modèle

`P5 = COMPLETE_LOCAL_TESTED_BOUNDED`; les cinq gates de checklist ont passé dans la portée locale bornée. `implementation_complete_claimed=false`. Les résultats ne préjugent ni de la réussite ni de l’échec futur d’AAM.


## 11. Addendum — réconciliation causale et documentaire (13 octobre 2026)

### Description / architecture / pipeline complet
L’autonomie produit des pulses et observations reliés par des hashes parents. Les demandes utilisateur ont priorité sur les actions internes; la note utilisateur réordonne le diagnostic mais ne remplace pas une vérification indépendante. Les poids sémantiques temporaires restent opt-in et query-scoped. Cette itération a réconcilié les erreurs d’audit historiques et recompilé les documents avant leur rendu complet.

### Commandes exécutées
```text
python scripts/o930_phase_exec.py P5 causal_memory_gate_tests_retest3 -- python -m unittest tests.test_p5_autonomy_o930 tests.test_p6_autonomy -v
python scripts/o930_phase_exec.py P5 autonomy_causality_contract_review_final -- python scripts/o930_p5_contract_review.py
python scripts/o930_phase_exec.py P5 full_regression_after_explicit_causal_gates -- python -m unittest discover -s tests -v
python scripts/o930_phase_exec.py P5 compile_and_render_p5_documents_retest -- python scripts/o930_compile_p5_documents.py
```

### Résultats / interprétation
- Tests ciblés autonomie P5/P6 : **16/16 PASS** — `logs/O930_P5_causal_memory_gate_tests_retest3_result.json`.
- Revue contractuelle structurelle : **16/16 PASS** — `logs/O930_P5_autonomy_causality_contract_review_final_result.json`.
- Régression complète : **154/154 PASS, zéro échec** — `logs/O930_P5_full_regression_after_explicit_causal_gates_result.json`.
- Compilation/rendu des documents : `logs/O930_P5_compile_and_render_p5_documents_retest_result.json` puis `logs/O930_P5_compile_and_render_p5_documents_final_retest_result.json`; le dernier build confirme les hashes et les 18/19 pages : `evidence/o930_p5_document_build.json`. Rendus complets sous `evidence/final_p5_formalisme_O93_0/` et `evidence/final_p5_laboratoire_O93_0/`.
- Les incidents d’outillage conservent leur trace originale; leur résolution est rattachée à un retest identifiable.

### Conséquences / conclusion / statut
Les cinq gates P5 ont été testées localement dans une portée bornée. Cela n’atteste pas la généralisation universelle, l’acceptation interactive native Windows, l’ouverture de matériel physique ou un accès à un fournisseur Internet réel. `implementation_complete_claimed=false`. P5 est clôturée comme COMPLETE_LOCAL_TESTED_BOUNDED après réconciliation checklist-registre-documents, contrôle des hashes, revue visuelle des rendus et vérification des références. La complétude globale reste non revendiquée.
