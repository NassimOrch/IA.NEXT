# Rapport final EX7 — version V002

## Résumé exécutif

EX7 visait à transformer la compacité des sondes Emplica/Orchestra OOF en véritable gain de vitesse et de ressources. Le travail couvre la lignée micro-MIXA → OOF → correcteur, plusieurs variantes de correcteurs, de folds, de capacité, et l'architecture originale Emplica Orchestra Org récursive.

**Conclusion : l'objectif scientifique global n'est pas atteint à ce stade.** Les ratios de paramètres ≥4 sont conservés dans les comparaisons présentées, mais les coûts de cross-fitting OOF et d'entraînement des sondes restent beaucoup plus élevés que les fits MLP. Le parallélisme CPU essayé n'accélère pas la campagne. Des résultats de log-loss intéressants existent pour certains correcteurs Emplica structurels, mais aucun ne cumule de façon robuste non-infériorité predictive et accélération du pipeline complet.

## Ce qui est exécuté

- Correcteurs de référence/légers/décrits : 50/50 ; distillation et base seule : 20/20.
- Cross-fitting 2-fold et 5-fold : 10/10 chacun ; la référence est 3-fold. Le 2-fold accélère le pipeline mais la non-infériorité n'est pas démontrée ; le 5-fold détériore la log-loss.
- Variantes structurelles de correcteurs : 60/60.
- Orchestra Org récursive originale : 5/5 modèles racine, 15/15 fits de folds OOF, 15 correcteurs, 10 correcteurs d'étages, 30 ablations, cinq contrôles indépendants, 25 variantes de capacité et 60 variantes structurelles.
- `centers_k4` : 5/5 graines ; réduction de paramètres, mais log-loss et temps moins bons que le MLP apparié.
- Parité vectorisée max 4.77e-7, export TorchScript exact ; accélération TorchScript seulement par rapport à eager, pas par rapport au MLP.

## Indicateurs saillants

- Référence historique EX6 : Emplica OOF 8 295 paramètres, accuracy 98.59 %, log-loss 0.03637 ; Orchestra OOF 8 512 paramètres, accuracy 98.12 %, log-loss 0.03982.
- Orchestra Org récursive RBF-Lite OOF : environ 6 800 paramètres, accuracy 97.88 %, log-loss 0.05535 ; pipeline OOF moyen reconstruit ≈21.99 s face à ≈0.40 s pour le MLP-ge4x apparié.
- `centers_k4` : 5 732 paramètres, accuracy 97.65 %, log-loss 0.07208 ; MLP apparié 27 221 paramètres, 98.59 %, 0.04791 ; fit 6.48 s vs 0.401 s.
- Emplica OOF structurel réduit `rbf_d1_k4` : log-loss 0.03884 vs MLP 0.04675, mais accuracy 98.35 % vs 98.82 % et pipeline ≈44.4× plus lent.
- Processus OOF parallèles : 27.34 s vs 16.11 s séquentiel ; échec du parallélisme CPU naïf dans cet environnement.

## Limites déterminantes

- Wisconsin historique seulement, développement ; aucune validation externe indépendante.
- GPU/CUDA et ONNX indisponibles ; `torch.compile` non exécuté.
- Énergie, DRAM, mémoire d'activation et peak RSS non mesurés de façon fiable.
- FLOPs incomplets ; appels d'opérateurs donnés seulement comme proxy partiel.
- Aucun argument de supériorité populationnelle à partir de cinq graines sur un split unique.

## Verdict

**DÉVELOPPEMENT UNIQUEMENT — VALIDATION EXTERNE NON ÉTABLIE — SUCCÈS GLOBAL EX7 NON DÉMONTRÉ.**

Pour le détail, lire `CONFORMITE_PROMPT_EX7_V002.md`, `AUDIT_RECURSIVE_ORG_V002.md` et `COMPARATEURS_MLP_VARIANTES_EX7_V002.md`.
