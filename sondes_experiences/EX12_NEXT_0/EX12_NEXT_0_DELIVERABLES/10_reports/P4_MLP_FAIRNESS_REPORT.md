# P4 — Audit d’équité du matching en paramètres entraînables

Statut : **PASS**

Paires contrôlées : 320/320.
Paires dans ±1 % : 320/320.
Recalculs de métriques de baseline liés aux 320 paires : 320/320.
Contrôles MLP P4 uniques présents et audités : 160/160.
Registre P4 : {'SUCCESS': 160, 'INTERRUPTED': 1}.

## Méthode

R0 et C2 sont comparées à M0_CORE (contrôle MLP P3 déjà apparié). C3 et C4 sont comparées aux nouveaux MLP P4 appariés sur le nombre de paramètres entraînables. Les buffers et scalaires persistants sont rapportés séparément : ils ne servent pas à déclarer l’égalité de capacité.

## Comparaisons appariées de validation

- C2 / boundary / nmae_train_scale: n=60, moyenne(candidate−MLP)=-0.0281478, médiane=-0.0100875, victoires=38, égalités=0, défaites=22.
- C2 / extrapolation / nmae_train_scale: n=60, moyenne(candidate−MLP)=0.180285, médiane=0.091576, victoires=11, égalités=0, défaites=49.
- C2 / interpolation / accuracy: n=10, moyenne(candidate−MLP)=0.01325, médiane=0.00125, victoires=5, égalités=0, défaites=5.
- C2 / interpolation / log_loss: n=10, moyenne(candidate−MLP)=0.0115573, médiane=0.0118757, victoires=3, égalités=0, défaites=7.
- C2 / interpolation / nmae_train_scale: n=60, moyenne(candidate−MLP)=-0.00798811, médiane=-0.00230398, victoires=32, égalités=0, défaites=28.
- C2 / shift / accuracy: n=10, moyenne(candidate−MLP)=0.0135, médiane=0.015, victoires=2, égalités=1, défaites=7.
- C2 / shift / log_loss: n=10, moyenne(candidate−MLP)=0.00149683, médiane=-0.00444841, victoires=6, égalités=0, défaites=4.
- C2 / shift / nmae_train_scale: n=60, moyenne(candidate−MLP)=-0.000943455, médiane=-0.00368126, victoires=36, égalités=0, défaites=24.
- C2 / validation / nmae_train_scale: n=10, moyenne(candidate−MLP)=-0.0104661, médiane=0.0131058, victoires=4, égalités=0, défaites=6.
- C3 / boundary / nmae_train_scale: n=60, moyenne(candidate−MLP)=-0.0247514, médiane=-0.000521754, victoires=30, égalités=0, défaites=30.
- C3 / extrapolation / nmae_train_scale: n=60, moyenne(candidate−MLP)=0.10406, médiane=0.0807508, victoires=17, égalités=0, défaites=43.
- C3 / interpolation / accuracy: n=10, moyenne(candidate−MLP)=-0.01575, médiane=-0.01125, victoires=7, égalités=0, défaites=3.
- C3 / interpolation / log_loss: n=10, moyenne(candidate−MLP)=0.0124412, médiane=0.00751006, victoires=3, égalités=0, défaites=7.
- C3 / interpolation / nmae_train_scale: n=60, moyenne(candidate−MLP)=0.00609018, médiane=0.00245605, victoires=28, égalités=0, défaites=32.
- C3 / shift / accuracy: n=10, moyenne(candidate−MLP)=0.0015, médiane=0.0025, victoires=5, égalités=0, défaites=5.
- C3 / shift / log_loss: n=10, moyenne(candidate−MLP)=-0.000177748, médiane=0.0044834, victoires=4, égalités=0, défaites=6.
- C3 / shift / nmae_train_scale: n=60, moyenne(candidate−MLP)=0.0150325, médiane=-0.000321769, victoires=30, égalités=0, défaites=30.
- C3 / validation / nmae_train_scale: n=10, moyenne(candidate−MLP)=-0.0079403, médiane=0.00337886, victoires=5, égalités=0, défaites=5.
- C4 / boundary / nmae_train_scale: n=60, moyenne(candidate−MLP)=0.00925267, médiane=0.00227955, victoires=29, égalités=0, défaites=31.
- C4 / extrapolation / nmae_train_scale: n=60, moyenne(candidate−MLP)=0.260536, médiane=0.0828643, victoires=15, égalités=0, défaites=45.
- C4 / interpolation / accuracy: n=10, moyenne(candidate−MLP)=-0.02275, médiane=-0.025, victoires=8, égalités=0, défaites=2.
- C4 / interpolation / log_loss: n=10, moyenne(candidate−MLP)=0.0201866, médiane=0.0165756, victoires=3, égalités=0, défaites=7.
- C4 / interpolation / nmae_train_scale: n=60, moyenne(candidate−MLP)=-0.00594661, médiane=-0.00250882, victoires=34, égalités=0, défaites=26.
- C4 / shift / accuracy: n=10, moyenne(candidate−MLP)=-0.011, médiane=-0.0125, victoires=7, égalités=0, défaites=3.
- C4 / shift / log_loss: n=10, moyenne(candidate−MLP)=0.00598062, médiane=0.00944818, victoires=3, égalités=0, défaites=7.
- C4 / shift / nmae_train_scale: n=60, moyenne(candidate−MLP)=-0.00721266, médiane=-0.00648546, victoires=39, égalités=0, défaites=21.
- C4 / validation / nmae_train_scale: n=10, moyenne(candidate−MLP)=-0.0202068, médiane=-0.00836028, victoires=7, égalités=0, défaites=3.
- R0 / boundary / nmae_train_scale: n=60, moyenne(candidate−MLP)=-0.0208343, médiane=-0.00251048, victoires=34, égalités=0, défaites=26.
- R0 / extrapolation / nmae_train_scale: n=60, moyenne(candidate−MLP)=0.18395, médiane=0.121569, victoires=10, égalités=0, défaites=50.
- R0 / interpolation / accuracy: n=10, moyenne(candidate−MLP)=-0.008, médiane=-0.01, victoires=5, égalités=0, défaites=5.
- R0 / interpolation / log_loss: n=10, moyenne(candidate−MLP)=0.0197297, médiane=0.0177731, victoires=2, égalités=0, défaites=8.
- R0 / interpolation / nmae_train_scale: n=60, moyenne(candidate−MLP)=-0.00424901, médiane=0.00250095, victoires=27, égalités=0, défaites=33.
- R0 / shift / accuracy: n=10, moyenne(candidate−MLP)=-0.0135, médiane=-0.00875, victoires=5, égalités=0, défaites=5.
- R0 / shift / log_loss: n=10, moyenne(candidate−MLP)=0.0175166, médiane=0.0122118, victoires=1, égalités=0, défaites=9.
- R0 / shift / nmae_train_scale: n=60, moyenne(candidate−MLP)=0.00125471, médiane=-0.000360854, victoires=30, égalités=0, défaites=30.
- R0 / validation / nmae_train_scale: n=10, moyenne(candidate−MLP)=-0.00982793, médiane=-0.00296206, victoires=6, égalités=0, défaites=4.

## Interruption conservée

Le run `P4_g6_log_quadratic_rational_s934109236_M0_C4_TRAINABLE_A01` est conservé comme interruption : `run_metadata.json` reste à STARTED, avec seulement `config.json, run_metadata.json`. Aucun checkpoint ni prédiction n’existe. La reprise réussie est `P4_g6_log_quadratic_rational_s934109236_M0_C4_TRAINABLE_A02`.

## Limites

Ces comparaisons portent exclusivement sur train/validation. Aucun test ni holdout n’a été consulté. Les résultats sont exploratoires ; ils ne prouvent ni supériorité générale ni non-infériorité confirmatoire.

## Erreurs de l’audit

Aucune divergence détectée.
