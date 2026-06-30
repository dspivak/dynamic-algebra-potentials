"""Faithfulness + integration tests for Generator 3, the activation cell.

Pins the ``AUDIT.md`` A' checklist (G1-G5) and the operad integration of ``Act``.
Run from the repo root:

    PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m pytest \
        sensemaking/kqv/test_activation_cell.py -q
"""

import inspect

import jax
jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp
import numpy as np
import pytest

from dap.functors import Phiconf, Phiphase
from dap.interpretation import smooth_interpretation, trivial_omega

from sensemaking.kqv import (
    Act,
    Head,
    Sub,
    act_block_sharp,
    act_param_dim,
    act_unpack,
    activation_cell,
    leaf,
    open_boxes,
    param_dim,
    realize,
    target_boxes,
    trace,
    width,
)

RNG = np.random.default_rng(0)
E, k, d, d_v = 4, 2, 3, 2


def rand(n):
    return jnp.asarray(RNG.standard_normal(n))


# ---- G2: shapes + the uniform residual interface --------------------------


def test_cell_shapes_and_interface():
    cell = realize(Act(E, k))
    assert (cell.out_dim_M, cell.in_dim_M, cell.out_dim_N, cell.in_dim_N) == (E, E, E, E)
    # carrier Q = Z (+) Hom(R^k, R^E): dim = k + E*k
    assert cell.Q.dim == act_param_dim(E, k) == k + E * k


# ---- G1: the carrier (z, D) lives in Q; D is learned ----------------------


def test_carrier_z_and_D_live_in_Q():
    cell = realize(Act(E, k))
    q = rand(cell.Q.dim)
    P = act_unpack(q, E, k)
    assert P["z"].shape == (k,) and P["D"].shape == (E, k)  # Z (+) Hom(R^k,R^E)
    # D is *in* Q: perturbing the D-block of q changes the read-out (D is not a constant
    # smuggled outside Q -- AUDIT G1).
    h = jnp.zeros(E)
    q2 = q.at[k:].add(1.0)  # bump the D block only
    assert not jnp.allclose(cell.out_f(q, h), cell.out_f(q2, h))
    # ... and perturbing the z-block changes it too (z is in Q).
    q3 = q.at[:k].add(1.0)
    assert not jnp.allclose(cell.out_f(q, h), cell.out_f(q3, h))


# ---- G2: out_f = Dz, Moore (no n); in_f = n; U = 1/2||h-Dz||^2 ------------


def test_out_f_is_moore_and_equals_Dz():
    cell = realize(Act(E, k))
    # Moore: out_f takes exactly (q, m_out) -- structurally cannot see n (rmk.moore).
    assert list(inspect.signature(cell.out_f).parameters) == ["q", "m_out"]
    q, h = rand(cell.Q.dim), rand(E)
    P = act_unpack(q, E, k)
    assert jnp.allclose(cell.out_f(q, h), P["D"] @ P["z"])
    # interpreted read-out matches out_f, with no descending input anywhere
    pos, _ = smooth_interpretation(cell)(q)
    out_n, _ = pos(h, trivial_omega(E))
    assert jnp.allclose(out_n, cell.out_f(q, h))


def test_in_f_is_transparent():
    cell = realize(Act(E, k))
    q, h, n = rand(cell.Q.dim), rand(E), rand(E)
    assert jnp.allclose(cell.in_f(q, h, n), n)  # in_f(z,D;h,n) = n


def test_potential_is_reconstruction_error():
    cell = realize(Act(E, k))
    q, h, n = rand(cell.Q.dim), rand(E), rand(E)
    P = act_unpack(q, E, k)
    Dz = P["D"] @ P["z"]
    # type Q x out_M x in_N -> R, scalar (A3); value 1/2||h - Dz||^2
    val = cell.U(q, h, n)
    assert jnp.ndim(val) == 0
    assert jnp.allclose(val, 0.5 * jnp.sum((h - Dz) ** 2))
    assert float(val) >= 0.0
    # zero iff h = Dz (clamp h to the prediction)
    assert float(cell.U(q, Dz, n)) < 1e-12
    # n is ignored by the default (bottom-up) U
    assert jnp.allclose(cell.U(q, h, n), cell.U(q, h, rand(E)))


def test_top_down_term_is_optional_and_symmetric():
    cell = realize(Act(E, k, top_down=True))
    q, h, n = rand(cell.Q.dim), rand(E), rand(E)
    P = act_unpack(q, E, k)
    Dz = P["D"] @ P["z"]
    expect = 0.5 * jnp.sum((h - Dz) ** 2) + 0.5 * jnp.sum((Dz - n) ** 2)
    assert jnp.allclose(cell.U(q, h, n), expect)  # symmetric Rao-Ballard cell


# ---- G3: the carrier is a vector space ------------------------------------


def test_carrier_is_rvect():
    cell = realize(Act(E, k))
    # Z and Hom(R^k,R^E) are R-vect: Q.dim finite, the sharp is a real (dim,dim) matrix
    # (a discrete carrier would not present a smooth sharp).  AUDIT G3.
    S = cell.Q.sharp_at(jnp.zeros(cell.Q.dim))
    assert S.shape == (cell.Q.dim, cell.Q.dim)
    assert jnp.all(jnp.isfinite(S))


# ---- G4: the fast/slow split is the BLOCK SHARP (data of Q) ----------------


def test_block_sharp_is_data_of_Q():
    eta_z, eta_D = 10.0, 0.1
    S = act_block_sharp(E, k, eta_z, eta_D).sharp_at(jnp.zeros(act_param_dim(E, k)))
    diag = jnp.diag(S)
    assert jnp.allclose(diag[:k], eta_z)          # z block fast
    assert jnp.allclose(diag[k:], eta_D)          # D block slow
    assert jnp.allclose(S - jnp.diag(diag), 0.0)  # purely diagonal: no off-block coupling
    # the cell built with it carries it as its OWN sharp (no optimizer object outside Q)
    cell = realize(Act(E, k, sharp=act_block_sharp(E, k, eta_z, eta_D)))
    assert jnp.allclose(cell.Q.sharp_at(jnp.zeros(cell.Q.dim)), S)


# ---- G5: arity-1 generator, substitutes via the SAME operad ops -----------


def test_act_is_arity1_and_substitutes_both_ways():
    assert Act(E, k).N == 1                       # arity-1 generator
    assert open_boxes(Act(E, k)) == 1
    assert width(Act(E, k)) == E and target_boxes(Act(E, k)) == 1

    # cell as a parent (Sub.parent generalized to a generator) and as a child
    parent = Sub(Act(E, k), (Head(1, E, d, d_v),))
    child = Sub(Head(1, E, d, d_v), (Act(E, k),))
    for t in (parent, child):
        arr = realize(t)
        # Q is the direct sum of the node carriers (independent count), iface uniform R^E
        assert arr.Q.dim == act_param_dim(E, k) + param_dim(E, d, d_v)
        assert (arr.out_dim_N, arr.in_dim_N) == (E, E)
        # runs under both dynamics functors (no new operation needed -- compose_seq only)
        for O in (Phiconf(arr), Phiphase(arr)):
            src = (jnp.zeros(arr.out_dim_M), trivial_omega(arr.in_dim_M))
            bnd = lambda op: (jnp.zeros(E), jnp.zeros(E))  # noqa: E731
            s, out = O.state, None
            for _ in range(3):
                out, _, s = O.with_state(s).run_one(src, bnd)
            assert jnp.all(jnp.isfinite(out[0]))


def test_sub_parent_validation_covers_cells():
    # an Act parent enforces the same arity/width contract as a Head parent
    with pytest.raises(ValueError):
        Sub(Act(E, k), (leaf(E), leaf(E)))         # arity-1 cell, two children
    with pytest.raises(ValueError):
        Sub(Act(E, k), (leaf(E + 1),))             # width mismatch
    # provenance trace distinguishes a cell parent from a head parent
    tr = trace(Sub(Act(E, k), (Head(1, E, d, d_v),)))
    assert "cell(k=2)" in tr


def test_q_is_direct_sum_in_an_interleaved_tower():
    # data -> head(2) -> cell -> head(1) -> cell(top): Q is the direct sum of all carriers
    bottom = Head(2, E, d, d_v)
    t = Sub(Act(E, k), (Sub(Head(1, E, d, d_v), (Sub(Act(E, k), (bottom,)),)),))
    arr = realize(t)
    expected = (
        param_dim(E, d, d_v)        # bottom head(2)
        + act_param_dim(E, k)       # lower cell
        + param_dim(E, d, d_v)      # middle head(1)
        + act_param_dim(E, k)       # top cell
    )
    assert arr.Q.dim == expected
    assert open_boxes(t) == 2       # the bottom head's two open data slots


# ---- the bilinear dead zone, at the atom (the scientific unit check) -------


def _run_cell(cell, h, n, init, steps):
    """Relax a single clamped cell under Phiconf; return the U trajectory."""
    O = Phiconf(cell)
    src = (h, trivial_omega(E))                    # child emission clamped = h
    bnd = lambda op: (jnp.zeros(E), n)             # noqa: E731  (apex context)
    s, Us = init, [float(cell.U(init, h, n))]
    for _ in range(steps):
        _, _, s = O.with_state(s).run_one(src, bnd)
        Us.append(float(cell.U(s, h, n)))
    return np.array(Us)


def test_atom_zero_init_is_a_stationary_point():
    # SPEC "Bilinear dead zone": at (z=0, D=0) both gradients vanish (each is
    # proportional to the OTHER block), so Phiconf cannot move -- U is frozen at
    # 1/2||h||^2.  This is the dead zone the near-zero-init tower test probes.
    cell = realize(Act(E, k, sharp=act_block_sharp(E, k, 0.3, 0.1)))
    h, n = rand(E), jnp.zeros(E)
    Us = _run_cell(cell, h, n, jnp.zeros(cell.Q.dim), steps=80)
    assert jnp.allclose(Us, 0.5 * float(jnp.sum(h ** 2)))  # frozen at 1/2||h||^2


def test_z_prior_term_and_breaks_the_dead_zone():
    # The sanctioned z-prior is a route-2 POTENTIAL term: U gains 1/2 lam||z - mu0||^2.
    mu0 = jnp.array([0.7, -0.4])
    base = realize(Act(E, k, sharp=act_block_sharp(E, k, 0.3, 0.1)))
    pri = realize(Act(E, k, sharp=act_block_sharp(E, k, 0.3, 0.1), prior_mu=mu0, prior_lambda=1.3))
    q, h, n = rand(base.Q.dim), rand(E), rand(E)
    z = act_unpack(q, E, k)["z"]
    assert jnp.allclose(pri.U(q, h, n) - base.U(q, h, n), 0.5 * 1.3 * jnp.sum((z - mu0) ** 2))
    # ... and with mu0 != 0 the all-zero state is NO LONGER stationary: from zero init the
    # cell now MOVES (dU/dz|_{z=0} = -lam*mu0 != 0), unlike the bare atom (frozen above).
    Us = _run_cell(pri, h, n, jnp.zeros(pri.Q.dim), steps=60)
    assert Us[-1] < Us[0] - 1e-6           # the prior kicks the state off the dead zone


def test_atom_escapes_from_random_init():
    # SPEC "Bare cell (the atom)": (0,0) is a SADDLE, not a min -- from a generic init
    # Phiconf descends well below 1/2||h||^2 (the cell reconstructs the clamped h).
    # So the atom does NOT collapse; the collapse risk is a tower-level question.
    cell = realize(Act(E, k, sharp=act_block_sharp(E, k, 0.3, 0.1)))
    h, n = rand(E), jnp.zeros(E)
    init = jnp.asarray(np.random.default_rng(3).standard_normal(cell.Q.dim)) * 0.3
    Us = _run_cell(cell, h, n, init, steps=1000)
    assert all(np.isfinite(Us))
    assert Us[-1] < 1e-6 * (0.5 * float(jnp.sum(h ** 2)))  # escaped the saddle, reconstructs h
