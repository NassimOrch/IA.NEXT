"""Numerical kernels for the EX12 HC-RBF P1 implementation tests.

The reference implementation deliberately uses an explicit center loop. The
optimized implementation uses batched matrix products. No model training is
performed in this module.
"""
from __future__ import annotations
import math
import torch
from torch import nn


def squared_distances_reference(z: torch.Tensor, centers: torch.Tensor,
                                precision: torch.Tensor) -> torch.Tensor:
    """Per-center diagonal Mahalanobis distances using an explicit loop."""
    if z.ndim != 2 or centers.ndim != 2 or precision.shape != centers.shape:
        raise ValueError("expected z[B,D], centers[K,D], precision[K,D]")
    if z.shape[1] != centers.shape[1]:
        raise ValueError("latent dimensions differ")
    return torch.stack([
        ((z - centers[k].unsqueeze(0)).square() * precision[k].unsqueeze(0)).sum(-1)
        for k in range(centers.shape[0])
    ], dim=1)


def squared_distances_vectorized_broadcast(z: torch.Tensor, centers: torch.Tensor,
                                           precision: torch.Tensor) -> torch.Tensor:
    """Vectorized direct-difference kernel; avoids per-center Python loops and
    retains the reference path's subtraction/square/reduction arithmetic.
    """
    if z.ndim != 2 or centers.ndim != 2 or precision.shape != centers.shape:
        raise ValueError("expected z[B,D], centers[K,D], precision[K,D]")
    if z.shape[1] != centers.shape[1]:
        raise ValueError("latent dimensions differ")
    delta = z.unsqueeze(1) - centers.unsqueeze(0)
    return (delta.square() * precision.unsqueeze(0)).sum(dim=-1)


def squared_distances_vectorized_identity64(z: torch.Tensor, centers: torch.Tensor,
                                            precision: torch.Tensor) -> torch.Tensor:
    """Batched-matmul identity with float64 accumulation to reduce cancellation.

    The output is cast to the input dtype; the accumulation cost is measured.
    """
    if z.ndim != 2 or centers.ndim != 2 or precision.shape != centers.shape:
        raise ValueError("expected z[B,D], centers[K,D], precision[K,D]")
    if z.shape[1] != centers.shape[1]:
        raise ValueError("latent dimensions differ")
    zd, cd, pd = z.to(torch.float64), centers.to(torch.float64), precision.to(torch.float64)
    weighted_z2 = zd.square() @ pd.transpose(0, 1)
    cross = zd @ (cd * pd).transpose(0, 1)
    center_term = (cd.square() * pd).sum(dim=1).unsqueeze(0)
    return (weighted_z2 - 2.0 * cross + center_term).clamp_min(0.0).to(dtype=z.dtype)


def squared_distances_vectorized(z: torch.Tensor, centers: torch.Tensor,
                                 precision: torch.Tensor) -> torch.Tensor:
    """Default fast, numerically reference-matched vectorized implementation."""
    return squared_distances_vectorized_broadcast(z, centers, precision)

def gaussian_activations(d2: torch.Tensor) -> torch.Tensor:
    return torch.exp(-0.5 * d2)


def normalize_activations(phi: torch.Tensor, eps: float = 1e-12) -> torch.Tensor:
    return phi / phi.sum(dim=-1, keepdim=True).clamp_min(eps)


def affine_rbf_readout(z: torch.Tensor, phi: torch.Tensor,
                       affine_w: torch.Tensor, affine_b: torch.Tensor,
                       rbf_w: torch.Tensor, rbf_b: torch.Tensor) -> torch.Tensor:
    return z @ affine_w + affine_b + phi @ rbf_w + rbf_b


def low_rank_modulation(z: torch.Tensor, embeddings: torch.Tensor,
                        U: torch.Tensor, a: torch.Tensor, Wc: torch.Tensor,
                        ws: torch.Tensor, wg: torch.Tensor,
                        alpha_c: float = 0.0, alpha_sigma: float = 0.0,
                        alpha_gamma: float = 0.0):
    """Input-conditioned bounded low-rank center/width/gain modulation."""
    q = torch.tanh(z @ U + a)                 # [B,R]
    mix = embeddings.unsqueeze(0) * q.unsqueeze(1)  # [B,K,R]
    delta_c = alpha_c * (mix @ Wc.transpose(0, 1))   # [B,K,D]
    delta_log_sigma = alpha_sigma * (mix * ws).sum(-1)  # [B,K]
    gamma = 1.0 + alpha_gamma * torch.tanh((mix * wg).sum(-1))
    return delta_c, delta_log_sigma, gamma


class ThreeRoundMessagePassing(nn.Module):
    """P1 cost reference matching the operation pattern of ARCH_UP_TEST_1 B4."""
    def __init__(self, latent_dim: int, n_centers: int, fp_dim: int,
                 hidden: int = 16, rounds: int = 3, seed: int = 0):
        super().__init__()
        if rounds != 3:
            raise ValueError("P1 reference is fixed to three rounds")
        self.n_centers = n_centers
        self.hidden = hidden
        self.node_encoder = nn.Linear(latent_dim + 2 + fp_dim, hidden)
        self.message_layers = nn.ModuleList([nn.Linear(hidden, hidden, bias=False) for _ in range(rounds)])
        g = torch.Generator().manual_seed(seed)
        adj = torch.rand((n_centers, n_centers), generator=g) < 0.35
        adj = torch.triu(adj, diagonal=1)
        adj = adj | adj.T
        adj.fill_diagonal_(True)
        self.register_buffer("mask", adj)

    def forward(self, rel: torch.Tensor, dist: torch.Tensor,
                phi: torch.Tensor, fingerprints: torch.Tensor) -> torch.Tensor:
        # rel[B,K,D], dist[B,K], phi[B,K], fp[K,F]
        fp = fingerprints.unsqueeze(0).expand(rel.shape[0], -1, -1)
        node_in = torch.cat([rel, dist.unsqueeze(-1), phi.unsqueeze(-1), fp], dim=-1)
        h = torch.tanh(self.node_encoder(node_in))
        for layer in self.message_layers:
            scores = (h @ h.transpose(1, 2)) / math.sqrt(self.hidden)
            scores = scores.masked_fill(~self.mask.unsqueeze(0), -1e9)
            attn = torch.softmax(scores, dim=-1)
            message = attn @ h
            h = torch.tanh(h + layer(message))
        return h


def hc_forward(x: torch.Tensor, encoder_w: torch.Tensor, encoder_b: torch.Tensor,
               centers: torch.Tensor, precision: torch.Tensor,
               affine_w: torch.Tensor, affine_b: torch.Tensor,
               rbf_w: torch.Tensor, rbf_b: torch.Tensor,
               method: str = "reference") -> torch.Tensor:
    z = torch.tanh(x @ encoder_w.transpose(0, 1) + encoder_b)
    if method == "reference":
        d2 = squared_distances_reference(z, centers, precision)
    elif method == "vectorized":
        d2 = squared_distances_vectorized(z, centers, precision)
    elif method == "identity64":
        d2 = squared_distances_vectorized_identity64(z, centers, precision)
    else:
        raise ValueError("method must be reference or vectorized")
    phi = gaussian_activations(d2)
    return affine_rbf_readout(z, phi, affine_w, affine_b, rbf_w, rbf_b)
