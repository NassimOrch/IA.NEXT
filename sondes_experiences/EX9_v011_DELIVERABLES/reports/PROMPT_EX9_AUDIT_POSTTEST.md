# Audit de conformité du prompt EX9 v011

## Verdict de spécification

**`prompt_ex9.json` est syntaxiquement valide et reprend les exigences de fond du prompt utilisateur.** Le texte embarqué contient les sections 0 à 14, soit 15 sections normatives, avec une section 14 ajoutée après l'audit pré-test pour verrouiller les deux corrections d'implémentation découvertes avant la campagne Rev2.

Le prompt ne présume ni réussite ni échec. Il distingue explicitement résultats historiques, développement, synthétique, pilote, non-exécuté, bloqué et confirmatoire réel. Les écarts d'exécution constatés ci-dessous ne sont pas masqués par la conformité du texte.

## Contrôle des exigences utilisateur

| Exigence de départ | Où elle est traitée dans `prompt_ex9.json` | Vérification |
|---|---|---|
| Reprendre les travaux EX3–EX8 et leurs règles générales | §1, §4, §11 | Présent ; prompts EX3, EX4, EX5, EX6, EX7, EX8 retrouvés et leurs règles communes synthétisées |
| Priorité B10/B11 et récupération de toutes les traces EX8 | §5 | Présent ; sources, configurations, historiques, prédictions et checkpoints audités dans les archives EX8 |
| Ne pas traiter B11 comme contrôle négatif | §5.1 | Présent ; le prompt établit explicitement B11 comme candidate indépendante |
| Poursuivre les ablations de B10 et réduire le coût de l'action language | §5.2, sections B–E | Présent : seuils, cardinalité, marge, désaccord, hard/soft, régularisation, factorisation, distillation et simplification |
| Étudier B11 et ses simplifications | §5.2 E | Présent |
| Suivre A0/PCA et ses hybrides | §6 | Présent : A0 fidèle, local/global seuls, PCA, D/K, fusions, partage, coût complet |
| Prendre au sérieux `th_sondes_core_test_0.tex` | §7 | Présent ; CNG/CNC séparés, graphes, spécialistes, comparateurs, interpolation/extrapolation |
| Formaliser les corrections dans `th_sondes_core_test_1.tex` | §7 et livrable | Réalisé ; source initiale préservée comme base, addendum normatif ajouté, PDF compilé |
| Prioriser ressources, vitesse entraînement et inférence | §2, §9 | Présent ; `P_total`, MAC/FLOPs, exp/RBF, RSS peak, batchs 1/16/64/256, temps end-to-end |
| Ratio d'au moins 4× sur `P_total` | §4.7–8, §2 | Présent ; ratio vérifié par run sur les 45 modèles de classification Rev2 |
| OOF strict et gestion transductive | §4.4–6, §14 | Présent ; contrôles OOF corrigés dans Rev2, initialisation KMeans globale explicitement déclarée `transductive_train_X` pour B10/B11 |
| Jeu confirmatoire réellement vierge et gel avant ouverture | §4, §10 | Présent dans la spécification ; l'ouverture `xor8` a échoué avant toute prédiction et le holdout est désormais déclaré consommé/compromis |
| Conserver tous les échecs et toutes les tentatives | §3, §11–12 | Présent ; runs Rev1 invalidés, pilotes incomplets et incident de holdout conservés |
| Livrer scripts, configurations, résultats, checkpoints, prédictions, logs et hashes | §3, §11 | Présent ; limites de capture historiques (historiques MLP/états optimiseur manquants) documentées |
| Workspace neuf `EX9_v011` sans données historiques dupliquées | §3, §11 | Respecté ; aucune archive ZIP historique ni checkpoint EX3–EX8 dans le workspace EX9 |
| Aucune omission des variantes exécutées | §11 | Respecté avec registre principal, registres complémentaires et index des artefacts |

## Héritage des prompts antérieurs

Les éléments génériques retenus sont :

- **EX3** : non-présomption, interdiction de fabriquer/masquer des résultats, comparaisons loyales, définitions `P_train`/`P_total`, reproductibilité et séparation développement/confirmation.
- **EX4** : budgets appariés sur `P_total`, coûts end-to-end, profilage de l'inférence et des étapes de construction, attention aux sélections et données exposées.
- **EX5** : validation multi-domaines, OOF, ablations, contrôles des branches de coordination, traitement explicite des données externes indisponibles et limites de ressources.
- **EX6** : OOF strict, propriété des observations, comptage des paramètres/buffers et coût d'entraînement, sauvegarde des états et traçabilité.
- **EX7** : architectures récursives/coordination, coût des appels et de l'orchestration, tests externes, séparation des hypothèses et preuves.
- **EX8** : PCA à base commune, récursion compacte, contrôle B10/B11, métriques par graine, audits d'intégrité et prudence sur Wisconsin/SMS déjà exposés.

Les hashes des prompts retrouvés sont dans `inputs/source_provenance_manifest.json`. Les arborescences des workspaces demandés ont un inventaire par hash dans `inputs/source_tree_inventory_addendum.json`.

## Limites de disponibilité des sources

- `last_sources_3.zip` : archive source reçue, taille 336 478 208 octets, SHA-256 `aee5b5e9e4dbd2f87e90de04e0473a3369aabe0b4e91675fb5909e8842bb74c1`; l'audit CRC initial est PASS.
- Les arbres `sondes_research_workspace_final`, EX4, EX5, EX6, EX7 V005, EX7 V003, EX8 résultats/méthodes, dossier B10 complet et `sources_ng_adapt_0` sont inventoriés.
- `sonde_adapt_global_research_final.zip` n'est pas présent comme archive ou répertoire distinct dans le contenu reçu. Il n'est pas prétendu avoir été inspecté sous ce nom.
- Les fichiers sources EX3–EX8 restent à l'extérieur de `EX9_v011`; le workspace ne contient que provenance, audit et nouveaux artefacts EX9.

## Conformité de l'exécution

Le prompt est conforme comme **spécification**, mais son exécution complète n'est pas atteinte dans cette session. Les branches réellement exécutées et les branches partielles/bloquées sont détaillées dans `EVIDENCE_MATRIX_EX9.md`. En particulier : pas de confirmation réelle externe, pas de résultat test `xor8`, pas de matrice A0 complète, pas de graphes CNC C1/C2 complets, et plusieurs profils de ressources restent `ND`.

**Conclusion : prompt final valide ; exécution partielle mais auditable ; aucune prétention d'achèvement scientifique complet.**


## Mise à jour de reprise et conformité d'exécution (2 novembre 2026)

Après la première interruption, l'état du workspace a été vérifié sans relancer les 45 runs principaux, les neuf pilotes CNG/CNC, les 35 ablations B10 ni le holdout `xor8`. L'audit a confirmé leurs artefacts et hashes. Les 35 ablations B10 sont désormais inventoriées, auditées et accompagnées d'une analyse de parité des seuils HARD_3X3 (aucun tie exact train/validation, donc aucun désaccord de bins sur les cinq seeds).

Les deux domaines synthétiques restants pré-déclarés (`concentric2`, `rotated_moons2`) ont ensuite été exécutés : 90 runs supplémentaires (45/domaines), avec checkpoints, configurations, prédictions, JSON et historiques MLP complets. L'audit indépendant validation passe 90/90. Un verrou séparé de 295 empreintes a été gelé, les 90 checkpoints ont été chargés avant toute génération test, puis les deux holdouts synthétiques ont été scorés une seule fois. L'audit des métriques depuis les prédictions sauvegardées passe 90/90, sans régénérer de données ni réexécuter les modèles.

Cette extension satisfait la confirmation **synthétique** multi-domaines, mais ne satisfait pas la demande de confirmation sur un jeu réel vierge. Aucun dataset réel externe neuf n'a été obtenu ou validé dans l'environnement hors-ligne. La branche CNG/CNC reste un pilote partiel : les graphes C1/C2 complets, la matrice M=1/2/4/7 et les comparateurs restent non exécutés. Les ablations structurelles avancées B10/B11 (distillation, partage RBF, kernels rapides) et la série complète A0 restent également partielles.

**Verdict d'exécution :** le prompt EX9 est construit et validé comme spécification ; l'exécution est substantielle, traçable et comprend désormais trois domaines synthétiques (un holdout xor8 compromis, deux holdouts synthétiques scorés), mais elle demeure partielle au regard du prompt de base (données réelles vierges, CNG/CNC complète, ablations end-to-end et mesures FLOPs/RSS/énergie complètes). Aucune réussite n'a été présumée.
