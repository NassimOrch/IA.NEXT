# Clarification M-029 — définition des mesures de couverture initiale

## 1. Description

Cette note clarifie deux mesures initiales qui avaient été présentées sous un même nom dans différents documents M-029. Le JSON canonique reste inchangé.

## 2. Architecture

Le tokenizer utilise `TOKEN_RE = whitespace | alphanumeric | non-whitespace-symbol`. Le champ `chat_first_lexeme_coverage` du JSON compte tout premier token non-espace, y compris les emojis. Le calcul du premier mot alphabétique applique ensuite `str.isalnum()` à cette première unité.

## 3. Pipeline complet

Les 13 réponses chat TRAIN sont relues depuis le résultat M-029 canonique. Pour chaque capacité, on compte d'abord les premiers tokens `TOKEN_RE` présents dans le vocabulaire, puis on filtre les ouvertures alphanumériques et on calcule leur couverture. Aucune donnée VAL/TEST n'est utilisée.

## 4. Commandes d'exécution

Aucun modèle n'a été exécuté. La clarification est un calcul dérivé du JSON canonique `P2_M029_TOKENIZER_CAPACITY_AUDIT_20261115.json` ; le fichier source n'a pas été modifié.

## 5. Résultats

Pour `max_vocab=16 384` :

- premiers tokens non-espace, emojis inclus : **10/13** ;
- premiers mots alphanumériques couverts, rapportés aux 13 réponses : **8/13** ;
- parmi les seules réponses dont le premier token est alphanumérique : **8/9**.

Pour le plafond 32 768 (vocabulaire effectif 25 719), les nombres sont identiques sur ces trois mesures. Les quatre ouvertures non alphanumériques sont des emojis/symboles ; deux tokens `🎬` sont présents dans le vocabulaire à 16 384, ce qui explique l'écart entre le comptage de tous les tokens et le comptage des mots alphabétiques.

## 6. Interprétation des résultats

10/13 et 8/13 ne sont pas deux résultats incompatibles : ils utilisent des définitions différentes. Le JSON canonique donne le compte de tous les premiers tokens non-espace. Les formalismes et commentaires portant sur les premiers mots doivent employer le compte alphanumérique. Le byte-fallback et la génération ne sont pas évalués par cette clarification.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

Les rapports doivent nommer précisément l'unité comptée et conserver le dénominateur. Les futures mesures de couverture doivent distinguer les mots, ponctuations et symboles/emoji.

## 8. Conclusions

La source canonique M-029 est conservée sans altération. Les documents sont harmonisés pour publier les deux mesures plutôt que remplacer l'une par l'autre.

## 9. Statut du modèle/expérience

`CALCUL_REPRODUIT_FROM_CANONICAL_JSON` — note de définition, sans entraînement, sans inférence, sans modification du checkpoint.
