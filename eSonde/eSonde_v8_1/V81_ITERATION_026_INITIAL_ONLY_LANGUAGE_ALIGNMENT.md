# Rapport V81-ITER-026 — politique initial_only, intention d’explication et alignement linguistique

## 1. Description

Cette itération traite trois défauts mesurés dans les générations libres : (i) le profil historique `context_response` améliore parfois l’ouverture mais injecte des associations hors sujet lorsqu’il agit à chaque token ; (ii) sa désactivation totale dégrade l’ouverture ; (iii) une génération routée en anglais a terminé par `que es el`, alors que ces tokens sont beaucoup plus caractéristiques de l’espagnol dans les statistiques TRAIN.

La sortie complète de l’ablation `OFF` reste : `The. algae h2o, que es el`. Elle a été générée sur 1 000 000 Obsiss, 8 tokens, non-réponse désactivée. Elle montre que la suppression intégrale du profil historique n’est pas un réglage par défaut satisfaisant.

## 2. Architecture / décisions de conception

### 2.1 Politique héritée `always | initial_only | off`

Le canal historique `context_response` possède maintenant trois politiques explicites. `always` préserve le comportement hérité ; `off` est une ablation ; `initial_only` autorise ce canal au choix du premier token, puis supprime uniquement ses associations lorsque le préfixe généré n’est plus vide. Les transitions OASST1, les associations sémantiques prompt→réponse récentes et les 16 observations Obsiss demeurent actives.

### 2.2 Intention d’explication

Le classifieur de surface distingue désormais une demande d’explication (`explanation_request`) à partir de verbes d’instruction observables dans plusieurs langues. Pour le premier token, un terme thématique présent dans le prompt peut recevoir une faible observation `response_role`; il ne s’agit ni d’une phrase de réponse ni d’un contenu imposé.

### 2.3 Alignement linguistique statistique

Une fonction calcule, à partir des fréquences TRAIN normalisées par taille de langue et avec lissage additif, le rapport entre le taux d’un token dans la langue sélectionnée et son taux maximal dans les autres langues. Un token n’est pénalisé que lorsque le taux étranger dépasse le taux sélectionné d’au moins un facteur 10 ; la pénalité logarithmique est plafonnée à 3. Elle est intégrée à l’observation existante `local_transition` et aux scores de propositions de départ/continuation. Aucun nouveau canal Obsiss ni liste noire lexicale n’est ajouté.

## 3. Pipeline complet

1. Charger le prompt et router la langue à partir des statistiques OASST1 TRAIN.
2. Construire le profil historique de dialogue sans stocker de conversation brute.
3. Choisir la politique `always`, `initial_only` ou `off` pour `context_response`.
4. À chaque étape, calculer les transitions conditionnées par prompt+préfixe, les associations sémantiques et les propositions.
5. Appliquer l’ajustement linguistique normalisé aux scores existants.
6. Construire les 16 observations nommées, sans fusionner leur espace avec les coordonnées CountSketch.
7. Évaluer les candidats par le vote Obsiss/P-R sur la population complète.
8. Appliquer la pénalité de répétition avant le tri du faisceau et enregistrer les preuves par token.

## 4. Commandes d’exécution

Compilation et tests :

```bash
cd Dmodel_eSonde_v8_1
python -m compileall -q src tests
PYTHONPATH=src pytest -q --disable-warnings --maxfail=1
```

Chat, politique initiale uniquement :

```bash
python -m esonde_v8.cli_v81 chat \
  --prompt "Explain photosynthesis simply." \
  --legacy-context-association-initial-only \
  --max-tokens 12 --beam-width 6 --candidate-limit 48 \
  --p-activation-mode first_state --json-out runs_v8_1/initial_only_photo.json
```

Le CLI conserve le contrôle du snapshot pré-exécution et l’option de non-réponse reste désactivée par défaut.

## 5. Résultats

- Compilation Python : réussie.
- Batterie complète : **129 tests réussis**, 27,03 s.
- Nouveaux tests : politique `initial_only` appliquée seulement après le premier token ; détection de demande d’explication ; terme du prompt comme observation d’ouverture ; pénalité linguistique dérivée des fréquences normalisées.
- Aucune génération n’a encore été exécutée avec cette nouvelle itération. Aucun résultat de cohérence n’est donc revendiqué pour cette politique.
- Checkpoint original inchangé ; aucune composante neuronale n’est importée.

## 6. Interprétation

L’ablation `OFF` précédente a prouvé que le profil historique est à la fois utile à l’ouverture et nuisible lorsqu’il contribue aux continuations. `initial_only` teste une séparation temporelle de ce rôle. L’alignement linguistique répond à un défaut concret de commutation anglais→espagnol observé dans l’ablation précédente. La reconnaissance d’une demande d’explication est limitée à l’acte de langage de surface ; elle ne fournit aucune réponse cible.

## 7. Conséquences

- **Théorique :** distinction entre signal d’ouverture, association thématique de tour et transition lexicale ; le modèle ne doit pas confondre ces rôles.
- **Conceptuelle :** le langage du dialogue est un contexte actif à maintenir, et non une simple contrainte de vocabulaire au premier token.
- **Opérationnelle :** le CLI permet une ablation reproductible ; le score linguistique utilise un rapport TRAIN normalisé et se fond dans `local_transition`.

## 8. Conclusion

Cette itération corrige des mécanismes précis et passe 129 tests. Elle n’est pas encore validée par génération libre. Le prochain essai obligatoire est une comparaison full/initial_only sur photosynthèse et une salutation, avec un million d’Obsiss et non-réponse désactivée, puis une évaluation tenue à l’écart du TRAIN. La cohérence finale et la généralisation restent non démontrées.

## 9. Statut du modèle

**eSonde v8.1 : prototype en développement ; code compilable, tests logiciels PASS, génération cohérente à confirmer.** Phase globale conservée en P0 conformément à la checklist héritée ; aucun passage de phase n’est déclaré.
