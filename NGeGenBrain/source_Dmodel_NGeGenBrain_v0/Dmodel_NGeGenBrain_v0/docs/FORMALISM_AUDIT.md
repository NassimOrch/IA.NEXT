# Audit du formalisme — NGeGenBrain_v0

## Objet et méthode

Cet audit compare `formalism/theorie_programation_compositionnelle_NG_0.tex`, le formalisme eGenBrain v4 (`formalism/formalime_eGenBrain_v4.tex`) et le complément de formalisation `theorie_programation_compositionnelle_3.tex` aux modules exécutables, actions, tests et reçus du dépôt. La matrice exhaustive de référence est `NGeGenBrain_v0_mise_en_oevre.json` et `preuves_NGeGenBrain_v0.json` (95 lignes de traçabilité dans cette révision). Chaque ligne indique la partie formelle, le chemin et le symbole d'implémentation, les tests qui l'exercent, le statut et la portée résiduelle.

La méthode ne confond pas présence de code et preuve. Les statuts distinguent les lignes exécutées dans la suite, les propriétés conditionnelles, les reconstructions documentaires, les limitations techniques explicites et les obligations théoriques encore ouvertes. Les échecs antérieurs restent dans `logs/` pour préserver l'audit.

## Description du modèle

Le runtime est un interpréteur d'AST JSON déclaratif, un registre de composants versionnés, un maillage typé de faits et hyperrègles, un moteur de dérivation avec certificats réévalués, un stockage SQLite avec événements chaînés par hash, un sous-système de mémoire, de vagues et de checkpoints, un synthétiseur à grammaire bornée et reprenable, une reconstruction de retrieval nommée ASCR-NG, un contrôleur ASCRC, des intentions déclaratives, un module d'évaluation de modèles du monde et des interfaces CLI/API/web partagées.

## Architecture

1. **Définition/registre** : `contracts.py` valide les identifiants, signatures, types, clauses de contrat, effets et modes d'implémentation admis.
2. **Exécution** : `engine.py` exécute les constructeurs AST, vérifie les capacités, les contrats et les budgets, et produit des résultats typés.
3. **Maillage** : `mesh.py` et `store.py` gèrent les faits, hyperrègles, unification, opérateurs de conclusion, certificats, provenance et révocation.
4. **Persistance/audit** : SQLite conserve composants, compositions, mémoire, checkpoints, événements, vagues, sessions de synthèse, candidats et évaluations. L'intégrité de base et la chaîne d'événements sont contrôlées séparément.
5. **Recherche/évolution** : `ascr.py`, `ascrc.py`, `synthesis.py`, `world_model.py` et `intents.py` traitent respectivement récupération, régulation, synthèse, prédiction/évaluation et interprétation déclarative de messages.
6. **Interfaces** : `ActionService` et `ACTION_DESCRIPTORS` sont le registre métier unique. Le CLI (`ngbrain.py`), l'API HTTP locale et l'explorateur web délèguent aux mêmes fonctions.

## Pipeline complet

1. Valider le schéma JSON et le nom d'action.
2. Résoudre le composant et la version depuis le registre.
3. Valider entrée/type/préconditions/capacités ; charger le budget.
4. Exécuter le nœud sous suivi des étapes, effets et ressources.
5. Valider la sortie/postconditions et conserver les statuts de résultat.
6. Écrire la trace et sa provenance ; les effets locaux sont transactionnels uniquement dans le domaine SQLite annoncé.
7. Pour une dérivation du maillage, résoudre les prémisses et contraintes, persister les conclusions dérivées et un certificat, puis permettre une vérification indépendante contre les faits/règles actifs.
8. Pour la mémoire, vérifier intégrité, version et dépendances avant le réveil ; les vues approximatives conservent un lien vers la source.
9. Pour ASCRC, appliquer les portes dures avant la priorité heuristique ; une priorité ou mise en veille ne change pas le statut épistémique.
10. Pour la synthèse, énumérer les candidats de façon paresseuse et reprendre un curseur vérifié ; la cohérence avec les exemples ne vaut pas preuve universelle.
11. Pour les modèles du monde, prédire avant d'exposer les cibles holdout au comparateur ; les prédictions demeurent `SIMULATED`.
12. Pour le langage naturel, résoudre un motif d'intention explicite et typé ; l'ambiguïté ou l'absence de motif est exposée, sans octroi de droits.
13. Persister les sorties et les statuts avant toute évaluation externe ; conserver les erreurs et les échecs de test.

## Commandes d'exécution et de contrôle

```sh
python3 ngbrain.py init
python3 ngbrain.py status
python3 ngbrain.py actions
python3 ngbrain.py verify
python3 ngbrain.py test
python3 ngbrain.py demo
python3 ngbrain.py serve --host 127.0.0.1 --port 8765
python3 ngbrain.py action system.actions --data '{}'
python3 ngbrain.py run --program examples/add.json --input null --capabilities '[]' --budget 1000
```

La documentation complète, avec les payloads d'exemple et le parcours web, est `docs/USER_GUIDE.md`.

## Résultats observés

Le reçu courant `audit/test_receipt_final.json` et son journal `logs/test_run_20261027_final_54.log` indiquent **54 tests réussis, 0 échec et 0 erreur** en 10.607 secondes sur Python 3.13.5, avec `ResourceWarning` traité comme erreur. Les journaux de tentatives précédentes et d’échecs intermédiaires restent conservés comme historique. Il inclut des tests unitaires, intégration HTTP/CLI, sécurité négative, tampering de certificat, intégrité de trace, rollback/commit, capacités, memory lifecycle, synthèse/reprise, ASCRC, modèles du monde et intentions.

Le registre d'actions décrit 51 actions partagées. Les tests confirment que les identifiants obtenus par le CLI et l'API web correspondent au même catalogue et que les ressources principales répondent en HTTP. Le test de reprise de synthèse vérifie la cohérence d'un curseur déterministe. Les tests eGenBrain vérifient notamment des dérivations à règle explicite, l'absence de règle inverse implicite et le rejet d'un certificat dont la conclusion a été falsifiée.

La passe élargie précédente a échoué sur des assertions de tests trop superficielles (résultat enveloppé, capacités explicitement requises). Le reçu correspondant est préservé sous `logs/test_failure_20261027_4.json`; après alignement des tests sur le contrat réel, les mêmes domaines repassent dans la suite finale.

## Interprétation des résultats

Le résultat des 54 tests de la suite finie établit le comportement des cas exécutés, pas la correction de tous les programmes AST possibles. Les tests de certificats établissent la vérification du fragment déclaratif implémenté, pas un assistant de preuve général. Les résultats de modèle du monde dépendent de la représentativité et de l'indépendance de l'échantillon holdout. L'intégrité cryptographique relie des contenus à des empreintes mais ne prouve pas leur vérité ou l'identité de l'émetteur.

## Conséquences théoriques

Le noyau offre une représentation compositionnelle générale et une sémantique opérationnelle avec types, effets, ressources, statuts, contrats et provenance. Le formalisme v3 a ajouté les obligations opérationnelles identifiées lors de l'implémentation : atomicité locale de `Txn`, statut de simulation pour le modèle du monde, protocole holdout, contrat de résolution des intentions et correspondance vérifiable entre formalisme, code et tests.

La théorie de l'expressivité de la machine à deux compteurs reste un argument relatif aux hypothèses d'encodage. Elle n'a pas été traduite en preuve machine du runtime Python. Il n'y a pas non plus de compilateur pratique livré pour chaque langage classique, ni de preuve de correction de toutes les traductions source→AST.

## Conséquences conceptuelles

Le maillage ne doit pas être pris pour une simple base de connaissances : le code distingue le graphe de faits, l'AST exécutable, les preuves, la provenance, l'activation, la mémoire et les effets. Réciproquement, la programmation compositionnelle ne se limite pas à une chaîne de fonctions : le runtime inclut contrôle, état, messages, mémoire, synthèse et transitions conditionnelles. Les scores de retrieval/synthèse/ASCRC ne peuvent pas hausser un candidat au statut de fait certifié.

## Conséquences opérationnelles

Le modèle est utilisable en local via un Python 3.11+ sans paquets tiers et une base SQLite persistante. L'interface ne requiert pas de service en ligne. L'exécution concurrente réelle de `Par` n'est pas implémentée : le moteur vérifie l'indépendance conservatrice puis sérialise les branches. Les effets hors SQLite ne sont pas couverts par l'atomicité locale. ASCR-NG est une reconstruction documentaire et ne revendique pas d'équivalence exacte avec une source historique absente. Le serveur embarqué est destiné au loopback local, non à l'exposition directe sur Internet.

## Conclusion

La livraison est couverte par un registre de traçabilité, des tests exécutables et un environnement reproductible. Le statut de l'implémentation est **fonctionnel dans le périmètre documenté et testé**, avec des obligations formelles/empiriques explicitement séparées. « Zéro anomalie sur toute exécution » n'est pas démontrable par une suite finie ; ce rapport n'en fait pas la promesse. Les lacunes d'équivalence historique, de compilation de langages existants, de preuve machine et de capacités distribuées sont formulées et conservées dans le registre au lieu d'être dissimulées.

## Statut du modèle

- **Exécutable** : oui, sous Python 3.11+.
- **Dépendances tierces** : aucune ; SQLite est fourni par Python.
- **Tests dans cet environnement** : consulter le reçu final et le journal associés ; le résultat est limité aux tests explicitement exécutés.
- **Parité des actions CLI/web/API** : vérifiée via le registre partagé et tests d'intégration.
- **Installation Windows** : fichiers `.bat` fournis ; le conteneur de construction est Linux, donc les scripts n'ont pas été exécutés par `cmd.exe` natif dans cet environnement.
- **ASCR historique** : runtime source absent ; ASCR-NG est une reconstruction du rôle de retrieval, non une équivalence démontrée.
- **Preuve machine du runtime** : non fournie ; les preuves mathématiques du texte sont conditionnelles et distinctes des tests.
- **État final** : livré avec les limites et obligations ci-dessus tracées, sans convertir un statut ouvert en succès déclaré.
