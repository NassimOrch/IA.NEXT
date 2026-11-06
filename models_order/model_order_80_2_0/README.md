# ORDER80.2.0 — Persistent Long-Running Adaptive Observation

Version : **8.0.2.0**  
Base : **ORDER80.2**

ORDER80.2.0 conserve le noyau de preuve ORDER80.2 et ajoute un contrôleur de recherche persistant destiné aux exécutions de longue durée.

## Schéma

```text
problème
→ observer
→ résoudre
→ échec
→ observer davantage
→ résoudre
→ …
→ décomposer
→ sous-problème
   → observer
   → résoudre
   → échec
   → observer davantage
   → …
   → décomposer à nouveau
→ preuve locale vérifiée
→ mise à jour mémoire
→ archive news/
→ retest problème complet
→ sondage des autres sous-problèmes
→ continuer
```

Quand aucun certificat complet n'est encore obtenu, le contrôleur recommence un cycle de découverte globale. Il ne relance pas le même état de synthèse sans changement du savoir formel ou de la mémoire.

## Durée

```bash
python3 run_order_8_0_2_0.py --duration 1h
python3 run_order_8_0_2_0.py --duration 24h
python3 run_order_8_0_2_0.py --duration 1week
python3 run_order_8_0_2_0.py --duration forever
```

Des formes comme `1h30m` sont aussi acceptées.

`forever` signifie que le contrôleur continue jusqu'à preuve complète ou interruption externe. Avec un budget borné, le statut de fin est `TIME_BUDGET_EXPIRED` si aucune preuve complète n'a été vérifiée.

## Observation réellement extensible

Le moteur combine :

- formel, théorème par théorème ;
- documentation/RAG, chunk par chunk ;
- bibliothèques locales ;
- web, par références, liens découverts et recherche ;
- dossier RAG dynamique surveillé pendant l'exécution.

Le web utilise un historique des URL, pages, chunks et requêtes. Les requêtes sont générées par vagues adaptatives pour éviter la répétition exacte.

## RAG dynamique

Le modèle crée :

```text
<output>/rag_requests/CURRENT_REQUEST.json
```

lorsqu'il n'obtient plus de nouvelles unités depuis les sources actuelles. Les nouvelles données peuvent être ajoutées pendant l'exécution ici :

```text
<output>/rag_inbox/documents/
<output>/rag_inbox/formal/
```

Les nouveaux fichiers sont indexés lors des tours suivants. Le moteur ne compte comme nouveau que du contenu réellement nouveau.

## Mémoire et nouveautés

Chaque démonstration nouvellement vérifiée par le noyau est admise dans la mémoire persistante. Une copie complète de la démonstration réellement produite par le modèle est archivée dans :

```text
<output>/news/<sequence>_<proof_fingerprint>/demonstration.txt
```

avec son certificat et ses métadonnées.

Aucune démonstration n'est ajoutée à `news/` avant la vérification indépendante du noyau.

## Web et bibliothèques : séparation stricte

Le web et les documents textuels sont de l'observation, pas des axiomes. Ils peuvent orienter la recherche et permettre de découvrir des sources ou des certificats formels; un certificat n'est utilisable qu'après passage par le noyau.

Les formats de preuve non compris par le noyau restent documentaires. Le moteur ne transforme pas automatiquement une affirmation web en vérité logique.

## Exécution Riemann

La cible par défaut est le fichier :

```text
data/tasks/RIEMANN_HYPOTHESIS_STRUCTURED.json
```

Le code exécutable ne contient aucune démonstration spécifique de la conjecture de Riemann et aucune conclusion injectée à l'avance.

## Fichiers principaux

- `run_order_8_0_2_0.py` — point d'entrée longue durée ;
- `src/order80/engine_longrun.py` — contrôleur persistant ;
- `src/order80/budget.py` — budgets temporels ;
- `src/order80/search_planner.py` — diversification web ;
- `src/order80/web_observe.py` — observation réseau ;
- `src/order80/observe.py` — observation formelle dynamique ;
- `src/order80/research.py` — RAG documentaire dynamique ;
- `src/order80/memory.py` — mémoire des certificats vérifiés ;
- `src/order80/synthesize.py` — synthèse des preuves ;
- `src/order80/proof.py` — noyau de vérification ;
- `self_test_order8020.py` — auto-test spécifique O80.2.0.

Les documents historiques ORDER78/ORDER79/ORDER80/ORDER80.2 sont conservés pour la traçabilité.
