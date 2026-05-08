"""End-to-end test: the chain-of-K-particles Klein-Gordon equation.

References sec.klein_gordon of dynamic-algebra-potentials.tex.

The Klein-Gordon chain extends the harmonic chain (sec.spring) by adding
an on-site mass term ``(m_0^2/2) v^2`` to each particle's potential:

    U(v, n_in) = (kappa/2)(v - n_in)^2 + (m_0^2/2) v^2.

The discrete recurrence is

    m * (v_i(t+2) - 2 v_i(t+1) + v_i(t))
        = kappa * (v_{i-1}(t) - 2 v_i(t) + v_{i+1}(t)) - m_0^2 * v_i(t).

For a pinned chain of length K the eigenmodes are
``v_j^{(n)} = sin(j n pi / (K+1))`` for ``n = 1, ..., K``, with

    omega_n^2 = m_0^2 / m + (kappa / m) * 4 sin^2(n pi / (2(K+1))).
"""

import os

import jax.numpy as jnp
import numpy as np
import pytest

from dap.functors import Phi
from dap.lens import PotLensMap
from dap.pvect import diagonal_pvect
from dap.wiring import compose_chain


# ---------------------------------------------------------------------------
# Single-particle Klein-Gordon factory.
# ---------------------------------------------------------------------------


def _kg_particle(m: float, kappa: float, m0: float) -> PotLensMap:
    """Single-particle PotLens for sec.klein_gordon:

    V = R, sharp(p) = p/m, out_f = id, in_f vacuous, and
    U(x, y) = (kappa/2)(x - y)^2 + (m_0^2/2) x^2.
    """
    V = diagonal_pvect(jnp.array([1.0 / m]))

    def out_f(v, m_out):
        return v

    def in_f(v, m_out, n_in):
        return jnp.zeros(0)

    def U(v, m_out, n_in):
        diff = v[0] - n_in[0]
        return 0.5 * kappa * diff * diff + 0.5 * (m0 * m0) * v[0] * v[0]

    return PotLensMap(
        V=V, out_dim_M=0, in_dim_M=0, out_dim_N=1, in_dim_N=1,
        out_f=out_f, in_f=in_f, U=U, label="KGPart",
    )


# ---------------------------------------------------------------------------
# Reference state-update for the K-particle KG chain.
# ---------------------------------------------------------------------------


def _kg_potlens_composite_final(v, p, v_prev_extern, xi_N_extern, m, kappa, m0):
    """Reference for the KG analogue of ``eqn.potlens_composite_final``.

    Adds the on-site contribution ``- m_0^2 v_i`` to ``p_i'`` for every i.
    """
    K = v.shape[0]
    v_new = v + p / m
    p_new = []
    for i in range(K):
        if i < K - 1:
            v_prev = v_prev_extern if i == 0 else v[i - 1]
            v_next = v[i + 1]
            p_i_new = (
                p[i]
                + kappa * (v_prev + v_next - 2.0 * v[i])
                - (m0 * m0) * v[i]
            )
        else:
            v_prev = v[i - 1] if K > 1 else v_prev_extern
            p_i_new = (
                p[i]
                + kappa * (v_prev - v[i])
                - xi_N_extern
                - (m0 * m0) * v[i]
            )
        p_new.append(p_i_new)
    p_new = jnp.stack(p_new)
    return v_new, p_new


# ---------------------------------------------------------------------------
# Helpers shared by the simulation tests.
# ---------------------------------------------------------------------------


_IN_POS = (jnp.zeros(0), (jnp.zeros((0, 0)), jnp.zeros(0)))


def _step_pinned(O, state, kappa):
    """One pinned-end step: v_prev = 0, xi_N = kappa * v_K (so v_{K+1} = 0)."""
    v, _ = state
    K = v.shape[0]
    v_prev = jnp.array([0.0])
    xi_N = jnp.array([kappa * float(v[K - 1])])
    in_dir = (xi_N, v_prev)
    org = O.with_state(state)
    _, _, new_state = org.run_one(_IN_POS, lambda _op: in_dir)
    return new_state


# ---------------------------------------------------------------------------
# Tests.
# ---------------------------------------------------------------------------


def test_kg_state_update():
    """Apply Phi to a 5-particle KG chain; check the KG state-update formula
    against the hand-coded reference for 5 random states."""
    K = 5
    m, kappa, m0 = 1.7, 2.3, 0.4
    Part = _kg_particle(m=m, kappa=kappa, m0=m0)
    composite = compose_chain([Part] * K)
    O = Phi(composite)

    rng = np.random.default_rng(20260508)
    for _ in range(5):
        v = jnp.asarray(rng.standard_normal(K))
        p = jnp.asarray(rng.standard_normal(K))
        v_prev = float(rng.standard_normal())
        xi_N = float(rng.standard_normal())

        org = O.with_state((v, p))
        in_dir = (jnp.array([xi_N]), jnp.array([v_prev]))
        _, _, new_state = org.run_one(_IN_POS, lambda _op: in_dir)
        new_v, new_p = new_state

        ref_v, ref_p = _kg_potlens_composite_final(
            v, p, v_prev, xi_N, m, kappa, m0
        )
        np.testing.assert_allclose(np.asarray(new_v), np.asarray(ref_v), atol=1e-10)
        np.testing.assert_allclose(np.asarray(new_p), np.asarray(ref_p), atol=1e-10)


def test_kg_recurrence():
    """Simulate T = 10 KG steps with pinned ends; verify the discrete KG
    recurrence holds at every interior site and every step."""
    K = 5
    T = 10
    m, kappa, m0 = 1.5, 0.9, 0.3

    Part = _kg_particle(m=m, kappa=kappa, m0=m0)
    composite = compose_chain([Part] * K)
    O = Phi(composite)

    rng = np.random.default_rng(20260508)
    v0 = jnp.asarray(rng.standard_normal(K))
    p0 = jnp.zeros(K)

    v_traj = [v0]
    state = (v0, p0)
    for _ in range(T + 2):
        state = _step_pinned(O, state, kappa)
        v_traj.append(state[0])

    v_arr = np.stack([np.asarray(v) for v in v_traj], axis=0)  # (T+3, K)

    for t in range(T):
        ddot_v = v_arr[t + 2] - 2.0 * v_arr[t + 1] + v_arr[t]
        v_aug = np.concatenate([[0.0], v_arr[t], [0.0]])
        laplacian = v_aug[:-2] - 2.0 * v_aug[1:-1] + v_aug[2:]
        residual = m * ddot_v - kappa * laplacian + (m0 * m0) * v_arr[t]
        np.testing.assert_allclose(residual, np.zeros(K), atol=1e-10)


def test_kg_dispersion():
    """Pinned-chain Dirichlet eigenmodes: initialize in eigenmode ``n``,
    evolve two steps, and check ``ddot v_j(0) / v_j(0)`` matches the
    predicted ``-omega_n^2`` to 1e-10.

    For pinned chain of length K, modes are
    ``v_j^{(n)} = sin(j n pi / (K+1))`` (j = 1, ..., K), with

        omega_n^2 = m_0^2 / m + (kappa / m) * 4 sin^2(n pi / (2(K+1))).

    The recurrence
        m * ddot v_j(t) = kappa (v_{j-1} - 2 v_j + v_{j+1})(t) - m_0^2 v_j(t)
    applied to a Dirichlet mode gives
        ddot v_j(0) = -omega_n^2 v_j(0)
    exactly (up to floating point), so this is a sharp identity test of
    the dispersion relation.
    """
    K = 7
    m, kappa, m0 = 1.3, 0.8, 0.5

    Part = _kg_particle(m=m, kappa=kappa, m0=m0)
    composite = compose_chain([Part] * K)
    O = Phi(composite)

    js = np.arange(1, K + 1)  # 1-indexed lattice sites
    for n in range(1, K + 1):
        v0 = jnp.asarray(np.sin(js * n * np.pi / (K + 1)))
        p0 = jnp.zeros(K)
        state = (v0, p0)
        v_traj = [v0]
        for _ in range(2):
            state = _step_pinned(O, state, kappa)
            v_traj.append(state[0])
        v_arr = np.stack([np.asarray(v) for v in v_traj], axis=0)  # (3, K)
        ddot_v = v_arr[2] - 2.0 * v_arr[1] + v_arr[0]
        omega2_pred = (m0 * m0) / m + (kappa / m) * 4.0 * np.sin(
            n * np.pi / (2.0 * (K + 1))
        ) ** 2
        # Identity expected: ddot v_j(0) = -omega_n^2 * v_j(0).
        ratio_lhs = ddot_v
        ratio_rhs = -omega2_pred * np.asarray(v0)
        np.testing.assert_allclose(ratio_lhs, ratio_rhs, atol=1e-10)


# ---------------------------------------------------------------------------
# Long-horizon divergence diagnostic (slow; opt-in).
# ---------------------------------------------------------------------------


@pytest.mark.slow
@pytest.mark.skipif(
    not os.environ.get("RUN_SLOW"),
    reason="long-horizon divergence diagnostic; set RUN_SLOW=1 to enable",
)
def test_kg_long_horizon_divergence():
    """Document the explicit-Euler-of-Hamiltonian-flow instability for KG.

    Simulates T = 200 pinned-end steps from a small random perturbation
    and prints the step at which max |v| first exceeds 10x, 100x, 1000x
    the initial peak. Mirrors the wave-equation behaviour described near
    eqn.state_update in the paper (the recurrence is an algebraic identity,
    not a stable time-stepper).
    """
    K = 5
    T = 200
    m, kappa, m0 = 1.5, 0.9, 0.3

    Part = _kg_particle(m=m, kappa=kappa, m0=m0)
    composite = compose_chain([Part] * K)
    O = Phi(composite)

    rng = np.random.default_rng(20260508)
    v0 = jnp.asarray(1e-3 * rng.standard_normal(K))
    p0 = jnp.zeros(K)
    state = (v0, p0)
    peak0 = float(np.max(np.abs(np.asarray(v0))))

    crossings = {10: None, 100: None, 1000: None}
    log = [(0, peak0)]
    for t in range(1, T + 1):
        state = _step_pinned(O, state, kappa)
        v_now = np.asarray(state[0])
        peak = float(np.max(np.abs(v_now)))
        log.append((t, peak))
        for thresh in (10, 100, 1000):
            if crossings[thresh] is None and peak > thresh * peak0:
                crossings[thresh] = t

    print(f"[KG long-horizon] peak0 = {peak0:.3e}")
    for thresh, t in crossings.items():
        if t is None:
            print(f"  threshold {thresh}x not reached within T={T}")
        else:
            _, peak_at = log[t]
            print(f"  threshold {thresh}x crossed at step {t} (peak = {peak_at:.3e})")
    print(f"  final peak (t={T}) = {log[-1][1]:.3e}")
