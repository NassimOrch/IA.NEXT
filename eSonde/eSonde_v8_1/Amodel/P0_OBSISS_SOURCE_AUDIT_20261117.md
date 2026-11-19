# Audit de la structure Obsiss v6/v7 — base de travail v8

## 1. Les 16 observations (canaux)

Le code source `src/esonde_v7/semantic_space.py` déclare exactement les 16 canaux suivants, dans cet ordre :

1. `local_transition` — support de continuation n-gramme observé ;
2. `prompt_association` — cooccurrence/distribution par rapport au prompt ;
3. `dialogue_association` — cooccurrence par rapport aux tours antérieurs ;
4. `lexical_recurrence` — continuité lexicale exacte au niveau occurrence ;
5. `morphological_affinity` — similarité de trigrammes de caractères, explicitement non équivalente à une identité sémantique ;
6. `response_role` — support de débuts de réponses avec rôle explicitement qualifié ;
7. `discourse_continuity` — association au préfixe généré ;
8. `polarity_observation` — co-observation de marqueurs explicites de négation ;
9. `temporal_observation` — co-observation de marqueurs temporels explicites ;
10. `boundary_observation` — compatibilité de ponctuation/frontières ;
11. `training_support` — fréquence/distribution de TRAIN ;
12. `subword_backoff` — indices caractère pour formes inconnues productives ;
13. `reference_continuity` — témoin lexical dans les tours précédents ;
14. `modality_observation` — co-observation de marqueurs modaux explicites ;
15. `speaker_alignment` — continuité lexicale des tours assistant antérieurs ;
16. `information_novelty` — nouveauté/répétition relativement au préfixe.

Ces canaux sont les « dimensions » d'observation au sens de l'utilisateur, sans transformer chaque dimension en Obsiss. Ils ne sont pas 16 neurones. Une Obsiss est une identité individuelle qui évalue les 16 canaux selon une perspective signée issue de sa ligne de checkpoint.

## 2. Calcul effectif des signaux et limites sémantiques

Le code `observe_candidate()` calcule chaque signal à partir du prompt, du dialogue, du préfixe, du candidat et des statistiques de TRAIN. Plusieurs signaux sont explicitement superficiels :

- La négation détecte des marqueurs tels que `not`, `no`, `pas`, `jamais`; elle ne calcule pas la portée logique, la négation enchâssée ou la portée sur des quantificateurs.
- La temporalité détecte des marqueurs tels que `before`, `after`, `today`, `avant`; elle ne construit pas une représentation temporelle complète.
- La modalité détecte `may`, `must`, `could`, `doit`; elle ne résout pas la portée et l'engagement épistémique.
- La morphologie compare des ensembles de n-grammes de caractères; le code la qualifie lui-même de faible indice, non d'identité lexicale ou de synonymie.
- `information_novelty` mesure l'absence du token dans le préfixe courant, pas la nouveauté conceptuelle.
- `response_role` utilise des fréquences de débuts de réponse explicitement qualifiées; le code documente que les débuts issus de tweets ne doivent pas être traités comme un prior de rôle assistant.

Ces signaux sont utiles comme observations distinctes, mais leur nom ne doit pas être confondu avec une compétence sémantique déjà acquise.

## 3. Population Obsiss

`src/esonde_v7/observers.py` confirme :
- le checkpoint doit avoir exactement 16 dimensions ;
- chaque Obsiss est une perspective complète sur les 16 canaux, pas un canal isolé ;
- les lignes de poids originales conservent leur identité ;
- le vote combine une base signée `(w_h+w_p)`, un état contextuel propre `q` et une permutation inter-observations déterministe ;
- les perspectives sont normalisées par somme des valeurs absolues ;
- les candidats sont évalués par votes individuels, agrégés par médiane, avec dispersion conservée ;
- les rangs sont des mid-ranks normalisés sur `[0,1]`, explicitement non probabilistes ;
- le score P/R peut être fusionné au rang par rang, sans mélanger les échelles brutes.

La population est évaluée paresseusement. Le nombre d'Obsiss actifs peut croître si le classement n'est pas stable. La stabilité est mesurée par rétention top-1, Jaccard top-k et Spearman, avec seuils 0.90/0.90/0.95. Ce test mesure la robustesse de l'ordre collectif aux changements de sous-population ; il ne prouve ni vérité, ni pertinence, ni cohérence de la réponse.

## 4. Nature non neuronale du mécanisme observé

Le code `esonde_v6/obsiss.py` définit des transformations arithmétiques déterministes, permutations signées, quantification int16, agrégation et interactions populationnelles. NumPy est un accélérateur optionnel et SciPy un index spatial optionnel. Il n'y a dans le chemin actif inspecté ni module torch/tensorflow, ni couche dense entraînable, ni MLP, ni Transformer, ni rétropropagation. La fonction `tanh` est utilisée comme transformation scalaire bornée dans le calcul d'une perspective, pas comme unité organisée en couche neuronale.

Cette constatation statique devra être répétée sur l'ensemble des dépendances et appels indirects du paquet final. Le checkpoint d'origine reste inchangé.

## 5. Conséquences de formalisation pour v8

- Garder `CHANNELS` comme espace `O(x, dialogue, candidate) ∈ R^16` et versionner l'ordre des canaux.
- Garder la population Obsiss `Ω={ω_i}` distincte de l'espace des canaux.
- Définir l'observation comme une fonction déterministe avec provenance; distinguer `0`, absence de preuve et signal non calculable.
- Établir les relations de dépendance entre canaux, mesurer la redondance et la contribution marginale par ablation appariée.
- Tester la robustesse à la paraphrase, au changement de langue, à l'ordre du contexte, aux distracteurs, à la négation de portée, à la temporalité et aux références pronominales.
- Ne pas promouvoir une stabilité de rang ou un score de transition en preuve sémantique.
- Toute amélioration doit être comparée à la même base, sur les mêmes prompts/splits, avec non-réponse désactivée.

## 6. Statut

La définition logicielle des 16 canaux et de la population Obsiss est lue directement dans les sources. La validité sémantique globale des canaux, leur indépendance et leur apport marginal ne sont pas établis par la seule présence du code. Les expériences d'ablation v8 restent nécessaires.

## 7. Correction essentielle : deux espaces 16D différents

Le checkpoint `weights.bin` et les états P/R V6 sont définis dans l'espace A des 16 coordonnées CountSketch (features hashées locales/globales). Les canaux nommés V7 sont l'espace B des 16 observations sémantiques calculées par `semantic_space.py`. Le runtime applique les poids et le vecteur P/R A aux rangs des canaux B parce que les deux dimensions valent 16; aucune preuve n'établit que les coordonnées A et B sont alignées sémantiquement.

Le code conserve bien l'identité de chaque ligne Obsiss et l'utilise comme perspective signée. Mais la phrase « chaque Obsiss a une perspective complète sur les 16 canaux » décrit l'usage opérationnel, pas une correspondance de bases démontrée. Il faut distinguer cette opération de son interprétation. L'audit a consigné une hypothèse de compatibilité des bases, à tester par ablations et mappings gelés.

## 8. Origine et diversité réelle des lignes Obsiss

`esonde_v6/model.py::build_weights()` calcule deux vecteurs de base sur TRAIN (`base_hidden`, `base_published`), puis applique à chaque indice Obsiss une permutation signée déterministe dérivée de `(global_seed,index)`, quantifiée en int16. Les lignes ne sont donc pas un million de paramètres indépendamment optimisés; elles sont des perspectives déterministes distinctes issues de deux vecteurs de base. L'état d'interaction peut différencier leur comportement, mais leur indépendance statistique n'est pas établie. Les tests doivent mesurer unicité, corrélation, diversité de vote et contribution marginale.

## 9. Apports de la théorie générale de l'observation

Le formalisme `NGeGenBrain_observation_formalisme_full_0.tex` fournit des obligations directement utiles :
- observation, mesure, enregistrement, empreinte, invariant et interprétation sont des objets distincts;
- l'indiscernabilité induite par une empreinte forme des fibres/quotients; une propriété se factorise par l'empreinte si et seulement si elle est constante sur chaque fibre;
- l'ajout d'une sonde affine les partitions; une sonde redondante n'apporte aucune nouvelle distinction sur le domaine déclaré;
- l'équivalence empirique sur un échantillon n'est pas une équivalence universelle;
- les valeurs manquantes, erreurs et timeouts sont des statuts typés, jamais des zéros;
- un effet après intervention n'identifie pas à lui seul un mécanisme;
- une statistique agrégée n'est pas un mécanisme exécutable;
- l'autonomie exige la fermeture des dépendances, sans oracle ou appel caché;
- la validation, la sélection et le test final doivent rester séparés;
- la généralisation sur un domaine infini n'est pas garantie par un nombre fini de tests;
- la provenance et les hashes garantissent seulement l'intégrité post-enregistrement sous hypothèses, pas la vérité ou l'exhaustivité de l'acquisition.

Pour Obsiss, le laboratoire peut utiliser le raffinement des partitions et l'entropie de partition target-free pour mesurer l'apport de chaque canal sans regarder la réponse cible. Ces mesures sont des diagnostics d'observation, non un nouveau score de cohérence.
