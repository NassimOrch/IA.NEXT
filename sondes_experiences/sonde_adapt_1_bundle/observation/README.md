# NGeGenBrain — formalisme unifié de l’observation et de la reconstruction

## Livrables

- `NGeGenBrain_observation_formalisme_full_0.tex` : source LaTeX maître refondue et harmonisée.
- `NGeGenBrain_observation_formalisme_full_0.pdf` : PDF final compilé, 109 pages A4.
- `NGeGenBrain_observation_formalisme_next_1.tex` et `.pdf` : suite autonome sur l’invariance contextuelle, l’information résiduelle, le temps et la décomposition invariant/variant.
- `sources/NGeGenBrain_observation_formalisme.tex` : source fondatrice.
- `sources/NGeGenBrain_observation_formalisme_next_0.tex` : formalisme du problème inverse et de la reconstruction mécaniste.
- `sources/NGeGenBrain_observation_formalisme_next_1.tex` : source corrigée de la suite invariant/variant incluse dans le maître.
- `audit_NGeGenBrain_observation_formalisme_full_0.md` : audit des corrections, validations et limites.
- `traceabilite_NGeGenBrain_observation_formalisme_full_0.csv` : traçabilité de tous les chapitres source.
- `verification_NGeGenBrain_observation_formalisme_full_0.json` : résultats structurels et empreintes.
- `verify_NGeGenBrain_observation_formalisme_full_0.py` : vérificateur structurel.
- `build_NGeGenBrain_observation_formalisme_full_0.py` : génération du maître et des registres depuis les sources archivées.
- `compile_final.log`, `compile_next_1_final.log` : journaux LaTeX finaux.
- `checksums.sha256` : sommes de contrôle internes du bundle, hors ce fichier lui-même.

## Organisation théorique

La théorie distingue l’observation, l’enregistrement, l’empreinte relative à un protocole, l’invariant relatif à une famille de transformations déclarée, la composante variable/résiduelle, la trace temporelle, le dossier d’évidence, le mécanisme candidat, le mécanisme exécutable et la validation indépendante. Elle couvre les échelles de sondes, les vues complémentaires, l’observation continue, les interventions, l’identifiabilité, le problème inverse, la composition hiérarchique récursive, l’incertitude et la provenance.

**Précision sur l’invariance.** Pour un objet, un contexte et une famille de sondes fixés, l’empreinte est une signature bien définie et constante sur les fibres d’indiscernabilité qu’elle induit. Cette constance par définition n’implique pas que la signature soit préservée sous une transformation de l’objet ou un changement de contexte. Une « invariance contextuelle » doit donc déclarer son ensemble de contextes et démontrer l’égalité correspondante.

Une empreinte seule ne permet généralement pas de reconstruire une observation complète si elle a éliminé des variantes pertinentes. Le problème inverse produit alors un ensemble de mécanismes compatibles, sauf si des hypothèses d’identifiabilité explicitement satisfaites permettent d’isoler une classe ou un mécanisme.

## Sources et traçabilité

Les trois sources archivées contiennent respectivement 25, 21 et 12 chapitres, soit 58 chapitres au total. Tous sont affectés au corps argumentatif ou aux annexes, avec une ligne par chapitre dans la matrice CSV. Aucun fichier distinct nommé `NGeGenBrain_observation_formalisme_0.tex` n’a été trouvé; aucun contenu manquant n’a été inventé. `next_1` est inclus parce qu’il formalise l’idée invariant/variant et les échelles d’observation.

## Reproduction

Prérequis : Python 3 et une distribution TeX avec `latexmk`/`pdflatex` et les paquets usuels utilisés par le préambule.

```bash
python build_NGeGenBrain_observation_formalisme_full_0.py
mkdir -p build
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build NGeGenBrain_observation_formalisme_full_0.tex
python verify_NGeGenBrain_observation_formalisme_full_0.py
```

Le script de génération reconstruit le `.tex` maître et les registres depuis les fichiers sous `sources/`. La compilation PDF est une étape distincte.

## Résultats structurels et limites

Le document maître contient 51 chapitres, 8 parties, 94 définitions, 3 environnements d’hypothèse explicite et 81 énoncés de type théorème/proposition/lemme/corollaire avec 81 environnements de démonstration correspondants. Les 58 chapitres source sont tracés. Ces comptes sont structurels; l’égalité du nombre d’énoncés et de preuves ne certifie pas automatiquement les preuves.

La compilation finale réussit sans erreur LaTeX, sans commande indéfinie, référence non résolue ni débordement horizontal; des avertissements `Underfull \\hbox` restent présents dans certains blocs étroits. Cette refondation n’est pas une certification par assistant de preuve ni une revue mathématique indépendante externe. Les hypothèses conditionnelles et les limites d’identifiabilité demeurent explicites.
