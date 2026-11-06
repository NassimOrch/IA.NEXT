# Expérience : réseau neuronal vs sondes adaptatives

## Contenu

- `rapport_experience_sondes_adaptatives.pdf` : rapport de résultats.
- `rapport_experience_sondes_adaptatives.tex` : source LaTeX du rapport.
- `experience_sondes_adaptatives.py` : expérience entièrement reproductible.
- `resultats_experience_sondes.csv` : métriques de chaque modèle et de chaque initialisation.
- `synthese_experience_sondes.json` : paramètres du protocole et statistiques récapitulatives.
- `frontieres_decision_sondes.png` : figure des frontières de décision.

## Réexécution

Dépendances : Python 3, `numpy`, `torch`, `scikit-learn`, `matplotlib`.

```bash
python experience_sondes_adaptatives.py
```

Le script réutilise les graines inscrites dans le code et écrit le CSV, le JSON et le PNG dans le même dossier.

## Résumé

- Réseau neuronal MLP : 49 paramètres entraînables ; précision moyenne 95,870 %.
- Sondes radiales adaptatives : 49 paramètres entraînables ; précision moyenne 96,005 %.
- Sondes radiales fixes (ablation) : 13 paramètres entraînables ; précision moyenne 86,230 %.

Les résultats décrivent un banc d'essai synthétique (`two moons`) et ne sont pas une expérience de reconstruction d'un LLM. Les écarts-types rapportés concernent cinq initialisations du modèle sur un jeu de test fixe ; ils ne mesurent pas à eux seuls l'incertitude liée à toutes les données possibles. Les sondes adaptatives sont une architecture apprenable, apparentée aux réseaux à fonctions de base radiales : l'expérience ne prouve pas qu'une sonde est fondamentalement différente d'un neurone.
