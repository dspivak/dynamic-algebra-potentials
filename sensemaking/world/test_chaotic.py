"""Tests for the CHAOTIC-season world: Phiphase chaos + decoder-window-ROBUST gate.

Run from the repo root:
    PYTHONPATH=$(pwd) misc/dap/.venv/bin/python -m pytest sensemaking/world/test_chaotic.py -q

Three things are checked, all genuine (no weakened assertions):

1. The world is an honest ``SmoothArrangement`` compiled by ``Phiphase``, closed and
   autonomous, and its symplectic roll stays finite and *bounded* over a long horizon
   (the quartic confinement is doing its job under ``dt = 1``).
2. The season is deterministic *chaos*: two ICs differing by ``1e-6`` diverge over time
   (sensitive dependence), and the season's autocorrelation decays (it is aperiodic --
   no single sensor can lock a period and extrapolate).
3. The **decoder-window-robust** gate: using the SAME held-out ridge decoder
   (``diagnose._decode_r2``) fair to single and pooled, the best single sensor decodes
   the season poorly at window 10 AND 50 AND 100 (it stays low as the window grows),
   while the pool decodes it -- across several weather seeds.
"""

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np

from dap.arrangement import SmoothArrangement

from sensemaking.kqv import KQVTerm
from sensemaking.world.chaotic import (
    CHAOTIC,
    GATE_WINDOWS,
    SENSE_CHAOTIC,
    chaotic_world_arrangement,
    roll_chaotic,
    standard_chaotic_world,
)
from sensemaking.world.diagnose import _decode_r2


# --- small signal helpers (local; no dependence on the optimized objective) ---


def _autocorr(x: np.ndarray, lag: int) -> float:
    """Normalised autocorrelation of ``x`` at ``lag`` (mean-removed)."""
    x = np.asarray(x, float)
    x = x - x.mean()
    denom = float(np.sum(x * x))
    if denom == 0.0:
        return 0.0
    return float(np.sum(x[:-lag] * x[lag:]) / denom)


def _crossings(x: np.ndarray) -> int:
    x = np.asarray(x, float) - np.mean(x)
    return int(np.sum(x[:-1] * x[1:] < 0))


# --------------------------------------------------------------------------- #
# 1. Phiphase-compiled, stable, bounded.
# --------------------------------------------------------------------------- #


def test_world_is_a_phiphase_arrangement_stable_and_bounded():
    # Honest SmoothArrangement (Arr framework), closed and autonomous, emitting
    # (season, confounders, weather); rolled by Phiphase it stays finite and bounded.
    arr = chaotic_world_arrangement(CHAOTIC["M"], k_slow=CHAOTIC["k_slow"], c=CHAOTIC["c"])
    assert isinstance(arr, SmoothArrangement)
    assert arr.out_dim_M == 0 and arr.in_dim_M == 0 and arr.in_dim_N == 0  # closed, autonomous
    assert arr.out_dim_N == CHAOTIC["k_slow"] + CHAOTIC["M"]  # emits (z_0..z_{k-1}, q_1..q_M)

    keys = ("k_slow", "m_slow", "a_slow", "b_slow", "g_slow", "c", "confound_scale",
            "slow_ic_scale", "fast_ic_scale")
    r = roll_chaotic(CHAOTIC["M"], T=4000, seed=0, **{k: CHAOTIC[k] for k in keys})
    assert np.all(np.isfinite(r.s)) and np.all(np.isfinite(r.obs))  # symplectic roll is stable
    assert np.all(np.isfinite(r.z))
    assert np.max(np.abs(r.z)) < 50.0    # slow block bounded (quartic confinement)
    assert np.max(np.abs(r.obs)) < 200.0  # weather bounded -- no blow-up over T=4000
    # the season actually moves (it is dynamics, not a fixed point) and the weather is faster
    assert _crossings(r.s) >= 4
    assert _crossings(r.obs[:, 0]) > 3 * max(_crossings(r.s), 1)


def test_world_is_not_in_the_suboperad():
    # the environment is a plain SmoothArrangement, NOT a KQVTerm (provenance boundary)
    assert not isinstance(chaotic_world_arrangement(8, k_slow=3), KQVTerm)


# --------------------------------------------------------------------------- #
# 2. The season is genuinely chaotic: sensitive dependence + aperiodic.
# --------------------------------------------------------------------------- #


def test_season_has_sensitive_dependence_on_initial_conditions():
    # Two seasons whose ICs differ by 1e-6 (only in the season coordinate) diverge:
    # the late-time separation is orders of magnitude larger than the initial 1e-6.
    keys = ("k_slow", "m_slow", "a_slow", "b_slow", "g_slow", "c", "confound_scale",
            "slow_ic_scale", "fast_ic_scale")
    common = {k: CHAOTIC[k] for k in keys}
    T = 4000
    r0 = roll_chaotic(CHAOTIC["M"], T=T, seed=0, season_kick=0.0, **common)
    r1 = roll_chaotic(CHAOTIC["M"], T=T, seed=0, season_kick=1e-6, **common)

    sep = np.abs(r0.s - r1.s)
    early = float(np.mean(sep[:50]))          # ~ the 1e-6 seed, before divergence
    late = float(np.max(sep[T // 2:]))        # after many Lyapunov times
    assert early < 1e-3                        # they start essentially identical
    assert late > 1e-2                          # and end up macroscopically apart
    assert late / max(early, 1e-12) > 1e3      # exponential separation (chaos), not roundoff


def test_season_is_aperiodic_autocorrelation_decays():
    # A periodic season would keep |autocorr| near 1 at its period; a chaotic one
    # decorrelates.  We require the autocorrelation to fall well below 1 at long lags
    # and to not revive (no clean period to lock onto and extrapolate).
    keys = ("k_slow", "m_slow", "a_slow", "b_slow", "g_slow", "c", "confound_scale",
            "slow_ic_scale", "fast_ic_scale")
    r = roll_chaotic(CHAOTIC["M"], T=8000, seed=0, **{k: CHAOTIC[k] for k in keys})
    s = r.s
    # decorrelation: by some long lag the autocorrelation has dropped well below 1 ...
    long_lags = range(400, 3000, 50)
    ac = [abs(_autocorr(s, L)) for L in long_lags]
    assert min(ac) < 0.3                       # it genuinely decorrelates
    assert np.mean(ac) < 0.6                    # and does not stay locked (no strict period)
    # ... and it is not a near-constant signal masquerading as "decorrelated":
    assert s.std() > 0.1


# --------------------------------------------------------------------------- #
# 3. The decoder-window-ROBUST necessary-communication gate.
# --------------------------------------------------------------------------- #


def _gate_numbers(s, views, window):
    singles = [_decode_r2(v, s, window) for v in views]
    best = float(max(singles))
    pooled = float(_decode_r2(np.concatenate(views, axis=1), s, window))
    return best, pooled


def test_decoder_window_robust_gate():
    # The deliverable's point: communication is necessary even for a LONG-window decoder.
    # Using the SAME held-out ridge decoder for single and pooled (apples-to-apples),
    # across several weather seeds: the best single sensor decodes the season poorly at
    # window 10 AND 50 AND 100 (it does NOT climb as the window grows -- chaos plus a
    # slow per-sensor confounder leave a single sensor stuck), while the pool decodes it.
    seeds = range(5)
    for window in GATE_WINDOWS:  # (10, 50, 100)
        for seed in seeds:
            roll, views = standard_chaotic_world(seed, T=4000)
            best, pooled = _gate_numbers(roll.s, views, window)
            assert best < 0.45, (window, seed, "best_single", best)
            assert pooled > 0.6, (window, seed, "pooled", pooled)


def test_pool_beats_every_single_sensor_at_each_window():
    # Robustness restatement: at every window the pool beats even the luckiest single
    # sensor by a clear margin (so the pool's advantage is not a short-memory artifact).
    for window in GATE_WINDOWS:
        roll, views = standard_chaotic_world(0, T=4000)
        best, pooled = _gate_numbers(roll.s, views, window)
        assert pooled - best > 0.2, (window, best, pooled)
