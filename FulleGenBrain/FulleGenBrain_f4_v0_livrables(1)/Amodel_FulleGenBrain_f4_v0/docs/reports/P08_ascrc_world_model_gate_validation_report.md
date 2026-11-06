# P08 — ASCRC, préservation d’ASCR et porte du modèle du monde

## 1. Description
Cette phase isole l’ordonnancement de ressources (ASCRC) du mécanisme historique ASCR d’eGenBrain, conserve les sources vérifiables par empreintes et ajoute une porte empirique pour l’activation d’un modèle de transition optionnel. L’adaptation vectorielle étend le prototype ASCRC V4 scalaire; elle ne se prétend pas identique dans tous les domaines à la référence.

## 2. Architecture
- `src/fullegenbrain/runtime/ascrc.py` : vecteurs de ressources nommées, budget dur par dimension, sélection et application atomique, pins/baux/transactions, contexte, dépendances, états `STALE`/`BLOCKED`/`REVOKED`, réveil comme demande, révocation différée jusqu’à l’arrêt sûr, snapshots et journal SHA-256 chaîné.
- `src/fullegenbrain/runtime/world_model_gate.py` : protocole immuable, registre append-only chaîné, paires de mesures, contrôle de protocole et de partition, seuil bootstrap de gain de `decision_utility`, plafond de coût supplémentaire et refus sur sûreté.
- `spec/upstream/reference_impl/` : référence V4 conservée sans modification; son empreinte est enregistrée dans `spec/evidence/ascr_source_preservation.json`.

## 3. Pipeline complet
1. Contrôler l’identité et les contrats des candidats.
2. Mesurer la consommation des candidats actifs; refuser un budget inférieur à la consommation existante.
3. Construire un plan sous budget résiduel, enregistrer raisons de report et empreintes.
4. Revalider hash, tick, empreintes, dépendances, contexte, état et coûts lors de l’application; ne changer les états qu’après validation exhaustive.
5. Conserver les ressources d’un candidat actif stale/révoqué jusqu’à l’arrêt sûr.
6. Pour le modèle du monde, enregistrer le protocole avant les mesures, vérifier les paires holdout, l’effectif, le gain avec borne bootstrap, le coût et la sûreté; sinon rester inactif.
7. Émettre preuve, diagnostic et événements chaînés; ne jamais transformer un score en statut épistémique.

## 4. Commandes d'exécution
```bash
python scripts/run_checked.py --label p08-ascrc-source-preservation-final-recheck --kind no_model -- env PYTHONPATH=src python3 scripts/verify_ascr_source_preservation.py
python scripts/run_checked.py --label p08-ascrc-and-world-gate-targeted-retest2 --kind model -- env PYTHONPATH=src python3 -W error::ResourceWarning -m unittest tests.test_p08_ascrc tests.test_p08_world_model_gate -v
python scripts/run_checked.py --label p08-full-suite-after-ascrc-fixes --kind model -- env PYTHONPATH=src python3 -W error::ResourceWarning -m unittest discover -s tests -v
python scripts/run_checked.py --label p08-compile-versioned-formalisms --kind no_model -- python3 scripts/validate_latex_sources.py
```

## 5. Résultats
- Les quatre fichiers ASCR historiques (`core.py`, `v2.py`, `v3.py`, `v4.py`) ont la longueur et le SHA-256 du manifeste de l’archive. Les fichiers référence ASCRC et world-gate et leurs tests conservent également les empreintes inscrites dans le rapport de préservation. Voir `spec/evidence/ascr_source_preservation.json`.
- Tests ciblés P08 : 27 réussis, receipt `logs/executions/P08/20261026T112820183894+0000_p08-ascrc-and-world-gate-targeted-retest2.receipt.json`.
- Suite complète : 195 réussis, zéro échec, `ResourceWarning` traité comme erreur; receipt `logs/executions/P08/20261026T112834099316+0000_p08-full-suite-after-ascrc-fixes.receipt.json`.
- Le test initial de P08 a échoué sur deux attentes de test : il attendait qu’une révocation bloque le planificateur entier plutôt que l’élément révoqué, et que la demande de réveil non finançable reste `DORMANT` plutôt que `BLOCKED`. Les assertions ont été corrigées selon les contrats opérationnels et le retest ciblé ainsi que la suite complète passent.
- Les valeurs SHA-256 détectent la modification des fichiers vérifiés; elles ne sont pas des signatures cryptographiques et ne garantissent pas l’identité de l’auteur.

## 6. Interprétation des résultats
L’implémentation respecte les plafonds déclarés par dimension et conserve la consommation des tâches actives tant qu’elles ne sont pas arrêtées sûrement. Les comparaisons avec V4 montrent une projection scalaire concordante sur les cas testés, sans preuve d’équivalence totale. La porte world-model est un filtre de déploiement empirique à portée limitée; elle ne prouve ni causalité ni validité générale et ne remplace pas un protocole d’évaluation propre au domaine.

## 7. Conséquences théoriques, conceptuelles et opérationnelles
### Théoriques
Le contrat affine la spécification de l’allocation comme ordre vectoriel sous ressources déclarées, avec commit conditionné par empreintes stables et absence de mutation concurrente dans la section critique.
### Conceptuelles
ASCR reste le mécanisme spécialisé historique; ASCRC est un plan distinct d’allocation/résidence. Les statuts épistémiques ne sont pas calculés par l’ordonnanceur. Un modèle du monde optionnel n’est activé que sous un protocole défini et une utilité appariée évaluée.
### Opérationnelles
La sélection et le commit sont deux opérations séparées; les budgets sont des filtres durs; les événements de réveil n’accordent aucun privilège; l’état `revocation_pending` ne libère pas prématurément les ressources. La porte world-model reste inactive à défaut de données et protocole conformes.

## 8. Conclusions
Les critères de phase P08 sont couverts par la vérification de provenance ASCR, les tests vectoriels ASCRC, les tests de gate, le rapport de validation et le passage de la suite complète. Ces observations attestent les artefacts et scénarios précis du dépôt, non une absence universelle de défauts ni un effet bénéfique général du modèle du monde.

## 9. Statut du modèle
**P08 PASS** après validation LaTeX et mise à jour des registres. Le modèle global demeure en développement : les phases P09–P13 portent encore sur les adaptateurs historiques, CLI/GUI, robustesse, documentation/conditionnement et audit de release.
