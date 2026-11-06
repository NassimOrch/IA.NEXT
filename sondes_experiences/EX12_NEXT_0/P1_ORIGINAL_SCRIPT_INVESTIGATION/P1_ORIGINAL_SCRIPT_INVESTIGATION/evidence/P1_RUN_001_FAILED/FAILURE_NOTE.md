# P1 run 001 — échec conservé

- Objet : premier essai du banc P1, sans entraînement.
- Statut : `FAILED` (ne pas agréger comme mesure valide finale).
- 384 lignes noyau / 15 360 mesures brutes / 54 tests enregistrés.
- 35 échecs provenaient du test de distance intermédiaire : la formule d'identité vectorisée calculée en float32 divergeait de la référence explicite jusqu'à 2.2888e-5 en absolu. Un des 18 tests pytest échouait aussi sur un gradient à cause d'une différence d'arrondi marginale.
- Les comparaisons de sortie complète / gradients préliminaires restaient sous 1e-6, mais cela ne justifiait pas d'ignorer la divergence intermédiaire.
- Action : adopter une accumulation float64 commune aux deux implémentations de référence/optimisée, caster le résultat vers le dtype d'entrée, puis retester. Le coût de cette précision supplémentaire doit rester visible dans les mesures.
- Tous les fichiers de ce run sont conservés tels quels. Aucune donnée n'a été remplacée.
