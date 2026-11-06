# NGeGenBrain v3_0 — work checkpoint

- Date : 2026-10-28
- Heure : session de finalisation, Africa/Algiers
- Objectif : livrer le réentraînement anglais, le modèle multi-facettes, le rapport LaTeX/PDF, l'audit et le suivi après validation propre des archives.
- Version : NGeGenBrain v3_0 / 3.0.0
- Environnement : Linux x86_64, Python 3.13.5, PyTorch 2.10.0+cpu; CUDA absent; `pdflatex` disponible.
- Racine exacte : `/mnt/data/ngv3_0_work/NGeGenBrain_v3_0`
- Modèle source V3 : `references/NG-Recomposed-TinyLM-v3/model` et entrée originale `model_produit_NG_v3.zip`.
- Modèle livré : `model_produit_NG_v3_0/model/model.pt`, 54 536 paramètres.
- Dataset anglais final : `research/english_dataset_v3_0_final2`, manifeste SHA-256 `d9919e0713bd33863dd08b30dd2b5d7974da6892e2bb2da2f6485877ca0b9281`.
- Résultats : NLL 1.853 nats/octet, PPL 6.379, top-1 48.16 %, routeur 62.5 % sur 16 documents; baseline V3 initiale et trigramme comparées sur le même holdout.
- Validation : suite logicielle 60/60 en arbre et extraction propre; chargement ZIP, chat CLI, health/load/chat Web validés. Les reçus exacts et les logs finaux sont dans `deliverables/verification/`.
- Rapport : `reports/rapport_experiences_NGeGenBrain_v3_0.tex` et PDF A4 9 pages vérifiées visuellement.
- Limites : corpus contrôlé et petit, génération longue faible, généralisation NLP non établie, reconstruction mécaniste d'un LLM externe non démontrée. Le BAT est validé statiquement seulement, non exécuté physiquement sous Windows.
- Clôture : les archives sont reconstruites depuis un manifeste fichier par fichier; les SHA-256 finaux sont dans `deliverables/checksums.sha256` et `deliverables/release_manifest_NGeGenBrain_v3_0.json`. Le manifeste de release externe évite toute auto-référence de hash.
