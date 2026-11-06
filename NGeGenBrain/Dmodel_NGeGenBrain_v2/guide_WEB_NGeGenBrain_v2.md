# Guide Web — NGeGenBrain_v2

Lancer `python ngbrain.py serve --host 127.0.0.1 --port 8766`, puis ouvrir `http://127.0.0.1:8766/`. Le serveur intégré accepte uniquement une adresse loopback.

## Interface utilisateur

Le tableau de bord permet de vérifier l'état des registres, d'interroger un modèle synthétique et de lancer le benchmark de reconstruction. Les résultats sont montrés sous forme JSON afin de préserver les champs de preuve et de provenance.

## API locale

| Méthode | Route | Action |
|---|---|---|
| GET | `/api/status` | santé, version et vérification des registres |
| GET | `/api/models` | modèles synthétiques et adapters connus |
| GET | `/api/experiments` | historique d'expériences et intégrité |
| GET | `/api/hypotheses` | hypothèses persistées |
| GET | `/api/observations` | observations persistées |
| GET | `/api/discovery` | résultats de découverte enregistrés |
| GET | `/api/reconstruction` | manifeste de reconstruction le plus récent |
| GET | `/api/plans` | plans expérimentaux enregistrés |
| GET | `/api/sweeps` | balayages d’interventions enregistrés |
| GET | `/api/counterexamples` | résultats de recherche de contre-exemples |
| GET | `/api/synthetic_ladder` | journal des essais d’architectures synthétiques |
| POST | `/api/observe` | corps `{"x":[0,1,0,1]}` |
| POST | `/api/experiments/intervention` | corps avec `bits`, `input`, `target`, `mode`, `parameters` |
| POST | `/api/hypotheses` | crée une hypothèse avec description et origine |
| POST | `/api/hypotheses/update` | met à jour un objet hypothèse fourni et conserve son historique |
| POST | `/api/discover` | découverte booléenne ou arithmétique avec jeu de validation séparé |
| POST | `/api/compose` | exécute un mécanisme du DSL contrôlé |
| POST | `/api/benchmark` | lance une expérience synthétique aveugle |
| POST | `/api/synthetic-ladder` | exerce huit architectures synthétiques et inscrit le résultat |
| POST | `/api/reconstruct-causal-lm` | entraîne un minuscule Transformer causal synthétique, découvre une règle sur train puis l’évalue sur holdout, compose deux reconstructions indépendantes et ajoute un événement à `reconstruction.jsonl` |
| POST | `/api/plan` | propose un plan en tenant compte des capacités déclarées |
| POST | `/api/experiments/sweep` | répète baseline/intervention sur plusieurs entrées |
| POST | `/api/counterexamples` | compare un candidat à des lignes fournies |
| POST | `/api/features/summary` | statistiques descriptives de captures |
| POST | `/api/activations/store` | stocke des activations comprimées avec hashes |
| POST | `/api/activations/verify` | vérifie l’intégrité des activations stockées |
| POST | `/api/reproducibility` | manifeste environnement et artefacts |
| POST | `/api/reconstruction` | alias de lancement de reconstruction synthétique |
| POST | `/api/validate` | vérifie les registres et un manifeste |
| POST | `/api/replay` | rejoue le protocole synthétique d'un manifeste et compare les métriques |
| POST | `/api/export` | exporte un registre dans `workspace/exports/` |
| POST | `/api/report` | écrit le rapport courant dans le workspace |

Les routes écrivent dans le `workspace` du serveur. Pour les actions longues, prévoir un workspace dédié. Le serveur intégré ne doit pas être exposé sur un réseau non fiable ; il n'implémente pas d'authentification réseau.

## Reconstruction causale via Web

La carte **Reconstruction d’un petit Transformer causal** appelle `POST /api/reconstruct-causal-lm` avec `seed`, `vocab_size`, `epochs` et `max_new_tokens`. Le résultat public donne le hash source, la matrice de capacités boîte noire, la qualité de la règle sur le holdout, la concordance des trajectoires, la fidélité de la table de logits sur le domaine interrogé et le hash d’enregistrement. La vérité de construction est écrite seulement dans `workspace/causal_lm_reconstruction/auditor_only/hidden_ground_truth.json`. Le test d’API vérifie aussi la présence de cette séparation.

Cette expérience porte sur un modèle synthétique entraîné, pas sur un checkpoint LLM pré-entraîné externe. La route n’autorise ni téléchargement réseau ni exécution de code du modèle. Le serveur reste limité à loopback ; il ne doit pas être exposé à un réseau non fiable.
