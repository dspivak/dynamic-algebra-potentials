"""Golden end-to-end test: the chain-of-K-particles wave equation.

References sec.spring of dynamic-algebra-potentials.tex:

* particle setup: sec.spring_first_pass (eqn.para_potential_lens_maps).
* state-update equation: ``eqn.potlens_composite_final``.
* discrete wave equation with pinned ends: ``eqn.discrete_wave``,
  ``eqn.wave_pin``, ``eqn.wave_bc``, ``eqn.state_update_explicit``.
"""

import jax
import jax.numpy as jnp
import numpy as np

from dap.functors import Phi
from dap.lens import PotLensMap
from dap.pvect import diagonal_pvect
from dap.wiring import compose_chain


def _harmonic_particle(m: float, kappa: float) -> PotLensMap:
    """Single-particle PotLens of sec.spring_first_pass:

    V = R with sharp(p) = p/m, out_f = id, in_f vacuous,
    U(x, y) = (kappa/2)(x - y)^2.
    """
    V = diagonal_pvect(jnp.array([1.0 / m]))

    def out_f(v, m_out):
        return v  # identity (paper line 2366)

    def in_f(v, m_out, n_in):
        return jnp.zeros(0)

    def U(v, m_out, n_in):
        diff = v[0] - n_in[0]
        return 0.5 * kappa * diff * diff

    return PotLensMap(
        V=V, out_dim_M=0, in_dim_M=0, out_dim_N=1, in_dim_N=1,
        out_f=out_f, in_f=in_f, U=U, label="Part",
    )


def _potlens_composite_final(v, p, v_prev_extern, xi_N_extern, m, kappa):
    """Reference implementation of ``eqn.potlens_composite_final``."""
    K = v.shape[0]
    v_new = v + p / m
    # p'_i = p_i + kappa(v_{i-1} + v_{i+1} - 2 v_i)  for 1 <= i < K
    # p'_K = p_K + kappa(v_{K-1} - v_K) - xi_N
    # with v_0 := v_prev_extern.
    p_new = jnp.zeros_like(p)
    # Build the surrounding-neighbor arrays:
    v_left = jnp.concatenate([jnp.array([v_prev_extern]), v[:-1]])  # (v_0, v_1, ..., v_{K-1})
    v_right_interior = v[2:K]                                       # v_{i+1} for i=1..K-2 (zero-indexed 0..K-3)
    # For i = 0..K-2 (1..K-1 in 1-indexed): p'_i = p_i + kappa(v_{i-1} + v_{i+1} - 2 v_i).
    p_new_interior = (
        p[:K - 1]
        + kappa * (v_left[:K - 1] + jnp.concatenate([v[1:K - 1], jnp.array([0.0])])
                   - 2.0 * v[:K - 1])
    )
    # Re-do interior more cleanly with explicit loop logic:
    p_new = []
    for i in range(K):
        if i < K - 1:
            v_prev = v_prev_extern if i == 0 else v[i - 1]
            v_next = v[i + 1]
            p_i_new = p[i] + kappa * (v_prev + v_next - 2.0 * v[i])
        else:
            v_prev = v[i - 1] if K > 1 else v_prev_extern
            p_i_new = p[i] + kappa * (v_prev - v[i]) - xi_N_extern
        p_new.append(p_i_new)
    p_new = jnp.stack(p_new)
    return v_new, p_new


def test_state_update_matches_potlens_composite_final():
    """Apply Phi to a 5-particle chain; check eqn.potlens_composite_final."""
    K = 5
    m, kappa = 1.7, 2.3
    Part = _harmonic_particle(m=m, kappa=kappa)
    composite = compose_chain([Part] * K)
    O = Phi(composite)

    # Source poly is yon (composite has out_dim_M=0, in_dim_M=0). The
    # src position has the 0-dim out_m and a 0-dim affine omega_M.
    in_pos = (jnp.zeros(0), (jnp.zeros((0, 0)), jnp.zeros(0)))

    rng = np.random.default_rng(20260507)
    for trial in range(5):
        v = jnp.asarray(rng.standard_normal(K))
        p = jnp.asarray(rng.standard_normal(K))
        v_prev = float(rng.standard_normal())
        xi_N = float(rng.standard_normal())

        org = O.with_state((v, p))
        in_dir = (jnp.array([xi_N]), jnp.array([v_prev]))
        out_pos, out_dir, new_state = org.run_one(in_pos, lambda _op: in_dir)
        new_v, new_p = new_state

        ref_v, ref_p = _potlens_composite_final(v, p, v_prev, xi_N, m, kappa)
        np.testing.assert_allclose(np.asarray(new_v), np.asarray(ref_v), atol=1e-10)
        np.testing.assert_allclose(np.asarray(new_p), np.asarray(ref_p), atol=1e-10)


def test_omega_N_is_harmonic_spring_field():
    """eqn.omegaprime / paper line 2418: omega_N(v_0) = -kappa(v_1 - v_0)
    for the chain composite, i.e. affine ``A_N = kappa, b_N = -kappa v_1``."""
    K = 5
    m, kappa = 1.0, 0.7
    Part = _harmonic_particle(m=m, kappa=kappa)
    composite = compose_chain([Part] * K)
    O = Phi(composite)

    v = jnp.array([0.4, -0.2, 1.1, 0.0, 2.3])
    p = jnp.zeros(K)
    org = O.with_state((v, p))

    act, fiber = O.step(org.state)
    in_pos = (jnp.zeros(0), (jnp.zeros((0, 0)), jnp.zeros(0)))
    out_pos, _ = fiber(in_pos)
    out_n, omega_N = out_pos
    A_N, b_N = omega_N
    np.testing.assert_allclose(np.asarray(out_n), np.asarray(v[K - 1:K]), atol=1e-10)
    # omega_N(v_0) = kappa*v_0 - kappa*v_1 = A_N v_0 + b_N
    np.testing.assert_allclose(np.asarray(A_N), np.array([[kappa]]), atol=1e-10)
    np.testing.assert_allclose(np.asarray(b_N), np.array([-kappa * float(v[0])]),
                               atol=1e-10)


def test_discrete_wave_equation_with_pinned_ends():
    """eqn.discrete_wave: m * (v_i(t+2) - 2 v_i(t+1) + v_i(t)) =
    kappa * (v_{i-1}(t) - 2 v_i(t) + v_{i+1}(t)) for interior i, all t.

    Uses the boundary conditions of eqn.wave_bc with L = 0:
    v_0(t) := 0, xi_N(t) := kappa * v_K(t) (so v_{K+1} := 0).
    """
    K = 5
    # The paper's update rule (eqn.potlens_composite_final) is a parallel
    # explicit-Euler step in (v, p), which is unconditionally unstable for
    # SHM: |v| grows ~exponentially. The discrete wave equation
    # eqn.discrete_wave is an *algebraic identity* of the recurrence, valid
    # at every step regardless of stability. We use a short horizon so
    # absolute residuals stay near float64 precision.
    T = 10
    m, kappa = 1.5, 0.9

    Part = _harmonic_particle(m=m, kappa=kappa)
    composite = compose_chain([Part] * K)
    O = Phi(composite)

    rng = np.random.default_rng(42)
    v0 = jnp.asarray(rng.standard_normal(K))
    p0 = jnp.zeros(K)

    # Trajectory storage for v.
    v_traj = [v0]
    state = (v0, p0)
    in_pos = (jnp.zeros(0), (jnp.zeros((0, 0)), jnp.zeros(0)))

    for _ in range(T + 2):
        v, p = state
        # Boundary conditions: v_prev = 0, xi_N = kappa * v_K (L = 0).
        v_prev = jnp.array([0.0])
        xi_N = jnp.array([kappa * float(v[K - 1])])
        in_dir = (xi_N, v_prev)
        org = O.with_state(state)
        _, _, new_state = org.run_one(in_pos, lambda _op: in_dir)
        state = new_state
        v_traj.append(state[0])

    v_arr = np.stack([np.asarray(v) for v in v_traj], axis=0)  # (T+3, K)

    # Check the discrete wave equation for every interior i and every t.
    for t in range(T):
        ddot_v = v_arr[t + 2] - 2.0 * v_arr[t + 1] + v_arr[t]
        # Augmented v with pinned ends:
        v_aug = np.concatenate([[0.0], v_arr[t], [0.0]])
        laplacian = v_aug[:-2] - 2.0 * v_aug[1:-1] + v_aug[2:]  # length K
        residual = m * ddot_v - kappa * laplacian
        np.testing.assert_allclose(residual, np.zeros(K), atol=1e-10)
