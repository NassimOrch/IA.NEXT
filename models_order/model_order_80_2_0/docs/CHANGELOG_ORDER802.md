# Changelog ORDER80.2

ORDER80.2 est une correction de maintenance de la release ORDER80.1 déclenchée par un test boîte noire strict.

## Corrections

1. Le vérificateur conserve les hypothèses globales et de contexte lors des projections de séquents.
2. Les marqueurs d’hypothèses de branches `or_elim` sont identifiés de manière stable et doivent être déchargés.
3. Ajout de `reuse_lemma` : un certificat déjà vérifié peut être réutilisé uniquement si son énoncé est identique et si son propre certificat passe à nouveau le noyau.
4. La mémoire persistante récupère désormais explicitement les dépendances formelles qu’elle réclame avant activation, puis les revalide.
5. Le noyau conserve une comptabilité par identifiants de tokens pour distinguer contexte externe, hypothèses locales et branches.

Aucune solution au problème de test n’est intégrée au moteur.
