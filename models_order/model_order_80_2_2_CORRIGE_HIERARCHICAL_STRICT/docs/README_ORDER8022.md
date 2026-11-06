# ORDER80.2.2 — guide complet de bout en bout

## 0. Nature de la correction

ORDER80.2.2 est une release corrective issue d’ORDER80.2.1. Le benchmark RAG a établi que l’entrypoint général actif d’O80.2.1 utilisait seulement `GeneralResearchEngine`: il observait, synthétisait et pouvait appeler une synthèse « solution » sans exécuter la boucle hiérarchique attendue.

O80.2.2 active le contrôleur hiérarchique `HierarchicalGeneralEngine` dans son nouvel entrypoint et corrige la sémantique des statuts.

## 1. Cycle exact

```text
problème
→ observer
→ résoudre
→ échec
→ observer davantage
→ résoudre
→ …
→ observation épuisée
→ décomposer
→ sous-problèmes
→ chaque sous-problème : observer → résoudre → observer davantage → … → décomposer encore
→ nouveauté vérifiée
→ mémoire
→ news/
→ retest racine
→ peer-probes
→ poursuivre
```

Le cycle est contrôlé par état de nœud et par fingerprint. La même connaissance documentaire ne doit pas être traitée comme un nouveau progrès uniquement parce que le moteur est entré dans un nouveau cycle.

## 2. Ce que signifie « résoudre »

Deux niveaux sont strictement séparés :

- `DOCUMENTED_INSIGHT`: une synthèse documentaire possède provenance et couverture suffisantes selon le contrat général. Elle peut être mémorisée comme insight et archivée dans `news/`.
- résolution complète du problème : nécessite un vérificateur de domaine explicite. O80.2.2 ne transforme jamais une source textuelle en preuve universelle par simple corroboration.

## 3. Références

Le manifeste des références sépare les racines locales, les URL de contenu et les moteurs de recherche. Les données sont non exécutables. Les hashes optionnels peuvent pinner des références.

## 4. RAG dynamique

Pendant un run, déposer de nouveaux documents dans `rag_inbox/documents/` ou des artefacts formels dans `rag_inbox/formal/`. Le moteur rescane ces répertoires pour les nœuds suivants. Quand aucune nouvelle unité n’est disponible, il crée `rag_inbox/requests/CURRENT_REQUEST.json`.

## 5. Mémoire et nouveautés

Une nouveauté documentaire vérifiée est fingerprintée, enregistrée dans `memory.json` et copiée dans `news/<revision>_<fingerprint>/`. Les artefacts de preuve restent distincts des observations brutes.

## 6. Lancement

```bash
python3 run_order_8_0_2_2.py --task task.json --references references.json --output run --duration 1h
python3 run_order_8_0_2_2.py --task task.json --references references.json --output run --duration 24h
python3 run_order_8_0_2_2.py --task task.json --references references.json --output run --duration forever
```

`--no-web` désactive le réseau sans modifier le fichier de référence utilisateur.

## 7. Vérification de domaine

Pour une résolution complète, le contrat doit fournir un vérificateur adapté au problème. Cette release refuse par défaut de confondre couverture documentaire et vérité du problème. Pour les domaines formels, la lignée O80 contient déjà un noyau de preuve séparé sous `legacy_order8020/`; son utilisation doit rester explicite.

## 8. Interprétation finale

`TIME_BUDGET_EXPIRED`, `INTERRUPTED` et `UNRESOLVED` décrivent le run. Ils ne constituent aucune conclusion universelle sur la possibilité ou l’impossibilité du problème étudié.
