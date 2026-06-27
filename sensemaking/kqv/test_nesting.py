"""Nesting / generalization tests for the KQV builders (Task 1).

The point of Task 1 is *structural generalization*: arbitrary and unseen tree shapes
(any ``N, N', N'', ...``, ragged, plus the lens tensor) compile and run with no
enumeration and no special-casing.  Run from the repo root:

    PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m pytest \
        sensemaking/kqv/test_nesting.py -q
"""

import jax
jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp
import numpy as np
import pytest

from dap.functors import Phiconf, Phiphase
from dap.interpretation import trivial_omega

from sensemaking.kqv import (
    Builder,
    Head,
    KQVSystem,
    Par,
    Sub,
    open_boxes,
    param_dim,
    realize,
    target_boxes,
)

E, d, d_v = 3, 2, 2
B = Builder(E, d, d_v)


def _run(arr, steps=2):
    """Step a (possibly open) arrangement under both integrators; assert finite."""
    src = (jnp.zeros(arr.out_dim_M), trivial_omega(arr.in_dim_M))
    bnd = lambda op: (jnp.zeros(arr.out_dim_N), jnp.zeros(arr.in_dim_N))  # noqa: E731
    for O in (Phiconf(arr), Phiphase(arr)):
        s, out = O.state, None
        for _ in range(steps):
            out, _, s = O.with_state(s).run_one(src, bnd)
        assert jnp.all(jnp.isfinite(out[0]))


def _leaves(term):
    if isinstance(term, Head):
        return 1 if term.N == 0 else 0
    if isinstance(term, Sub):
        return sum(_leaves(c) for c in term.children)
    if isinstance(term, Par):
        return sum(_leaves(p) for p in term.parts)


def _expected_dim(term):
    """Independent expectation of the realized Q.dim (direct sum of node params)."""
    if isinstance(term, Head):
        return E if term.N == 0 else param_dim(E, d, d_v)
    if isinstance(term, Sub):
        return param_dim(E, d, d_v) + sum(_expected_dim(c) for c in term.children)
    if isinstance(term, Par):
        return sum(_expected_dim(p) for p in term.parts)


def test_nest_single_level_is_flat():
    t = B.nest([4])  # N' = 0 case: one head over 4 prior leaves
    arr = realize(t)
    assert open_boxes(t) == 0 and _leaves(t) == 4
    assert (arr.out_dim_M, arr.out_dim_N) == (0, E)
    assert arr.Q.dim == param_dim(E, d, d_v) + 4 * E
    _run(arr)


def test_nest_multilevel_shapes():
    t = B.nest([2, 3])  # root: 2 boxes, each with 3 inner boxes
    assert _leaves(t) == 6 and open_boxes(t) == 0
    arr = realize(t)
    assert arr.Q.dim == _expected_dim(t)
    _run(arr)


def test_nest_deep_and_wide():
    for arities in ([2, 2, 2, 2], [5], [12], [1, 1, 1, 1, 1], [3, 1, 4]):
        t = B.nest(arities)
        arr = realize(t)
        assert arr.Q.dim == _expected_dim(t)
        assert open_boxes(t) == 0
        _run(arr)


def test_nest_rejects_zero_arity():
    with pytest.raises(ValueError):
        B.nest([2, 0, 2])  # a 0 in the middle is ill-formed; use a shorter list


def test_ragged_tree():
    t = B.node(B.leaf(), B.node(B.leaf(), B.leaf()), B.nest([3]))
    assert _leaves(t) == 1 + 2 + 3 and open_boxes(t) == 0
    arr = realize(t)
    assert arr.Q.dim == _expected_dim(t)
    _run(arr)


def test_par_lens_tensor_width():
    t = B.par(B.nest([2]), B.nest([3]))  # two independent subsystems side by side
    assert target_boxes(t) == 2 and _leaves(t) == 5
    arr = realize(t)
    assert (arr.out_dim_N, arr.in_dim_N) == (2 * E, 2 * E)
    assert arr.Q.dim == _expected_dim(t)
    _run(arr)


def test_par_cannot_be_a_sub_child():
    # a lens tensor has multiple target boxes, so it is not substitutable into one box
    with pytest.raises(ValueError):
        Sub(Head(1, E, d, d_v), (B.par(B.leaf(), B.leaf()),))


def test_term_algebra_is_total():
    # an invalid generator cannot be constructed -- membership is validated, not deferred
    with pytest.raises(ValueError):
        Head(-1, E, d, d_v)
    with pytest.raises(ValueError):
        B.head(-1)
    with pytest.raises(ValueError):
        Head(0, 0)  # residual width E must be >= 1
    with pytest.raises(ValueError):
        Head(2, E, 0, d_v)  # internal ranks must be >= 1 when N >= 1


def test_system_carries_and_exposes_provenance():
    s = KQVSystem(B.nest([2, 2]))
    assert s.arrangement.Q.dim == _expected_dim(s.term)
    tr = s.trace()
    assert tr.count("leaf") == 4  # 2 x 2 prior leaves
    assert tr.count("sub") == 3  # root + 2 middle heads
    _run(s.arrangement)


def test_provenance_trace_covers_the_lens_tensor():
    # KQVSystem.trace() must work for EVERY realized construct, including Par
    s = KQVSystem(B.par(B.nest([2]), B.leaf()))
    tr = s.trace()
    assert "par" in tr
    assert tr.count("leaf") == 3  # 2 from nest([2]) + 1 standalone
    _run(s.arrangement)


def test_system_validates_its_term_at_construction():
    # provenance is enforced, not annotated: a KQVSystem cannot wrap a non-term
    with pytest.raises(TypeError):
        KQVSystem(42)
    with pytest.raises(TypeError):
        KQVSystem(realize(B.nest([2])))  # a raw SmoothArrangement is not a KQVTerm


def test_open_terms_run_under_both_integrators():
    # An OPEN term (inner boxes left unwired) is a legitimate suboperad member; it must
    # also interpret. The environment supplies the source emissions (out_M) at the
    # boundary. Closes the coverage gap that the builders only ever emit closed trees.
    bare = B.head(2)  # a bare arity-2 head: source <2E|2E>, two open inner boxes
    assert open_boxes(bare) == 2
    arr = realize(bare)
    assert (arr.out_dim_M, arr.in_dim_M, arr.out_dim_N, arr.in_dim_N) == (2 * E, 2 * E, E, E)
    _run(arr)

    partial = Sub(Head(2, E, d, d_v), (B.leaf(), B.head(1)))  # one child still open
    assert open_boxes(partial) == 1
    _run(realize(partial))


def test_generalization_to_unseen_shapes():
    # The whole spirit: random/unseen tree shapes compile + run, no enumeration.
    rng = np.random.default_rng(31415)

    def rand_term(depth):
        if depth <= 0 or rng.random() < 0.4:
            return B.leaf()
        N = int(rng.integers(1, 4))
        return B.node(*[rand_term(depth - 1) for _ in range(N)])

    for _ in range(15):
        N = int(rng.integers(1, 4))
        t = B.node(*[rand_term(int(rng.integers(1, 4))) for _ in range(N)])
        arr = realize(t)
        assert arr.Q.dim == _expected_dim(t)  # provenance dim matches an independent count
        assert open_boxes(t) == 0
        _run(arr, steps=1)
