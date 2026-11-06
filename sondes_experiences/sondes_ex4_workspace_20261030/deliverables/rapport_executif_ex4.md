# Rapport exécutif EX4 — 30 octobre 2026

## Décision

**Résultat : progrès réel en compacité, mais objectif complet non atteint.** La meilleure piste mesurée dans la campagne v005/v006 est la sonde dynamique d8/k4. Elle utilise en moyenne 356 paramètres totaux lorsque le prétraitement commun est inclus, contre 1 448 pour son MLP-ge4x (ratio 4,067×). Son accuracy moyenne est égale à celle du MLP associé (97,65 %), mais sa log-loss reste supérieure (0,05952 contre 0,05394). Son temps de fit et sa latence médiane/p95 sont également supérieurs.

Aucune des 12 familles de sondes ne satisfait simultanément sur les cinq seeds les critères de paramètres ≥4×, accuracy non inférieure, log-loss non inférieure, temps de fit non supérieur et latence médiane non supérieure. **Nombre de familles avec réussite conjointe : 0/12.**

## Ce qui a été fait

- Inventaire et vérification d'intégrité des archives sources ; lecture complète du prompt EX3 et du fichier `debrit_0.txt`.
- Copie de `prompt_ex3.json` vers `prompt_ex4.json`, puis correction du contrat P_total, des contrôleurs, du comptage dynamique et du prétraitement partagé.
- Reconstruction du point de départ v009 et développement versionné v001–v006.
- Campagne Wisconsin de développement sur cinq graines : 60 entraînements de sondes, 135 MLP distincts, 120 comparaisons appariées (matched + ge4x).
- Correction v006 du comptage du `StandardScaler` partagé : 60 coefficients numériques (30 moyennes + 30 échelles) sont maintenant ajoutés aux deux côtés du ratio ; 50 MLP-ge4x manquants ont été entraînés sans réentraîner les sondes.
- Vérification automatique : prédictions brutes, accuracy/log-loss/F1, comptes paramétriques, ratios ≥4× par seed, manifestes de partitions et intégrité JSONL. Test d'intégrité réussi.

## Résultats clés v006 (moyennes sur cinq initialisations)

| Sonde | P_total sonde | P_total MLP ≥4× | Ratio | Accuracy sonde / MLP | Log-loss sonde / MLP |
|---|---:|---:|---:|---:|---:|
| d2/k4 croissance | 146 | 590 | 4,041× | 97,88 / 97,88 % | 0,07868 / 0,05552 |
| d4/k8 croissance | 463,6 | 1 863,8 | 4,018× | 97,65 / 98,12 % | 0,07791 / 0,05296 |
| d8/k4 croissance | 356 | 1 448 | 4,067× | 97,65 / 97,65 % | 0,05952 / 0,05394 |
| d4/k16 croissance | 443,4 | 1 791,2 | 4,046× | 97,65 / 97,88 % | 0,06593 / 0,05341 |
| d4/k8 maturation | 793 | 3 197 | 4,032× | 96,71 / 98,59 % | 0,08199 / 0,05057 |
| MIXA d4/k8 | 1 037 | 4 154 | 4,006× | 97,41 / 98,12 % | 0,09153 / 0,05175 |
| d16/k32 base | 4 489 | 17 981 | 4,006× | 97,65 / 98,82 % | 0,07710 / 0,04531 |

Les valeurs MLP sont propres au MLP-ge4x construit pour la même candidate et le même seed ; l'agrégat ci-dessus est descriptif. Voir `ex4_paired_comparison_per_seed.csv` pour chaque comparaison.

## Lecture des variantes

- **Croissance dynamique :** utile pour réduire réellement le nombre de paramètres actifs. d8/k4 a la meilleure log-loss des sondes testées. Sa qualité probabiliste reste derrière le MLP ; elle est aussi plus lente en inférence.
- **Maturation :** correction après inspection directe des traces complètes : le plateau adaptation déclenche bien la maturation sur les 5/5 seeds d4/k8 (epochs 30, 51, 33, 34, 33). Mais le meilleur checkpoint de validation est antérieur au déclenchement sur chaque seed ; `alpha_at_best_epoch=0`. Les scores reportés ne mesurent donc pas l'effet de la coordination après maturation.
- **RETRO :** `retro_adaptctl` atteint le déclencheur sur 5/5 seeds, mais après le meilleur checkpoint ; au checkpoint retenu `alpha=0` et `beta_local=1`, donc RETRO n'a pas encore modifié les mises à jour qui produisent le score publié. `retro_linear` exerce la rampe inverse (alpha croît, beta décroît) ; sa log-loss est mauvaise (0,09493 en moyenne) et le fit très long (4,61 s contre 0,210 s pour le MLP-ge4x apparié).
- **MIXA :** le contrôleur atteint le plateau sur 5/5 seeds, mais uniquement après le checkpoint retenu ; `alpha_at_best_epoch=0`. Le MIXA évalué au meilleur checkpoint ne bénéficie donc pas de la coordination émergente. Il compte 1 037 paramètres totaux prétraitement inclus, log-loss 0,09153 ; aucun avantage ici.
- **d2/k4 :** accuracy moyenne non inférieure au MLP (97,88 %), mais log-loss très dégradée de 0,02316 et latence médiane environ 5,5 fois supérieure.

## Limites décisives

1. Wisconsin est historiquement exposé dans EX2 ; ce n'est pas un domaine confirmatoire vierge.
2. Les cinq seeds changent l'initialisation, pas les observations ; la campagne n'est pas une validation indépendante multi-jeux.
3. Le checkpoint est choisi par log-loss validation puis évalué sur cette même validation : les scores sont des mesures de développement optimistes, pas des estimations test indépendantes. Pour maturation/RETRO/MIXA, le plateau se déclenche dans la trace après le meilleur checkpoint ; les métriques publiées capturent donc essentiellement l'état pré-maturation.
4. Le chargeur sklearn construit l'objet source complet en mémoire ; le code n'indexe ensuite que train/validation/adaptation, n'entraîne ni ne sélectionne sur les lignes test, et n'envoie pas leurs valeurs au modèle. Il ne s'agit pas d'une isolation mémoire au niveau du processus.
5. FLOPs/MACs complets, RAM RSS, VRAM, énergie, débit multi-batch et coût total de recherche ne sont pas mesurés. CUDA n'est pas disponible et le nom exact du CPU n'est pas fourni par l'environnement.
6. La campagne v006 est une campagne de validation d'architecture et de ratios, pas une confirmation externe. Les six domaines EX3 cités dans les débris ne sont pas rejouables sans leurs workspaces et données brutes.

## Conclusion utilisable

La croissance dynamique donne des sondes réellement beaucoup plus petites, mais les MLP-ge4x gardent un avantage de log-loss et de latence. L'objectif recherché — précision conjointe au moins égale et ressources égales ou plus faibles — **n'est pas démontré**. La branche d8/k4 est le meilleur point de départ technique à poursuivre sur données externes avec mesures FLOPs/RAM, non un vainqueur déclaré.


---

## Mise à jour de reprise — micro-MIXA et transfert externe (30 octobre 2026)

### Vérification de la continuité
La reprise a conservé les campagnes v005 et v006 sans les relancer. Les tests existants passent : v005 (60 sondes, 85 MLP, 120 couples) et v006 (60 sondes, 135 MLP, 120 couples). v007 possède un registre étendu de 95 lignes au lieu des 70 attendues par son test historique ; ce test échoue sur le registre mélangé, mais les 70 lignes initiales et les 25 lignes micro-MIXA ont été séparées et auditées dans les filtres dédiés v007/v008. Aucun agrégat non filtré v007 n'est utilisé.

### micro-MIXA reconstruite
Les cinq ablations micro-MIXA sur Wisconsin ont été récupérées sans réentraînement (25 sondes, 30 MLP distincts, 50 comparaisons). L'hypothèse hybride est donc testée explicitement ; elle n'est pas reproduite à l'identique du prototype EX3 perdu. La branche fixe seule est la moins performante. Le mélange/gating peut améliorer l'accuracy par rapport à l'adaptatif seul, mais n'atteint pas le log-loss du MLP.

### Transfert Iris
Une seule tâche extérieure aux fichiers historiques du projet a pu être chargée localement : Iris (`sklearn.load_iris`), 150 observations, 4 variables, 3 classes. Quatre candidates sur cinq graines, 40 MLP uniques et un test descriptif de 30 observations ont été exécutés. Les comparateurs ge4x respectent tous le ratio total corrigé, minimal 4,015625×. Les micro-MIXA égal/gates ont une accuracy test moyenne de 0,9600–0,9667, contre 0,9667 pour leurs MLP ge4x ; leur log-loss reste plus élevée (0,12062–0,17272 contre 0,09331–0,09633). La latence batch 1 reste environ 5,5–6,4 fois supérieure pour les MIXA entraînés sur Iris ; leur fit est environ 5,2–8,8 fois plus long. Les durées de fit du bras adaptatif sont indisponibles, car seuls ses checkpoints de meilleure validation avaient été sauvegardés avant l'interruption initiale ; ses poids ont été récupérés, et aucun temps n'a été inventé.

### Décision finale
**L'objectif principal n'est pas atteint.** Les ratios de paramètres sont satisfaits, mais l'équivalence conjointe accuracy/log-loss et l'avantage de ressources ne le sont pas. La micro-MIXA est une piste crédible de réduction de capacité et de MACs analytiques, pas une solution gagnante : la calibration et surtout la latence restent moins bonnes. Iris est petit et le test ne contient que 30 exemples ; les cinq seeds réutilisent ces mêmes observations. Le rapport ne revendique aucune non-infériorité statistique formelle.

### Réserves et éléments non terminés
- L'API `load_iris()` matérialise le tableau complet ; la stratification lit le vecteur cible pour assigner les partitions et le CSV/NPZ source complet est archivé. Aucune ligne test n'est utilisée pour fit, arrêt, prétraitement, métrique ou sélection avant gel, mais l'isolation mémoire/processus absolue n'est pas revendiquée.
- Les tentatives de téléchargement UCI Banknote et MAGIC ont échoué sur une limitation réseau/DNS de l'environnement ; aucun résultat n'est prétendu sur ces jeux.
- FLOPs/MACs complets (matériel), VRAM, énergie et coût complet de recherche ne sont toujours pas mesurés. Les MAC reportés sur Iris sont analytiques et incomplets.
- Le workspace EX3 complet, ses checkpoints, données et scripts restent absents ; les mentions de ses performances sont des débris non reproductibles.

Les détails et preuves se trouvent dans `rapport_micro_mixa_ex4.md`, `rapport_transfert_externe_iris.md`, `AUDIT_V007_MIXED_REGISTRY.md` et les versions v008/v009.
