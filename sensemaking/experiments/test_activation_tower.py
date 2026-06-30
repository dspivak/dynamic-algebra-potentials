"""Fast smoke + provenance tests for the activation tower (Phase R).

The heavy science (reconstruction, datum-dependence, the near-zero verdict) lives in
``activation_tower.main()`` and is run by hand; here we only pin the cheap invariants:
provenance (C0), the layout helper mirrors ``realize``, ``z_top`` is extractable, and the
near-zero dead zone is frozen (robust regardless of step count).  Run:

    PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m pytest \
        sensemaking/experiments/test_activation_tower.py -q
"""

import jax
jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp
import numpy as np

from sensemaking.kqv import KQVSystem, Act
from sensemaking.experiments.activation_tower import (
    tower_term,
    param_slices,
    top_cell,
    run_tower,
)

E, k, d, d_v = 3, 1, 2, 2
CFG = dict(E=E, k=k, d=d, d_v=d_v, n_bottom=2, depth=2, eta_z=0.1, eta_D=0.03, eta_w=0.01)


def test_provenance_and_layout():
    term = tower_term(**CFG)
    sysm = KQVSystem(term)                                    # provenance (C0): a real term
    tr = sysm.trace()
    assert "cell(k=1)" in tr and "head(N=2" in tr            # interleaved tower (cells + heads)
    arr = sysm.arrangement
    slices, total = param_slices(term)
    assert total == arr.Q.dim                                # layout mirrors realize exactly
    # the top cell (z_top) is the root parent => the LAST slice (compose puts parent last)
    assert top_cell(slices)["start"] == max(s["start"] for s in slices)


def test_z_top_extractable_and_runs_finite():
    term = tower_term(**CFG)
    data = jnp.asarray(np.random.default_rng(0).standard_normal(CFG["n_bottom"] * E))
    r = run_tower(term, data, E=E, init_scale=0.3, steps=20, seed=0)
    assert r["z_top"].shape == (k,)
    assert np.all(np.isfinite(r["U"])) and np.all(np.isfinite(r["z_top"]))


def test_near_zero_is_a_frozen_dead_zone():
    # The decisive mechanism, cheaply: from near-zero init the bilinear gradients vanish,
    # so sum U does not move and the tracking norms stay at init (Phase R FAIL criterion).
    term = tower_term(**CFG)
    data = jnp.asarray(np.random.default_rng(0).standard_normal(CFG["n_bottom"] * E))
    r = run_tower(term, data, E=E, init_scale=1e-3, steps=40, seed=0)
    assert abs(r["U"][-1] - r["U"][0]) < 1e-6 * max(r["U"][0], 1.0)   # U frozen
    assert r["D_mean"][-1] < 1e-2 and r["Om_mean"][-1] < 1e-2         # norms frozen near 0


def test_z_prior_breaks_silence_in_the_tower():
    # The sanctioned z_top prior moves z_top off zero even from near-zero init (it need not
    # make z_top datum-dependent -- that is the experiment's finding, not asserted here).
    mu0 = jnp.ones(k)
    term = tower_term(**CFG, top_prior_lambda=1.0, top_prior_mu=mu0)
    data = jnp.asarray(np.random.default_rng(0).standard_normal(CFG["n_bottom"] * E))
    r = run_tower(term, data, E=E, init_scale=1e-3, steps=60, seed=0)
    assert float(np.linalg.norm(r["z_top"])) > 0.05           # silence broken at the top
