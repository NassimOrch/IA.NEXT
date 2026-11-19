# eSonde v8.1 — Rapport d'expérience V81-FREE-GEN-001

## Description
Essai exploratoire de génération libre sur une salutation française après intégration du modèle de transitions assistant OASST1 TRAIN-only. L'option de non-réponse est désactivée. Aucune réponse cible n'est injectée.

## Architecture
Runtime indépendant `esonde_v8.generation_v81`; priors de début de réponse OASST1 TRAIN-only; transitions trigramme→bigramme→unigramme; 16 observations sémantiques nommées `E_O`; état original P/R CountSketch `E_C`; fusion au niveau des scores candidats.

## Pipeline complet
1. Vérification de la sauvegarde et de l'empreinte du checkpoint.
2. Chargement des 1 000 000 Obsiss disponibles.
3. Détection de la langue à partir du tour utilisateur.
4. Proposition du premier token depuis le prior français global.
5. Recherche de continuation dans le modèle n-gramme conditionné par la langue.
6. Classement Obsiss et calcul P/R.
7. Génération libre, non-réponse désactivée.

## Commandes d'exécution
```bash
PYTHONPATH=src python RUN_CLI_V81.py chat --prompt \"Bonjour, comment vas-tu ?\" --min-obsiss 32 --max-tokens 48 --beam-width 4 --candidate-limit 24 --no-trace
```

## Résultats
- Sortie : `La ville, il est grand chapeau de`
- Route linguistique : `fr`
- Non-réponse : désactivée, non déclenchée
- Population disponible : 1 000 000; population active à ce test : 32
- Association prompt-réponse active : non (scores de contexte nuls)
- Fichier de sortie : `v81_chat_greeting_oasst_lm_20261118.json`

## Interprétation des résultats
L'enchaînement possède un support de transition français mais ne répond pas à l'intention pragmatique du message. La convergence des votes Obsiss établit une stabilité de classement, pas la correction conversationnelle. Le prior de départ global choisit `la`; le contexte de salutation n'alimente aucune association de réponse parce que ses marqueurs ne sont pas des ancres thématiques.

## Conséquences
- **Théorique :** une transition linguistique conditionnée par la langue n'est pas suffisante pour la cohérence prompt-réponse.
- **Conceptuelle :** il faut mesurer séparément les associations contextuelles de début de réponse, dérivées des liens parent-enfant TRAIN, sans transformer les marqueurs de salutation en thèmes.
- **Opérationnelle :** construire un agrégat cue→début de réponse sans texte brut, l'exposer dans un canal E_O existant et réévaluer sur des arbres held-out.

## Conclusion
Échec du critère de cohérence sur cette salutation; exécution runtime réussie. L'erreur est ouverte sous `V81-GEN-001`.

## Statut du modèle
Prototype v8.1 en évaluation active; aucune conclusion sur la réussite finale ou l'échec général du modèle. Checkpoint original inchangé. Aucun composant neuronal déclaré.
