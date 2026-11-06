# Algorithme bout en bout ORDER80.2

## A. Initialisation

1. Charger la tâche et le séquent racine `∅ ⊢ G`.
2. Construire les index locaux sans activer leurs unités probantes.
3. Initialiser la mémoire persistante ; les entrées héritées restent inactives tant qu'elles ne sont pas revalidées.
4. Préparer les canaux web et bibliothèques selon la configuration.

## B. Boucle complète d'un nœud

Pour chaque nœud `N = (Γ ⊢ G)`, y compris chaque descendant :

```text
bootstrap observation
→ tentative de résolution
→ échec ?
   oui → FailureProfile
       → observation focused
       → tentative
       → si échec → observation expanded
       → tentative
       → si échec → observation broad
       → tentative
       → …
       → aucun nouveau matériau accessible
       → décomposition
non → preuve vérifiée locale
```

Le fait d'entrer en `broad` autorise l'observation de nouvelles unités même si elles ne correspondent pas lexicalement au but. Ce mécanisme évite de définir « observer davantage » comme un simple déplacement vers le fichier suivant.

## C. Sources d'observation

### Formelle

Une source JSON peut exposer plusieurs théorèmes. L'unité d'observation est le théorème, pas le fichier entier.

### Documentaire locale

Un même document est découpé en chunks. Un sous-problème ultérieur peut donc récupérer un autre chunk du même document.

### Web

Le moteur peut consommer des URLs explicitement configurées, des URLs découvertes dans des chunks effectivement observés et des résultats de recherche via des templates configurables.

Une URL présente seulement dans une partie non observée du corpus local n'est pas injectée prématurément dans la file web.

### Bibliothèques

`--library` ajoute des racines locales supplémentaires. Les JSON contenant des certificats suivent le canal formel ; les autres formats restent documentaires tant qu'aucun adaptateur formel ne les transforme en certificat vérifiable.

## D. Décomposition récursive

Si la résolution du nœud échoue après épuisement des sources accessibles pour ce nœud, `decompose()` produit zéro ou plusieurs enfants.

Chaque enfant est un nœud complet :

```text
observer
→ résoudre
→ observer davantage
→ …
→ décomposer
```

Il n'existe donc pas de niveau où l'observation est définitivement arrêtée.

## E. Succès local et propagation

Après une preuve `Γ ⊢ H` vérifiée :

1. fermer le séquent en `(∧Γ) → H` ;
2. vérifier de nouveau la preuve fermée ;
3. enregistrer le certificat et sa provenance dans la mémoire ;
4. tester immédiatement la racine ;
5. si la racine n'est pas résolue, tester immédiatement les nœuds en attente avec le nouvel état de connaissance ;
6. poursuivre l'arbre.

Ainsi, un résultat local ne reste pas isolé dans son sous-arbre.

## F. Terminaison

Une exécution s'arrête lorsque la racine possède une preuve vérifiée, que l'espace accessible est épuisé, ou qu'une ressource d'exécution explicitement demandée interrompt la recherche.

Aucune de ces conditions n'est convertie en affirmation mathématique d'impossibilité, de falsité ou de possibilité hors du certificat effectivement produit.
