# Rapport de phase P1 — Observation universelle locale

## Description
Renforcement de `aam_o93/observer.py` pour l'observation de fichiers par instantané brut, empreintes avant/après, provenance, détection de mutation pendant l'observation, niveaux d'observation distincts et miroirs. Ajout de lecteurs structurels optionnels DOCX/PDF/Parquet avec statuts qui n'inventent pas un décodage quand la dépendance n'est pas disponible.

## Architecture
- Entrée : chemin local contrôlé ou valeur déjà fournie, sans exécution du contenu observé.
- Pipeline : contrôle de chemin/limite, lecture binaire, empreinte, vues typées, extraction structurelle disponible, empreinte après lecture, attribution de provenance et de statut.
- Accès matériels : autorisation explicite et fermeture ; les tests sur adaptateurs ne prétendent pas être un test sur un appareil physique.

## Pipeline complet exécuté
1. Consultation préalable : `logs/O930_P1_preflight_full_regression.json` (PASS_BOUNDED).
2. Suite ciblée P1 : 23/23 (`logs/O930_P1_unittest.stderr.txt`).
3. Régression complète : 112/112 tests PASS (`logs/O930_P1_full_unittest.stderr.txt`).
4. Mise à jour du registre et de la checklist : `checklist_de_travail_O93_0.json`, `registre_prouves.json`, registres d'erreurs.

## Commandes d'exécution
```bash
python scripts/preflight_O93_0.py --operation 'P1-full-regression' --output logs/O930_P1_preflight_full_regression.json
python -m unittest discover -s tests -v
```

## Résultats
- Régression complète : 112 tests, 112 passés, 0 échec.
- Les chemins Unicode, la mutation concurrente, les entrées malformées, les liens symboliques, les statuts de décodage et les contraintes d'autorisation sont couverts par les tests locaux.
- Un décodeur Parquet manque dans l'environnement ; le fichier est explicitement `NOT_DECODED`, pas présenté comme interprété.

## Interprétations
Un succès de test prouve uniquement les contrats exercés dans cet environnement. Il ne prouve pas l'équivalence d'observation universelle, la reproduction parfaite d'une compétence ni sa généralisation sur de nouvelles données. Aucun résultat de ce type n'est déduit.

## Conséquences
- Théorique : les vues d'observation et leur provenance sont explicitées; l'identité observée demeure relative aux sondes et décodeurs disponibles.
- Conceptuelle : observation brute et décodage sont séparés; type inconnu/dépendance manquante ne devient pas une observation sémantique inventée.
- Opérationnelle : le moteur reçoit un statut exploitable et peut détecter une mutation de source pendant la lecture.

## Conclusion
**P1 : COMPLETE_BOUNDED_LOCAL.** La phase est acceptée dans le périmètre local avec tests passés. Les appareils réels, Windows natif et les intégrations Web réelles restent en `NOT_RUN` pour les gates d'environnement concernées. P2 peut commencer selon l'ordre de phase. Le RAG multi-espace sémantique n'est pas affirmé implémenté.

## Statut du modèle
Observation de fichiers renforcée et testée au niveau local; aucune affirmation de complétude globale d'O93_0 et aucun verdict préalable de réussite/échec du modèle.
