# Journal d'incidents d'exécution EX7

- **Correcteurs légers 3-fold** : une première invocation a atteint la limite de durée de l'environnement. Le script a été rendu reprenable avec conservation des résultats déjà écrits ; l'ensemble attendu a été complété (50 exécutions = 2 familles × 5 graines × 5 variantes). Les exécutions terminées n'ont pas été relancées.
- **Orchestra Org cascade** : les premières graines ont été achevées lors d'une première fenêtre ; la campagne a repris sur checkpoints/progress atomiques et les cinq graines principales ont été complétées.
- **Orchestra Org OOF** : cross-fitting imbriqué 3-fold sur cinq graines ; les fichiers partiels/checkpoints OOF ont été conservés ; les cinq graines et les quinze fits de correcteur demandés par ce bras ont été achevés.
- **Parallélisme OOF** : benchmark parallèle distinct avec suffixe `parallelbench`; les checkpoints initiaux séquentiels sont préservés. Les poids obtenus sont identiques (différence max 0), le wall time concurrent est plus long.
- **Profils latence strictement appariés sur cinq graines** : une tentative de re-profilage à 100 répétitions n'a pas terminé avant le plafond de l'environnement ; aucun résultat incomplet de cette tentative n'est utilisé. La comparaison publiée utilise les mesures présentes dans les logs/JSON de la campagne et indique explicitement les nombres de répétitions différents.
- Aucun arrêt n'a été déclenché en réponse à un résultat de validation défavorable ; aucun test externe n'a été ouvert. Tous les essais négatifs sont conservés.

- **OOF 5-fold** : première invocation interrompue par la limite de l'environnement ; la campagne a été reprise de façon additive depuis les checkpoints et terminée sur 10/10 runs (5 graines Emplica + 5 Orchestra). Les artefacts partiels de reprise sont conservés ; les temps muraux issus de reprises ne sont pas utilisés comme comparaison normalisée.
- **Ablations causales Org** : 30/30 exécutions (six bras × cinq graines) terminées ; résultats négatifs ou non compétitifs conservés.
- **Distillation / modèle sans correcteur** : 20/20 exécutions terminées.
