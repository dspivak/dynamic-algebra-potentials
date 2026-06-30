"""KQV activation cell: Generator 3 of the attention suboperad (route 2).

Faithful to ``SPEC.md`` ("Generator 3 -- the activation cell"). A cell is an
**arity-1** ``SmoothArrangement``

    act : (R^E | R^E)  -->  (R^E | R^E)

a state box on a wire, so an inferred activation can sit at an *interior* level of a
tower of heads.  Its reactive parameter ``Q`` carries a fast **activation**
``z in Z = R^k`` (the cause) and a slow **decode** ``D : R^k -> R^E``
(``Q = Z (+) Hom(R^k, R^E)``), under a **block sharp** (``z`` fast, ``D`` slow).  The
bottleneck ``k <= E`` (like ``d_v`` the rank ``k`` never reaches the interface).  The
three smooth maps are exactly

    out_f(z, D ; h)    = D z                       -- emit the cause upward; Moore: no n
    in_f(z, D ; h, n)  = n                          -- transparent backward leg
    U(z, D ; h, n)     = 1/2 || h - D z ||^2        -- bottom-up reconstruction

(optionally plus a top-down term ``1/2 || D z - n ||^2`` for a symmetric Rao--Ballard
cell).  The child ``h`` enters *only* through ``U``: relaxing ``z`` to minimize
``1/2||h - D z||^2`` *is* the projection ``z* = D^+ h`` of ``h`` into the code -- there
is no explicit encoder ``R^E -> R^k`` (``SPEC.md``, "Input = projection by inference").

The decode ``D`` is **learned**, so it lives in ``Q`` (``AUDIT.md`` G1): the cell is a
linear autoencoder with an *inferred* code.  Because ``Z`` and ``Hom(R^k, R^E)`` are
R-vector spaces (G3) and the cell is built only from substitution + the lens tensor
(G5), adding it keeps us a **suboperad of ``sarr``** -- the closure of one more
``sarr``-generator under the *same* operad operations.

The fast/slow split is **data of ``Q``** (the block sharp ``act_block_sharp``,
``rmk.optimizer``), never an external optimizer: a large ``eta`` on the ``z`` block and
a small ``eta`` on the ``D`` block makes the activation relax (inference) inside each
slow ``D`` step (learning).  This is the only thing the auditor must check is *inside*
the formalism (``AUDIT.md`` G4).
"""

from __future__ import annotations

import math

import jax.numpy as jnp
from jax import Array

from dap.arrangement import SmoothArrangement
from dap.rvect import ReactiveVectorSpace, diagonal


def _act_layout(E: int, k: int):
    """Parameter blocks of a cell, in packing order: fast ``z`` then slow ``D``."""
    return (
        ("z", (k,)),       # the activation / cause -- fast
        ("D", (E, k)),     # the decode R^k -> R^E   -- slow (learned, lives in Q: G1)
    )


def act_param_dim(E: int, k: int) -> int:
    """Dimension of the cell's reactive parameter ``Q = Z (+) Hom(R^k, R^E)``."""
    return sum(math.prod(shape) for _, shape in _act_layout(E, k))


def act_unpack(q: Array, E: int, k: int) -> dict:
    """Split the flat parameter ``q in Q`` into ``{z, D}`` (``z`` first, then ``D``)."""
    out, i = {}, 0
    for name, shape in _act_layout(E, k):
        n = math.prod(shape)
        out[name] = q[i : i + n].reshape(shape)
        i += n
    return out


def act_block_sharp(E: int, k: int, eta_z: float = 1.0, eta_D: float = 1.0) -> ReactiveVectorSpace:
    """The cell's **block sharp** (``rmk.optimizer``): ``z`` fast, ``D`` slow.

    A constant diagonal sharp ``diag(eta_z * I_k, eta_D * I_{E k})`` on
    ``Q = Z (+) Hom(R^k, R^E)``.  With ``eta_z >> eta_D`` the activation equilibrates
    (inference) inside each slow ``D`` step (learning) -- the two-timescale split of
    ``PLAN.md`` Phase R, written into the metric of ``Q`` (G4), not an outside optimizer.
    ``eta_z = eta_D = 1`` recovers plain gradient descent (the Euclidean sharp).
    """
    diag = jnp.concatenate([jnp.full(k, float(eta_z)), jnp.full(E * k, float(eta_D))])
    return diagonal(diag)


def activation_cell(
    E: int, k: int, *, sharp=None, top_down: bool = False,
    prior_mu=None, prior_lambda: float = 0.0, label=None,
) -> SmoothArrangement:
    """The activation-cell generator (Generator 3, ``SPEC.md``).

    Arity-1 ``(R^E|R^E) -> (R^E|R^E)``; carrier ``Q = R^k (+) R^{E x k}`` (fast ``z``,
    slow ``D``).  ``sharp`` is the reactive vector space on ``Q`` (the optimizer,
    ``rmk.optimizer``); default the block sharp ``act_block_sharp(E, k)`` (Euclidean
    until the timescale split is dialed in).  ``top_down=True`` adds the optional
    symmetric Rao--Ballard term ``1/2||D z - n||^2``.

    ``prior_lambda > 0`` adds the **``z``-prior potential** ``lambda/2 || z - mu0 ||^2``
    (``mu0 = prior_mu``, a fixed length-``k`` vector): the route-2 anti-collapse lever of
    ``SPEC.md`` ("Top-closure caveat", "Bilinear dead zone").  It is a potential term
    (writer monad), still an ``sarr`` arrangement; with ``mu0 != 0`` it makes
    ``dU/dz|_{z=0} = -lambda*mu0 != 0``, so the all-zero state is no longer stationary --
    breaking the dead zone.  (The SPEC's *learned* ``mu`` is the multi-datum form; here
    ``mu0`` is a fixed hyperparameter, the single-datum lever -- see SPEC-gap note in
    ``activation_tower.py``.)
    """
    if E < 1:
        raise ValueError("residual width E must be >= 1")
    if k < 1:
        raise ValueError("code rank k must be >= 1")

    dim = act_param_dim(E, k)
    Q = sharp if sharp is not None else act_block_sharp(E, k)
    if Q.dim != dim:
        raise ValueError(f"sharp dim {Q.dim} != cell param dim {dim}")
    lam = float(prior_lambda)
    mu0 = jnp.zeros(k) if prior_mu is None else jnp.asarray(prior_mu, float)
    if mu0.shape != (k,):
        raise ValueError(f"prior_mu must have shape ({k},), got {mu0.shape}")

    def out_f(q: Array, m_out: Array) -> Array:
        # SPEC Gen 3: out_f(z, D ; h) = D z.  Moore: no n (the read-out cannot see the
        # descending context).  The child emission h = m_out is IGNORED here -- it
        # enters only through U (input = projection by inference).
        P = act_unpack(q, E, k)
        return P["D"] @ P["z"]

    def in_f(q: Array, m_out: Array, n_in: Array) -> Array:
        # SPEC Gen 3: in_f(z, D ; h, n) = n.  Transparent backward leg: the descending
        # prediction passes straight through to the child.
        return n_in

    def U(q: Array, m_out: Array, n_in: Array) -> Array:
        # SPEC Gen 3: U = 1/2||h - D z||^2 (bottom-up reconstruction); optionally
        # + 1/2||D z - n||^2 (top-down, symmetric Rao-Ballard); + lambda/2||z - mu0||^2
        # (the sanctioned z-prior, anti-collapse lever).
        P = act_unpack(q, E, k)
        Dz = P["D"] @ P["z"]
        u = 0.5 * jnp.sum((m_out - Dz) ** 2)
        if top_down:
            u = u + 0.5 * jnp.sum((Dz - n_in) ** 2)
        if lam:
            u = u + 0.5 * lam * jnp.sum((P["z"] - mu0) ** 2)
        return u

    return SmoothArrangement(
        Q=Q,
        out_dim_M=E,
        in_dim_M=E,
        out_dim_N=E,
        in_dim_N=E,
        out_f=out_f,
        in_f=in_f,
        U=U,
        label=label or f"kqv_cell(k={k},E={E})",
    )
