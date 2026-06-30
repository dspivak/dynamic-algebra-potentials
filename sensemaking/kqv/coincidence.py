"""KQV coincidence head: a SECOND-ORDER generator of an enlarged suboperad of ``sarr``.

The attention head (``con.head``) summarizes its children with a *first-order* statistic
(a weighted mean, ``eq.pool``), so it is blind to *coincidences* -- "child i and child j
fired together" is a product ``h_i (x) h_j``, which no mean can see. The coincidence head
sends up a **second moment** instead, making co-activation explicit:

    out_f(V,Wo ; h)  = Wo . vech(P Pᵀ),   P = Σ_j V h_j ∈ R^r      (degree-2 read-out)
    in_f(. ; h, n)_i = n                                          (transparent backward leg)
    U(V,G ; h, n)    = ½ || vech(P Pᵀ) − G n ||²                  (predict the coincidences)

The pooled feature ``P`` is first order; squaring it, ``P Pᵀ``, exposes the cross terms
``(V h_i)(V h_j)ᵀ`` (i≠j) -- the coincidences between children. ``out_f`` is a learned
read-out of that second moment (the "sense" that climbs); ``U`` is *second-order predictive
coding* -- it predicts the second moment from the descending context ``n``, so its residual
``vech(P Pᵀ) − G n`` is the **unexpected coincidence** ("something is happening").

Faithfulness (a clean enlarged suboperad, like the activation cell):
- arity-independent weights ``(V, Wo, G)`` -- the pool ``Σ_j`` is the only ``K``-dependence
  (``rmk.supertoken``), so one head applies to any number of children;
- permutation-invariant (the pool is a sum -- ``obs.equivariance``);
- Moore (``out_f`` has no ``n`` -- ``rmk.moore``); R-vect carrier; block/Euclidean sharp;
- substitution + lens tensor only -- no new operad operation.

Design lesson (from ``experiments/coincidence_tower.py``): do **not** make every level
second order. Squaring destroys signs (``(±1)² = 1``), erasing the features a higher level
needs to correlate; first-order summaries must climb to *preserve* features, with the
coincidence head placed where two features must be correlated.
"""

from __future__ import annotations

import jax.numpy as jnp
from jax import Array

from dap.arrangement import SmoothArrangement
from dap.rvect import euclidean


def _sym_dim(r: int) -> int:
    """Dimension of the symmetric second moment ``vech(R^{r×r})`` = ``r(r+1)/2``."""
    return r * (r + 1) // 2


def coinc_param_dim(E: int, r: int) -> int:
    """Dimension of ``Q = (V, Wo, G)``: ``V:r×E``, ``Wo:E×sym``, ``G:sym×E``."""
    sym = _sym_dim(r)
    return r * E + E * sym + sym * E


def coinc_unpack(q: Array, E: int, r: int) -> dict:
    """Split the flat parameter into ``{V, Wo, G}`` (feature, read-out, predictor)."""
    sym = _sym_dim(r)
    i, out = 0, {}
    for name, shape in (("V", (r, E)), ("Wo", (E, sym)), ("G", (sym, E))):
        n = shape[0] * shape[1]
        out[name] = q[i : i + n].reshape(shape)
        i += n
    return out


def coincidence_head(K, E, r, *, sharp=None, label=None) -> SmoothArrangement:
    """The coincidence-head generator of arity ``K`` over residual width ``E``.

    ``r`` is the feature rank (``r ≤ E`` keeps the second moment low rank). ``sharp`` is the
    reactive vector space on ``Q`` (the optimizer, ``rmk.optimizer``); default Euclidean.
    """
    if K < 1:
        raise ValueError("coincidence head arity K must be >= 1")
    if E < 1 or r < 1:
        raise ValueError("E and r must be >= 1")

    sym = _sym_dim(r)
    iu = jnp.triu_indices(r)
    dim = coinc_param_dim(E, r)
    Q = sharp if sharp is not None else euclidean(dim)
    if Q.dim != dim:
        raise ValueError(f"sharp dim {Q.dim} != coincidence param dim {dim}")

    def out_f(q: Array, m_out: Array) -> Array:
        # eq.pool analogue, degree 2: P = Σ_j V h_j; read out vech(P Pᵀ). Moore: no n.
        W = coinc_unpack(q, E, r)
        P = (m_out.reshape(K, E) @ W["V"].T).sum(0)   # (r,) pooled feature
        return W["Wo"] @ jnp.outer(P, P)[iu]          # (E,)

    def in_f(q: Array, m_out: Array, n_in: Array) -> Array:
        # transparent backward leg: the descending context passes to each child.
        return jnp.tile(n_in, K)                       # (K*E,)

    def U(q: Array, m_out: Array, n_in: Array) -> Array:
        # second-order predictive coding: predict the second moment vech(P Pᵀ) from n.
        W = coinc_unpack(q, E, r)
        P = (m_out.reshape(K, E) @ W["V"].T).sum(0)
        c = jnp.outer(P, P)[iu]                         # (sym,) observed coincidences
        return 0.5 * jnp.sum((c - W["G"] @ n_in) ** 2)

    return SmoothArrangement(
        Q=Q,
        out_dim_M=K * E,
        in_dim_M=K * E,
        out_dim_N=E,
        in_dim_N=E,
        out_f=out_f,
        in_f=in_f,
        U=U,
        label=label or f"kqv_coinc(K={K},E={E},r={r})",
    )
