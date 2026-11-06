# Historique de validation — sav_ng_0

- Le test V1 a d'abord été lancé sans `PYTHONPATH=src` depuis le répertoire historique : import error `ModuleNotFoundError: ngegenbrain`; ce lancement est conservé comme erreur de configuration.
- Relance corrigée : `PYTHONPATH=src PYTHONWARNINGS=error::ResourceWarning python -m unittest discover -s tests -v` depuis `legacy_NGeGenBrain_v1/` : 65 tests réussis.
- Deux exécutions du validateur monolithique ont dépassé le budget de temps de l'outil avant d'écrire un reçu exploitable. Elles ne sont pas comptées comme des résultats de tests et ne sont pas interprétées comme échec du modèle.
- Les tests V2, les tests V1, la compilation, LaTeX et les commandes CLI ont ensuite été effectués séparément avec journaux distincts.
