# Rapport de reprise, continuité et traçabilité EX5

1. Lecture du prompt EX5 1.1, EX4 et EX3, inventaire complet des sources et archives.
2. Vérification des archives et manifestes EX4 ; absence de réentraînement des résultats EX4 vérifiés.
3. Création du workspace EX5 et v001, pré-enregistrement Wisconsin développement uniquement.
4. RETRO, facteur alpha/beta, traces pré/post-activation et Adam/gel ; duplication retro_linear/1501 conservée et dédupliquée seulement pour les stats.
5. Proportions fixe/adaptative et gates ; micro-MIXA statique ; OOF résiduel.
6. v002 alternance A↔B et tests de gel strict.
7. v003 transfert Wine/Digits ; manifeste de freeze écrit avant test ; bootstrap corrigé.
8. v004 ablations question/réponse ; correction sidecar du champ Q-only trop large.
9. v005 sharing/factorisation de l'encodeur et centres.
10. v006 PCA question-only et vectorisation exacte v005 ; reprise checkpoint toutes les cinq époques pour les runs fixes longs.
11. Audit global des JSON, JSONL, checkpoints, prédictions, métriques et rapports ge4x après v006.
12. Vérification ZIP et empreinte après consolidation.

Les runs interrompus par les limites de durée des commandes ont été repris depuis les checkpoints, pas redémarrés. Les doublons de reprise sont explicitement notés ; les résultats bruts restent append-only. Le workspace final permet de retrouver par version le script, la configuration, le jeu de données, la graine, le checkpoint et la prédiction.
