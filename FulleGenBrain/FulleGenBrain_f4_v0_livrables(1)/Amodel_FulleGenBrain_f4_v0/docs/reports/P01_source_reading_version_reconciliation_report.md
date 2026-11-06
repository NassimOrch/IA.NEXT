# Rapport de validation — P01 : lecture des sources et réconciliation des versions

**Modèle :** `FulleGenBrain_f4_v0`  
**Date :** 26 octobre 2026  
**Statut :** `PASS` dans la portée des sources effectivement livrées et examinées.

## 1. Description

P01 établit une hiérarchie de provenance pour éviter un assemblage arbitraire de modèles. L'architecture FulleGenBrain 4 gouverne l'intégration; la théorie compositionnelle 2 gouverne la sémantique; l'interface 4 est un prototype de conception, non la spécification autoritaire du runtime.

## 2. Architecture

Les pièces sont classées en sources canoniques, modèles historiques exécutables, audits seulement, versions de comparaison et données incomplètes. La matrice de réconciliation associe à chaque adaptation une provenance, une justification et une preuve de test quand elle est applicable.

## 3. Pipeline complet

1. Lire les trois documents canoniques FulleGenBrain 4.
2. Examiner les registres de validation, scripts, points d'entrée et suites historiques.
3. Distinguer ORDER, AAM et eGenBrain par version et type de preuve.
4. Relever les chevauchements et contradictions sans écraser les sources d'origine.
5. Produire `docs/source_reconciliation.md`, `spec/evidence/source_reconciliation_matrix.json` et les empreintes canoniques.
6. Maintenir les sources antérieures dans `spec/upstream` et `vendor` avec leurs notices.

## 4. Commandes d'exécution

```sh
python scripts/run_checked.py --label p01-preflight --kind no_model -- python scripts/preflight.py --read-only-check
python scripts/run_checked.py --label p01-verify-vendored-sources --kind no_model -- python scripts/verify_vendored_files.py
```

## 5. Résultats

- `spec/upstream/formalisme_FulleGenBrain_4.tex`, `theorie_programation_compositionnelle_2.tex` et `interface_FulleGenBrain_4.tex` sont préservés.
- `formalisme_FulleGenBrain_5.tex` et `theorie_programation_compositionnelle_3.tex` portent les évolutions, sans remplacer les originaux.
- Le contrôle de sources vendoriées a vérifié 298 fichiers sur quatre composants, sans différence signalée dans le dernier reçu PASS.
- L'inventaire eGenBrain signale explicitement le fragment `part02` manquant.
- AAM O94.6 et ORDER 80.4.7 demeurent documentés comme audit/comparaison lorsqu'aucun runtime source compatible n'est disponible; leurs fonctions ne sont pas fabriquées.

## 6. Interprétation des résultats

La réconciliation prouve que les sources auditées ont été identifiées et que leurs rôles sont consignés. Elle ne prouve pas que tout le contenu possible des dépôts historiques a été transmis, ni que chaque extension est équivalente en toutes circonstances à une version source. Les adaptations fonctionnelles possèdent des tests et reçus spécifiques.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

### Théoriques

Les responsabilités formelles et opérationnelles restent séparées; les invariants de composition priment sur le prototype d'interface.

### Conceptuelles

Les apports de sources différentes ne sont pas fusionnés sans justification; audit, comparaison et exécution sont des catégories différentes.

### Opérationnelles

Les manifestes, hashes, reçus et notices rendent les origines traçables et révèlent les morceaux absents.

## 8. Conclusions

La matrice de provenance et les sources canoniques ont été établies. Les limites liées aux sources manquantes sont visibles et ne sont pas cachées derrière un statut global.

## 9. Statut du modèle

**P01 : `PASS` pour la réconciliation des sources disponibles.** La base historique eGenBrain reste `PARTIAL` tant que son second fragment n'est pas fourni et vérifié.
