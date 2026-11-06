# Rapport de phase P9 — paquetage vérifiable

**Horodatage UTC :** 2026-10-14T11:28:59Z  
**Statut :** `COMPLETE_LOCAL_TESTED_BOUNDED`  
**Portée :** construction et validation locale bornée des archives; P10 reste distinct et non démarrée.

## Description

P9 transforme l’arbre testé en paquets portables accompagnés d’un audit de code, de tests, de registres et de reçus de validation. Le statut P9 ne signifie pas que la totalité des capacités est validée sur tout matériel/OS.

## Architecture

`Dmodel_AAM_O93_0.zip` contient le runtime, les ressources et l’archive source exacte; `Amodel_AAM_O93_0.zip` contient l’audit, les scripts/tests, les registres et preuves; `suivi_model_AAM_O93_0.zip` porte les reçus de release et l’état de reprise. Les manifestes SHA-256 sont non récursifs et partagent un même ensemble de chemins dans chaque paquet.

## Pipeline complet

1. Lecture préalable du formalisme, laboratoire, checklist de phase et deux registres d’erreurs.
2. Vérification du checkpoint P8 clôturé, absence d’erreurs P8/P9 ouvertes et identité SHA-256 de `sources_AAM_17.zip`.
3. Synchronisation des README, checklists, registre de preuve et statuts.
4. Rafraîchissement des manifestes; refus des liens symboliques, chemins non confinés et fichiers manquants/non répertoriés.
5. Création des archives, `ZipFile.testzip`, extraction dans des dossiers vierges, vérification des manifestes avant/après tests, smoke CLI et régression ciblée.
6. Enregistrement des SHA-256 définitifs et des reçus de chaque archive dans `suivi_model_AAM_O93_0.zip` et dans `O930_delivery_manifest.json` externe.

## Commandes de vérification

```bash
python scripts/verify_all_manifests.py .
python verify_manifest.py .
python -m aam_o93 status
python -m pytest -q -p no:cacheprovider tests/test_p8_action_router.py tests/test_p8_integration.py tests/test_p8_security.py tests/test_p9_preregistered_v2_integrity.py tests/test_p9_preflight_status_vocabulary.py
```

## Résultats et interprétation

L’exercice candidat précédant la synchronisation finale a passé le ZIP, l’extraction propre, les deux vérificateurs de manifestes, le smoke CLI et 46 tests ciblés (plus 5 sous-tests). Les trois archives finales sont soumises aux mêmes vérifications; leurs hashes absolus doivent être lus dans le reçu de livraison compagnon, calculé après construction. La provenance de la source doit conserver le SHA-256 `add72728952cd4ec83b6994a02d28022339fbbed29835d40c01b8f26bca60c38`.

Un succès de hash/extraction prouve l’intégrité et la complétude de l’ensemble des fichiers répertoriés dans les limites du manifeste; il ne prouve ni l’universalité de l’observation, ni la généralisation des compétences, ni l’acceptation externe.

## Conséquences

- **Théoriques :** les preuves de contenu sont des observations finies, dépendantes du protocole.
- **Conceptuelles :** une livraison reproductible est distincte d’une compétence universellement acquise.
- **Opérationnelles :** les trois paquets se vérifient indépendamment; les reçus externes évitent de placer le hash d’une archive dans l’archive elle-même.

## Erreurs, limites et état final

Les anciens défauts et incidents de tooling demeurent dans les registres historiques; les enregistrements résolus ont un retest référencé. P10 n’a pas démarré : le système d’exploitation natif Windows, les ACL/installateurs, les capteurs réels, les fournisseurs réseau/MCP/API réels et les tests physiques de coupure de courant ne sont pas disponibles dans ce laboratoire.

**Conclusion :** P9 est clôturée uniquement dans la portée `LOCAL_TESTED_BOUNDED`. `implementation_complete_claimed=false`; P10 reste `NOT_STARTED`. Aucune réussite ou échec futur n’est prédéterminé.
