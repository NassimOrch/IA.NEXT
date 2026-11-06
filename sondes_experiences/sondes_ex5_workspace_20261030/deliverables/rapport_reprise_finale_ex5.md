# EX5 — Rapport final de reprise, conformité et résultats

**Date de clôture de cette reprise : 30 octobre 2026.**  
**Prompt exécuté : `prompt_ex5.json`, révision 1.1, SHA-256 `88f67fc34bf34c5ca0817da42a057ed71dfb092cfb33720be5532da96bab3291`.**  
**Versions présentes : v001 à v007.**

## 1. Verdict de conformité générale

Le prompt a été relu intégralement (486 lignes, environ 60 000 caractères), avec ses sections 0 à 17, et croisé avec EX3, EX4, les pré-enregistrements, scripts, registres bruts, checkpoints, prédictions et tests. Le travail a repris depuis les artefacts existants ; les campagnes validées n'ont pas été relancées pour la forme.

La campagne EX5 est **largement exécutée sur les axes réalisables dans cet environnement**, et les résultats bruts sont préservés. Toutefois, il serait faux de déclarer que toutes les obligations du prompt sont intégralement satisfaites : les MACs complets de l'entraînement, l'énergie, la VRAM, une partie des métriques RSS/checkpoint homogènes et les domaines Banknote/MAGIC restent non mesurés ou bloqués. La règle rouge prédictive-ressources n'est pas atteinte. Le statut honnête est donc : **campagne expérimentale substantiellement exécutée, mais réussite scientifique globale non atteinte et quelques exigences obligatoires encore partielles/bloquées**.

## 2. Reprise incrémentale — versions et campagnes

| Version | Périmètre | Réutilisation et résultats | État |
|---|---|---|---|
| v001 | RETRO/factoriel, proportion fixe-adaptative, OOF, premières topologies Q/A | 12 familles RETRO sur 5 graines ; balayage des proportions ; correction résiduelle OOF ; contrôles Q/A | Exécutée, anomalies/doublons documentés |
| v002 | Sémantiques Adam/gel, correction alternée A↔B | 25 essais Adam/AdamW (5 politiques × 5 graines) ; 7 bras alternés × 5 graines ; tests de gel bitwise | Exécutée, contrôles stricts passés |
| v003 | Transfert externe Wine et Digits | 30 sondes, 60 MLP ; gel des modèles avant ouverture du test ; bootstrap apparié pré-enregistré | Exécutée ; non-infériorité conjointe non démontrée |
| v004 | Ablations hiérarchiques question/réponse | 7 contrôles × 5 graines ; MLP appariés ; Q-only, réponses supervisées, topologies hybrides et OOF | Exécutée, règle rouge non atteinte |
| v005 | Optimisation micro-MIXA par partage d'encodeur/centres | 4 configurations × 5 graines ; comparateurs MLP matched/ge4x | Exécutée, gains de compacité mais pas de victoire complète |
| v006 | PCA question-only, micro-MIXA et vectorisation | 6 configurations × 5 graines ; 30 sondes ; 40 modèles MLP uniques et 60 liens ; doublons de reprise audités | Exécutée, aucun candidat ne passe la règle rouge |
| v007 | Profilage d'inférence TorchScript/Numba du candidat Q-only | 5 graines ; pas de réentraînement ; 25 exports hashés ; parité stricte | Exécutée ; backends optimisés non admissibles ou plus lents |

Les fichiers source EX2/EX3/EX4 et les versions précédentes EX5 sont conservés. Les journaux bruts append-only demeurent la source d'autorité ; les tableaux présentés sont des agrégats, avec dédoublonnage analytique explicite lorsque les clés et hashes le justifient.

## 3. RETRO maturation, factoriel alpha×beta et optimiseurs

La campagne RETRO v001 contient 12 familles de calendriers/contrôles et 5 graines, soit 60 paires uniques. Le registre possède 61 lignes à cause d'une répétition `retro_linear/1501` : checkpoints et prédiction identiques, mais temps mural discordant. Les deux lignes sont conservées ; le temps le plus élevé est utilisé pour l'analyse conservatrice des coûts.

Le contrôleur de maturation a bien déclenché sur 5/5 graines pour `maturation` et `retro_inverse`, mais le checkpoint choisi par la règle de validation globale est resté pré-activation (`alpha=0`, `beta_local=1`). Le meilleur snapshot post-activation a une log-loss moyenne d'environ 0,1630 pour maturation et 0,1495 pour RETRO inverse, contre 0,08199 au checkpoint pré-activation. Ce résultat ne prouve pas que toute forme de RETRO est impossible ; il indique que les calendriers effectivement essayés dégradent ici les snapshots post-activation et n'améliorent pas le checkpoint sélectionné.

`retro_delta`, `retro_grad`, `retro_gamma_half`, `retro_gamma_two`, `retro_linear`, `immediate`, `linear`, `local_only` et les contrôles de base sont consignés séparément dans `retro_post_activation_summary_ex5.csv`. La cellule factorielle A0B0 s'effondre sur cette configuration (accuracy moyenne 48 %, log-loss ≈0,6997) et doit rester rapportée comme ablation défavorable, pas être retirée. Les effets de coordination et de plasticité locale sont étudiés, mais l'inférence statistique reste limitée par le dataset de développement déjà exposé.

L'étude Adam/gel v002 comprend 25 essais. Les 20 phases strictement gelées passent les contrôles de stabilité des paramètres et des états concernés. Les contrôles sémantiques confirment que LR=0 avec `step()` n'est pas un gel d'état (moments et compteur changent), qu'un gradient nul avec `step()` peut modifier les poids sous momentum, et que l'interpolation delta=0 peut laisser les poids constants tout en faisant évoluer l'optimiseur. La journalisation exhaustive par époque de tous les moments/schedulers n'est toutefois pas homogène dans les expériences historiques : cette sous-exigence reste partielle.

## 4. Proportions fixe/adaptative et optimisation micro-MIXA

Le balayage 100/0, 75/25, 50/50, 25/75 et 0/100 a été fait sous budget de paramètres tenu constant et complété par la vue à unités de branches constantes. Les dimensions `P_A_total`, `P_F_total`, `rho_A`, `rho_F`, paramètres du gate et capacité totale sont conservées dans les CSV dédiés.

Les extensions v005/v006 ont étudié encodeur et centres partagés, plusieurs gates, branches fixes/adaptatives et PCA question-only. Le partage réduit les paramètres et MACs, mais n'a pas préservé de manière générale la log-loss du MLP. Les six candidats PCA-Q v006 sont tous derrière leurs MLP ge4x en accuracy/log-loss ; 30/30 ont moins de MACs forward et de bytes déployés, mais 0/30 ont une latence batch 1 p50 ou p95 inférieure, et seulement 1/30 un temps pipeline inférieur ou égal.

Le profilage v007 n'a réentraîné aucun modèle. TorchScript `trace` reproduit exactement les logits sur cinq graines, mais la latence batch 1 moyenne de la sonde est ≈0,09597 ms, contre ≈0,01239 ms pour le MLP tracé (≈7,75× plus lente). `optimize_for_inference` dépasse la tolérance pré-enregistrée de 1e-6 sur au moins un modèle de chaque paire et est exclu. Numba v1 est invalidé (primitive MLP incorrecte) ; Numba v2 conserve la parité MLP 5/5 mais la sonde ne passe la parité stricte que sur 1/5 graine. Aucune de ces variantes ne fournit un chemin de déploiement admissible plus rapide que le MLP.

## 5. Correction alternée A↔B et hiérarchie question/réponse

La variante `micro_mixa_alternating_error_corrector` a sept bras sur cinq graines. Les rôles A/B, les résidus, les cycles et le gel strict sont journalisés ; les hashes bitwise du correcteur gelé restent invariants pendant les phases strictes. Les comparateurs MLP matched/ge4x sont présents. L'alternance réduit parfois le nombre de MACs et la taille déployée, mais le temps d'entraînement et la latence batch 1 dépassent le MLP ; elle ne satisfait donc pas la règle rouge.

Les topologies Q/A comprennent hybride/hybride, fixe→adaptatif, adaptatif→fixe, Q-only strict, answer-side supervisé, contrôles neutres/conjoints et résidus OOF. Le niveau question reçoit X seulement ; Y_train n'est cible de supervision que dans les bras answer-side qui le déclarent. Le forward d'inférence n'accepte que X. Les résidus du correcteur OOF sont issus de prédictions out-of-fold train.

### Appariement OOF MLP vérifié

Un audit spécifique a formalisé 20 liens candidate×graine×type (`matched` et `ge4x`) pour les deux correcteurs OOF. Aucun MLP n'a été réentraîné : 10 modèles physiques du cache sont partagés exactement par budget et graine entre les deux têtes OOF. Le système complet OOF a `P_total=1 160`; le MLP ge4x a 4 649 paramètres, ratio 4,007759× ; le MLP matched a 1 151 paramètres (écart de −0,8 %, ratio 0,99224×).

| Candidate OOF | Accuracy val. | Log-loss val. | MLP ge4x accuracy | MLP ge4x log-loss | Temps pipeline sonde / MLP | Latence p50 batch1 sonde / MLP |
|---|---:|---:|---:|---:|---:|---:|
| Correcteur adaptatif | 97,65 % | 0,05218 | 98,59 % | 0,05037 | 2,138 s / 0,268 s | 0,3407 ms / 0,0166 ms |
| Correcteur fixe | 97,65 % | 0,06856 | 98,59 % | 0,05037 | 1,992 s / 0,268 s | 0,3670 ms / 0,0166 ms |

Les 10 fichiers de prédictions OOF ont été recalculés par `calc_metrics` ; écart maximal par rapport aux métriques enregistrées : 0,0 ; checkpoints, prédictions et cibles appariées passent les hashes/contrôles. L'OOF adaptatif est une piste prédictive intéressante, mais échoue en coût total d'entraînement et en latence batch 1 ; il ne franchit donc pas la règle rouge.

## 6. Transfert et statistiques

La campagne v003 a évalué Wine et Digits après gel cryptographique des candidats, hyperparamètres, marges et scripts, avant ouverture des tests. Cinq graines représentent des initialisations sur les mêmes sujets ; elles ne sont pas comptées comme cinq jeux d'observations indépendants. Le bootstrap apparié et la correction multiple pré-enregistrés n'établissent la non-infériorité conjointe accuracy/log-loss pour aucune des six comparaisons (3 candidates × 2 domaines). Wine est petit ; Digits montre des écarts plus importants en faveur du MLP. Iris est un transfert historique EX4 exploratoire et n'est pas compté comme confirmation EX5.

Banknote Authentication et MAGIC Gamma Telescope ont été recherchés depuis les sources UCI/OpenML, mais le runtime ne résout pas leurs hôtes (DNS indisponible). Aucun fichier ni résultat n'a été fabriqué. Aucun autre domaine extérieur vérifiable et local n'était disponible dans cet environnement au moment de la reprise.

## 7. Règle rouge — ressources et MLP ge4x

L'audit global contient 437 enregistrements de comparateur MLP ge4x ; aucun n'a un ratio inférieur à 4 ; le minimum est 4,000735×. Le mapping OOF ajoute 10 liens ge4x spécifiques par réutilisation exacte du cache, sans réentraîner les modèles. Les compteurs incluent les buffers, paramètres fixes, gates et prétraitements persistants.

La dimension `forward MACs` est favorable aux sondes dans les couples audités. En revanche, les taux de passage sont faibles pour le temps d'entraînement et quasi nuls pour la latence batch 1 sur les campagnes principales. Les bytes déployés et RSS sont parfois favorables, mais les mesures RSS/checkpoint ne sont pas uniformes dans tout l'historique. Les MACs complets d'entraînement ne sont pas instrumentés ; énergie non mesurée ; VRAM indisponible (CPU-only). Il n'existe donc aucune candidate satisfaisant simultanément la qualité prédictive et chaque dimension obligatoire mesurable.

## 8. Intégrité, anti-triche et exceptions conservées

Dernier audit global des versions v001–v007 :

- 1 850 fichiers JSON valides dans v001–v007, 0 erreur de parsing ;
- 1 720 lignes JSONL valides dans 53 registres, 0 erreur de parsing ;
- 1 313 références de checkpoints, 0 échec SHA-256 ;
- 1 162 références canoniques de prédictions, 0 échec SHA-256 ;
- 40 anciens pointeurs de prédiction superseded, explicitement documentés ;
- 826 fichiers de prédictions recalculés, 0 divergence de métriques ;
- 437 ratios ge4x, 0 sous 4, minimum 4,000735×.

Exceptions préservées : doublons v006 liés à une reprise concurrente (mêmes checkpoints/prédictions/historiques, temps différents ; dédoublonnage analytique par clé et temps le plus défavorable), doublon `retro_linear/1501` (temps conservateur), ancienne erreur de métadonnée du bras supervisé conjoint Q/A (sidecar correctif, brut intact), 40 pointeurs de fichiers externes historiques superseded, prototype Numba v1 invalide, et ancien test EX4 v007 attendant 70 lignes alors que le registre historique mélangé en contient 95. Aucun historique brut n'a été réécrit.

Les tests canoniques passent : v001 final integrity et sémantique Adam ; v002 alternance/Adam ; v003 disjonction des partitions ; v004 (2 tests), v005 (1), v006 (3), v007 (3 fonctions invoquées individuellement ; collecte pytest globale non revendiquée), et tests OOF workspace (4). L'ancien test v001 à chemins obsolètes est signalé comme obsolète, pas présenté comme un test réussi.

Un audit de l'ensemble du workspace, distinct de l'audit centré sur les versions, a ensuite contrôlé 3 951 fichiers non-cache : 1 865 JSON valides, 1 720 lignes JSONL valides dans 53 fichiers et 60 CSV rectangulaires. Aucun défaut de parsing ou de forme n'a été détecté. Les deux copies du prompt EX5 correspondent au SHA-256 attendu ; aucun lien symbolique ne sort du workspace. Le manifeste final SHA-256 est `deliverables/sha256_manifest_workspace_final.csv`.

## 9. Conclusion

Le prompt EX5 a guidé une campagne incrémentale et auditée jusqu'à v007. Les comparaisons MLP ge4x, le correcteur OOF, les proportions, RETRO, Adam/gel, alternance, topologies Q/A et le profilage CPU sont documentés. Les résultats négatifs ont été conservés. Cependant, la performance prédictive conjointe et la règle rouge ressources ne sont pas satisfaites ; les domaines Banknote/MAGIC et plusieurs instruments de ressources restent bloqués/non mesurés. **EX5 n'est donc pas déclaré intégralement satisfait ni victorieux.**

Les chemins directs des preuves sont listés dans `WORKSPACE_INDEX_EX5_FINAL.md` et les tables CSV/JSON associés dans `deliverables/`.


## 11. Livraison consolidée

Le workspace final v001–v007 est archivé dans `sondes_ex5_workspace_20261030.zip`. Le test ZIP (`unzip -t`) et le SHA-256 détaché (`sondes_ex5_workspace_20261030.zip.sha256`) sont fournis séparément. Le manifeste interne `deliverables/sha256_manifest_workspace_final.csv` couvre les 3 951 fichiers non-cache du workspace, hors manifeste lui-même et hors caches compilés/pytest.
