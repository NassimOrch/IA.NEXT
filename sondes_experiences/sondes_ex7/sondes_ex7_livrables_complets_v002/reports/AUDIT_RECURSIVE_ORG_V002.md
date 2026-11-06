# Audit de la version récursive originale — EX7 V002

## Verdict d'exécution

**Oui : la variante récursive originale « Emplica Orchestra Org » est implémentée et exécutée.** Elle n'est pas restée au stade « structuré l'architecture et l'expérience ». Les éléments sont présents dans le code, les checkpoints, les runs et les audits. La complétude d'exécution de cette branche ne signifie toutefois pas que ses objectifs de qualité et de vitesse sont atteints.

## Architecture observée dans le code

Script de référence : `src/run_orchestra_org_recursive.py`.

- 7 couches × 5 probes = 35 probes.
- Composition adaptive/fixe : `5/0`, `1/4`, `1/4`, `4/1`, `3/2`, `1/4`, `3/2` (18 probes adaptatives, 17 fixes).
- Chaque probe possède ses paramètres et son optimisation locale.
- Au niveau couche : `pi_l = softmax(phi_l)` coordonne les probes, avec état et objectif de coordination distincts.
- Au niveau ensemble : `rho = softmax(Psi)` coordonne les couches avec un état/objectif distinct.
- Les couches reçoivent la représentation de cascade constituée de l'entrée initiale et des sorties précédentes.
- Les objectifs de coordination utilisent les sorties locales détachées ; les mises à jour globales ne rétropropagent pas dans les probes locales.
- Les coordinateurs ont des optimiseurs séparés ; leur mise à jour est espacée de cinq époques.
- La modulation locale du learning rate suit l'extension EX7 `eta0 × (0.5 + 5 × pi_lj) × (0.5 + 7 × rho_l)`.

La formule source historique avait été décrite pour N=4 probes. Son extension à N=5 et à L=7 est enregistrée comme variante EX7, pas comme un résultat déjà validé par les sources historiques.

## Campagne réellement terminée

| Élément | Réalisé |
|---|---:|
| Entraînements racine, graines 1501/1607/1717/2029/3037 | 5/5 |
| Campagnes OOF | 5/5 graines |
| Fits de folds OOF | 15/15 (3 par graine) |
| Correcteurs OOF racine | 15/15 (3 types × 5 graines) |
| Correcteurs sur sorties d'étages | 10/10 (2 types × 5 graines) |
| Ablations causales | 30/30 (6 types × 5 graines) |
| Contrôle couches indépendantes unique | 5/5 |
| Variantes capacité/profondeur | 25/25 |
| Variantes correcteurs structurels | 60/60 |

Le compteur historique ambigu de 20 entrées (5 fits racine + 15 fits OOF) est corrigé par les tableaux séparés `EX7_ORCHESTRA_ORG_ROOT_SEEDS_ONLY.csv` et `EX7_ORCHESTRA_ORG_OOF_FOLD_MODELS_ONLY.csv`. Il ne faut pas lire ce compteur comme 20 graines principales.

## Qualité et coût — résultats importants

| Modèle / correcteur | Paramètres moyens | Accuracy | Log-loss | Pipeline complet estimé | MLP apparié |
|---|---:|---:|---:|---:|---:|
| Org base seul | 6712 | 98.35% | 0.06187 | 5.92 s | 0.401 s |
| Org OOF temp-bias | 6715 | 98.35% | 0.06195 | 21.86 s | 0.401 s |
| Org OOF lin-context | 6778 | 98.12% | 0.05765 | 21.92 s | 0.401 s |
| Org OOF RBF-Lite 1 probe | 6800 | 97.88% | 0.05535 | 21.99 s | 0.401 s |

Le comparateur MLP est apparié par graine, avec 27 221 paramètres. Les rapports des sorties d'étages et des ablations sont également comparés dans les nouveaux fichiers `EX7_ORCHESTRA_ORG_STAGE_OOF_MLP_COMPARISONS_*` et `EX7_ORCHESTRA_ORG_ABLATIONS_MLP_COMPARISONS_*`.

## Parité et intégrité

- Parité calcul vectorisé vs boucle de référence : écart maximal rapporté `4.77e-7`.
- La couverture OOF est vérifiée : chaque ligne train reçoit exactement une prédiction dans chacun des 3 folds, indices et hashes conformes.
- Checkpoints racine, folds, correcteurs et variantes de capacité/structure sont chargeables et les métriques des prédictions racine sont recalculables.
- Audit machine associé : `results/metrics/EX7_RECURSIVE_VARIANTS_AUDIT.json`.

## Ce qui reste non démontré

L'Org récursive n'a pas atteint la qualité des deux correcteurs OOF de référence EX6 (0.03637 Emplica, 0.03982 Orchestra). Son RBF-Lite récursif donne environ 0.05535 de log-loss. Le pipeline OOF reconstruit est de l'ordre de 22 secondes, face à environ 0.40 seconde pour le MLP comparateur. Le parallélisme naïf CPU mesuré n'accélère pas les folds ni les couches. L'énergie, la mémoire d'activation/DRAM et la confirmation externe restent non mesurées/indisponibles.

**Conclusion : branche récursive implémentée et expérimentalement complète ; succès qualité-vitesse-ressources non établi.**
