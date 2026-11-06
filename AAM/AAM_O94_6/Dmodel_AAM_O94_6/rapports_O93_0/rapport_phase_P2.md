# Rapport de phase P2 — Moteur de création de sondes différenciées

## Description
La phase vérifie la fabrique de sondes versionnées, le mécanisme de miroirs et de composition, les mesures de diversité/collisions, la recherche adaptative reprenable et la séparation entre observation, preuve de reproduction et preuve de généralisation.

## Architecture
- `aam_o93/probes.py::ProbeFactory` : catalogue, canonicalisation/hash, opérations de sondes, miroirs et compositions, évaluation de portefeuille, boucle adaptative et checkpoint.
- `aam_o93/competence.py` : la découverte de candidats est distincte de la promotion d’une compétence.
- `tests/test_p2_probes.py` : tests des contrats attendus.
- `checklist_de_travail_O93_0.json` et `registre_prouves.json` : gates et traçabilité.

## Pipeline complet
1. Charger les contrats normatifs, la checklist de phase et les deux registres d’erreurs.
2. Définir/versionner et hasher les sondes candidates.
3. Exécuter les sondes sans transmettre la cible au prédicteur.
4. Calculer la diversité inter-sondes, les distances typées, les collisions et les fausses séparations.
5. Reprendre la génération si le lot courant ne suffit pas; distinguer budget atteint, arrêt utilisateur et preuves positives.
6. Évaluer reproduction source-off et holdout indépendant séparément; ne pas confondre une candidate de développement avec une compétence validée.
7. Enregistrer les traces, exécuter la régression complète, mettre à jour checklists et registre.

## Commandes d'exécution
- `python -m unittest discover -s tests -p 'test_p2_probes.py' -v`
- `python -m unittest discover -s tests -v`
- `python scripts/preflight_O93_0.py --operation P2-full-regression-retry --output logs/O930_P2_preflight_full_regression_retry.json`

## Résultats
- Tests ciblés : **15/15 PASS** (`logs/O930_P2_probe_unittest_final.stderr.txt`).
- Régression locale : **118/118 PASS** (`logs/O930_P2_full_unittest_retry.stderr.txt`).
- Échec de workflow initial : 117/118, dû à une assertion de test exigeant P1 après la progression légitime vers P2; correction du test et nouvelle exécution 118/118.
- Statut des gates : cinq gates `PASS_BOUNDED`; P2 `COMPLETE`, portée `LOCAL_TESTED_BOUNDED`.

## Interprétation des résultats
Les contrats et le comportement de contrôle de la fabrique sont couverts par les tests dans l’environnement local. La réussite de tests synthétiques ne prouve ni la reproduction parfaite d’une compétence arbitraire ni sa généralisation universelle. La promotion de compétence reste séparée; les évaluations réelles doivent être préenregistrées pour la compétence et le domaine concernés.

## Conséquences
### Théoriques
Le moteur sépare identité exacte/provenance des mesures de proximité typée; une empreinte de hachage n’est pas utilisée seule comme distance sémantique.
### Conceptuelles
Une sonde candidate peut enrichir l’observation sans être assimilée à une compétence. La convergence de recherche est conditionnelle aux protocoles testés.
### Opérationnelles
Les checkpoints permettent la reprise; un budget atteint reste non concluant. Les essais sur matériel réel, réseau réel et Windows natif restent hors de cette phase.

## Conclusions
La phase P2 est clôturée dans le périmètre de tests locaux déclaré. Les exigences de RAG sémantique multi-espaces restent assignées à P3 et ne sont pas déclarées réalisées ici.

## Statut du modèle
`P2 = COMPLETE / LOCAL_TESTED_BOUNDED`; `P3 = IN_PROGRESS`. Aucune conclusion anticipée sur la réussite ou l’échec global d’AAM n’est formulée.
