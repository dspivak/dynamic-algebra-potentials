"""Distributed partial observability: per-box views of the world (Task 2).

The ``M`` weather modes are partitioned into ``N`` disjoint groups, one per box, so
that each box senses a *different* slice of the world and pooling boxes adds genuine
information.  ``partition_modes`` returns the raw per-box modes (used by the decode
diagnostic -- the information physically available to a box); ``embed_views`` encodes
each box's slice into the residual width ``R^E`` the KQV boxes consume.

Nothing here is in the suboperad -- it is the environment's sensory interface.
"""

from __future__ import annotations

from typing import List

import numpy as np


def partition_modes(obs: np.ndarray, N: int) -> List[np.ndarray]:
    """Split the ``M`` weather modes into ``N`` disjoint per-box slices.

    ``obs`` is ``(T, M)``; returns a list of ``N`` arrays ``(T, |group_i|)``.  Each box
    sees a different, non-overlapping subset of the modes (so pooling adds info).
    """
    M = obs.shape[1]
    if N > M:
        raise ValueError(f"need at least one mode per box: N={N} > M={M}")
    groups = np.array_split(np.arange(M), N)
    return [obs[:, g] for g in groups]


def sense(obs: np.ndarray, N: int, *, noise: float, seed: int) -> List[np.ndarray]:
    """Per-box *noisy* observations: each box's mode-slice plus independent sensor noise.

    The independent noise is the observation/sensor model (this layer, not the world
    dynamics, which stays a pure Phiphase oscillator).  It is what makes a single box's
    view genuinely insufficient -- pooling averages independent noise away -- so the
    necessary-communication regime does not rest on linear observability alone.
    """
    views = partition_modes(obs, N)
    rng = np.random.default_rng(seed)
    return [v + rng.standard_normal(v.shape) * noise for v in views]


def embed_views(views: List[np.ndarray], E: int, *, seed: int) -> List[np.ndarray]:
    """Encode each box's raw modes into the residual width ``R^E`` (a fixed sensor).

    A fixed random linear map per box -- the box's "sensory transduction" -- producing
    the ``(T, E)`` stream fed to that box as its source emission.
    """
    rng = np.random.default_rng(seed)
    out = []
    for v in views:
        k = v.shape[1]
        W = rng.standard_normal((k, E)) / np.sqrt(k)
        out.append(v @ W)
    return out
