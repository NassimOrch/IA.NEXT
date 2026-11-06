#!/usr/bin/env python3
"""Reproducible toy experiment: MLP neurons vs adaptive RBF probes.

Python 3; dependencies: numpy, torch, scikit-learn, matplotlib.
Writes metrics CSV, summary JSON and a decision-boundary figure next to this script.
"""
from pathlib import Path
import json, random
import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss, f1_score

OUT = Path(__file__).resolve().parent
TORCH_SEEDS = [101, 202, 303, 404, 505]
TRAIN_SEED = 20261028
TEST_SEED = 20261029
N_TRAIN = 1200
N_TEST = 4000
NOISE = 0.22
EPOCHS = 500
LR = 0.02
WEIGHT_DECAY = 1e-4
N_UNITS = 12

torch.set_num_threads(1)

class NeuralNetwork(torch.nn.Module):
    """One-hidden-layer tanh MLP: 49 trainable parameters."""
    def __init__(self):
        super().__init__()
        self.hidden = torch.nn.Linear(2, N_UNITS)
        self.output = torch.nn.Linear(N_UNITS, 1)
    def forward(self, x):
        return self.output(torch.tanh(self.hidden(x)))

class AdaptiveProbeEnsemble(torch.nn.Module):
    """12 trainable radial probes + logistic readout: 49 parameters total."""
    def __init__(self):
        super().__init__()
        self.centers = torch.nn.Parameter(torch.randn(N_UNITS, 2) * 0.6)  # 24
        self.log_widths = torch.nn.Parameter(torch.zeros(N_UNITS))        # 12
        self.weights = torch.nn.Parameter(torch.randn(N_UNITS, 1) * 0.15) # 12
        self.bias = torch.nn.Parameter(torch.zeros(1))                    # 1
    def activations(self, x):
        squared_distance = ((x[:, None, :] - self.centers[None, :, :]) ** 2).sum(dim=2)
        widths = torch.exp(self.log_widths).clamp(min=0.08, max=10.0)
        return torch.exp(-squared_distance / (2.0 * widths[None, :] ** 2))
    def forward(self, x):
        return self.activations(x) @ self.weights + self.bias

class FixedProbeEnsemble(torch.nn.Module):
    """Ablation: fixed random centers/widths; only readout (13 params) learns."""
    def __init__(self):
        super().__init__()
        self.register_buffer('centers', torch.randn(N_UNITS, 2) * 0.6)
        self.register_buffer('widths', torch.ones(N_UNITS))
        self.weights = torch.nn.Parameter(torch.randn(N_UNITS, 1) * 0.15)
        self.bias = torch.nn.Parameter(torch.zeros(1))
    def activations(self, x):
        squared_distance = ((x[:, None, :] - self.centers[None, :, :]) ** 2).sum(dim=2)
        return torch.exp(-squared_distance / (2.0 * self.widths[None, :] ** 2))
    def forward(self, x):
        return self.activations(x) @ self.weights + self.bias

def build_data():
    x_train, y_train = make_moons(n_samples=N_TRAIN, noise=NOISE, random_state=TRAIN_SEED)
    x_test, y_test = make_moons(n_samples=N_TEST, noise=NOISE, random_state=TEST_SEED)
    scaler = StandardScaler().fit(x_train)  # fit on training set only to avoid leakage
    x_train = scaler.transform(x_train).astype(np.float32)
    x_test = scaler.transform(x_test).astype(np.float32)
    tensors = (torch.tensor(x_train), torch.tensor(y_train, dtype=torch.float32).reshape(-1, 1),
               torch.tensor(x_test), torch.tensor(y_test, dtype=torch.float32).reshape(-1, 1))
    return tensors, (x_train, y_train, x_test, y_test, scaler)

def fit_one(model_class, seed, tensors, epochs=EPOCHS):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    x_train, y_train, x_test, y_test = tensors
    model = model_class()
    trainable_count = sum(p.numel() for p in model.parameters() if p.requires_grad)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    loss_fn = torch.nn.BCEWithLogitsLoss()
    losses = []
    for _ in range(epochs):
        optimizer.zero_grad()
        train_loss = loss_fn(model(x_train), y_train)
        train_loss.backward()
        optimizer.step()
        losses.append(float(train_loss.detach()))
    model.eval()
    with torch.no_grad():
        train_logits = model(x_train).numpy().ravel()
        test_logits = model(x_test).numpy().ravel()
    probs = 1.0 / (1.0 + np.exp(-np.clip(test_logits, -40, 40)))
    predictions = (probs >= 0.5).astype(int)
    metrics = {
        'accuracy': float(accuracy_score(y_test.numpy().ravel(), predictions)),
        'auc': float(roc_auc_score(y_test.numpy().ravel(), probs)),
        'log_loss': float(log_loss(y_test.numpy().ravel(), probs)),
        'f1': float(f1_score(y_test.numpy().ravel(), predictions)),
        'final_train_loss': float(loss_fn(torch.tensor(train_logits).reshape(-1, 1), y_train).item()),
        'trainable_parameters': int(trainable_count),
    }
    return model, metrics, losses, probs

def main():
    tensors, arrays = build_data()
    x_train, y_train, x_test, y_test, scaler = arrays
    model_classes = {
        'reseau_neuronal_MLP': NeuralNetwork,
        'sondes_adaptatives_RBF': AdaptiveProbeEnsemble,
        'sondes_fixes_ablation': FixedProbeEnsemble,
    }
    rows, histories, model_instances = [], {}, {}
    for name, cls in model_classes.items():
        per_seed = []
        for seed in TORCH_SEEDS:
            model, metrics, losses, probs = fit_one(cls, seed, tensors)
            row = {'model': name, 'initialization_seed': seed, **metrics}
            rows.append(row)
            per_seed.append((metrics, losses, probs))
        histories[name] = [item[1] for item in per_seed]
        model_instances[name] = [item[2] for item in per_seed]

    import csv
    csv_path = OUT / 'resultats_experience_sondes.csv'
    fieldnames = list(rows[0].keys())
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader(); writer.writerows(rows)

    metric_names = ['accuracy', 'auc', 'log_loss', 'f1', 'final_train_loss', 'trainable_parameters']
    summary = {
        'experiment': 'Comparaison réseau neuronal / ensemble de sondes adaptatives sur two moons',
        'data': {'train_samples': N_TRAIN, 'test_samples': N_TEST, 'noise': NOISE,
                 'train_data_seed': TRAIN_SEED, 'test_data_seed': TEST_SEED,
                 'standardization': 'StandardScaler ajusté uniquement sur le jeu d’entraînement'},
        'training': {'initialization_seeds': TORCH_SEEDS, 'epochs': EPOCHS, 'optimizer': 'Adam',
                     'learning_rate': LR, 'weight_decay': WEIGHT_DECAY, 'batching': 'full-batch',
                     'loss': 'binary cross-entropy with logits'},
        'metrics': {},
        'interpretation_note': 'La moyenne et l’écart-type sont calculés sur 5 initialisations du modèle, sur un jeu de test fixe. Ils mesurent surtout la sensibilité à l’initialisation, pas l’incertitude due au choix des données.'
    }
    for name in model_classes:
        subset = [r for r in rows if r['model'] == name]
        summary['metrics'][name] = {}
        for metric in metric_names:
            vals = [r[metric] for r in subset]
            summary['metrics'][name][metric] = {'mean': float(np.mean(vals)), 'sd_sample': float(np.std(vals, ddof=1)) if len(vals)>1 else 0.0}
    json_path = OUT / 'synthese_experience_sondes.json'
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')

    # Decision-boundary visualization using the first fixed seed model from each condition.
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.1), constrained_layout=True)
    names = list(model_classes.keys())
    model_labels = ['Réseau neuronal (MLP)', 'Sondes adaptatives (RBF)', 'Sondes fixes (ablation)']
    gx = np.linspace(x_test[:, 0].min()-0.3, x_test[:, 0].max()+0.3, 220)
    gy = np.linspace(x_test[:, 1].min()-0.3, x_test[:, 1].max()+0.3, 220)
    xx, yy = np.meshgrid(gx, gy)
    grid = torch.tensor(np.c_[xx.ravel(), yy.ravel()], dtype=torch.float32)
    for ax, name, label in zip(axes, names, model_labels):
        torch.manual_seed(TORCH_SEEDS[0]); np.random.seed(TORCH_SEEDS[0]); random.seed(TORCH_SEEDS[0])
        model, _, _, _ = fit_one(model_classes[name], TORCH_SEEDS[0], tensors)
        with torch.no_grad():
            pp = torch.sigmoid(model(grid)).numpy().reshape(xx.shape)
        ax.contourf(xx, yy, pp, levels=[0, .5, 1], alpha=0.22)
        ax.contour(xx, yy, pp, levels=[.5], linewidths=1.4)
        ax.scatter(x_test[:, 0], x_test[:, 1], c=y_test, s=5, alpha=.32, linewidths=0)
        ax.set_title(label, fontsize=10)
        ax.set_xlabel('x₁ standardisé')
        ax.set_ylabel('x₂ standardisé')
    fig.suptitle('Frontières de décision — illustration sur une initialisation fixe', fontsize=12)
    fig_path = OUT / 'frontieres_decision_sondes.png'
    fig.savefig(fig_path, dpi=170)
    plt.close(fig)

    print('CSV:', csv_path)
    print('JSON:', json_path)
    print('FIGURE:', fig_path)
    for name, data in summary['metrics'].items():
        print(name)
        for metric in ['accuracy','auc','log_loss','f1','final_train_loss','trainable_parameters']:
            d=data[metric]
            print(f"  {metric}: {d['mean']:.6f} ± {d['sd_sample']:.6f}")

if __name__ == '__main__':
    main()
