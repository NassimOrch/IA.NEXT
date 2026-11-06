# Analyse ressources — EX8 v010

## Environnement

Exécution CPU-only : Python 3.13.5, PyTorch 2.10.0+cpu, NumPy 2.3.5, scikit-learn 1.8.0, SciPy 1.17.0 ; 3 cœurs logiques, RAM installée 6,24 Go. Aucun GPU/VRAM. Énergie non mesurée.

Latences mesurées avec 30 warm-ups et 200 répétitions aux batchs 1/16/64/256 ; p50/p95/p99 et débit sont dans `V010_LATENCY_PAIRED_PER_RUN.csv` et `V010_LATENCY_PAIRED_SUMMARY.csv`. Les temps sont ceux du chemin modèle sur features déjà préparées ; les scalers/prétraitements externes ne sont pas tous inclus.

## PCA et opérations RBF

A0/A4 : 56 évaluations de centres RBF par observation, batch1 p50 ≈0,203/0,202 ms. A1/A2/A3 : 16 évaluations, ≈0,169–0,172 ms. Réduire RBF accélère modérément le modèle, mais dégrade la log-loss. Le temps fit A0/A4 enregistré par le script local omettait le fit du global historique réutilisé ; le temps end-to-end corrigé du tableau ressources ajoute la durée de ce stage global et doit être préféré pour comparer les durées.

## Récursion et coûts structurels

V004 full : 35 probes, 5 niveaux, K8 = 280 évaluations de centres par observation, batch1 p50 historique autour de 1,1 ms sur v001. Dans v010 : B3 = 15 probes/5 niveaux/120 évaluations, p50 0,789 ms ; B4 = 15 probes/3 niveaux/120 évaluations, p50 0,476 ms ; B5 = 15 probes/5 niveaux/K4/60 évaluations, p50 0,619 ms. Réduire le nombre de niveaux diminue la latence sérielle ; réduire K diminue les évaluations RBF. Ces axes ne sont pas interchangeables.

B8 sur le full 35/5 reste à 280 centres et atteint 1,724 ms ; la coordination ne remplace pas les calculs de probes. B10/B11 à cinq probes parallèles n’évaluent que 20 centres et une couche : B11 p50 0,116 ms ; B10 0,332 ms. Le calcul des appartenances floues et du lookup B10 ajoute du temps, ce qui établit que la table n’est pas un accélérateur sur ce test.

## Fit, paramètres, stockage

Les tableaux `V010_ARM_RESOURCE_QUALITY_SUMMARY.csv` reportent P_total, paramètres appariés, temps de fit, bytes checkpoint, nombre de centres et latence p50/p95. Les temps OOF/correcteurs sont comptés dans les estimations end-to-end, les stages partagés A0/A4 sont explicitement corrigés.

Les FLOPs/MACs exacts, le coût énergétique et le RSS processus complet incluant toutes activations/optimiseurs ne sont pas mesurés de façon robuste. Le nombre d’évaluations de centres est un proxy structurel, pas un comptage complet d’opérations. Ne pas lire cette campagne comme une étude complète de consommation mémoire/énergie.
