# Manuel complet de programmation compositionnelle dans AAM O94.6

## 1. L'idée en une phrase

La programmation compositionnelle consiste à **construire un programme en assemblant des briques aux contrats explicites**, plutôt qu'à écrire tous les détails du programme dans un seul bloc monolithique. Une brique réalise une action précise; une composition décrit l'ordre, les données et les conditions qui relient ces actions.

C'est proche d'un atelier : les briques sont des outils vérifiables, le graphe est le plan d'assemblage, le compilateur transforme le plan en artefact exécutable, et les tests vérifient le résultat. Une composition n'est fiable que si ses briques de base, préconditions, effets, erreurs et sorties sont eux-mêmes fiables.

## 2. Ce que le terme signifie dans AAM

O94.6 expose deux surfaces différentes dans l'onglet **Programmation par composition**. Elles ne doivent pas être confondues.

### 2.1 Graphe de compétences (compatibilité historique)

Le sous-onglet `Graphe de compétences` permet de composer des compétences déjà répertoriées, d'enregistrer et d'exécuter un graphe versionné. Le bouton `Compiler → JSON` valide/enregistre la forme déclarative du graphe : ce n'est pas à lui seul un compilateur Python général. Les sorties correspondent aux appels de compétences bornées exposées par le runtime.

### 2.2 Compilateur de programmes exécutables

Le sous-onglet `Compilateur de programmes réels` prend une composition JSON versionnée, vérifie son schéma, résout les références à des composants approuvés, produit une source Python, la compile en bytecode CPython et peut exécuter le programme avec une confirmation séparée. Le DSL n'accepte pas d'imports utilisateur ni de fragments Python arbitraires. Il ne permet donc pas à un auteur de composition de glisser directement une réponse attendue dans un fragment Python caché.

Les programmes compilés utilisent les droits du compte qui exécute AAM. **Ce n'est pas un bac à sable (sandbox)** : vérifiez workspace, chemins, opérations d'écriture et cible avant de confirmer une exécution.

## 3. Vocabulaire de base

- **Brique de base / composant** : action de faible niveau enregistrée et disposant d'un identifiant stable (ex. inventorier un dossier, vérifier une requête, compiler un fichier, attacher l'intégrité à un résultat).
- **Méthode** : procédure réutilisable qui organise plusieurs actions (ex. vérifier un projet avant de permettre son exécution).
- **Règle** : contrainte qui détermine quand une branche est autorisée ou quel statut doit être produit.
- **Composition** : assemblage d'invocations, séquences, conditions et boucles sur les sorties précédentes.
- **Entrée** : paramètres donnés au début de la composition (`workspace`, `inventory_limit`, chemin de projet, etc.).
- **Sortie nommée** : valeur produite par une brique et référencée ensuite par une expression `var`.
- **Artefact compilé** : source Python, bytecode, manifeste avec empreintes et rapport de compilation.
- **Trace** : explication des étapes exécutées, statuts et sorties qui aident au diagnostic.
- **Vérificateur indépendant** : programme de test séparé qui calcule ce que la sortie devrait signifier à partir des entrées, sans donner cette valeur au runtime lors de l'exécution.

## 4. Composition d'exemple réellement livrée

Spécification source :

`examples/compositions/O94_6_project_quality_gate.json`

SHA-256 : `8af6f0e7233f50752f14d84e0c0a936e1d6390d29f826093872475ecca7ae7cf`.

Cette composition contient 10 nœuds et utilise trois catégories de brique approuvées :

1. `workbench.validate_request` — valider qu'une requête de construction est recevable;
2. `workbench.dispatch` — lancer une action de l'atelier, comme inventaire, compilation de fichiers Python ou tests de projet;
3. `result.attach_integrity` — créer un résultat avec les métadonnées d'intégrité et les hashes.

### 4.1 Schéma logique simplifié

```text
Entrée : workspace + inventory_limit
        |
        v
validate_request(build_project)
        |
        v
list_files(workspace, limit)
        |
        v
POUR CHAQUE fichier de l'inventaire
   |-- suffixe .py --> workbench.dispatch(check_python)
   |-- autre suffixe -> result.attach_integrity(path, size, suffix)
        |
        v
workbench.dispatch(build_project)
        |
        v
workbench.dispatch(test_project, confirmation explicite)
        |
        v
result.attach_integrity(résultats + manifestes)
        |
        v
Reçu JSON final, erreurs et hashes
```

### 4.2 Exemple de structure JSON (extrait pédagogique)

Ce fragment illustre une invocation avec une variable d'entrée et une sortie nommée. Le fichier source complet reste la référence; n'utilisez pas ce fragment isolément en espérant compiler toute la composition.

```json
{
  "kind": "invoke",
  "component_id": "workbench.dispatch",
  "inputs": {
    "request": {
      "object": {
        "workspace": {"var": "input.workspace"},
        "action": {"literal": "list_files"},
        "limit": {"var": "input.inventory_limit"}
      }
    }
  },
  "output": "inventory"
}
```

`literal` est une valeur inscrite dans le graphe; `var` est une référence au contexte d'exécution. Une brique suivante peut ainsi utiliser `inventory.files` sans connaître à l'avance les noms de fichiers qui seront effectivement trouvés.

## 5. Pas à pas : exécuter la composition

### Préparer l'environnement

Depuis la racine O94.6 :

```bash
python scripts/preflight_o946.py
```

Si le préflight ne retourne pas `PASS_BOUNDED`, arrêter l'expérience et lire le reçu/diagnostic avant de compiler.

### Exécuter le contrôle compositionnel complet

```bash
python scripts/o946_run_composition_quality_gate.py \
  --project-root examples/compositions/O94_6_quality_gate_demo \
  --variant-limit 2
```

Le script :

1. charge le JSON source;
2. valide le schéma et les références de composants;
3. compile vers source Python et bytecode;
4. exécute la composition avec une confirmation explicite et un chemin cible déclaré;
5. construit l'inventaire et compile les fichiers Python du projet;
6. lance les tests du projet;
7. écrit un reçu de compilation/exécution avec les hashes;
8. modifie une variante du graphe (`variant-limit=2`) et compare le comportement;
9. fait vérifier indépendamment l'inventaire/actions par un autre calcul à partir du fichier `data/assets.json`.

### Exécuter directement le projet cible

```bash
cd examples/compositions/O94_6_quality_gate_demo
PYTHONPATH=src python -m assetops.cli --input data/assets.json --max-overdue-days 3
```

Exemple de compteurs JSON produits :

```json
{
  "asset_count": 4,
  "action_counts": {
    "AUDIT_DUE": 1,
    "AUDIT_OVERDUE": 1,
    "HOLD_DISPATCH": 1,
    "MONITOR": 1
  },
  "status": "PASS_BOUNDED"
}
```

La sortie complète est enregistrée dans `real_task_tests/O94_6_replay/evidence/composition_quality_gate/direct_cli_execution.json`.

## 6. Comment lire le résultat d'exécution

Données du projet :

| ID | Dépôt | Dernier audit, jours | Intervalle, jours | Calcul | Action |
|---|---|---:|---:|---:|---|
| LM-204 | Cedar | 14 | 9 | 14 − 9 = 5 jours en retard | `HOLD_DISPATCH` (seuil de maintien > 3 jours) |
| VX-318 | Juniper | 18 | 17 | 18 − 17 = 1 jour en retard | `AUDIT_OVERDUE` |
| QR-509 | Alder | 28 | 28 | 28 − 28 = 0 | `AUDIT_DUE` |
| TS-404 | Birch | 7 | 12 | échéance dans 5 jours | `MONITOR` |

Le résultat n'est pas évalué par « le programme dit qu'il a réussi ». Un vérificateur indépendant recalcule les deltas et les statuts depuis le JSON d'entrée et les compare au JSON de sortie. Le reçu montre 4/4 lignes conformes, 6 fichiers Python compilés, aucun échec de compilation et les tests du projet passés. Le but ici est de tester la construction et l'exécution auditables d'un outil défini, pas de faire passer un exemple métier pour un système de décision prêt à contrôler des équipements réels.

## 7. Modifier la composition

1. Faire une copie du fichier JSON source; ne pas écraser le témoin historique.
2. Donner un nouveau nom au champ `name`.
3. Modifiez une règle observable, par exemple `inventory_limit`, le filtre de suffixes, une séquence d'invocations ou le format du reçu.
4. Gardez les identifiants de briques sous leur forme exacte. Un identifiant inconnu doit provoquer une erreur de validation et non être exécuté comme du code.
5. Compilez la copie et inspectez le diff source/manifeste.
6. Exécutez avec un workspace jetable et une confirmation explicite.
7. Testez au moins : entrée nominale, liste vide, chemin inexistant, fichier Python invalide, test en erreur, timeout, workspace en lecture seule et variante modifiée.
8. Recalculez les sorties attendues **à partir des entrées de test par un script d'évaluation séparé**.
9. Enregistrez source, entrée, sortie, stderr, statut, durée, hashes et code de retour. Ne supprimez pas le reçu quand un test échoue.

### Exécuter les tests de non-régression du compilateur/workbench

```bash
xvfb-run -a python -m pytest -q tests/test_o945_composition_compiler_workbench.py -vv --tb=short
```

Pour la preuve de compilation/exécution multi-fichiers :
`real_task_tests/O94_6_replay/evidence/composed_editor_build_test.json`.

## 8. Atelier de code (éditeur multi-fichiers)

Depuis l'onglet « Programmation par composition », cliquez **Ouvrir Atelier de Code**. L'atelier permet d'ouvrir plusieurs fichiers en onglets, de modifier et sauvegarder les fichiers, d'inspecter le projet, compiler ses sources Python, exécuter les tests puis lancer une commande explicite. La sauvegarde atomique et les contrôles de conflit évitent d'écraser silencieusement une version externe modifiée.

Conseil de test : créez un mini-projet dans un nouveau dossier, avec un fichier de logique, un module de données et des tests séparés. Construisez d'abord en mode compilation/tests, vérifiez les fichiers générés, et seulement ensuite exécutez. Le bouton d'exécution ne crée pas un environnement isolé; aucun secret ni document de production ne doit se trouver dans le workspace d'une cible expérimentale non fiable.

## 9. Comment éviter de confondre réutilisation et invention autonome

Le programme d'exemple est une cible indépendante d'évaluation. AAM l'a compilé et a orchestré son inventaire/tests au moyen de briques approuvées; ce n'est pas une preuve que le modèle a spontanément inventé le code complet du projet à partir d'une phrase en langage naturel. Pour tester l'invention autonome, concevez un benchmark différent : donnez une spécification fonctionnelle sans code, gardez les tests d'acceptation hors de la zone visible par AAM, faites générer une solution, puis exécutez ces tests cachés. Rapportez succès/échec et les modifications sans déplacer l'oracle dans le runtime.

## 10. Pourquoi la programmation compositionnelle pourrait-elle être le futur ?

C'est plausible parce qu'elle rend la structure explicite, favorise la réutilisation, donne des interfaces testables et permet d'auditer des effets et une provenance. Elle est particulièrement adaptée aux pipelines de données, tâches d'entreprise et orchestration d'outils. Mais aucune méthode n'est un avenir garanti : les graphes deviennent difficiles à comprendre à grande échelle, les contrats peuvent évoluer, et les algorithmes serrés ou les abstractions de langage bénéficient souvent de code traditionnel. La trajectoire la plus robuste est probablement **un mélange** : composants et workflows composés, avec du code conventionnel pour la logique spécialisée, tous deux soumis à tests, versions, analyse statique et preuves de comportement.
