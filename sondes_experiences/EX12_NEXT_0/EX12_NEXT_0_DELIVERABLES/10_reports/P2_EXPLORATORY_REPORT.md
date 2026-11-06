# EX12 P2 — rapport de criblage exploratoire

**Intégrité : PASS** — 80/80 configurations logiques réussies, 6 interruptions conservées; le registre du premier runner conserve ses 80 tentatives échouées dues à `yva` absent.

## Protocole
Deux graines pilote pré-enregistrées, quatre fonctions, 630 train et 135 validation par cellule. Données nouvellement générées avec flux RNG EX12. Aucun test, holdout ou extrapolation n’a été généré ou chargé. P2 est un criblage exploratoire de deux graines, pas une confirmation. Matching du total persistant à ±1 % par rapport au MLP correspondant.

| Tâche | Variante | NMAE candidat | NMAE MLP | Δ NMAE | Wins / 2 | Temps fit / MLP | Temps run / MLP |
|---|---:|---:|---:|---:|---:|---:|---:|
| f1_sin | R0 | 0.00499 | 0.00540 | -0.00041 | 1/2 | 0.95× | 0.59× |
| f1_sin | C1 | 0.02151 | 0.00540 | +0.01611 | 0/2 | 1.69× | 1.28× |
| f1_sin | C2 | 0.00593 | 0.00540 | +0.00053 | 0/2 | 1.51× | 0.73× |
| f1_sin | C3 | 0.00685 | 0.00540 | +0.00145 | 0/2 | 1.45× | 0.83× |
| f1_sin | C4 | 0.00889 | 0.00750 | +0.00139 | 1/2 | 1.90× | 1.38× |
| f1_sin | G1 | 0.00595 | 0.00436 | +0.00160 | 0/2 | 7.06× | 5.10× |
| f1_sin | G2 | 0.00840 | 0.00436 | +0.00404 | 0/2 | 8.34× | 5.29× |
| f2_mul | R0 | 0.01085 | 0.01063 | +0.00021 | 1/2 | 1.64× | 1.69× |
| f2_mul | C1 | 0.37428 | 0.01063 | +0.36365 | 0/2 | 1.03× | 0.99× |
| f2_mul | C2 | 0.01120 | 0.01063 | +0.00057 | 1/2 | 1.51× | 1.50× |
| f2_mul | C3 | 0.01380 | 0.01063 | +0.00317 | 0/2 | 1.90× | 2.64× |
| f2_mul | C4 | 0.01611 | 0.01292 | +0.00320 | 0/2 | 1.38× | 1.41× |
| f2_mul | G1 | 0.21735 | 0.01063 | +0.20671 | 0/2 | 6.81× | 4.59× |
| f2_mul | G2 | 0.22252 | 0.01063 | +0.21189 | 0/2 | 4.72× | 3.61× |
| f3_square_plus | R0 | 0.01683 | 0.01144 | +0.00539 | 0/2 | 1.06× | 0.86× |
| f3_square_plus | C1 | 0.02098 | 0.01144 | +0.00954 | 0/2 | 1.51× | 1.38× |
| f3_square_plus | C2 | 0.01428 | 0.01144 | +0.00284 | 0/2 | 0.91× | 1.33× |
| f3_square_plus | C3 | 0.01618 | 0.01144 | +0.00474 | 0/2 | 1.39× | 1.11× |
| f3_square_plus | C4 | 0.00992 | 0.01184 | -0.00193 | 2/2 | 1.09× | 1.10× |
| f3_square_plus | G1 | 0.02330 | 0.01144 | +0.01186 | 0/2 | 6.98× | 7.10× |
| f3_square_plus | G2 | 0.02350 | 0.01144 | +0.01206 | 0/2 | 4.54× | 4.50× |
| f4_sin_product | R0 | 0.04997 | 0.09032 | -0.04035 | 2/2 | 1.49× | 2.29× |
| f4_sin_product | C1 | 0.14666 | 0.09032 | +0.05634 | 0/2 | 2.15× | 2.44× |
| f4_sin_product | C2 | 0.04789 | 0.09032 | -0.04243 | 2/2 | 1.62× | 1.63× |
| f4_sin_product | C3 | 0.07627 | 0.09032 | -0.01405 | 2/2 | 1.32× | 1.29× |
| f4_sin_product | C4 | 0.06051 | 0.08589 | -0.02537 | 2/2 | 1.74× | 1.77× |
| f4_sin_product | G1 | 0.22527 | 0.09620 | +0.12908 | 0/2 | 1.98× | 2.01× |
| f4_sin_product | G2 | 0.22010 | 0.09620 | +0.12391 | 0/2 | 1.88× | 1.90× |

## Interprétation
Les résultats sont hétérogènes. C1 (couverture globale seule) est fortement dégradée sur multiplication et moins bonne sur les quatre fonctions. G1/G2 sont généralement plus coûteuses et très dégradées sur plusieurs tâches; aucune valeur spécifique du graphe réel n’est établie dans ce criblage. R0 et C2 donnent les meilleurs signaux sur sinus/sinus-produit; C4 est favorable sur carré-plus et sinus-produit, mais aucun candidat ne domine partout. Les temps concernent optimisation et temps total d’entraînement/initialisation; aucune latence inference batchée ni mémoire peak n’est mesurée dans P2.
Aucune inférence statistique confirmatoire n’est faite avec deux graines. Les résultats par graine sont dans `P2_PAIRED_RESULTS_FULL.csv`. Les 80 métriques sont recalculées depuis les prédictions (MAE/RMSE tolérance 1e-10; NMAE 1e-8); hashes et séparation train/validation vérifiés; aucune donnée test.

## Décision P2
PASS pour le criblage exploratoire prévu. R0, C2, C3 et C4 restent admissibles à un pilote élargi; C1 et G1/G2 sont conservés comme contrôles/références, et ne sont pas promus. C5 et C6 restent différés, non implémentés. Aucune sélection définitive ni verdict de remplacement MLP.

## Artefacts principaux
- `00_governance/P2_RUN_REGISTRY.jsonl`: 80 premières tentatives échouées, conservées.
- `00_governance/P2_RUN_REGISTRY_RETRY1.jsonl`: 80 succès logiques et interruptions conservées.
- `09_analysis/P2/P2_FULL_INTEGRITY_AUDIT.json`: contrôle complet.
- `09_analysis/P2/P2_PAIRED_RESULTS_FULL.csv/.json`: toutes les paires.
- `09_analysis/P2/P2_RUN_SCRIPT_PROVENANCE.json`: scripts exacts par run.
- `04_code/p2_screen_v2.py`, `p2_screen_resume.py`, `ex12_models.py`, `generate_p2_data.py`.
