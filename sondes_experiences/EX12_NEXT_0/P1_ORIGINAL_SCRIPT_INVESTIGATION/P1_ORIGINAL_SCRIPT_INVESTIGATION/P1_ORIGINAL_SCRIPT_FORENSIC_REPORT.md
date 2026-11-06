# RAPPORT D'ENQUETE DE PROVENANCE ET DE REPRODUCTIBILITE

## Incident : scripts sources originaux non retrouves pour P1_RUN_001 et P1_RUN_002

**Reference :** EX12-P1-SOURCE-PROVENANCE-INVESTIGATION-001  
**Experience :** EX12_NEXT_0 / phase P1  
**Date de l'enquete :** 4 novembre 2026  
**Statut de la recherche :** originaux exacts non recuperes ; le present rapport de lacune est donc applicable.

---

## 1. Attestation principale

J'atteste les constats suivants, limites aux elements effectivement inspectes dans l'environnement accessible :

1. **Les resultats de P1_RUN_001 et P1_RUN_002 existent.** Les CSV de mesures brutes, CSV de synthese, fichiers JSON de tests numeriques et metadonnees sont presents dans le workspace `EX12_NEXT_0`.
2. **Les scripts sources originaux exacts de ces deux executions n'ont pas ete retrouves.** Aucun fichier source, snapshot de code, hash de producteur ou log de commande permettant d'identifier byte pour byte le code execute pour RUN_001 ou RUN_002 n'est present dans les artefacts accessibles.
3. Les scripts actuellement disponibles (`hc_kernels.py`, `p1_microbench.py`, `p1_microbench_repeat.py`, `test_p1_kernels.py`, `analyze_p1.py`) sont les sources des executions canoniques posterieures RUN_003/RUN_004 et de leur analyse. **Ils ne peuvent pas etre declares originaux de RUN_001/RUN_002**, car leurs dates de creation sont posterieures a celles des resultats des deux premiers runs.
4. Les fichiers de resultats actuels sont **internement coherents** avec leurs mesures brutes : tous les groupes ont 40 observations, les cles ne sont pas dupliquees, les agregats recalcules concordent a moins de `1e-8` d'ecart absolu, et les copies de RUN_001 sont byte-identiques.
5. Cette coherence interne ne prouve pas l'identite du programme producteur historique. L'absence des sources exactes empeche une reproduction complete et identique des prototypes 001/002.

**Conclusion formelle :** resultats presents ; sources exactes des scripts producteur absentes des emplacements inspectes ; origine precise de cette absence non determinable avec les traces actuellement disponibles.

## 2. Perimetre de l'enquete

Les recherches ont porte sur :

- l'integralite du workspace `/mnt/data/EX12_NEXT_0`, en particulier `04_code/`, `08_benchmarks/P1/`, `00_governance/` et `10_reports/` ;
- les autres artefacts accessibles sous `/mnt/data`, y compris l'archive de livraison EX12 ;
- les repertoires temporaires accessibles `/tmp` et `/var/tmp` ;
- les repertoires utilisateur accessibles `/root` et `/home/oai` ;
- les journaux accessibles sous `/var/log`, `/opt/terminal-server` et `/usr/local/init_scripts` ;
- le corpus extrait `last_sources_3`, y compris les fichiers sources et les 18 archives imbriquees deja extraites ;
- les caches Python `.pyc`, les historiques shell disponibles, la base d'historique IPython, les repertoires de sauvegarde et les metadonnees de controle de version.

Aucun depot Git ou SVN, repertoire de sauvegarde, snapshot ou checkpoint Jupyter du projet n'a ete trouve. La base IPython accessible contient une session, mais **zero entree de code et zero sortie enregistree**. Aucun fichier d'historique Bash, sh ou zsh n'a ete trouve dans les emplacements utilisateur examines. La recherche des journaux systeme accessibles n'a retourne aucune trace textuelle de `P1_RUN_001`, `P1_RUN_002` ou `p1_microbench.py`.

### Limite d'acces au systeme hote

Le processus dispose de `uid=0(root)` dans le conteneur. Le workspace repose toutefois sur un systeme de fichiers `overlayfs`. Les chemins de couches `upperdir` et `lowerdir` annonces par le montage ne sont pas accessibles depuis cet espace de noms. Les capacites du processus ne comprennent notamment pas `CAP_SYS_ADMIN`, `CAP_SYSLOG` et `CAP_DAC_READ_SEARCH`. Il n'a donc pas ete possible d'inspecter les couches de stockage cote hote, les journaux noyau/audit hote ou d'effectuer une recuperation de fichiers desalloues hors du conteneur.

Cette limite n'annule pas les recherches realisees dans le workspace visible ; elle interdit de pretendre a une expertise forensique complete du systeme hote ou a une recuperation garantie de fichiers supprimes dans ses couches non exposees.

## 3. Inventaire des resultats retrouves

### 3.1 P1_RUN_001_FAILED

| Element | Constat |
|---|---:|
| Lignes de synthese | 384 |
| Mesures brutes | 15 360 |
| Groupes kernel/batch/centres/dimension | 384 |
| Mesures par groupe | 40 |
| Tests numeriques enregistres | 54 |
| Tests en echec | 35 |
| Doublons de lignes brutes | 0 |
| Cles de synthese dupliquees | 0 |
| Groupes dont l'agregat diverge de plus de `1e-8` | 0 |

Les 35 echecs concernent `distance_output_equivalence` (35 echecs sur 36 cas). La note d'echec rapporte une divergence maximale d'environ `2.2888e-5`, au-dessus de la tolerance `1e-6`, pour le calcul intermediaire des distances. Les 15 controles de sortie complete/gradient et les 3 controles de forme/finitude du bloc de message sont reussis. Les maxima de sortie complete et de gradient presentes dans les metadonnees (`1.19e-7` et `2.24e-7`) concernent ces controles de bout en bout et ne contredisent pas l'echec des distances intermediaires.

Les fichiers au niveau racine de `08_benchmarks/P1/` et ceux de `attempts/P1_RUN_001_FAILED/` sont des copies byte-identiques pour les quatre artefacts compares : synthese, donnees brutes, tests numeriques et metadonnees. Les copies dans `attempts/` ont une date de naissance et un `ctime` ulterieurs, alors que leur `mtime` a ete conserve. Cela correspond a une operation de copie/archivage des resultats, et non a une disparition de ces fichiers.

### 3.2 P1_RUN_002

| Element | Constat |
|---|---:|
| Lignes de synthese | 420 |
| Mesures brutes | 16 800 |
| Groupes kernel/batch/centres/dimension | 420 |
| Mesures par groupe | 40 |
| Tests numeriques enregistres | 54 |
| Tests numeriques en echec | 0 |
| Doublons de lignes brutes | 0 |
| Cles de synthese dupliquees | 0 |
| Groupes dont l'agregat diverge de plus de `1e-8` | 0 |

**Limitation methodologique importante :** `PROVISIONAL_LIMITATION_NOTE.md`, le registre append-only et le rapport P1 precisent que les kernels `topq_select_and_readout_q*` mesuraient la selection/lecture sur des activations deja preparees, alors que la reference dense comprenait davantage d'operations (distance, activation, lecture). Cette comparaison n'etait donc pas end-to-end et appariee. RUN_002 ne peut pas servir a conclure sur la vitesse top-q par rapport au dense.

Le fichier `P1_BENCHMARK_METADATA.json` porte le statut `PASS` parce que ses 54 tests numeriques passent. Le registre plus specifique porte `PROVISIONAL_PASS_WITH_COMPARISON_LIMIT` et la note de limitation a ete ajoutee. Pour l'interpretation scientifique, le statut plus specifique du registre et la note ulterieure prevalaient : RUN_002 est un prototype provisoire, exclu de la conclusion top-q.

### 3.3 Verification des agregats

Pour RUN_001 et RUN_002, chaque cle de groupe possede exactement une ligne de synthese et exactement 40 lignes brutes. Les p50, p95, p99, moyennes, ecarts-types et debits ont ete recalcules depuis les mesures brutes. Les ecarts absolus maximaux observes sont inferieurs a `1e-8` :

| Mesure | RUN_001 | RUN_002 |
|---|---:|---:|
| p50 | 2.22e-16 | 9.97e-17 |
| p95 | 8.88e-16 | 4.44e-16 |
| p99 | 4.44e-16 | 4.44e-16 |
| Moyenne | 8.88e-16 | 4.44e-16 |
| Ecart-type | 1.11e-16 | 4.44e-16 |
| Debit | 7.45e-9 | 3.73e-9 |

La colonne `cold_ms` ne peut pas etre recalculee depuis le CSV brut, car celui-ci stocke les 40 repetitions chronometrees, pas la mesure froide unique. Cela constitue une limite de verification, pas une divergence detectee.

## 4. Chronologie des fichiers et de la provenance

Les dates ci-dessous sont les horodatages UTC conserves dans les metadonnees de fichiers du conteneur :

| Horodatage UTC | Evenement |
|---|---|
| 11:13:32 | Ecriture des resultats RUN_001 (synthese, brut, tests, metadata) |
| 11:14:51 | Creation du dossier `attempts/P1_RUN_001_FAILED/` et copie des resultats deja ecrits ; copies identiques, `mtime` conserve |
| 11:15:11 | Ecriture des resultats RUN_002 |
| 11:16:53 | Creation de `hc_kernels.py`, `p1_microbench.py` et `test_p1_kernels.py` |
| 11:17:02 | Ecriture des resultats RUN_003 |
| 11:19:58 | Creation de `p1_microbench_repeat.py` et de son hash de script |
| 11:20:06 | Ecriture des resultats RUN_004 |
| 11:21:08 | Creation de `analyze_p1.py` |
| 11:23:03 | Creation du registre P1 final, de la note de limitation RUN_002, du rapport P1 et de `P1_SOURCE_HASHES.json` |
| 11:50:43 | Creation des caches `.pyc` des sources actuellement presentes |

Cette chronologie est centrale : les scripts actuels P1 ont ete ecrits apres RUN_001 et RUN_002. Le manifeste `P1_SOURCE_HASHES.json` est lui aussi posterieur et ne reference que les scripts reutilisables/canoniques conserves ensuite. Il n'existe pas d'empreinte de producteur pour RUN_001 ou RUN_002.

Les caches `.pyc` retrouves ne restaurent pas les versions historiques : ils ont ete crees a 11:50:43 et leur en-tete encode les dates et tailles des sources actuelles (11:16:53 ou 11:19:58). Ils sont donc des compilations des fichiers actuellement presents, et non des copies bytecode anterieures de RUN_001/002.

## 5. Pourquoi les resultats existent-ils alors que les scripts sont absents ?

### 5.1 Ce qui est etabli

- Les scripts producteurs n'ont pas ete inclus dans les dossiers de resultats de RUN_001 et RUN_002.
- Aucun hash de ces scripts n'a ete inscrit pour ces runs.
- Les fichiers de resultats ont ete ecrits separement et sont encore disponibles.
- Les sources reutilisables actuelles ont ete sauvegardees et hashees ensuite pour RUN_003/RUN_004.
- Les traces disponibles ne montrent ni le nom du fichier temporaire producteur, ni la commande exacte, ni une operation de suppression identifiable visant ces scripts.

### 5.2 Explication operationnelle la plus compatible avec les traces

L'explication la plus compatible avec la chronologie est une **lacune de conservation de la source au moment des deux premiers prototypes** : le code d'execution initial a probablement ete lance depuis une cellule/commande transitoire, un heredoc, un fichier temporaire, ou une autre forme de code non archivee dans `04_code/`. Les donnees de sortie ont, elles, ete ecrites dans le workspace. Une version reutilisable et structuree du banc a ensuite ete sauvegardee comme `p1_microbench.py`, puis dupliquee/adaptee pour RUN_004 et enfin hash-registree.

Cette explication est une hypothese de processus, pas un fait directement observe. Les traces permettent egalement qu'un fichier ait ete supprime, conserve dans un emplacement non monte, ou perdu lors d'un changement d'environnement. Faute d'historique de commandes, de journal d'audit du systeme hote ou de sauvegarde, ces scenarios ne peuvent pas etre distingues objectivement.

### 5.3 Ce qui n'est pas demontre

Aucun element retrouve ne permet d'attester un sabotage, un vol de donnees, une suppression intentionnelle, une manipulation ou une appropriation du travail. Inversement, l'absence de preuve ne permet pas d'attester qu'aucune suppression n'a jamais eu lieu. La conclusion honnete est : **lacune de provenance et de conservation de code confirmee ; intention et mecanisme exact non etablis**.

## 6. Pourquoi les sources RUN_003/RUN_004 ne peuvent pas remplacer les originaux

`p1_microbench.py` a ete cree a 11:16:53, apres les sorties RUN_001 et RUN_002. Il configure le dossier de sortie `P1_RUN_003`, la graine `120402` et un ensemble de 600 lignes de synthese. `p1_microbench_repeat.py` est cree a 11:19:58 ; il differe notamment par le dossier `P1_RUN_004`, la graine `120403` et les identifiants de run. Ces sources correspondent donc aux runs canoniques ulterieurs.

RUN_001 a 384 lignes, RUN_002 420 lignes et les deux runs canoniques 600 lignes. Les noms de kernels et le perimetre de mesure ont aussi evolue : RUN_002 emploie notamment `topq_select_and_readout_q*`, tandis que les runs canoniques introduisent la pipeline complete `topq_rbf_pipeline_q*`. Substituer le code RUN_003/004 aux premiers prototypes changerait le protocole et ne restituerait pas le code exact.

Les cinq fichiers de code actuels dont le hash est enregistre dans `P1_SOURCE_HASHES.json` correspondent bien a leurs hashes actuels. Cela valide leur identite courante pour les runs ulterieurs ; cela ne cree pas retroactivement une empreinte pour RUN_001/002.

## 7. Verdict et traitement scientifique

| Question | Reponse de l'enquete |
|---|---|
| Resultats RUN_001 presents ? | Oui |
| Resultats RUN_002 presents ? | Oui |
| Scripts originaux exacts retrouves ? | Non |
| Copies identiques des resultats RUN_001 ? | Oui, deux emplacements controles |
| Coherence interne raw/synthese ? | Oui, pour les agregats verifiables |
| Reproduction byte-pour-byte des producteurs historiques possible ? | Non, sans source originale |
| Sabotage ou vol etabli ? | Non |
| Cause exacte de l'absence connue ? | Non ; lacune de conservation la plus probable |

Traitement a conserver dans EX12 :

- RUN_001 demeure un prototype numerique echoue, conserve mais exclu des comparaisons canoniques.
- RUN_002 demeure un prototype provisoire ; il est exclu des conclusions de vitesse top-q/dense non appariees.
- RUN_003 et RUN_004 restent les seuls runs P1 canoniques pour les conclusions de performance, avec leurs sources, tests et hashes disponibles.
- Le present rapport et le script d'audit fourni ne doivent jamais etre presentes comme les scripts producteurs originaux de RUN_001/002.

## 8. Signature et reserve d'authenticite

**Attestation redigee et signee sous forme textuelle :**

**ChatGPT — assistant IA OpenAI**  
Redacteur du rapport d'enquete de provenance P1  
Date : 4 novembre 2026  
Reference : `EX12-P1-SOURCE-PROVENANCE-INVESTIGATION-001`

Cette signature est une signature declarative de l'assistant ayant redige le rapport. Ce n'est ni une signature electronique qualifiee, ni un certificat d'identite, ni une expertise judiciaire independante. Les empreintes SHA-256 jointes permettent de verifier que les fichiers livres n'ont pas change depuis leur hachage dans cet environnement.

---

## Annexe A — empreintes SHA-256 des resultats historiques

**RUN_001 summary**  
`43a5cf8c5ad19ba512e6fe539767ad977f31d864f903923ea5d63789842f1c3d`

**RUN_001 raw**  
`665fd7a9b613a497ebede5ee9380a769de350aa7bc10a4b06b056e7fef8d7bcb`

**RUN_001 tests**  
`2534984ee727e2340349e05622ef739d1f8b8b5f39eccea6a1b8b0fd04f39e98`

**RUN_002 summary**  
`13b721676035e637c0618f4c51c5749a4995a1c12f9ccfba61ee372a6ae76bc5`

**RUN_002 raw**  
`4a951c6c43a8c30946c1750d08f92ed648029d15bed808a8e270ecd552249e5e`

**RUN_002 tests**  
`d4c44fa1650b0299a1e9ae24646b83a000048bd3778bd3113fa55d174c7c9db6`

Les empreintes des metadonnees, scripts de reference, registres, audits et pieces annexes sont detaillees dans `P1_ORIGINAL_SCRIPT_FORENSIC_AUDIT.json` et `EVIDENCE_SHA256SUMS.txt`.
