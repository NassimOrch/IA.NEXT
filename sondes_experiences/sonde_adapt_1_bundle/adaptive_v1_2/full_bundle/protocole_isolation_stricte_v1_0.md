# Addendum de protocole — réplication à séparation de processus v1.0

Date de gel prévu : 2026-10-28 (UTC/heure du système enregistrée dans le manifeste d'exécution).

## Objet
Cette réplication renforce les contrôles anti-fuite des expériences déjà décrites dans `protocole_preregistere.md`, `protocole_preregistere_composition_v1_2.md` et `protocole_supplement_digits_v1_0_1.md`. Elle ne remplace ni ne réécrit ces expériences : elle ajoute une exécution séparée sous identités Unix distinctes.

## Rôles et frontières
- `ngb_cls` : entraîne les quatre méthodes de classification à partir d'un seul fichier contenant les partitions train/validation autorisées. Ne doit pas pouvoir lire les fichiers d'entrée de test, le coffre de labels, ni le code-oracle `src/run_experiment.py`.
- `ngb_imit` : entraîne une sonde à partir d'un seul fichier opaque d'observations entrée-sortie du neurone cible. Ne reçoit ni l'identité/famille/graine cible, ni paramètres/formule, ni entrées ou sorties de test.
- `ngb_teacher` : entraîne un petit MLP enseignant sur train seulement et observe ses activations uniquement sur train.
- `ngb_comp` : entraîne une sonde de composant à partir des seules entrées train et activations train observées pour un neurone.
- `www-data` : inférence uniquement ; lit les entrées de test et les modèles gelés, mais pas le coffre de labels de référence.
- `root` : préparation des données/références, contrôle des permissions et calcul des métriques après production des prédictions.

Les répertoires de rôles sont configurés en `0700`, les fichiers en `0600`; les sources d'oracle sont temporairement protégées en retirant le droit d'accès aux utilisateurs non privilégiés pendant les appels d'entraînement. L'accès effectif est vérifié en lançant `test -r` sous chaque identité. Il s'agit d'un bac à sable local basé sur les permissions Unix, pas d'une preuve formelle contre un administrateur, un noyau compromis, les canaux auxiliaires ou tout défaut du système.

## Conditions confirmatoires
1. Classification : trois tâches synthétiques (`two_moons`, `circles`, `xor_product`) et le benchmark public `breast_cancer`, graines 714/825/936, même split que la réplication de référence (split seed = seed + 100), prétraitement ajusté sur train. Méthodes A sonde RBF adaptative, B règle d'adaptation méta-apprise, sonde RBF fixe, MLP. Évaluation par le processus d'inférence sans labels, puis scoring privilégié.
2. Imitation boîte noire : neuf neurones scalaires cachés, trois familles (ReLU, tanh, sigmoid), trois budgets (64, 256, 1024 observations), trois graines d'initialisation de sonde (111, 222, 333), 4000 entrées de test par cible. Chaque entraîneur reçoit seulement les observations d'apprentissage dans un fichier doté d'un jeton opaque.
3. Composition : `two_moons` et `breast_cancer`, graines 411/522/633, un MLP enseignant à 16 unités cachées, 16 sondes entraînées séparément sur les activations d'entraînement observées, remplacement de 1, 4 ou 16 unités. Les paramètres du readout enseignant restent conservés ; cette expérience mesure le remplacement local, pas un modèle autonome.

## Gel et reprise
Les scripts suivants sont gelés avant exécution de cet addendum :
- `src/strict_models.py`
- `src/strict_learner_worker.py`
- `src/run_strict_isolated_replication.py`
Leurs SHA-256 doivent être consignés dans `audit/strict_isolation_preexecution_hashes.json`. Toute modification après le gel exige un incrément de version et un nouvel enregistrement d'empreintes avant l'exécution affectée.

## Critères d'intégrité
- Les rôles d'apprentissage peuvent lire leurs fichiers d'entraînement et ne peuvent lire ni les entrées de test, ni le coffre de labels, ni le code-oracle.
- L'identité d'inférence peut lire entrées de test et modèles gelés, mais pas les labels de test.
- Les références restent root-only jusqu'à la fin de l'inférence.
- Les données des partitions et les permissions sont journalisées ; les prédictions et résultats sont conservés sans sélectionner seulement les résultats favorables.
- Les écarts de réplication sont enregistrés ; les résultats antérieurs ne sont pas silencieusement remplacés.

## Limites interprétatives préétablies
Même si les contrôles passent, les conclusions restent limitées à la fidélité observée sur ces fonctions, tâches, budgets et distributions. Les sondes RBF peuvent avoir davantage de paramètres que le neurone cible. La substitution dans le réseau garde le readout enseignant et n'établit donc pas l'autonomie de la composition. Une erreur faible sur échantillon ne prouve pas une équivalence fonctionnelle universelle.
