# ORDER80.4.7 — rapport complet de bout en bout

## 1. Objet expérimental

ORDER80.4.7 teste une architecture modulaire dérivée de la réflexion suivante : au lieu d'un seul micro-model lourd qui apprend tout à la fois, plusieurs micro-models spécialisés apprennent des propriétés différentes du teacher; un micro-model maître observe uniquement leurs sorties et ORDER acquiert ensuite le maître par une interface boîte noire.

L'expérience sépare :

1. apprentissage du comportement de perte du teacher;
2. observation de l'attention standard avec deux niveaux de granularité, `surface` et `focused`;
3. apprentissage du comportement de l'entraînement;
4. apprentissage d'une compétence `focus` capable de recommander surface ou focalisé;
5. fusion de ces sorties par `micro_model_master`;
6. acquisition du maître par ORDER via OIFL-8047;
7. orchestration `prompt → think → rethink → act`;
8. adaptation sur un nouveau dataset à l'aide du substitut de perte acquis;
9. RAG et raisonnement composés sur des preuves externes.

Aucune conclusion de succès ou d'échec n'est supposée avant mesure.

## 2. Lignée utilisée

La base réellement disponible avant cette branche était ORDER80.4.3. Le teacher et ses données canoniques ont été conservés depuis cette lignée. Les anciens worktrees inexistants ne sont pas simulés ni restaurés artificiellement.

## 3. Teacher LLM

Architecture : petit Transformer causal réel, `111 424` paramètres, 2 couches, 4 têtes, `d_model=64`, contexte 64, vocabulaire 121, dropout 0, batch 4, 40 étapes.

Checkpoint canonique : SHA-256 `862acdf5c3079ab420b222fa7dd6fb26ca586e315c8fa219088525f85526f5b3`.

Données canoniques :

- train : 77 103 octets, SHA-256 `3c599ca43da8ea4f379f5cb90649126a3f4855ed634014c597d2f442bf368d8a`;
- valid : 20 943 octets, SHA-256 `2f4f75264efff0bb79c0e773a097df7c6ca22520c46e3859faa5b6356a20d`;
- test : 18 370 octets, SHA-256 `96c03fac544fc8e2aa6b3d5ba78e802711b1fbd8d47ae8d37e26ab55e76d606e`.

Le run comporte 123 événements et 123 archives NPZ. Le manifeste relie chaque archive à son hash.

## 4. Observations teacher

Les observations comprennent les entrées/cibles, logits, activations, Q/K/V, scores/cartes d'attention, gradients pré-update, paramètres post-update et états optimiseur pour les événements d'entraînement. Les nouvelles probes indépendantes utilisent un nouveau dataset et ne servent pas à entraîner le micro.

Nouveau dataset OOD : `new_dataset/{train,valid,test}.txt`; probes teacher : 12 NPZ dans `new_observation_probe/`.

## 5. Micro-model modulaire

Cinq spécialistes indépendants :

- `micro_model_loss` : prédit le comportement de perte à partir d'observations de logits/cibles; il n'implémente pas la cross-entropy du teacher comme solution;
- `micro_model_attention_surface` : observation pauvre mais précise de Q/K et positions;
- `micro_model_attention_focused` : observation plus riche de composants Q/K;
- `micro_model_training` : apprend la dynamique observée des gradients/états optimiseur;
- `micro_model_focus` : apprend quel niveau d'observation réduit réellement l'erreur.

Le corpus brut n'est pas utilisé comme cible d'apprentissage du chemin strict des spécialistes.

### Résultats spécialistes

Sur les 40 événements d'entraînement du teacher, séparation temporelle 32/8 :

- loss holdout MAE : `0.0784888`;
- attention surface holdout MAE : `0.0270276`;
- attention focused holdout MAE : `0.0271598`;
- gain vrai moyen `surface - focused` : `-0.0001322`;
- erreur du prédicteur focus : `0.0028798`;
- focused meilleur que surface : `62.5 %` des événements holdout.

Le nouveau dataset OOD donne :

- micro loss MAE : `0.225563`;
- surface attention MAE : `0.0252363`;
- focused attention MAE : `0.0274596`;
- focused meilleur : `25 %`.

Le focus n'est donc pas un gain universel : l'expérience montre ici que le mode surface est plus robuste sur ce nouveau dataset.

## 6. Micro-model master

Le master reçoit exclusivement les sorties des cinq spécialistes :

`loss`, `surface_attention_mean`, `focused_attention_mean`, `training_delta`, `focus_utility`.

Split master : 32 lignes train, 8 lignes holdout; aucune trace teacher brute n'est accessible au master.

Résultats holdout :

- loss MAE : `0.269603`;
- attention MAE : `0.0140939`;
- focus MAE : `6.50e-05`.

La métrique focus est interprétée comme reproduction du signal du spécialiste, et non comme une vérité indépendante du teacher.

## 7. Acquisition ORDER

ORDER commence avec une mémoire vide : `entries=0`.

L'acquisition s'effectue par OIFL-8047, en boîte noire. 32 requêtes d'acquisition sont enregistrées; 8 observations restent holdout. `target_observations=0`.

Les artefacts actifs sont uniquement les adaptateurs acquis et le routeur. Le binaire/master Python et les spécialistes ne sont pas présents dans la mémoire active de production.

Reproductibilité binaire de l'acquisition : les `specialists.pkl`, `micro_master.pkl` et `acquired_master_adapters.pkl` reconstruits dans une exécution fraîche sont byte-identiques aux artefacts de release.

## 8. Orchestration

Le routeur apprend à sélectionner les compétences. La séquence d'exécution est :

`prompt → think → rethink → act`.

Le mécanisme `focus` agit comme gate : il recommande `surface` ou `focused`; lorsque l'action nécessite des observations Q/K, ORDER repense puis déclenche l'action attention adéquate.

Un test d'activation réel donne la trace :

`prompt → think → act(focus) → rethink → act(attention)`.

Le routeur atteint 1.0 sur le petit jeu de contrôle interne; ce score ne doit pas être confondu avec une généralisation linguistique.

## 9. Test de perte sur nouveau dataset

Le nouveau dataset n'est pas utilisé pour apprendre les spécialistes. Après acquisition, ORDER utilise le substitut de perte acquis comme critère de sélection de petites perturbations de paramètres.

Sur la campagne enregistrée :

- sélection par substitut, test : `15.5123`;
- sélection aléatoire, test : `18.6954`;
- sélection oracle, test : `13.3552`.

Le substitut améliore donc la sélection aléatoire (`-3.1831` de perte de test dans cette campagne), mais reste moins bon que l'oracle. L'oracle est uniquement une borne de comparaison; il n'est pas utilisé dans la sélection substitut.

## 10. RAG + raisonnement

Le test contient des sources courantes et obsolètes. Le RAG sélectionne la source courante, puis transmet le fichier d'évidence au sujet expérimental de raisonnement.

Résultat : la combinaison `rag_reasoning` est activée et produit les paramètres courants `a=3, b=2`, en utilisant `current.md` avant `obsolete.md`.

Cette expérience valide la composition retrieval→evidence→reasoning; elle ne démontre pas une capacité générale de compréhension du monde.

## 11. Résultat OOD du final

Sur les 12 probes réellement nouvelles :

- erreur moyenne prédiction de perte : `1.56257`;
- attention surface MAE : `0.0769753`;
- attention focused MAE : `0.0803382`;
- décision focus correcte : `83.33 %`;
- le mode focused n'était pas meilleur sur ces 12 probes (`0 %`).

Le niveau de confiance approprié est donc différencié : le final sait exploiter les compétences acquises et choisir un niveau de focus avec un signal mesurable, mais la généralisation de la perte est nettement moins bonne sur ce nouveau domaine et l'attention n'atteint pas la fidélité observée pendant l'acquisition.

## 12. Comparaison avec le LLM

Le LLM teacher apprend directement la génération autoregressive via sa fonction de perte réelle et possède des paramètres entraînables. ORDER80.4.7 n'est pas un LLM : il ne doit pas être jugé par perplexité comme métrique principale.

Le teacher dispose de 111 424 paramètres. Le final ORDER fonctionne comme système de compétences structurées : acquisition, routage, attention, focus, adaptation, RAG et raisonnement. L'objectif expérimental est donc l'acquisition et la composition de compétences, pas la réplication architecturale exacte du Transformer.

## 13. Conséquences conceptuelles

1. Une compétence complexe peut être factorisée en plusieurs micro-observateurs spécialisés.
2. Un master qui n'observe que les sorties spécialistes réduit le couplage entre le final et les implémentations internes.
3. Le focus est mieux traité comme compétence de décision que comme mode forcé.
4. L'acquisition boîte noire permet de retirer ensuite le master vivant de l'exécution cible.
5. Un substitut de perte peut être utile comme critère de sélection même sans reproduire exactement l'optimiseur du teacher.
6. Les résultats OOD montrent que l'acquisition locale ne garantit pas une généralisation uniforme : c'est une conséquence expérimentale importante, pas un défaut à cacher.

## 14. Conséquences opérationnelles

Le pipeline modulaire est plus facile à remplacer ou ablater qu'un micro monolithique. On peut changer un spécialiste sans modifier le contrat master. OIFL permet en outre de transporter une empreinte compacte plutôt qu'un objet Python.

Pour une future branche, l'ablation la plus pertinente est de comparer plusieurs budgets de focalisation et plusieurs distributions OOD, avec des seeds supplémentaires, avant d'en faire une politique par défaut.

## 15. Innovations et statut

Innovation expérimentale revendiquée : architecture de transfert en chaîne `teacher → spécialistes → master boîte noire → ORDER`, avec OIFL, orchestration adaptative et compétence focus apprise.

Ce travail ne constitue pas une preuve de supériorité sur les LLM modernes ni une validation industrielle. Le niveau d'innovation est **expérimental / architecture de recherche**, avec une contribution méthodologique sur la séparation des rôles et l'auditabilité.

## 16. Intégrité et anti-triche

Les spécialistes n'implémentent pas explicitement `cross_entropy`, `softmax` ou le calcul analytique Q·K pour produire les cibles d'attention. Les tests statiques recherchent ces raccourcis.

L'acquisition final→master utilise uniquement l'échange OIFL. Le master n'est pas exécuté pendant les tâches cibles. `target_observations=0`.

## 17. Reproduction

Extraire les quatre ZIP sous le même répertoire :

```text
release_root/
  model_order_8_0_4_7/
  micro_model_order_8_0_4_7/
  LLM_model_order_8_0_4_7/
  audit_order_8_0_4_7/
```

Puis :

```bash
bash LLM_model_order_8_0_4_7/reproduce_llm_order8047.sh
bash model_order_8_0_4_7/pipeline/reproduce_order_8_0_4_7.sh
```

La seconde commande reconstruit spécialistes, flux d'observation, master, acquisition OIFL, routeur et tests.

## 18. Verdict

ORDER80.4.7 démontre une chaîne modulaire fonctionnelle et auditée. Le gain n'est pas uniforme : surface attention est meilleure que focused sur le nouveau dataset, le substitut de perte est utile mais imparfait, et la généralisation OOD de la perte du final reste la partie la plus faible.

Ces résultats sont conservés tels quels dans la release; aucune métrique n'est remplacée par un résultat favorable non reproductible.
