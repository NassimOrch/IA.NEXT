# Guide utilisateur O76

Lancez une démonstration :

```bash
python3 run_math_O76.py examples/prove_groebner.json
```

Un fichier JSON utilisateur suit le même contrat que les exemples. Le champ `mode` choisit la famille ; `variables`, `assumptions`, `equations`, `target`, `domains`, `matrix`, `definitions` et `congruences` sont ensuite validés selon la famille.

Les sorties `PROVEN` et `REFUTED` contiennent un certificat et une section `verification`. `UNRESOLVED` signifie uniquement qu'aucun certificat n'a été obtenu dans le portefeuille et les ressources du run.

Ressources :

```bash
python3 run_math_O76.py probleme.json --time 600 --max-steps 100 --max-gb-pairs 100000
```

Les checkpoints sont automatiquement associés au hash du problème. Une mutation de l'entrée empêche la restauration d'un ancien état.
