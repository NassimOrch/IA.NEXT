# Rapport d'implémentation — profil conversationnel et logique de génération v8

## Description

Cette révision corrige deux défauts du chemin chat v8 et ajoute une factorisation de calcul destinée à diminuer le travail redondant pendant le beam. Elle concerne uniquement le profil de dialogue agrégé OASST1; elle ne remplace pas le moteur candidat/Obsiss/P-R hérité.

## Architecture

`EsondeV8ChatRuntime` injecte désormais le module `esonde_v8.dialogue_learning` dans `esonde_v7.generation.generate_chat`. Le module v8 expose un seul profil `everyday_dialogue`, vérifie son schéma et exige `neural_components: []`. Il fournit le calcul d'associations de contexte, le support d'ancres distinctes, les transitions dépendantes du préfixe, les propositions et la fusion neutre dans les canaux `dialogue_association` et `local_transition`.

## Pipeline complet

1. Charger et valider le profil, puis vérifier le SHA-256 du profil et du checkpoint original.
2. Construire le contexte courant à partir du prompt et de l'historique explicite.
3. Extraire les ancres une seule fois par tour; calculer les associations ancre→réponse et le support par ancres distinctes.
4. Pour chaque préfixe de chaque branche du beam, chercher les continuations au plus haut niveau observé : trigramme, puis bigramme, puis unigramme; au premier token, utiliser d'abord les débuts de réponse.
5. Normaliser le compteur retenu par `log1p(c)/log1p(c_max)` et enregistrer le niveau utilisé. Cette transformation n'est pas une probabilité calibrée.
6. Fusionner les scores de profil dans les deux canaux existants seulement si le pool possède un score positif pour le canal. Si l'ensemble des scores est nul, conserver les valeurs héritées exactement.
7. Transmettre les candidats au moteur Obsiss/P-R hérité, sans introduire de nouvelle observation ni de poids appris.

## Commandes d'exécution

Tests ciblés :

```bash
cd Dmodel_eSonde_v8
PYTHONPATH=src pytest -q tests/test_esonde_v8_dialogue_learning.py tests/test_esonde_v8_preflight.py
```

Suite active complète :

```bash
PYTHONPATH=src pytest -q tests
```

Contrôle administratif portable :

```bash
python RUN_CLI.py status --workspace .
python RUN_CLI.py verify --workspace .
```

La commande `chat` demeure bloquée au préflight tant que P0/P1/P2 ne sont pas closes; aucun contournement n'est réalisé dans ce rapport.

## Résultats

- Suite active : 66 tests passés, 0 échec.
- Tests spécifiques au profil + préflight : 15 tests passés, 0 échec.
- Préflight portable `status` : PASS; 33 fichiers de savepoint, 242 450 887 octets, tailles et SHA-256 vérifiés.
- Le checkpoint original reste 64 000 000 octets, SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`.
- Le profil OASST1 reste 178 134 753 octets, SHA-256 `24780eea05de8cb8c77a772f8d03776adc33dc497fcb7d6e896690f8e99ce0e6`.
- Les trois sources LaTeX passent chacune deux compilations `pdflatex -halt-on-error`.
- La tentative de génération v8 n'a pas été exécutée : les phases P0/P1/P2 sont toujours incomplètes.

## Interprétation des résultats

Les tests confirment les propriétés programmées : repli des transitions lorsqu'un niveau long est absent, fusion neutre si le profil n'apporte aucun signal et validation stricte du manifeste de sauvegarde. La mesure de calcul statique une seule fois est cohérente avec la dépendance des statistiques associatives au seul contexte de tour; l'expérience d'appariement de performance H1 reste à effectuer.

Aucun des tests ne mesure la cohérence d'une réponse générée, la pertinence multi-tour, la factualité ou la généralisation hors distribution. Ces propriétés sont non évaluées à cette étape.

## Conséquences

### Théoriques

Le choix hiérarchique du niveau de continuation est défini sur les compteurs observés; le statut de repli fait partie de la sortie instrumentée. Le support par ancres distinctes n'est pas interprété comme indépendance statistique.

### Conceptuelles

Le profil OASST1 reste un soutien statistique de proposition, pas un moteur de restitution de réponses ni une mémoire d'exemples. L'absence d'évidence est une opération identité sur les canaux du modèle hérité.

### Opérationnelles

Le calcul d'associations est partagé entre les branches de beam d'un même tour; les transitions restent préfixe-dépendantes. Les points de sauvegarde sont vérifiés fichier par fichier; les contrôles portable sont embarqués avec le Dmodel.

## Conclusion

Deux défauts logiciels identifiés sont corrigés et testés : backoff trigramme→bigramme→unigramme et fusion neutre en cas d'absence de signal. Le chargement CLI/GUI et le préflight v8 sont raccordés. Le runtime reste un moteur Obsiss/P-R V7 hérité avec profil v8; aucune génération libre v8 n'a encore été mesurée.

## Statut du modèle

`8.0.0-dev` — implémentation de profil chat partiellement avancée, tests logiciels passés, qualité dialogique `NON_EVALUE`. P0 reste `IN_PROGRESS`; P1, P2, P3, P4 restent `NOT_STARTED` dans le registre de phases. Aucun verdict de réussite ou d'échec n'est émis.

## Addendum — 17 novembre 2026, 14:58 Africa/Algiers

Since the initial 66-test report, the language-aware route was implemented in the runtime and covered by four focused tests. A selected V6 language route filters OASST1 associations to the selected language's TRAIN unigram vocabulary and withholds the multilingual aggregate OASST1 response transitions; the global/ambiguous route retains the aggregate fallback. This is a lightweight runtime filter, not a complete language-separated profile, and its response quality remains unevaluated.

The active suite now passes 81 tests (0 failures, 24.36 s). This count includes two new portable-preflight tests. The status and verify CLI commands pass. No free-running v8 generation was executed; P0 remains IN_PROGRESS and P1/P2/P3 remain NOT_STARTED. The older counts above are retained as historical run records, not substituted for this latest result.

## Addendum — résultats de diagnostic supplémentaires (17 novembre 2026, 2026-11-17T15:08:02+01:00)

- Le routeur de dernier tour USER basé sur les priors OASST1 TRAIN a été évalué sur des contextes dédupliqués. Politique retenue sur VALIDATION : fenêtre 24 tokens, indice de script direct activé, seuils (1 token, couverture 0,05, marge 0,03). TEST gelé : 1 080 contextes uniques, couverture 98,89 %, exactitude sélective 99,25 %, part correcte sur tous les contextes 98,15 %. Ce résultat mesure la classification de la langue de route uniquement, pas la qualité de réponse.
- Le diagnostic Obsiss held-out a été **exécuté** (et non simplement préflighté) sur 12 exemples, 256 Obsiss et cinq variantes. Le rappel du pool de candidats est 1/12 (8,33 %) et le MRR 0,020833 pour toutes les variantes. Onze tokens cibles n'étaient pas présents dans le pool avant le classement ; un seul y figurait au rang 4. Ce résultat signale un problème de rappel des propositions sur cet échantillon, non une conclusion générale sur le modèle.
- Les fichiers JSON et leurs hashes sont répertoriés dans les rapports  et .

## Addendum — résultats de diagnostic supplémentaires (17 novembre 2026)

- Le routeur de dernier tour USER basé sur les priors OASST1 TRAIN a été évalué sur des contextes dédupliqués. Politique retenue sur VALIDATION : fenêtre 24 tokens, indice de script direct activé, seuils (1 token, couverture 0,05, marge 0,03). TEST gelé : 1 080 contextes uniques, couverture 98,89 %, exactitude sélective 99,25 %, part correcte sur tous les contextes 98,15 %. Ce résultat mesure la classification de la langue de route uniquement, pas la qualité de réponse.
- Le diagnostic Obsiss held-out a été exécuté sur 12 exemples, 256 Obsiss et cinq variantes. Le rappel du pool de candidats est 1/12 (8,33 %) et le MRR 0,020833 pour toutes les variantes. Onze tokens cibles n'étaient pas présents dans le pool avant le classement ; un seul y figurait au rang 4. Ce résultat signale un problème de rappel des propositions sur cet échantillon, non une conclusion générale sur le modèle.
- Les reçus primaires et leurs SHA-256 sont documentés dans `P0_HELDOUT_NEXT_TOKEN_DIAGNOSTIC_20261117.md` et `P0_LANGUAGE_ROUTE_EVALUATION_20261117.md`.
