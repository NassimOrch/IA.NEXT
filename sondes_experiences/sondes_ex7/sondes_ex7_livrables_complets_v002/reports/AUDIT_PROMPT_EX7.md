# Audit de conformité du prompt EX7

## Héritage du prompt EX6

- `inputs/prompt_ex6_parent.json` est l'instantané parent.
- Le champ `prompt` du fichier EX7 commence exactement par le champ `prompt` du parent : **préfixe identique, caractère par caractère**.
- Le prompt parent comporte 19 sections numérotées `## 0` à `## 18` ; elles sont conservées intégralement.
- L'addendum EX7 ajoute les sections A à L sans neutraliser les règles rouges, les interdictions anti-triche/anti-sabotage ni les règles de séparation des données.
- `schema_version=7`, JSON valide.

## Identifiants cryptographiques

- SHA-256 du texte prompt parent EX6 : `72744213da2626174e63c45256a6e7a69c6de84c2b810d7a4a94e931c885237c`.
- SHA-256 du fichier JSON `prompt_ex7.json` : `3faf35349da74b62db043e81a8889189132cc0ce6ad5e0bdc75eb068e8b066ea`.
- Date de révision : `2026-10-31` ; addendum déclaré : A–L.

## Portée scientifique de l'addendum

L'addendum impose de travailler sur la filiation micro-MIXA → OOF → Emplica/Orchestra avec correcteur OOF, et de convertir la compacité en gains mesurés. Il exige notamment des correcteurs compacts, une étude de coûts OOF 2/3/5 folds, le vectoriel et le parallélisme réel, des profils batch 1/16/64/256, une version originale récursive Emplica Orchestra Org, ses ablations, des comparateurs MLP-ge4x et des livrables intègres.

## Conclusion d'audit

Le prompt de base est préservé fidèlement. La matrice `CONFORMITE_PROMPT_EX7.md` distingue les bras exécutés et leurs résultats, les bras seulement partiellement couverts, et les éléments indisponibles ou non mesurés. Le fait qu'un bloc soit exécuté n'implique pas qu'il réussisse son critère de qualité ou de vitesse. Le verdict global demeure **INCOMPLET — DÉVELOPPEMENT UNIQUEMENT — VALIDATION EXTERNE NON ÉTABLIE**.
