# M-031 — Objectif auxiliaire de continuité du dialogue de scénario

## Question expérimentale

M-031 ajoute à l’objectif conditionnel M-024 une tâche causale de prédiction de la prochaine réplique d’un scénario, à partir des quatre tours précédents au maximum. La question est de mesurer son effet sur la prédiction de répliques tenues à l’écart, en comparaison avec le checkpoint M-024 64D gelé.

## Portée et prudence d’interprétation

Le corpus canonique ne contient que 17 paires chat distinctes : 13 TRAIN, 1 VALIDATION et 3 TEST. Les 346 exemples TRAIN dérivés sont des tours provenant de 13 scènes, et non 346 conversations indépendantes. Les trois scènes TEST sont les trois seuls groupes de provenance du test. Tous les exemples sont issus de demandes de création de scénarios ; ils ne représentent pas les conversations ordinaires. M-031 mesure donc la continuité de dialogue de scénario, pas la généralisation conversationnelle générale.

## Construction des exemples

Le constructeur conserve les partitions canoniques eGenBrain : toute une scène reste dans un seul split. Pour chaque exemple, le prompt contient uniquement les tours précédant la cible et la cible est la prochaine réplique avec son étiquette de locuteur. Le chargeur vérifie les SHA-256 des fichiers sources, les SHA des JSONL dérivés, les volumes déclarés, l’unicité des identifiants et l’absence de chevauchement entre partitions. Une ligne JSONL malformée, `batch_dataset.jsonl:784`, est conservée comme anomalie de source et exclue par le chargeur canonique sans réparation.

## Protocole d’apprentissage enregistré avant exécution

Le protocole complet est dans `experiments/P2_M031_SCREENPLAY_DIALOGUE_PREREGISTRATION_20261116.json`. Le modèle conserve l’architecture M-024 64D, dix Obsiss actives, sans panneau sentinelle ; tokenizer limité à 1 024 entrées, quatre époques, lot effectif 32 et micro-lot physique 4. L’accumulation de gradients conserve un seul pas d’optimiseur et un dénominateur global de tokens supervisés par lot logique. Les coefficients sont 8 pour les réponses chat canoniques, 1,5 pour MathQA et 8 pour la prochaine réplique de scénario.

Le checkpoint V6 d’origine est en lecture seule. Le checkpoint M-031 est exporté uniquement dans Amodel ; aucune promotion au runtime public n’est réalisée par cette expérience.

## Évaluation

La métrique primaire est l’entropie croisée et la perplexité token-level non pondérées sur les 49 exemples TEST, après sélection du checkpoint par VALIDATION seulement. Le M-024 64D gelé sera évalué sur exactement les mêmes prompts/cibles avec son propre tokenizer. Une génération libre greedy à partir d’un manifeste prompts-only sera conservée séparément ; le générateur n’aura pas accès aux réponses de référence. Les 49 exemples sont regroupés en trois scènes sources et ne seront pas présentés comme 49 conversations indépendantes.

Aucun résultat ni direction d’effet n’est présumé par ce protocole.
