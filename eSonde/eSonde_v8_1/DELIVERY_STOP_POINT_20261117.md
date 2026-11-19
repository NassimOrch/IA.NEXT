# Point d'arrêt vérifiable — eSonde v8 (17 novembre 2026)

## Description
Snapshot expérimental eSonde v8, fonction chat uniquement. Le checkpoint original est eSonde v6 ; la génération candidate et Obsiss/P-R reste héritée de v7. La couche v8 ajoute le profil statistique OASST1 `everyday_dialogue`, les associations contexte-réponse, les transitions de réponse, le routeur linguistique basé sur le dernier tour USER et le préflight de phase.

## Architecture et pipeline présent
Le prompt et l'historique forment le contexte ; les ancres sont extraites une fois par tour avec pondération de récence. Le profil propose des candidats à partir des associations contextuelles et des transitions du plus long préfixe disponible (trigramme, bigramme, unigramme). Les priors OASST1 TRAIN routent la langue du dernier tour USER ; la langue ciblée limite les propositions selon le vocabulaire V6 TRAIN. Le moteur Obsiss/P-R hérité évalue les candidats. `EsondeV8ChatRuntime` délègue encore la génération complète à `esonde_v7.generation.generate_chat`.

## Commandes et contrôles vérifiés
- `PYTHONPATH=src pytest -q tests` : 81 tests passés, 0 échec, 24,36 s.
- CLI `status` : PASS.
- CLI `verify` : PASS.
- Dans le paquet portable, `status` et `verify` passent sans savepoint embarqué.
- Le CLI/GUI `chat` n'a pas été exécuté ; le préflight de phase et l'exigence d'un savepoint externe le bloquent.

## Données OASST1
Source : 84 437 lignes TRAIN, 4 401 VALIDATION, 88 838 messages et 10 364 arbres. Splits dérivés sans arbre partagé : 48 557 TRAIN, 2 495 VALIDATION, 2 653 TEST. Le profil consomme 48 557 lignes, 48 549 exemples non vides, 57 884 ancres, 252 793 tokens de vocabulaire, 6 950 298 tokens de réponse et 1 762 580 préfixes trigrammes. Profil : 178 135 159 octets, SHA-256 `c517a0a5023add538d7588853652cc01cc7e5f3b305e404d34df6d35cc881544`. Priors de langue chargés par le runtime : SHA-256 `8b769436d13b31ce9b8639720bf97a902b35bed82a17c7b4f713ad0739d15e91`.

## Résultats d'expériences réels
1. **Ablation teacher-forced des transitions** : 2 000 exemples TRAIN et 500 validation internes ; couverture 46,2 % → 86,3 %, précision top-5 tous tokens 20,67 %. Ceci ne mesure pas la génération libre.
2. **Routage linguistique latest-user** : seuils et fenêtre sélectionnés sur VALIDATION puis gelés. TEST dédupliqué : 1 080 contextes uniques, 1 068 routés, couverture 98,89 %, exactitude sélective 99,25 %, fraction correctement routée sur tous les contextes 98,15 %. Il s'agit d'une tâche de classification de route, pas d'une mesure de cohérence dialogique.
3. **Diagnostic Obsiss held-out premier token** : 12 contextes TEST, 256 Obsiss, 5 variantes. Rappel du pool de candidats 1/12 (8,33 %) ; MRR 0,020833 dans chaque variante. Onze tokens cibles étaient absents du pool avant classement ; l'unique cible présente était rang 4. Résultat primaire SHA-256 `4d97e25e03ddffdf99936f21e12d0d165d1d470888a61f33dcf58fba0fd1fd9f`. Échantillon exploratoire restreint, pas de génération libre.
4. **Vues linguistiques séparées en SQLite** : interruption à 10 750/48 557 lignes TRAIN ; aucune table finale publiée ni substitution du profil actif.
5. **Baseline V7** : timeout à 300 s sur 3 prompts, 0 génération complète.
6. **Génération libre V8** : aucune génération complète évaluée.

## Interprétation et conséquences
Le diagnostic held-out révèle un goulot immédiat de rappel des candidats sur son petit échantillon : le classeur Obsiss ne peut pas classer les tokens non proposés. Les métriques de routage indiquent une attribution linguistique utile mais ne prouvent pas la compréhension. La stabilité interne de classement, les tests logiciels et les mesures teacher-forced ne sont pas des substituts à la cohérence de séquence ou à la généralisation.

## Statut exact des phases
- P0_SOURCE_RECONCILIATION : `IN_PROGRESS`.
- P1_FORMALISM_AND_LAB : `NOT_STARTED`.
- P2_IMPLEMENTATION : `NOT_STARTED` dans le verrou de phase.
- P3_EVALUATION : `NOT_STARTED`.
- P4_DOCUMENTATION_AND_DELIVERY : `NOT_STARTED` dans la checklist de phase.

Le registre de source compte 2 018 chemins : 160 DEEP_READ, 1 699 STRUCTURAL_INVENTORY_ONLY et 159 METADATA_ONLY. Après déduplication : 152 contenus uniques DEEP_READ, 1 299 STRUCTURAL_INVENTORY_ONLY et 124 METADATA_ONLY. Le deep-read exhaustif de la source n'est donc pas achevé. Les trois LaTeX compilent deux passes, mais les cinq passes de revue formelle ne sont pas clôturées.

## Prochaine étape exacte
Analyser la cause du rappel candidat de 1/12 et préenregistrer un diagnostic plus large sur le split TEST, en rapportant le rappel séparément par source de proposition, sans exposer la cible au générateur. Continuer le deep-read fichier par fichier de `theorie_emp`, corriger les fondations Obsiss et les espaces CountSketch/observations, achever les passes formelles ; ensuite seulement réévaluer le verrou de génération. Ne pas confondre les résultats du routeur avec une amélioration du dialogue.

## Intégrité et exclusions
Le checkpoint original (64 000 000 octets) conserve SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`. Le profil et les priors sont vérifiés par le runtime. Les sources attachées, les Parquet bruts, le workspace SQLite de construction et les snapshots de sauvegarde ne sont pas inclus dans les trois livrables. Le modèle est `8.0.0-dev / EXPERIMENTAL / FREE_GENERATION_QUALITY=NON_EVALUE`; aucun verdict anticipé de réussite ou d'échec n'est porté.
