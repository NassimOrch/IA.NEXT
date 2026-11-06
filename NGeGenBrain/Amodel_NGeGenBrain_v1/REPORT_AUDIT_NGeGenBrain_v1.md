# Rapport d’audit indépendant, de correction et de comparaison — NGeGenBrain_v1

**Date de campagne :** 27 octobre 2026  
**Version analysée :** `NGeGenBrain_v0` (`0.3.0`) puis `NGeGenBrain_v1` (`1.0.0`)  
**Source normative :** `formalism/theorie_programation_compositionnelle_NG_0.tex`, complétée par `theorie_programation_compositionnelle_3.tex`  
**Environnement de travail :** `NGeGenBrain_v1_work_1`  
**Registre exigence → code → test :** `NGeGenBrain_v1_mise_en_oevre.json`  
**Registre de preuves :** `preuves_NGeGenBrain_v1.json`  
**Portée :** exécutions Linux/Python 3.13.5, tests unitaires et d’intégration, CLI, HTTP local, benchmark indépendant de 15 scénarios. L’exécution native Windows n’est pas revendiquée.

## 1. Description

L’objectif de cette campagne n’était pas de réutiliser les tests du projet comme unique preuve. J’ai extrait le Dmodel V0 réellement livré, vérifié son SHA-256, créé des bases SQLite neuves et conçu un banc indépendant avec oracles externes. Les 15 scénarios comprennent des propriétés arithmétiques avec des rationnels exacts, une fermeture de graphe vérifiée par une oracle indépendante de parcours, des types de faits qui entrent en collision sur leurs valeurs, un modèle du monde mal typé, des valeurs de budgets non finies, une charge concurrente, la corruption d’une mémoire, des règles invalides, la falsification d’un certificat, des entrées JSON adversariales, un AST profond, un filtre de contexte et une jointure volontairement sans solution.

Le banc n’injecte pas une réponse attendue dans le moteur. Les assertions servent uniquement d’oracles externes pour vérifier un comportement déclaré. Les entrées de référence et les résultats sont enregistrés séparément; le moteur ne lit aucun jeu de vérité cachée lors de l’exécution.

## 2. Architecture évaluée et modifications de V1

Le système reste un moteur compositionnel local : AST JSON déclaratif, composants et opérateurs enregistrés, contrats d’entrée/sortie, capacités, exécution avec résultats typés, stockage SQLite, maillage stratifié, règles multi-prémisses, certificats, trace d’événements chaînée, mémoire persistante, ASCRC, synthèse bornée, modèles du monde, intentions déclaratives, CLI et web local. L’identité du paquet, le manifeste et les lanceurs sont versionnés V1.

Les corrections sont ciblées sur des obligations générales, non sur des réponses du banc :

1. La clé de déduplication du maillage prend maintenant en compte les types déclarés et le contexte au lieu de seulement les valeurs visibles.
2. Une prédiction de modèle du monde ne peut améliorer le score ni activer le modèle si sa sortie viole le type de sortie déclaré.
3. Les budgets rejettent les nombres non finis et les dimensions inconnues avant l’exécution; les coûts de composants doivent être finis, non négatifs et de dimensions reconnues.
4. Le moteur prévalide itérativement la forme JSON/AST et transforme une profondeur excessive en rejet typé avec événement de provenance, au lieu de laisser remonter un `RecursionError` brut.
5. Les requêtes du maillage appliquent le filtre de contexte.
6. Le plafond de recherche compte les comparaisons de prémisses/faits, y compris les jointures partielles sans solution, et rend `BUDGET_EXHAUSTED` explicite. Il ne prétend pas que ce résultat soit reprenable en l’absence d’un front persistant.
7. Quatre régressions supplémentaires couvrent les dimensions de budget inconnues, les permissions données sous forme d’une chaîne, les entiers de coût trop grands et un plafond de jointure nul.

Ces modifications ne modifient pas la source historique NG_0; les obligations sont ajoutées à la théorie 3 comme règles de raffinement et de validation de l’implémentation.

## 3. Pipeline complet de test

1. Calcul du SHA-256 de `Dmodel_NGeGenBrain_v0.zip` et test CRC ZIP.
2. Extraction dans un répertoire distinct sans utiliser le workspace du build.
3. Initialisation d’une base de benchmark vide pour chaque famille de cas; absence des données de démonstration comme données d’entrée.
4. Exécution des mêmes 15 scénarios sur V0 et V1, avec graine `20261027` et le même code de banc.
5. Comparaison des résultats avec les oracles exacts, fermeture transitive indépendante, invariants attendus, statut d’exécution et compteurs réels.
6. Écriture du JSON brut avec chaque entrée, sortie observée, verdict, durée, environnement, hash de l’archive source et hash du banc.
7. Régression du dépôt V1 sous `PYTHONWARNINGS=error::ResourceWarning`, tests CLI, test HTTP local, intégrité SQLite et chaîne de trace.
8. Validation de la matrice exigence→source→code→test, création des archives, contrôle CRC et extraction propre de l’archive finale. Le reçu exact de l’archive publiée est conservé dans l’archive d’audit accompagnante afin d’éviter une référence de hash circulaire à l’intérieur du Dmodel lui-même.

## 4. Commandes de reproduction

Depuis la racine extraite de `Dmodel_NGeGenBrain_v1.zip` :

```sh
PYTHONWARNINGS=error::ResourceWarning PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 ngbrain.py test
PYTHONPATH=src python3 ngbrain.py init
PYTHONPATH=src python3 ngbrain.py status
PYTHONPATH=src python3 ngbrain.py verify
PYTHONPATH=src python3 ngbrain.py demo
PYTHONPATH=src python3 scripts/smoke_cli.py --db build/cli_smoke.sqlite3
PYTHONPATH=src python3 scripts/smoke_web.py --db build/web_smoke.sqlite3
python3 scripts/generate_traceability.py
python3 scripts/generate_proof_registry.py
python3 scripts/validate_release.py
```

Le banc de test dur, indépendant du paquet, est fourni dans l’archive d’audit. Après extraction d’un modèle dans `$MODEL_ROOT`, son invocation reproductible est :

```sh
python3 independent_hard_bench_v1.py \
  --model-root "$MODEL_ROOT" \
  --source-archive /path/to/Dmodel_NGeGenBrain_v1.zip \
  --output hard_benchmark_v1.json \
  --seed 20261027
```

Pour le baseline, utiliser l’archive V0 et son extraction exacte; la graine, la suite et les oracles restent identiques.

## 5. Résultats détaillés du benchmark indépendant

| ID | Objet | V0 | V1 | Observation déterminante |
|---|---|---:|---:|---|
| `ARITH-001` | 2 400 opérations exactes contre `Fraction` | PASS | PASS | 0 écart sur addition, soustraction, multiplication et division admissible. |
| `MESH-001` | Clôture d’un graphe dirigé de 12 nœuds | PASS | PASS | 35 paires accessibles, aucune absente ni superflue par rapport à la fermeture indépendante. |
| `MESH-002` | Identité d’un fait typé | FAIL | PASS | V0 conserve seulement le fait cible `String`, ne crée aucun fait `Int`; V1 conserve les deux types et crée le fait dérivé `Int` avec certificat vérifiable. |
| `WM-001` | Contrat de sortie du modèle du monde | FAIL | PASS | V0 autorise l’activation sur 10/10 valeurs textuellement exactes malgré `output_type=Int`; V1 classe les 10 cas comme sorties incomplètes/mal typées et bloque l’activation. |
| `BUDGET-001` | Budget non fini | FAIL | PASS | V0 accepte un résultat `Success` sous limite mémoire 1 KiB et budget `NaN`; V1 renvoie `Rejected` pour le budget non fini, tandis que le budget fini reste `Partial`. |
| `BUDGET-002` | Coût de composant `NaN` | FAIL | PASS | V0 accepte la déclaration; V1 la refuse. |
| `TRACE-001` | 200 ajouts concurrents, 8 travailleurs | PASS | PASS | 200 événements conservés, chaîne valide, aucun échec d’écriture. |
| `MEM-001` | Payload mémoire altéré | PASS | PASS | L’altération déclenche une erreur CRC; le payload retourné est nul et n’est pas approuvé. |
| `MESH-003` | Trois règles structurellement invalides | PASS | PASS | Aucun enregistrement invalide n’est persisté. |
| `CERT-001` | Certificat valide et conclusion falsifiée | PASS | PASS | Le certificat valide est accepté; la conclusion modifiée et re-hachée est rejetée faute d’entailment. |
| `TYPE-001` | 10 formes JSON via identité typée `Any` | PASS | PASS | Aucune erreur sur les formes testées. |
| `SEC-001` | Injection de code fournie comme texte | PASS | PASS | La chaîne reste une donnée inerte; aucun code système n’est exécuté. |
| `ROBUST-001` | AST de 1 200 niveaux | FAIL | PASS | V0 laisse remonter `RecursionError`; V1 renvoie `Rejected` avec raison de profondeur et événement de trace. |
| `MESH-005` | Filtre de contexte multi-tenant | FAIL | PASS | V0 renvoie `alice` et `bob` pour le tenant alpha; V1 ne renvoie que `alice`. |
| `MESH-006` | Jointure sans résultat, plafond de comparaison = 1 | FAIL | PASS | V0 effectue 33 330 appels de matching et indique à tort `FIXPOINT_REACHED`; V1 effectue 1 comparaison, signale `BUDGET_EXHAUSTED` et ne produit aucun fait. |
| **Total** | **15 scénarios indépendants** | **8 PASS / 7 FAIL** | **15 PASS / 0 FAIL** | **Les sept classes de défaut reproduites ont des tests de non-régression.** |

La suite de tests de développement V1 contient **65 tests : 65 réussites, 0 échec, 0 erreur**, avec `ResourceWarning` transformé en erreur. Les parcours smoke CLI et HTTP contiennent chacun six vérifications; les reçus détaillés et leurs journaux sont conservés séparément. Les résultats ci-dessus décrivent ce que ces tests mesurent; ils ne prouvent pas la correction pour toute entrée concevable.

## 6. Interprétation des résultats

Les défauts V0 n’étaient pas de simples différences de score : ils affectaient respectivement la sémantique d’identité du maillage, la porte d’activation d’un modèle prédictif, les gardes de ressources, la robustesse du runtime, la confidentialité contextuelle de requêtes et la garantie de bornage d’une recherche. Le fait que les 54 tests livrés antérieurement réussissent n’avait pas détecté ces cas limites. C’est pourquoi V1 ajoute des régressions directement dérivées des défauts constatés, sans intégrer les réponses métier de l’expérience au moteur.

Pour V1, les mêmes cas et la même graine passent, y compris depuis l’extraction propre de l’archive finale. Les invariants corrigés sont couverts par les tests nommés dans `NGeGenBrain_v1_mise_en_oevre.json`; les données brutes sont stockées dans `hard_benchmark_v1_final.json` de l’archive d’audit. Le benchmark est fini : il ne couvre pas toutes les attaques, tous les ordres de concurrence, tous les contextes, tous les types personnalisés ni tous les programmes possibles.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

### Théoriques

La théorie 3 explicite l’identité typée/contexualisée du fait, la validation numérique du budget, la borne sur les explorations partielles des jointures, la porte de type de sortie du modèle du monde et le rejet typé d’AST invalides. Les preuves associées sont conditionnelles à l’exhaustivité des validateurs et au passage de toutes les voies d’exécution par ceux-ci. La théorie n’est pas prétendue machine-vérifiée globalement.

### Conceptuelles

La pertinence d’une valeur ne suffit pas à justifier un fait de type différent. Une égalité d’octets n’annule pas une violation de contrat. Un plafond de recherche doit compter le travail effectué même quand aucune solution ne sort. Les prédictions simulées et les mesures d’observation restent distinctes. Ces règles sont maintenant représentées dans le code plutôt que seulement dans le discours.

### Opérationnelles

V1 rejette explicitement les budgets non finis et certaines entrées AST au-delà de la politique de profondeur/structure. La recherche qui épuise son plafond renvoie `BUDGET_EXHAUSTED`, sans prétendre reprendre là où elle s’est arrêtée sans checkpoint du front. Les usages doivent consulter le statut et la trace, pas seulement la présence d’une valeur. Les requêtes multi-tenant doivent fournir leur contexte explicite.

## 8. Limites et risques résiduels

- L’argument d’expressivité du noyau est relatif et conditionnel; ce dépôt ne fournit ni preuve machine globale ni compilateurs pratiques pour chaque langage de programmation existant.
- Les sources exécutables historiques ASCR/AAM n’étaient pas disponibles. ASCR-NG reste une reconstruction de rôle; l’équivalence historique n’est pas démontrée.
- Le benchmark de 15 cas est un stress test indépendant utile, mais il n’est pas une campagne complète de fuzzing, de model checking, de test distribué ou de sécurité en production.
- La prévalidation actuelle utilise des seuils opérationnels documentés pour éviter les exceptions brutes; elle ne doit pas être interprétée comme une preuve que les AST de profondeur supérieure sont sémantiquement impossibles. Une augmentation de capacité doit être accompagnée d’une stratégie d’exécution adaptée.
- Le runtime Python n’a pas pu être embarqué car le téléchargement officiel a échoué dans l’environnement de génération. Python 3.11+ est requis; les lanceurs `.bat` ont été analysés statiquement, pas exécutés dans un Windows natif.
- Le modèle du monde utilise une politique statistique d’activation; elle requiert un holdout indépendant et représentatif et ne constitue pas un théorème causal.

## 9. Conclusion

L’audit a détecté sept défauts dans le paquet V0 malgré sa suite livrée verte. Ils ont été reproduits par un banc indépendant, corrigés dans V1, puis couverts par des régressions; les mêmes quinze scénarios ont passé sur la copie V1 et la régression complète V1 a atteint 65/65. La livraison définitive exige en plus que l’archive Dmodel construite à partir de ces sources soit extraite et testée par son hash exact, avec ses reçus archivés.

## 10. Statut du modèle

**Statut : V1 corrigée et testée dans le périmètre déclaré, y compris par extraction propre du ZIP final.** Ce statut n’affirme ni une absence absolue de défauts, ni une équivalence non prouvée avec les artefacts historiques indisponibles, ni la validation native Windows. Le reçu de clean-room associe les résultats au SHA-256 exact de l’archive finale dans le paquet Amodel. Les échecs V0 sont conservés dans l’audit et ne sont pas effacés par le succès V1.
