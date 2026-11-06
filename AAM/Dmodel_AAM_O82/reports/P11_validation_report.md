# AAM O82 — Rapport P11 Validation adverse et ablations

## Description
Validation des contrats et observations malformés, recovery après corruption, contrôle de policy, teacher cutover et ablations mémoire/fingerprint/hiérarchie.

## Architecture
Les contrôles réutilisent les mêmes contrats, probes, mémoire, verifier et Engine que le runtime. Les jeux de contrôle sont générés localement et n'injectent aucune règle de domaine dans le noyau.

## Pipeline complet
`fuzz -> corruption -> adaptive/random control -> memory ablation -> fingerprint ablation -> hierarchy ablation -> teacher cutover -> aggregate gate`.

## Commandes d'exécution
```bash
PYTHONPATH=src python scripts/validate_o82.py
PYTHONPATH=src python -m unittest tests.test_validation -v
```

## Résultats
Le gate P11 a atteint 45/45 tests `PASS`. Les contrôles ont confirmé le rejet des entrées invalides, la détection/récupération d'une corruption, l'utilisation de la policy adaptative sous son contrat de score, l'effet de la mémoire quotient, l'effet du retrieval par sous-empreinte, l'adressabilité hiérarchique et le blocage du teacher en `FINAL`.
