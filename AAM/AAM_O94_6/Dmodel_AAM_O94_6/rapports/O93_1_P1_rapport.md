# Rapport P1 O93_1 — intégration réelle du chat RAG et du modèle de langue

## Description
Le défaut de O93_0 faisait terminer une requête de chat sur une enveloppe de preuves RAG sans invoquer le modèle compact entraîné. O93_1 lie les passages sémantiques et les métadonnées de provenance à la génération sélectionnée.

## Architecture
Observation de la requête → recherche sémantique O93 → passages cités et bornés → prompt/context hashés et traités comme données non fiables → capsule locale entraînée ou backend explicitement configuré → résultat non vérifié avec provenance → journal causal. En l’absence de générateur valide, fallback extractif de passages complets.

## Pipeline complet
1. Charger le corpus dans un workspace temporaire isolé. 2. Construire l’espace RAG sémantique. 3. Entraîner une capsule réelle. 4. Envoyer une question au mode chat. 5. Capturer le prompt livré au générateur et vérifier qu’il contient la donnée de source. 6. Vérifier route, citation, hashes, statut de génération et événements de journal. 7. Tester fallback sans modèle, sélection manuelle invalide, chat sans index et contrat backend local.

## Commandes d’exécution
```sh
python scripts/o931_preflight.py --label before_p1_chat_pipeline_tests_local_backend
PYTHONPATH=. pytest -q tests/test_o931_chat_pipeline.py
```

## Résultats
PASS : 6 tests, 0 échec. Reçu : `logs/O931/p1_chat_pipeline_tests_local_backend.stdout.txt`. La suite vérifie l’appel réel de la capsule entraînée et l’injection des passages sémantiques. Le backend configuré a été exercé avec un faux endpoint contrôlé, sans accès réseau réel.

## Interprétation
Le défaut de branchement est corrigé et le chat sait appeler une capsule enregistrée avec le contexte retourné par le RAG. La réponse du petit modèle reste non vérifiée. Le passage du texte dans le prompt ne garantit pas une compréhension sémantique, et les citations prouvent la provenance du contexte, pas l’exactitude de la réponse.

## Conséquences théoriques, conceptuelles et opérationnelles
Théorique : séparation entre retrieval, génération et validation. Conceptuelle : RAG et modèle ne sont plus deux voies mutuellement exclusives. Opérationnelle : l’interface peut afficher modèle, statut, hashes et sources; la sélection invalide échoue explicitement; le fallback ne prétend pas générer.

## Erreurs et limites
Les erreurs de test initiales sont conservées. L’identifiant d’entraînement est `run_id`, tandis que le catalogue l’expose comme `skill_id`; les tests utilisent le contrat effectivement fourni. Un service LLM local utilisateur n’a pas été contacté. Le smoke graphique complet, la suite de non-régression et le packaging restent dans P2–P4.

## Conclusion et statut du modèle
P1 = `COMPLETE_LOCAL_TESTED_BOUNDED`. P2 est autorisée. Cela ne constitue ni une preuve d’exactitude universelle ni une prédiction de succès ou d’échec futur.

## Preuves et critère restant
Voir `tests/test_o931_chat_pipeline.py`, `logs/O931/p1_chat_pipeline_tests_local_backend.stdout.txt`, les entrées `O931-CHAT-RAG-001` et `O931-P1-*` dans les checklists d’erreurs, ainsi que `checklist_de_travail_O93_1.json`.
