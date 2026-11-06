# ORDER80.2.2 — moteur généraliste hiérarchique corrigé

Cette release est la correction d’ORDER80.2.1 après benchmark RAG. Elle rétablit la logique de contrôle hiérarchique au niveau de l’entrypoint général et sépare explicitement une **synthèse documentaire vérifiée** d’une **solution du problème**.

## Cycle

```text
problème
→ observer
→ résoudre
→ échec
→ observer davantage
→ résoudre
→ …
→ décomposer
→ sous-problèmes
→ chaque sous-problème : observer → résoudre → observer davantage → décomposer encore
→ nouveauté vérifiée
→ mémoire
→ news/
→ retest racine
→ peer-probes
→ poursuivre
```

Le cycle est enregistré dans `events.jsonl` et `subproblem_tree.json`. Une nouvelle tentative ne constitue pas un progrès si l’état documentaire est identique.

## Sens des statuts

Le moteur ne considère plus une réponse provenant de plusieurs sources comme une « solution » universellement vérifiée. Une `DOCUMENTED_INSIGHT` peut être mémorisée et placée dans `news/`, mais la résolution complète d’un problème exige un vérificateur de domaine explicite. Sans celui-ci, la fin de run est `NO_DOMAIN_VERIFIED_COMPLETE_SOLUTION_IN_THIS_EXECUTION`.

## Installation

Python 3.10+ et bibliothèque standard uniquement.

```bash
unzip model_order_8_0_2_2.zip -d model_order_8_0_2_2
cd model_order_8_0_2_2/model
python3 -m pytest -q
python3 self_test_order8022.py
```

## Lancement

```bash
python3 run_order_8_0_2_2.py --task task.json --references references.json --output run --duration 1h
python3 run_order_8_0_2_2.py --task task.json --references references.json --output run --duration 24h
```

`--no-web` coupe le réseau. Les références locales sont limitées au manifeste. Le RAG dynamique accepte les nouveaux documents dans `run/rag_inbox/documents/` et `run/rag_inbox/formal/`. Quand aucun nouveau contenu n’est disponible, `run/rag_inbox/requests/CURRENT_REQUEST.json` est écrit.

## Nouveautés

Les connaissances documentaires nouvellement vérifiées comme couvrant le contrat sont mémorisées comme `DOCUMENTED_INSIGHT`. Elles ne sont jamais promues automatiquement en axiome ou en certificat mathématique. Un vrai certificat doit passer le vérificateur correspondant au domaine.

## Sécurité

Les règles web de la branche 8.0.2.1 sont conservées : HTTPS par défaut, allowlist des domaines, validation DNS/public IP, ports autorisés, redirections contrôlées, taille/type bornés, contenu non exécuté, hashes optionnels et journalisation.

## Audit

Chaque run produit `events.jsonl`, `observation_ledger.json`, `memory.json`, `subproblem_tree.json`, `checkpoint.json`, `news/` et `rag_inbox/`.
