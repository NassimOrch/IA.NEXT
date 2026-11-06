# P10 — CLI et interface graphique locale : rapport de validation

**Statut de phase : PASS selon les critères P10 mesurés.** Les éléments d'interface encore partiels/non connectés et les vérifications manuelles d'accessibilité restent explicitement listés dans la matrice; ils ne sont pas présentés comme terminés.

## 1. Description

P10 fournit une surface CLI pour diagnostiquer, inventorier les composants et spécialistes, valider et exécuter un AST JSON, lancer/reprendre une recherche CEGIS, gérer la mémoire durable, prévisualiser ASCRC, exporter/vérifier l'audit, observer des données locales et démarrer l'interface web locale. La GUI utilise les mêmes API applicatives et contrats que le CLI.

## 2. Architecture

- **CLI** : `src/fullegenbrain/cli.py`, commandes explicites, données/audit sous `--data-dir`; sorties JSON et codes de retour définis par le contrat.
- **Application/runtime** : `FulleGenBrainApplication`, interpréteur AST fermé, validateur statique et adaptateurs spécialisés versionnés.
- **GUI** : `src/fullegenbrain/webapp.py` avec `web/index.html`, `web/app.js` et `web/style.css`; endpoints séparés pour health, composants/adaptateurs, mémoire/tâches, validation/exécution, synthèse/reprise, observation, ASCRC, spécialistes, dataset, évaluation, diff de composition, quarantaine et audit.
- **Stockage** : SQLite local; l'évaluation report-only utilise un magasin éphémère par cas et n'altère pas la mémoire persistante.
- **Sécurité réseau** : liaison loopback uniquement, validation de l'en-tête Host, POST same-origin, `Content-Type` JSON exigé, corps borné, CSP et assets locaux, aucun CDN ni LLM/RAG externe implicitement configuré.
- **Preuves UI** : `spec/evidence/ui_acceptance_matrix.json` réconcilie les IDs UI-01 à UI-20 avec tests ou preuves documentaires et énonce séparément les statuts partiels/non connectés.

## 3. Pipeline complet

1. Le CLI ou HTTP reçoit une requête JSON dans une limite de taille.
2. Les entrées sont contrôlées avant tout effet : type, forme, références, contrats, capacités, split de dataset et collisions pertinentes.
3. Le runtime renvoie statut, diagnostic, empreinte et trace; les statuts partiels/bloqués/non résolus ne sont pas promus automatiquement.
4. Les tâches sont persistées localement; une évaluation report-only isole chaque cas et n'écrit pas dans la mémoire persistante ni ne choisit/promet un candidat.
5. L'export d'audit masque les contenus/commandes sensibles selon le contrat UI.
6. Chaque exécution contrôlée conserve stdout/stderr, code retour, hashes, reçu et point de sauvegarde.

## 4. Commandes d'exécution

Depuis la racine du projet :

```sh
python3 scripts/preflight.py --read-only-check
PYTHONPATH=src PYTHONWARNINGS=error::ResourceWarning python3 -m pytest -q -W error::ResourceWarning tests/test_p10_cli_gui.py tests/test_p10_cli_ui.py
PYTHONPATH=src PYTHONWARNINGS=error::ResourceWarning python3 scripts/check_cli_documented_examples.py
PYTHONPATH=src PYTHONWARNINGS=error::ResourceWarning python3 -m pytest -q -W error::ResourceWarning tests
PYTHONPATH=src python3 -m fullegenbrain --data-dir ./data serve --host 127.0.0.1 --port 8765
```

Les commandes de validation CI-like ont été lancées via `scripts/run_checked.py`. Les reçus y enregistrent les commandes et les retours exacts; le gate machine-readable est `spec/evidence/P10_acceptance_gate.json`.

## 5. Résultats

- Tests P10 CLI/GUI : **40 passés**; `ResourceWarning` est traité comme erreur.
- Smoke CLI sur dossier de données neuf : **18 commandes** documentées exécutées et consignées; les statuts bornés de synthèse/reprise sont rapportés tels quels, sans affirmation de correction universelle.
- Régression globale à la clôture P10 : **253 tests passés et 166 sous-tests passés**.
- Gate indépendant : PASS, **20 IDs UI uniques**, **24 références de preuve résolues**, reçus requis présents, 0 erreur ouverte.
- Vérifications réseau/interface : tests same-origin/Content-Type, host non-loopback refusé, corps HTTP borné, assets locaux sans CDN; connecteurs externes non configurés.

## 6. Interprétation des résultats

Ces résultats valident le contrat testé pour le CLI et l'interface locale dans cette révision, sur les fixtures et le runtime présents. Ils ne démontrent pas une correction universelle des programmes générés. La matrice UI distingue explicitement : 10 critères IMPLEMENTED, 1 IMPLEMENTED_OFFLINE_DEFAULT, 1 PARTIAL_JSON_ONLY, 2 NOT_CONNECTED, 1 INSPECT_ONLY, 1 NOT_CONNECTED_EXTERNAL_CONNECTORS_DISABLED, 1 STRUCTURAL_DIFF_ONLY, 1 audit manuel d'accessibilité, 1 audit responsive manuel et 1 PROMOTION_NOT_ENABLED. Ces états restent des gaps visibles plutôt que des succès fictifs.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

### Théorique

L'interface n'ajoute pas de sémantique au moteur : elle expose les statuts, contrats, effets et preuves du runtime. Les exemples cachés holdout/test ne pilotent pas la sélection du candidat.

### Conceptuelle

Observation, tâche enregistrée, exécution, statut épistémique, test sur un périmètre, preuve universelle et non-résolution restent distincts.

### Opérationnelle

La GUI est locale/offline par défaut et l'évaluation est isolée. Les capacités d'entraînement complet, connecteurs LLM/RAG, clonage exécutable, promotion et audits manuels d'accessibilité restent explicitement non connectés ou incomplets dans la matrice d'acceptation.

## 8. Conclusions


## 9. Statut du modèle

**P10 PASS.** Les critères de surface CLI/GUI, tests, sécurité locale, documentation et traçabilité UI sont satisfaits selon le gate. P11 — robustesse/sécurité/performance — est l'étape suivante autorisée. Cette clôture de phase n'affirme ni que tous les spécialistes historiques sont complets ni que FulleGenBrain est une preuve formelle universelle; ces revendications requièrent leurs phases et critères propres.

**P10 : PASS dans le périmètre documenté.** Les limites non connectées restent signalées dans la matrice UI.
