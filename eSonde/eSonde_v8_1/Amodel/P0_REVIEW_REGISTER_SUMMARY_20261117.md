# P0 — état de couverture de la revue source (mise à jour 17 novembre 2026)

## Périmètre vérifié
- Archive source principale : 2 273 entrées dans l'inventaire initial.
- `theorie_emp/` : 2 018 chemins inventoriés avec taille et SHA-256.
- `theorie_emp/formalismes/` : 1 925 chemins.
- `theorie_emp/PCH/` : 85 chemins, dont 34 sources TeX; versions successives et doublons exacts cartographiés.
- `formalismes/sondes_experiences/` : 12 familles de campagnes identifiées; les READMEs et rapports de référence sont recensés.

## Contrôles d'intégrité et de structure
- Réconciliation SHA-256 des 2 018 fichiers de `theorie_emp/` : 2 018/2 018 PASS.
- Savepoint pré-runtime vérifié : 352/352 fichiers (manifeste historique du snapshot).
- Delta de reprise P0 : 17/17 fichiers vérifiés par SHA-256.
- JSON : 470 fichiers parseables; un fichier à extension `.json` contient en réalité un README Markdown (extension erronée, pas une corruption).
- JSONL : 14/14 fichiers parseables.
- CSV : 114/114 fichiers parseables avec lecteur UTF-8 et largeur cohérente.
- Shell : 9/9 scripts passent `bash -n`.
- Sources Python : compilation syntaxique globale réussie, bytecode redirigé hors de l'arbre source.

## Couverture sémantique au dernier relevé
Le registre `P0_FILE_REVIEW_REGISTER_20261117.jsonl` classe les 2 018 chemins :
- 160 `DEEP_READ` : fichiers ayant été lus au niveau contenu et synthétisés;
- 1 699 `STRUCTURAL_INVENTORY_ONLY` : hash, taille, sections/entêtes/schéma et inventaire vérifiés, mais lecture sémantique complète encore à faire;
- 159 `METADATA_ONLY` : PDF/images, conformément à la consigne de ne pas prioriser la lecture des PDF LaTeX.

Au niveau des contenus uniques (1 575 SHA-256 uniques parmi les 2 018 chemins) :
- 152 `DEEP_READ`;
- 1 299 `STRUCTURAL_INVENTORY_ONLY`;
- 124 `METADATA_ONLY`.

Les 288 groupes de doublons exacts correspondent à 443 chemins supplémentaires. La lecture profonde d'un contenu peut couvrir ses copies byte-identiques, mais les chemins individuels restent tous inscrits. Ces nombres ne signifient pas que les 1 925 fichiers `formalismes/` ont tous été lus en détail.

## Sources théoriques et expérimentales synthétisées
- Théorie des empreintes / observation : empreintes, fibres, quotients, factorisation conditionnelle, limites de l'observation; défauts LaTeX diagnostiqués dans `th_emp_observation_formalisme_0.tex` sans modification de l'original.
- PCH : familles historiques, pré-routage variationnel v11, noyau proximal, cas dégénérés, gain normalisé faux et tie-break non défini; détails dans `PCH_ROUTE_VARIATIONAL_DEEP_REVIEW_20261117.md` et `P0_FORMALISMES_NONNEURAL_REVIEW_20261117.md`.
- eGenBrain v4/v1 : maillage typé, provenance, certificats, distinction observé/dérivé/supposé; lecteur Parquet eGenBrain réutilisé avec adaptation OASST1 BOOLEAN.
- NGeGenBrain v2 : laboratoire mécaniste; voies PyTorch, hooks, MLP, Transformers et Hugging Face exclues de l'architecture v8; sous-outils GF(2)/arithmétiques non appris uniquement comme expériences bornées potentielles.
- eLLM v1 : Transformer pré-entraîné, états cachés et sondes apprises explicitement incompatibles, non repris.
- FulleGenBrain 4 : contrats, composition, provenance et contrôle de ressources; ASCRC complet/mémoire vivante/29 opérateurs non intégrés; le registre source déclare l'intégration E2E non évaluée.
- AAM O94.6 : enveloppes de tâche, statuts, sous-questions et vérification séparée; deux mentions rédactionnelles 448 contredites par les reçus finaux 449, désormais résolues au niveau de la preuve primaire; replay de holdout 2/2 UNRESOLVED.
- ORDER80.2.2 : distinction `DOCUMENTED_INSIGHT` / `SOLVED`; seule une vérification de domaine promeut une résolution; moteur extractif et mémoire RAG non repris comme générateur.
- EX4–EX12 et NG-ADAPT : campagnes de sondes RBF/MLP/HC-RBF conservées en audit historique; aucune architecture neuronale de ces campagnes n'est appelée par le runtime v8.

## État opérationnel v8 au point courant
- OASST1 : 84 437 train + 4 401 validation, 88 838 messages source; splits dérivés sans chevauchement d'arbres.
- Profil agrégé TRAIN : 48 557 lignes consommées, 48 549 exemples non vides; `dialogue_profiles.json` SHA-256 `24780eea05de8cb8c77a772f8d03776adc33dc497fcb7d6e896690f8e99ce0e6`.
- Poids originaux : SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`, inchangés.
- Suite ciblée de composants/runtime : 51 tests PASS; il ne s'agit pas d'une validation CLI+GUI E2E.
- Aucune génération libre eSonde v8 achevée/évaluée n'est attestée. Le baseline v7 OASST1 a timeout après 300 s avant sa première génération enregistrée.
- Défauts d'intégration P2 : GUI ne charge pas le profil v8 et ne fournit pas encore le toggle de non-réponse; CLI/GUI n'appliquent pas encore le preflight v8 canonique; branches v7 secondaires encore présentes.
- Défauts scientifiques ouverts : bases CountSketch/observation distinctes sans mappage prouvé; fonctions de fusion sans preuve neutre pour données absentes; spécification MASK à compléter; redondance/marginalité des canaux et budget Obsiss à mesurer; PCH non intégré; généralisation du profil inconnue.

## Décision de phase
P0 reste `IN_PROGRESS`. L'inventaire et la synthèse des familles centrales progressent, mais 1 699 chemins sont encore `STRUCTURAL_INVENTORY_ONLY` et 159 `METADATA_ONLY`. Les READMEs/rapports d'expérience doivent être reliés un par un à leurs scripts, données, reçus et sorties avant clôture. Aucun passage à P1/P2 n'est autorisé sur la seule base des hashes, tests logiciels ou rapports de synthèse. Aucune prédiction de réussite ou d'échec d'eSonde v8 n'est formulée.
