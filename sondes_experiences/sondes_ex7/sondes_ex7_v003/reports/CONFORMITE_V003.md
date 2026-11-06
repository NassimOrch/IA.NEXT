# Matrice de conformité EX7 — V003

| Exigence | Statut | Preuve / remarque |
|---|---|---|
| Pré-enregistrement avant entraînement | PASS | `configs/PRE_REGISTRATION_V003.*` |
| Cinq seeds gelées | PASS | 1501, 1607, 1717, 2029, 3037 |
| Même train/validation pour les bras | PASS | NPZ de développement, hash vérifié |
| Aucune donnée test chargée/ouvert | PASS | NPZ absent de arrays test, scripts lisent seulement Xtr/ytr/Xva/yva/scaler ; flags test_opened=false |
| Split adaptation documenté | PASS | 57 lignes, non utilisées explicitement |
| Shards locaux stratifiés et disjoints | PASS | code vérifie partition complète/disjointe par probe |
| Objectif gate à logits détachés | PASS | code candidate ; mise à jour rho distincte |
| MLP matched | PASS | 1 349 paramètres totaux, cinq seeds |
| MLP-ge4x | PASS | 5 375 / 1 341 = 4,008×, vérifié par seed |
| Références historiques exactes | PASS | dix checkpoint/predictions hashes validés |
| Métriques réévaluées | PASS | audit indépendant et comparatif par graine |
| Paramètres complets incluant scaler | PASS | `P_total` ajoute 60 coeffs de StandardScaler |
| Latence batch 1/16/64/256 | PASS | 100 profils pour chaque scope ; 30 warmups, 200 répétitions |
| Latence raw end-to-end | PASS | scaler inclus, IO fichiers exclu ; résultats dédiés |
| Temps entraînement complet bout en bout | NON MESURÉ | seul fit loop chronométré, après initialisation |
| Temps d'initialisation / KMeans | NON MESURÉ | à mesurer dans une future itération |
| MAC/FLOP complets | NON MESURÉ | proxy MAC linéaire seulement, ops RBF non incluses |
| Peak RAM isolée comparable | NON MESURÉ | RSS process partagé non comparable |
| Énergie | NON MESURÉ | aucun instrument fiable dans l'environnement |
| Domaines externes vierges | NON EXÉCUTÉ | Wisconsin historiquement exposé ; pas de domaine externe ouvert |
| Audit indépendant | PASS | 91 contrôles sur 91 |
| Archive ZIP CRC | À exécuter au scellement | voir manifeste de livraison après création |

## Verdict

**Pas de succès global EX7.** Les gains de taille et de latence face à Orchestra sont réels, mais V003 ne respecte pas la marge de log-loss et reste plus lente que les MLP en inférence. Les dimensions ressources non mesurées et l'absence de validation externe interdisent également un verdict global positif.
