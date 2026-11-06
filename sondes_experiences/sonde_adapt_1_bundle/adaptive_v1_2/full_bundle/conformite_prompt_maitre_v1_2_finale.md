# Conformité finale au prompt maître — campagne NGeGenBrain v1.2

**Verdict global : `PASS_WITH_LIMITATIONS`.** Cette matrice couvre les campagnes historiques conservées et la réplication indépendante strictement isolée v1.2. Les états indiquent des vérifications réellement documentées ; ils ne constituent pas une preuve absolue d'absence de canal auxiliaire ni une preuve mathématique de l'hypothèse générale.

## Matrice de conformité

| Exigence | État | Preuve effectivement disponible | Limites restantes |
|---|---|---|---|
| Lire les deux sources exigées | CONFORME | Copies dans `references/`, SHA-256 vérifiés contre les fichiers source présents | Aucun doute sur l'intégrité des copies ; interprétation toujours limitée au contenu théorique réellement spécifié. |
| Tracer le formalisme source jusqu'à la sonde qui apprend | CONFORME AVEC DISTINCTION EXPLICITE | `formalisme_sonde_adaptative.tex`, `src/strict_models_v1_2.py`, rapport final §14.2 | `full_0` définit une sonde comme opérateur d'observation abstrait ; il n'impose ni RBF ni apprentissage. La RBF avec paramètres ajustables est une instanciation expérimentale documentée, et non une équation prétendument copiée du source. |
| A — sonde adaptative naturelle sur tâches communes | CONFORME DANS LE PÉRIMÈTRE TESTÉ | CSV de classification par graine, comparaisons RBF/MLP, campagne stricte v1.2 | Trois graines par tâche ; le contrôle fixe dispose de moins de paramètres ajustables. |
| B — sonde apprenant son propre mécanisme | PARTIELLEMENT CONFORME, DÉFINITION LIMITÉE | `results/vitesses_adaptation_apprises.csv`, `results/strict_isolation_meta_rates_v1_2.csv`, protocole v1.2 | Quatre taux d'actualisation par groupe sont méta-appris par hypergradient. L'architecture RBF et l'optimisation par gradient sont préspécifiées : aucun optimiseur général n'est découvert à partir de zéro. |
| C — imitation boîte noire de neurones | CONFORME DANS LA FAMILLE TESTÉE | 81 entraînements (9 cibles × 3 budgets × 3 graines), 324 000 sorties d'évaluation, audits d'accès | Les cibles sont neuf neurones artificiels scalaires à deux entrées, avec tanh/ReLU/sigmoïde ; ce n'est pas une preuve sur toutes les classes de neurones. |
| D — référence neuronale | CONFORME COMME BASELINE | MLP de référence dans les tâches de classification et comme réseau source pour les remplacements locaux | Le readout/source est conservé pour les expériences de composition ; ce n'est pas une reconstruction autonome. |
| Contrôle fixe et budget de paramètres | CONFORME AVEC DÉSÉQUILIBRE DOCUMENTÉ | Contrôle RBF fixe dans les CSV et rapports | Le contrôle fixe a une capacité paramétrique inférieure dans certaines tâches ; aucune conclusion causale simple sur le seul effet de l'adaptation. |
| Étape 1 — fonctions contrôlées | CONFORME | tâches synthétiques et imitation de composants | Les résultats ne démontrent pas une capacité universelle. |
| Étape 2 — neurones isolés | CONFORME DANS LE DOMAINE ÉVALUÉ | budgets d'observation 64/256/1024 ; 4 000 points d'évaluation indépendants par cible-budget ; nouvelles cibles v1.2 | Familles d'activation limitées et domaine d'entrée borné. |
| Étape 3 — composition | CONFORME COMME REMPLACEMENT LOCAL | 96 sondes de composant, 6 systèmes source et 18 conditions de remplacement v1.2 ; CSV fidélité et composition | Le readout original reste conservé ; écart de logits croissant avec le nombre d'unités remplacées, même quand l'exactitude reste élevée. |
| Étape 4 — plusieurs tâches | CONFORME | Deux lunes, cercles, XOR produit, Wine binaire ; benchmarks publics antérieurs breast cancer et digits 10 classes | Les campagnes sont séparées par protocole et par graines ; les résultats ne sont pas agrégés comme si les tâches étaient identiques. |
| Étape 5 — usage réel | PARTIELLEMENT CONFORME | Benchmarks publics WDBC, Wine et `load_digits` | Jeux de laboratoire compacts, non système de production ; aucune validation clinique ou opérationnelle n'est revendiquée. |
| Règle rouge : données train/val/test distinctes | CONFORME AUX CONTRÔLES EXÉCUTÉS | Audits par hashes de lignes et accès aux partitions ; tous les contrôles listés des trois phases v1.2 passent | Un audit local ne peut exclure absolument tout canal indirect possible. |
| Règle rouge : paramètres cibles cachés | CONFORME AUX CONTRÔLES D'ACCÈS EXÉCUTÉS | Rôles séparés, répertoires privés, modules dédiés et vérification réelle des permissions ; la sonde d'imitation reçoit des paires observées autorisées seulement | Les audits prouvent les accès vérifiés, pas la sécurité contre tout processus hostile. |
| Nouveau protocole, graines neuves et gel préalable | CONFORME | `protocole_isolation_stricte_v1_2.md`, `audit/strict_isolation_v1_2_preexecution_hashes.json` ; graines v1.2 disjointes des campagnes historiques selon les audits | Les résultats de v1.1 invalidés pour graines non nouvelles restent conservés comme historique et ne sont pas confondus avec v1.2. |
| Gel des modèles et répétabilité d'inférence | CONFORME | `audit/strict_isolation_v1_2_inference_replay.json` : 18/18 JSON rejoués identiques octet pour octet | Cela teste la répétabilité de l'inférence des modèles enregistrés, pas une reproductibilité indépendante de chaque environnement matériel. |
| Intégrité/corruption des données de livraison | CONFORME AUX CONTRÔLES EFFECTUÉS | `audit/audit_integrite_livraison_finale_v1_2.json`, SHA-256 des sources et artefacts clés, validation des schémas/tailles/clefs uniques, vérification ZIP indépendante | Les contrôles détectent les différences testées ; ils ne prouvent pas une vérité scientifique ou l'absence de modifications antérieures aux empreintes. |
| Rapport PDF et source | CONFORME | PDF final v1.2 17 pages, source TeX, rendu visuel de toutes les pages, extraction textuelle valide | Les fichiers auxiliaires LaTeX ne sont pas inclus dans l'archive de livraison ; la source `.tex` et les données nécessaires le sont. |
| Code, protocoles, données, résultats, audit, manifestes et archive | CONFORME POUR RÉEXÉCUTION | dossier de projet, `requirements.txt`, scripts, CSV/JSON, références, ZIP final v1.2 | Les poids d'entraînement historiques non sauvegardés ne sont pas inventés : la reproduction des entraînements nécessite de relancer les scripts. |

## Résultats de la réplication stricte v1.2

- Classification : 48 évaluations (4 tâches × 3 graines × 4 méthodes), 13 392 prédictions exportées ; aucun doublon de clé détecté dans les tables canoniques.
- Imitation : 81 modèles entraînés, 324 000 prédictions exportées, 9 cibles × 3 budgets × 3 graines ; mesures finies et clés uniques vérifiées.
- Composition : 96 modèles/sondes de composants, 6 systèmes (deux tâches × trois graines), 18 conditions de remplacement ; 4 752 lignes de prédiction, clés uniques.
- Rejeu d'inférence gelée : 18 sur 18 fichiers identiques octet par octet et sommes concordantes.
- Audits des rôles : classification 12/12, imitation 8/8, composition 14/14 contrôles d'accès réussis. Contrôle des splits : classification 12/12 et composition 6/6 sans chevauchement détecté.

## Conclusion scientifique admissible

Les observations soutiennent que l'instanciation RBF de la sonde peut apprendre des tâches limitées, approximer des neurones simples à partir d'observations entrée-sortie et remplacer localement des unités dans certaines compositions. Les résultats ne démontrent pas que tout neurone soit universellement un cas particulier de toute sonde, que l'équivalence soit exacte, que B découvre un optimiseur général, ni qu'une composition de sondes constitue un réseau autonome complet.

## Résultats et tableaux à utiliser

Pour les mesures par répétition, utiliser `results/strict_isolation_classification_v1_2_by_seed.csv`, `results/strict_isolation_imitation_v1_2_by_target.csv` et `results/strict_isolation_composition_v1_2_by_seed.csv`. Pour les intervalles descriptifs calculés, utiliser les fichiers `*_ci95_v1_2.csv`. Certains CSV historiques de synthèse contiennent des lignes de métadonnées d'agrégation multi-index (cellules numériques vides) ; elles ne sont pas des observations et ne doivent pas être utilisées comme telles. Les CSV de répétitions canoniques testés ici n'ont pas de lignes dupliquées ou de métriques numériques non finies.
