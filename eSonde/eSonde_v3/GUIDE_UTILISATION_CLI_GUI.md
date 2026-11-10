# Guide d'utilisation de bout en bout — CLI et interface graphique

Ce document réunit les parcours recommandés pour les deux interfaces d'eSonde v3. Les deux interfaces appellent le même runtime `ProbeModel` et partagent les mêmes fichiers JSON de modèle et sidecars SHA-256.

## A. Première utilisation depuis un dossier extrait

1. Décompresser le dossier de livraison.
2. Vérifier Python : `python --version` (Python 3.10+).
3. Vérifier le CLI : `python run_esonde.py --version` puis `python run_esonde.py --help`.
4. Vérifier la GUI si une session graphique est disponible : `python run_esonde_gui.py`.
5. Lire `README.md`, `docs/CLI_GUIDE.md`, `docs/GUI_GUIDE.md` et `docs/PROTOCOL_EXPERIMENTAL_VALIDATION.md`.
6. Conserver une copie séparée des données d'entrée et des checkpoints avant toute mise à jour.

Le moteur runtime n'utilise que la bibliothèque standard Python. La GUI nécessite en plus le module Tkinter/Tcl-Tk fourni par certaines distributions Python comme composant optionnel. Aucun accès réseau n'est utilisé.

## B. Entraînement initial via CLI

Préparer trois dossiers au niveau document : `corpus/train`, `corpus/validation`, `corpus/test`. Leur contenu doit être disjoint, y compris en empreinte SHA-256.

```bash
python run_esonde.py train \
  --corpus ./corpus/train \
  --validation ./corpus/validation \
  --config ./examples/training_config.json \
  --output ./models/my_model.json
```

Le résultat `TRAINED` indique que l'opération de construction et de sauvegarde est terminée ; il ne représente pas une évaluation de la qualité. Le checkpoint est accompagné de `my_model.json.sha256`.

## C. Entraînement initial via GUI

1. Lancer `python run_esonde_gui.py`.
2. Dans **Entraînement / mise à jour**, choisir le dossier de train.
3. Choisir le dossier validation (facultatif mais recommandé pour calibrer COORD).
4. Choisir le chemin de sortie du modèle.
5. Cliquer **Entraîner** et attendre le message « Terminé : Entraînement ».
6. Vérifier dans le journal les documents, supports de sondes et le chemin de sauvegarde.
7. Le chemin du modèle courant est mis à jour après réussite.

Le GUI n'expose pas toutes les clés de configuration avancée ; utiliser la CLI et le JSON de configuration pour un contrôle complet des paramètres.

## D. Génération

CLI :

```bash
python run_esonde.py generate --model ./models/my_model.json \
  --prompt "Le système" --max-tokens 32 --strategy greedy
```

GUI : dans **Génération**, saisir le prompt, régler le nombre maximal de tokens et choisir `greedy` ou `sample`, puis cliquer **Générer**. La GUI utilise une graine fixe 0.

## E. Évaluation indépendante

CLI :

```bash
python run_esonde.py score --model ./models/my_model.json \
  --corpus ./corpus/test --top-k 5 --output ./reports/test_score.json
```

GUI : dans **Évaluation / récupération**, choisir `corpus/test`, puis cliquer **Évaluer (score)**.

La métrique n'a de sens qu'avec un jeu test indépendant et suffisamment représentatif. Une évaluation sur quelques dizaines de tokens est une observation exploratoire, non une preuve de généralisation.

## F. Récupération / inspection / audit

CLI :

```bash
python run_esonde.py retrieve --model ./models/my_model.json --query "énergie et mémoire" --top-k 5
python run_esonde.py inspect --model ./models/my_model.json --family SEM --output ./reports/sem.json
python run_esonde.py audit --model ./models/my_model.json --output ./reports/audit.json
python run_esonde.py info --model ./models/my_model.json
```

GUI : utiliser **Évaluation / récupération** pour RETR et **Inspection / audit** pour examiner une famille, le coordonnateur ou lancer l'audit.

## G. Mise à jour et recalibration

CLI :

```bash
python run_esonde.py update --model ./models/my_model.json \
  --corpus ./corpus/new_batch --batch-id batch-2026-11-09 \
  --output ./models/my_model_v2.json
python run_esonde.py calibrate --model ./models/my_model_v2.json \
  --validation ./corpus/validation_v2
```

GUI : renseigner le dossier **Corpus à ajouter** et **Identifiant de lot**, puis **Mettre à jour le modèle courant**. Ensuite choisir le corpus validation dans l'onglet entraînement/mise à jour et cliquer **Recalibrer COORD**.

Pour une mise à jour sûre, conserver le checkpoint précédent et le nouveau checkpoint ; vérifier les sidecars et enregistrer la provenance du lot. Ne pas écraser l'unique copie valide.

## H. Rapport et reproductibilité

Pour chaque expérience, consigner la description, architecture, pipeline, commandes exactes, résultats bruts, interprétation, conséquences théoriques/conceptuelles/opérationnelles, conclusions et statut du modèle. Inclure les empreintes SHA-256 des données, paramètres, scripts et checkpoints ; enregistrer seed, split, version Python, système et code de retour.

Les logs d'exécution et modèles d'exemple de cette version sont sous `results/` et `models/`. Les archives sources d'origine ne sont pas intégrées dans la distribution runtime.


## Extensions P6 : relations, coréférence, retrait de lot et contexte

La CLI ajoute `relations`, `coref` et `remove-batch`. L'interface graphique ajoute les zones de recherche relationnelle, de candidats d'alias/coréférence et un bouton de retrait de lot. Ces opérations utilisent exactement le même objet `ProbeModel` que l'entraînement et la génération. Les relations A–relation–B sont induites sans analyseur externe à partir de partitions locales de clauses observées ; les candidats d'alias sont classés avec scores et preuves, sans résolution unique imposée.

Un nouveau checkpoint conserve les textes des lots et de validation afin que `remove-batch` puisse reconstruire toutes les tables et le réservoir RETR par rejeu déterministe. Le fichier JSON contient donc les documents d'entraînement : contrôlez ses permissions et son stockage. Un ancien checkpoint sans ce registre complet rejette le retrait exact plutôt que de simuler une suppression.

Dans une configuration d'entraînement, `max_context: 0` désactive le plafond global de contexte additionnel. Les fenêtres locales des sondes restent configurables (`seq_max_order`, `sem_window`, `disc_window`, `retrieval_context_window`, motifs SKIP_REL, etc.) ; les coûts augmentent avec ces portées et sont à mesurer sur le corpus cible.

### Diagnostics de portée du contexte

Avec `max_context` positif, `predict_next` retourne `TRUNCATED_CONTEXT` et le bloc `context_scope` qui donne les éléments fournis, retenus et écartés. La commande `score` fournit `context_window.truncated_context_targets` et `discarded_context_items`. Le mode `max_context: 0` désactive seulement le plafond global supplémentaire ; il ne supprime pas les limites locales propres aux sondes.

### Parcours CLI de retrait exact

```bash
python run_esonde.py info --model ./models/my_model.json
python run_esonde.py remove-batch --model ./models/my_model.json --batch-id batch-2026-11-09
python run_esonde.py audit --model ./models/my_model.json
```

Avant le retrait, copiez le JSON et son sidecar SHA-256. La reconstruction exacte est disponible seulement pour les modèles qui conservent le registre complet des textes de lot ; les modèles historiques incomplets la refusent. Après l'opération, vérifiez le nouveau checksum et le résumé des identifiants de lot restants.
