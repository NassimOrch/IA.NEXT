# Formalisme ORDER80.2

## 1. État d'un nœud

Un nœud est :

\[
N=(\Gamma\vdash G, O_F, O_R, O_W, M, D, B, k),
\]

avec :

- `Γ` : contexte local ;
- `G` : objectif local ;
- `O_F` : unités formelles observées et vérifiées ;
- `O_R` : chunks documentaires observés ;
- `O_W` : pages/chunks web observés ;
- `M` : mémoire de certificats vérifiés ;
- `D` : profil du déficit de résolution ;
- `B` : ressources explicites ;
- `k` : compteur d'observation propre au nœud.

## 2. Fonction d'observation adaptative

On définit :

\[
O_{k+1}=ObserveMore(G,\Gamma,D,mode_k).
\]

avec :

\[
mode_k \in \{bootstrap,focused,expanded,broad\}.
\]

La progression des modes est monotone :

`bootstrap → focused → expanded → broad → broad → …`.

Un mode `broad` peut sélectionner une unité encore inconnue sans correspondance lexicale directe. La sélection n'est donc pas équivalente à une simple relecture de tout le corpus.

## 3. Résolution

\[
Resolve(\Gamma\vdash G,O_F,M) \to P \mid FailureProfile.
\]

Le synthétiseur produit un certificat candidat `P`. Celui-ci ne devient utilisable qu'après passage du noyau.

## 4. Décomposition récursive

\[
Decompose(N)=\{N_1,\ldots,N_m\}.
\]

Chaque `N_i` est soumis au même opérateur :

\[
Loop(N_i)=Observe\to Resolve\to ObserveMore^{*}\to Decompose^{*}.
\]

Le symbole `*` signifie répétition jusqu'à obtention d'un succès, absence de nouveau matériau accessible ou ressource explicitement atteinte.

## 5. Fermeture d'un sous-problème

Si `Γ ⊢ H` est prouvé, le moteur construit :

\[
C(Γ,H)=(\bigwedge\Gamma)\to H.
\]

Le certificat `C` est réévalué par le noyau avant admission mémoire.

## 6. Propagation

Après mise à jour `M'` :

\[
RootTest(P,O,M')
\]

est exécuté immédiatement. En cas d'échec global, des tests de propagation sur la frontière sont exécutés immédiatement :

\[
PeerProbe(N_j,O,M')\quad pour\quad N_j\in Frontier.
\]

## 7. Vérification récursive

\[
Verify(P,G,O)=PASS
\]

ssi tous les nœuds respectent la règle associée, que les hypothèses locales sont correctement déchargées, que les lemmes observés sont eux-mêmes vérifiés et qu'aucune hypothèse ouverte ne subsiste à la racine.

## 8. Séparation vérification / nouveauté

La notion de certificat et la notion de nouveauté sont distinctes.

- `VERIFIED_COMPLETE` : certificat complet accepté par le noyau ;
- `NOVEL_DEMONSTRATION` : certificat vérifié et non déjà présent selon la politique de mémoire ;
- `NOT_NOVEL` : certificat vérifié mais déjà présent selon cette politique ;
- `UNRESOLVED` : aucun certificat complet accepté pendant cette exécution.

`UNRESOLVED` n'est pas un énoncé sur la vérité ou la fausseté mathématique du but.
