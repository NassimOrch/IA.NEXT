# Rapport Efficacité d’implémentation — EX11

## D1/D2 : équivalence numérique
- 40 cas (10 graines × 4 batchs) ; toutes les comparaisons passent.
- Erreur maximale sorties : 1.788e-07 ; gradient entrée : 3.725e-09 ; gradients paramètres : 2.980e-08.
- Tolérance : `1e-6`; script SHA-256 `101fabb31171eac724f95f8e2f6df9a0467cb74a3a1917ad9c9743cc7ebaddc0`.

## Microbenchmark initial — CPU mono-thread

| Batch | Paramètres D1/D2 | D1 forward p50 ms | D2 forward p50 ms | Gain D1/D2 | D1 train-step p50 ms | D2 train-step p50 ms | Gain train-step | D3 forward p50 ms | D3 paramètres |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 819 | 0.2487 | 0.0615 | 4.04× | 1.4207 | 0.4426 | 3.21× | 0.0514 | 411 |
| 16 | 819 | 0.2707 | 0.0761 | 3.56× | 1.4926 | 0.5105 | 2.92× | 0.0668 | 411 |
| 64 | 819 | 0.3357 | 0.1207 | 2.78× | 1.7030 | 0.6662 | 2.56× | 0.1023 | 411 |
| 256 | 819 | 0.5889 | 0.3366 | 1.75× | 2.1799 | 1.1069 | 1.97× | 0.2259 | 411 |

## Interprétation

- D1 et D2 ont exactement les mêmes 819 paramètres ; leur équivalence sorties/gradients a été démontrée à la tolérance préenregistrée.
- D2 réduit le p50 forward d’environ 4,0× pour batch 1, 3,6× pour batch 16, 2,8× pour batch 64 et 1,75× pour batch 256 dans ce microbenchmark.
- Le train-step est environ 3,2×, 2,9×, 2,6× et 2,0× plus rapide respectivement dans ces conditions.
- D3 a 411 paramètres contre 819 (environ 50 % de moins), mais c’est une architecture différente : l’équivalence ne s’applique pas, et sa précision doit être jugée sur les runs D3Q v004 qui ne sont pas encore réalisés.
- Les mesures RSS sont le high-water mark cumulatif du processus et ne permettent pas une attribution par variante. Aucun wattmètre/compteur d’énergie fiable n’est disponible : énergie `NOT_MEASURED`.

## Qualité D3Q
- D3Q v001 : 160/160 runs persistés et réconciliés, mais exploratoires (centres non KMeans, GE4X insuffisant pour certaines variantes, timings sous contention).
- D3Q v004 (KMeans train-only, GE4X ≥4× plus grande sonde, mêmes ordres de batchs) : non démarré à ce snapshot.
