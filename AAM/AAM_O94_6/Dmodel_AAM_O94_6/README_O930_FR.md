# AAM O93_0 — statut P9 vérifié localement

Cette remise comprend le modèle, le formalisme, le laboratoire, la checklist phasée, les registres d’erreurs, le registre de preuve, les données sources et les tests. `implementation_complete_claimed=false` : la clôture P9 ne signifie pas que toutes les exigences O93_0 ou l’acceptation externe P10 sont terminées.

## Commandes de contrôle

```bash
python -m aam_o93 status
python scripts/preflight_O93_0.py --operation p9-package-validation --output logs/P9_PREFLIGHT.json
python scripts/verify_all_manifests.py .
python verify_manifest.py .
python -m pytest -q -p no:cacheprovider tests/test_p8_action_router.py tests/test_p8_integration.py tests/test_p8_security.py tests/test_p9_preregistered_v2_integrity.py tests/test_p9_preflight_status_vocabulary.py
```

## Statut des phases

- P0 : source et provenance inspectées; SHA-256 de l’archive source contrôlé.
- P1–P7 : clôturées dans leur portée documentée, sans extension implicite à tout matériel ou format.
- P8 : `COMPLETE_LOCAL_TESTED_BOUNDED`; 30 modules/222 tests rapportés passent sur l’arbre de travail actuel.
- P9 : `COMPLETE_LOCAL_TESTED_BOUNDED`; contrôle de paquet, extraction propre, manifestes et retests décrits dans `logs/O930_P9_closure_result.json` et le paquet de suivi compagnon.
- P10 : `NOT_STARTED`; les tests natifs, dispositifs physiques et services distants restent un contrôle séparé.

## Règle de preuve

Les anciens échecs restent dans l’historique même lorsque corrigés. Un statut `RESOLVED_RETEST_PASS` demande un reçu de retest; un statut local borné ne vaut pas certification externe. Les compétences expérimentales ne sont pas promues par le seul fait que les manifestes passent.
