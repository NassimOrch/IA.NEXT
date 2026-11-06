# EX9 v011 — réplication multi-domaines synthétiques (pré-test)

**Statut : 90 runs terminés ; audit validation PASS ; aucun holdout généré ou consulté à la rédaction de ce rapport.**

Cette cohorte complète les domaines `concentric2` et `rotated_moons2` déjà pré-déclarés. Elle n’est pas une confirmation sur données réelles externes. Chaque domaine possède un split train/validation fixe partagé par les cinq seeds de modèles ; les seeds mesurent la variabilité d’optimisation, pas cinq jeux indépendants.

## Protocole

- 600 train et 240 validation par domaine ; 5 seeds de modèle : 1501, 1607, 1717, 2029, 3037.
- Candidates B10, B11, A0 ; pour chacune MLP apparié et MLP_GE4X calculé sur P_total.
- Prétraitement StandardScaler ajusté sur train uniquement.
- B10/B11 partagent 5 sondes parallèles d4/K4 ; A0 est PCA/global/local avec OOF à 100 epochs fixes.
- 45 runs par domaine, 90 au total. JSON, checkpoint, config pour chaque run ; historiques MLP inclus.
- aucun seed test (61301 et 62301) généré à ce stade.

## Log-loss validation (moyenne sur seeds modèle ; écart-type entre seeds)

| Domaine | Candidat | Candidat | MLP apparié | MLP ≥4× | Wins candidat vs apparié / GE4X |
|---|---|---:|---:|---:|---:|
| concentric2 | B10 | 0.282177 (0.031692) | 0.045578 | 0.039877 | 0/5 ; 0/5 |
| concentric2 | B11 | 0.284219 (0.032037) | 0.046408 | 0.039040 | 0/5 ; 0/5 |
| concentric2 | A0 | 0.199706 (0.077495) | 0.039272 | 0.042231 | 0/5 ; 0/5 |
| rotated_moons2 | B10 | 0.293651 (0.040859) | 0.154635 | 0.153480 | 0/5 ; 0/5 |
| rotated_moons2 | B11 | 0.291933 (0.049205) | 0.154494 | 0.153687 | 0/5 ; 0/5 |
| rotated_moons2 | A0 | 0.269514 (0.072097) | 0.153671 | 0.153051 | 0/5 ; 0/5 |

Sur ces deux domaines, les candidates ne gagnent contre aucun des deux MLP sur aucune des cinq graines : 0/5 pour B10, B11 et A0, contre le MLP apparié comme contre le MLP_GE4X. Les tests de signes exacts calculés sur les cinq graines donnent p=0,0625 lorsqu’il n’y a pas de ties ; ils sont présentés comme descriptifs, car les graines partagent le même split.

## Paramètres, temps d’entraînement et latence

| Domaine | Candidat | P_total | Fit E2E candidat (s) | Fit MLP apparié (s) | p50 batch1 E2E candidat (ms) | p50 MLP apparié (ms) | Ralentissement inférence candidat |
|---|---|---:|---:|---:|---:|---:|---:|
| concentric2 | B10 | 268 | 2.623 | 2.308 | 0.3847 | 0.0171 | 22.5× |
| concentric2 | B11 | 219 | 2.011 | 2.284 | 0.2228 | 0.0170 | 13.1× |
| concentric2 | A0 | 554 | 3.178 | 2.290 | 0.3456 | 0.0171 | 20.3× |
| rotated_moons2 | B10 | 268 | 1.243 | 1.567 | 0.3669 | 0.0170 | 21.6× |
| rotated_moons2 | B11 | 219 | 1.005 | 1.478 | 0.2048 | 0.0169 | 12.1× |
| rotated_moons2 | A0 | 554 | 1.848 | 1.428 | 0.2911 | 0.0174 | 16.8× |

Le profil est CPU, warmup 20 et 40 répétitions par batch. La latence end-to-end inclut StandardScaler. La variabilité p95/p99 n’est pas suffisamment échantillonnée pour une conclusion de queue de distribution. La vitesse d’inférence PyTorch favorise ici très nettement les MLP. Le temps d’entraînement varie selon le domaine et la candidate ; il ne donne pas un avantage stable aux sondes.

## Mesure des ressources : portée et limites

- `P_total` inclut paramètres entraînables, buffers de modèle et scaler selon le même compteur que les comparateurs.
- Les MLP appariés sont proches de 1× la candidate ; les MLP_GE4X dépassent 4× P_total run par run.
- Les scripts conservent les proxies MAC structurels `mac_proxy_lower_bound_per_example` pour les candidates, mais ils excluent non-linéarités, exponentielles RBF, kernels distances, softmax et une partie de la coordination. Ils ne constituent pas un FLOPs/MAC complet comparable ; ils ne sont pas utilisés pour un verdict de ressources.
- FLOPs/MAC complet, RSS peak indépendant par run, énergie et consommation GPU restent non mesurés.
- Le profil CPU peut refléter l’overhead des petits kernels PyTorch ; il mesure néanmoins le code exécuté et ne justifie pas une affirmation sur une future implémentation optimisée.

## Intégrité

- `src/audit_multi_domain.py` : PASS sur 90/90 runs.
- Probabilités reconstruites depuis les checkpoints : différence maximale 0 ; log-loss recalculée : écart maximal 0.
- Scaler et matrices train/validation recalculés depuis les tableaux bruts archivés ; SHA-256 vérifiés.
- Checkpoints, JSON, configs, ratios GE4X et historiques MLP vérifiés.
- Aucun fichier de test ni seed test n’a été généré ou chargé dans cette phase.

## Conclusion

**Le signal Wisconsin historique EX8 ne se reproduit pas sur ces deux tâches synthétiques : B10/B11/A0 sont nettement moins bonnes en log-loss que les MLP et environ 12 à 22 fois plus lentes en inférence batch 1 dans ce profil CPU.** Les candidates gardent un `P_total` inférieur au MLP_GE4X, mais le critère de paramètres seuls est insuffisant : qualité et vitesse ne suivent pas. Aucune conclusion sur des données réelles externes n’est permise.

## Artefacts

- Registres : `results/processed/CONCENTRIC2_DEV_REGISTRY.csv`, `ROTATED_MOONS2_DEV_REGISTRY.csv`.
- Résumés : `results/processed/CONCENTRIC2_DEV_SUMMARY.json`, `ROTATED_MOONS2_DEV_SUMMARY.json`, `MULTI_DOMAIN_DEV_AGGREGATES.json`.
- Audit : `results/processed/MULTI_DOMAIN_INTEGRITY_AUDIT.json`.
- Données train/validation : `inputs/concentric2_dev_arrays.npz`, `inputs/rotated_moons2_dev_arrays.npz`.
- Pré-enregistrement : `inputs/PRE_REGISTRATION_MULTI_DOMAIN_DEV.md`; verrou protocolaire : `inputs/MULTI_DOMAIN_DEV_LOCK.json`.
- Script d’entraînement : `src/multi_domain_dev.py`; auditeur : `src/audit_multi_domain.py`.
