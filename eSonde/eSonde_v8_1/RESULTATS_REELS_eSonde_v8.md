# Résultats réels eSonde v8 — 17 novembre 2026

## Description
Snapshot expérimental chat-only, héritant du moteur Obsiss/P-R V7 et du checkpoint V6, avec profil OASST1 agrégé et règles de proposition v8.

## Architecture
Le profil OASST1 apporte associations contextuelles et transitions de réponses; le routeur linguistique hérité filtre les associations et neutralise les transitions OASST1 multi-langues quand une langue spécifique est reconnue. Les Obsiss/P-R hérités évaluent les candidats. Aucun composant neuronal/MLP n'est ajouté.

## Pipeline complet
Profil TRAIN agrégé; ancres du prompt/historique avec récence; associations de tokens; backoff trigramme/bigramme/unigramme; route de langue; fusion neutre si absence d'évidence; classement Obsiss/P-R.

## Commandes
`PYTHONPATH=src pytest -q tests`; `RUN_CLI.py status --workspace .`; `RUN_CLI.py verify --workspace .`.

## Résultats
81 tests PASS; status/verify PASS; checkpoint et profil SHA vérifiés. Ablation teacher-forced : couverture 46,2% → 86,3% au seuil minimum 1, précision top-5 tous tokens 20,67% sur le protocole décrit dans les rapports source. Tables linguistiques séparées : arrêtées à 10 750/48 557 lignes, sans publication. Baseline V7 : timeout à 300 secondes, 0/3 génération complète. Aucun chat libre v8 achevé.

## Interprétation
Les métriques teacher-forced mesurent le choix du token suivant sous contexte cible, pas une conversation auto-régressive complète. 81 tests mesurent du logiciel, pas de l'intelligence ou de la cohérence générale.

## Conséquences théoriques, conceptuelles et opérationnelles
La séparation des bases CountSketch/observations reste à prouver; les observations sont redondantes jusqu'à mesure contraire; PCH n'est pas encore runtime. Le profil reste statistique, sans mémoire de paires prompt/réponse. Les validations externes et le savepoint sont requis avant la génération.

## Conclusions
Les modules, profil et interfaces sont construits et testés au niveau logiciel; les résultats de cohérence libre et généralisation ne sont pas encore disponibles.

## Statut du modèle
P0 `IN_PROGRESS`; P1/P2/P3/P4 `NOT_STARTED`; qualité libre `NON_EVALUE`. Aucun verdict anticipé de succès ou d'échec.
