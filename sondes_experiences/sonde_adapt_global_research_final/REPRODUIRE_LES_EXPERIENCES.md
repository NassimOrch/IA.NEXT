# Reproduire les expériences

## 0. Pré-requis et répertoire

Système testé : Linux x86_64, Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0, scikit-learn 1.8.0, PyTorch 2.10.0+cpu, Matplotlib 3.10.8. La campagne n'a pas utilisé de GPU. Les scripts utilisent le dossier `results/` relatif à leur répertoire de travail; se placer à la racine de la livraison.

```bash
cd /chemin/vers/sonde_adapt_global_research_v2
python3 -m pip install numpy pandas scipy scikit-learn torch matplotlib jsonschema
```

Les versions ci-dessus sont celles observées dans cet environnement; ne pas remplacer les versions dans une reproduction sans le noter. Les commandes ci-dessous peuvent produire des sorties différentes avec d'autres versions BLAS/PyTorch, bien que le replay historique réalisé dans l'environnement fourni ait donné des fichiers identiques.

## 1. Tests rapides (faisabilité uniquement)

```bash
python3 code/run_architecture_benchmark.py --quick --out-dir /tmp/ngadapt_smoke
```

Le mode rapide utilise une seule graine et 8 epochs. **Ses métriques ne doivent pas être citées comme résultats de l'étude.** Le script écrit dans un répertoire de sortie dédié.

## 2. Benchmark principal complet (165 runs)

Le mode complet prend environ plusieurs minutes et doit être séparé par tâche pour reprendre plus facilement une interruption. Le benchmark utilise 90 epochs et trois seeds dans `configs/experiment_main.json`.

```bash
for task in two_moons circles xor_product wine_binary digits_3_vs_8; do
  python3 code/run_architecture_benchmark.py --epochs 90 --tasks "$task" \
    --out-dir "results/replay_${task}" \
    >"logs/replay_${task}.stdout.log" 2>"logs/replay_${task}.stderr.log"
  printf '%s\n' "$?" >"logs/replay_${task}.exitcode"
done
```

Pour conserver intacts les résultats déjà livrés, choisir un nouveau suffixe dans `--out-dir`, comme dans l'exemple. Les fichiers d'origine de la campagne ont été sauvegardés dans `results/architecture_benchmark/<task>/`.

## 3. Reproduction historique stricte

Le script source de référence est copié sans modification sous `reproduction/base_toy/experience_sondes_adaptatives.py`. Il dépend de son arborescence source et de ses données associées; la commande de référence utilisée est enregistrée dans `logs/base_reproduction.stdout.log`. Pour vérifier le résultat qui est livré sans le modifier :

```bash
sha256sum reproduction/base_toy/*
```

Les hashes attendus des CSV et JSON sont consignés dans `RESULTATS_COMPLETS.md` et dans le manifeste des sources. Le replay original a été effectué dans un dossier de travail propre et ses résultats étaient identiques octet par octet aux résultats de référence.

## 4. Ablation de coordination globale

```bash
python3 code/run_global_coordination_ablation.py \
  >logs/replay_global_ablation.stdout.log 2>logs/replay_global_ablation.stderr.log
printf '%s\n' "$?" >logs/replay_global_ablation.exitcode
```

Comparer les conditions sonde locale, coordinateur gelé, coordinateur entraîné et coordinateur dont les cibles de mise à jour sont permutées. Le contrôle « gelé » doit reproduire exactement les sorties locales dans ce protocole.

## 5. Boucle de rétroaction et robustesse

```bash
python3 code/run_loop_robustness.py \
  >logs/replay_loop_robustness.stdout.log 2>logs/replay_loop_robustness.stderr.log
printf '%s\n' "$?" >logs/replay_loop_robustness.exitcode
```

Le flux est predict-then-reveal : prédire, révéler l'étiquette d'adaptation (ou son absence), consigner le résidu/empreinte, puis effectuer la mise à jour autorisée. Les labels d'évaluation ne sont pas fournis à l'API d'update. Le flux artificiel reste un test contrôlé, pas une preuve sur un environnement réel.

## 6. Reconstruction `x → f(x) → g(f(x)) ≈ x`

```bash
python3 code/run_reconstruction_experiment.py \
  >logs/replay_reconstruction.stdout.log 2>logs/replay_reconstruction.stderr.log
printf '%s\n' "$?" >logs/replay_reconstruction.exitcode
```

L'identité directe est un contrôle trivial; elle ne doit pas être décrite comme un réseau appris. La deuxième fonction n'a pas accès à `x` directement et aucune connexion résiduelle de `x` à la sortie n'est autorisée. Le code démarre explicitement un état Adam frais au début de la boucle online; il ne réutilise pas implicitement l'état de pré-entraînement.



## 7. Boucle causale par empreinte (FBR-1)

Le run livré a été exécuté sur 3 graines et architectures A–E. Il utilise un seuil q90 calculé sur validation propre avant la phase d'adaptation. Pour le rejouer, choisir une copie propre de la livraison, car le script consolide les checkpoints dans `results/fingerprint_feedback_loop/`.

```bash
python3 code/run_fingerprint_feedback_loop.py --seeds 1501 1607 1717 --architectures A B C D E \
  > logs/replay_fbr1.stdout.log 2> logs/replay_fbr1.stderr.log
printf '%s\n' "$?" > logs/replay_fbr1.exitcode
```

## 8. Boucle causale pour la reconstruction (RBF-R1)

Le run enregistré est déjà complet (6 paires, 162 lignes métriques, 23 040 événements). Le programme saute toute paire ayant ses trois checkpoints présents. La commande ci-dessous ne réentraîne donc pas les six paires complètes si elle est exécutée depuis la livraison intacte, mais réagrège le résultat; faire une copie pour modifier les artefacts.

```bash
python3 code/run_reconstruction_feedback_gate.py --seeds 101 202 303 \
  --models RBF2_free_global RBF2_free_tanh_global \
  > logs/replay_rbf_r1.stdout.log 2> logs/replay_rbf_r1.stderr.log
printf '%s\n' "$?" > logs/replay_rbf_r1.exitcode
```

## 9. Audit indépendant complet

```bash
python3 -m compileall -q code
python3 code/audit_independent.py
```

L’audit v6 doit produire 49 contrôles PASS sur 49. Un PASS signifie que les invariants instrumentés sont respectés sur les artefacts audités; ce n'est ni un test statistique confirmatoire ni une preuve universelle.

## 10. Audit indépendant et tests sources

```bash
python3 code/audit_independent.py
cat results/independent_audit.json
```

Les contrôles sur les paquets sources peuvent être reproduits dans les répertoires d'extraction listés dans `docs/INVENTAIRE_SOURCES.md`. En particulier, pour les tests du v2 :

```bash
PYTHONPATH="$V2/src:$V2/legacy_NGeGenBrain_v1/src" pytest -q "$V2"
```

Pour la suite v3.1 :

```bash
PYTHONPATH="$V3/src" pytest -q "$V3"
python3 "$V3/ngbrain.py" legacy-test
```

`V2` et `V3` doivent désigner des extractions propres des ZIP internes indiqués dans le manifeste. L'archive livrée contient les logs des appels effectués, pas toutes les archives binaires de modèle originales. Le contenu original est gardé en dehors de la livraison et contrôlé par ses SHA-256.

## 11. Recalcul des métriques existantes

Les prédictions de test par graine sont dans `results/architecture_benchmark/<task>/predictions_test_evaluation_only.csv`; les agrégats se trouvent dans `summary_by_architecture.csv/json` et `paired_contrasts.csv/json`. Les métriques d'ablation, boucle et reconstruction sont dans leurs sous-dossiers homonymes. Pour reproduire les chiffres sans relancer les modèles, recalculer accuracy/log-loss à partir de la colonne `y_true` et des colonnes de probabilité sauvegardées; ce recalcul n'est pas un nouvel entraînement.

## 12. Statut à respecter

- « Smoke test » = exécutable, pas résultat scientifique.
- « Reproduction » = script original relancé et artefacts comparés.
- « Audit PASS » = contrôles instrumentés réussis, pas absence de tout biais possible.
- « Soutenu dans le domaine testé » ne signifie pas preuve universelle.

### Validation finale des fichiers livrés

Après décompression de la livraison, depuis son répertoire racine :

```bash
python3 code/validate_delivery.py
```

Ce script vérifie le hash du `prompt.txt` copié, la référence de l'archive source inscrite dans l'audit, les 49 contrôles instrumentés, la syntaxe de tous les fichiers JSON/JSONL/CSV livrés, la cohérence du manifeste SHA-256 et les métadonnées du PDF. Il vérifie l'intégrité technique des artefacts, pas la validité scientifique universelle des hypothèses.
