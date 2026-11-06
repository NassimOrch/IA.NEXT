# Protocole préenregistré — NG-ADAPT-2026-10-29-v1

**Horodatage / gel logique :** avant les exécutions principales A–J à 90 epochs. Les sorties smoke test à 8 epochs sont conservées en journal, mais explicitement exclues des résultats scientifiques.

## Hypothèses/questions

H1 — Le réseau de probes locales B atteint une performance comparable au MLP A dans les tâches étudiées, avec des compromis de calibration/coût.

H2 — Le coordinateur C peut modifier la perte de test au-delà de B; on ne suppose pas que son effet est positif. Une ablation gelée doit reproduire B sous mêmes seeds/shards.

H3 — L'activation de sortie `tanh` (D/E) a un effet isolable par comparaison D–B, E–C, et interaction `(E-C)-(D-B)`.

H4 — Une boucle en ligne après révélation de l'observation (F–J) peut améliorer ou dégrader les performances, en fonction de la qualité du flux.

H5 — La composition `x -> f(x) -> g(f(x)) ≈ x` sera comparée à identité, RBF non entraîné, deux sondes apprises, trois sondes, bottleneck latent 1 et autoencodeurs MLP latents 1/2.

## Jeux de données

| Tâche | Définition |
|---|---|
| two_moons | `make_moons(n=1800, noise=0.22, random_state=20261121)` |
| circles | `make_circles(n=1800, factor=0.48, noise=0.16, random_state=20261122)` |
| xor_product | Uniforme `[-2,2]^2`, cible `1[x0*x1>0]`, 4% labels bruités, seed `20261123` |
| wine_binary | sklearn Wine, classe 0 contre classes 1/2; aucune interprétation médicale |
| digits_3_vs_8 | sklearn Digits 8×8, sous-ensemble binaire 3 vs 8, pixels divisés par 16 |

Les doublons exacts de caractéristiques avec même label sont supprimés avant split avec un registre explicite; les conflits éventuels sont signalés. Normalisation avec `StandardScaler` ajusté uniquement sur la partition train. Split stratifié fixe 60/15/10/15 train/validation/adaptation/test. Il y a un seul split par tâche. Seeds de modèles : 1501, 1607, 1717.

## Architectures

- A : MLP 1 couche cachée tanh, 16 neurones.
- B : quatre sondes RBF locales, sans paramètre global.
- C : B + `phi` global de quatre logits softmax et adaptation locale conditionnée par les poids.
- D : B + `tanh` appliqué aux sorties de sonde.
- E : C + cette activation.
- F–J : même ordre A–E avec flux d'adaptation observé après prédiction, fingerprint, mise à jour en ligne.
- K : contrôle RBF à centres/largeurs fixes (17 paramètres dans les tâches observées); contrôle de capacité, non égal en paramètres.

L'optimiseur est Adam, `BASE_LR=0.015` pour la classification, weight decay `1e-4`, 90 epochs. Pour C/E, `GLOBAL_LR=0.05` et synchronisation globale toutes les cinq epochs. Les détails déterminants sont dans `code/probe_lab.py`.

## Métriques

Primaires : accuracy et log-loss. Secondaires : précision, rappel, F1, ROC-AUC, PR-AUC, Brier, ECE à 10 bins, confusion matrix, durée de train, durée d'adaptation, latence d'inférence, paramètres entraînables/partagés, pas locaux/globaux et volume théorique de messages flottants. Les métriques sont calculées sur les prédictions d'un test réservé, après la seule adaptation sur la partition adaptation.

## Conditions de boucle préspécifiées

Test de résistance ciblé sur `two_moons`, A–E, trois seeds : sans boucle, boucle complète, boucle avec updates désactivés, 30% observations/labels manquants, 20% de labels inversés, 50% de labels trompeurs et flux avec décalage covariable (offset `x0 + 0.75`). Le seuil de fingerprint est le quantile 95% du résidu absolu sur validation propre.

## Reconstruction

`x -> f_theta(x) -> g_psi(f_theta(x))`, sans connexion de saut et sans passage du x original au second module. `make_moons(2400, noise=.22, seed=20261131)`, même principe de split; 300 epochs, Adam LR .01. Comparateurs : identité directe; RBF non entraîné; composition RBF 2 maps libre; variante locale (f apprise puis gelée, g appris); activation tanh; 3 maps; bottleneck RBF latent 1; autoencodeur MLP latent 1/2. Evaluations : test source, auto-reconstruction sous bruit, reconstruction vers le parent propre, décalage de test +0.75. Les cibles de la tâche de base sont X même, donc le baseline identité est exactement nul; c'est intentionnel et constitue un test anti-trivialité, pas une « victoire » apprise.

### Amendement transparent d'implémentation

Le préenregistrement nommait l'état d'optimiseur mais ne spécifiait pas explicitement le sort des moments Adam à la frontière entre pré-entraînement et boucle de reconstruction. Le code a choisi et déclare explicitement **un nouvel état Adam au début de la boucle**; l'optimiseur de pré-entraînement n'est pas silencieusement réutilisé. Les premières sorties de développement ont été recalculées après correction du comptage des paramètres (total stocké/mis à jour vs `requires_grad` après gel du premier module); la livraison finale contient le comptage corrigé. Ces détails sont enregistrés dans `reconstruction_config.json` et le code.

## Politique statistique et limites

Les différences sont appariées par seed parce que tâches/splits sont constants. Moyennes, SD et IC t à 95% sont descriptifs : trois seeds d'optimisation sur une partition fixe ne permettent pas une inférence fiable sur la variabilité des données. Aucune p-value confirmatoire n'est utilisée, donc aucune correction de multiplicité de p-values n'est revendiquée. Pas de critères d'arrêt basés sur le test. Les échecs de lancement, les logs smoke, les tentatives interrompues et les reprises par tâche sont conservés.
