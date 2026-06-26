"""Regression test of Stage 3 (revised after audit): beta-mediated self-maintenance.

Honest claims (see stage3_selfmaintenance.py docstring): self-maintenance and bistability
PASS; INTRINSIC irreversibility FAILS (margin=0 revives); MARGIN-CONDITIONED irreversibility
PASSES (margin>=~0.2, justified by the null baseline). Trains seeds 0,1,2 (cached).

Run: PYTHONPATH=$(pwd) misc/dap/.venv/bin/python -m pytest sensemaking/experiments/test_stage3.py -q
"""

import functools

import numpy as np

from sensemaking.experiments.stage2_routing import gen_episodes
from sensemaking.experiments.stage3_selfmaintenance import _r2, null_r2, run_dynamics, train


@functools.lru_cache(maxsize=4)
def _W(seed):
    return train(seed)


def _margin(W, seed):
    return null_r2(W, seed=seed) + 0.03  # no-credit-below-null baseline


def test_r1_sharpness_load_bearing():
    # real sweep, seeds 0,1,2: flat ~ null, sharp alive, rises then plateaus
    for seed in (0, 1, 2):
        W = _W(seed)
        h, tgt, _ = gen_episodes(200, np.random.default_rng(9000 + seed))
        r0, r025, r1, r2 = (_r2(W, h, tgt, b) for b in (0.0, 0.25, 1.0, 2.0))
        assert r0 < 0.3, (seed, r0)  # flat attention ~ null baseline
        assert r1 > 0.85 and r2 > 0.85, (seed, r1, r2)  # sharp = alive
        assert r025 > r0 and r2 > r025 - 0.05, (seed, r0, r025, r2)  # rises then plateaus


def test_r2_self_maintenance():
    # seeds 0,1,2, with the principled null-derived margin
    for seed in (0, 1, 2):
        W = _W(seed)
        m = _margin(W, seed)
        assert run_dynamics(W, 2.8, world="predict", steps=120, margin=m, seed=seed)[-1][0] > 1.5  # MAINTAIN
        assert run_dynamics(W, 2.8, world="scramble", steps=120, margin=m, seed=seed)[-1][0] < 0.2  # DISSOLVE
        assert run_dynamics(W, 2.8, world="predict", steps=120, margin=m, knock=(60, 0.5), seed=seed)[-1][0] > 1.5  # REPAIR
        assert run_dynamics(W, 2.8, world="predict", steps=120, margin=m, gain=0.0, seed=seed)[-1][0] < 0.2  # CONTROL


def test_r3_irreversibility_is_margin_conditioned_not_intrinsic():
    W = _W(0)
    # INTRINSIC irreversibility FAILS: with no margin, restoring the world revives the structure
    assert run_dynamics(W, 2.8, world="revive", steps=240, margin=0.0)[-1][0] > 1.0
    # MARGIN-CONDITIONED irreversibility PASSES: with margin >= ~0.2 the dead state is absorbing
    assert run_dynamics(W, 2.8, world="revive", steps=240, margin=0.2)[-1][0] < 0.2


def test_bistability_two_attractors_thin_dead_basin():
    # bistable: beta=0 is a dead attractor, beta clearly above threshold is the alive one.
    # (The dead basin is razor-thin -- threshold < 0.01 -- so this is bistability with a
    #  near-degenerate dead basin, stated honestly, not a wide dead region.)
    W = _W(0)
    m = _margin(W, 0)
    assert run_dynamics(W, 0.0, world="predict", steps=150, margin=m)[-1][0] < 0.2  # dead attractor
    assert run_dynamics(W, 0.5, world="predict", steps=150, margin=m)[-1][0] > 1.5  # alive attractor
