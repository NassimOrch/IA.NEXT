# Revue du protocole M-030 — ablation tokenizer 16K

## 1. Description

Question : une augmentation contrôlée du vocabulaire lexical de 1 024 à 16 384 modifie-t-elle la prédiction conditionnelle et la génération libre, à données et objectifs identiques ? M-030 est une ablation d'entraînement sur le transducteur 64D, distincte du runtime public.

## 2. Architecture

Témoin : checkpoint M-024 64D, vocabulaire lexical 1 024 et tête de sortie 1 291 classes. Intervention : vocabulaire lexical 16 384, espace de sortie attendu de 16 651 classes. L'architecture GRU/attention par occurrence, 10 Obsiss initiales, embeddings 24, état caché 48 et fenêtre utilisateur 64 restent identiques ; aucune sentinelle n'est utilisée.

## 3. Pipeline complet

- Vocabulaire ajusté sur TRAIN seulement (texte multilingue, prompts/réponses chat TRAIN, prompts/réponses MathQA TRAIN).
- SMS exclu ; partitions VALIDATION et TEST exclues de l'ajustement du vocabulaire.
- Entraînement demandé sur TRAIN, sélection sur VALIDATION.
- Après gel du checkpoint : évaluation TEST, parité runtime et trois générations prompt-only.
- Toute génération est sans réponse de référence et avec non-réponse désactivée.

## 4. Commandes d'exécution

La commande exacte est dans `experiments/P2_M030_ATTEMPT2_COMMAND_20261115.json`. Paramètres : seed 20261114, 4 époques, batch 32, AdamW 0,001, decay 0,0001, poids chat 8, poids MathQA 1,5, gradient clipping 1,0, 2 threads, toutes les données TRAIN. Préflight P2 : PASS.

## 5. Résultats

M-029 distingue maintenant deux mesures d'ouverture pour éviter de compter emoji et mots sous un intitulé unique :

| Mesure TRAIN chat | Vocabulaire 1 024 | Vocabulaire 16 384 |
|---|---:|---:|
| OOV lexical des réponses | 30,8723 % | 5,9334 % |
| Unités byte-fallback | 28 000 | 6 276 |
| Premier token non-espace, symboles inclus | 0/13 | 10/13 |
| Premier mot alphanumérique couvert, dénominateur 13 réponses | 0/13 | 8/13 |
| Couverture parmi les seuls débuts alphanumériques | 0/13 | 8/9 |

Réduction des unités byte-fallback : 77,59 %. La deuxième tentative M-030 a terminé avec code `-9` après deux époques sur quatre. Validation mixte pondérée : 26,4778 à l'époque 1 et 16,6326 à l'époque 2 ; chat : 71,3209 puis 50,1833 ; MathQA : 24,2779 puis 14,5854. Aucun checkpoint final n'a été écrit ; TEST et générations libres non exécutés. Voir `RAPPORT_P2_M030_TRAINING_INTERRUPTED_ATTEMPT2_20261115.md`.

## 6. Interprétation des résultats

La capacité 16 384 réduit le byte-fallback des cibles TRAIN et couvre davantage de tokens initiaux. 10/13 désigne tous les premiers tokens non-espace, y compris les symboles/emoji ; 8/13 désigne les premiers mots alphanumériques couverts, les 13 paires restant au dénominateur. Ces mesures sont complémentaires. Les deux époques d'entraînement ne sont pas un résultat final et ne permettent aucune conclusion causale sur la qualité générative.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

- **Théoriques :** distinguer couverture lexicale, prédiction conditionnelle et compétence conversationnelle.
- **Conceptuelles :** byte-fallback préserve la couverture mais peut allonger la production d'un mot rare ; davantage de lexèmes ne prouve pas la compréhension.
- **Opérationnelles :** le trainer doit persister à chaque frontière d'époque le modèle, l'optimiseur, les états RNG, la configuration et l'empreinte des données, puis valider une reprise déterministe sur fixture avant la nouvelle tentative M-030.

## 8. Conclusions

Le pré-enregistrement reste valide comme question à une variable. L'exécution actuelle est incomplète ; aucun checkpoint ni TEST n'est disponible. Aucun paramètre n'a été changé en cours d'exécution. Le résultat devra être repris après amélioration de la persistance et une nouvelle sauvegarde vérifiée.

## 9. Statut du modèle/expérience

`INCOMPLETE` — M-029 est terminé comme audit TRAIN-only ; M-030 tentative 2 est interrompue après 2/4 époques, sans checkpoint final ; P2 reste `IN_PROGRESS`.
