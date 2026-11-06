# AAM O93_1 — Livraison française

Cette version corrige le chemin de réponse Chat/RAG/modèle, ajoute un entraînement explicite du petit modèle de langue (distinct de l’acquisition d’une compétence), connecte cette action à Runtime/CLI/interface, et corrige une actualisation de catalogues qui pouvait bloquer Tk pendant un long entraînement.

## Démarrage

Depuis le dossier extrait, avec Python 3.11+ et Tkinter pour l’interface :

```bash
python -m aam_o93 --workspace ./workspace_o93_1 status
python -m aam_o93 --workspace ./workspace_o93_1 ui
```

Pour les commandes de sources et RAG, le guide utilisateur explique le chargement, l’observation, l’ingestion, la reconstruction, la sélection d’un modèle, la lecture des sources/citations et les diagnostics.

## L’entraînement génératif n’est pas l’acquisition d’une compétence

Dans l’onglet **Entraînement**, utiliser le panneau **Modèle de langue génératif pour le chat** puis **Entraîner modèle de langue du chat**. L’action `Lancer acquisition` acquiert une compétence de tâche; elle ne signifie pas automatiquement que le générateur de chat a été entraîné. Une capsule complète doit apparaître dans le sélecteur du chat et son identifiant/hash doit apparaître dans les détails techniques après invocation.

CLI équivalente :

```bash
python -m aam_o93 --workspace ./workspace_o93_1 train-language-model ./corpus.txt --epochs 5 --max-vocab 128 --dim 16 --context-size 5 --seed 92
```

## Statut de validation

P3 est clôturée au statut `COMPLETE_LOCAL_TESTED_BOUNDED` après 15/15 critères de sortie. L’acceptation bornée sur 120 SMS réels montre que l’exemple tenu hors entraînement est récupéré par le RAG, transmis au prompt et que la capsule entraînée correspondante est réellement invoquée. Sur cet essai, la candidate générée a été rejetée comme inutilisable et le chat a affiché un fallback extractif cité ; l’invocation est prouvée, l’utilité de ce texte généré ne l’est pas.

Le test d’acceptation sur les 5 574 SMS n’a pas produit de rapport final dans le budget de test et reste `NOT_VALIDATED`; il n’est interprété ni comme réussite ni comme échec fonctionnel. L’acceptation externe P10 (OS natif, vrais capteurs, réseau/MCP/API et tests crash/ACL/rollback) n’est pas démarrée.

## Intégrité

Les originaux de `sources_AAM_17.zip`, des datasets et des documents de conception O93_0 sont conservés. Les manifestes SHA-256 décrivent les fichiers livrés, hors fichiers manifestes eux-mêmes. Exécuter `python scripts/verify_all_manifests.py .` depuis la racine extraite pour vérifier les hashes et les fichiers non manifestés. Les contrôles finaux et hashes de l’ensemble des trois archives figurent dans `O931_delivery_manifest.json` livré séparément.

Consulter `GUIDE_UTILISATEUR_O93_1.md`, `formalisme_O93_1.tex`, `laboratoire_O93_1.tex` et `registre_prouves_O93_1.json` pour le fonctionnement détaillé et les limites de preuve.
