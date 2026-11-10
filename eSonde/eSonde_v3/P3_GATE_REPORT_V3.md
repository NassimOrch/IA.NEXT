# Rapport de phase P3 v3 — architecture et runtime pure-probe

**Phase :** P3 — runtime et intégration BYTE  
**Version :** 0.3.0  
**Statut :** PASS_WITH_DOCUMENTED_LIMITATIONS

## 1. Description

P3 vérifie que le moteur réel exécute les familles prévues, que BYTE n'est pas seulement un module autonome et que les poids/checkpoints historiques sont compatibles sans altération.

## 2. Architecture

`ProbeModel` orchestre SEQ, SKIP_REL, MORPH, SEM, DISC, RETR, BYTE et COORD. BYTE est initialisée avec le modèle, entraînée avec le flux lexical, sollicitée dans la prédiction et le scoring, utilise les mêmes transitions UTF-8 dans le calcul de probabilité et l'échantillonnage, propose des candidats pour génération, contribue au mélange COORD, et est sérialisée/restaurée. Le tokenizer 2 reste disponible pour les checkpoints v2 ; les nouveaux checkpoints utilisent tokenizer 3.

## 3. Pipeline complet

1. Charger configuration et tokenizer versionnés.
2. Construire les tables de sondes à partir de train.
3. Accumuler les transitions BYTE sur UTF-8 avec BOS/EOS/backoff.
4. Obtenir chaque loi conditionnelle et combiner par COORD.
5. Utiliser la même loi BYTE pour score et continuation.
6. Sauvegarder avec checksum payload/fichier et sidecar.
7. Migrer les états v2 en leur attribuant un poids BYTE nul sans modifier les fichiers originaux.

## 4. Commandes d'exécution

```bash
python -m compileall -q src/esonde tests
PYTHONPATH=src python -m unittest discover -s tests -p 'test_core_p2.py' -v
PYTHONPATH=src python -m unittest discover -s tests -p 'test_byte_v3.py' -v
PYTHONPATH=src python -m unittest discover -s tests -p 'test_p6_advanced.py' -v
PYTHONPATH=src python run_esonde.py info --model models/esonde_v3_demo_checkpoint.json
PYTHONPATH=src python run_esonde.py audit --model models/esonde_v3_demo_checkpoint.json
```

## 5. Résultats

- Core/tokenizer : 16/16 (EXEC-0067).
- BYTE : 7/7 (EXEC-0068), incluant OOV, normalisation, génération/scoring et round-trip.
- Avancé SEM/DISC/COREF/lots/context : 10/10 (EXEC-0069).
- Compatibilité v2 : trois checkpoints originaux préservés et hashes identiques ; poids BYTE absent interprété comme nul dans le chargement historique.
- Audit AST : 21 fichiers runtime, aucun finding (EXEC-0081).

## 6. Interprétation

P3 démontre l'intégration logicielle des sept familles et la conformité structurelle observée au scan AST. Il ne démontre pas une supériorité linguistique ou une capacité de raisonnement générale. Le modèle de démonstration demeure limité par son corpus d'entraînement.

## 7. Conséquences

- **Théoriques :** distributions des familles conditionnelles et mélange convexe commun.
- **Conceptuelles :** BYTE traite les chaînes de surface OOV plutôt qu'une classe inconnue unique.
- **Opérationnelles :** les checkpoints v2 sont lisibles ; les originaux restent bit-identiques ; les checkpoints récents ont une empreinte vérifiable.

## 8. Conclusion

Les critères d'intégration, de sérialisation, d'OOV et de migration sont satisfaits par les tests recensés. La preuve de pureté AST couvre les fichiers runtime listés ; elle ne remplace pas une vérification formelle de toutes les dépendances possibles à l'exécution.

## 9. Statut du modèle

P3 fermée avec la réserve documentaire que l'audit static AST doit être relancé depuis l'arborescence extraite au packaging. Aucun composant neuronal n'a été ajouté.
