# AAM O93_1 — note de version et de livraison

## Description / architecture

O93_1 / runtime 0.93.1 réunit l’observation, les sondes, le RAG observation-first, les compétences composables, la mémoire causale et l’autonomie persistante. Le chat récupère des preuves RAG, transmet les passages au modèle de langue sélectionné et conserve la provenance (capsule, prompt, contexte, citations). Une candidate non exploitable est journalisée puis rejetée au profit d’un extrait source cité ; le message affiché ne doit pas être confondu avec le texte brut du générateur.

L’entraînement du générateur de chat est distinct de l’acquisition d’une compétence de tâche. Il est disponible via API Runtime, la CLI `train-language-model` et un panneau dédié dans l’onglet Entraînement. L’autonomie démarre par défaut et son arrêt manuel reste distinct de la fermeture de l’application.

## Pipeline de livraison

Lecture des formalismes et checklists O93_0/O93_1 → préflight → tests de régression → registre de preuves → manifestes SHA-256 → ZIP → extraction propre → self-check, smoke CLI, tests de runtime/UI et validation des documents. Les échecs initiaux et les essais interrompus sont conservés dans les registres.

## Résultats / interprétation

Les candidats Dmodel et Amodel passent chacun la matrice ciblée depuis une extraction propre : 49 tests en 12,58 s et 49 tests en 10,88 s respectivement. Le paquet de suivi passe son contrôle de manifeste, son analyse de cohérence de 6 JSON et la compilation TeX des deux sources O93_1. Les archives finales ont été reconstruites depuis le même état et leurs tests exacts sont enregistrés dans le manifeste de livraison détaché.

Sur 120 SMS réels, une ligne cible exclue de l’entraînement est retrouvée via RAG et incluse dans le prompt d’une capsule réellement appelée. Sa candidate contenant `<unk>` a été rejetée ; l’utilisateur a reçu un passage RAG cité. Le corpus complet de 5 574 SMS est `NOT_VALIDATED` après timeout d’ingestion, sans conclusion sur le potentiel général du modèle.

## Conséquences et statut

Théorique : séparation de la preuve d’invocation et de la qualité sémantique de la réponse. Conceptuelle : entraînement de compétence et entraînement du générateur de chat sont deux flux distincts. Opérationnelle : l’utilisateur vérifie les citations et détails techniques. P1–P4 sont clôturées dans le périmètre local borné; l’acceptation externe OS natif/ACL/capteurs/endpoints réels n’est pas incluse. `implementation_complete_claimed=false`.
