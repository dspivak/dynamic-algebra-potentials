"""Tests for the Task 2 world: Phiphase oscillator + necessary-communication gate.

Run from the repo root:
    PYTHONPATH=$(pwd) misc/dap/.venv/bin/python -m pytest sensemaking/world/test_world.py -q
"""

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np

from dap.arrangement import SmoothArrangement

from sensemaking.kqv import Builder, KQVSystem, KQVTerm
from sensemaking.world import (
    GATE_WINDOW,
    SENSE,
    WORLD,
    decode_gate,
    roll_world,
    run_in_world,
    standard_world,
    world_arrangement,
)


def _crossings(x):
    x = x - x.mean()
    return int(np.sum(x[:-1] * x[1:] < 0))


def test_world_is_a_phiphase_oscillator_arrangement():
    # The world is an honest SmoothArrangement (Arr framework), closed and autonomous,
    # emitting (season, weather); rolled by Phiphase it OSCILLATES and stays bounded.
    arr = world_arrangement(WORLD["M"], c=WORLD["c"], m_s=WORLD["m_s"])
    assert isinstance(arr, SmoothArrangement)
    assert arr.out_dim_M == 0 and arr.in_dim_M == 0 and arr.in_dim_N == 0  # closed, autonomous
    assert arr.out_dim_N == 1 + WORLD["M"]  # emits (s, q_1..q_M)

    keys = ("c", "m_s", "k_s", "season_amp", "fast_ic_scale")
    r = roll_world(WORLD["M"], T=1500, seed=0, **{k: WORLD[k] for k in keys})
    assert np.all(np.isfinite(r.s)) and np.all(np.isfinite(r.obs))  # symplectic roll is stable
    assert np.max(np.abs(r.obs)) < 100.0  # bounded -- no blow-up
    # oscillation (Phiphase), not relaxation (Phiconf): the season cycles, weather faster
    assert _crossings(r.s) >= 2
    assert _crossings(r.obs[:, 0]) > 3 * _crossings(r.s)


def test_world_is_not_in_the_suboperad():
    # the environment is a plain SmoothArrangement, NOT a KQVTerm (provenance boundary)
    assert not isinstance(world_arrangement(8), KQVTerm)


def test_necessary_communication_gate_passes_robustly():
    # The strong gate everything downstream depends on: NO single box (even the best)
    # decodes the season, the pool does. (Tuning verified 8 weather seeds; here 4.)
    for seed in range(4):
        roll, views = standard_world(seed, T=2000)
        g = decode_gate(roll.s, views, window=GATE_WINDOW)
        assert g["pass"], (seed, g)
        assert g["best_single"] < 0.45  # even the luckiest box can't decode the season
        assert g["pooled"] > 0.68  # the pool can
        assert g["margin"] > 0.25  # the pool beats every single box by a clear margin


def test_necessity_is_relative_to_bounded_decoder_memory():
    # Honest, documented limitation (codex Task-2 finding): a single sensor is
    # insufficient only for a BOUNDED-memory decoder.  The season is slow and periodic,
    # so a single sensor with a LONG temporal window can extrapolate it -- necessity is
    # relative to the decoder window.  The gate window (10) is matched to the
    # experiment's short-memory boxes (per-step spatial attention, no 50-step
    # accumulator), for which communication is genuinely necessary.  A
    # decoder-window-robust world would need an aperiodic (chaotic) season (future).
    from sensemaking.world.diagnose import _decode_r2

    roll, views = standard_world(0, T=2000)
    best_short = max(_decode_r2(v, roll.s, 10) for v in views)
    best_long = max(_decode_r2(v, roll.s, 50) for v in views)
    assert best_short < 0.45  # short memory (the boxes): a single sensor fails
    assert best_long > 0.60  # long memory: a single sensor extrapolates the periodic season


def test_open_box_runs_in_world():
    # an open KQVSystem driven by the world stays finite (Task 2 = plumbing, no learning)
    E, d, d_v, N = 8, 4, 4, SENSE["N"]
    _, views = standard_world(0, T=300)
    system = KQVSystem(Builder(E, d, d_v).head(N))
    out = run_in_world(system, views, E, seed=1, steps=150)
    assert out.shape == (150, E)
    assert np.all(np.isfinite(out))
