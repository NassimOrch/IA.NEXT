# Amodel eGenBrain v4 — audit du modèle

Cette archive regroupe le code source auditable, les tests, les sorties brutes, les résultats de scoring post-hoc, les traces, les journaux de correction et les formalismes. Les échecs/interruption de harnais et les résultats négatifs ont été conservés; une exécution PASS ne signifie pas nécessairement que le résultat du modèle est exact.

## Résultats principaux vérifiés

- Suite complète: 136/136 tests sur le code source, `ResourceWarning` élevé au rang d'erreur.
- Campagne aveugle: 66 inférences brutes (11 cas × 6 modes), persistées avant scoring, avec 8 cas positifs demandant une composition et 3 cas où une abstention était attendue. Le mode complet a 8/8 dérivations positives et 3/3 abstentions attendues dans ces micro-mondes finis.
- Intégration réelle au MG historique: problème des œufs -> `18`, certificat `PASS`, sans fallback v3. Le hash du MG historique est inchangé.
- Installation à partir des ZIP runtime finaux: taille et SHA-256 de la base reconstituée conformes, SQLite integrity check `ok`, zéro violation FK. Le test runtime à froid est aussi conservé.

Les réponses de référence sont dans `experiments/references_sealed.json`, utilisé uniquement par le scorer après les inférences; il ne fait pas partie du paquet Dmodel runtime. Les empreintes finales des archives sont consignées dans `manifest_livraison_eGenBrain_v4.json` et l'archive de suivi.

Le score de 8/8 ne vaut que pour les 8 cas positifs construits. Les opérateurs arithmétiques sont des primitives déterministes génériques; le facteur `dozen=12` est une primitive explicitement fournie. L'induction autonome des opérateurs/règles et l'intelligence générale restent des questions ouvertes.
