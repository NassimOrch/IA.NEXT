# AUDIT_SOURCES_EX6

Date de l'audit : 2026-10-31  
Archive source : `last_sources.zip`  
SHA-256 : `5f7a86cb3875f97324f75c46e379b6639673dfe9cc265a173fa8749f1be0f8eb`  
Taille : 457 109 554 octets

## 1. Intégrité et inventaire

L'archive externe contient :
- `prompt_ex3.json` et `debrit_0.txt` ;
- `sonde_adapt_global_research_final.zip` ;
- `sondes_research_workspace_final.zip` ;
- `sources_ng_adapt_0.zip` ;
- `sondes_ex4_workspace_20261030.zip` ;
- `sondes_ex5_workspace_20261030.zip`.

Les cinq ZIP principaux ont passé `ZipFile.testzip()` sans membre corrompu. Les 12 ZIP internes trouvés dans `sources_ng_adapt_0.zip` ont également passé le contrôle CRC, dont `sonde_adapt_1_bundle.zip`, les deux bundles de sondes adaptatives, le bundle d'observation, les archives NGeGenBrain et le ZIP SMS. Les tailles, nombres de membres, SHA-256 et résultats CRC sont consignés dans `checksums/source_manifest.json`.

Les archives ont été conservées comme références immuables ; le workspace EX6 est séparé. Les chemins extraits et les copies utiles sont répertoriés dans le manifeste.

## 2. Ordre de priorité retenu

1. `sondes_ex5_workspace_20261030.zip` : dernière campagne historique, référence prioritaire pour les règles les plus récentes et les résultats OOF/alternance/correction.
2. `sondes_ex4_workspace_20261030.zip` : règles de comptage, splits, micro-MIXA, comparaison MLP et traçabilité.
3. `sondes_research_workspace_final.zip` : état des recherches et candidats antérieurs.
4. `sonde_adapt_global_research_final.zip` : travaux sur adaptation globale, effets de coordination et formalisation.
5. `sources_ng_adapt_0.zip` : théorie générale, observation, premiers bundles de sondes, NGeGenBrain et datasets.
6. `debrit_0.txt` : matériau de réflexion ancien ; conservé, mais non utilisé comme preuve d'un résultat.

## 3. Lecture des prompts historiques

### EX3
EX3 pose la recherche de sondes adaptatives compactes et l'exploration de variantes, dont RETRO et MIXA, avec comparaison à des MLP. Il fournit la genèse de la méthode et le cadre expérimental initial. Ses résultats ne sont pas utilisés comme verdict actuel sans reprise de leurs artefacts.

### EX4
EX4 renforce la reconstruction des candidats et le comptage complet `P_total`, ajoute les variantes micro-MIXA et la distinction entre développement, adaptation, validation et test. Il impose une comparaison appariée aux MLP et clarifie que des résultats historiques ou des tests déjà consultés ne peuvent pas être présentés comme confirmatoires.

### EX5
EX5 ajoute les règles les plus strictes sur la consommation réelle de ressources, les paramètres fixes/gelés/buffers/prétraitement, les coûts de déploiement, les splits scellés, les corrections OOF, l'alternance de rôles et l'audit d'optimiseur. Les critères sont conjonctifs : une diminution du nombre de paramètres ne compense ni une latence supérieure, ni un entraînement plus lent, ni une dégradation prédictive.

## 3 bis. Empreintes des prompts historiques

| Fichier | Taille (octets) | SHA-256 |
|---|---:|---|
| `prompt_ex3.json` | 54 789 | `d4e1b25768703abd074b4b8cb41aa50190fda50076efce3c62e056c7c02933be` |
| `prompt_ex4.json` | 73 879 | `39471af7dabb7ad80a6379b6c2d2cc53a41d8a35af6369c344b82bd1546b36d4` |
| `prompt_ex5.json` | 68 019 | `88f67fc34bf34c5ca0817da42a057ed71dfb092cfb33720be5532da96bab3291` |

Le prompt EX6 final est la révision 1.0.1 ; son empreinte figure dans `AUDIT_PROMPT_EX6.md` et `checksums/source_manifest.json`.

## 4. Formalismes théoriques

Les quatre textes copiés sous `inputs/reference_theory/` ont été considérés comme fondement conceptuel :
- théorie générale des empreintes ;
- formalisme de l'observation ;
- étude/formalisme de la sonde adaptative ;
- formalisme de l'adaptation globale.

La distinction utile pour EX6 est entre paramètres locaux des experts (`theta`), coordination globale interne (`phi`), adaptation globale externe (`psi`) et états de procédure/optimiseur/synchronisation/RNG/provenance (`s`). Les formalismes motivent ces niveaux, mais ne prouvent pas empiriquement qu'une composition de couches sera plus rapide ou meilleure. Leurs hypothèses mathématiques doivent être séparées des mesures de code réel.

## 5. Résultats historiques déterminants

Les résultats EX5 existants montrent le piège de l'optimisation d'un seul axe. Pour la sonde OOF adaptative de référence, les moyennes historiques rapportées sur cinq graines sont environ :
- `P_total` sonde : 1 160 ; MLP-ge4x : 4 649 ;
- accuracy validation : 97,65 % vs 98,59 % ;
- log-loss : 0,05218 vs 0,05037 ;
- temps de pipeline rapporté : 2,138 s vs 0,268 s ;
- latence batch 1 p50 : 0,341 ms vs 0,0166 ms.

La sonde satisfait le ratio de paramètres, mais pas les objectifs de qualité et de vitesse. Les historiques d'alternance A/B et des variantes Q-only/PCA-Q donnent des signaux similaires : certaines économies de capacité/opérations n'ont pas produit une accélération de bout en bout et/ou dégradent la qualité.

Le chiffre de log-loss 0,05218 est une moyenne de cinq graines. Pour la graine 1501, la valeur de son checkpoint est 0,07835. Cette différence est expliquée dans les notes de résultats ; elle ne doit pas être interprétée comme une incohérence du checkpoint.

## 6. Limites des données historiques

Le dataset Wisconsin utilisé dans le pilote EX6 est le split historique de développement `v009` : train 341, validation 85, adaptation 57, test historique 86. Les partitions test liées à EX2–EX5 sont historiquement exposées et ne conviennent pas à une validation confirmatoire vierge.

Dans le pilote EX6, les lignes test n'ont pas été utilisées pour l'entraînement, la sélection, le réglage, le calcul de métriques ou le choix d'activation. Néanmoins, le chargeur fondé sur `sklearn.load_breast_cancer()` matérialise le dataset source complet en mémoire et lit les identifiants de test pour vérifier la disjonction des indices. Le protocole n'atteint donc pas le niveau d'isolation d'un chargeur strict qui n'exposerait que les partitions autorisées. Ce pilote est classé **développement historique uniquement** ; aucune revendication confirmatoire ou de généralisation vierge n'est permise.

Les essais antérieurs d'autres datasets (Digits, Wine, SMS, Banknote, MAGIC, etc.) sont également historiques/exposés ou incomplets. Les erreurs DNS/téléchargement rapportées ne sont pas transformées en résultats négatifs.

## 7. Conclusion de l'audit des sources

Les sources sont accessibles et leur intégrité ZIP vérifiée. Les règles méthodologiques EX5 prévalent lorsqu'elles précisent EX4/EX3. Les développements historiques justifient d'étudier Replica et les deux architectures Emplica, mais ne préjugent pas du résultat. Le workspace EX6 repart des scripts/checkpoints vérifiables, sans écraser les sources originales.
