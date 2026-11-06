# ORDER72 e2 — Runtime boundary

Le runtime de cette expérience contient uniquement le micro-modèle d'inférence trajectory-link et les WM O72 nécessaires à la recherche.

Entrée du micro-modèle :
- `problem_fp`
- `candidate_trajectory_fps`
- `candidate_choice_fps`

Sortie : index/probabilités des candidats.

Il n'existe pas d'argument `solution_fp` dans l'API runtime. Le checkpoint d'inférence ne contient pas l'encodeur de solution `e_S`. Le dataset brut, le chemin de solution de référence et le checkpoint complet d'entraînement sont conservés uniquement dans l'archive d'audit.

Le chemin CERTIFY n'appelle pas l'intuition trajectory-link. Le guide n'est donc pas un vérificateur.
