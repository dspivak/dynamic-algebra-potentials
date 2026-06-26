"""Operad-law and faithfulness tests for the KQV suboperad (Task 0; AUDIT.md A,B).

Each test cites the law it pins down.  Run from the repo root:

    PYTHONPATH=$(pwd) misc/dap/.venv/bin/python -m pytest \
        sensemaking/kqv/test_operad_laws.py -q
"""

import inspect

import jax
jax.config.update("jax_enable_x64", True)  # exact comparisons need float64

import jax.numpy as jnp
import numpy as np
import pytest

from dap.functors import Phiconf, Phiphase
from dap.interpretation import smooth_interpretation, trivial_omega
from dap.rvect import euclidean
from dap.wiring import compose_seq

from sensemaking.kqv import (
    Head,
    Sub,
    attention_head,
    flat,
    leaf,
    open_boxes,
    param_dim,
    realize,
    unpack,
)

RNG = np.random.default_rng(0)
E, d, d_v = 4, 3, 2


def rand(n):
    return jnp.asarray(RNG.standard_normal(n))


def _run_closed(O, steps=3):
    """Step a closed-bottom arrangement (source <0|0>); world feeds zeros at the root."""
    in_pos = (jnp.zeros(0), trivial_omega(0))
    s, out_pos = O.state, None
    for _ in range(steps):
        out_pos, _, s = O.with_state(s).run_one(
            in_pos, lambda op: (jnp.zeros(E), jnp.zeros(E))
        )
    assert jnp.all(jnp.isfinite(out_pos[0]))


# ---- A. faithfulness ------------------------------------------------------


def test_head_shapes_and_arity_independent_weights():
    h2 = attention_head(2, E, d, d_v)
    assert (h2.out_dim_M, h2.in_dim_M, h2.out_dim_N, h2.in_dim_N) == (2 * E, 2 * E, E, E)
    assert h2.Q.dim == param_dim(E, d, d_v)
    # one head applies to any arity: weight count is arity-independent (rmk.supertoken)
    assert attention_head(5, E, d, d_v).Q.dim == h2.Q.dim


def test_uniform_residual_interface():
    # both legs of every box are R^E, so any term substitutes into any box (obs.residual)
    for term in [Head(3, E, d, d_v), leaf(E), flat(2, E, d, d_v)]:
        arr = realize(term)
        assert arr.out_dim_N == E and arr.in_dim_N == E


def test_moore_out_f_has_no_input():
    # out_f takes exactly (q, m_out): the read-out structurally cannot see n (rmk.moore).
    # (The name of the second arg may be renamed by composition, e.g. dap's `l_out`;
    #  what matters is the arity -- there is no descending-input argument.)
    head = attention_head(3, E, d, d_v)
    assert list(inspect.signature(head.out_f).parameters) == ["q", "m_out"]
    arr = realize(flat(3, E, d, d_v))
    assert len(inspect.signature(arr.out_f).parameters) == 2
    # the interpreted read-out equals out_f(q, m_out), with no descending input anywhere
    q = rand(arr.Q.dim)
    pos, _ = smooth_interpretation(arr)(q)
    out_n, _ = pos(jnp.zeros(arr.out_dim_M), trivial_omega(arr.in_dim_M))
    assert jnp.allclose(out_n, arr.out_f(q, jnp.zeros(arr.out_dim_M)))


def test_potential_is_error_unit():
    # U(q, h, n) = 1/2||h - Omega n||^2 >= 0, zero iff h = pred (obs.erroreunit, eq.Uattn)
    arr = attention_head(2, E, d, d_v)
    q, n = rand(arr.Q.dim), rand(E)
    W = unpack(q, E, d, d_v)
    pred = W["Wo"] @ (W["Wv"] @ n)  # Omega n
    h_pred = jnp.concatenate([pred, pred])  # both boxes sit at the prediction
    assert float(arr.U(q, h_pred, n)) < 1e-12
    h_off = h_pred + rand(2 * E) * 0.1
    assert float(arr.U(q, h_off, n)) > 0.0
    assert jnp.ndim(arr.U(q, h_off, n)) == 0  # scalar


# ---- B. operadic integrity ------------------------------------------------


def test_sigma_equivariance():
    # permuting inner boxes leaves out_f invariant and permutes in_f's rows (obs.equivariance)
    N = 4
    arr = attention_head(N, E, d, d_v)
    q, n = rand(arr.Q.dim), rand(E)
    h = RNG.standard_normal((N, E))
    perm = RNG.permutation(N)
    hp = h[perm]
    assert jnp.allclose(
        arr.out_f(q, jnp.asarray(h).reshape(-1)),
        arr.out_f(q, jnp.asarray(hp).reshape(-1)),
    )
    o = arr.in_f(q, jnp.asarray(h).reshape(-1), n).reshape(N, E)
    op = arr.in_f(q, jnp.asarray(hp).reshape(-1), n).reshape(N, E)
    assert jnp.allclose(op, o[perm])


def test_substitution_typechecks_and_runs():
    arr = realize(flat(3, E, d, d_v))
    assert (arr.out_dim_M, arr.in_dim_M) == (0, 0)  # closed at the bottom
    assert (arr.out_dim_N, arr.in_dim_N) == (E, E)  # open to the world at the root
    assert arr.Q.dim == param_dim(E, d, d_v) + 3 * E  # parameter is the direct sum
    _run_closed(Phiconf(arr))
    _run_closed(Phiphase(arr))


def test_arbitrary_depth_mixed_arity():
    # depth-3 closed tree, mixed arities; no silent depth cap (AUDIT B3)
    sub2 = Sub(Head(2, E, d, d_v), (leaf(E), leaf(E)))
    sub3 = Sub(Head(3, E, d, d_v), (leaf(E), leaf(E), leaf(E)))
    mid = Sub(Head(2, E, d, d_v), (sub2, sub3))
    root = Sub(Head(2, E, d, d_v), (mid, leaf(E)))
    arr = realize(root)
    assert (arr.out_dim_M, arr.out_dim_N) == (0, E)
    assert open_boxes(root) == 0
    _run_closed(Phiconf(arr))
    _run_closed(Phiphase(arr))


def test_deep_relaxation_is_well_posed_from_random_init():
    # The benign zero-init runs above only certify type-correctness at a trivial fixed
    # point. Here we exercise the *dynamics*: a deep tree from a NON-TRIVIAL random
    # init, with a sensible small-eta sharp (the optimizer knob, rmk.optimizer).
    # Phiconf must descend U (genuine relaxation); Phiphase must stay bounded.
    # Well-posedness is conditional on the step size: at the default eta=1, explicit
    # GD overshoots and diverges, exactly as standard gradient descent; the
    # conservative phase step has its own (smaller) stability threshold (see SPEC.md).
    rng = np.random.default_rng(7)  # local seed: deterministic, order-independent

    def build(eta):
        hs = euclidean(param_dim(E, d, d_v), eta)
        H = lambda N: Head(N, E, d, d_v, sharp=hs)  # noqa: E731
        L = lambda: leaf(E, sharp=euclidean(E, eta))  # noqa: E731
        return realize(Sub(H(2), (Sub(H(2), (L(), L())), Sub(H(3), (L(), L(), L())))))

    src = (jnp.zeros(0), trivial_omega(0))
    n_world = jnp.asarray(rng.standard_normal(E))  # fixed descending context
    boundary = lambda op: (jnp.zeros(E), n_world)  # noqa: E731

    # Phiconf at a sensible step size descends U from a non-trivial init.
    arr = build(1e-2)
    q0 = jnp.asarray(rng.standard_normal(arr.Q.dim)) * 0.3
    potential = lambda q: float(arr.U(q, jnp.zeros(0), n_world))  # noqa: E731
    O, s, Us = Phiconf(arr), q0, []
    for _ in range(300):
        Us.append(potential(s))
        _, _, s = O.with_state(s).run_one(src, boundary)
    assert all(np.isfinite(u) for u in Us)
    assert Us[0] > 1e-3  # init was non-degenerate (not already at the minimum)
    assert Us[-1] < 0.9 * Us[0]  # genuine relaxation, not a frozen fixed point

    # Phiphase (conservative) at a smaller step size stays bounded -- no blow-up.
    arrp = build(1e-3)
    qp = jnp.asarray(rng.standard_normal(arrp.Q.dim)) * 0.1
    Op, sp, peak = Phiphase(arrp), (qp, jnp.zeros(arrp.Q.dim)), 0.0
    for _ in range(200):
        out_pos, _, sp = Op.with_state(sp).run_one(src, boundary)
        assert jnp.all(jnp.isfinite(out_pos[0]))
        peak = max(peak, float(jnp.max(jnp.abs(out_pos[0]))))
    assert peak < 50.0


def test_functoriality_of_F():
    # F preserves composition: Phiconf(g . f) == Phiconf(f).then(Phiconf(g)), at random params.
    # Compared on the forward read-out AND the backward covector (out_dir).
    f = attention_head(1, E, d, d_v, label="f")
    g = attention_head(1, E, d, d_v, label="g")
    O_seq = Phiconf(compose_seq(f, g))
    O_then = Phiconf(f).then(Phiconf(g))

    qf, qg = rand(f.Q.dim), rand(g.Q.dim)
    in_pos = (rand(E), trivial_omega(E))

    # freeze the boundary so both sides see identical (xi_N, in_n)
    xiN, inn = rand(E), rand(E)
    boundary = lambda op: (xiN, inn)  # noqa: E731

    o_seq, d_seq, _ = O_seq.with_state(jnp.concatenate([qf, qg])).run_one(in_pos, boundary)
    o_then, d_then, _ = O_then.with_state((qf, qg)).run_one(in_pos, boundary)

    assert jnp.allclose(o_seq[0], o_then[0])  # forward read-out agrees
    assert jnp.allclose(d_seq[0], d_then[0])  # backward xi_M agrees
    assert jnp.allclose(d_seq[1], d_then[1])  # backward in_m agrees


# ---- membership by construction -------------------------------------------


def test_realize_rejects_non_terms():
    with pytest.raises(TypeError):
        realize(attention_head(1, E, d, d_v))  # a raw SmoothArrangement is not a KQVTerm
    with pytest.raises(TypeError):
        realize(42)


def test_sub_validates_arity_and_width():
    with pytest.raises(ValueError):
        Sub(Head(2, E, d, d_v), (leaf(E),))  # wrong child count
    with pytest.raises(ValueError):
        Sub(Head(2, E, d, d_v), (leaf(E), leaf(E + 1)))  # width mismatch
    with pytest.raises(ValueError):
        Sub(leaf(E), ())  # a 0-ary box cannot be a parent
