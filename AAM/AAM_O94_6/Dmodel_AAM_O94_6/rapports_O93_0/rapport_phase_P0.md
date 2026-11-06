# Rapport de phase P0 — audit du corpus et définition de preuve

**Statut :** `IN_PROGRESS` jusqu'à la fin du test de fondation et de non-régression. Ce rapport ne certifie aucune fonctionnalité O93_0 comme complète.

## 1. Description

P0 a pour but d'établir la provenance du corpus, de construire les documents normatifs O93_0, de distinguer ce qui vient du modèle O93 hérité de ce qui est réellement démontré pour O93_0, et de mettre en place les gates et le registre avant toute modification fonctionnelle.

## 2. Architecture

Les entrées normatives prioritaires sont `DDD_Base_theorie_des_empreintes_complete_order_5.tex` et ses compléments de `theorie_emp/`, puis les spécifications et historiques O93/O92_0. Le code récent O93 est conservé dans `aam_o93/`; les composants O92 restent disponibles sous `aam_o92/`. Le runtime cible doit réunir observateur, moteur de sondes, empreintes, RAG multi-espace, compétences, mémoire causale, autonomie, interface, dataset et contrôle d'accès sous des contrats communs.

La théorie des empreintes impose notamment que l'identité observable soit relative à un contexte et à une famille/échelle de sondes; les sondes équivalentes n'ajoutent pas de nouvelles fibres; le raffinement des sondes affine les classes d'indiscernabilité; une égalité d'empreinte n'établit pas l'égalité brute des objets. Ces propriétés sont incorporées au formalisme cible mais ne sont pas toutes implémentées dans O93_0.

## 3. Pipeline exécuté

1. SHA-256 de l'archive originale et inventaire récursif des fichiers et ZIP intégrés.
2. Lecture des sources prioritaires et indexation AST du code O93/O92/tests.
3. Traitement exhaustif des membres du corpus : décodage/structure des textes, validation JSON/JSONL/CSV, extraction texte PDF, lecture des métadonnées PNG/WAV, empreinte des fichiers binaires.
4. Construction de `laboratoire_O93_0.tex` puis `formalisme_O93_0.tex`, compilation PDF et contrôle visuel des rendus.
5. Création de `checklist_de_travail_O93_0.json`, des registres d'erreurs, du préflight et du registre de 48 groupes d'exigences.
6. Préflight avant tests. Les tests de phase et la checklist doivent être mis à jour après leur résultat.

## 4. Commandes d'exécution

```bash
python scripts/preflight_O93_0.py --operation 'P0-audit-every-archive-member' --output logs/O930_P0_preflight_full_archive.json
python scripts/audit_entire_archive.py
python -m unittest discover -s tests -v
```

La première exécution de l'audit a échoué lors de la synthèse, car le code supposait à tort un champ `kind` pour chaque entrée. L'erreur a été enregistrée dans `checklist_erreurs_no_model.json`; le script a été corrigé et l'audit a été relancé avec succès.

## 5. Résultats

Source : `sources_AAM_17.zip`, SHA-256 `add72728952cd4ec83b6994a02d28022339fbbed29835d40c01b8f26bca60c38`, taille 39 758 574 octets.

`source_corpus_audit.json` indique : 1 620 entrées inventoriées, 1 616 fichiers traités, 4 dossiers, toutes les empreintes des membres concordent, zéro erreur de lecture de membre; 224 TeX structurellement analysés; 164 modules Python parsés par AST avec 1 924 symboles; 712 fichiers JSON; 31 JSONL; 18 PDF et 422 pages textuellement extraits; 36 PNG décodés pour métadonnées; 28 WAV lus pour métadonnées; 3 CSV analysés. Quatre fichiers portant l'extension `.json` sont vides; ils ne sont pas interprétés comme des preuves. Le Parquet `dataset/0000.parquet` est haché et conservé, mais son schéma n'a pas été décodé faute de `pyarrow`/`duckdb` dans cet environnement.

Le SHA-256 de l'archive, les hachages de membres, les résumés de source, les rendus TeX et les préflights sont conservés dans les fichiers de preuve correspondants.

## 6. Interprétation des résultats

L'inventaire et l'audit d'intégrité du corpus sont reproductibles dans cet environnement. La lecture structurelle exhaustive permet de tracer les sources de texte et de code, mais n'équivaut pas à l'interprétation humaine de chaque octet binaire. Une extraction de texte PDF ne prouve pas la fidélité de mise en page; les métadonnées d'image/audio ne valent pas compréhension sémantique multimodale.

L'analyse O93 trouve une base de sondes avec miroirs/compositions et recherche adaptative bornée, un runtime commun, une mémoire événementielle et une boucle autonome hérités. Les principaux écarts envers O93_0 demeurent : absence du RAG final itoken/vtoken multi-espace pondéré, autonomie qui ne démarre pas sur toute initialisation runtime, interface limitée aux cinq onglets hérités, et couverture de décodage multimodal dépendante des lecteurs.

## 7. Conséquences

- **Théoriques :** le formalisme O93_0 garde la relativité contextuelle de l'empreinte, la distinction entre observation brute et représentation, les échelles de sondes, les collisions observationnelles et l'exigence de preuves de généralisation hors sondes.
- **Conceptuelles :** recherche lexicale et RAG fondé sur des espaces sémantiques sont deux mécanismes distincts; « compétence présente » et « compétence validée » sont des statuts distincts.
- **Opérationnelles :** aucune phase fonctionnelle ne peut être déclarée complète sur la seule présence du code hérité; toutes les capacités restent traçables vers un test et une preuve précise.

## 8. Erreurs et limites

Le premier run d'audit a eu une erreur de code de synthèse, enregistrée et corrigée. Quatre anciens fichiers JSON sont vides; cela est documenté et n'est pas assimilé à un résultat vide de test valide. Le lecteur Parquet n'est pas installé; le contenu sémantique du Parquet n'est pas revendiqué comme lu. Les capteurs physiques, caméra, Windows natif, ACL/NTFS, crash/rollback et fournisseur Internet réel restent `NOT_RUN` dans cet environnement.

## 9. Conclusion

Les artefacts de spécification, l'inventaire et les registres de phase sont prêts. Après ajustement du seul test historique P9, la suite finale est à 105/105 tests réussis. Les sept gates P0 sont PASS et P0 est COMPLETE. P1 vient de passer à IN_PROGRESS; aucune phase n'a été sautée.

## 10. Statut du modèle

**O93_0 : phase P0 complète; phase P1 en cours.** Aucune conclusion anticipée de réussite ou d'échec n'est portée sur les capacités futures du modèle. Les fonctions héritées sont décrites comme héritées; les nouvelles fonctions non vérifiées restent ouvertes ou non implémentées selon `registre_prouves.json`.


## 11. Retest final

Commande : `python -m unittest discover -s tests -v` après le préflight `logs/O930_P0_preflight_tests_retry.json`. Résultat final : 105 tests, 105 réussis, 0 échec, code retour 0. Le premier run à 104/105 et le décalage historique de phase sont conservés dans l’historique et le registre d’erreurs; la correction a ajusté uniquement le test en lecture seule.
