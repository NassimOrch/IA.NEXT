# Protocole de reconstruction d’un modèle causal génératif

## But

Tester si NGeGenBrain_v3 peut reconstruire et recomposer un comportement de prochain-token à partir de sorties observées d’un modèle neuronal entraîné, avec séparation entre le moteur de découverte et la vérité de construction. Le test est falsifiable et ses résultats sont bornés au modèle, aux entrées, à la classe d’hypothèses et aux interventions employées.

## Chemin expérimental synthétique

1. Le banc entraîne `TinyCausalLanguageModel` sur un langage de tokens cyclique. La règle cible est connue du constructeur de banc mais n’est jamais passée aux algorithmes de découverte.
2. Le modèle est enveloppé par `QueryOnlyAdapter`. Le descripteur ne révèle pas la structure ni les paramètres ; la capture d’activations est désactivée dans les capacités exposées au moteur.
3. Les contextes de longueur deux sont partagés en ensembles train et holdout avant l’ajustement. Le hash de chaque partition est enregistré. Le holdout ne choisit pas entre candidats.
4. L’algorithme cherche les candidats dans la classe pré-déclarée `modular_affine_next_token_v1`: `next=(a*previous+b*current+bias) mod V`. Il ne choisit que si un candidat unique explique toutes les observations d’entraînement.
5. Le modèle composé exécute sa règle et la boucle autoregressive sans appeler la source. La validation mesure exactitude de prochain token et trajectoires gloutonnes.
6. En parallèle, une reconstruction lookup enregistre les logits pour un domaine fini explicite. Le modèle composé lookup rejoue les logits et génère sans appeler la source ; sa validité ne s’étend pas aux contextes absents.
7. Le constructeur conserve la vérité cachée dans `auditor_only/hidden_ground_truth.json`. Elle est accessible à l’auditeur de benchmark, mais ne doit pas être fournie au moteur de découverte.

## Résultats officiels à déclarer

Les métriques numériques autorisées sont celles des fichiers `public_summary.json`, `rule_reconstruction.json`, `finite_context_lookup_reconstruction.json` et du rapport généré. Rapporter l’exactitude sur holdout, exact-match de génération, exactitude des logits sur les contextes interrogés, nombre de contextes, hashes et statut. Ne pas assimiler une bonne reconstruction comportementale à une équivalence de circuits internes.

## Chemin Hugging Face local

Le chemin `huggingface-local` fonctionne en mode `local_files_only=True`, `trust_remote_code=False`. L’utilisateur fournit les identifiants de tokens explicites pour les contextes et prompts. Le protocole lookup exige une couverture suffisante pour les suffixes atteints pendant la génération ; en cas de contexte inconnu, le résultat est non validé. Les logits sont ceux du modèle sous le tokenizer et la configuration locaux. Aucune charge utile distante n’est exécutée.

## Contre-tests recommandés

- retirer un sous-ensemble de contextes du jeu lookup et vérifier que leur usage en génération est reporté non couvert ;
- créer plusieurs règles qui expliquent les observations train et vérifier que le moteur conserve l’ambiguïté ;
- permuter ou altérer les labels de découverte et mesurer la perte de validation ;
- changer la graine, la taille du vocabulaire et le nombre d’époques ;
- comparer comportement sous interventions au comportement source lorsque l’adaptateur offre réellement l’intervention ;
- vérifier que les modèles composés ne conservent ni objet, ni poids, ni appel à la source.

## Portée

Une expérience réussie sur cette tâche donne une preuve de capacité dans ce benchmark synthétique. Elle ne signifie pas que le système a déjà reconstruit un LLM pré-entraîné, ni qu’il a identifié les mécanismes internes exacts. Les expériences externes doivent être mesurées séparément et utiliser une provenance indépendante.

## Recherche de règles sur un vocabulaire large

La recherche exhaustive des triples `(a,b,bias)` modulo `V` coûte `O(V^3)` et ne convient pas à un vocabulaire de dizaines de milliers de tokens. La classe `small_coefficient_modular_affine_v1` examine les neuf couples `a,b ∈ {-1,0,1}` modulo `V`, calcule le biais compatible avec la première ligne d’entraînement, puis teste chaque candidate restante sur toutes les lignes d’entraînement. Son coût est `O(9*n)` dans cette classe déclarée. Elle élargit l’échelle praticable sans prétendre à la découverte universelle : aucune candidate signifie seulement qu’aucune règle de cette classe n’explique exactement les lignes observées. La sélection ne consulte pas le holdout.

Pour les API Python, `hypothesis_class="auto"` choisit `modular_affine_next_token_v1` quand `vocab_size <= 32` et `small_coefficient_modular_affine_v1` au-delà. Ce sélecteur est fondé uniquement sur le coût de l’espace de recherche, et le choix est sérialisé dans le résultat. Le CLI HF local utilise par défaut la seconde classe et permet de la nommer explicitement avec `--rule-class`.
