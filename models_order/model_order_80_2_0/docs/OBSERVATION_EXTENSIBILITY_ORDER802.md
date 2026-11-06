# Observation extensible ORDER80.2

## 1. Pourquoi le changement

Une observation « document entier » rendait `observe_more` peu informative sur les petits corpus : après quelques fichiers, demander une observation supplémentaire pouvait simplement constater que la source était déjà consommée.

ORDER80.2 change l'unité d'observation et ajoute une progression de couverture :

- formel = théorème ;
- documentaire = chunk ;
- web = page puis chunk ;
- bibliothèque = unités indexées selon leur type.

## 2. Progression d'un nœud

Chaque échec peut faire monter le niveau d'observation du nœud :

```text
bootstrap → focused → expanded → broad → broad → ...
```

`focused` utilise le but, le contexte et le profil d'échec. `expanded` ajoute un voisinage structurel/lexical. `broad` peut récupérer une unité encore inconnue même sans correspondance directe.

Ainsi, « observer davantage » est une véritable opération d'élargissement et non une simple répétition.

## 3. RAG local

Le rang local est actuellement lexical et déterministe. Les tokens du but, du contexte et du `FailureProfile` servent à classer les unités non encore observées.

Le formel est activé théorème par théorème. Le documentaire est activé chunk par chunk. Un autre sous-problème peut donc observer une autre partie d'un même document.

## 4. Web autonome

`WebObserver` possède :

- URLs de référence explicites ;
- URLs découvertes **uniquement dans des chunks déjà observés** ;
- recherche via des templates configurables ;
- liste de domaines autorisés ;
- suivi de liens ;
- hachage des pages/chunks ;
- journal des réussites et erreurs réseau.

Une URL présente uniquement dans une portion encore non observée du corpus local n'est pas injectée en avance dans la file web.

Le web reste documentaire : une page n'est jamais traitée comme axiome simplement parce qu'elle a été téléchargée.

## 5. Bibliothèques

`--library` et `library_paths` ajoutent des racines locales. Un JSON contenant des certificats sous `theorems` peut alimenter le canal formel ; les formats Lean/Coq/Isabelle/etc. restent documentaires tant qu'un adaptateur/certificat compatible n'existe pas.

Plusieurs bibliothèques peuvent être ajoutées et leurs fichiers sont hachés/audités par les observateurs concernés.

## 6. Séparation index / observation

L'indexation permet au moteur de savoir ce qui existe sans promouvoir immédiatement le contenu. L'observation est l'étape qui rend une unité utilisable par le RAG correspondant.

Les URLs web suivent la même règle : référence explicite ou découverte après observation effective du contenu local.
