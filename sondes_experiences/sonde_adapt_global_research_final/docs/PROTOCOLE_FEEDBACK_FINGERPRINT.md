# Protocole complémentaire FBR-1 — empreinte effectivement causale

**Gel avant exécution.** Ce supplément ne remplace et ne réécrit pas les résultats A–J déjà calculés. Il répond à une lacune d'implémentation découverte à l'audit : dans A–J, les empreintes étaient journalisées, mais ne pilotaient pas les mises à jour. FBR-1 teste séparément un véritable effet causal de l'empreinte sur l'actualisation.

- Tâche principale : `two_moons`, partitions originales du benchmark principal; mêmes trois graines de modèle (1501, 1607, 1717). Cinq architectures A–E.
- Flux : le flux d'adaptation préfixé de 180 exemples; pour le décalage, flux nouvellement généré indépendamment, translation brute de +0,75 sur la première coordonnée, puis normalisé avec le scaler ajusté uniquement sur train.
- Seuil : quantile 0,90 des résidus absolus `|y-p|` calculé sur la partition validation propre, avant toute adaptation. Le seuil n'est jamais réglé sur le test.
- Ordre causal : prédiction avant révélation → révélation de l'observation mesurée si disponible → création de l'empreinte → décision de quarantaine et routage éventuel → mise à jour → prochain élément indépendant du flux. Le modèle ne reçoit jamais le marqueur de corruption de l'évaluateur.
- Politiques : (1) mise à jour round-robin non filtrée; (2) quarantaine déclenchée par empreinte, round-robin; (3) même quarantaine avec routage RBF vers la sonde au résidu local maximal; (4) contrôle de suppression aléatoire indépendante à 10 %; ainsi qu'un contrôle sans aucune mise à jour sur les deux distributions d'évaluation.
- Conditions : labels propres; 30 % de mesures manquantes; 20 % de labels inversés aléatoirement; 50 % de labels trompeurs; flux covarié décalé. Pour les observations manquantes, aucune valeur cible n'est imputée par la prédiction.
- Métriques : accuracy, log-loss, F1, ROC-AUC, PR-AUC, Brier, ECE-10 bins, temps d'adaptation, nombre d'updates, anomalies détectées et observations disponibles. Les résumés sur trois graines sont descriptifs; les intervalles t sont fragiles et aucune p-value confirmatoire ni supériorité universelle ne sera revendiquée.
- Contrôle d'intégrité : résultats par graine, empreintes événements, provenance, configuration et registre d'erreurs. Toutes les conditions et erreurs sont conservées.
