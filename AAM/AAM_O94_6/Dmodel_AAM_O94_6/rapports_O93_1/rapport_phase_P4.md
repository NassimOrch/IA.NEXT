# Rapport de phase P4 — Paquet, audit et guide AAM O93_1

**Version :** O93_1 / runtime 0.93.1  
**Statut :** `COMPLETE_LOCAL_TESTED_BOUNDED`  
**Périmètre :** packaging local, audit de traçabilité, guide et vérifications d’extraction.

## 1. Description

P4 livre trois archives versionnées : modèle autonome, audit du code/tests/preuves et suivi de phase. Les sources normatives O93_0 sont conservées comme référence historique; les corrections incrémentales et leurs preuves sont identifiées O93_1.

## 2. Architecture

Le paquet modèle inclut le runtime, tests, sources de référence, datasets et journaux. L’audit est une copie de ce même contenu avec une note d’audit dédiée et un manifeste indépendant. Le suivi contient les checklists, les deux registres d’erreurs synchronisés, les formalismes, le laboratoire, le guide, les rapports et les reçus. Les hashes finaux des trois ZIP sont dans le manifeste détaché pour éviter la circularité.

## 3. Pipeline complet

Consultation des formalismes/checklists/ledgers → préflight → guide et notes de version → registre `registre_prouves_O93_1.json` → compilation source TeX → prévalidation d’emballage → génération SHA-256 sans auto-hash → ZIP → CRC → extraction propre → manifeste → smoke CLI → matrice de tests → synchronisation des statuts → reconstruction de release → vérification exacte finale. Les tentatives échouées/interrompues restent conservées.

## 4. Commandes d’exécution

```bash
python scripts/o931_preflight.py --label p4_final_build_preflight
python scripts/o931_refresh_manifests.py --root . --package Dmodel_AAM_O93_1
python verify_manifest.py <répertoire_extrait>
python -m aam_o93 status
xvfb-run -a env PYTHONPATH=. TERM=xterm python -W error::SyntaxWarning -m pytest -q \
  tests/test_o931_chat_pipeline.py tests/test_o931_language_model_training_surface.py \
  tests/test_o931_ui_smoke.py tests/test_o931_ui_busy_catalog_refresh.py \
  tests/test_o931_autonomy_boot_lifecycle.py tests/test_o931_record_preserving_rag.py \
  tests/test_o931_sparse_proximity_optimization.py tests/test_o931_release_identity.py \
  tests/test_p8_security.py tests/test_p8_integration.py
```

## 5. Résultats

- Préflight O93_1 et contrôle de version/formalisme : `PASS_BOUNDED`.
- Régression sur la source pré-emballage : 49 tests passés en 14,34 s, code 0 (`logs/O931/p4_final_source_regression.json`).
- Candidate Dmodel du cycle précédent, extraite proprement : 49 tests passés en 12,58 s, code 0; manifeste avant/après tests PASS. Son SHA-256 est conservé dans `logs/O931/p4_candidate_builder_success_receipt.json`; ces métriques sont historiques et ne sont pas les hashes de la release reconstruite.
- Candidate Amodel du même cycle : une première exécution combinée a expiré; l’exécution séparée du même test a d’abord révélé un seul dépassement intermittent de la première pulsation autonome (fenêtre 8 s). Le test a ensuite réussi en isolé, dans le groupe complet (4/4), dans la suite complète (49/49) et lors de 10 répétitions sur workspaces neufs (10/10). L’incident reste suivi en statut `INTERMITTENT_RETEST_PASS_MONITORED` ; il n’est pas effacé ni présenté comme un correctif de code.
- Manifeste de l’archive Amodel précédente : 5 322 fichiers déclarés, zéro écart avant et après tests; CRC ZIP valide. Les totaux/tailles des anciennes candidates sont historiques. Les hashes, nombres d’entrées et reçus post-extraction de la release reconstruite sont externalisés dans `O93_1_delivery_manifest.json` et `preuves_livraison/validation_archives_finales.json` du paquet de suivi afin d’éviter un hash auto-référentiel.
- Le suivi contient 6 registres JSON parsables et les sources TeX O93_0/O93_1 compilées avec `pdflatex -halt-on-error`; aucun PDF n’a été inspecté visuellement.
- Acceptation SMS bornée : 120 lignes réelles, cible tenue hors entraînement retrouvée par RAG et présente dans le prompt; capsule entraînée réellement invoquée avec hash correspondant. La candidate générée a été rejetée et le chat a livré un extrait source cité de 340 caractères.
- Acceptation SMS complète : 5 574 lignes; plusieurs exécutions ont dépassé le budget supervisé, dont 420 s sans rapport final. Statut conservé `NOT_VALIDATED`.

- Régression supplémentaire sur l’arbre source final après synchronisation des documents : 49 tests passés en 14,34 s, code 0 (`logs/O931/p4_final_source_regression.json`).
- Smoke CLI dans un workspace temporaire isolé : `version=0.93.1`, `autonomy=RUNNING`, code 0 (`logs/O931/p4_final_cli_status.json`).
- Les tests de cycle de vie couvrent le démarrage automatique, requête utilisateur, arrêt/reprise manuels de la boucle autonome et fermeture explicite d’AAM.

## 6. Interprétation

La chaîne de récupération et l’invocation du générateur sont démontrées sur un sous-ensemble de données authentiques, pas sur l’ensemble du corpus. La provenance d’une génération n’est pas une garantie de qualité; dans le cas éprouvé, le texte candidat a été rejeté et l’extrait observé est clairement présenté comme repli. La campagne totale n’est pas convertie en PASS.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

**Théoriques :** preuve de provenance et qualité de réponse restent deux critères différents. **Conceptuelles :** l’acquisition d’une compétence et l’entraînement du générateur de chat sont distincts. **Opérationnelles :** le guide enseigne l’ingestion RAG, l’entraînement de la capsule du chat, la sélection explicite, les contrôles de provenance, l’autonomie et le dépannage. Les hashes permettent de détecter une altération après packaging.

## 8. Erreurs et limites

Les premiers essais de collecte de reçus TeX/manifeste et le premier validateur composite d’extraction ont révélé des erreurs de harnais; elles sont documentées et résolues après retests. Un test de cycle de vie de l’autonomie a échoué une fois en test groupé, puis est passé en isolé, en suite complète et 10/10 répétitions fraîches; l’occurrence initiale reste en surveillance, sans cause racine prouvée. Le corpus SMS complet reste `NOT_VALIDATED`. Les essais Windows/ACL, capteurs physiques, endpoints Internet/MCP/API externes et crash/rollback natifs ne sont pas réalisés dans cet environnement.

## 9. Conclusion et statut du modèle

P1–P4 sont `COMPLETE_LOCAL_TESTED_BOUNDED`; l’implémentation complète universelle n’est pas revendiquée (`implementation_complete_claimed=false`). Le statut `NOT_VALIDATED` du corpus complet et des acceptations externes est maintenu explicitement. Aucun résultat ne prédit le potentiel général d’AAM. Les hashes des archives de release et les résultats d’extraction exacts sont attachés dans le manifeste de livraison détaché et le paquet de suivi.
