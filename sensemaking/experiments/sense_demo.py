"""Sense-making demo (Stage-4 seed): data in at the BOTTOM, sense out at the TOP.

THE REFRAME (replaces the dead necessity-gate / chaotic-world branch). We realize the
Dama--Spivak "account of sense-making" arc inside DAP via the KQV suboperad: operadic
composition is a TOWER OF ABSTRACTION LEVELS. A nested arrangement of attention heads
takes a low-level datum in at the bottom and coordinates it up into a single high-level
"sense" at the top. Interpreted under ``Phiconf`` this is hierarchical predictive coding
(``slo.pc`` of attention-suboperad.tex): predictions flow down, errors flow up, the
configuration relaxes to minimize ``sum U``. The settling is the "click".

ORIENTATION MATTERS -- this file is the finding.

  * DATA AT THE TOP (closed tree, ``relax_top``): a tree bottoming out in 0-ary priors is
    closed at the bottom, open at the top; hand the datum to the open top. It RELAXES, but
    DEGENERATELY -- ``sum U -> 0`` the lazy way: the free priors copy the (barely-moved)
    top-down predictions and the read-out collapses to ~0. The datum is *ignored*, not
    represented. This is posterior collapse: the bare potential's global min is the trivial
    fixed point, so an unclamped top target can always be explained by going silent.

  * DATA AT THE BOTTOM (open tree, ``relax_bottom``): leave the bottom boxes OPEN and clamp
    the datum there, as the source emissions. Now the datum is an IMMOVABLE BOUNDARY -- the
    tower cannot zero it -- so it must relax its weights to ACCOUNT for it. The sense is the
    root's top emission. Result: a *nested* tower (depth >= 2) coordinates the bottom slots
    into a non-silent, DATUM-DEPENDENT top sense; a flat single head cannot (depth does real
    work). The account is PARTIAL (``sum U`` settles well above 0) -- a compressive sense,
    not a copy, which is the point.

HONEST SCOPE. This is single-datum *weight* relaxation (fit the tower to account for one
clamped datum), not yet multi-datum learning or activation inference, and the read-out is
the root's bottom-up emission. Genuine sense-making across data, and supersession (behavior
running off the formed sense), are the next steps. Provenance: everything is a ``KQVTerm``
realized via ``KQVSystem.arrangement`` (factors through the KQV suboperad by construction).

Run: PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m sensemaking.experiments.sense_demo
"""

from __future__ import annotations

import jax
jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp
import numpy as np

from dap.functors import Phiconf
from dap.interpretation import trivial_omega
from dap.rvect import euclidean

from sensemaking.kqv.operad import Head, Sub, KQVSystem, leaf
from sensemaking.kqv.head import param_dim


# --- two towers, same generators, opposite orientation -----------------------

def closed_tower(E, d, d_v, arities, eta):
    """Balanced CLOSED tree (``Builder.nest``): bottoms out in 0-ary priors, open at top."""
    if not arities:
        return leaf(E, sharp=euclidean(E, eta))
    N, rest = arities[0], arities[1:]
    parent = Head(N, E, d, d_v, sharp=euclidean(param_dim(E, d, d_v), eta))
    return Sub(parent, tuple(closed_tower(E, d, d_v, rest, eta) for _ in range(N)))


def open_tower(E, d, d_v, arities, eta):
    """OPEN tree: bottom heads keep their inner boxes open -- those are the clamped data slots."""
    N, rest = arities[0], arities[1:]
    parent = Head(N, E, d, d_v, sharp=euclidean(param_dim(E, d, d_v), eta))
    if not rest:
        return parent
    return Sub(parent, tuple(open_tower(E, d, d_v, rest, eta) for _ in range(N)))


# --- relaxation under Phiconf ------------------------------------------------

def relax_top(arities, *, E=4, d=4, d_v=4, eta=0.15, steps=150, seed=0, data_seed=1):
    """DATA AT THE TOP. Returns (sumU trajectory, settled root emission, datum)."""
    arr = KQVSystem(closed_tower(E, d, d_v, arities, eta)).arrangement
    assert arr.out_dim_M == 0 and arr.in_dim_N == E       # closed bottom, open top
    O = Phiconf(arr)
    state = jnp.asarray(np.random.default_rng(seed).standard_normal(arr.Q.dim)) * 0.3
    data = jnp.asarray(np.random.default_rng(data_seed).standard_normal(E))
    src = (jnp.zeros(0), trivial_omega(0))
    boundary = lambda out_pos: (jnp.zeros(E), data)        # datum handed to the open TOP
    Us = [float(arr.U(state, jnp.zeros(0), data))]
    for _ in range(steps):
        out_pos, _, state = O.with_state(state).run_one(src, boundary)
        Us.append(float(arr.U(state, jnp.zeros(0), data)))
    return np.array(Us), np.asarray(out_pos[0]), np.asarray(data)


def relax_bottom(arities, *, E=4, d=4, d_v=4, eta=0.05, steps=400, seed=0, data_seed=1, apex=0.0):
    """DATA AT THE BOTTOM. Returns (sumU trajectory, settled top sense, datum, #slots)."""
    arr = KQVSystem(open_tower(E, d, d_v, arities, eta)).arrangement
    assert arr.out_dim_M > 0 and arr.in_dim_N == E         # open bottom (data clamps here)
    O = Phiconf(arr)
    state = jnp.asarray(np.random.default_rng(seed).standard_normal(arr.Q.dim)) * 0.3
    data = jnp.asarray(np.random.default_rng(data_seed).standard_normal(arr.out_dim_M))
    apex_ctx = jnp.full(E, apex)                            # fixed apex context (NOT the data)
    src = (data, trivial_omega(arr.in_dim_M))              # datum CLAMPED at the bottom
    boundary = lambda out_pos: (jnp.zeros(E), apex_ctx)
    Us = [float(arr.U(state, data, apex_ctx))]
    for _ in range(steps):
        out_pos, _, state = O.with_state(state).run_one(src, boundary)
        Us.append(float(arr.U(state, data, apex_ctx)))
    return np.array(Us), np.asarray(out_pos[0]), np.asarray(data), arr.out_dim_M // E


def _spark(xs):
    b = "▁▂▃▄▅▆▇█"
    lo, hi = min(xs), max(xs)
    if hi - lo < 1e-12:
        return b[0] * len(xs)
    return "".join(b[min(7, int((x - lo) / (hi - lo) * 7.999))] for x in xs)


if __name__ == "__main__":
    print("=" * 72)
    print("DATA AT THE TOP (closed tree) -- relaxes, but degenerately (collapse)")
    print("=" * 72)
    Us, root, data = relax_top([2, 2])
    print(f"  nest([2,2]):  sum U {Us[0]:.3f} -> {Us[-1]:.1e}   relax: {_spark(Us[::5])}")
    print(f"  settled root emission norm = {np.linalg.norm(root):.3f}  (~0 => the tower went SILENT)")
    print(f"  datum norm = {np.linalg.norm(data):.3f}  -> the datum is ignored, not represented.")

    print("\n" + "=" * 72)
    print("DATA AT THE BOTTOM (open tree) -- the datum is an immovable boundary")
    print("=" * 72)
    for arities, name in (([6], "flat  [6]   "), ([2, 3], "nested [2,3]")):
        Us, sense, data, nslots = relax_bottom(arities)
        print(f"  {name}: {nslots} bottom slots -> 1 top sense | "
              f"sum U {Us[0]:.2f} -> {Us[-1]:.2f} ({100*(1-Us[-1]/Us[0]):.0f}%) "
              f"| sense norm {np.linalg.norm(sense):.3f}")
        print(f"               relax: {_spark(Us[::max(1,len(Us)//40)])}")
    print("  => depth does the work: the flat head stays ~silent; the nested tower forms a sense.")

    print("\n" + "=" * 72)
    print("Does the SENSE depend on the datum? (nested [2,3], two different bottom data)")
    print("=" * 72)
    _, sA, _, _ = relax_bottom([2, 3], data_seed=1)
    _, sB, _, _ = relax_bottom([2, 3], data_seed=2)
    cos = float(np.dot(sA, sB) / (np.linalg.norm(sA) * np.linalg.norm(sB) + 1e-12))
    print(f"  ||sense_A - sense_B|| = {np.linalg.norm(sA - sB):.3f},  cos = {cos:+.3f}")
    print("  > 0 and cos < 1  =>  the top sense DEPENDS on the bottom datum (no collapse).")
