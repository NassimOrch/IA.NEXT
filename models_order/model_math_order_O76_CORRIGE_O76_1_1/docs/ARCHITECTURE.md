# Architecture O76

`contract.py` normalise et hache le problème. `fingerprint.py` construit la distinction structurelle et ordonne les trajectoires. `solver.py` génère des objets mathématiques et des certificats. `proof.py` formalise ces certificats. `verifier.py` reconstruit les objets depuis le texte et rejoue les identités indépendamment. `memory.py` conserve une mémoire non-oraculaire par hash/provenance. `checkpoint.py` persiste les fronts lourds. `engine.py` ferme la boucle observation → trajectoire → preuve → rejeu → mémoire.

Le coeur émergent n'est pas une pondération statistique : c'est la capacité du système à réorganiser son portefeuille à partir de l'empreinte et de son expérience. La mémoire peut seulement favoriser une stratégie ou pénaliser une voie déjà coûteuse ; elle ne fournit jamais le résultat mathématique et n'évite jamais le rejeu du certificat.
