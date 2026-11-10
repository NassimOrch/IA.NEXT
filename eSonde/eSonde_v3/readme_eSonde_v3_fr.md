
# eSonde v3
## Modèle de langage non neuronal à sondes explicites

**Version :** 3  
**Statut :** preuve de concept logicielle fonctionnelle — capacité généraliste non démontrée  
**Architecture :** sondes statistiques explicites, mémoire structurée et coordination probabiliste  
**Contrainte fondamentale :** zéro neurone, zéro MLP, zéro réseau neuronal

---

## 1. Présentation

eSonde v3 est une architecture expérimentale de modélisation du langage qui remplace les réseaux neuronaux conventionnels par un ensemble de sondes statistiques explicites.

Contrairement aux architectures fondées sur des transformeurs, des réseaux récurrents ou des MLP, eSonde ne repose pas sur des couches neuronales apprises, des embeddings denses ou des mécanismes d'attention Q/K/V.

Son état interne est constitué de structures inspectables :

- compteurs statistiques ;
- tables creuses ;
- index de recherche ;
- graphes de relations ;
- historiques de séquences ;
- structures morphologiques ;
- modèles de transitions d'octets ;
- paramètres de coordination probabiliste.

L'objectif est d'étudier jusqu'où une architecture exclusivement fondée sur des sondes explicites peut apprendre, modéliser et générer du langage.

**Important :** eSonde v3 constitue une réalisation logicielle fonctionnelle de cette approche. Les résultats disponibles ne démontrent pas encore qu'il possède les performances linguistiques nécessaires à un modèle généraliste compétent.

Il faut donc distinguer deux objectifs :

1. La réalisation d'une architecture non neuronale exécutable et vérifiable.
2. La démonstration expérimentale de sa capacité à comprendre, généraliser et produire du langage.

Le premier est étayé par les contrôles logiciels disponibles. Le second reste un objectif de recherche.

---

## 2. Principes architecturaux

### 2.1. Invariants fondamentaux

L'architecture respecte les contraintes suivantes :

- aucun neurone artificiel ;
- aucun perceptron multicouche (MLP) ;
- aucun transformeur ;
- aucune attention neuronale Q/K/V ;
- aucun embedding dense appris ;
- aucune couche neuronale dissimulée sous une autre appellation.

Les mécanismes d'apprentissage utilisent des statistiques explicites, des structures de données et des paramètres de coordination.

Les sondes doivent rester identifiables, inspectables et évaluables individuellement.

### 2.2. Architecture générale

Le modèle repose sur sept familles de sondes et un coordinateur probabiliste.

```text
                    CONTEXTE LINGUISTIQUE
                             |
                             v
                     TOKENIZER V3
                             |
                             v
                      PROBE MODEL
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
         SEQ              SKIP_REL             MORPH
          |                  |                  |
          v                  v                  v
      Séquences          Relations           Morphologie
      observées          distantes            de surface
          |                  |                  |
          +------------------+------------------+
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
         SEM               DISC                RETR
          |                  |                  |
          v                  v                  v
       Relations          Mémoire            Récupération
       sémantiques        discursive          de contextes
          |                  |                  |
          +------------------+------------------+
                             |
                             v
                           BYTE
                             |
                             v
                    Transitions UTF-8
                             |
                             v
                         COORD
                             |
                             v
                 Distribution probabiliste
                             |
                             v
                 PRÉDICTION / GÉNÉRATION
```

Les familles produisent des propositions probabilistes distinctes. COORD les combine selon leur disponibilité et leur poids de coordination.

---

## 3. Les sept familles de sondes

### 3.1. SEQ — mémoire des séquences

SEQ mémorise les continuations observées après des suffixes de tokens.

Elle exploite des contextes de différentes longueurs, de 1 à 5 tokens.

Son fonctionnement est proche d'un modèle statistique n-gramme.

**Rôle :**
- mémoriser les enchaînements fréquents ;
- estimer les continuations probables ;
- exploiter les régularités locales du langage.

**Limite :** les dépendances longues ou les formulations inédites sont difficiles à généraliser à partir de simples fréquences.

### 3.2. SKIP_REL — relations non contiguës

SKIP_REL recherche des régularités entre des positions éloignées dans le contexte.

Elle peut notamment exploiter des relations entre le token courant et des tokens situés plusieurs positions auparavant.

**Rôle :**
- identifier des dépendances locales non contiguës ;
- compléter les informations de SEQ ;
- exploiter des motifs récurrents dans les séquences.

**Limite :** une relation statistique entre positions ne constitue pas automatiquement une relation syntaxique ou sémantique comprise.

### 3.3. MORPH — régularités morphologiques

MORPH exploite les propriétés de surface des tokens :

- préfixes ;
- suffixes ;
- sous-chaînes ;
- formes ;
- longueurs ;
- régularités orthographiques.

**Rôle :**
- détecter des ressemblances lexicales ;
- exploiter certaines régularités morphologiques ;
- fournir des indices lorsque les tokens exacts sont rares.

**Limite :** les ressemblances de forme ne garantissent pas une proximité de sens.

### 3.4. SEM — relations sémantiques

SEM construit des structures explicites à partir des cooccurrences et de motifs relationnels observés.

Elle peut notamment représenter des associations de type :

```text
SUJET -- RELATION --> OBJET
```

**Rôle :**
- mémoriser des relations observées ;
- retrouver des associations ;
- exploiter des motifs de type sujet-relation-objet.

**Limite :** les graphes de cooccurrences ne démontrent ni une compréhension complète du sens ni la véracité des relations enregistrées.

### 3.5. DISC — mémoire discursive

DISC conserve des indices relatifs aux mentions, aux noms et aux alias présents dans un texte.

Elle propose des candidats de coréférence accompagnés d'éléments de preuve.

**Rôle :**
- suivre les mentions ;
- retrouver des entités déjà introduites ;
- fournir des candidats de résolution discursive.

**Limite :** une proposition de coréférence reste incertaine tant qu'elle n'a pas été évaluée sur des annotations de référence.

### 3.6. RETR — récupération de contextes

RETR utilise un réservoir borné d'exemples antérieurs.

Elle s'appuie notamment sur un index inversé et une comparaison du recouvrement des termes.

**Rôle :**
- retrouver des contextes similaires ;
- réutiliser des exemples observés ;
- fournir des indices issus de la mémoire du modèle.

**Limite :** la récupération d'un exemple similaire n'est pas un mécanisme de raisonnement et peut ramener un contexte trompeur.

### 3.7. BYTE — modélisation des chaînes UTF-8

BYTE est l'une des évolutions techniques majeures de la version 3.

Elle modélise les chaînes sous forme de transitions conditionnelles d'octets.

Son mécanisme comprend notamment :

- l'encodage UTF-8 ;
- les transitions d'octets ;
- les marqueurs BOS et EOS ;
- le lissage probabiliste ;
- le backoff ;
- la prise en charge des tokens hors vocabulaire (OOV).

Une chaîne inconnue peut ainsi recevoir une probabilité non nulle sans devoir être remplacée par une classe OOV unique.

BYTE utilise un historique interne d'ordre trois et conditionne notamment la chaîne par le dernier token du contexte.

Il ne s'agit donc pas d'un modèle profond de l'ensemble du contexte linguistique.

La recherche de candidats par beam search reste approximative : certaines chaînes peuvent être éliminées avant l'exploration complète de l'espace de recherche.

**Apport démontré :** sur l'échantillon MLQA étudié, BYTE attribue une probabilité aux tokens OOV et améliore considérablement la couverture probabiliste par rapport à l'ablation sans BYTE.

---

## 4. COORD — coordination probabiliste

COORD combine les distributions proposées par les familles actives.

La distribution finale est un mélange convexe :

\[
P(y\mid h,M)=
\sum_f \lambda_f(h,M)Q_f(y\mid h,M)
\]

où :

- \(y\) désigne le token candidat ;
- \(h\) représente le contexte ;
- \(M\) représente l'état du modèle ;
- \(Q_f\) désigne la distribution proposée par la famille \(f\) ;
- \(\lambda_f\) représente son poids de coordination.

Les poids respectent :

\[
\lambda_f\geq 0
\]

et :

\[
\sum_f\lambda_f=1
\]

Les paramètres sont calibrés sur les données de validation.

Ce mécanisme conserve une séparation entre les propositions des familles et permet d'inspecter leur contribution.

Un mélange convexe est mathématiquement cohérent, mais sa pertinence empirique doit être mesurée.

L'ajout d'une famille ne garantit pas automatiquement une amélioration. Sur l'échantillon MLQA étudié, BYTE seul obtient même une NLL légèrement meilleure que COORD.

Cette observation justifie des campagnes d'ablation et de calibration plus approfondies.

---

## 5. Données et apprentissage

Le checkpoint v3 actif décrit dans l'audit a été réentraîné avec le tokenizer v3 sur un petit ensemble d'exemples.

| Indicateur | Valeur rapportée |
|---|---:|
| Documents d'entraînement | 8 |
| Tokens d'entraînement | 415 |
| Documents de validation | 2 |
| Cibles de validation | 80 |
| Taille du vocabulaire | 279 tokens |

Ces volumes sont insuffisants pour établir la compétence d'un modèle généraliste.

Ils permettent toutefois de vérifier le fonctionnement de certains mécanismes logiciels et statistiques.

### 5.1. Apprentissage

L'apprentissage met à jour les structures internes des sondes à partir des exemples.

Selon la famille, ces mises à jour concernent notamment :

- les compteurs de séquences ;
- les relations non contiguës ;
- les statistiques morphologiques ;
- les graphes de relations ;
- les mentions discursives ;
- les index de récupération ;
- les transitions d'octets.

### 5.2. Calibration

COORD ajuste ses poids à partir des données de validation.

La validation doit rester distincte de l'entraînement afin d'éviter de mesurer artificiellement la qualité sur les exemples ayant servi à construire les structures du modèle.

### 5.3. Gestion des lots

La gestion des lots permet de suivre les contributions des données aux structures internes.

Le système inclut des mécanismes de mise à jour et de retrait de lots.

La réversibilité est un avantage architectural important, mais elle doit rester vérifiée par des tests portant sur l'état exact avant et après chaque opération.

### 5.4. Checkpoints

Les checkpoints permettent de sauvegarder et de restaurer l'état du modèle.

Les trois checkpoints v2 originaux sont conservés dans le livrable exécutable.

Ils ne doivent pas être confondus avec le checkpoint v3 actif.

Toute migration doit préserver les poids et les données historiques d'origine.

---

## 6. Résultats des tests logiciels

Selon le rapport final P6 et le journal EXEC-0086, la suite complète comporte 43 tests réussis.

| Groupe | Résultat |
|---|---:|
| Cœur et tokenizer | 16/16 |
| BYTE | 7/7 |
| Fonctions avancées SEM/DISC/COREF/lots | 10/10 |
| CLI | 6/6 |
| GUI | 4/4 |
| **Total** | **43/43** |

Le journal rapporte :

- statut : OK ;
- code de sortie : 0 ;
- durée : 41,369 secondes.

Les contrôles portent notamment sur :

- l'entraînement ;
- la prédiction ;
- la génération ;
- les probabilités et les tokens OOV ;
- la sérialisation ;
- le rechargement ;
- la détection d'altération ;
- la migration des checkpoints v2 ;
- les opérations sur les lots ;
- les interfaces CLI et GUI ;
- la séparation entraînement/validation ;
- l'audit statique du runtime.

Un audit AST portant sur 21 fichiers du runtime n'a pas trouvé les constructions ou imports interdits recherchés.

Ces résultats étayent l'intégrité logicielle et la conformité architecturale des fichiers examinés.

Ils ne mesurent pas directement la compréhension linguistique.

**Attention :** ces résultats sont ceux des rapports et journaux examinés. Ils ne doivent pas être présentés comme une nouvelle exécution des tests si aucune campagne n'a été relancée.

---

## 7. Évaluation linguistique MLQA

L'évaluation rapportée utilise un échantillon multilingue de sept langues.

| Indicateur | Résultat |
|---|---:|
| Langues | 7 |
| Paragraphes | 56 |
| Tokens évalués | 4 055 |
| Tokens OOV | 3 510 |
| Taux OOV | 86,56 % |
| NLL COORD | 31,366 nats/token |
| NLL sans BYTE | 598,449 nats/token |
| NLL BYTE seul | 30,830 nats/token |
| Perplexité COORD | \(4,19\times10^{13}\) |

La perplexité est calculée à partir de la NLL :

\[
PP=\exp(NLL)
\]

Une perplexité extrêmement élevée indique une forte incertitude du modèle sur les unités évaluées.

### 7.1. Résultats par langue

| Langue | OOV | NLL COORD | Perplexité |
|---|---:|---:|---:|
| Anglais | 66,61 % | 20,292 | \(6,50\times10^8\) |
| Arabe | 89,71 % | 29,082 | \(4,27\times10^{12}\) |
| Allemand | 87,43 % | 26,022 | \(2,00\times10^{11}\) |
| Espagnol | 72,91 % | 22,559 | \(6,27\times10^9\) |
| Hindi | 94,53 % | 72,453 | \(2,92\times10^{31}\) |
| Vietnamien | 93,59 % | 25,788 | \(1,58\times10^{11}\) |
| Chinois | 98,75 % | 22,013 | \(3,63\times10^9\) |

Les unités de tokenisation diffèrent selon les langues. Il faut donc éviter d'interpréter directement ces valeurs comme un classement de compétence linguistique.

Le cas du chinois illustre cette précaution : la segmentation en caractères individuels peut modifier fortement le nombre de tokens et le taux OOV.

Le Hindi présente une NLL particulièrement élevée et nécessite une investigation spécifique.

### 7.2. Limites du protocole

Le script d'évaluation construit une séquence à partir d'éléments du titre, du contexte et de la question.

Il évalue la vraisemblance de cette séquence ; il ne calcule pas exclusivement la probabilité de la réponse à la question conditionnée par le contexte complet.

Les réponses MLQA ne sont pas utilisées dans cette mesure, ce qui évite une fuite directe des réponses.

Cependant, cette expérience n'est pas le benchmark officiel MLQA en Exact Match et F1.

La baseline unigramme à 6,244 nats n'est pas directement comparable à BYTE : elle regroupe les OOV dans une classe unique, tandis que BYTE attribue une probabilité aux chaînes exactes.

### 7.3. Interprétation

Les résultats démontrent :

- une couverture probabiliste des chaînes OOV sur l'échantillon ;
- un apport important de BYTE par rapport à l'ablation sans BYTE ;
- une capacité à évaluer des séquences multilingues avec le tokenizer et le runtime v3.

Ils ne démontrent pas :

- une bonne compréhension des sept langues ;
- une réponse correcte aux questions ;
- une généralisation linguistique robuste ;
- une génération fluide ;
- une performance compétitive face aux modèles de langage existants.

---

## 8. Qualité de génération

Un test de génération rapporté utilise le prompt :

```text
Les sondes observent
```

La génération greedy produit :

```text
# Les sondes observent.....
```

Cinq tokens de ponctuation sont produits dans cet exemple.

Ce résultat met en évidence une faiblesse de génération.

Il doit rester documenté et ne doit pas être masqué par les résultats des tests logiciels.

Une campagne spécifique devra évaluer :

- la fluidité ;
- la cohérence locale ;
- la cohérence à longue distance ;
- la diversité ;
- la répétition ;
- la pertinence par rapport au prompt ;
- la stabilité multilingue.

---

## 9. État scientifique de l'architecture

### 9.1. Points forts

**Explicabilité**

Les sondes reposent sur des structures explicites qui peuvent être inspectées.

Leurs statistiques, supports, contextes et contributions peuvent être étudiés séparément.

**Modularité**

Les familles ont des fonctions distinctes.

BYTE peut être améliorée sans réécrire SEQ ; RETR peut être évaluée indépendamment ; COORD peut être recalibré.

**Réversibilité**

La gestion des lots permet de suivre et de retirer des contributions de données.

Cette propriété facilite les audits et les expériences contrôlées.

### 9.2. Difficultés fondamentales

**Absence de compositionnalité profonde démontrée**

Les graphes sémantiques et les cooccurrences permettent de représenter des associations observées.

Ils ne démontrent pas encore la capacité à composer des concepts nouveaux et à généraliser à des situations inédites.

**Rareté des données**

415 tokens d'entraînement ne constituent pas une base suffisante pour évaluer sérieusement un modèle généraliste.

Il faut des corpus indépendants, représentatifs et correctement licenciés.

**Complémentarité des sondes**

BYTE seul obtient une NLL légèrement meilleure que COORD sur l'échantillon MLQA.

Les autres familles ne démontrent donc pas encore une contribution complémentaire positive sur cette tâche.

Il faut mesurer les performances individuelles, les ablations et les gains de coordination sur plusieurs corpus.

---

## 10. Apport des manuscrits probabilistes et quantiques

Les travaux théoriques associés à eSonde contiennent des idées mathématiques réutilisables.

L'idée pertinente pour le modèle linguistique est la formalisation de noyaux probabilistes conditionnels :

\[
Q_f(y\mid h,M)
\]

Cette notation permet de décrire la réponse probabiliste d'une famille en fonction du contexte et de l'état du modèle.

Le mélange convexe de COORD est également cohérent avec cette formalisation.

En revanche, les éléments suivants ne sont pas intégrés au runtime linguistique :

- espaces de Hilbert complexes ;
- opérateur \(J\) ;
- amplitudes et phases ;
- POVM ;
- règle de Born ;
- interférence quantique.

Aucun gain linguistique démontré ne justifie actuellement leur introduction.

La recherche quantique reste donc séparée du moteur de langage.

Seules les idées probabilistes générales sont retenues lorsqu'elles apportent une utilité opérationnelle démontrable.

---

## 11. Les trois livrables

Les trois archives sont conçues pour séparer le modèle exécutable, l'audit scientifique et le suivi du projet.

### 11.1. Dmodel_eSonde_v3.zip

Livrable du modèle exécutable.

Contenu annoncé :

- runtime ;
- code source ;
- documentation ;
- checkpoint v3 ;
- trois checkpoints v2 originaux ;
- tests ;
- manifeste d'intégrité.

Contrôles rapportés :

- 95 fichiers couverts par le manifeste ;
- environ 57,5 Mo décompressés ;
- SHA-256 conformes pour les fichiers couverts.

### 11.2. Amodel_eSonde_v3.zip

Livrable d'audit.

Contenu annoncé :

- rapports P0 à P6 ;
- journaux d'exécution ;
- incidents ;
- inventaires des sources ;
- analyse des expériences ;
- revue des manuscrits probabilistes et quantiques ;
- manifestes et éléments de preuve.

Contrôles rapportés :

- 126 fichiers couverts par le manifeste ;
- environ 23,9 Mo décompressés ;
- SHA-256 conformes pour les fichiers couverts.

### 11.3. suivi_model_eSonde_v3.zip

Livrable de suivi et de traçabilité.

Contenu annoncé :

- checklists ;
- journaux ;
- preuves ;
- incidents ;
- historique des checkpoints ;
- snapshots ;
- script de réassemblage.

Contrôles rapportés :

- 7 archives ;
- 3 800 fichiers couverts ;
- environ 4,12 Go décompressés ;
- 23 snapshots annoncés ;
- tests CRC réussis ;
- manifeste global SHA-256 vérifié après réassemblage.

**Réserve administrative :** la checklist livrée indique encore P7 comme `IN_PROGRESS`. Les contrôles d'intégrité rapportés ne justifient pas de modifier rétroactivement ce statut.

---

## 12. Protocole recommandé pour eSonde v4

La prochaine version ne doit pas commencer par l'ajout systématique de nouvelles sondes.

La priorité est de déterminer expérimentalement si les familles existantes apprennent et généralisent.

### Phase 1 — Corpus de référence

Constituer un corpus d'entraînement indépendant, multilingue, suffisamment volumineux et correctement licencié.

Documenter :

- provenance ;
- licence ;
- langues ;
- domaines ;
- volumes ;
- prétraitement ;
- déduplication ;
- séparation entraînement/validation/test.

MLQA ne doit pas être utilisé comme corpus d'entraînement sur la base de l'archive étudiée.

### Phase 2 — Évaluation individuelle

Évaluer séparément :

- SEQ ;
- SKIP_REL ;
- MORPH ;
- SEM ;
- DISC ;
- RETR ;
- BYTE.

Mesurer les performances sur plusieurs jeux indépendants.

### Phase 3 — Ablations et coordination

Comparer :

- chaque famille seule ;
- BYTE seul ;
- les meilleures combinaisons ;
- COORD ;
- les différentes stratégies de calibration.

Le gain de COORD doit être mesuré et non présumé.

### Phase 4 — Généralisation

Construire des tests avec :

- formulations inédites ;
- contextes nouveaux ;
- relations absentes du corpus ;
- sujets non rencontrés ;
- variations syntaxiques ;
- changements de domaine.

### Phase 5 — Évaluation de la compréhension

Séparer les tâches :

- prédiction du token suivant ;
- récupération d'information ;
- résolution de coréférence ;
- questions-réponses officielles ;
- raisonnement sur des données structurées.

Pour MLQA, utiliser un protocole officiel et rapporter EM et F1 lorsque la tâche évaluée est le question-réponse.

### Phase 6 — Évaluation de génération

Définir à l'avance des critères mesurables :

- fluidité ;
- répétition ;
- cohérence ;
- pertinence ;
- diversité ;
- stabilité multilingue.

Conserver les sorties brutes et les prompts pour rendre les résultats reproductibles.

### Phase 7 — Respect des invariants

Toute évolution doit préserver l'objectif architectural :

**zéro neurone, zéro MLP, zéro transformeur et aucune couche neuronale cachée.**

Les améliorations doivent être réalisées au moyen de sondes explicites, de structures statistiques, de mémoires inspectables et de mécanismes probabilistes vérifiables.

---

## 13. Verdict final

| Propriété | État |
|---|---|
| Architecture pure-sonde | Réalisée selon l'audit |
| Absence de neurones et de MLP dans le runtime examiné | Étayée par audit statique |
| Intégration BYTE | Validée par les tests rapportés |
| Migration v2 | Validée par les tests rapportés |
| Sérialisation et interfaces | Validées par les tests rapportés |
| Couverture OOV multilingue | Démontrée sur l'échantillon |
| Qualité linguistique générale | Non démontrée |
| Compréhension générale | Non démontrée |
| Raisonnement général | À expérimenter |
| Capacité généraliste compétitive | Non démontrée |

### Conclusion

eSonde v3 est une preuve de concept logicielle fonctionnelle d'une architecture de langage non neuronale à sondes explicites.

Sa valeur actuelle réside dans son architecture inspectable, sa modularité, sa gestion probabiliste et sa capacité à intégrer plusieurs mécanismes statistiques dans un runtime cohérent.

Les tests logiciels étayent le fonctionnement des composants examinés.

Les résultats linguistiques montrent toutefois que le modèle est encore très éloigné d'une compétence généraliste démontrée.

La prochaine étape scientifique n'est pas d'affirmer qu'eSonde comprend déjà le langage.

Elle consiste à lui fournir des données suffisantes, à définir des protocoles indépendants et à mesurer rigoureusement jusqu'où une architecture sans neurones peut apprendre, généraliser et produire du langage.

**eSonde v3 établit une architecture. Les prochaines expériences devront établir sa compétence.**

