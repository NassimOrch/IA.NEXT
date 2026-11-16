# Rapport P2 — vérification logicielle et compilation avant entraînement

## 1. Description
Vérification de l'état expérimental avant toute initialisation de paramètres conditionnels. Cette opération ne génère aucune réponse et n'entraîne aucun modèle.

## 2. Architecture vérifiée
Runtime eSonde v7 (base v6, contexte, observations causales 16D, adaptation Obsiss 64D/130D), transducteur GRU conditionnel préparé, outil d'entraînement situé dans Amodel.

## 3. Pipeline complet
1. Lecture des modules runtime et tests.
2. Exécution de toute la suite unitaire.
3. Compilation bytecode des modules, tests et outil d'entraînement.
4. Compilation LaTeX des quatre documents en mode arrêt sur erreur.
5. Contrôle d'empreinte du checkpoint V6 original.

## 4. Commandes d'exécution
```bash
cd Dmodel_eSonde_v7
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src tests ../Amodel_eSonde_v7/tools/train_conditional_obsiss.py
cd ../Amodel_eSonde_v7/formalism
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/esonde_v7_texcheck formalisme_eSonde_v7.tex
```
Les trois autres fichiers TeX ont été compilés par la même commande.

## 5. Résultats
- Tests : **43 passés, 0 échec, 0 erreur** (durée indiquée par unittest : 1,977 s).
- `compileall` : PASS.
- Quatre documents TeX : PASS avec `-halt-on-error`.
- SHA-256 checkpoint V6 : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`.
- Aucun entraînement ni chat conditionnel exécuté.

## 6. Interprétation
Le contrat logiciel de la projection 130D, du repli binary16, des observations causales, du panel sentinelle et du pas GRU pur Python est couvert par les tests présents. Les tests ne mesurent ni la qualité des réponses ni la généralisation.

## 7. Conséquences
- Théoriques : aucune conclusion sur la capacité conversationnelle.
- Conceptuelles : la variante 130D reste une hypothèse comparée à l'agrégat 64D.
- Opérationnelles : le code peut passer au préflight P2 et à l'entraînement expérimental sauvegardé.

## 8. Conclusion
Vérifications pré-entraînement réussies.

## 9. Statut du modèle
`SOFTWARE_VERIFIED_TRAINING_NOT_STARTED`; P2 reste `IN_PROGRESS`.

SHA-256 du journal : `3125ccf70637bdabad3dfa6cd02d6dde7d0410a4fdf04dc1045875ef65ac0c99`.
