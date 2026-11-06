# Rapport de validation P11 — robustesse, sûreté et performances

Date de vérification : 2026-10-26T13:59:30+00:00

## 1. Description

P11 valide les frontières d’entrée, les permissions des données, la résistance à la corruption, la reprise après interruption, l’idempotence des événements, les limites de ressources et les performances sur des fixtures reproductibles. Ce rapport est fondé sur des reçus enregistrés et des manifests vérifiés, et non sur une promesse de performance universelle.

## 2. Architecture

Le noyau intégré utilise un AST versionné, un interpréteur explicite, des services SQLite transactionnels, un journal d’audit append-only, des checkpoints signés par hash, une frontier de synthèse paresseuse et des adaptateurs spécialistes identifiés par provenance. Les sources originales vendoriées sont vérifiées séparément du noyau intégré.

## 3. Pipeline complet

1. Préflight des chemins, checklists d’erreurs et état de phase.
2. Tests d’entrées invalides, de références/chemins, corruption des payloads/checkpoints et permissions POSIX.
3. Injection d’arrêt brutal, fermeture/réouverture SQLite, rejeu idempotent et tests de conflits d’effets/budgets.
4. Mesures du runtime mémoire et durable sur une entrée d’addition fixe avec résultat sémantique identique.
5. Mesures de frontière paresseuse contre une référence eager, puis comparaison de l’API publique à la voie prévalidée sur la même grammaire.
6. Exécution isolée des tests amont, vérification des hashes vendoriés, préservation d’ASCR, inspection de la présence des morceaux de base eGenBrain et vérification/restauration du dernier savepoint.

## 4. Commandes d'exécution

```bash
python scripts/run_checked.py --label p11-integrated-suite-final-before-phase-closure --kind no_model -- python -W error::ResourceWarning -m pytest -q
python scripts/run_checked.py --label p11-verify-vendor-source-hashes-final --kind no_model -- python scripts/verify_vendor_sources.py
python scripts/run_checked.py --label p11-ascr-source-preservation-verify-final --kind no_model -- python scripts/verify_ascr_source_preservation.py
python scripts/run_checked.py --label p11-savepoint-restore-final --kind no_model -- python scripts/savepoint.py verify --restore-smoke
```

Les suites amont séparées et les benchmarks sont référencés par leurs reçus JSON dans `logs/executions/P11/`.

## 5. Résultats

- Suite intégrée : **263 tests** et **174 sous-tests réussis**, sans `ResourceWarning`.
- Suites amont isolées : référence FulleGenBrain 46, AAM O82 105, ORDER O76 13, ORDER 80.2.2 11, soit **175 tests réussis** dans ces quatre suites.
- Vérification de provenance vendoriée : 4 composants, 298 fichiers vendoriés vérifiés, 297 fichiers source comparés, zéro divergence.
- Préservation ASCR : 4 fichiers contrôlés, tous identiques aux hashes du manifeste.
- Frontière combinatoire : vitesse médiane de l’API publique / voie prévalidée = **8.751×** sur le fixture spécifié; émissions et frontier finale identiques. Eager/lazy et la mémoire sont mesurés séparément.
- Fixture d’addition : résultats sémantiques identiques et intégrité SQLite/trace PASS.
- Source initiale `source_orderX_0.zip` : 493682442 octets, SHA-256 `e423f5f207eba4b38ed5606da81e00eb74504410f77c251a82dcef23a1ee3303`, test CRC ZIP PASS.
- Savepoint : 1321 fichiers vérifiés, restauration smoke test PASS.

## 6. Interprétation des résultats

Les tests et contrôles passent pour les chemins exercés. Les benchmarks sont des micro-mesures propres aux fixtures fournies; ils ne prédisent pas le comportement de toute grammaire et ne sont pas présentés comme une comparaison équivalente avec les anciens modèles. Les tests amont sont exécutés séparément pour respecter leurs chemins et environnements d’origine.

Le registre eGenBrain reste **PARTIAL** concernant la base SQLite historique : le `part01` de 824389632 octets correspond à son manifeste, mais `part02` est absent de tous les répertoires et archives fournis. Le contrôle web exact nom/hash n’a retourné aucun résultat public. Aucun octet n’est fabriqué; la voie mesh autonome est testée, mais le modèle hérité MG n’est pas déclaré reconstitué.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

- Théoriques : la validation avant effet et les statuts `PARTIAL/UNRESOLVED` restent distincts d’une preuve de correction universelle.
- Conceptuelles : les mécanismes d’élagage paresseux et de validation sont utiles sur les fixtures contrôlées; leur portée et leurs hypothèses sont documentées.
- Opérationnelles : le stockage est privé sur POSIX, la reprise contrôlée vérifie les hashes, les tests amont ne polluent pas la découverte pytest intégrée et les données sources restent traçables.

## 8. Conclusions

Les critères P11 sont satisfaits pour le périmètre exécutable et les scénarios testés; le registre n’a aucune erreur ouverte. La disponibilité partielle de la base eGenBrain héritée demeure une limitation des données d’entrée et est exposée dans les preuves, non dissimulée.

## 9. Statut du modèle

**P11 PASS**. Phases P00–P11 validées. P12 — documentation, licence et empaquetage — devient la première phase active. La qualification finale de release dépendra de la reconstruction propre et de la vérification des trois livrables.
