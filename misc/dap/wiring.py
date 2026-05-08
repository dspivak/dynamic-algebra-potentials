"""Wiring constructors in ``potlens`` (sec.wd_operads, sec.spring).

Provides:

* ``finset_chain_wire(K)`` -- the lens ``phi_K`` of ex.lens_finsetop /
  sec.spring_first_pass: ``out_f(*) = K``, ``in_f(n) = n``.
* ``chain_wire(K)``        -- its image under ``R^-`` (lemma.lens_rr),
  realized as a parameter-free ``PotLensMap``: a K-ary wiring morphism
  ``box^K -> box`` in ``potlens`` with ``V = R^0`` and ``U = 0``.
* ``compose_chain(parts)`` -- the K-ary composite
  ``chain_wire(K)(Part_1, ..., Part_K)`` directly in ``potlens``,
  yielding a 0-ary morphism per the formulas of
  sec.spring_first_pass (eqn.sharp_chain and surrounding prose).
* ``parallel_potlens(p1, p2)`` -- monoidal product in potlens.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

import jax.numpy as jnp
from jax import Array

from .lens import PotLensMap
from .pvect import PairedVectorSpace, trivial_pvect


# ---------------------------------------------------------------------------
# The finset-op lens phi_K (ex.lens_finsetop, sec.spring_first_pass).
# ---------------------------------------------------------------------------


def finset_chain_wire(K: int) -> Tuple[List[int], List[int]]:
    """Return ``(out_f, in_f)`` for ``phi_K: <K|K> -> <1|1>``.

    Per sec.spring_first_pass, identifying ``K+1`` with the disjoint
    union of (1) the big-box input and (2) the K small-box outputs:

        out_f: 1 -> K   chooses the last wire, ``out_f(0) = K-1`` (0-indexed).
        in_f : K -> K+1 sends ``n |-> n``                (i.e. picks the first K).
    """
    out_f = [K - 1]               # singleton; selects index of last small box
    in_f = list(range(K))         # picks the first K of K+1 wires
    return out_f, in_f


# ---------------------------------------------------------------------------
# chain_wire(K) as a PotLensMap, the image under R^- (lemma.lens_rr).
# ---------------------------------------------------------------------------


def chain_wire(K: int) -> PotLensMap:
    """Image of ``phi_K`` under ``R^-`` (lemma.lens_rr), as a potlens morphism.

    Source ``M = box^K = <R^K | R^K>``, target ``N = box = <R | R>``,
    parameter ``V = R^0``, no potential. Per the paragraph just below
    ex.lens_finsetop in sec.spring_first_pass:

        out_f((v_1, ..., v_K)) = v_K
        in_f((v_1, ..., v_K), v_0) = (v_0, v_1, ..., v_{K-1})
    """

    if K < 1:
        raise ValueError("K must be >= 1")

    V = trivial_pvect()

    def out_f(v_wire: Array, m_out: Array) -> Array:
        # m_out: shape (K,). Output: scalar = v_K = m_out[-1].
        return m_out[K - 1:K]  # shape (1,)

    def in_f(v_wire: Array, m_out: Array, n_in: Array) -> Array:
        # m_out: (K,), n_in: (1,). Output: (v_0, v_1, ..., v_{K-1}) of shape (K,).
        v_0 = n_in[0]
        return jnp.concatenate([jnp.array([v_0]), m_out[: K - 1]])

    def U(v_wire: Array, m_out: Array, n_in: Array) -> Array:
        return jnp.array(0.0)

    return PotLensMap(
        V=V,
        out_dim_M=K,
        in_dim_M=K,
        out_dim_N=1,
        in_dim_N=1,
        out_f=out_f,
        in_f=in_f,
        U=U,
        label=f"chain_wire({K})",
    )


# ---------------------------------------------------------------------------
# Composition in potlens for the chain-of-particles example.
#
# Each Part_i: <R^0|R^0> -> <R|R> has parameter V_i and data
#   out_f_i: V_i -> R    (here identity).
#   in_f_i:  V_i x R -> R^0 (vacuous).
#   U_i:     V_i x R -> R   (the per-particle potential).
# Composing chain_wire(K)(Part_1, ..., Part_K) in potlens (as in
# sec.para_general / the prose around eqn.sharp_chain) gives a
# 0-ary morphism with parameter V_{tot} = V_wire (+) V_1 (+) ... (+) V_K,
# whose data is given in the paper between eqs. (2388)-(2398).
# ---------------------------------------------------------------------------


def compose_chain(parts: Sequence[PotLensMap]) -> PotLensMap:
    """Compose ``chain_wire(K)(Part_1, ..., Part_K)`` directly in potlens.

    Specialized to the wave-equation chain: each ``Part_i`` must have
    source ``<R^0 | R^0>`` and target ``<R | R>``. The composite has

        V_tot     = V_1 (+) ... (+) V_K     (V_wire = R^0 absorbs)
        out_f_tot = out_f_K(v_K, *)          # = v_K when out_f_i = id
        in_f_tot  vacuous (target is <R^0|R^0>)
        U_tot     = sum_i U_i(v_i, v_{i-1})  (with v_0 the external in_n)
    """

    K = len(parts)
    if K < 1:
        raise ValueError("Need at least one particle in chain")

    # All particles must have <R^0|R^0> source and <R|R> target.
    for i, P in enumerate(parts):
        if not (P.out_dim_M == 0 and P.in_dim_M == 0):
            raise ValueError(f"Part {i}: expected source <R^0|R^0>")
        if not (P.out_dim_N == 1 and P.in_dim_N == 1):
            raise ValueError(f"Part {i}: expected target <R|R>")

    # Combined paired vector space V_tot = V_1 (+) ... (+) V_K. We do
    # NOT include V_wire = R^0 since direct_sum with the trivial pvect
    # is the identity but inv(0x0) blows up; just sum the parts.
    V_tot = parts[0].V
    for P in parts[1:]:
        V_tot = V_tot.direct_sum(P.V)

    dims = [P.V.V_dim for P in parts]
    offsets = [0]
    for d in dims:
        offsets.append(offsets[-1] + d)

    def split_v(v_tot: Array):
        return [v_tot[offsets[i]: offsets[i + 1]] for i in range(K)]

    def out_f(v_tot: Array, m_out: Array) -> Array:
        # m_out: shape (0,); compute v_K using K-th particle's out_f.
        v_chunks = split_v(v_tot)
        # Each particle's out_f returns shape (1,). The wire selects v_K.
        v_K = parts[K - 1].out_f(v_chunks[K - 1], jnp.zeros(0))
        return v_K  # shape (1,) for target out_dim_N = 1

    def in_f(v_tot: Array, m_out: Array, n_in: Array) -> Array:
        # Target in_dim_M = 0; vacuous.
        return jnp.zeros(0)

    def U(v_tot: Array, m_out: Array, n_in: Array) -> Array:
        # n_in: shape (1,) i.e. v_0 (the external input).
        v_chunks = split_v(v_tot)
        # Build the sequence (v_0, v_1, ..., v_K) of "neighbor" inputs
        # that the wire's in_f would have routed: each Part_i sees
        # in_n = v_{i-1} (for i = 1, ..., K).
        v_outs = [parts[i].out_f(v_chunks[i], jnp.zeros(0)) for i in range(K)]
        # Sum of per-particle potentials with their wired neighbor input:
        #     U_i(v_i_param, v_{i-1}_output) where v_0_output := n_in.
        total = jnp.array(0.0)
        for i in range(K):
            neighbor = n_in if i == 0 else v_outs[i - 1]
            total = total + parts[i].U(v_chunks[i], jnp.zeros(0), neighbor)
        return total

    return PotLensMap(
        V=V_tot,
        out_dim_M=0,
        in_dim_M=0,
        out_dim_N=1,
        in_dim_N=1,
        out_f=out_f,
        in_f=in_f,
        U=U,
        label=f"chain_wire({K})(parts)",
    )


# ---------------------------------------------------------------------------
# Monoidal (parallel) composition in potlens (sec.para_general).
# ---------------------------------------------------------------------------


def parallel_potlens(p1: PotLensMap, p2: PotLensMap) -> PotLensMap:
    """Monoidal product in potlens: side-by-side independent boxes."""

    V = p1.V.direct_sum(p2.V)
    n1 = p1.V.V_dim

    def split(v: Array) -> Tuple[Array, Array]:
        return v[:n1], v[n1:]

    d_out_M = p1.out_dim_M + p2.out_dim_M
    d_in_M = p1.in_dim_M + p2.in_dim_M
    d_out_N = p1.out_dim_N + p2.out_dim_N
    d_in_N = p1.in_dim_N + p2.in_dim_N

    def out_f(v: Array, m_out: Array) -> Array:
        v1, v2 = split(v)
        m1, m2 = m_out[: p1.out_dim_M], m_out[p1.out_dim_M:]
        n1_out = p1.out_f(v1, m1)
        n2_out = p2.out_f(v2, m2)
        return jnp.concatenate([n1_out, n2_out])

    def in_f(v: Array, m_out: Array, n_in: Array) -> Array:
        v1, v2 = split(v)
        m1, m2 = m_out[: p1.out_dim_M], m_out[p1.out_dim_M:]
        n1_in, n2_in = n_in[: p1.in_dim_N], n_in[p1.in_dim_N:]
        a = p1.in_f(v1, m1, n1_in)
        b = p2.in_f(v2, m2, n2_in)
        return jnp.concatenate([a, b])

    def U(v: Array, m_out: Array, n_in: Array) -> Array:
        v1, v2 = split(v)
        m1, m2 = m_out[: p1.out_dim_M], m_out[p1.out_dim_M:]
        n1_in, n2_in = n_in[: p1.in_dim_N], n_in[p1.in_dim_N:]
        return p1.U(v1, m1, n1_in) + p2.U(v2, m2, n2_in)

    return PotLensMap(
        V=V,
        out_dim_M=d_out_M,
        in_dim_M=d_in_M,
        out_dim_N=d_out_N,
        in_dim_N=d_in_N,
        out_f=out_f,
        in_f=in_f,
        U=U,
        label=f"({p1.label} || {p2.label})",
    )
