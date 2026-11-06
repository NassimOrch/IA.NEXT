# État de livraison AAM O94.5

- Release : O94.5 / 0.94.5
- Parent : O94.4 conservé comme point de référence immuable.
- P0–P6 : `COMPLETE_EVIDENCED`. P6 : 419 tests passés, 0 échec, 5 avertissements, 21 sous-tests.
- P7 : en cours dans cette version de fichier; documentation CLI/GUI, rapport, registre de preuves, matrice, lanceurs et restauration viennent d'être créés.
- P8 : pas encore clos tant que build des ZIP, extraction vierge, CRC, manifeste, préflight et tailles ne sont pas vérifiés.
- Qualification ouverte : génération sur les poids SmolLM2-360M réels de l’utilisateur (non fournis dans la session). Le contrat local Transformers est testé, mais pas l’inférence de ces poids.

Livrables prévus dans `/mnt/data`: `Dmodel_AAM_O94_5.zip`, `Amodel_AAM_O94_5.zip`, `suivi_model_AAM_O94_5.zip`, accompagnés de `formalisme_O94_5.tex`, `laboratoire_O94_5.tex`, `RAPPORT_TESTS_O94_5_FR.md`, `GUIDE_UTILISATEUR_O94_5.md` et de leur manifeste externe.


## P7 reconciliation (2026-10-20)

P7 is `COMPLETE_EVIDENCED`: both LaTeX sources compile; the restore verifier is read-only by default and checks the immutable parent plus O94.5 overlay; three P7 test files report 6 passed; the documentation audit reports 18 required documents, 10 proof entries, 7 targeted batteries and zero broken references. Evidence: `receipts/O94_5/P7_documentation_restore_final.json` and `receipts/O94_5/P7_post_registry_documentation_audit.json`. P8 is now `IN_PROGRESS`; the full release regression, package construction and fresh-extraction checks remain required before delivery closure.
