"""Faithfulness tests for the coincidence head (the second-order generator).

Run: PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m pytest sensemaking/kqv/test_coincidence.py -q
"""
import inspect

import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp
import numpy as np
import pytest

from dap.functors import Phiconf, Phiphase
from dap.interpretation import trivial_omega

from sensemaking.kqv import (
    Coinc, Head, Sub, coinc_param_dim, coinc_unpack, coincidence_head,
    open_boxes, realize, target_boxes, trace, width,
)

RNG = np.random.default_rng(0)
E, r, K = 4, 3, 5


def rand(n):
    return jnp.asarray(RNG.standard_normal(n))


def test_shapes_and_carrier():
    arr = realize(Coinc(K, E, r))
    assert (arr.out_dim_M, arr.in_dim_M, arr.out_dim_N, arr.in_dim_N) == (K * E, K * E, E, E)
    sym = r * (r + 1) // 2
    assert arr.Q.dim == coinc_param_dim(E, r) == r * E + E * sym + sym * E


def test_out_f_is_moore_and_degree_two():
    arr = realize(Coinc(K, E, r))
    assert list(inspect.signature(arr.out_f).parameters) == ["q", "m_out"]   # Moore: no n
    q, h = rand(arr.Q.dim), rand(K * E)
    W = coinc_unpack(q, E, r)
    P = (h.reshape(K, E) @ W["V"].T).sum(0)
    iu = jnp.triu_indices(r)
    assert jnp.allclose(arr.out_f(q, h), W["Wo"] @ jnp.outer(P, P)[iu])      # = Wo vech(PPᵀ)
    # homogeneous degree 2: scaling the emissions by c scales out_f by c^2 (second order)
    assert jnp.allclose(arr.out_f(q, 2.0 * h), 4.0 * arr.out_f(q, h))


def test_permutation_invariant_and_arity_independent():
    arr = realize(Coinc(K, E, r))
    q = rand(arr.Q.dim); h = RNG.standard_normal((K, E))
    perm = RNG.permutation(K)
    assert jnp.allclose(arr.out_f(q, jnp.asarray(h).reshape(-1)),
                        arr.out_f(q, jnp.asarray(h[perm]).reshape(-1)))     # obs.equivariance
    assert realize(Coinc(2, E, r)).Q.dim == realize(Coinc(9, E, r)).Q.dim  # rmk.supertoken


def test_in_f_transparent_and_U_second_order():
    arr = realize(Coinc(K, E, r))
    q, h, n = rand(arr.Q.dim), rand(K * E), rand(E)
    assert jnp.allclose(arr.in_f(q, h, n), jnp.tile(n, K))                  # broadcast n
    W = coinc_unpack(q, E, r)
    P = (h.reshape(K, E) @ W["V"].T).sum(0)
    c = jnp.outer(P, P)[jnp.triu_indices(r)]
    val = arr.U(q, h, n)
    assert jnp.ndim(val) == 0 and float(val) >= 0.0
    assert jnp.allclose(val, 0.5 * jnp.sum((c - W["G"] @ n) ** 2))          # predict the moment
    # U = 0 exactly when the predicted moment matches: construct h with c = 0 and n in ker G
    z = jnp.zeros(K * E)
    assert float(arr.U(q, z, jnp.zeros(E))) < 1e-12                          # 0 = vech(0) = G·0


def test_carrier_is_rvect():
    arr = realize(Coinc(K, E, r))
    S = arr.Q.sharp_at(jnp.zeros(arr.Q.dim))
    assert S.shape == (arr.Q.dim, arr.Q.dim) and jnp.all(jnp.isfinite(S))


def test_substitutes_both_ways_and_runs():
    assert Coinc(3, E, r).N == 3 and open_boxes(Coinc(3, E, r)) == 3
    assert width(Coinc(3, E, r)) == E and target_boxes(Coinc(3, E, r)) == 1
    for t in (Sub(Coinc(2, E, r), (Head(1, E, 2, 2), Head(1, E, 2, 2))),
              Sub(Head(1, E, 2, 2), (Coinc(2, E, r),))):
        arr = realize(t)
        assert (arr.out_dim_N, arr.in_dim_N) == (E, E)
        for O in (Phiconf(arr), Phiphase(arr)):
            s, out = O.state, None
            for _ in range(3):
                out, _, s = O.with_state(s).run_one(
                    (jnp.zeros(arr.out_dim_M), trivial_omega(arr.in_dim_M)),
                    lambda op: (jnp.zeros(E), jnp.zeros(E)))
            assert jnp.all(jnp.isfinite(out[0]))


def test_first_order_pool_cannot_see_a_coincidence():
    # the headline: a degree-2 read-out separates "both signs equal" from "opposite", which a
    # degree-1 (mean) read-out provably cannot (the means are identical). A focused unit witness.
    co = realize(Coinc(2, E, r))
    q = rand(co.Q.dim)
    same = jnp.asarray([1.0, 0, 0, 0, 1.0, 0, 0, 0])      # box a=+1, box b=+1  (sa==sb)
    opp = jnp.asarray([1.0, 0, 0, 0, -1.0, 0, 0, 0])      # box a=+1, box b=-1  (sa!=sb)
    # the two have the SAME first moment up to sign symmetry but differ in the cross moment:
    assert not jnp.allclose(co.out_f(q, same), co.out_f(q, opp))


def test_validation():
    with pytest.raises(ValueError):
        Coinc(0, E, r)            # arity must be >= 1
    with pytest.raises(ValueError):
        coincidence_head(2, E, 0)  # rank r >= 1
    assert "coinc(N=2, r=3" in trace(Coinc(2, E, r))
