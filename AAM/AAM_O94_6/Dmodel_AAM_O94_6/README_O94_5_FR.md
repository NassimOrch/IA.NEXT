# AAM O94.5 — observation outillée, compilation compositionnelle et orchestration causale

**Version : 0.94.5 — 20 octobre 2026**

O94.5 corrige des défauts fonctionnels identifiés dans O94.4 et ajoute des contrats vérifiables dans cinq domaines : chargement de bundles de modèles, observation multimodale locale, compilation de programmes composés, feedback causal et unification du runtime conversationnel.

## Validation mesurée

La suite automatisée complète a terminé avec **419 tests réussis, 0 échec, 5 avertissements et 21 sous-tests réussis en 199,38 s**, sous Xvfb. Le reçu machine est `receipts/O94_5/P6_full_suite_regression_20261020T114952Z_19680.json`; le journal lié par SHA-256 est `logs/O94_5/P6_full_suite_regression_20261020T114952Z_19680.log`. Les reçus ciblés sont détaillés dans `O94_5_TEST_MATRIX.json` et `registre_prouves_O94_5.json`.

Cette campagne confirme les contrats et scénarios locaux couverts. Elle **ne certifie pas** l’inférence avec les poids SmolLM2 de l’utilisateur : les poids/config/tokenizer n'étaient pas présents dans les archives livrées et le runtime Transformers n'était pas installable dans cette session, dont l’accès à l’index de paquets échouait. La capacité locale native est implémentée et testée par contrat/dispatch, mais la génération sur les vrais poids doit encore être qualifiée dans l'environnement qui les contient. Voir `checklist_erreurs_no_model_O94_5.json`.

## Démarrage

Prérequis pratique : Python 3.11 ou version compatible avec les dépendances du paquet; Tk/Tcl est requis pour la fenêtre graphique. Après extraction intégrale :

```bash
python scripts/preflight_o945.py
python -m aam_o93 status
python -m aam_o93 ui
```

Lanceurs de confort inclus : `run_AAM_O94_5.sh`, `run_AAM_O94_5.bat` et `run_AAM_O94_5.ps1`. Le guide détaillé CLI/GUI est `GUIDE_UTILISATEUR_O94_5.md`.

## Principales voies opérationnelles

- **Observation** : `observe_media` appelle les outils présents (Tesseract, Poppler, FFprobe/FFmpeg, parsing DOCX standard); image/PDF scanné et audio/vidéo sont couverts par de vrais tests d'outils locaux. Le rapport conserve les hashes et le statut de chaque étape; une commande réussie ne vaut pas preuve de compréhension.
- **Modèles externes** : Transformers local avec bundle Hugging Face, backend TorchScript, Ollama, endpoint compatible OpenAI lorsque explicitement autorisé, et adaptateurs Python/PyTorch enregistrés avec politique et empreinte de code. Un fichier de poids seul n'identifie pas une architecture : config, tokenizer et clés doivent correspondre. Aucun fallback silencieux vers un autre générateur n’est permis.
- **Composition/compilation** : DSL JSON versionné, validation stricte, catalogue de composants, émission de source Python déterministe, compilation CPython/bytecode, manifeste d'intégrité puis exécution autorisée et bornée. L'atelier contient un éditeur multi-onglets, sauvegarde atomique, détection de conflit, diagnostics de compilation de projet et action LaTeX réelle.
- **Récompense/punition** : préférence utilisateur, fiabilité d'exécution et résultat vérifié sont des dimensions distinctes; mises à jour causales bornées, idempotentes et non concluantes non pénalisées automatiquement.
- **Chat intégré** : requête, pièce jointe, RAG, modèle sélectionné, compétence, mémoire, composition et feedback se rejoignent dans la même chaîne de runtime. Le chat n’annonce pas une vérification qui n’a pas été exécutée.

## Politique de preuve

Le statut `PASS_BOUNDED` signifie que le scénario a fonctionné dans son périmètre explicite; il ne signifie ni généralité universelle ni entraînement réussi sur n'importe quel modèle. Les cas non testés et les limites sont inscrits dans le rapport et les registres au lieu d'être convertis en succès implicite.

## P7 — documentation et restauration

Le paquet contient `scripts/preflight_o945.py` (gate spécifique à la version), `scripts/restore_o945_savepoint.py` et l’audit croisé `scripts/audit_o945_documentation.py`. La validation P7 a exécuté 14 contrôles sans échec, dont 6 tests dédiés, la compilation effective des deux sources LaTeX et une vérification de référence à zéro anomalie. Reçu : `receipts/O94_5/P7_documentation_restore_final.json`.
