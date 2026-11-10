# Protocole de validation expérimentale — eSonde v3

**Version :** 3.0  
**Date :** 10 novembre 2026  
**Statut :** protocole de validation logicielle et diagnostic linguistique ; résultats séparés par niveau de preuve.

## 1. Description

Le protocole vérifie les invariants et interfaces du runtime à sondes explicites, puis évalue séparément les prédictions next-token sur des corpus disjoints. Il ne pose ni succès ni échec généraliste à l'avance. Les métriques faibles restent des observations du checkpoint, de la tâche, du corpus et des paramètres considérés.

## 2. Architecture et objets mesurés

La distribution linguistique est le mélange convexe des familles actives `SEQ`, `SKIP_REL`, `MORPH`, `SEM`, `DISC`, `RETR`, `BYTE`, coordonné par `COORD`. Les contrôles logiciels ciblent les familles et leurs invariants. Les mesures linguistiques ciblent la NLL conditionnelle, la perplexité, la couverture OOV, la précision top-k et les résultats par langue/document. Les mesures officielles de QA doivent être rapportées séparément (EM/F1) ; le script fourni n'est pas un évaluateur officiel MLQA.

## 3. Pipeline complet

1. Identifier le checkpoint, sa version de tokenizer, son SHA-256 et son provenance.
2. Définir explicitement les splits par document et vérifier les doublons par identifiant et SHA-256.
3. Entraîner seulement sur train ; utiliser validation uniquement pour COORD ; garder test hors entraînement et calibration.
4. Exécuter d'abord les tests unitaires et l'audit de pureté.
5. Calculer NLL, perplexité, couverture OOV et diagnostics par langue.
6. Comparer les ablations en conservant la même cible et le même espace de sortie ; signaler toute baseline dont l'espace de sortie diffère.
7. Enregistrer les sorties brutes, les paramètres, versions, codes de sortie, hashes et interprétation.
8. Créer un snapshot vérifié avant la campagne suivante.

## 4. Commandes

Voir `CLI_GUIDE.md` et `VALIDATION_V3.md`. Les commandes centrales : `train`, `calibrate`, `generate`, `score`, `retrieve`, `relations`, `coref`, `inspect`, `audit`, `info`. Pour MLQA, `scripts/evaluate_mlqa_next_token.py --help` publie le contrat complet.

## 5. Résultats

La suite logicielle est consignée dans `VALIDATION_V3.md` et les journaux `EXEC-0066` à `EXEC-0084`. Le diagnostic MLQA sur 56 paragraphes/4 055 tokens/7 langues indique un OOV à 86,56 %, une NLL COORD de 31,3662 nats et une NLL sans BYTE de 598,4486 nats. Ces valeurs ne doivent pas être confondues avec une mesure officielle QA. Le modèle a seulement 415 tokens de train et 80 cibles de validation.

## 6. Interprétation

L'intégration BYTE améliore nettement ce diagnostic par rapport à l'ablation sans BYTE en donnant des probabilités aux chaînes OOV. La NLL reste élevée ; les scores absolus ne montrent pas une qualité linguistique généraliste. La baseline qui regroupe tous les OOV sous une classe ne partage pas le même espace d'événements et n'est donc pas un comparateur équivalent.

## 7. Conséquences

- **Théorique :** les distributions des familles sont conditionnelles au contexte et à l'état ; COORD réalise un mélange convexe normalisé.
- **Conceptuelle :** OOV n'est pas un token unique ; BYTE traite la chaîne de surface.
- **Opérationnelle :** les splits, hashes et paramètres sont indispensables ; pas de train MLQA dans l'archive fournie.
- **Évaluation :** il faut un corpus d'entraînement généraliste distinct et des tests indépendants pré-enregistrés pour évaluer plus largement le comportement.

## 8. Conclusion et statut

Le protocole v3 est défini et un diagnostic linguistique a été exécuté. Les contrôles logiciels par groupes sont passés ; la suite combinée doit être actualisée après les dernières modifications. L'évaluation générale reste ouverte. Ce statut ne préjuge pas de l'issue future de l'architecture.
