# Algorithme bout en bout ORDER80.2.0

## A. Initialisation

1. Charger la cible.
2. Charger la mémoire persistante et ses certificats en attente.
3. Indexer le formel, la documentation locale, les bibliothèques et le dossier RAG dynamique.
4. Initialiser le navigateur web, le planificateur de requêtes et le budget de temps.
5. Faire un bootstrap limité.

## B. Recherche d'un nœud

Pour un séquent `Γ ⊢ G`:

```text
synthétiser
→ si preuve: vérifier
→ sinon profiler l'échec
→ observation supplémentaire
→ recommencer
```

Quand l'observation disponible du nœud n'ajoute plus d'unité immédiatement exploitable, le moteur décompose le nœud. Chaque enfant possède son propre compteur d'observation.

## C. Propagation

Après chaque preuve locale vérifiée:

```text
preuve locale
→ fermeture du séquent
→ vérification indépendante
→ mémoire
→ archive news/
→ retest racine
→ peer-probe
```

## D. Cycle global persistant

Quand aucun certificat racine n'est encore vérifié:

```text
nouvelle donnée formelle/mémoire ?
  oui → nouveau cycle de synthèse
  non → nouvelle observation / nouvelle requête web / polling RAG
```

Un cycle de synthèse identique n'est pas exécuté simplement parce que le délai a augmenté.

## E. Déduplication

Une unité déjà observée est identifiée par un identifiant stable ou un hash de contenu.

Pour le web, URL, page, chunk et requête sont suivis séparément. Une nouvelle requête n'est considérée productive que si elle permet d'obtenir une page/chunk non déjà vu.

## F. Checkpoint

Le moteur conserve périodiquement:

- mémoire persistante;
- signatures de connaissance;
- compteur de cycles;
- état du web;
- arbre de sous-problèmes;
- observation ledger;
- demandes RAG;
- événements JSONL.

Un arrêt utilisateur produit un état récupérable et n'est pas confondu avec une impossibilité de résolution.
