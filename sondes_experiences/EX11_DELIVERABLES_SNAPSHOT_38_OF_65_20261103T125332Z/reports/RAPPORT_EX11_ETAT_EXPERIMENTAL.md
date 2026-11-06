# Rapport d’état expérimental EX11

Snapshot : 2026-11-03 12:52:15 UTC

**Source de vérité : fichiers et registres persistés. Aucun fichier du holdout tabulaire n’est chargé.**

## 1. Portes P0–P2

- Prompt : `2.3.1-reconstructed`, JSON valide, corps/Markdown identiques : `True`, SHA-256 corps : `a39cd3ca1d4d772670b96fe4c7ebff0aa594ea1ef098caeb23f18fd48cb65258`.
- Splits : 13 jeux, 65/65 splits, vérification indépendante : PASS.
- ARFF extraits : 13 fichiers.
- Tests logiciels : relancer `PYTHONPATH=$PWD pytest -q`; résultats historiques conservés sous `logs/runs/`.
- Holdout tabulaire : non consulté ; mode lecture seule `0440` ; P4 fermée.

## 2. REPLICA-U

- v003 : 65/65 blocs terminés ; exploratoire, déviation refit final.
- v004 : 37/65 blocs complets au registre ; statut INCOMPLETE_QUOTA / EN COURS.

|Dataset|Seeds|Backbone|Teacher|Student64/32|Student32/16|MLPmatched64/32|MLP GE4X|
|---|---|---|---|---|---|---|---|
|dataset_31_credit-g|5|0.52306|0.55872|0.51119|0.51387|0.50785|0.50998|
|dataset_44_spambase|5|0.19504|0.19294|0.17418|0.17881|0.17918|0.18193|
|dataset_50_tic-tac-toe|5|0.08390|0.08178|0.06520|0.06486|0.04894|0.04853|
|gina_agnostic|5|0.25878|0.32793|0.26072|0.26681|0.24925|0.25246|
|kc1|5|0.36716|0.36788|0.34818|0.34726|0.34588|0.34954|
|kc2|5|0.41140|0.42133|0.36646|0.36428|0.36426|0.36456|
|pc1|5|0.20493|0.21554|0.20872|0.20944|0.20260|0.19659|
|pc3|2|0.31677|0.32109|0.29665|0.29172|0.27576|0.26699|


## 3. CNG

- v001 : 18 runs ; exploratoire (KMeans absent).
- v004 : 0 runs confirmatoires inscrits.
- LOO F/R : consulter le registre dédié ; ne pas assimiler script compilé et runs terminés.

## 4. CNC

- Registre : 3 tentatives ; rapports terminés : 2.
- CNC_composition_1501_v003 : COMPLETED_VALIDATION_AND_HELDOUT_COMPOSITION; C1 g1–g3=0.50133,0.60310,0.25120; C2=0.50507,0.61561,0.04217; holdout g4/g5 C1=1.11122,0.28794; C2=1.06770,0.33680.
- CNC_composition_1501_v004 : COMPLETED_VALIDATION_AND_HELDOUT_COMPOSITION; C1 g1–g3=0.50195,0.60193,0.24854; C2=0.50723,0.62959,0.04017; holdout g4/g5 C1=1.11061,0.28888; C2=1.07529,0.41169.

## 5. Efficacité D1/D2/D3

- D3Q v001 : 160/160 ; exploratoire (centres non-KMeans, GE4X inadéquat pour D1/D2, durées contended).
- D3Q v004 : 0 runs persistés ; confirmatoire uniquement après complétude et audit.

Équivalence D1/D2 : 40/40, erreurs max sortie=1.788e-07, grad entrée=3.725e-09, grad paramètres=2.980e-08.

|Batch|D1 fwd ms|D2 fwd ms|Speedup fwd|D1 step ms|D2 step ms|Speedup step|D3 params|
|---|---|---|---|---|---|---|---|
|1|0.2487|0.0615|4.04×|1.4207|0.4426|3.21×|411|
|16|0.2707|0.0761|3.56×|1.4926|0.5105|2.92×|411|
|64|0.3357|0.1207|2.78×|1.7030|0.6662|2.56×|411|
|256|0.5889|0.3366|1.75×|2.1799|1.1069|1.97×|411|


## 6. Limites de mesure et décision

- RSS disponible : high-water mark de processus partagé, pas isolé par modèle. Pas de compteur énergétique fiable ; énergie non mesurée.
- Les durées de campagne exécutées en contention sont seulement descriptives. Les mesures microbenchmark pré-campagne D1/D2/D3 sont isolées mono-thread.
- P3 est terminée uniquement quand toutes les campagnes préenregistrées ont été exécutées ou explicitement déclarées `INCOMPLETE_QUOTA` avec les absences listées. P4 reste interdite avant gel.
- Ne jamais inférer les runs manquants et ne jamais extrapoler un résultat local à tous les domaines.
