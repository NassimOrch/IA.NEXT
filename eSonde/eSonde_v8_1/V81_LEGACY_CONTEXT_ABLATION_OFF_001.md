# RAPPORT_V81_LEGACY_CONTEXT_ABLATION_OFF_001

Date locale : 2026-11-18T16:08:27+01:00

## 1. Description

Expérience contrôlée visant à mesurer la contribution du profil historique v8 `context_response` à la cohérence d'une explication, sans modifier les poids ni les données d'apprentissage actives.

Prompt : `Explain photosynthesis simply.`

Option testée : `--disable-legacy-context-association`. Toutes les autres sources linguistiques et sémantiques restent actives : priors de langue, débuts de réponse OASST1, transitions de langue, index sémantique prompt→réponse et transitions conditionnées par ancre du prompt + préfixe généré.

## 2. Architecture

Runtime `EsondeV81ChatRuntime` indépendant du verrou de phase → propositions locales/OASST1 → Obsiss nommées E_O (16 canaux) → calcul P/R E_C sur les mêmes lignes Obsiss → fusion scalaire des rangs → sélection token. Aucun neurone/MLP/Transformer n'est utilisé ; `neural_components=[]` dans le reçu. `allow_non_response=false`.

## 3. Pipeline complet

1. Lecture des contrôles/checklists et validation du snapshot complet pré-exécution.
2. Vérification SHA-256 des poids actifs et de leur copie de sauvegarde.
3. Chargement de la population originale complète (1 000 000 Obsiss).
4. Sélection de langue basée sur le prompt courant : anglais (`TRAIN_DISTRIBUTION_ROUTE`).
5. Désactivation de `context_response` historique pour cette exécution seulement.
6. Maintien des propositions du LM OASST1 et de l'index sémantique contextualisé ; vote E_O et score P/R E_C pour chaque token.
7. Écriture JSON et journaux token-par-token.

## 4. Commande d'exécution

```bash
PYTHONPATH=src python -m esonde_v8.cli_v81 chat \
  --prompt "Explain photosynthesis simply." \
  --max-tokens 8 --beam-width 1 --candidate-limit 48 \
  --p-activation-mode first_state \
  --disable-legacy-context-association \
  --workspace /mnt/data/esonde_audit/v8_1_work \
  --output-dir suivi_model_eSonde_v8_1/experiments/v81_photo_legacy_context_ablation_off_fullpop_20261118/runtime \
  --json-out suivi_model_eSonde_v8_1/experiments/v81_photo_legacy_context_ablation_off_fullpop_20261118/result.json
```

## 5. Résultats

- Statut d'exécution : `GENERATED`.
- Réponse : **`The. algae h2o, que es el`**.
- Tokens produits : 8.
- Population : 1000000 Obsiss actifs et disponibles.
- Taille du faisceau : 1 ; limite de candidats : 48.
- Non-réponse : désactivée (`allowed=false`, `triggered=false`).
- Langue sélectionnée : `en`.
- Checkpoint : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4` ; `checkpoint_unchanged=true`.
- SHA-256 réponse : `c2a5ff530816d740a9d2e2d3476dc606440c65d55b9243d31e4e31b64b82410f`.
- JSON SHA-256 : `3b65c72600b72af6eb0b6203d99ec83dbc555c392067f58ee646b69ab34a47f9`.

## 6. Interprétation

L'ablation totale supprime effectivement les candidats de l'ancien canal de cooccurrence. Le pool initial tombe à 19 candidats, contre 48 dans le réglage complet, et les propositions parasites `chimera`, `planarian` et `kanye` disparaissent. Cependant, le démarrage devient générique (`The.`), puis la continuation dérive (`algae h2o, que es el`). Le modèle a sélectionné la route de langue `en`, mais la séquence contient une continuation espagnole (`que es el`), ce qui indique un problème de bruit linguistique ou de classement à analyser.

L'ancien canal semble utile à l'ouverture thématique, mais nuisible lorsqu'il reste actif à chaque token. L'option `off` ne doit donc pas devenir le défaut. L'hypothèse de travail suivante est `initial_only` : conserver le signal historique à la première décision, puis le retirer dès qu'un préfixe assistant existe. Ce choix sera évalué, pas présumé.

## 7. Conséquences

- Théorique : pas de changement aux opérateurs P/R ni aux 16 observations.
- Conceptuelle : distinguer un signal de sélection d'ouverture d'une association réutilisée comme signal de continuation.
- Opérationnelle : conserver `full`, `initial_only` et `off` comme trois conditions expérimentales comparables ; analyser également l'adéquation de la langue au cours du préfixe.

## 8. Conclusion

L'ablation `off` est fonctionnellement exécutable en population complète, mais ne fournit pas de réponse cohérente. Elle démontre seulement que supprimer le profil historique entier dégrade l'ouverture et ne suffit pas à corriger les continuations.

## 9. Statut du modèle

Prototype conversationnel v8.1 en développement. Cohérence et généralisation non démontrées. L'incident/constat reste ouvert pour comparaison avec `initial_only`.
