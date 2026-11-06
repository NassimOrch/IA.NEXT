# Architecture ORDER80.2

```text
                        ┌────────────────────────┐
                        │       Tâche Γ ⊢ G       │
                        └────────────┬───────────┘
                                     │
                           ┌─────────▼─────────┐
                           │ Adaptive Engine    │
                           │ node-local loop    │
                           └───────┬────────────┘
                                   │
                 ┌─────────────────┼──────────────────┐
                 │                 │                  │
          Formal observer   Research observer   Web observer
          theorem units      chunk units          page/chunks
                 │                 │                  │
                 └────────────┬────┴───────┬──────────┘
                              │            │
                       Proof candidates  documentary context
                              │            │
                              ▼            │
                       Proof Synthesizer  │
                              │            │
                              ▼            │
                         Proof Kernel ◄────┘
                              │
                      verified certificate
                              │
                              ▼
                       Persistent Memory
                         │           │
                    root retest   peer probes
                         │           │
                         └─────┬─────┘
                               ▼
                        Recursive tree
                         node ↺ observe
                              resolve
                              decompose
```

## Principes

1. **Chaque nœud est autonome dans son cycle de recherche.** Le compteur d'observation est local au nœud ; le compteur global sert à l'audit.
2. **L'observation est progressive.** Les niveaux `bootstrap`, `focused`, `expanded`, `broad` permettent d'élargir la couverture.
3. **Le formel et le documentaire sont séparés.** Un texte de recherche, une page web ou une source de bibliothèque non certifiée ne devient pas un axiome.
4. **Le noyau est indépendant du générateur.** Un certificat doit fermer toutes ses obligations et ses lemmes sont revalidés.
5. **La propagation est immédiate.** Toute preuve locale ferme le séquent, met à jour la mémoire, reteste la racine et sonde les autres nœuds en attente.
