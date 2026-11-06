# Statut actuel du test synthétique `xor8`

`PRE_TEST_REPORT.md` est un snapshot historique rédigé avant l'essai d'ouverture. Après ce snapshot, `score_sealed_test.py` a créé `SEALED_TEST_OPENED.json`, généré les labels test en mémoire, puis échoué lors du chargement du premier checkpoint (`__main__.MLP`) avant toute prédiction.

Conséquence : le holdout est classé **consommé/compromis et non scoré**. Il n'est ni rouvert, ni rescorré avec le correctif de désérialisation. `SEALED_TEST_FAILURE.json` documente la cause, et `src/score_sealed_test_v2_UNEXECUTED.py` est un correctif conservé comme référence mais refuse explicitement d'exécuter l'ancien test.

Le champ `test_opened:false` dans `MODEL_LOCK.json` est une photographie immuable de l'état au moment du gel pré-ouverture ; il n'est pas un état actuel. Le statut postérieur prévaut pour toute interprétation : `OPENED_BUT_NOT_SCORED`.

Aucune métrique test, prédiction test, ni revendication confirmatoire n'existe pour `xor8`.
