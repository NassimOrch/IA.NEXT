# Rapport final d’audit indépendant — NGeGenBrain_v0 → NGeGenBrain_v1

**Date :** 27 octobre 2026  
**Objet :** audit de l’archive V0 livrée, test indépendant complexe, corrections ciblées, puis répétition du même banc sur l’archive V1 finale.  
**Source V0 exacte :** `Dmodel_NGeGenBrain_v0.zip` — SHA-256 `6ffcc921732a9c58bda5d2aa1461bfa5d9dfad99cc5ef6e3b9331d85b078fe8d`.  
**Archive V1 finale testée :** `Dmodel_NGeGenBrain_v1.zip` — SHA-256 `71534f98ff590e5c1a103888f0e553e9e8966d34d7f0364429eac8eae238b5c8`.  
**Banc indépendant :** `independent_hard_bench_v1.py` — SHA-256 `9325f55cf7e8694fd88c6f6df928e5b4a9f568f447fd41e6b80014659749b816`.  
**Graine commune :** `20261027`.  
**Environnement d’exécution :** Linux x86-64, Python 3.13.5; dépendances du runtime : bibliothèque standard Python.

## 1. Description et méthode

L’objet était de tester le binaire logiciel réellement livré, plutôt que de s’appuyer uniquement sur la suite de tests incluse dans le dépôt. Le ZIP V0 a été haché et extrait dans un dossier indépendant. Un banc séparé a exécuté 15 scénarios sur une base SQLite neuve, sans charger les faits de démonstration du projet et sans injecter de réponse cible dans le moteur. Les oracles sont calculés indépendamment : arithmétique exacte par `fractions.Fraction`, clôture de graphe par parcours indépendant, invariants structurels et statuts contractuels.

Le même fichier de banc, le même hash de banc, les mêmes 15 identifiants de cas et la même graine ont ensuite été appliqués à l’extraction propre de l’archive V1 finale. Les résultats bruts conservent les sorties, mesures, verdicts, durées, versions, chemins, empreintes et informations d’environnement. Aucun échec baseline n’a été effacé après correction.

## 2. Architecture évaluée

Le système testé est un runtime de programmation compositionnelle locale : AST JSON déclaratif, composants et opérateurs enregistrés, contrats et types, capacités, budget, exécution par résultats typés, maillage de faits et règles multi-prémisses, certificats vérifiables dans le fragment pris en charge, trace d’événements chaînée, stockage SQLite, mémoire, contrôleur ASCRC, ASCR-NG reconstruit pour le retrieval, synthèse/reprise, modèle du monde avec statut `SIMULATED`, intentions déclaratives, CLI et interface web locale.

La correction V1 ne code pas les sorties attendues des tests. Elle resserre des invariants généraux : l’identité d’un fait inclut ses types et son contexte; une sortie mal typée ne peut être promue par une bonne correspondance de valeur; les budgets et coûts doivent être finis, non négatifs et utiliser des dimensions reconnues; un AST excessivement profond est rejeté avec statut et trace; les requêtes honorent le contexte; et le plafond de recherche compte également les jointures infructueuses.

## 3. Pipeline complet reproductible

1. Vérifier SHA-256 et CRC du ZIP source.
2. Extraire chaque modèle dans un répertoire distinct et utiliser une nouvelle base de données de test.
3. Exécuter le banc indépendant avec `--seed 20261027` et les mêmes 15 cas.
4. Comparer les résultats aux oracles extérieurs et conserver chaque JSON brut.
5. Exécuter la suite du dépôt avec `ResourceWarning` traité comme erreur.
6. Exécuter les parcours CLI et les contrôles HTTP locaux; vérifier SQLite et la chaîne d’événements.
7. Exécuter le validateur de release et vérifier les références formelles/tests.
8. Tester à nouveau l’archive V1 définitive extraite, puis calculer l’empreinte exacte qui est associée au reçu.

## 4. Commandes de reproduction

Après extraction du ZIP V1, depuis `Dmodel_NGeGenBrain_v1/` :

```sh
PYTHONWARNINGS=error::ResourceWarning PYTHONPATH=src python3 ngbrain.py test
PYTHONWARNINGS=error::ResourceWarning PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 ngbrain.py init
PYTHONPATH=src python3 ngbrain.py status
PYTHONPATH=src python3 ngbrain.py verify
PYTHONPATH=src python3 ngbrain.py demo
PYTHONPATH=src python3 scripts/validate_release.py
```

Rejouer le banc d’audit depuis l’archive Amodel :

```sh
python3 independent_hard_bench_v1.py \
  --model-root /path/to/extracted/Dmodel_NGeGenBrain_v1 \
  --source-archive /path/to/Dmodel_NGeGenBrain_v1.zip \
  --output hard_benchmark_v1_final.json \
  --seed 20261027
```

Pour le baseline, utiliser l’archive V0 et son extraction, sans modifier le banc ni la graine.

## 5. Résultats du benchmark indépendant

| Cas | Propriété vérifiée | V0 exact | V1 final exact | Mesure principale |
|---|---|---:|---:|---|
| `ARITH-001` | Arithmétique rationnelle contre oracle `Fraction` | PASS | PASS | 2 400 opérations, zéro différence pour l’addition, la soustraction, la multiplication et la division admissible. |
| `MESH-001` | Clôture d’un graphe dirigé de 12 nœuds | PASS | PASS | 35 paires atteignables, aucune omission ni paire superflue contre l’oracle indépendant. |
| `MESH-002` | Identité de fait typé | FAIL | PASS | V0 supprime une dérivation `Int` lorsque le même SPO a déjà une autre déclaration de type; V1 conserve `String` et `Int` séparément et ajoute la dérivation typée. |
| `WM-001` | Contrat de sortie du modèle du monde | FAIL | PASS | V0 active le modèle avec une sortie chaîne malgré `output_type=Int` (exact-match 1.0); V1 signale `incomplete_holdout_predictions` et n’active pas le modèle. |
| `BUDGET-001` | Garde-fous pour budgets non finis | FAIL | PASS | V0 retourne `Success` sur budget `NaN`; V1 le rejette. Un budget fini de 1 KiB sur l’entrée de 200 KiB retourne `Partial`. |
| `BUDGET-002` | Validation du coût d’un composant | FAIL | PASS | V0 accepte `resource_cost.cpu=NaN`; V1 refuse la déclaration. |
| `TRACE-001` | Ajout concurrent de 200 événements | PASS | PASS | 8 travailleurs, 25 événements chacun; 200 événements conservés, chaîne valide, aucun échec d’écriture. |
| `MEM-001` | Corruption d’un payload mémoire gzip | PASS | PASS | Le CRC échoue (`CRC check failed`); `get_memory` expose l’erreur et fixe le payload à `None`, qui ne peut donc être consommé comme donnée valide. |
| `MESH-003` | Admission de trois règles invalides | PASS | PASS | Les trois règles sont rejetées; aucune n’est persistée. |
| `CERT-001` | Vérification d’un certificat falsifié | PASS | PASS | Le certificat valide passe; la conclusion modifiée puis re-hachée est rejetée faute de dérivation depuis les prémisses/règles. |
| `TYPE-001` | Dix formes JSON avec identité typée `Any` | PASS | PASS | Dix formes traitées sans erreur dans le contrat déclaré. |
| `SEC-001` | Code Python fourni sous forme de chaîne | PASS | PASS | Le texte `__import__(...)` demeure une valeur inerte; le banc ne constate aucune exécution de commande. |
| `ROBUST-001` | AST de 1 200 niveaux | FAIL | PASS | V0 laisse remonter `RecursionError`; V1 renvoie `Rejected`, raison `maximum JSON/AST nesting depth exceeded`, et enregistre une trace. |
| `MESH-005` | Filtre de contexte / tenant | FAIL | PASS | Pour `tenant=alpha`, V0 retourne `alice` et `bob`; V1 ne retourne qu’`alice`. |
| `MESH-006` | Borne d’exploration sur jointure sans solution | FAIL | PASS | Avec un plafond de 1, V0 effectue 33 330 appels de matching et renvoie à tort `FIXPOINT_REACHED`; V1 s’arrête après une comparaison et renvoie `BUDGET_EXHAUSTED`, sans fait produit. |
| **Total** | **15 scénarios identiques** | **8 PASS / 7 FAIL** | **15 PASS / 0 FAIL** | **Les 7 classes de défaut observées ont été reproduites puis testées après correction.** |

### Défauts V0 reproduits

1. Identité du maillage insuffisamment typée, conduisant à supprimer une dérivation valide.
2. Porte d’activation du modèle du monde fondée sur une bonne correspondance de valeur malgré un contrat de type violé.
3. Budgets `NaN` ouvrant la porte de ressource au lieu de provoquer un refus.
4. Coût de composant non fini accepté au registre.
5. AST très profond faisant remonter une exception Python brute hors du résultat typé.
6. Filtre de contexte ignoré, exposant un fait d’un autre contexte dans la requête.
7. Plafond de jointure ne limitant pas les explorations partielles infructueuses et rapportant un faux point fixe.

## 6. Résultats de régression et d’intégration sur l’archive finale

- Tests de dépôt : **65/65 PASS**, 0 échec, 0 erreur; `ResourceWarning` est traité comme erreur.
- Validateur de release : **31/31 contrôles PASS**.
- Smoke CLI : **6/6 PASS**, y compris initialisation, statut, catalogue d’actions, exécution d’AST, vérification de base et catalogue par action.
- Smoke HTTP : **6/6 PASS**, dont page HTML, JavaScript, registre d’actions, santé API, vérification SQLite et POST d’action.
- Parcours CLI individuels `init`, `status`, `verify`, `demo` : tous terminent avec code de sortie 0 sur base isolée.
- SQLite : `PRAGMA integrity_check = ok`; `PRAGMA foreign_key_check` ne signale aucune violation.
- ZIP : CRC et extraction propres réussis; le benchmark V1 enregistre le SHA-256 exact `71534f98ff590e5c1a103888f0e553e9e8966d34d7f0364429eac8eae238b5c8`.

Le JSON de résultat proprement dit est `hard_benchmark_v1_final.json`. Le fichier `comparison_v0_v1_final.json` confirme que les IDs, la graine et l’empreinte du banc sont identiques. Les journaux stdout, CLI, HTTP, les reçus du validateur et les entrées de preuve sont conservés dans l’archive Amodel.

## 7. Interprétation

Les sept échecs V0 ne sont pas de simples différences de score : ils touchent l’identité sémantique, la promotion d’une prédiction, l’application de garde-fous de ressources, la robustesse du runtime, le filtrage contextuel et la borne réelle du travail de recherche. Le fait que la suite de tests livrée avec V0 ait été verte ne détectait pas ces cas. Le banc indépendant les a révélés, puis les tests de régression V1 empêchent leur retour sur les formes testées.

Les mêmes 15 cas et la même graine passent sur le ZIP V1 exact. Cette amélioration est bien mesurée dans la portée testée; elle n’autorise pas à conclure que toutes les entrées, programmes concurrents, extensions, usages ou attaques possibles sont maintenant sans défaut.

## 8. Conséquences théoriques, conceptuelles et opérationnelles

### Théoriques

La théorie 3 formalise désormais l’identité typée/contexualisée des faits, les budgets numériques fermés, la borne sur les explorations partielles de règles, la porte de type de sortie du modèle du monde et le rejet typé de structures AST excessives. Ces garanties restent conditionnelles à l’utilisation effective du chemin validé et aux contrats des composants; la théorie entière n’a pas été vérifiée par assistant de preuve.

### Conceptuelles

Une égalité de valeur ne remplace pas l’égalité du type et du contexte. La qualité prédictive seule ne rend pas un modèle admissible si ses sorties violent son contrat. Un budget de recherche doit compter les comparaisons réalisées même quand aucune conclusion n’est produite. Une valeur simulée ne devient pas une observation au seul motif qu’elle correspond à une cible.

### Opérationnelles

V1 refuse explicitement les budgets non finis/dimensions inconnues et les déclarations de coût non valides; l’AST hors des limites structurales est retourné comme rejet typé; l’épuisement du plafond d’exploration est signalé. Les applications doivent traiter les statuts et les traces plutôt que se fier uniquement à une valeur présente dans le résultat.

## 9. Limites résiduelles et anomalies non masquées

- Ce banc n’est ni un fuzzing universel, ni un model checker, ni un audit complet de sécurité de production. Il couvre 15 scénarios délibérés et reproductibles, avec une graine fixe.
- Les 65 tests et 31 contrôles de release apportent des éléments de vérification finis; ils ne prouvent pas l’absence absolue de défauts.
- L’équivalence historique avec les exécutables ASCR/AAM non fournis n’est pas démontrée. Le retrieval `ASCR-NG` est une reconstruction fonctionnelle documentée, pas une copie vérifiée bit-à-bit.
- L’exécution native Windows de `.bat` et PowerShell n’a pas été possible dans l’environnement Linux. Le runtime Python portable n’est pas inclus parce que le téléchargement officiel a échoué; Python 3.11+ ou le bootstrapper sous Windows connecté est nécessaire.
- Une exécution combinée du smoke de cycle de vie a initialement atteint le délai global du shell; l’exécution séparée des commandes `init`, `status`, `verify`, `demo` a ensuite terminé chacune avec code 0. L’interruption initiale demeure inscrite dans les journaux/outils de suivi.
- Une copie erronée du chemin de staging lors de l’assemblage initial de l’audit a échoué sans modifier les sources; la copie a été reprise sur le chemin vérifié. L’incident est consigné dans le suivi de travail.

## 10. Conclusion et statut du modèle

**Statut de NGeGenBrain_v1 : corrigé et vérifié dans le périmètre expérimental annoncé, incluant tests de dépôt, interfaces et benchmark independent sur le ZIP exact.** Le résultat comparatif est de 8/15 sur la V0 livrée contre 15/15 sur la V1 finale pour le banc choisi. Les échecs V0 et leur historique restent conservés. La revendication d’absence totale de défauts, de généralité universelle prouvée ou d’équivalence historique avec une implémentation non disponible n’est pas faite.
