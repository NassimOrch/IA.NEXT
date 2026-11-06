# B10/B11 — récupération historique et réplication EX9

## Résultats historiques EX8

B10 et B11 sont deux candidates sérieuses. Sur le Wisconsin de développement EX8, B10 a une log-loss moyenne de 0,04138964 et B11 de 0,04442526, sur les mêmes cinq graines. B10 bat son MLP apparié et son MLP ≥4× sur 5/5 graines ; B11 bat aussi ses comparateurs propres sur 5/5 graines. La différence B10−B11 est de −0,003036 en moyenne, mais les IC apparié et bootstrap imbriqué incluent zéro et le test exact bilatéral de signes donne p=0,0625. Ce sont des résultats de développement historiques, non une confirmation indépendante.

Le backbone partagé est cinq AdaptiveRBF parallèles (`d=4`, `K=4`, 20 évaluations RBF par exemple). B10 utilise deux signaux (marge et désaccord), seuils train-OOF, memberships floues 3×3, table 9×5 et softmax de lignes pour combiner les cinq logits. La table ne décide pas de la classe. B11 utilise un gate softmax standard sur les mêmes cinq sondes. EX8 rapporte P_total 884/835 et latence p50 batch 1 approximative 0,332/0,116 ms pour B10/B11 : B10 est 2,85× plus lent. Les codes, prédictions, checkpoints, histories, configs, manifestes et résultats sont récupérés dans les sources et leurs hashes sont contrôlés ; aucun de ces artefacts historiques n'est copié dans ce workspace.

## Réplication synthétique EX9 (`xor8`, développement)

| Candidate | LL | MLP apparié | MLP ≥4× | Gagnant vs MLP apparié |
|---|---:|---:|---:|---:|
| B10 | 0,549981 | 0,314458 | 0,300874 | 0/5 |
| B11 | 0,554089 | 0,306784 | 0,301720 | 0/5 |

Sur ce générateur synthétique précis, les deux candidates perdent nettement face aux MLP. B10 possède 400 paramètres persistants contre 1 602 pour MLP_GE4X ; B11 351 contre 1 404. Le seuil 4× est respecté, mais la qualité n'est pas conservée. Les temps de fit E2E moyens des candidates sont B10 1,251 s, B11 0,712 s ; p50 E2E batch1 0,408 ms et 0,233 ms. Les MLP ont p50 E2E autour de 0,017–0,018 ms. L'objectif ressources/vitesse n'est donc pas démontré par cette réimplémentation sur xor8.

## Conclusion

L'indice positif historique Wisconsin mérite réplication sur des domaines réels neufs ; le pilote xor8 ne le reproduit pas. Il ne prouve pas que B10/B11 sont mauvais dans tous les contextes, mais interdit la conclusion d'une amélioration générale. La priorité expérimentale est d'isoler pourquoi le backbone est si lent en petit batch et de tester la robustesse du gate/action sur données indépendantes, sans sélectionner les seuils sur le holdout.


## Réserve OOF de la réplication EX9

Les gradients/probes sont shardés par owner et la loss du gate/action masque bien la sonde propriétaire. Cependant, le constructeur `ProbeBank(X, ...)` initialise les centres KMeans à partir de l'ensemble des `X_train`, sans labels, avant les mises à jour supervisées de chaque shard. C'est `transductive_train_X` (pas une fuite des labels), et non un cross-fit complètement fold-pure des caractéristiques. Cette exception est visible dans le `fit_record` de chaque JSON. Une ablation KMeans strictement shard-train-only reste à exécuter ; sans elle, B10/B11 ne doivent pas être décrits comme strictement inductifs au niveau des features d'initialisation.


## Ablations B10 supplémentaires (EX9, 35 runs)

Un lot séparé de 35 ablations (7 variantes × 5 graines) a été exécuté après la campagne principale, à backbone B10 gelé, sur la même validation `xor8` déjà utilisée. L'audit indépendant passe pour 35/35 checkpoints et prédictions (écarts de recalcul nuls). La variante marge seule (sans signal de désaccord) obtient une log-loss moyenne 0,544668 contre 0,549981 pour B10 parent et gagne sur 5/5 graines modèle ; la factorisation 3+3 donne 0,544697 (4/5), et le hard codebook 2×2 présente la meilleure latence p50 batch1 (0,3258 ms contre 0,4076 ms parent). Tous restent à une log-loss >0,54 et sont largement derrière les MLP du même domaine (~0,30). Le split est réutilisé et sert à sélectionner le meilleur epoch : ces ablations sont exploratoires, pas confirmatoires. Voir `REPORT_B10_ABLATIONS_EX9.md`, le registre dédié et les 35 artefacts bruts.


## Réplication synthétique multi-domaines scorée

Les domaines additionnels pré-déclarés `concentric2` et `rotated_moons2` ont chacun 5 seeds B10/B11, MLP appariés et MLP_GE4X. Les tests (1 200 lignes chacun) ont été ouverts une seule fois sous un verrou séparé.

| Domaine | B10 test | B10 MLP apparié / GE4X | B11 test | B11 MLP apparié / GE4X |
|---|---:|---:|---:|---:|
| concentric2 | 0,255830 | 0,063186 / 0,059463 | 0,255024 | 0,064854 / 0,058597 |
| rotated_moons2 | 0,256111 | 0,122245 / 0,121291 | 0,255320 | 0,122342 / 0,121378 |

B10 et B11 perdent face à leurs deux MLP sur 5/5 seeds dans les deux domaines. Les CIs bootstrap appariés sur seeds et observations sont entièrement positifs ; la différence B10/B11 historique Wisconsin ne constitue donc pas une généralisation de performance. Les sondes ont un `P_total` inférieur au MLP_GE4X mais une latence CPU batch1 d'environ 12–22× plus élevée que le MLP apparié dans ces domaines. Voir `SYNTHETIC_CONFIRMATION_EX9.md` et `MULTI_DOMAIN_SYNTH_DEV_REPORT.md`.
