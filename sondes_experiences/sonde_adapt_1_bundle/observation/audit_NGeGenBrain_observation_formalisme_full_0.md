# Audit de consolidation — NGeGenBrain_observation_formalisme_full_0

## 1. Périmètre et sources

La refonte se fonde sur trois sources LaTeX exactes, dont tous les chapitres sont tracés :

| Source | Taille (octets) | Chapitres | Rôle |
|---|---:|---:|---|
| `NGeGenBrain_observation_formalisme.tex` | 88 984 | 25 | Fondations : observations, sondes, empreintes, seuils, expérience et audit du pipeline |
| `NGeGenBrain_observation_formalisme_next_0.tex` | 78 773 | 21 | Problème inverse : classes de mécanismes compatibles, identification, reconstruction et composition |
| `NGeGenBrain_observation_formalisme_next_1.tex` | 32 146 | 12 | Décomposition invariant/variant, information résiduelle, multi-échelle et temps |
| **Total** | **199 903** | **58** | |

Aucun fichier distinct `NGeGenBrain_observation_formalisme_0.tex` n’était présent dans le workspace; aucune source inexistante n’a été inventée. Le document `next_1` a été inclus parce qu’il porte la formalisation invariant/variant, la reconstruction temporelle et la précision sur l’invariance contextuelle.

## 2. Décisions conceptuelles principales

- **Empreinte et dossier d’évidence sont des objets différents.** L’empreinte est une application (ou famille d’applications) calculée par un protocole; le dossier conserve données, contextes, interventions, incertitudes et provenance.
- **Invariance contextuelle : distinction corrigée.** Pour une famille fixe de sondes et un contexte fixe, la signature est bien définie et constante sur ses propres fibres d’indiscernabilité. Cela ne prouve pas qu’elle soit préservée par une transformation de l’objet ou un changement de contexte. L’invariance sous une famille de transformations exige une égalité explicite, avec quantificateurs et domaine.
- **Information stable, variable et temporelle : pas de décomposition gratuite.** Une empreinte générale n’est pas nécessairement invariante; une empreinte volontairement invariantielle peut perdre des variantes. La décomposition invariant/variant n’est pas unique sans contrainte d’identifiabilité.
- **Reconstruction exacte, génération conditionnelle et identification sont séparées.** L’injectivité donne un critère exact de reconstruction de l’enregistrement; un ensemble de mécanismes compatibles n’est pas une preuve d’unicité.
- **Temps et multi-échelle sont distincts.** Le protocole distingue échelles instrumentales, familles de sondes, contexte, intervention, histoire, horloges et pertes d’événements. Une trace échantillonnée ne détermine pas un signal arbitraire entre les échantillons.
- **Les interventions sont définies par le protocole.** Une différence après intervention n’identifie pas à elle seule un mécanisme causal complet.
- **Les résultats empiriques sont relatifs au domaine testé.** Le chapitre sur le logiciel v3.1 est explicitement un audit historique repris de la source, pas une nouvelle exécution du logiciel.

## 3. Corrections mathématiques opératoires

1. Le théorème de reconstruction précise que l’inverse est défini sur l’image `I(Y)`, c’est-à-dire sur les signatures effectivement produites; une extension à toutes les valeurs de codomaine non atteintes n’est pas nécessaire.
2. Un exemple temporel a été corrigé pour démontrer l’invariance sous une action d’état non triviale sans assimiler invariance et constance dans le temps.
3. Une proposition explicite distingue l’invariance sous transformations de la simple constance sur les fibres d’une signature à contexte fixé, avec contre-exemple.
4. Les conditions nécessaires à une décomposition additive unique et à la reconstruction des variantes sont déclarées, au lieu d’être supposées.
5. La classe de mécanismes, le protocole, les échelles, les transformations, les critères de compatibilité et le domaine de validité doivent être nommés; si l’identifiabilité échoue, plusieurs candidats restent dans l’ensemble inverse.

## 4. Traçabilité et contrôles structurels

Le maître contient :

- 8 parties et 51 chapitres;
- 94 définitions et 3 environnements d’hypothèse explicite;
- 81 énoncés de type théorème/proposition/lemme/corollaire et 81 environnements de démonstration correspondants;
- 58 lignes de traçabilité, une pour chaque chapitre des sources.

L’égalité du nombre d’énoncés et de preuves est un contrôle structurel, non une certification de validité logique. Les démonstrations héritées ont été réordonnées/harmonisées et des incohérences identifiées ont été corrigées, mais la livraison n’est pas une revue indépendante ligne par ligne par des mathématiciens externes ni une certification par assistant de preuve.

## 5. Compilation et validation

- Compilation maître par `latexmk -pdf -interaction=nonstopmode -halt-on-error` : code de sortie 0.
- PDF maître : 109 pages A4; `next_1` autonome : 21 pages.
- Aucun `LaTeX Error`, `Undefined control sequence`, référence non résolue ou `Overfull \\hbox` dans les journaux finaux.
- Des avertissements typographiques `Underfull \\hbox` subsistent dans certains blocs étroits; ils sont rapportés comme avertissements de mise en page, pas comme erreurs de compilation.
- Les empreintes SHA-256 finales sont enregistrées dans les fichiers de sommes de contrôle. Le bundle contient les sources et les scripts nécessaires à la régénération.

## 6. Limites scientifiques

La théorie formule les conditions permettant de construire une empreinte, de définir une invariance, d’identifier les variantes et de rechercher un mécanisme exécutable. Elle ne démontre pas qu’un LLM arbitraire est reconstructible exactement à partir d’un nombre fini de mesures. Cette conclusion dépend de la classe de mécanismes, des sondes, des interventions, des budgets, des hypothèses de régularité et de l’identifiabilité. Les résultats conditionnels restent conditionnels; le statut « non identifiable avec les données présentes » est un résultat acceptable et ne doit pas être remplacé artificiellement par un mécanisme unique.
