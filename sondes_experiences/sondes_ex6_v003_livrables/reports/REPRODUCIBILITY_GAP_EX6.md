# REPRODUCIBILITY_GAP_EX6

## Constat

Les artefacts bruts sont présents, les prédictions et checkpoints existants ont été recalculés/inspectés, et une trace des cellules interactives de définition et d'exécution est sauvegardée dans `logs/pilot_execution_trace_cells.md`.

La séquence historique a toutefois fonctionné ainsi :
1. définition de `EmplicaStack` et entraînements par cellules interactives ;
2. entraînement Replica par une boucle interactive qui charge les checkpoints OOF EX5 ;
3. entraînement Orchestra homogène et diagnostic early-exit par cellules ;
4. sauvegarde ultérieure de scripts autonomes dans `src/` pour reprendre la recherche.

Les horodatages des résumés sont antérieurs à ceux des scripts empaquetés et les clés/schémas de certains résumés ne correspondent pas à la version actuelle des scripts. Les scripts empaquetés ne peuvent donc pas être déclarés comme le code exact hashé utilisé lors de chaque run historique.

## Ce qui est vérifié

- les 62 fichiers de prédictions sélectionnés ont des métriques recalculées cohérentes ;
- les 20 comparaisons candidate/MLP-ge4x respectent le ratio paramétrique ;
- les comptes de tensors des checkpoints correspondent à `P_total - 60` coefficients du scaler ;
- les cinq paires Replica ont des tenseurs primaire/clone identiques ;
- les scripts autonomes actuels se compilent, leurs interfaces `--help` fonctionnent, les imports fonctionnent, le chargeur et les forwards de modèles sont testés ;
- les dépendances minimales des cinq checkpoints EX5 nécessaires à Replica ont été copiées et hashées dans `inputs/reference_code/ex5_replica_source/`.

## Ce qui n'est pas vérifié

- le SHA exact du code source chargé en mémoire pour chaque run historique ;
- le SHA de configuration par run au moment d'entraînement ;
- la commande exacte et l'environnement de processus pour chaque exécution initiale ;
- la reproductibilité bit-à-bit des temps de mesure et checkpoints.

## Mesure corrective

À partir de la prochaine campagne :
- lancer uniquement depuis les scripts versionnés présents dans `src/` ;
- générer un nouvel identifiant de run non existant, refuser tout écrasement ;
- écrire dans chaque `summary.json` le SHA-256 du code, de la config, du dataset/split et du checkpoint ;
- capturer la commande, l'environnement complet, les versions et logs stdout/stderr ;
- sauvegarder les sorties brutes avant calcul d'agrégat ;
- conserver les anciens résultats tels quels.

**Verdict traçabilité première campagne : PARTIELLE.** La cohérence des résultats enregistrés est vérifiée, mais l'identité exacte code-run n'est pas attestée. Cette limite est incluse dans le verdict global `INCOMPLET`.
