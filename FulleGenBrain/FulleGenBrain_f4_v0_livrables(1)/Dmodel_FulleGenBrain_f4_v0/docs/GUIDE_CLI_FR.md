# Guide CLI — FulleGenBrain_f4_v0

## 1. Pré-requis et lancement

Le runtime cible Python 3.11+ et privilégie la bibliothèque standard. Depuis le dossier qui contient `src/`, `web/` et `vendor/`, les commandes suivantes lancent le paquet sans installation préalable :

```bash
export PYTHONPATH=src
python3 -m fullegenbrain --data-dir ./data doctor
python3 -m fullegenbrain --data-dir ./data test
```

L'option globale `--data-dir` doit précéder la sous-commande. `FGB_DATA_DIR` peut fournir le dossier de données par défaut. Le répertoire contient la base SQLite, le journal d'audit et les données locales; ne l'effacez pas pour « réparer » une erreur avant d'en faire une copie.

## 2. Diagnostic, composants et sources

```bash
python3 -m fullegenbrain --data-dir ./data doctor
python3 -m fullegenbrain --data-dir ./data components
python3 -m fullegenbrain --data-dir ./data adapters
python3 -m fullegenbrain --data-dir ./data inspect-sources
```

`doctor` contrôle runtime, mémoire SQLite, journal et adaptateurs. `components` décrit les contrats intégrés; `adapters` et `inspect-sources` recensent les adaptateurs historiques sans les exécuter. Un statut `PARTIAL`, `AUDIT_ONLY`, `COMPARISON_ONLY`, `BLOCKED` ou `MISSING_SOURCE` n'est pas un succès d'exécution.

## 3. Valider et exécuter un programme JSON

Le programme doit être une enveloppe JSON validée par le schéma de l'AST. Il ne s'agit pas de code Python, et `eval`/`exec` ne sont pas utilisés.

```bash
python3 -m fullegenbrain --data-dir ./data validate examples/addition_program.json --input-file examples/addition_input.json
python3 -m fullegenbrain --data-dir ./data run examples/addition_program.json --input-file examples/addition_input.json --max-steps 1000 --timeout 10
```

Une entrée inline est également possible :

```bash
python3 -m fullegenbrain --data-dir ./data run examples/addition_program.json --input-json '{"left":2,"right":3}'
```

`validate` ne doit pas exécuter les effets du programme. `run` retourne le statut runtime, la trace, les diagnostics et le coût mesuré. Les budgets `--max-steps`, `--max-depth`, `--max-iterations`, `--max-items`, `--max-candidates` et `--timeout` sont des plafonds, pas des garanties de réussite.

## 4. Synthèse et reprise CEGIS

```bash
python3 -m fullegenbrain --data-dir ./data synthesize \
  --grammar examples/identity_grammar.json \
  --examples examples/identity_examples.json \
  --search-id identity-demo-001 --max-candidates 20
python3 -m fullegenbrain --data-dir ./data resume identity-demo-001 --max-candidates 20
```

Un `search-id` doit être stable et unique pour une recherche. La reprise vérifie l'état enregistré et les empreintes du programme/de la grammaire; un checkpoint incompatible est refusé plutôt que réinterprété silencieusement. Les splits de recherche (`train`, `cegis`/`counterexample`, `holdout`, `test`) gardent leurs rôles séparés. Une sélection de candidat n'est pas automatiquement une preuve de correction. Les oracles externes ne sont disponibles que si l'hôte en a explicitement enregistré un; aucun oracle réseau n'est configuré par défaut.

## 5. Mémoire et vagues d'événements

```bash
python3 -m fullegenbrain --data-dir ./data memory check
python3 -m fullegenbrain --data-dir ./data memory objects
python3 -m fullegenbrain --data-dir ./data memory put \
  --object-id note-demo --payload-json '{"kind":"note","text":"exemple"}' \
  --metadata-json '{"epistemic_status":"UNKNOWN"}'
python3 -m fullegenbrain --data-dir ./data memory get note-demo
python3 -m fullegenbrain --data-dir ./data memory checkpoint --name before-change --payload-json '{"reason":"manual checkpoint"}'
```

Les actions `hibernate`, `wake` et `revoke` sont explicites. Les statuts opérationnels et épistémiques restent distincts. Les commandes `subscribe`, `emit-wave`, `receive-waves` et `replay-waves` gèrent la diffusion persistante et idempotente; `replay-waves` exige une raison d'audit.

## 6. ASCRC, audit, spécialistes et interface

```bash
python3 -m fullegenbrain --data-dir ./data ascrc-plan examples/ascrc_plan.json
python3 -m fullegenbrain --data-dir ./data audit --limit 200 --output ./data/audit-export.json
python3 -m fullegenbrain --data-dir ./data observe --input-json '{"sensor":"demo","value":3}' --label sample
python3 -m fullegenbrain --data-dir ./data serve --host 127.0.0.1 --port 8765
```

`ascrc-plan` est une prévisualisation sauf présence explicite de `--apply`; un passage n'est pas appliqué implicitement au runtime. L'adaptateur spécialiste doit être demandé par ID et opération, avec réseau désactivé par défaut. `serve` n'accepte que les adresses loopback.

## 7. Codes de sortie CLI

| Code | Signification |
|---:|---|
| `0` | Succès déclaré par la commande (`PASS`, `SUCCESS`, `COMPLETED`) |
| `1` | Échec ou erreur d'exécution |
| `2` | Entrée invalide / validation impossible |
| `3` | Résultat partiel, non résolu, non exécuté ou délai budgétaire |
| `4` | Opération bloquée, révoquée, périmée ou source réservée à l'audit/comparaison |

Le statut JSON est l'information principale; le code de sortie facilite l'automatisation. Conservez les fichiers JSON de sortie pour l'audit.
