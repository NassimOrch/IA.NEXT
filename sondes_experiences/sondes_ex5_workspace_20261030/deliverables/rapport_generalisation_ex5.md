# Généralisation et statistiques externes

La campagne externe v003 compare trois candidates sélectionnées sur validation Wisconsin sur Wine et Digits, cinq graines par candidate et domaine : 30 sondes, 60 MLP (matched/ge4x). Le manifeste `FROZEN BEFORE TEST ACCESS` est écrit avant les prédictions test. Les comparaisons ge4x respectent le ratio sur les 30 liens sonde/MLP ge4x, minimum environ 4,007.

Bootstrap apparié par sujet, 20 000 rééchantillonnages et correction Bonferroni sur six comparaisons. Les graines sont répétitions d'initialisation sur les mêmes sujets, non 5 tests indépendants. Marges : -2 points d'accuracy et +5 % de log-loss relative.

| Domaine | Candidate | n test | Delta accuracy sonde−MLP | Excès relatif log-loss | Non-infériorité conjointe |
|---|---|---:|---:|---:|---|
| wine | A3F1_d4k16_equal | 36 | -0.0056 | +0.830 | NON |
| wine | A3F1_d4k8_equal | 36 | -0.0056 | +0.048 | NON |
| wine | A3F1_d4k8_input | 36 | +0.0222 | -0.401 | NON |
| digits | A3F1_d4k16_equal | 360 | -0.0750 | +2.654 | NON |
| digits | A3F1_d4k8_equal | 360 | -0.1061 | +4.549 | NON |
| digits | A3F1_d4k8_input | 360 | -0.1006 | +3.871 | NON |


Les six comparaisons échouent à la non-infériorité conjointe. Sur Wine, la variante gate entrée a un point d'estimation favorable (delta accuracy +2,22 points et log-loss relative -40,1 %) mais les bornes de confiance corrigées ne prouvent pas la non-infériorité conjointe, en particulier avec 36 cas de test. Sur Digits (360 cas), les trois candidates sont nettement derrière le MLP en accuracy et log-loss.

Banknote Authentication et MAGIC Gamma Telescope ont été tentés mais les archives de données n'ont pas été récupérées dans l'environnement à cause de l'indisponibilité DNS ; aucune métrique n'est inventée. Iris est un transfert EX4 antérieur, exploratoire et de taille test limitée, et n'est pas compté comme confirmation de EX5.
