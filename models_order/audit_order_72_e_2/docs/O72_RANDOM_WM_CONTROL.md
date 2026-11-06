# Random WM control

Three compatible attention WMs are fresh random initializations and never trained.

Hashes:

- seed 7207201: `3b8fa668d5c69480140fb0faae9dc61a7d34cf5dd2600a558b6e78bb36f7c87b`
- seed 7207202: `b2db27ad8e5c65ecb7765e9e6fefae1bf89d32ddaf1566360b344be2050279dd`
- seed 7207203: `0f340546979921d56c0277d639d3403653fc8cb1b205fb5a2212cd916c2c7ae7`

The control uses the same O72 e1 code, budget, verifier and environments. It changes the WM, not the controller.

The control succeeds 24/24 exact cases and 12/12 open cases in the final campaign.
