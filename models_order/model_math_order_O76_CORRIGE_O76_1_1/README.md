# MODEL mathématique O76 — version corrigée O76-1.1

O76 est un moteur mathématique exact orienté preuve. Il n'utilise ni modèle de langage, ni oracle de benchmark, ni solveur symbolique externe dans son chemin de décision. La production d'un statut `PROVEN` ou `REFUTED` exige un certificat rejouable par un vérificateur indépendant.

## Exécution en une commande

```bash
python3 run_math_O76.py examples/prove_groebner.json
```

Sous Windows :

```text
py run_math_O76.py examples/prove_groebner.json
```

Le fichier de configuration `config/o76.json` permet de régler temps, nombre de trajectoires, paires Buchberger, cas d'énumération, mémoire et stratégie. Les mêmes paramètres sont surchargeables par la ligne de commande.

## Contrat de sortie

- `PROVEN` : certificat présent et accepté par le vérificateur exact.
- `REFUTED` : contre-certificat exact, par exemple contre-exemple exhaustif ou contre-modèle propositionnel.
- `UNRESOLVED` : aucune conclusion certifiée n'a été obtenue dans le portefeuille et les ressources déclarées. Ce statut ne signifie pas « impossible ».

## Familles natives

Arithmétique rationnelle exacte; identités polynomiales; conséquences linéaires; systèmes linéaires; idéaux polynomiaux avec Buchberger et certificat d'identité explicite; tours polynomiales triangulaires avec contradiction exacte; racines univariées rationnelles et réelles par Sturm; matrices sur Q; équations diophantiennes linéaires; CRT; Pell x^2-D y^2=1; logique propositionnelle; énumération exacte de domaines finis.

## Architecture émergente

Le noyau applique une boucle observée et récursive : empreinte structurelle → portefeuille de trajectoires → transformation exacte → certificat → vérification indépendante → mémoire évolutive de faits/échecs → nouvelle sélection. La théorie des empreintes sert à observer et ordonner; elle n'est jamais un oracle de réponse.

## Ce que signifie « preuve »

La garantie est opérationnelle et rejouable : le vérificateur recalcule l'objet mathématique et l'identité du certificat. Le runtime Python et le code du vérificateur constituent toutefois la base de confiance; O76 n'est pas lui-même une implémentation formellement vérifiée dans Lean/Coq/Isabelle.

## Correction O76-1.1 et test décisif

Les corrections décisives et de régression observées pendant le test externe ont été intégrées :

1. `TRIANGULAR_TOWER_EXACT` ajoute une preuve algébrique exacte par élimination arrière pour toute tour structurelle `x1^k-c=0`, `x(i+1)^k-xi=0`, `xn-r=0`, sans dépendre de la réussite de Buchberger. Les coefficients du certificat sont rejoués indépendamment.
2. `UNSUPPORTED_FORM` valide la relation entière avant de l'accepter comme mathématique : une prose contenant des signes `=` internes, comme l'énoncé de Collatz, reste hors contrat. Les `UNRESOLVED` portent maintenant les stratégies tentées et la raison `portfolio_exhausted` lorsque le portefeuille ne conclut pas.

Sur l'instance de stress profondeur 12, la version O76-1.0 n'a pas produit de certificat dans le délai de l'expérience et a dépassé le watchdog externe; O76-1.1 produit un certificat `TRIANGULAR_TOWER_CONTRADICTION` vérifié indépendamment en environ 1 seconde sur la machine de test.

Les problèmes ouverts Riemann/Collatz restent `UNRESOLVED`/`UNSUPPORTED_FORM` : le modèle ne transforme pas une question mathématique ouverte en pseudo-preuve.

La procédure complète et les résultats détaillés sont dans `rapport_experience_decisive_O76.tex`.
