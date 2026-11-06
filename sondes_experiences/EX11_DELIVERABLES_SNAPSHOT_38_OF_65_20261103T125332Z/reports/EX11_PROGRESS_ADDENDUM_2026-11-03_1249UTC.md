# Addendum de progression EX11 — 2026-11-03 12:49 UTC

## REPLICA-U v004

- Runner actif : PID 11597 ; registre append-only `logs/append_only/replica_u_campaign_v004.jsonl`.
- Plan complet : 13 jeux × 5 graines = 65 blocs, cinq folds OOF et refit final sur tout le train extérieur.
- 31/65 blocs terminés `COMPLETED_VALIDATION_ONLY`, sans échec explicite ; les 31 rapports passent l'audit indépendant v002.
- Couverture : German Credit 5/5, Spambase 5/5, Tic-Tac-Toe 5/5, GINA 5/5, KC1 5/5, KC2 5/5, PC1 1/5 ; six jeux restent à démarrer.
- Aucun holdout tabulaire scellé n'est lu.

### Log-loss validation moyenne (graines terminées)

| Dataset | n | Backbone | Teacher | Student64/32 | Student32/16 | MLP matched64/32 | MLP GE4X |
|---|---:|---:|---:|---:|---:|---:|---:|
| German Credit | 5 | 0.52306 | 0.55872 | 0.51119 | 0.51387 | 0.50785 | 0.50998 |
| Spambase | 5 | 0.19504 | 0.19294 | 0.17418 | 0.17881 | 0.17918 | 0.18193 |
| Tic-Tac-Toe | 5 | 0.08390 | 0.08178 | 0.06520 | 0.06486 | 0.04894 | 0.04853 |
| GINA | 5 | 0.25878 | 0.32793 | 0.26072 | 0.26681 | 0.24925 | 0.25246 |
| KC1 | 5 | 0.36716 | 0.36788 | 0.34818 | 0.34726 | 0.34588 | 0.34954 |
| KC2 | 5 | 0.41140 | 0.42133 | 0.36646 | 0.36428 | 0.36426 | 0.36456 |
| PC1 | 1 | métriques disponibles dans `RAPPORT_EX11_ETAT_EXPERIMENTAL.md` ; une seed, pas de moyenne interprétable | | | | | |

### Statistiques appariées

Le fichier `reports/REPLICA_U_PAIRED_STATS_V004.md` contient les différences par graine et les IC t bilatéraux non ajustés. Conclusions robustes aux seules données terminées :

- Spambase : student64 bat le backbone sur 5/5 graines ; différence moyenne −0.02086, IC95% [−0.03516 ; −0.00656]. Face au MLP apparié, l'écart moyen est −0.00500, mais l'IC95% [−0.01667 ; 0.00667] contient zéro.
- Tic-Tac-Toe : le MLP apparié bat le student64 sur 5/5 graines ; différence student−MLP +0.01626, IC95% [0.00437 ; 0.02815].
- GINA : le teacher est moins bon que le backbone sur 5/5 graines ; différence moyenne +0.06915, IC95% [0.04238 ; 0.09592].
- German Credit, KC1 et KC2 : les IC student−MLP contiennent zéro ; aucun avantage stable du student sur le MLP apparié n'est établi.

Les IC sont descriptifs (n=5), par jeu, sans correction de multiplicité ; ils n'autorisent pas à généraliser entre jeux.

### Coût d'entraînement

Les ratios appariés (moyenne par graine de student64/MLP matched64) sont supérieurs à 1 sur tous les jeux complets : German Credit 1.63×, Spambase 3.63×, Tic-Tac-Toe 1.36×, GINA 4.65×, KC1 1.57×, KC2 1.06×. Le student est donc plus lent à entraîner que le MLP apparié dans les six jeux terminés. Ce calcul ne comprend pas le coût OOF total ; le coût total REPLICA est séparément enregistré. Latence d'inférence REPLICA : pas encore mesurée dans cette campagne.

## Autres branches et preuves déjà acquises

- REPLICA-U v003 : 65/65 complet, mais exploratoire (refit final pas sur tout le train externe).
- CNG v001 : 18 runs audités, exploratoires (centres non-KMeans) ; CNG v004/LOO v004 : aucune exécution confirmatoire enregistrée.
- CNC v003 un seed exploratoire ; CNC v004 un seed KMeans train-only mais non apparié en ordre de batch ; CNC v005 apparié préparé mais non exécuté.
- D3Q v001 160/160, exploratoire (KMeans/GE4X/chronométrie non conformes) ; D3Q v004 corrigé non exécuté.
- D1/D2 : 40/40 équivalences sortie/gradient sous 1e-6 ; microbenchmark mono-thread pré-campagne : D2 1.75–4.04× plus rapide en forward, 1.97–3.21× en train-step.

## Intégrité et phases

- 13 ARFF identiques à l'archive ; 130 train/validation + 65 holdouts = 195 CSV vérifiés ; holdouts `0440`.
- Prompt v2.3.1-reconstructed synchronisé ; audit prompt 13/13 ; tests logiciels 24/24 PASS.
- P0/P1/P2 fermées ; P3 en cours ; P4 non commencée/interdite ; P5 snapshot packagé mais archive finale doit être régénérée après stabilisation.
- Énergie `NOT MEASURED`; RSS high-water partagé, non attribuable aux variantes.
