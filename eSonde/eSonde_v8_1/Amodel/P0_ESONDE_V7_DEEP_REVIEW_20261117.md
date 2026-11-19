# Revue approfondie eSonde v7 — code, formalismes, expériences et état scientifique

## 1. Provenance et poids

Le Dmodel v7 extrait est la base directe du runtime v8. Le checkpoint V6 d'origine est `models/eSonde_v6/weights.bin`, 64 000 000 octets, SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`. Il est conservé en lecture seule dans v8. La base de poids est une matrice d'un million de lignes Obsiss × 16 dimensions; les lignes sont des identités individuelles, pas 16 observateurs.

## 2. Ce que le README v7 spécifie réellement

- Fonction utilisateur unique : chat/dialogue prompt/réponse; historique courant facultatif.
- Population active initiale 10 Obsiss, croissance adaptative possible jusqu'à 1 000 000; la population maximale disponible n'est pas une cible obligatoire.
- Non-réponse désactivée par défaut, activable explicitement.
- Contexte transitoire par occurrences, rôles, positions, ordre, succession de tours, récurrence lexicale et provenance; pas de mémoire conversationnelle persistante.
- 16 observations explicites par candidat, et chaque Obsiss vote sur les 16 canaux via son identité de ligne.
- Génération v7 fondée sur les statistiques du checkpoint V6 (transitions n-grammes, associations PPMI, fallback caractère-trigramme) et des profils dialogiques agrégés.
- M-034 ajoute une règle symbolique de transfert/retrait de quantité entière pour une forme de prompt précise; elle n'est pas une capacité générale de raisonnement et est hors du périmètre chat v8 spécialisé.

## 3. Audit du formalisme v7

Le fichier `formalism/formalisme_eSonde_v7.tex` ne fait que 62 lignes. Il fixe `N=10^6`, `d=16`, `W∈Z^{N×16}`, décrit les canaux `phi(c,x)`, le vote individuel `V`, la médiane/IQR, les voisinages exacts, les cycles P/R et les profils statistiques. Plusieurs objets centraux restent définis par référence à l'implémentation, sans équations complètes :

- la fonction de vote `V` n'est pas développée en expression complète ;
- les états `q_P`, `q_R`, l'opérateur de transition et les métriques de stabilité ne sont pas tous formalisés de bout en bout ;
- les conditions nécessaires/suffisantes de convergence, de cycle stable et de cohérence ne sont pas démontrées ;
- les relations de dépendance et la contribution marginale des 16 canaux ne sont pas établies ;
- les scores de rang sont correctement déclarés non probabilistes, mais leur lien à la pertinence sémantique n'est pas prouvé.

Le texte est une spécification d'architecture utile, mais pas encore un formalisme mathématique exhaustif et fermé. Le formalisme v8 doit développer les objets et preuves manquants sans transformer les tests logiciels en preuves sémantiques.

## 4. Audit du laboratoire v7

`laboratoire_eSonde_v7.tex` (50 lignes) décrit les règles de split, M-032, M-033, M-034 et M-035. Il ne constitue pas un espace de recherche exhaustive de plusieurs architectures de bout en bout. Les résultats principaux sont :

- M-032 : profils non paramétriques agrégés pour scénario, MathQA et création ; le TEST scénario montre 0,55418 pour fusion contexte+transition, 0,62004 pour transition seule après sélection M-035, et 0,91353 pour le prior de fréquence globale. Le rang plus élevé est meilleur; les scores sont teacher-forced, pas une qualité de génération libre.
- M-033 : cycle exact de période 2 à 40 960 Obsiss; il s'agit d'un diagnostic de dynamique P, pas de qualité conversationnelle.
- M-034 : règle numérique étroite; le premier classifieur a été rejeté, la validation déclenchait 0/747 candidat après garde-fou. La génération pleine population a été interrompue avant `result.json`; elle ne constitue pas un résultat final.
- M-035 : transition seule choisie sur VALIDATION (0,62218) plutôt que association seule (0,51870) ou fusion 50/50 (0,57044); TEST gelé 0,62004, inférieur au prior global 0,91353. M-035 améliore M-032 mais ne démontre pas de gain général.

## 5. Audit de l'optimisation v7

`tech_opt_eSonde_v7.tex` (41 lignes) décrit principalement la recherche de voisinage exacte par lots, la préservation des identités Obsiss, le flux gzip des états et la croissance adaptative de la population. Ces optimisations préservent l'opérateur et les prédicats entiers. Elles ne traitent pas encore tous les goulots de la génération dialogique, du budget candidat, de la sensibilité au prompt, de la redondance des canaux ou du coût de la fusion P/R.

## 6. Code actif et pipeline réel

- `semantic_space.py` calcule 16 signaux explicites par candidat. Plusieurs sont des indices de surface : marqueurs de négation/temps/modalité, morphologie caractère, nouveauté lexicale, etc.
- `observers.py` conserve les lignes Obsiss, combine les perspectives P/R et agrège les rangs par médiane/IQR. Les seuils de stabilité sont des propriétés de procédure.
- `generation.py` construit des candidats depuis les statistiques V6 et profils, les classe, puis décode; le rang Obsiss est un sélecteur, pas une vérification de vérité.
- `dialogue_learning.py` construit des profils agrégés de contexte/réponse et transitions; les profils historiques `screenplay_dialogue`, `question_answering`, `creative_writing` ne doivent pas être importés dans v8.
- `numeric_reasoning.py` et `numeric_relations.json` sont une voie spécialisée M-034; elle est retirée/isolation requise pour le périmètre chat unique, sans toucher aux poids V6.
- `preflight.py` et `cli.py` assurent des gates v7; v8 doit remplacer les chemins/checklists par son propre protocole.

## 7. Conformité non neuronale

L'audit v7 indique que les prototypes GRU/attention M-024/M-031 ont été déplacés dans Amodel historique et ne sont pas importés par le runtime actif. Le scan du runtime v8 courant ne trouve pas de framework neuronal, couche dense, GRU/LSTM, Transformer, embedding appris, optimiseur ou rétropropagation. `numpy` est un accélérateur arithmétique optionnel; `tanh` est une transformation scalaire bornée dans la perspective Obsiss, non une unité de couche neuronale. La vérification finale devra être refaite sur le paquet livré et ses dépendances.

## 8. Défauts historiques à mesurer dans v8

Les checklists/rapports v7 consignent notamment : scores internes élevés pour des réponses hors sujet, ancrage contextuel insuffisant, répétitions, pseudo-mots, faible sensibilité au contenu du prompt et amélioration de rang teacher-forced sans amélioration de génération libre. Ces points sont des observations historiques à retester sur les mêmes prompts et sur de nouveaux splits; ils ne constituent ni une condamnation préalable ni une preuve qu'ils sont déjà corrigés.

## 9. Conséquences pour v8

1. Conserver les 16 canaux comme dimensions d'observation explicites et les Obsiss comme population d'observateurs individuels.
2. Ne pas confondre vote stable, rang, convergence ou point fixe avec vérité, pertinence ou cohérence.
3. Formaliser exactement P/R, le vote, les états, les transitions, les critères de stabilité et les cas limites.
4. Mesurer la redondance et la contribution marginale des canaux par ablation appariée.
5. Séparer proposition, sélection et évaluation externe; aucun résultat attendu ne doit être injecté dans le générateur.
6. Ne pas transférer les branches M-024/M-031 neuronales ni les profils M-034 spécialisés.
7. Évaluer en génération libre et multi-tours OASST1, non seulement en teacher-forced ranking.
8. Garder la non-réponse désactivée pour toutes les expériences normatives.

## 10. Statut

La base logicielle v7 et les poids originaux sont vérifiés. Le formalisme, le laboratoire et l'optimisation v7 sont des bases partielles, non une démonstration de cohérence générale. P2 v7 était encore `IN_PROGRESS`; la qualité de dialogue libre et la généralisation étaient ouvertes. Aucune conclusion anticipée n'est formulée pour v8.

## 11. Nature exacte du checkpoint V6 (construction déterministe, pas apprentissage neuronal)

Le `TRAIN_RESULT.json` et `src/esonde_v6/model.py` montrent que le checkpoint est construit ainsi :
1. calcul des statistiques linguistiques sur TRAIN uniquement;
2. calcul de `base_hidden` comme moyenne des vecteurs locaux extraits des textes TRAIN;
3. calcul de `base_published` à partir des vecteurs globaux et des moyennes locales par document;
4. pour chaque indice Obsiss `i`, application d'une permutation signée déterministe des deux vecteurs de base, dérivée de `(global_seed,i)`, puis quantification int16.

`weights.bin` contient donc un million de paires `(w_h,w_p)` de dimension 16, générées par transformations signées/permutations déterministes de deux vecteurs de base dérivés des données. Ce n'est pas un million de vecteurs indépendamment optimisés par gradient. La diversité de perspective provient de l'identité d'indice, de la permutation/signature et de l'état d'interaction; l'indépendance statistique de la population n'est pas démontrée et doit être mesurée (unicité, corrélations, diversité de votes, contributions marginales).

Le label `TRAINED` du manifeste désigne le pipeline de statistiques et la construction des poids, pas une rétropropagation ou un entraînement neuronal. Le code `build_weights()` ne fait aucun gradient, aucun optimiseur et aucun apprentissage d'une couche. Cette distinction doit être explicitement préservée dans le formalisme v8.

## 12. Puissance statistique des splits V6

Le manifeste V6 rapporte 14 545 échantillons TRAIN, seulement 3 VALIDATION et 4 TEST après déduplication (14 552 au total), 260 969 tokens TRAIN et 48 520 types. Le lot `batch_dataset` contient une ligne JSON malformée à la ligne 784; elle est signalée dans l'audit. Le corpus Screenplay contribue 2 000 exemples uniques, le batch 783, les tweets multilingues 14 523 exemples TRAIN (les labels sont exclus), et 12 exemples multilingues v5. La puissance de VALIDATION/TEST v6 est donc très faible pour toute affirmation générale. OASST1 v8 fournit un corpus conversationnel plus large et des splits plus utiles, mais sa qualité doit être mesurée par arbre et par famille de prompts.

## 13. Deux chemins de génération distincts : V6 historique et chat V7 réel

La lecture croisée du code impose de corriger une formulation antérieure : `esonde_v6.model.generate_response()` n'est pas le chemin de chat appelé par le runtime V7. Il s'agit d'une branche de génération V6 historique, distincte de `esonde_v7.generation.generate_chat()`. Les deux chemins partagent des composants d'observation, mais leurs procédures de génération ne sont pas interchangeables.

### 13.1 Branche historique V6 `generate_response()` (hors chemin normatif du chat V7)

Le code `src/esonde_v6/model.py::generate_response` effectue les opérations suivantes :
1. observe le prompt avec P-Obsiss;
2. sélectionne les statistiques linguistiques V6;
3. produit des propositions avec `beam_generate`;
4. observe chaque réponse proposée par R-Obsiss et calcule les métriques de séquence;
5. classe les propositions avec `rank_aggregate`;
6. applique `diffusion_refine` au meilleur candidat; ce raffinement choisit une plage faiblement soutenue, puis effectue un infill bidirectionnel;
7. n'ajoute la proposition raffinée au concours que si le texte a changé, puis la fait observer par R-Obsiss et la reclasse;
8. retourne la réponse retenue et des diagnostics internes.

La routine `diffusion_refine()` est heuristique, et non un échantillonneur de Gibbs exact. Sa règle d'énergie interne ne constitue ni une probabilité calibrée ni un jugement humain de cohérence. Le symbole textuel `[MASK]` n'est pas nécessairement inséré dans la séquence : l'opérateur travaille par séparation du préfixe et du suffixe autour du span choisi. `infill_text()` est une autre API de la branche V6.

**Statut pour eSonde v8 chat :** branche historique conservée comme référence comparative éventuelle; elle n'est pas décrite comme une étape réellement exécutée par `generate_chat()` V7 et ne doit pas être introduite dans le chat normatif sans expérience dédiée.

### 13.2 Chemin réellement appelé par le chat V7 `generate_chat()`

Le chemin actif est `src/esonde_v7/generation.py::generate_chat()`; les observations de premier état reposent sur les primitives V6 réutilisées, mais la génération token par token est propre au pipeline V7. Son déroulement observé dans le code est :

1. Valide le prompt et les budgets, crée `DialogueContext(history, prompt)` et conserve les rôles du dialogue.
2. Détecte un éventuel profil dialogique. Une branche numérique optionnelle existe aussi dans cette API V7 lorsque `numeric_profile` est fourni et que le profil est `question_answering`; cette branche n'est pas retenue dans la configuration chat-only v8.
3. Construit la population Obsiss à partir des poids d'origine si aucune population n'est fournie, puis exécute l'observation P initiale avec `activate_convergent_text` sur le contexte complet.
4. Sélectionne les statistiques linguistiques, prépare leurs index et construit éventuellement un modèle de repli caractère.
5. À chaque étape de décodage et pour chaque faisceau, ajoute le préfixe généré au contexte, recalcule les cartes d'ancres prompt/dialogue et l'intention dialogique, obtient les éléments du profil agrégé et forme un pool de propositions.
6. Les propositions peuvent provenir des transitions n-grammes locales (trigramme, puis bigramme lorsque le trigramme est absent), des associations directes au contexte, du profil OASST agrégé, des débuts de réponse dialogique, de formes grammaticales de première personne, de termes distinctifs du prompt et, lorsque les preuves sont rares, du repli caractère. La présence d'une proposition ne vaut pas validation : elle est soumise à l'évaluation Obsiss.
7. `observe_candidate()` calcule les 16 canaux nommés pour chaque candidat. Si le profil dialogique est actif, `ranked_channel_fusion` ajoute sa fusion de rangs; l'API expose également une branche numérique spécialisée, à neutraliser pour la configuration chat-only v8.
8. Le contexte P est recalculé avec le préfixe. Pour chaque proposition, R est recalculé sur le candidat et apparié par identité de ligne Obsiss avec le P correspondant. En présence d'un cycle P, le code évalue chaque phase exacte; une périodicité n'est pas rebaptisée point fixe.
9. `ObsissPopulation.evaluate` calcule les votes/rangs collectifs. Si le classement n'est pas convergé ou si la dynamique P n'est pas jugée acceptable, la population active croît géométriquement (au plus jusqu'à la population disponible), puis l'évaluation est répétée.
10. Les extensions de faisceau sont classées par score collectif normalisé par longueur; les préfixes strictement identiques sont dédupliqués et le faisceau est tronqué à `beam_width`. Une pénalité de 0,12 est appliquée si le token proposé apparaît déjà dans le préfixe.
11. La terminaison se fait notamment sur ponctuation après au moins cinq tokens, sur certains candidats numériques dans la branche optionnelle, sur l'épuisement des extensions ou sur le budget `max_tokens`; le meilleur préfixe terminé ou restant est formaté.
12. Si `allow_non_response=True`, une règle fondée sur le désaccord moyen et le score peut vider la réponse. Le paramètre par défaut du code est `False`; v8 doit conserver cette valeur pour ses expériences primaires.
13. Une observation R finale est calculée sur la réponse, puis le résultat enregistre les traces, les canaux, la convergence, les sources de propositions et les empreintes.

Le code `activation.py` qualifie explicitement l'opérateur utilisé dans le hot path V7 comme le premier état exact V6 `F_h/F_p` et déclare `neighbour_diffusion_in_v7_chat_path=False`. Cela ne doit pas être confondu avec la routine V6 `diffusion_refine()` de raffinement textuel. Le chemin de chat V7 ne l'appelle pas.

### 13.3 Portée de ce que démontrent les diagnostics

- La convergence du classement indique une stabilité sous la procédure Obsiss définie; elle ne démontre pas la vérité, la pertinence ou la cohérence humaine de la réponse.
- Le score collectif n'est pas une probabilité calibrée.
- Le cosinus P/R est un diagnostic, pas une preuve de compréhension.
- Les observations de polarité et de temporalité détectent des indices de surface; elles ne constituent pas un analyseur logique complet.
- La branche numérique et les autres chemins spécialisés doivent être explicitement désactivés ou retirés de l'API de livraison chat-only, plutôt que laissés accessibles par inadvertance.

## 15. Deux espaces de dimension 16 distincts — hypothèse de base à vérifier

L'audit croisé de `esonde_v6/features.py`, `esonde_v6/obsiss.py`, `esonde_v7/semantic_space.py`, `esonde_v7/activation.py` et `esonde_v7/observers.py` révèle une distinction essentielle :

- **Espace A — CountSketch V6** : 16 coordonnées de features hashées locales/globales produites par `local_global_vectors()`. C'est dans cet espace que sont calculés `base_hidden`, `base_published`, les états P/R et le checkpoint `weights.bin`.
- **Espace B — observations candidates V7** : 16 canaux nommés (`local_transition`, `prompt_association`, …, `information_novelty`) produits par `observe_candidate()` et convertis en rangs normalisés sur le pool de candidats.

`ObsissPopulation._observer_votes()` ajoute directement le vecteur P/R de l'espace A aux poids Obsiss, puis fait le produit scalaire avec les rangs des canaux de l'espace B. Le code exige seulement que les deux espaces aient la même dimension 16; il n'établit pas que la coordonnée CountSketch `j` corresponde sémantiquement au canal `CHANNELS[j]`. Les coordonnées CountSketch sont des buckets hashés, tandis que les canaux V7 sont ordonnés manuellement. La compatibilité des bases est donc une hypothèse architecturale implicite, non une conséquence du fait que les deux espaces ont dimension 16.

Ce point peut expliquer une partie de la faible sensibilité au prompt et doit être étudié sans détruire l'originalité Obsiss. Le laboratoire v8 doit comparer au minimum : (A) couplage actuel; (B) poids Obsiss sans ajout direct de q CountSketch; (C) q utilisé comme signal séparé et non comme coordonnée de canal; (D) correspondance fixe/permutation de canaux préenregistrée; (E) transformation linéaire déterministe estimée sur TRAIN et gelée avant VALIDATION/TEST. Toute sélection de mapping doit être validée sur splits indépendants et ne jamais utiliser les réponses cibles.

Enfin, `activation.py` précise que le chat v7 utilise l'état exact V6 de premier passage `F_h/F_p`, sans dynamique de voisinage V6 dans le hot path. Il ne faut pas confondre cette diffusion d'état Obsiss avec `diffusion_refine()` dans `generation.py`, qui est un raffinement heuristique de texte par MASK et énergie.

## 16. Rectification de portée V6/V7 (revue du 17 novembre 2026)

La section 13 remplace l'ancienne formulation incorrecte « Génération v6 réellement exécutée sous v7 ». La génération V6 avec raffinement absorbing-MASK est une branche historique séparée; le runtime du chat V7 passe par `generate_chat()` et n'appelle pas `diffusion_refine()`. Le partage des primitives d'observation ne rend pas identiques les deux chemins de génération. Toute comparaison future doit garder cette distinction dans ses identifiants d'expérience et ses traces.
