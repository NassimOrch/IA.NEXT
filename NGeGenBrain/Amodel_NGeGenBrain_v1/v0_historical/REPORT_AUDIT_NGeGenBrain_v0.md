# Rapport d’audit et de mise en œuvre — NGeGenBrain_v0

**Version applicative :** `0.3.0`  
**Environnement de génération :** `NGeGenBrain_v0_work_1`, Linux, Python 3.13.5  
**Formalisme normatif original :** `formalism/theorie_programation_compositionnelle_NG_0.tex`  
**Formalisme intégré et complété :** `theorie_programation_compositionnelle_3.tex`  
**Matrice exigence → code → tests :** `NGeGenBrain_v0_mise_en_oevre.json` — 95 entrées  
**Registre de preuves :** `preuves_NGeGenBrain_v0.json`

## 1. Description

NGeGenBrain_v0 est un runtime local de programmation compositionnelle. Les programmes utilisateur sont des AST JSON déclaratifs, validés avant interprétation. Le système combine un catalogue de composants versionnés, des contrats et capacités, un moteur d’exécution avec résultats typés, un maillage stratifié de faits et règles multi-prémisses, des opérateurs, des certificats revalidés, une mémoire persistante, une trace append-only chaînée par hash, un gestionnaire ASCRC, un mécanisme de récupération ASCR-NG reconstruit, une synthèse bornée/reprenable, un modèle du monde à sorties simulées, des intentions déclaratives ainsi qu’un CLI, une API HTTP locale et une interface web partageant le même registre d’actions.

Le code n’utilise pas `eval` ou `exec` pour interpréter les programmes utilisateur. Il n’y a pas de dépendance Python tierce déclarée. Un interpréteur Python 3.11+ est néanmoins requis. Le runtime Windows binaire n’est pas inclus dans l’archive : le conteneur de construction n’a pas pu résoudre `www.python.org`. Le bootstrapper vérifie l’archive officielle par SHA-256 avant extraction, mais son installation native reste à tester sur Windows.

## 2. Architecture

1. **Registre et contrat** — `src/ngegenbrain/contracts.py`, `operators.py` : signatures typées, versions, préconditions, postconditions, effets, capacités et ressources.
2. **Sémantique du programme** — `engine.py`, `results.py` : dispatch des constructeurs AST, budget, état, erreurs/résultats typés, garde-fous et trace.
3. **Maillage** — `mesh.py`, `store.py` : faits typés, règles multi-prémisses, unification, dérivations, provenance, certificats recalculés et invalidation transitive.
4. **Persistance, mémoire et événements** — `store.py` : SQLite, chaînes de trace, checkpoints, veille/réveil, résumés liés à leur source, événements avec TTL/déduplication et transactions locales.
5. **Régulation et évolution** — `ascr.py`, `ascrc.py`, `synthesis.py`, `world_model.py`, `intents.py` : retrieval reconstruit, allocation/activation, candidats reprenables, prédictions `SIMULATED` et intentions déclaratives typées.
6. **Façades** — `cli.py`, `actions.py`, `web.py`, `web/` : 51 actions communes ; le CLI, l’API et l’interface web délèguent au même `ActionService`.
7. **Audit** — `NGeGenBrain_v0_mise_en_oevre.json`, `preuves_NGeGenBrain_v0.json`, `docs/FORMALISM_AUDIT.md`, reçus JSON, journaux et tests.

### Provenance et fidélité aux sources

Le formalisme NG_0 est conservé séparément et inchangé. Le document eGenBrain v4 sert de source pour le maillage typé, les hyperrègles, opérateurs, statuts épistémiques et certificats. Le runtime historique ASCR/AAM n’était pas disponible : `ASCR-NG` remplit le rôle documenté de récupération et de classement de candidats, mais aucune équivalence comportementale historique n’est revendiquée. AAM n’est pas une dépendance d’exécution : le maillage, les règles et les certificats nécessaires sont implémentés dans le runtime local. Toute adaptation restante est identifiée par sa portée dans la matrice et le registre de preuves.

## 3. Pipeline complet d’exécution

1. Lire l’entrée et conserver sa représentation; vérifier que le programme est une donnée AST conforme et non du code source libre.
2. Résoudre les composants et versions depuis le registre, puis vérifier types, contrats, préconditions, capacités et budgets.
3. Évaluer les constructeurs de contrôle, valeurs, effets et résultats selon `engine.py`; un résultat inconnu, partiel, rejeté, périmé ou épuisé n’est pas promu silencieusement en succès.
4. Contrôler les postconditions et enregistrer résultat, coûts, dépendances, événements et provenance.
5. Pour le maillage, unifier les faits typés avec les règles actives, évaluer les opérateurs déclarés, construire un certificat, puis vérifier les prémisses et la conclusion sans se contenter du hash.
6. Pour une transaction, borner l’atomicité au même stockage SQLite. Les effets externes non couverts sont refusés avant exécution dans ce chemin transactionnel ; un rollback local ne prétend pas annuler un effet distant.
7. Pour la mémoire, vérifier intégrité, schéma, versions et dépendances au réveil. Un résumé approximatif conserve un lien vers sa source ; les objets révoqués/périmés ne sont pas utilisables comme prémisses certifiées.
8. Pour ASCRC, appliquer les contraintes de sûreté avant le classement heuristique. Le score ne constitue pas une preuve et ne modifie pas le statut épistémique.
9. Pour la synthèse, générer des candidats dans la grammaire déclarée sous budget; conserver le curseur et les candidats éliminés. La sortie reste candidate tant qu’un vérificateur indépendant ne l’a pas validée.
10. Pour le modèle du monde, afficher `SIMULATED` et évaluer séparément sur holdout contre une baseline. Une petite quantité de données ou la cohérence interne ne suffit pas à activer le modèle.
11. Pour le chat, résoudre une intention et des slots explicitement déclarés. Une ambiguïté reste non résolue ; l’interprétation de texte ne confère pas de capacité sensible.
12. Enfin, produire les reçus de vérification ; le scoring de références ne fait pas partie du chemin qui génère la réponse testée.

## 4. Commandes d’exécution reproductibles

Toutes les commandes se lancent depuis la racine après extraction :

```sh
python3 ngbrain.py init
python3 ngbrain.py status
python3 ngbrain.py actions
python3 ngbrain.py verify
python3 ngbrain.py run --program examples/add.json --input null --capabilities '[]' --budget 1000
python3 ngbrain.py action system.actions --data '{}'
python3 ngbrain.py test
python3 ngbrain.py demo
python3 ngbrain.py serve --host 127.0.0.1 --port 8765
python3 scripts/validate_release.py
python3 scripts/smoke_cli.py
python3 scripts/smoke_web.py
```

Sous Linux/macOS, `sh scripts/run_tests.sh` réalise le test de régression. Sous Windows, `test_NGeGenBrain_v0.bat` exécute les tests et `launch_NGeGenBrain_v0.bat` démarre le serveur et ouvre le navigateur lorsque le port local répond HTTP 200. Les scripts `.bat` ont été contrôlés statiquement ici ; faute de `cmd.exe` et PowerShell dans l’environnement Linux, ils ne sont pas déclarés testés nativement.

## 5. Résultats observés

### 5.1 Suite automatisée

Le reçu `audit/test_receipt_final.json` et le journal `logs/test_run_20261027_final_54.log` indiquent **54 tests réussis, 0 échec et 0 erreur** sur Python 3.13.5 avec `ResourceWarning` traité comme erreur. Les domaines couverts comprennent typage et contrats, capacité/sandbox, AST, arithmétique exacte, dimensions, résultats partiels/indéterminés, falsification de certificat, règles non implicites, invalidation transitive, veille/réveil, vagues/TTL, budgets, checkpoints, rollback/commit SQLite, synthèse/reprise, ASCRC, modèle du monde, intentions, version runtime, bootstrap Windows statique et parité des actions.

### 5.2 CLI et HTTP

Le reçu `audit/cli_smoke_receipt.json` enregistre **6/6 commandes** sur une base nouvellement créée : initialisation, état, catalogue, exécution d’un AST d’exemple, vérification de base et lecture d’action. Le résultat de l’AST est `Success`, les 51 identifiants d’action sont uniques et la vérification SQLite répond `valid=true`. Le reçu `audit/web_smoke_receipt.json` enregistre **6/6 contrôles HTTP** avec statut 200 sur la racine HTML, l’asset JavaScript, le catalogue, la santé, la vérification de la base et un POST d’action. Ces contrôles ont été exécutés par les outils du dépôt sous Linux.

### 5.3 Traçabilité et validateur

La matrice générée contient **95 entrées** dont **46 lignes de constructeurs AST** et couvre les **51 actions**. Le générateur du registre de preuves rapporte **0 chemin de code manquant** et **0 identifiant de test invalide**. Le validateur `scripts/validate_release.py` recalcule les empreintes, vérifie les références source/test, la cohérence de version, les reçus, le registre d’actions, la syntaxe Python, l’absence des appels directs `eval`/`exec` dans le runtime inspecté et les contrats statiques Windows. Le validateur passe **25/25 contrôles, 0 échec** (`audit/release_integrity_check.json`) ; les précédents échecs y sont conservés séparément dans `logs/`.

### 5.4 Portabilité et archive

Le bootstrapper cible le fichier officiel `python-3.14.10-embed-amd64.zip`, avec le SHA-256 `90905e64a840557d8c1bc4f5b74db3d7ee85e3ffb217611cac1c7813acea4159`, lié depuis la page de publication Python 3.14.10 : <https://www.python.org/downloads/release/python-31410/>. Le téléchargement a été tenté par shell et un second mécanisme mais le DNS vers `python.org` a échoué ; le binaire n’est donc pas inclus et l’installation native Windows demeure ouverte. Ce n’est pas présenté comme un succès de bootstrap.

Le contrôle de release suit `tools/build_release_archives.sh` : chaque archive est vérifiée par `unzip -t`, sa taille est comparée au plafond de 200 MiB et les empreintes SHA-256 sont écrites dans `SHA256SUMS_NGeGenBrain_v0.txt`. Le paquet D a été extrait de nouveau dans un dossier propre après le dernier correctif : **54/54 tests runtime, validateur 25/25, 6/6 commandes CLI et 6/6 contrôles HTTP**. Le reçu clean-room conserve le SHA-256 exact de cette archive testée. Le reçu exact — notamment le hash de l’archive testée, le chemin d’extraction et les journaux — est conservé dans `audit/cleanroom_test_receipt.json` de l’archive de suivi/audit. Le premier essai lancé un niveau trop haut dans l’arborescence est conservé comme erreur de procédure ; aucun test n’y avait été exécuté. Le reçu clean-room final indique l’empreinte exacte du Dmodel testée, et doit coïncider avec le hash du ZIP dans `SHA256SUMS_NGeGenBrain_v0.txt`. Le runtime Python n’est pas inclus : le paquet ne dépend d’aucune bibliothèque PyPI mais nécessite Python 3.11+ ou le bootstrap Windows avec accès réseau. Les `.bat` sont contrôlés statiquement mais n’ont pas été exécutés sous Windows natif dans cet environnement Linux.

## 6. Interprétation des résultats

Ces essais établissent le comportement des chemins et entrées effectivement testés. Ils ne constituent pas une démonstration d’absence absolue de défauts. La présence de hash détecte certaines modifications et la vérification de certificats reconstruit la conclusion dans le fragment supporté ; aucune des deux ne prouve la vérité du contenu indépendamment de ses prémisses. La parité CLI/web démontre l’usage d’un catalogue unique pour les actions, pas une équivalence universelle entre texte naturel et programme arbitraire.

## 7. Conséquences

### Théoriques

La théorie 3 complète NG_0 sur transactions locales, modèle du monde, intentions typées, portabilité, provenance des preuves et protocole de mise en œuvre. Les arguments algébriques et d’expressivité restent conditionnels aux hypothèses écrites et ne sont pas vérifiés par un assistant de preuve. Le runtime implémente un fragment exécuté et contrôlé, pas un compilateur complet de chaque langage de programmation classique.

### Conceptuelles

Composition du programme, maillage de faits, provenance, effets, activation et preuve sont reliés, sans être confondus. Une pertinence n’est pas la vérité, un candidat n’est pas certifié, la veille ne réfute pas et un résultat simulé ne devient pas observation. Les limites d’implémentation sont formulées par portée, pas masquées comme capacités héritées.

### Opérationnelles

Le programme est local, sans services en ligne de runtime, et utilise SQLite. Les données résident dans le profil utilisateur ou une base `--db` explicitement fournie. `Txn` n’est atomique que pour les effets locaux pris en charge ; `Par` est actuellement sérialisé après analyse conservatrice ; le bootstrap Windows nécessite accès réseau ou un interpréteur existant. Ces points sont explicitement documentés et testés statiquement ou dynamiquement dans la mesure disponible.

## 8. Conclusions et statut du modèle

**Statut : runtime intégré dans le périmètre de code et de tests décrit ; 54/54 tests runtime, 6/6 commandes CLI et 6/6 contrôles HTTP sont passés.** La couverture est reliée à 95 entrées de traçabilité. Les trois ZIP ont passé le contrôle CRC et restent sous 200 MiB ; les tailles et SHA-256 sont publiés dans `SHA256SUMS_NGeGenBrain_v0.txt`. Le paquet D a été retesté depuis une extraction propre. La validation native Windows n’est pas acquise dans l’environnement courant. Les obligations ouvertes de preuve machine, équivalence ASCR historique, concurrence, effets distribués et compréhension libre universelle restent déclarées.

Ce rapport ne prétend pas qu’un logiciel est garanti sans défaut possible. Il fournit la chaîne d’évidence et ses limites de façon vérifiable afin que les tests puissent être réexécutés sur le poste cible.
