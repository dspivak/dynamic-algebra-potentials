"""Couple the world to a box (Task 2): the environment driving an open KQV term.

The world's per-box observations are embedded to ``R^E`` and fed as the open KQV
term's SOURCE EMISSIONS (``in_pos``), exactly as dap streams training data into a
learner.  For Task 2 this just demonstrates the plumbing runs and stays finite; the
capacity-bounded learning and the controls are Task 3.

Provenance (AUDIT.md C0): this interprets ONLY ``system.arrangement`` and never
constructs a ``SmoothArrangement`` -- so the box it drives still provably factors
through the KQV suboperad.
"""

from __future__ import annotations

from typing import List

import jax.numpy as jnp
import numpy as np

from dap.functors import Phiconf
from dap.interpretation import trivial_omega

from .observe import embed_views


def run_in_world(system, sensed_views: List[np.ndarray], E: int, *, seed: int,
                 steps: int = None, init_scale: float = 0.1) -> np.ndarray:
    """Stream the world's observations through an open ``KQVSystem``; collect its read-out.

    ``system`` must wrap an open arity-``N`` term whose source is ``(R^E|R^E)^{tensor N}``
    (e.g. ``KQVSystem(Builder(E,d,d_v).head(N))``).  Returns the ``(steps, E)`` array of
    the box's pooled emissions.
    """
    embedded = embed_views(sensed_views, E, seed=seed)  # list of N arrays (T, E)
    N, T = len(embedded), embedded[0].shape[0]
    arr = system.arrangement  # the ONLY thing we touch (provenance)
    if arr.out_dim_M != N * E:
        raise ValueError(f"box source dim {arr.out_dim_M} != N*E = {N * E}")

    O = Phiconf(arr)
    rng = np.random.default_rng(seed)
    state = jnp.asarray(rng.standard_normal(arr.Q.dim)) * init_scale  # non-trivial weights
    boundary = lambda op: (jnp.zeros(arr.out_dim_N), jnp.zeros(arr.in_dim_N))  # noqa: E731

    steps = steps or T
    outs = []
    for t in range(steps):
        out_m = jnp.concatenate([jnp.asarray(embedded[i][t]) for i in range(N)])
        out_pos, _, state = O.with_state(state).run_one(
            (out_m, trivial_omega(arr.in_dim_M)), boundary
        )
        outs.append(np.asarray(out_pos[0]))
    return np.stack(outs)
