"""Regression test of Stage 3 (revised after audit): beta-mediated self-maintenance.

Honest claims (see stage3_selfmaintenance.py docstring): self-maintenance and bistability
PASS (MAINTENANCE margin = null+eps, seeds 0,1,2); INTRINSIC irreversibility FAILS (margin=0
revives, seeds 0,1,2); MARGIN-CONDITIONED irreversibility PASSES only under a STRICTER cutoff
(IRREVERSIBILITY_MARGIN ~ 0.2, seeds 0,1,2). The null+eps maintenance margin is NOT a reliable
irreversibility margin -- it straddles the per-seed knee (seeds 0,1 revive, seed 2 dies), and
that caveat is pinned by its own test below. Trains seeds 0,1,2 (cached).

Run: PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m pytest sensemaking/experiments/test_stage3.py -q
"""

import functools

import numpy as np

from sensemaking.experiments.stage2_routing import gen_episodes
from sensemaking.experiments.stage3_selfmaintenance import (
    IRREVERSIBILITY_MARGIN,
    _r2,
    maintenance_margin,
    run_dynamics,
    train,
)


@functools.lru_cache(maxsize=4)
def _W(seed):
    return train(seed)


def _margin(W, seed):
    return maintenance_margin(W, seed=seed)  # null+eps: the maintenance margin (R2/bistability)


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
    # seeds 0,1,2. INTRINSIC irreversibility FAILS and MARGIN-CONDITIONED irreversibility PASSES.
    for seed in (0, 1, 2):
        W = _W(seed)
        # INTRINSIC FAIL: with no margin, restoring the world revives the structure
        assert run_dynamics(W, 2.8, world="revive", steps=240, margin=0.0, seed=seed)[-1][0] > 1.0, seed
        # CONDITIONED PASS: with the stricter margin >= ~0.2 the dead state is absorbing
        assert run_dynamics(W, 2.8, world="revive", steps=240, margin=IRREVERSIBILITY_MARGIN, seed=seed)[-1][0] < 0.2, seed


def test_r3_null_eps_is_not_a_reliable_irreversibility_margin():
    # HONESTY LOCK: the null+eps MAINTENANCE margin does NOT imply irreversibility. It straddles
    # the per-seed knee in [0.18, 0.20]: seeds 0,1 REVIVE under null+eps, seed 2 dies. This pins
    # the caveat so no future edit can quietly upgrade null+eps into an irreversibility margin.
    finals = {}
    for seed in (0, 1, 2):
        W = _W(seed)
        m = maintenance_margin(W, seed=seed)
        finals[seed] = run_dynamics(W, 2.8, world="revive", steps=240, margin=m, seed=seed)[-1][0]
    assert finals[0] > 1.0, finals  # seed 0 revives under null+eps
    assert finals[1] > 1.0, finals  # seed 1 revives under null+eps
    assert finals[2] < 0.2, finals  # seed 2 dies under null+eps
    # NOT all seeds die under null+eps -> null+eps does not earn irreversibility (only ~0.2 does)
    assert not all(v < 0.2 for v in finals.values()), finals


def test_bistability_two_attractors_thin_dead_basin():
    # bistable: beta=0 is a dead attractor, beta clearly above threshold is the alive one.
    # (The dead basin is razor-thin -- threshold < 0.01 -- so this is bistability with a
    #  near-degenerate dead basin, stated honestly, not a wide dead region.)
    W = _W(0)
    m = _margin(W, 0)
    assert run_dynamics(W, 0.0, world="predict", steps=150, margin=m)[-1][0] < 0.2  # dead attractor
    assert run_dynamics(W, 0.5, world="predict", steps=150, margin=m)[-1][0] > 1.5  # alive attractor
