# EX7 V003 — OuterCoord-Lite-7x1

Cette version teste une architecture simplifiée à sept `AdaptiveRBF` indépendantes et un coordinateur externe `rho` unique. Elle retire les sept gates internes et la cascade 7×5 d'Orchestra Org. Tous les résultats négatifs et limites sont conservés.

## Résultat clé

- Paramètres persistants : 1 341 (contre 6 712 pour Orchestra 7×5).
- Moyenne cinq seeds : accuracy 97,88 %, macro precision 97,34 %, log-loss 0,06806.
- MLP apparié : 98,12 % accuracy, log-loss 0,05136 ; MLP-ge4x : 98,59 %, log-loss 0,05222.
- Latence raw-end-to-end p50 batch 1 : 0,290 ms V003, 1,490 ms Orchestra outer-only, 0,025 ms MLP matched.
- Verdict : gain structurel et contre Orchestra, mais pas de supériorité globale ; marges de log-loss non respectées et inférence plus lente que les MLP.

## Reproduction

Depuis la racine du projet, dans un environnement compatible décrit par `configs/ENVIRONMENT_V003.json` :

```bash
python src/run_outercoord_lite_v003.py
python src/profile_end_to_end_v003.py
python src/audit_v003.py
```

`run_outercoord_lite_v003.py` entraîne la candidate et les deux MLP pour les cinq seeds, vérifie les références, profile le modèle seul et consolide les tableaux. Le profil raw-end-to-end inclut le scaler. Les runs existants ne sont pas écrasés : ils sont réutilisés après contrôle de leur hash.

## Principaux dossiers

- `inputs/` : prompt, données dev-only et références V002 compactes immuables.
- `configs/` : pré-enregistrement, configuration parent, environnement.
- `src/` : entraînement, inférence, profilage, parité et audit indépendant.
- `results/raw/` : prédictions, résultats par seed, historiques.
- `results/models/` : checkpoints et état d'optimiseur.
- `results/metrics/` : agrégats, différences appariées, latence brute et métriques.
- `reports/` : rapports de performance, protocole, conformité, anomalies et audit.
- `logs/` : sorties/stdout/stderr originaux, y compris l'anomalie de consolidation.
- `checksums/` : manifestes finaux SHA-256.

## Limites essentielles

Wisconsin est un split de développement historiquement exposé, non une validation externe vierge. Le test externe n'a pas été ouvert. Les 57 lignes d'adaptation n'ont pas été utilisées. Temps complet d'initialisation/training, RAM isolée comparable, FLOP complets et énergie sont `NON MESURÉ`. Le verdict est développement uniquement.
