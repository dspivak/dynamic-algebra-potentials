"""The functor chain ``cint -> leg -> dyn`` and its composite ``Phi``.

Implements:

* ``cot``      -- the cotangent functor on ``mfd = R^d`` (def.cot).
* ``T``, ``Tstar`` -- pvect endofunctors (prop.TT_endofunctors).
* ``Lens_cot`` -- the lifted cotangent functor (lem.cot_lifts_lens_potential).
* ``cint``     -- cotangent internalization (lem.potlens_to_para_poly).
* ``leg``      -- Legendre refinement (lem.para_rho).
* ``dyn``      -- dynamical realization (lem.poly_to_org).
* ``Phi``      -- the composite of thm.functor.

The intermediate types ``ParaCotPoly`` and ``ParaCotTPoly`` are book-
keeping wrappers; they record which Para action is in force, but for
the v1 specialization to ``R^d`` the underlying smooth-map data is
unchanged from one stage to the next. ``dyn`` does the heavy lifting,
turning the parameterized poly map into the ``OrgMorphism`` of
def.pq_coalg, exactly as in the unpacking of ``Phi`` in
sec.dynamics_functor (eqs. 2261-2295 of the .tex).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import jax
import jax.numpy as jnp
from jax import Array

from .lens import PotLensMap, SmoothMap
from .polynomial import (
    Cot,
    DirichletProduct,
    PolyMap,
    Poly,
    PolyValue,
    Yon,
)
from .pvect import PairedVectorSpace
from .org import OrgMorphism


# ---------------------------------------------------------------------------
# cot: mfd -> poly (def.cot), restricted to R^d in v1 (VOCAB design (5)).
# ---------------------------------------------------------------------------


def cot_object(d: int) -> Cot:
    """Apply def.cot on objects: ``R^d |-> Cot(d)``."""
    return Cot(d)


def cot_map(f: SmoothMap, src_dim: int, tgt_dim: int, label: str = "") -> PolyMap:
    """Apply def.cot on morphisms: ``f: R^a -> R^b`` to its poly map.

    Forward part is ``f``; backward (direction) part at point ``x`` is
    the cotangent pullback ``(T_x f)^T: T*_{f(x)} R^b -> T*_x R^a`` via
    ``jax.vjp`` (VOCAB design (8)).
    """

    def position_action(x: Array) -> Array:
        return f(x)

    def direction_action(x: Array, xi_target: Array) -> Array:
        # (T_x f)^T xi_target via jax.vjp.
        _, vjp_fn = jax.vjp(f, x)
        (xi_source,) = vjp_fn(xi_target)
        return xi_source

    return PolyMap(
        src=Cot(src_dim),
        tgt=Cot(tgt_dim),
        position_action=position_action,
        direction_action=direction_action,
        label=label or "cot(f)",
    )


# ---------------------------------------------------------------------------
# T, T*: pvect endofunctors (prop.TT_endofunctors).
# ---------------------------------------------------------------------------


def T(V: PairedVectorSpace) -> PairedVectorSpace:
    """``T: V |-> V (+) V`` (prop.TT_endofunctors)."""
    return V.direct_sum(V)


def Tstar(V: PairedVectorSpace) -> PairedVectorSpace:
    """``T*: V |-> V (+) V*`` (prop.TT_endofunctors).

    The sharp on ``V (+) V*`` is the canonical symplectic sharp
    eqn.canonical_sharp: ``(xi, v) |-> (v, -xi)``.
    """
    n = V.V_dim
    # Block-antidiagonal: sharp((xi, v)) = (v, -xi).
    S = jnp.zeros((2 * n, 2 * n))
    S = S.at[:n, n:].set(jnp.eye(n))      # top-right block: identity
    S = S.at[n:, :n].set(-jnp.eye(n))     # bottom-left block: -identity
    return PairedVectorSpace(V_dim=2 * n, sharp=S)


# ---------------------------------------------------------------------------
# Lens(cot): lmfd^R -> Lens(poly)^R (lem.cot_lifts_lens_potential).
#
# In v1 we never represent a bare lmfd^R-morphism as a separate type:
# our ``PotLensMap`` already carries the Para parameter, and ``cint``
# below applies ``Lens cot`` and ``Theta_d`` together. For
# completeness we expose the action of ``Lens cot`` on a single
# unparametrized lens morphism, which a small test exercises.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _UnparamLens:
    """A potentialized manifold lens (out_f, in_f, U), no Para parameter.

    Used to exhibit ``Lens cot`` on a representative morphism in
    lem.cot_lifts_lens_potential.
    """

    out_dim_M: int
    in_dim_M: int
    out_dim_N: int
    in_dim_N: int
    out_f: Callable[[Array], Array]                         # m_out -> n_out
    in_f: Callable[[Array, Array], Array]                   # (m_out, n_in) -> m_in
    U: Callable[[Array, Array], Array]                      # (m_out, n_in) -> R


@dataclass(frozen=True)
class _LiftedLens:
    """Image of an unparametrized lens under ``Lens cot``.

    The lifted polynomial-lens has forward part ``cot(out_f)``, backward
    part the ``+1`` along ``U``-cotangent splitting. We just store the
    callables; consumers (here ``cint``) use them directly.
    """

    out_dim_M: int
    in_dim_M: int
    out_dim_N: int
    in_dim_N: int
    out_f: Callable[[Array], Array]
    in_f: Callable[[Array, Array], Array]
    U: Callable[[Array, Array], Array]


def Lens_cot(L: _UnparamLens) -> _LiftedLens:
    """``Lens cot`` on a representative unparametrized lens.

    Implements lem.cot_lifts_lens_potential. In v1 (R^d only) the lift
    is data-preserving on the smooth-map level; what changes is the
    semantics of how the resulting object's directions are interpreted
    (cotangent pullbacks, ``+1`` for ``U``).
    """
    return _LiftedLens(
        out_dim_M=L.out_dim_M,
        in_dim_M=L.in_dim_M,
        out_dim_N=L.out_dim_N,
        in_dim_N=L.in_dim_N,
        out_f=L.out_f,
        in_f=L.in_f,
        U=L.U,
    )


# ---------------------------------------------------------------------------
# cint: potlens -> Para(cot, poly) (lem.potlens_to_para_poly).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ParaCotPoly:
    """A morphism in ``Para(cot, poly)`` (lem.potlens_to_para_poly).

    Records the V-parameterized polynomial-lens data after applying
    ``Lens cot`` and ``Theta_d`` together: the same smooth callables,
    now to be interpreted in ``poly`` with V acting via ``cot V``.
    """

    V: PairedVectorSpace
    out_dim_M: int
    in_dim_M: int
    out_dim_N: int
    in_dim_N: int
    out_f: SmoothMap
    in_f: SmoothMap
    U: SmoothMap


def cint(plm: PotLensMap) -> ParaCotPoly:
    """Implements lem.potlens_to_para_poly; cotangent internalization.

    Composite ``Para(pvect, Lens cot) ; Para(pvect, Theta_d)``. In v1
    this is bookkeeping: the data of ``plm`` is forwarded as a
    ``ParaCotPoly`` to be re-interpreted by downstream functors.
    """
    return ParaCotPoly(
        V=plm.V,
        out_dim_M=plm.out_dim_M,
        in_dim_M=plm.in_dim_M,
        out_dim_N=plm.out_dim_N,
        in_dim_N=plm.in_dim_N,
        out_f=plm.out_f,
        in_f=plm.in_f,
        U=plm.U,
    )


# ---------------------------------------------------------------------------
# leg: Para(cot, poly) -> Para(cot T*, poly) (lem.para_rho).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ParaCotTPoly:
    """A morphism in ``Para(cot T*, poly)`` (lem.para_rho)."""

    V: PairedVectorSpace
    Vstar_state: PairedVectorSpace  # = T*V, the canonical-symplectic state space
    out_dim_M: int
    in_dim_M: int
    out_dim_N: int
    in_dim_N: int
    out_f: SmoothMap
    in_f: SmoothMap
    U: SmoothMap


def leg(pcp: ParaCotPoly) -> ParaCotTPoly:
    """Implements lem.para_rho; the Legendre refinement induced by rho.

    ``rho_V: cot(T*V) => cot(V)`` of def.legendre_projection has
    position-part ``(v, xi) |-> v`` and direction-part ``xi_V |->
    (xi_V, sharp_V xi)``. At the level of ``Para`` parameters this
    means the new state space is ``T*V`` (positions ``(v, xi)``), with
    sharp ``sharp_X`` from eqn.sharp_X.
    """
    return ParaCotTPoly(
        V=pcp.V,
        Vstar_state=Tstar(pcp.V),
        out_dim_M=pcp.out_dim_M,
        in_dim_M=pcp.in_dim_M,
        out_dim_N=pcp.out_dim_N,
        in_dim_N=pcp.in_dim_N,
        out_f=pcp.out_f,
        in_f=pcp.in_f,
        U=pcp.U,
    )


# ---------------------------------------------------------------------------
# dyn: Para(cot T*, poly) -> org (lem.poly_to_org).
# ---------------------------------------------------------------------------


def _phi_box_poly(d_out: int, d_in: int) -> Poly:
    """``Phi(<R^{d_in}/R^{d_out}>)`` as a poly object.

    Per eqn 2228-2230, ``Phi <M_in / M_out>`` is a polynomial whose
    positions are pairs ``(out_m, omega_M)`` and whose directions at
    ``(out_m, omega_M)`` are pairs ``(xi, in_m)``. We do not allocate
    a class for this; we use a tagged ``DirichletProduct(Cot(d_out),
    Cot(d_in))`` as a convenient representative and rely on the
    ``OrgMorphism.step`` closure to thread covector-field data
    explicitly. The covector field ``omega_M`` is carried alongside
    out_m as a Python value (an ``(matrix, vector)`` affine pair, per
    VOCAB design (9)) wherever it shows up.
    """
    # We only need this object as a tag; a DirichletProduct of two
    # Cot's records the dimensions in a self-documenting way.
    return DirichletProduct(Cot(d_out), Cot(d_in))


def dyn(pct: ParaCotTPoly) -> OrgMorphism:
    """Implements lem.poly_to_org; dynamical realization via the action square.

    Builds the OrgMorphism whose state set is ``X = T*V`` (eqn.state_space),
    state ``(v, xi)``, and step the unpacked formulas of
    sec.dynamics_functor (eqs. eqn.outpn, eqn.omegaprime, eqn.inptm,
    eqn.bigtheta, eqn.state_update).
    """

    V = pct.V
    sharp_V = V.sharp
    out_f = pct.out_f
    in_f = pct.in_f
    U = pct.U
    d_out_M, d_in_M = pct.out_dim_M, pct.in_dim_M
    d_out_N, d_in_N = pct.out_dim_N, pct.in_dim_N

    src_p = _phi_box_poly(d_out_M, d_in_M)
    tgt_p = _phi_box_poly(d_out_N, d_in_N)

    # Initial state: zero in T*V = V (+) V*.
    init_state = (jnp.zeros(V.V_dim), jnp.zeros(V.V_dim))

    def step(state):
        v, xi = state

        # ------------------------------------------------------------------
        # Position action (eqn.outpn, eqn.omegaprime).
        #
        # Inputs are positions (out_m, omega_M) where omega_M is an
        # affine covector field on R^{d_in_M}, encoded as
        # (A_M: (d_in_M, d_in_M), b_M: (d_in_M,)).
        # Outputs (out_n, omega_N) similarly affine on R^{d_in_N}.
        # ------------------------------------------------------------------

        def position_action(in_pos):
            out_m, omega_M = in_pos
            A_M, b_M = omega_M
            # Output position out_n = out_f(v, out_m) (eqn.outpn).
            out_n = out_f(v, out_m)

            # Output covector field omega_N (eqn.omegaprime), on R^{d_in_N}:
            #   omega_N(in_n) = (T_{in_n} in_f(v, out_m, .))^T omega_M(in_f(v,out_m,in_n))
            #                + dU(v, out_m, .)|_{in_n}
            # which is affine in in_n. We compute its affine form
            # (A_N, b_N) by symbolically differentiating once.
            def omega_N_at(in_n):
                # First summand: cotangent pullback of omega_M along in_f.
                in_f_vm = lambda y: in_f(v, out_m, y)
                in_m_at_in_n = in_f_vm(in_n)
                omega_M_val = A_M @ in_m_at_in_n + b_M
                _, vjp_in_f = jax.vjp(in_f_vm, in_n)
                (pull_back,) = vjp_in_f(omega_M_val)
                # Second summand: dU(v, out_m, .)|_{in_n}.
                Ux_partial = lambda y: U(v, out_m, y)
                dU_at = jax.grad(Ux_partial)(in_n)
                return pull_back + dU_at

            # Compute affine form (A_N, b_N) by Jacobian + value at 0.
            zero_in_n = jnp.zeros(d_in_N)
            b_N = omega_N_at(zero_in_n)
            A_N = jax.jacfwd(omega_N_at)(zero_in_n)
            omega_N = (A_N, b_N)
            return (out_n, omega_N)

        # ------------------------------------------------------------------
        # Direction action (eqn.bigtheta, eqn.inptm, second component of
        # eqn.state_update).
        #
        # in_pos = (out_m, omega_M); in_dir = (xi_N, in_n).
        # out_dir = (xi_M, in_m), where in_m = in_f(v, out_m, in_n).
        # ------------------------------------------------------------------

        def direction_action(in_pos, in_dir):
            out_m, omega_M = in_pos
            A_M, b_M = omega_M
            xi_N, in_n = in_dir

            in_m = in_f(v, out_m, in_n)                       # eqn.inptm

            # (T_{(v,out_m,in_n)} in_f)^T omega_M(in_m).
            omega_M_val = A_M @ in_m + b_M

            # We compute (T out_f)^T xi_N = (xi_V_a, xi_M_a)
            # and (T in_f)^T omega_M_val = (xi_V_b, xi_M_b, xi_inN_b)
            # and dU = (xi_V_c, xi_M_c, xi_inN_c).
            # Sum these to get (xi_V, xi_M, xi_inN).

            def out_f_pair(va, ma):
                return out_f(va, ma)

            (_, _), vjp_out_f = jax.vjp(out_f_pair, v, out_m)
            xi_V_a, xi_M_a = vjp_out_f(xi_N)

            def in_f_triple(va, ma, na):
                return in_f(va, ma, na)

            _, vjp_in_f = jax.vjp(in_f_triple, v, out_m, in_n)
            xi_V_b, xi_M_b, xi_inN_b = vjp_in_f(omega_M_val)

            # dU(v, out_m, in_n).
            dU_v, dU_m, dU_n = jax.grad(U, argnums=(0, 1, 2))(v, out_m, in_n)

            xi_V = xi_V_a + xi_V_b + dU_v
            xi_M = xi_M_a + xi_M_b + dU_m
            # xi_inN = xi_inN_b + dU_n  # equals omega_N(in_n); not needed for out_dir.

            # Output direction is (xi_M, in_m) (paper line 2287-2289).
            return (xi_M, in_m)

        # The inner-hom poly map (the action a^beta(s) in def.pq_coalg).
        act = PolyMap(
            src=src_p,
            tgt=tgt_p,
            position_action=position_action,
            direction_action=direction_action,
            label="Phi(plm)",
        )

        # ------------------------------------------------------------------
        # Moore-form fiber: in_pos -> (out_pos, in_dir -> (out_dir, new_state))
        # The state update closes over the captured in_pos (eqn.state_update).
        # ------------------------------------------------------------------

        def fiber(in_pos):
            out_pos = position_action(in_pos)
            out_m, omega_M = in_pos
            A_M, b_M = omega_M

            def at_pos(in_dir):
                xi_N, in_n = in_dir
                in_m = in_f(v, out_m, in_n)                 # eqn.inptm
                omega_M_val = A_M @ in_m + b_M

                # Pullback covectors and dU contributions (eqn.bigtheta).
                _, vjp_out_f = jax.vjp(lambda va, ma: out_f(va, ma),
                                        v, out_m)
                xi_V_a, xi_M_a = vjp_out_f(xi_N)
                _, vjp_in_f = jax.vjp(
                    lambda va, ma, na: in_f(va, ma, na), v, out_m, in_n
                )
                xi_V_b, xi_M_b, _ = vjp_in_f(omega_M_val)
                dU_v, dU_m, _ = jax.grad(U, argnums=(0, 1, 2))(v, out_m, in_n)

                xi_V = xi_V_a + xi_V_b + dU_v
                xi_M = xi_M_a + xi_M_b + dU_m

                out_dir = (xi_M, in_m)

                # State update (eqn.state_update):
                #   x' = (v + sharp_V(xi), xi - xi_V).
                new_v = v + sharp_V @ xi
                new_xi = xi - xi_V
                return out_dir, (new_v, new_xi)

            return out_pos, at_pos

        return act, fiber

    return OrgMorphism(
        src_poly=src_p,
        tgt_poly=tgt_p,
        state=init_state,
        step=step,
    )


# ---------------------------------------------------------------------------
# Phi: potlens -> org (thm.functor).
# ---------------------------------------------------------------------------


def Phi(plm: PotLensMap) -> OrgMorphism:
    """Implements thm.functor; the composite ``cint -> leg -> dyn``."""
    return dyn(leg(cint(plm)))
