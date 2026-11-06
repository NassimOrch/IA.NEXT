# Rapport P12 — documentation, licence et préparation des livrables

Vérification de travail : 26 octobre 2026. Ce rapport est mis à jour après la construction et la vérification finales des archives.

## 1. Description

P12 regroupe la documentation de bout en bout, les conditions de réutilisation, la traçabilité des sources et la préparation des trois livrables demandés. La publication sur GitHub n'est pas exécutée : les archives sont préparées localement, vérifiées et laissées à la décision de l'auteur.

Le paquet d'exécution vise le noyau Python autonome, fondé sur la bibliothèque standard. Les tests de développement requièrent `pytest`; chaque modèle historique amont garde ses propres prérequis, licence et état d'exécutabilité. Les éléments `AUDIT_ONLY`, `COMPARISON_ONLY`, `PARTIAL`, `BLOCKED` et `MISSING_SOURCE` ne sont pas requalifiés en runtimes complets.

## 2. Architecture

Le dépôt présente un `README.md` français, `LICENSE` non commerciale pour les nouveaux éléments FulleGenBrain, `THIRD_PARTY_NOTICES.md`, `.gitignore`, les guides CLI et UI, les formalismes versionnés, les schémas JSON, les exemples, les sources amont préservées, les adaptateurs, les reçus d'exécution et les rapports normalisés. Le paquet `Dmodel` contient le noyau, les assets locaux et les éléments requis pour une exécution native; `Amodel` regroupe preuves, rapports, historiques et journaux; `suivi_model` apporte checklists, tests, outils de vérification et formalismes de suivi.

La licence non commerciale ne se substitue pas aux licences des œuvres amont. Les usages des composants vendoriés restent soumis aux notices correspondantes. L'archive source originale n'est pas modifiée par le build et reste disponible au chemin enregistré dans `chemins_FulleGenBrain_f4_v0.json` de l'environnement de travail.

## 3. Pipeline complet

1. Lire et valider les chemins, la checklist de phase et les deux registres d'erreurs.
2. Vérifier les sources amont avec manifests et SHA-256; vérifier l'archive originale par CRC ZIP et hash.
3. Rejouer les tests intégrés, les commandes CLI documentées dans des répertoires de données temporaires et les contrôles de compilation LaTeX enregistrés.
4. Vérifier la cohérence des guides, liens, neuf sections des rapports, licences et preuves.
5. Construire chaque ZIP avec un manifeste interne listant la taille et le SHA-256 de chaque membre; vérifier CRC, inventaire et hashes avant livraison.
6. Extraire les paquets dans un environnement propre, exécuter les contrôles d'exécution minimaux, puis reconstruire les archives finales après l'ajout du rapport P13.
7. Vérifier une dernière fois les trois fichiers livrés et émettre un manifeste de livraison externe contenant leurs tailles et SHA-256.

## 4. Commandes d'exécution

Depuis la racine du projet :

```bash
python scripts/run_checked.py --label p12-docs-gate --kind no_model -- python scripts/validate_p12_documents.py
python scripts/run_checked.py --label p12-tests --kind model -- python -W error::ResourceWarning -m pytest -q
python scripts/run_checked.py --label p12-vendor-hashes --kind no_model -- python scripts/verify_vendor_sources.py
python scripts/run_checked.py --label p12-eGenBrain-fragments --kind no_model -- python scripts/verify_egenbrain_reassembly.py
python scripts/run_checked.py --label p12-package --kind no_model -- python scripts/package_deliverables.py
python scripts/run_checked.py --label p12-package-check --kind no_model -- python scripts/verify_deliverable_archive.py /path/to/Dmodel_FulleGenBrain_f4_v0.zip
```

Les commandes `check_cli_examples_bounded.py --group core|run|memory|services` ont été exécutées via le lanceur contrôlé dans des répertoires temporaires. Les durées limite sont documentées dans chaque reçu; l'évaluation de synthèse sous budget ne vaut pas preuve universelle. Le serveur UI se lance sur loopback (`127.0.0.1`) et n'active pas implicitement d'accès réseau externe.

## 5. Résultats

Résultats présents à la préparation du rapport :

- Suite intégrée actuelle : 263 tests et 174 sous-tests passés, avec `ResourceWarning` traité comme erreur.
- Exemples CLI documentés : 18 commandes passées dans quatre groupes `core`, `run`, `memory` et `services`, chacun sur une zone de données temporaire; le groupe `services` a été retesté avec un délai par commande de 15 s après que 5 s se soit révélé trop court.
- Vérification de source : archive `source_orderX_0.zip` de 493 682 442 octets, SHA-256 `e423f5f207eba4b38ed5606da81e00eb74504410f77c251a82dcef23a1ee3303`, CRC ZIP PASS.
- Provenance vendoriée : 298 fichiers vérifiés, 297 comparés directement à l'arbre source disponible, zéro divergence.
- ASCR : fichiers sources vérifiés identiques aux manifestes; ASCR reste séparé du contrôleur ASCRC.
- Formalismes : les trois documents ont un rapport de compilation deux passes à code de sortie zéro; la réattestation courante confirme que les logs sont postérieurs aux sources actuelles, les PDF compilés sont présents et aucun `Overfull \hbox` n'est recensé. Les avertissements `Underfull \hbox` sont consignés, pas dissimulés. La dernière invocation wrapper de compilation n'a pas émis de reçu; l'attestation LaTeX l'indique explicitement au lieu de prétendre qu'elle a produit un reçu.
- Fragment eGenBrain : `part01` conforme, `part02` absent; le statut de reconstitution demeure `PARTIAL` et aucun octet n'est fabriqué.
- Sauvegardes : le manifeste de la sauvegarde la plus récente est vérifiable; un test de restauration antérieur a restauré 1 453 fichiers sans erreur de hash.

Les tailles et SHA-256 de livraison ne seront considérées finales qu'après reconstruction et vérification des trois archives finales; ils sont consignés dans `deliverables/release_manifest.json` hors des archives elles-mêmes pour éviter une empreinte auto-référentielle.

## 6. Interprétation des résultats

Les résultats étayent l'exécutabilité du noyau natif, la cohérence des interfaces documentées et l'intégrité des fichiers contrôlés. Ils ne constituent pas une preuve de correction universelle pour tous les programmes possibles. Les benchmarks portent sur des fixtures fixes, l'évaluation UI est report-only et ne sélectionne/promeut pas les candidats, et les statuts de sources historiques restent conservateurs.

L'archive principale passe le contrôle de CRC; les composants vendoriés ont une provenance et des hashes explicites. L'absence de la moitié de la base historique eGenBrain est une lacune d'entrée documentée, pas un résultat négatif sur la faisabilité globale du projet et pas un motif pour générer de fausses données.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

- **Théoriques :** les formalismes `formalisme_FulleGenBrain_5.tex` et `theorie_programation_compositionnelle_3.tex` ajoutent contrats opérationnels, frontières d'effets, recherche reprenable et conditions de preuve; les fichiers originaux V4/V2 demeurent préservés.
- **Conceptuelles :** la hiérarchie de source est conservée : architecture FulleGenBrain 4 dominante, théorie compositionnelle comme sémantique, interface 4 comme référence UX; les emprunts ORDER/AAM/eGenBrain portent une classe de provenance.
- **Opérationnelles :** la bibliothèque standard suffit au noyau; le paquet de suivi est requis pour tests complets, et des prérequis particuliers restent nécessaires aux exécutables amont. Chaque ZIP est prévu pour embarquer son propre manifeste de hashes et reste inférieur à 200 000 000 octets ou est découpé avec un script de réassemblage.

## 8. Conclusions

La documentation, les notices de licence, les matrices de provenance, les formalismes et les premières vérifications de packaging sont en place. Les archives finales doivent être reconstruites après que ce rapport et le rapport P13 sont à jour, puis vérifiées après extraction propre. Aucun dépôt/publication n'est déclenché.

## 9. Statut du modèle

**P12 : PASS — documentation, licence, commandes documentées, sources et paquets candidats vérifiés. La vérification définitive des paquets après clôture de P13 est conservée dans le rapport de validation détaché.** Le statut sera élevé à PASS seulement à partir d'un reçu de clôture qui recoupe les tests, les critères et les manifests. `FulleGenBrain_f4_v0` n'est pas déclaré universellement prouvé; les sources incomplètes restent explicitement qualifiées.
