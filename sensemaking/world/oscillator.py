"""The world as a Phiphase-compiled arrangement (Task 2).

The environment is NOT a numpy hack and NOT a KQVTerm: it is an honest
``SmoothArrangement`` in the Arr framework, compiled to a coalgebra by the *phase*
integrator ``Phiphase`` (so it oscillates -- a season *cycles*; ``Phiconf`` would
relax to a fixed point and the world would die).  It sits OUTSIDE the communication
suboperad (it is the environment), which keeps the provenance boundary clean.

Structure (a coupled oscillator, the kind dap was built for -- cf. ``compose_chain``
/ ``compose_graph``): one **slow mode** ``q_0 = s`` (the hidden season) and ``M``
**fast modes** ``q_1..q_M`` (daily "weather" at M locations), each tethered to the
season by a spring ``(q_i - c*s)``.  So every fast mode oscillates *around* ``c*s``:
its slow drift carries the season, its fast oscillation is the local weather.  The
fast springs are heterogeneous (incommensurate frequencies) and the initial phases
are random, so from a *few* modes the season is buried under fast variation, while
*pooling many* modes averages the weather away and reveals ``s``.  That is the
"distributed partial observability" engine -- realized as physics, with the apparent
noise being unresolved fast modes rather than injected randomness.

``roll_world`` runs ``Phiphase(world_arrangement(...))`` and returns the emitted
trajectory; the season ``s`` is component 0 of the emission (ground truth, withheld
from the boxes) and the ``M`` weather modes are components ``1..M``.
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


def world_arrangement(
    M: int,
    *,
    m_s: float = 4000.0,
    k_s: float = 1.0,
    m_fast: float = 1.0,
    k_fast_lo: float = 0.05,
    k_fast_hi: float = 0.15,
    c: float = 1.0,
    label: str = "world",
) -> SmoothArrangement:
    """The coupled-oscillator world as a ``SmoothArrangement`` (compiled by ``Phiphase``).

    ``ndof = 1 + M``: ``q_0 = s`` (season), ``q_1..q_M`` (weather).  The reactive sharp
    is ``diag(1/m)`` (masses), and the potential is the quadratic spring energy

        U(q) = 1/2 k_s s^2 + sum_i 1/2 k_i (q_i - c s)^2,

    so the season is a slow oscillator (large mass ``m_s``) and each weather mode is a
    fast oscillator (mass ``m_fast``, stiffness ``k_i`` spread over [k_fast_lo, k_fast_hi]
    for incommensurate frequencies) tethered to ``c*s``.  Closed source ``(R^0|R^0)``;
    the readout emits the full presented position ``(s, q_1..q_M)``.
    """
    ndof = 1 + M
    k_fast = jnp.linspace(k_fast_lo, k_fast_hi, M)
    inv_mass = jnp.concatenate([jnp.array([1.0 / m_s]), jnp.full((M,), 1.0 / m_fast)])
    Q = diagonal(inv_mass)  # reactive sharp = diag(1/m)

    def out_f(q, m_out):
        return q  # emit the full state; the harness withholds s from the boxes

    def in_f(q, m_out, n_in):
        return jnp.zeros(0)

    def U(q, m_out, n_in):
        s = q[0]
        fast = q[1:]
        return 0.5 * k_s * s**2 + 0.5 * jnp.sum(k_fast * (fast - c * s) ** 2)

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
class WorldRoll:
    """A rolled-out world trajectory."""

    s: np.ndarray  # (T,)   the hidden season (ground truth)
    obs: np.ndarray  # (T, M) the M weather modes (what sensing draws on)
    arr: SmoothArrangement  # the Phiphase-compiled arrangement that produced it


def roll_world(
    M: int,
    *,
    T: int,
    seed: int,
    season_amp: float = 1.0,
    fast_ic_scale: float = 1.0,
    **params,
) -> WorldRoll:
    """Run ``Phiphase(world_arrangement(M, ...))`` for ``T`` steps.

    The **season** starts from a *fixed* initial condition (``q_s = season_amp``,
    ``p_s = 0``), so the yearly cycle has a consistent amplitude across runs; only
    the **weather** (the fast modes) is seeded randomly.  Randomness thus enters only
    through the weather's initial phases (dap's IC convention); the evolution is the
    deterministic phase flow of the arrangement.
    """
    arr = world_arrangement(M, **params)
    O = Phiphase(arr)
    ndof = 1 + M
    rng = np.random.default_rng(seed)
    q0 = jnp.asarray(np.concatenate([[season_amp], rng.standard_normal(M) * fast_ic_scale]))
    p0 = jnp.asarray(np.concatenate([[0.0], rng.standard_normal(M) * fast_ic_scale]))
    state = (q0, p0)

    src = (jnp.zeros(0), trivial_omega(0))
    boundary = lambda op: (jnp.zeros(ndof), jnp.zeros(0))  # autonomous: no force on output

    S, OBS = [], []
    for _ in range(T):
        out_pos, _, state = O.with_state(state).run_one(src, boundary)
        emit = np.asarray(out_pos[0])
        S.append(emit[0])
        OBS.append(emit[1:])
    return WorldRoll(s=np.array(S), obs=np.stack(OBS), arr=arr)
