"""A CHAOTIC-season world as a Phiphase-compiled arrangement (Task 2, window-robust variant).

This is the decoder-window-ROBUST sibling of ``oscillator.py``.  The architecture is
the same in spirit -- one **slow season** ``s`` plus ``M`` **fast weather modes**
tethered to it, the whole thing an honest ``SmoothArrangement`` rolled by the *phase*
integrator ``Phiphase`` -- but with two deliberate changes that together make a single
sensor insufficient *regardless of how long a temporal window the decoder is given*:

1. **The season is deterministic chaos, not a periodic oscillation.**  The slow
   subsystem is a ring of ``K_slow`` nonlinearly coupled double-well (Duffing /
   ``phi^4``-chain) oscillators -- a canonical bounded Hamiltonian-chaos system.  The
   on-site quartic ``1/4 a z^4 - 1/2 b z^2`` is a symmetric double well; neighbours are
   coupled by ``g (z_r - z_{r+1})^2`` (ring).  With ``K_slow >= 2`` this is
   non-integrable, and at energies near the inter-well barrier the orbit hops between
   wells irregularly: the season ``s = z_0`` is aperiodic, broadband, and shows
   sensitive dependence on initial conditions.  The quartic term is *confining*
   (``U -> +infinity`` as ``|z| -> infinity``), so the motion is bounded for **any**
   energy -- boundedness is structural, not a tuned coincidence (important: a nonlinear
   potential can blow up under the ``dt = 1`` symplectic Euler step of ``Phiphase``).
   Because the season never repeats, no single sensor can lock onto a period and
   *extrapolate* it from a long window.

2. **Each weather mode carries a slow, sensor-specific confounder that cancels only in
   the pool.**  In ``oscillator.py`` a fast mode tethers to ``c*s`` alone, so a long
   window can average the fast oscillation *and* the sensor noise away and read off
   ``c*s`` -- the long window wins by *de-noising*, not by exploiting periodicity, so
   chaos alone would not defeat it.  Here the confounder coordinates ``z_1..z_{K-1}``
   (the other slow chaotic DOF) are mixed by a fixed, **column-centred** random matrix
   ``B`` into per-mode slow nuisances ``u_i = sum_r B_{i r} z_{r+1}``, and mode ``i``
   tethers to ``c*s + u_i``.  ``u_i`` is *slow* (so temporal averaging cannot remove
   it) and *sensor-specific* (so a single sensor cannot separate it from ``s``); but
   ``B`` is centred, ``sum_i u_i = 0``, so **pooling** the modes averages the
   confounders to zero and the fast weather away, exposing ``c*s``.  Necessity is thus
   robust to the decoder's temporal window: a single sensor is confounded at window 10,
   50, and 100 alike, while the pool decodes the season.

``roll_chaotic`` runs ``Phiphase(chaotic_world_arrangement(...))`` and returns the
emitted trajectory; the season ``s`` is component 0 of the emission (ground truth,
withheld from the boxes) and the ``M`` weather modes are components ``1..M`` -- exactly
the layout ``observe.partition_modes`` / ``observe.sense`` / ``diagnose._decode_r2``
expect, so the gate machinery is reused unchanged.

It sits OUTSIDE the communication suboperad (it is the environment): a plain
``SmoothArrangement``, never ``realize`` / ``KQVSystem``, never importing
``sensemaking.kqv``.
"""

from __future__ import annotations

from dataclasses import dataclass

import jax
jax.config.update("jax_enable_x64", True)  # long symplectic rolls want float64

import jax.numpy as jnp
import numpy as np

from dap.arrangement import SmoothArrangement
from dap.functors import Phiphase
from dap.interpretation import trivial_omega
from dap.rvect import diagonal


def _centered_mixing(M: int, R: int, *, seed: int, scale: float) -> jnp.ndarray:
    """A fixed ``M x R`` random mixing whose columns sum to zero (centred confounders).

    Each column mixes one slow confounder coordinate ``z_{r+1}`` into the ``M`` weather
    modes.  Centring (subtracting each column's mean) guarantees ``sum_i B_{i r} = 0``,
    so pooling all ``M`` modes cancels every confounder while a single mode is fully
    confounded -- the structural reason the gate is window-robust rather than
    noise-limited.
    """
    rng = np.random.default_rng(seed)
    B = rng.standard_normal((M, max(R, 0)))
    if R > 0:
        B = B - B.mean(axis=0, keepdims=True)  # centre each column: sum_i B_{i r} = 0
        B = B * scale
    return jnp.asarray(B)


def chaotic_world_arrangement(
    M: int,
    *,
    k_slow: int = 3,
    m_slow: float = 2000.0,
    a_slow: float = 1.0,
    b_slow: float = 1.0,
    g_slow: float = 0.3,
    m_fast: float = 1.0,
    k_fast_lo: float = 0.05,
    k_fast_hi: float = 0.15,
    c: float = 1.0,
    confound_scale: float = 0.6,
    mix_seed: int = 7,
    label: str = "chaotic-world",
) -> SmoothArrangement:
    """The chaotic-season world as a ``SmoothArrangement`` (compiled by ``Phiphase``).

    ``ndof = k_slow + M``: the first ``k_slow`` coordinates ``z_0..z_{k_slow-1}`` are the
    slow chaotic subsystem (``z_0 = s`` is the season, ``z_1..z_{k_slow-1}`` are the
    confounder generators), and ``q_1..q_M`` are the fast weather modes.  The reactive
    sharp is ``diag(1/m)`` (slow mass ``m_slow`` on the slow block, fast mass ``m_fast``
    on the weather block), and the potential is

        U(z, q) = sum_r [ 1/4 a z_r^4 - 1/2 b z_r^2 ]            (on-site double wells)
                + sum_r g (z_r - z_{r+1 mod k_slow})^2           (ring coupling)
                + sum_i 1/2 k_i ( q_i - c*z_0 - u_i )^2,         (weather tethers)

    where ``u_i = sum_{r>=1} B_{i,r-1} z_r`` is mode ``i``'s slow confounder built from a
    fixed column-centred random mixing ``B`` of the confounder coordinates.  The slow
    block is a confining ``phi^4``-chain (bounded chaos); each weather mode is a fast
    oscillator (mass ``m_fast``, stiffness ``k_i`` spread over ``[k_fast_lo, k_fast_hi]``
    for incommensurate frequencies) tethered to ``c*s`` plus its slow confounder.  Closed
    source ``(R^0|R^0)``; the readout emits the full presented position
    ``(s, z_1..z_{k_slow-1}, q_1..q_M)``.

    Stability note (conditional well-posedness).  ``Phiphase`` is semi-implicit Euler
    with ``dt = 1``; a harmonic mode is stable iff ``stiffness / mass < 4``.  Here the
    slow effective stiffness is the Hessian of the ``phi^4``-chain, bounded by roughly
    ``3 a z^2 + b + 4 g`` on the (confined) orbit; with ``m_slow`` large this is far
    below ``4 m_slow``, and the fast modes keep ``k_i / m_fast <= k_fast_hi < 4``.  So
    the whole motion stays in the stable regime and the quartic confinement keeps it
    bounded.
    """
    if k_slow < 2:
        raise ValueError(f"need >= 2 slow DOF for chaos (>=4-dim phase space): k_slow={k_slow}")
    ndof = k_slow + M
    k_fast = jnp.linspace(k_fast_lo, k_fast_hi, M)
    inv_mass = jnp.concatenate(
        [jnp.full((k_slow,), 1.0 / m_slow), jnp.full((M,), 1.0 / m_fast)]
    )
    Q = diagonal(inv_mass)  # reactive sharp = diag(1/m): slow block heavy, fast block light

    B = _centered_mixing(M, k_slow - 1, seed=mix_seed, scale=confound_scale)  # (M, k_slow-1)

    def out_f(q, m_out):
        return q  # emit the full state; the harness withholds s (and the confounders) from the boxes

    def in_f(q, m_out, n_in):
        return jnp.zeros(0)

    def U(q, m_out, n_in):
        z = q[:k_slow]      # slow chaotic block
        fast = q[k_slow:]   # fast weather block
        s = z[0]

        # On-site symmetric double wells (Duffing): 1/4 a z^4 - 1/2 b z^2 (confining quartic).
        onsite = jnp.sum(0.25 * a_slow * z**4 - 0.5 * b_slow * z**2)

        # Ring coupling g (z_r - z_{r+1})^2 over the slow chain (makes it non-integrable).
        z_next = jnp.roll(z, -1)
        coupling = g_slow * jnp.sum((z - z_next) ** 2)

        # Per-mode slow confounder u_i = sum_r B_{i r} z_{r+1}; centred B => sum_i u_i = 0.
        confound = z[1:]                      # (k_slow-1,)
        u = B @ confound if (k_slow - 1) > 0 else jnp.zeros(M)  # (M,)

        # Weather tethers: each fast mode springs to c*s + u_i (slow target).
        tether = 0.5 * jnp.sum(k_fast * (fast - c * s - u) ** 2)

        return onsite + coupling + tether

    return SmoothArrangement(
        Q=Q,
        out_dim_M=0,
        in_dim_M=0,
        out_dim_N=ndof,
        in_dim_N=0,
        out_f=out_f,
        in_f=in_f,
        U=U,
        label=label,
    )


@dataclass(frozen=True)
class ChaoticWorldRoll:
    """A rolled-out chaotic-world trajectory."""

    s: np.ndarray  # (T,)   the hidden chaotic season (ground truth)
    obs: np.ndarray  # (T, M) the M weather modes (what sensing draws on)
    z: np.ndarray  # (T, k_slow) the full slow chaotic block (s plus confounder generators)
    arr: SmoothArrangement  # the Phiphase-compiled arrangement that produced it


def roll_chaotic(
    M: int,
    *,
    T: int,
    seed: int,
    k_slow: int = 3,
    slow_ic_scale: float = 1.4,
    slow_p_scale: float = 0.0,
    fast_ic_scale: float = 1.0,
    season_kick: float = 0.0,
    **params,
) -> ChaoticWorldRoll:
    """Run ``Phiphase(chaotic_world_arrangement(M, ...))`` for ``T`` steps.

    The **slow chaotic block** starts from a *fixed* initial condition driven by
    ``slow_ic_scale`` (positions) and ``slow_p_scale`` (momenta) -- a *deterministic*
    seed for the chaos, so the season trajectory is reproducible and identical across
    weather seeds (only the weather changes with ``seed``).  ``slow_ic_scale`` is chosen
    so the slow energy sits near the inter-well barrier, where the ``phi^4``-chain hops
    between wells and the season is strongly aperiodic.  ``season_kick`` perturbs only
    the season's initial position (used by the sensitive-dependence test to launch two
    nearby ICs).  Only the **weather** (fast modes) is seeded randomly from ``seed``;
    the evolution is the deterministic phase flow of the arrangement.
    """
    arr = chaotic_world_arrangement(M, k_slow=k_slow, **params)
    O = Phiphase(arr)
    ndof = k_slow + M
    rng = np.random.default_rng(seed)

    # Deterministic, slightly heterogeneous slow ICs (so the chain is not on a symmetric
    # invariant manifold): a fixed spread of well-offsets seeded from a *fixed* generator.
    slow_rng = np.random.default_rng(20_259)
    z0 = slow_rng.standard_normal(k_slow) * slow_ic_scale
    z0[0] = z0[0] + season_kick  # perturb only the season's IC (sensitive-dependence probe)
    pz0 = slow_rng.standard_normal(k_slow) * slow_p_scale

    q0 = jnp.asarray(np.concatenate([z0, rng.standard_normal(M) * fast_ic_scale]))
    p0 = jnp.asarray(np.concatenate([pz0, rng.standard_normal(M) * fast_ic_scale]))
    state = (q0, p0)

    src = (jnp.zeros(0), trivial_omega(0))
    boundary = lambda op: (jnp.zeros(ndof), jnp.zeros(0))  # autonomous: no force on output

    S, OBS, Z = [], [], []
    for _ in range(T):
        out_pos, _, state = O.with_state(state).run_one(src, boundary)
        emit = np.asarray(out_pos[0])
        S.append(emit[0])
        Z.append(emit[:k_slow])
        OBS.append(emit[k_slow:])
    return ChaoticWorldRoll(s=np.array(S), obs=np.stack(OBS), z=np.stack(Z), arr=arr)


# ---------------------------------------------------------------------------
# The locked chaotic-world configuration (mirrors standard.py).
# ---------------------------------------------------------------------------

# Slow chaotic block + weather + sensing parameters for the window-robust gate.
CHAOTIC = dict(
    M=48,
    k_slow=4,
    m_slow=2000.0,
    a_slow=1.0,
    b_slow=1.0,
    g_slow=0.3,
    c=2.0,
    confound_scale=0.6,
    slow_ic_scale=1.4,
    fast_ic_scale=1.0,
)
SENSE_CHAOTIC = dict(N=48, noise=4.0)  # one mode per sensor, high independent sensor noise
GATE_WINDOWS = (10, 50, 100)


def standard_chaotic_world(seed: int, *, T: int = 4000):
    """Roll the locked chaotic world and produce the ``N`` noisy per-box observations.

    Returns ``(roll, sensed_views)`` where ``roll.s`` is the hidden chaotic season
    (ground truth, for diagnostics) and ``sensed_views`` is a list of ``N`` arrays
    ``(T, k_i)`` -- the noisy mode-slices each box senses.  The chaotic season is fixed
    (deterministic); weather (fast modes) and sensor noise are seeded from ``seed``.
    """
    from .observe import sense  # local import: keep the world layer decoupled at import time

    roll = roll_chaotic(
        CHAOTIC["M"],
        T=T,
        seed=seed,
        k_slow=CHAOTIC["k_slow"],
        m_slow=CHAOTIC["m_slow"],
        a_slow=CHAOTIC["a_slow"],
        b_slow=CHAOTIC["b_slow"],
        g_slow=CHAOTIC["g_slow"],
        c=CHAOTIC["c"],
        confound_scale=CHAOTIC["confound_scale"],
        slow_ic_scale=CHAOTIC["slow_ic_scale"],
        fast_ic_scale=CHAOTIC["fast_ic_scale"],
    )
    views = sense(roll.obs, SENSE_CHAOTIC["N"], noise=SENSE_CHAOTIC["noise"], seed=10_000 + seed)
    return roll, views
