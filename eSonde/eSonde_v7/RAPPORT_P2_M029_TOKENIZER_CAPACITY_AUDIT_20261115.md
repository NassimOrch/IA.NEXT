# RAPPORT P2-M029 — audit de capacité du tokenizer

**Date :** 15 novembre 2026  
**Statut :** audit TRAIN-only terminé ; aucun modèle entraîné ou exécuté ; ablation de capacité préparée.

## 1. Description

M-029 mesure la couverture lexicale du tokenizer WordByte à plusieurs plafonds de vocabulaire, avec les données TRAIN uniquement utilisées par M-024. Le but est de quantifier la charge byte-fallback susceptible d'affecter les ouvertures et la continuité lexicale, sans conclure à l'avance que cette variable explique les défauts conversationnels.

## 2. Architecture et méthode

Le tokenizer courant utilise une expression régulière mot/ponctuation/espace, un vocabulaire de lexèmes appris sur TRAIN (`min_frequency=2`), et un encodage UTF-8 byte-fallback pour tout lexème absent. Les ID réservés sont conservés ; seuls les plafonds de vocabulaire lexical varient. Les ensembles de validation/test ne servent ni à ajuster le vocabulaire, ni à choisir des lexèmes.

Le périmètre TRAIN utilisé pour construire chaque vocabulaire : 13 paires chat, 5 978 paires MathQA et 13 759 textes autonomes TRAIN. Le SMS est exclu. L'ensemble lexical global contient 61 927 lexèmes distincts observés.

## 3. Pipeline complet et commande

Le lecteur canonique eGenBrain a réconcilié les splits ; les textes TRAIN sont tokenisés avec chaque plafond ; la couverture lexicale, les mots OOV, les unités byte-fallback et la couverture des premiers lexèmes des réponses chat sont calculés par source. Aucun réseau, checkpoint expérimental ou décodeur n'est initialisé.

```bash
python Amodel_eSonde_v7/tools/audit_tokenizer_capacity.py \
  --source-root /mnt/data/work_esonde_v7 \
  --v6-model-dir Dmodel_eSonde_v7/models/eSonde_v6 \
  --capacities 1024,2048,4096,8192,16384,32768 \
  --output Amodel_eSonde_v7/experiments/P2_M029_TOKENIZER_CAPACITY_AUDIT_20261115.json
```

## 4. Résultats chat TRAIN

| Plafond | Vocabulaire réel | Couverture lexicale réponses | Lexèmes OOV | Unités byte-fallback | Premiers mots alphanumériques couverts (sur 13 réponses) |
|---:|---:|---:|---:|---:|---:|
| 1,024 | 1,024 | 69.13% | 3,663 | 28,000 | 0/13 |
| 2,048 | 2,048 | 76.78% | 2,755 | 21,611 | 0/13 |
| 4,096 | 4,096 | 84.58% | 1,829 | 15,096 | 0/13 |
| 8,192 | 8,192 | 89.36% | 1,262 | 10,726 | 4/13 |
| 16,384 | 16,384 | 94.07% | 704 | 6,276 | 8/13 |
| 32,768 | 25,719 | 96.01% | 473 | 4,219 | 8/13 |

À la capacité actuelle de 1 024 lexèmes, 3 663 des 11 865 occurrences lexicales de réponse chat TRAIN (30,87 %) sont OOV. Elles génèrent 28 000 unités byte-fallback, en comptant les marqueurs `BYTE_START`/`BYTE_END`. La couverture des premiers mots alphanumériques des 13 réponses est de 0/13 ; les 13 premiers tokens non-espace sont byte-fallback à la capacité actuelle.

À 16 384 lexèmes, la couverture passe à 94,07 %, les unités byte-fallback descendent à 6 276 (−77,6 % par rapport à 1 024), et 8/13 premiers mots alphanumériques sont couverts (8/9 parmi les seules réponses commençant par un mot). Le JSON canonique compte tous les premiers tokens non-espace, y compris les symboles et emojis : selon cette définition, le compte est 10/13 à 16 384 et également 10/13 à la capacité effective 25 719. La différence 8/13 vs 10/13 vient donc de l'unité comptée, pas d'une modification des sources. Les premiers mots alphanumériques non couverts à 16 384 comprennent `FADE`; les autres réponses non couvertes selon la mesure alphanumérique sont des ouvertures symboliques.

## 5. Interprétation

Le tokenizer 1 024 laisse une charge OOV importante, particulièrement sur le texte autonome et les dialogues créatifs ; la première unité de chacune des 13 réponses chat est `BYTE_START`. Une capacité 16 384 réduit fortement cette charge sans éliminer le fallback. Il s'agit d'une limitation mesurée de représentation lexicale, pas d'une preuve causale que le tokenizer explique à lui seul les sorties répétitives. Le biais top-1 `BYTE_START` observé en M-027 est compatible avec les statistiques de données, mais M-027 ne démontre pas qu'il en est la cause unique.

La croissance du vocabulaire augmente le coût de l'embedding et surtout de la tête de sortie. Le prochain test doit donc être un ablation contrôlée, non une promotion automatique du plafond le plus grand.

## 6. Conséquences théoriques, conceptuelles et opérationnelles

- **Théoriques :** séparer la capacité de représentation lexicale, la modélisation conditionnelle et la sélection contextuelle des réponses.
- **Conceptuelles :** byte-fallback préserve la couverture universelle, mais n'assure pas à lui seul l'apprentissage correct de la morphologie ou de l'orthographe des mots rares.
- **Opérationnelles :** M-030 (ablation contrôlée) comparera 1 024 et 16 384 lexèmes à données, graine, architecture GRU/attention, pertes et budget identiques. Le TEST restera exclu de l'entraînement et ne sera consulté qu'après gel du checkpoint.

## 7. Conclusion et statut

M-029 confirme que la capacité lexicale actuelle est faible au regard des lexèmes du TRAIN et que 16 384 réduit substantiellement le recours au byte-fallback. Il ne détermine pas encore le plafond optimal et ne valide pas la qualité conversationnelle. P2 reste `IN_PROGRESS`.

## 8. Intégrité

- JSON : `Amodel_eSonde_v7/experiments/P2_M029_TOKENIZER_CAPACITY_AUDIT_20261115.json`
- SHA-256 JSON : `a27f47d286e4d8057f8a2be3abce676b6a37ff1cfd4c8641865d7f4d0080f050`
- Checkpoint V6 : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4` (64 000 000 octets, inchangé)
- Sources utilisées : hashes eGenBrain Parquet/JSONL et corpus textuel consignés dans le JSON.
- Modèle exécuté : non. Entraînement : non. Génération : non.
