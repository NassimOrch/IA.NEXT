# Architecture eSonde v7 — spécification opérationnelle

## 1. Périmètre

La seule capacité utilisateur est le chat : historique courant facultatif, prompt, réponse générée. `status` et `verify` sont des opérations de maintenance. Aucun mode traduction, classification, résumé, recherche ou infill n'est exposé.

Le checkpoint eSonde v6 est conservé en lecture seule : 1 000 000 de lignes Obsiss, 16 coordonnées, 64 000 000 octets. Le runtime v7 peut activer un préfixe du checkpoint. Il commence par défaut à 10 Obsiss et augmente la population uniquement si la dynamique ou la stabilité décisionnelle exigée n'est pas atteinte. Un million est le maximum disponible, pas un objectif.

## 2. Pipeline de dialogue

```text
Historique courant + prompt
        │
        ▼
Occurrences (tour, rôle, token, position, provenance)
        │
        ▼
Contexte éphémère C_t
        │
        ├── Dynamique P exacte v6 sur la population active
        │      └── q_i apparié par identifiant d'Obsiss
        │
        ▼
Pour chaque préfixe du beam :
  reconstruction du contexte avec le préfixe
  rafraîchissement de l'état P du préfixe
  propositions n-grammes / PPMI / retour caractère TRAIN
  16 observations explicites par candidat
  rang de chaque observation dans le pool
  voix individuelle de chaque Obsiss
  médiane collective + IQR + stabilité de population
  extension du beam
        │
        ▼
Réponse produite
        │
        ▼
Dynamique R exacte v6 conditionnée par q_i P apparié
        │
        ▼
Résultat, traces, preuves, erreurs éventuelles et snapshot
```

Le contexte est reconstruit à partir des messages et du préfixe généré. Il ne constitue ni une base de réponses ni une mémoire persistante du modèle.

## 3. Obsiss : perspective complète sur 16 observations

Chaque ligne `i` conserve son identité et ses deux vecteurs originaux `w_h[i]` et `w_p[i]`. Une Obsiss n'est pas affectée à une dimension primaire/secondaire : elle observe les 16 canaux à travers sa propre perspective. Pour `j` dans `0..15` :

```text
pi(j) = (7*j + 3) mod 16
u[i,j] = tanh((w_h[i,j] + w_p[i,j]) / 8192)
         + 0.50*tanh(q[i,j] / 8192)
         + 0.25*tanh(q[i,pi(j)] / 8192)
a[i,:] = u[i,:] / (sum(abs(u[i,:])) + epsilon)
v[i,c] = sum_j(a[i,j] * rank_j(c))
```

La voix `v[i,c]` est calculée pour chaque Obsiss et chaque candidat. La médiane des voix établit le centre collectif ; l'IQR conserve le désaccord. Le hash SHA-256 de la colonne ordonnée des voix permet de vérifier un recalcul sans sérialiser un million de flottants dans chaque événement. Les résultats individuels sont reproductibles à partir de la ligne d'origine, du contexte et du pool.

## 4. Les 16 observations

| # | Canal | Mesure opératoire |
|---:|---|---|
| 1 | Transition locale | Succession bigramme/trigramme TRAIN |
| 2 | Association prompt | Association PPMI avec ancrages du prompt et recouvrement exact |
| 3 | Association dialogue | Association PPMI pondérée par récence |
| 4 | Récurrence lexicale | Correspondance exacte d'occurrences actives |
| 5 | Affinité morphologique | N-grammes de caractères, sans équivalence sémantique implicite |
| 6 | Rôle de réponse | Support de débuts de réponse TRAIN |
| 7 | Continuité discursive | Association avec le préfixe déjà généré |
| 8 | Polarité observée | Marqueurs explicites de négation |
| 9 | Temporalité observée | Marqueurs temporels explicites |
| 10 | Frontière | Compatibilité de ponctuation et frontière de token |
| 11 | Support TRAIN | Fréquence lexicale TRAIN |
| 12 | Retour sous-mot | Modèle caractère-trigramme TRAIN pour propositions OOV |
| 13 | Continuité référentielle | Témoin lexical dans les tours antérieurs |
| 14 | Modalité observée | Marqueurs modaux explicites |
| 15 | Alignement de locuteur | Continuité lexicale avec les tours assistant |
| 16 | Nouveauté informationnelle | Nouveauté ou répétition dans le préfixe récent |

Les canaux sont des mesures bornées. La présence d'un marqueur n'est pas une analyse complète de sa portée ; une récurrence lexicale ne prouve pas la coréférence ; l'ordre ne prouve pas la causalité.

## 5. Deux tests indépendants de convergence

### 5.1 Dynamique Obsiss P/R

La fonction `activate_convergent_text` exécute le mécanisme exact d'interaction de v6 sur une vue en lecture seule des premières `n` lignes. `NO_ACTIVE_NEIGHBORS` signifie que l'index de voisinage exact ne trouve plus d'arête active au point de contrôle. `VECTOR_LENGTH_REACHED` signifie seulement que la borne de `d-1` mises à jour a été atteinte. Ce second statut n'est jamais appelé convergence.

### 5.2 Stabilité de la décision

Pour chaque pool de candidats, les voix sont recalculées sur la population active. Pour `2 <= n <= 128`, chaque Obsiss est retirée une fois ; au-dessus, huit partitions déterministes disjointes sont évaluées. La décision est stable si la rétention du top-1 est au moins `0.90`, le Jaccard top-k moyen au moins `0.90` et le Spearman moyen au moins `0.95`. Un pool singleton ne permet pas d'établir cette stabilité.

La croissance part de `min(10, N_disponible)` puis double lorsque l'un des critères manque. Le système s'arrête au premier niveau satisfaisant les critères ou au plafond explicite. Le rapport distingue toujours convergence dynamique, stabilité de classement, et convergence combinée. Aucune de ces propriétés ne prouve la factualité.

## 6. Génération de texte

Les candidats sont construits à partir des transitions n-grammes, associations PPMI et fréquences TRAIN. Lorsque le pool lexical local est faible, un retour caractère-trigramme dérivé de TRAIN propose des formes lexicales supplémentaires. Les canaux observent alors prompt, dialogue, préfixe, morphologie, ponctuation, marqueurs et support de langue. Le vote intervient avant chaque extension du beam, et non après la phrase complète. L'activation R candidate-spécifique intervient elle aussi avant ce choix ; l'état R de chaque candidat est associé à la même Obsiss que son état P et son empreinte est conservée dans les témoins du token retenu.

Le générateur demeure conditionné par les statistiques lexicales de v6. L'espace d'observations et le vote Obsiss ne sont pas un parseur syntaxique complet ni un système de vérité factuelle. Les réponses doivent être évaluées sur corpus et par annotation indépendante.

## 7. Contexte transitoire inspiré d'eGenBrain

La conception reprend la discipline occurrence-level, les relations typées, la provenance, la distinction ordre/causalité, et la reconstruction locale d'un maillage. Le graphe est dérivé des messages et préfixes présents ; il est détruit à la fin de l'appel. Le runtime n'importe pas une base de faits persistante eGenBrain et ne récupère pas de réponses stockées.

## 8. Non-réponse

`allow_non_response=False` est la valeur par défaut. Le mode est activable explicitement par `--allow-no-response` dans le CLI ou la case de l'interface. Lorsque le mode est désactivé, un faible niveau d'accord ne peut pas être converti en silence. Une erreur technique reste une erreur, non une non-réponse.

## 9. État expérimental

Les tests logiciels vérifient le fonctionnement des opérateurs et les invariants de programme. La qualité des réponses, la robustesse multi-tours et la comparaison équitable avec des architectures LLM restent des mesures empiriques distinctes. Les conclusions doivent s'appuyer sur des sorties de dialogue réelles et sur une évaluation externe aveugle.
