# Noyau de vérification ORDER80.2

## Principe

Le moteur de recherche peut produire des arbres candidats ; le noyau est séparé et décide uniquement si cet arbre respecte les règles du calcul implémenté.

## Validation récursive

La vérification descend jusqu'aux feuilles et retourne un compteur d'hypothèses ouvertes.

Exemple :

```text
⊢ A → A
│
├── assume A
└── exact A
```

La feuille `assume A` ouvre une hypothèse `A`. `imp_intro` décharge exactement une occurrence de cette hypothèse.

Pour `or_elim`, chaque branche est exécutée sous son hypothèse puis cette hypothèse est déchargée par la règle.

## Lemmatisation

`apply_lemma` n'est pas une instruction « faire confiance à ce nom ». Le certificat associé au nom est passé de nouveau au noyau avant son utilisation.

Une dépendance cyclique est rejetée.

## Résultat de la vérification

Le rapport contient :

- `proof_fingerprint` ;
- nombre total de nœuds ;
- nombre de nœuds vérifiés ;
- dépendances ;
- hypothèses ouvertes ;
- trace de chaque obligation locale.

Cela donne un objet auditable différent d'une simple réponse booléenne.


## ORDER80.2 verified-lemma reuse

Added the kernel/synthesizer rule `reuse_lemma`. It can only reuse an already observed and independently re-verified complete certificate whose statement is exactly the current goal. It introduces no new mathematical premise.
