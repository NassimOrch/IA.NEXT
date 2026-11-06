# Limites et interprétation des résultats

## 1. Portée générale

ORDER80.2.1 est généraliste au niveau du protocole : il accepte un problème libre, une frontière de références et une mémoire persistante, puis orchestre observation, recherche, synthèse, vérification et archivage.

## 2. Nature de la synthèse intégrée

Le synthétiseur livré est extractif et déterministe. Il sélectionne des passages pertinents à partir des références réellement observées. Il ne constitue pas un agent sémantique universel capable, par lui-même, d'inventer une preuve arbitraire ou d'exécuter une analyse scientifique complète.

## 3. Vérification

Le vérificateur général contrôle provenance et couverture selon les critères du `task.json`. Le statut `EVIDENCE_SYNTHESIS_VERIFIED` ne signifie pas que chaque affirmation est universellement vraie. Pour une garantie de domaine forte, un vérificateur de domaine explicite doit être branché.

## 4. Recherche web

La sécurité applicative réduit le risque de sortie de périmètre, de SSRF et de contenu inattendu, mais ne remplace pas le firewall, le proxy, l'isolation système ni la politique réseau de la machine qui exécute le modèle.

## 5. Fin d'exécution

`TIME_BUDGET_EXPIRED` signifie que le budget s'est écoulé. `UNRESOLVED` signifie qu'aucune synthèse satisfaisant le vérificateur général n'a été obtenue pendant ce run. Aucun de ces statuts ne permet de conclure à l'impossibilité ou à la fausseté d'un problème.
