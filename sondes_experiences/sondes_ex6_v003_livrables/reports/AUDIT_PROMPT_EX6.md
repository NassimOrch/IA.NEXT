# AUDIT_PROMPT_EX6

Révision auditée : `1.0.1`  
Fichier : `prompt_ex6.json`  
SHA-256 : `72744213da2626174e63c45256a6e7a69c6de84c2b810d7a4a94e931c885237c`  
Encodage : UTF-8 JSON valide  
Nombre de sections numérotées : 19 (sections 0 à 18)

## 1. Vérifications structurelles

- Le JSON se parse sans erreur.
- Les copies racine, version et `inputs/prompt_ex6.json` sont identiques octet pour octet.
- Les prompts EX3, EX4 et EX5 sont inclus dans `inputs/`.
- Les formalismes théoriques, le fichier de réflexions historique, le manifeste du split et les scripts de référence sont inclus.
- Les sections 0–18 existent et le prompt relie exigences, garde-fous, ordre d'exécution, livrables et règles de verdict.
- La révision 1.0.1 nomme explicitement l'interdiction de triche et de sabotage, et garde la règle de non-préjugement des résultats.

## 2. Contrôle méthodologique de bout en bout

| Domaine | Exigence dans EX6 | Contrôle |
|---|---|---|
| Neutralité | Aucun présupposé de succès ou d'échec ; résultats défavorables conservés | Présent |
| Anti-triche | Pas de sous-dimensionnement du MLP, asymétrie d'entraînement/données, paramètres cachés, sélection après résultat ou effacement | Présent |
| Anti-sabotage | Pas de manipulation ou de favoritisme direct/indirect ; timeouts et erreurs conservés | Présent |
| Paramètres | P_train, P_fixed, buffers, prétraitement, P_total et copies comptés | Présent |
| Baselines | MLP matched et MLP-ge4x recréés pour chaque candidate et graine | Présent |
| Données | Train/adaptation/validation/test séparés ; historique exposé marqué développement | Présent |
| Replica | Clone figé, flux de gradients, partition de calcul, duplication, sérialisation et mesures serial/parallèle | Présent |
| Emplica simple | Hétérogène, homogène, spécialiste, budgets contrôlés, interfaces et OOF | Présent |
| Orchestra | Global externe + local/global interne, variantes, messages, OOF, activation/cascade et ablations | Présent |
| Ressources | Temps total, latences p50/p95/p99, débit, MAC/FLOP, RSS/VRAM, bytes, énergie si instrumentée | Présent |
| Statistiques | Comparaisons appariées, intervalles, marges NI pré-enregistrées, multiplicité et domaines indépendants | Présent |
| Traçabilité | Workspaces versionnés, JSONL append-only, checksums, logs, checkpoints et audits | Présent |
| Verdict | Réussite conjonctive ; `NON MESURÉ`, `NON EXÉCUTÉ`, `NON VÉRIFIÉ` explicites | Présent |

## 3. Examen des trois nouvelles idées

### Replica
L'idée utilisateur peut correspondre à plusieurs mécanismes qui ne sont pas mathématiquement équivalents. Le prompt exige d'isoler : (a) la partition d'experts, (b) le partitionnement de calcul interne, (c) la répartition du batch pour le débit, (d) le partage d'intermédiaires/fusion. Il exige aussi une distinction entre copie gelée pour inférence, assistance en entraînement avec règle de gradient démontrée et copie périodiquement rafraîchie. C'est nécessaire : une copie gelée ne peut pas fournir des gradients au modèle primaire sans chemin explicite défini.

### Emplica simple
Le prompt transforme l'exemple 7×5 en plan de bras contrôlés plutôt qu'en architecture unique : hétérogène, homogène avec la meilleure variante, spécialiste par couche, contrôle mono-couche et ablations. Les sorties de couche et les résidus doivent être formalisés ; OOF ou procédure d'entraînement conjoint équivalente exigés pour éviter la fuite de prédictions in-sample.

### Emplica Orchestra
La hiérarchie voulue est explicite : adaptation globale externe sur des couches dont chacune contient adaptation locale et globale interne. Les états locaux, globaux par couche et externes sont séparés. Les familles hétérogène/homogène/spécialiste, gates statiques/input-conditioned, ablations sans messages, OOF et cascades sont distinguées. Le prompt interdit d'utiliser les vrais labels à l'inférence et impose de mesurer la sélection/activation de couche.

## 4. Point critique de faisabilité

Le prompt est cohérent comme protocole complet, mais il dépasse ce qui est réalisable avec un seul split historique et le matériel CPU disponible. La section 16 impose des domaines indépendants et une validation finale après gel ; elle ne peut pas être réputée exécutée par les pilotes EX6 actuels.

Les pilotes déjà exécutés dans ce workspace sont descriptifs et postérieurs à la rédaction initiale du prompt. Les configs/scripts enregistrés permettent de les reproduire, mais ils ne doivent pas être requalifiés rétrospectivement comme pré-enregistrés. La révision 1.0.1 corrige le texte d'intégrité mais ne rend pas rétroactivement ces pilotes pré-enregistrés.

## 5. Ambiguïtés résiduelles à régler avant confirmatoire

1. Définir les marges de non-infériorité d'accuracy et de log-loss par domaine, avec justification, avant l'accès au jeu externe.
2. Fixer le coût budgétaire maximum et les tailles batch réellement pertinentes pour le déploiement, sans choisir en fonction des résultats du pilote.
3. Formaliser le flux de gradient de Replica si le calcul partagé est actif pendant l'entraînement.
4. Pré-définir le protocole OOF pour les résidus inter-couches, incluant folds, répétitions et coût de calcul.
5. Spécifier comment la variante « spécialiste par couche » est choisie dans une boucle imbriquée sans réutiliser la validation externe.
6. Fixer le protocole énergétique si un instrument calibré devient disponible ; sinon cette dimension demeure `NON MESURÉ`.

## 6. Verdict d'audit du prompt

**VALIDÉ COMME CAHIER DES CHARGES SCIENTIFIQUE EX6.** La structure contient les règles rouge anti-triche/anti-sabotage, la protection des sources, le workspace versionné, les trois architectures et la règle de verdict neutre. 

**VALIDÉ NE SIGNIFIE PAS EXÉCUTÉ.** L'exécution présente est partielle et le statut de la campagne est `INCOMPLET`. Aucune architecture n'a validé le succès global avec les données et mesures disponibles.
