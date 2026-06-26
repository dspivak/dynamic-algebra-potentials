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
    window: int = 10,
    best_max: float = 0.45,
    typical_max: float = 0.40,
    pooled_min: float = 0.68,
    margin_min: float = 0.25,
) -> dict:
    """The (strong) necessary-communication gate: NO single box decodes ``s``, the pool does.

    This is the *every-box* reading of PLAN.md's "no single slice determines ``s``":
    even the **best** single box must decode poorly (``best_single < best_max``), the
    pool must decode it (``pooled > pooled_min``), and the pool must beat even the
    luckiest box by a clear margin (``pooled - best_single > margin_min``).  The
    typical (median) box is reported too.

    Two limitations stated, not hidden:
    1. Suppressing even the best box requires enough independent sensor noise that the
       pooled level sits near the noise floor (~0.76), so ``pooled_min`` is set
       accordingly -- an honest high-noise distributed-sensing regime, not a low-noise
       one where the pool would reach ~0.9.
    2. Necessity is **relative to the decoder's temporal window**.  The season is a
       slow *periodic* signal, so a single sensor with a long enough memory can
       temporally extrapolate it (best_single climbs with ``window``).  The default
       ``window=10`` is matched to the experiment's SHORT-MEMORY boxes (per-step
       spatial attention, no long temporal accumulator); for them communication is
       genuinely necessary.  A decoder-window-robust world would need an *aperiodic*
       (chaotic) season -- a future option, see ``test_world.py``.
    """
    singles = sorted(_decode_r2(v, s, window) for v in views)
    median_single = float(singles[len(singles) // 2])
    best_single = float(singles[-1])
    pooled = float(_decode_r2(np.concatenate(views, axis=1), s, window))
    return {
        "best_single": best_single,
        "median_single": median_single,
        "pooled": pooled,
        "margin": pooled - best_single,
        "pass": bool(
            best_single < best_max
            and median_single < typical_max
            and pooled > pooled_min
            and pooled - best_single > margin_min
        ),
    }
