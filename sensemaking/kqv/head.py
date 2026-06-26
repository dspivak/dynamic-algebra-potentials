"""KQV attention head: the generator of the attention suboperad of ``sarr``.

Faithful to ``attention-suboperad.tex`` (``con.head``). A head of arity ``N`` is a
``SmoothArrangement``

    f : (R^E | R^E)^{(x)N}  -->  (R^E | R^E)

whose reactive parameter ``Q`` carries the query/key/value/output projections
``(Wq, Wk, Wv, Wo)`` together with a learned outer query ``w_star`` (``con.head``,
``rmk.circuits``; the learned-query option of ``eq.pool``).  The three smooth maps
are exactly

    out_f(W, h)      = Wo sum_j softmax(<w_star, Wk h_j>/sqrt d)_j Wv h_j     (eq.pool)
    in_f(W, h, n)_i  = Wo sum_{j in 1..N, *} A_ij Wv h_j,  A = softmax row     (eq.attn)
    U(W, h, n)       = 1/2 || h - Omega n ||^2,   Omega = Wo Wv               (eq.Uattn)

where the ``*`` column of the attention is the key/value built from the outer
input ``n`` (``eq.attn``), and the potential's prediction is the OV-circuit image
``Omega n`` of the descending context (``rmk.circuits``; the canonical concrete
choice for the schematic ``pred`` of ``eq.Uattn``).  Both legs of every box are the
residual stream ``R^E`` (``sec.attention``, ``obs.residual``); ``d_q = d_k = d`` and
``d_v`` are internal ranks that never reach an interface (``rmk.circuits``).

The weight count is **independent of the arity ``N``**: one head applies to any
number of tokens, which is why a single learned head composes into trees of every
shape (the structural seed of compositionality, ``rmk.supertoken``).

The optimizer lives in the sharp (``rmk.optimizer``): the reactive vector space
``Q`` carries the metric, so the choice of optimizer is data of ``Q``, never an
object outside the formalism.  Any regularization is added to ``U`` (the writer
monad adds potentials), never applied on the side.
"""

from __future__ import annotations

import math

import jax.nn as jnn
import jax.numpy as jnp
from jax import Array

from dap.arrangement import SmoothArrangement
from dap.rvect import euclidean


def _layout(E: int, d: int, d_v: int):
    """Parameter blocks of a head, in packing order (``con.head`` carrier)."""
    return (
        ("Wq", (d, E)),
        ("Wk", (d, E)),
        ("Wv", (d_v, E)),
        ("Wo", (E, d_v)),
        ("w_star", (d,)),
    )


def param_dim(E: int, d: int, d_v: int) -> int:
    """Dimension of the head's reactive parameter space ``Q`` (``con.head``)."""
    return sum(math.prod(shape) for _, shape in _layout(E, d, d_v))


def unpack(q: Array, E: int, d: int, d_v: int) -> dict:
    """Split the flat parameter ``q in Q`` into ``{Wq, Wk, Wv, Wo, w_star}``."""
    out, i = {}, 0
    for name, shape in _layout(E, d, d_v):
        n = math.prod(shape)
        out[name] = q[i : i + n].reshape(shape)
        i += n
    return out


def attention_head(N, E, d, d_v, *, sharp=None, label=None) -> SmoothArrangement:
    """The attention head generator of arity ``N`` (``con.head``).

    ``N = 0`` returns the prior box (``ex.zeroary``).  ``sharp`` is the reactive
    vector space on ``Q`` (the optimizer, ``rmk.optimizer``); default Euclidean,
    whose configuration dynamics is plain gradient descent.
    """
    if N < 0:
        raise ValueError("arity N must be >= 0")
    if N == 0:
        return prior_box(E, sharp=sharp, label=label)  # ex.zeroary

    dim = param_dim(E, d, d_v)
    Q = sharp if sharp is not None else euclidean(dim)
    if Q.dim != dim:
        raise ValueError(f"sharp dim {Q.dim} != head param dim {dim}")
    scale = 1.0 / math.sqrt(d)

    def out_f(q: Array, m_out: Array) -> Array:
        # eq.pool -- pooled read-out via the learned query w_star. Moore: no n (rmk.moore).
        P = unpack(q, E, d, d_v)
        h = m_out.reshape(N, E)
        keys = h @ P["Wk"].T  # (N, d)
        vals = h @ P["Wv"].T  # (N, d_v)
        a = jnn.softmax((keys @ P["w_star"]) * scale)  # (N,)
        return P["Wo"] @ (a @ vals)  # (E,)

    def in_f(q: Array, m_out: Array, n_in: Array) -> Array:
        # eq.attn -- softmax routing of the Gram matrix, with the '*'=n key/value column.
        P = unpack(q, E, d, d_v)
        h = m_out.reshape(N, E)
        Qi = h @ P["Wq"].T  # (N, d) queries
        K_all = jnp.concatenate([h @ P["Wk"].T, (P["Wk"] @ n_in)[None, :]], 0)  # (N+1, d)
        V_all = jnp.concatenate([h @ P["Wv"].T, (P["Wv"] @ n_in)[None, :]], 0)  # (N+1, d_v)
        A = jnn.softmax((Qi @ K_all.T) * scale, axis=1)  # (N, N+1) row-stochastic
        return ((A @ V_all) @ P["Wo"].T).reshape(N * E)  # (N*E,)

    def U(q: Array, m_out: Array, n_in: Array) -> Array:
        # eq.Uattn -- squared prediction error; pred = Omega n, Omega = Wo Wv (rmk.circuits).
        P = unpack(q, E, d, d_v)
        h = m_out.reshape(N, E)
        pred = P["Wo"] @ (P["Wv"] @ n_in)  # (E,)
        return 0.5 * jnp.sum((h - pred[None, :]) ** 2)

    return SmoothArrangement(
        Q=Q,
        out_dim_M=N * E,
        in_dim_M=N * E,
        out_dim_N=E,
        in_dim_N=E,
        out_f=out_f,
        in_f=in_f,
        U=U,
        label=label or f"kqv_head(N={N},E={E})",
    )


def prior_box(E, *, sharp=None, label=None) -> SmoothArrangement:
    """The 0-ary generator (``ex.zeroary``): a box that emits a learned constant.

    Source ``(R^0|R^0)`` (no children), target the residual box ``(R^E|R^E)``.  The
    emitted constant is the parameter ``q in R^E`` itself; the descending context is
    ignored (nothing is wired below it) and ``U = 0`` -- its "prior" is learned from
    whatever environment it is wired into, exactly as ``learning.parameterized_map``
    (the data-marginal signal of ``ex.zeroary``).  A predictive-coding variant
    ``U = 1/2 ||q - n||^2`` is the natural alternative and is deferred to the
    experiment layer (see SPEC.md, "modeling choices").
    """
    Q = sharp if sharp is not None else euclidean(E)
    if Q.dim != E:
        raise ValueError(f"sharp dim {Q.dim} != E {E}")
    return SmoothArrangement(
        Q=Q,
        out_dim_M=0,
        in_dim_M=0,
        out_dim_N=E,
        in_dim_N=E,
        out_f=lambda q, m_out: q,
        in_f=lambda q, m_out, n_in: jnp.zeros(0),
        U=lambda q, m_out, n_in: jnp.array(0.0),
        label=label or f"prior_box(E={E})",
    )
