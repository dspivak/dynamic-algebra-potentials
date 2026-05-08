"""One functoriality witness per functor in the chain (per task spec)."""

import jax.numpy as jnp
import numpy as np

from dap.functors import (
    Lens_cot,
    Phi,
    T,
    Tstar,
    _UnparamLens,
    cint,
    cot_map,
    cot_object,
    dyn,
    leg,
)
from dap.lens import PotLensMap
from dap.pvect import PairedVectorSpace, diagonal_pvect


def test_T_endofunctor_doubles_dim():
    """prop.TT_endofunctors: ``T V = V (+) V``."""
    V = diagonal_pvect(jnp.array([2.0, 3.0]))
    TV = T(V)
    assert TV.V_dim == 4
    np.testing.assert_allclose(
        TV.sharp,
        jnp.diag(jnp.array([2.0, 3.0, 2.0, 3.0])),
        atol=1e-10,
    )


def test_Tstar_canonical_symplectic_sharp():
    """prop.TT_endofunctors / eqn.canonical_sharp: ``T*V`` has sharp(xi,v)=(v,-xi)."""
    V = diagonal_pvect(jnp.array([1.0]))
    TsV = Tstar(V)
    assert TsV.V_dim == 2
    # sharp_{T*V} . (xi, v) = (v, -xi)
    np.testing.assert_allclose(TsV.sharp @ jnp.array([3.0, 7.0]),
                               jnp.array([7.0, -3.0]), atol=1e-10)


def test_Lens_cot_smoke():
    """lem.cot_lifts_lens_potential: Lens(cot) preserves smooth-data shape on R^d."""
    L = _UnparamLens(
        out_dim_M=1, in_dim_M=1, out_dim_N=1, in_dim_N=1,
        out_f=lambda m: m,
        in_f=lambda m, n: m,
        U=lambda m, n: jnp.sum(m * n),
    )
    LL = Lens_cot(L)
    # Just check the shape invariants.
    assert LL.out_dim_M == 1 and LL.in_dim_N == 1
    np.testing.assert_allclose(LL.U(jnp.array([2.0]), jnp.array([3.0])), 6.0)


def _harmonic_particle(m: float, kappa: float) -> PotLensMap:
    """Single-particle PotLens of sec.spring_first_pass."""
    V = diagonal_pvect(jnp.array([1.0 / m]))  # sharp(p) = p/m

    def out_f(v, m_out):
        return v  # identity (eqn.para_potential_lens_maps with M_out trivial)

    def in_f(v, m_out, n_in):
        return jnp.zeros(0)

    def U(v, m_out, n_in):
        # U(x, y) = (kappa/2) (x - y)^2; v plays the role of x, n_in is y.
        diff = v[0] - n_in[0]
        return 0.5 * kappa * diff * diff

    return PotLensMap(
        V=V, out_dim_M=0, in_dim_M=0, out_dim_N=1, in_dim_N=1,
        out_f=out_f, in_f=in_f, U=U, label="Part",
    )


def test_cint_carries_the_data_through():
    """lem.potlens_to_para_poly: cint forwards the V/sharp/smooth-data."""
    P = _harmonic_particle(m=2.0, kappa=3.0)
    out = cint(P)
    assert out.V.V_dim == 1
    np.testing.assert_allclose(out.V.sharp, jnp.array([[0.5]]), atol=1e-10)


def test_leg_state_space_is_T_star_V():
    """lem.para_rho: leg sets the state-space pvect to T*V."""
    P = _harmonic_particle(m=1.5, kappa=2.0)
    out = leg(cint(P))
    assert out.Vstar_state.V_dim == 2  # = 2 * V_dim


def test_dyn_state_update_one_particle():
    """lem.poly_to_org: dyn realises the unpacked formula of sec.dynamics_functor.

    For a single particle we expect the eqn 2488 formula:
      (v, p) -> (v + p/m, p - xi_N + kappa(v_prev - v))
    on the momentum side, with v_prev supplied via in_dir.
    """
    m, kappa = 2.0, 3.0
    P = _harmonic_particle(m=m, kappa=kappa)
    O = dyn(leg(cint(P)))

    v0 = jnp.array([0.7])
    p0 = jnp.array([1.1])
    org = O.with_state((v0, p0))

    # in_pos = (out_m=(0,), omega_M=(0x0 matrix, 0-vector))
    in_pos = (jnp.zeros(0), (jnp.zeros((0, 0)), jnp.zeros(0)))
    xi_N = jnp.array([0.4])
    v_prev = jnp.array([0.55])
    in_dir = (xi_N, v_prev)

    _, _, new_state = org.run_one(in_pos, lambda _out_pos: in_dir)
    new_v, new_p = new_state
    expected_v = v0 + p0 / m
    expected_p = p0 - xi_N + kappa * (v_prev - v0)
    np.testing.assert_allclose(new_v, expected_v, atol=1e-10)
    np.testing.assert_allclose(new_p, expected_p, atol=1e-10)


def test_Phi_equals_dyn_leg_cint():
    """thm.functor: Phi = cint ; leg ; dyn (composite agrees on smoke input)."""
    P = _harmonic_particle(m=1.0, kappa=1.0)
    O1 = Phi(P)
    O2 = dyn(leg(cint(P)))
    # State spaces and steps should agree on a sample.
    s = (jnp.array([0.3]), jnp.array([-0.2]))
    in_pos = (jnp.zeros(0), (jnp.zeros((0, 0)), jnp.zeros(0)))
    in_dir = (jnp.array([0.1]), jnp.array([0.05]))
    _, _, s1 = O1.with_state(s).run_one(in_pos, lambda _o: in_dir)
    _, _, s2 = O2.with_state(s).run_one(in_pos, lambda _o: in_dir)
    np.testing.assert_allclose(s1[0], s2[0], atol=1e-10)
    np.testing.assert_allclose(s1[1], s2[1], atol=1e-10)
