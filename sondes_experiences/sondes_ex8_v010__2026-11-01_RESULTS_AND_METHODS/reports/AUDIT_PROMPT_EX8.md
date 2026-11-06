# Audit de conformité au prompt EX8 — v010

## Autorité méthodologique

Le prompt EX8 v1.0 est conservé à la racine de version (`prompt_ex8.json`) ainsi que dans `inputs/`. Son empreinte de la copie active est `e99b4dd8aedd4f0886dae375c23556762a8762dd2b77f16da28c339ec7258802`. La source texte générale est archivée comme provenance. Le pré-enregistrement A/B est dans `configs/PRE_REGISTRATION_V010_AB.md` ; la piste 5 a un addendum enregistré avant B10/B11 dans `configs/ADDENDUM_PRE_REGISTRATION_ACTION_LANGUAGE_B10_B11.md`.

## Conformité opérationnelle

Le développement Wisconsin utilise cinq graines fixes `[1501, 1607, 1717, 2029, 3037]`, le train de 341 lignes et la validation de 85 lignes. Toutes les candidates et MLP ont le même ordre des étiquettes de validation. Chaque candidate a un MLP de taille appariée et un MLP au moins quatre fois plus grand en paramètres totaux. Les sélections de checkpoints utilisent la validation uniquement ; les seuils, OOF et initialisations apprenables sont déterminés depuis le train.

Le loader Wisconsin n’accède qu’à `Xtr/ytr/Xva/yva` et au scaler ; il n’indexe pas les clés `Xad/yad`. L’adaptation n’a pas été chargée dans v010 ; aucun tableau test n’est présent dans le NPZ de développement. Ce statut concerne les valeurs, non les noms de clés inventoriés.

Les sorties brutes, prédictions, historiques, checkpoints, configurations et identifiants de run sont persistés. Les écritures de run utilisent des sorties atomiques et le statut est consolidé depuis tous les fichiers, non depuis le dernier lot de calcul.

## Écarts / limites au prompt

1. Les FLOPs/MAC complets, énergie et RSS processus complet ne sont pas mesurés. Le nombre de centres RBF/exp évalués et les latences sont des mesures de structure et de temps, pas un profil FLOP complet.
2. Le test de confirmation est fermé. SMS est une seconde réplication de domaine historiquement exposée (EX5/V007/V009), pas un holdout vierge.
3. L’initialisation K-means de certaines couches supérieures voit la matrice de features train complète sans étiquette, même quand les sorties supervisées sont OOF. Cela rend l’OOF transductif côté initialisation non supervisée ; ce n’est pas une fuite de labels, mais ce n’est pas du cross-fit strict de tous les prétraitements.
4. Les ablations avancées de robustesse des seuils et de cardinalité du codebook B10 ne sont pas exécutées. B10/B11 est un premier test contrôlé, non une validation complète du langage d’actions.

Le tableau ligne par ligne est `deliverables/CONFORMITY_MATRIX_V010.csv`. Les états incomplets ou non mesurés ne sont pas requalifiés en succès global.
