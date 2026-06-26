"""The necessary-communication gate (Task 2).

Before any learning, verify the world is in the regime that makes communication
*necessary*: a single box cannot decode the season ``s`` from its own slice, but the
pooled boxes can.  We use an oracle linear decoder with a temporal window (so the
single box gets a fair chance to average its fast modes over time) and an honest
train/test split (fit on the first part, score R^2 on the held-out tail).

PASS = best-single-box R^2 is low AND pooled R^2 is high.  If it fails, the world is
misconfigured for the experiment and Task 3 would be meaningless -- this is the gate.
"""

from __future__ import annotations

from typing import List

import numpy as np


def _windowed(X: np.ndarray, window: int) -> np.ndarray:
    """Stack the last ``window`` frames at each time: ``(T, k) -> (T-window+1, k*window)``."""
    T = X.shape[0]
    return np.stack([X[i : i + window].reshape(-1) for i in range(T - window + 1)])


def _decode_r2(
    X: np.ndarray, s: np.ndarray, window: int, train_frac: float = 0.6, ridge: float = 10.0
) -> float:
    """Held-out R^2 of a *standardized ridge* linear (FIR) decode of ``s`` from ``X``.

    Standardizing the windowed features and ridge-regularizing keeps the decode
    honest and well-conditioned regardless of feature count, so the single-box and
    pooled scores are apples-to-apples (same decoder, same regularization) rather
    than an artifact of overfitting the higher-dimensional pooled features.
    """
    F = _windowed(X, window)
    y = s[window - 1 :]
    n = len(y)
    ntr = int(n * train_frac)
    Ftr, Fte = F[:ntr], F[ntr:]
    mu, sd = Ftr.mean(0), Ftr.std(0) + 1e-9
    Ftr = (Ftr - mu) / sd
    Fte = (Fte - mu) / sd
    ymu = float(y[:ntr].mean())
    k = Ftr.shape[1]
    coef = np.linalg.solve(Ftr.T @ Ftr + ridge * np.eye(k), Ftr.T @ (y[:ntr] - ymu))
    pred = Fte @ coef + ymu
    yte = y[ntr:]
    ss_res = float(np.sum((yte - pred) ** 2))
    ss_tot = float(np.sum((yte - yte.mean()) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0


def decode_gate(
    s: np.ndarray,
    views: List[np.ndarray],
    *,
    window: int = 12,
    single_max: float = 0.5,
    pooled_min: float = 0.85,
) -> dict:
    """The gate: best single-box vs pooled decode of the season.

    Returns ``{single, pooled, gap, pass}``.  ``pass`` is true iff the best single box
    decodes ``s`` poorly (``< single_max``) while the pool decodes it well
    (``> pooled_min``) -- i.e. communication across boxes is *necessary*.
    """
    singles = [_decode_r2(v, s, window) for v in views]
    single = float(max(singles))
    pooled = _decode_r2(np.concatenate(views, axis=1), s, window)
    return {
        "single": single,
        "pooled": pooled,
        "gap": pooled - single,
        "singles": [float(x) for x in singles],
        "pass": bool(single < single_max and pooled > pooled_min),
    }
