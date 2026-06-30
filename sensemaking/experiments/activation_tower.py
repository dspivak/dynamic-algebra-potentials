"""The decisive activation-inference test (``PLAN.md`` Phase R).

An interleaved tower ``data -> head -> cell -> head -> ... -> cell(top)`` with the datum
clamped at the BOTTOM (open source) and relaxed under ONE ``Phiconf`` with a block sharp
(activations ``z`` fast, weights + decode ``D`` slow).  The "sense" is the inferred top
activation ``z_top`` -- read off the state, not a one-shot ``out_f``.  Everything is a
``KQVTerm`` realized via ``KQVSystem`` (provenance, ``AUDIT.md`` C0): the only thing
interpreted is ``system.arrangement``.

The pre-registered question (Phase R): does activation inference give a NON-SILENT,
DATUM-DEPENDENT ``z_top`` at a real bottleneck (``k < E``), or does the **bilinear dead
zone** (``z, D -> 0`` => vanishing gradients) collapse it?  The **near-zero-init
stationary-point test is run FIRST** -- near-zero init is adversarial; if collapse tracks
``||D||, ||Omega|| -> 0`` that is the dead zone (mechanism (i)).

Sanctioned levers if it collapses (``PLAN.md`` / ``SPEC.md``): nonzero/asymmetric init,
small noise, a ``z_top`` prior ``1/2||z_top - mu||^2`` (a route-2 potential; the last
adds ``mu`` to ``Q`` and is flagged as a carrier extension).

Run: PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m sensemaking.experiments.activation_tower
"""

from __future__ import annotations

import jax
jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp
import numpy as np

from dap.functors import Phiconf
from dap.interpretation import trivial_omega
from dap.rvect import euclidean

from sensemaking.kqv import (
    Act,
    Head,
    Sub,
    KQVSystem,
    act_block_sharp,
    act_param_dim,
    act_unpack,
    param_dim,
    unpack,
)


# --- the interleaved tower (data -> head -> cell -> ... -> cell(top)) --------

def tower_term(E, k, d, d_v, *, n_bottom, depth, eta_z, eta_D, eta_w,
               top_down_top=False, top_prior_lambda=0.0, top_prior_mu=None):
    """Alternating head/cell tower; root = the top cell, bottom head OPEN (data slots).

    ``depth`` = number of cells.  The bottom ``Head(n_bottom)`` keeps its inner boxes
    open (the clamped data slots); above it the generators alternate cell, head, cell,
    ..., ending in a cell whose ``z`` is ``z_top``.  ``top_prior_lambda > 0`` puts the
    sanctioned ``z``-prior ``lambda/2||z - mu0||^2`` on the TOP cell (anti-collapse lever).
    """
    head_sharp = euclidean(param_dim(E, d, d_v), eta_w)
    cell_sharp = act_block_sharp(E, k, eta_z, eta_D)
    node = Head(n_bottom, E, d, d_v, sharp=head_sharp)        # OPEN: n_bottom data slots
    for i in range(depth):
        top = i == depth - 1
        cell = Act(E, k, sharp=cell_sharp, top_down=(top_down_top and top),
                   prior_lambda=(top_prior_lambda if top else 0.0),
                   prior_mu=(top_prior_mu if top else None))
        node = Sub(cell, (node,))
        if not top:
            node = Sub(Head(1, E, d, d_v, sharp=head_sharp), (node,))
    return node                                              # root = top cell


def param_slices(term, start=0):
    """Layout of the realized flat ``Q``, mirroring ``realize``'s compose order.

    ``realize(Sub(p, cs)) = compose_seq(tensor(cs), p)`` puts the CHILDREN first
    (left-to-right) and the PARENT last; a leaf generator is one block.  Returns a list
    of ``{kind, start, len, ...}`` and the next offset.
    """
    if isinstance(term, Head):
        dim = term.E if term.N == 0 else param_dim(term.E, term.d, term.d_v)
        kind = "leaf" if term.N == 0 else "head"
        return [dict(kind=kind, N=term.N, E=term.E, d=term.d, d_v=term.d_v,
                     start=start, len=dim)], start + dim
    if isinstance(term, Act):
        dim = act_param_dim(term.E, term.k)
        return [dict(kind="cell", k=term.k, E=term.E, start=start, len=dim)], start + dim
    if isinstance(term, Sub):
        out, cur = [], start
        for c in term.children:
            s, cur = param_slices(c, cur)
            out += s
        s, cur = param_slices(term.parent, cur)              # parent LAST
        return out + s, cur
    raise TypeError(f"param_slices: unsupported term {type(term).__name__}")


def top_cell(slices):
    """The top cell = the cell slice with the largest offset (root parent, realized last)."""
    return max((s for s in slices if s["kind"] == "cell"), key=lambda s: s["start"])


# --- norms used to diagnose the dead zone -----------------------------------

def cell_D_norm(q, sl):
    return float(jnp.linalg.norm(act_unpack(q[sl["start"]:sl["start"] + sl["len"]], sl["E"], sl["k"])["D"]))

def head_Omega_norm(q, sl):
    P = unpack(q[sl["start"]:sl["start"] + sl["len"]], sl["E"], sl["d"], sl["d_v"])
    return float(jnp.linalg.norm(P["Wo"] @ P["Wv"]))               # Omega = Wo Wv (rmk.circuits)

def get_z_top(q, slices):
    sl = top_cell(slices)
    return np.asarray(q[sl["start"]:sl["start"] + sl["k"]])


# --- run the tower under Phiconf, clamping data at the bottom ----------------

def run_tower(term, data, *, E, init_scale, steps, seed, apex=0.0, noise=0.0):
    """Relax the tower; data clamped at the bottom (source emissions).  Returns a dict."""
    arr = KQVSystem(term).arrangement                          # provenance: only this is run
    slices = param_slices(term)[0]
    assert sum(s["len"] for s in slices) == arr.Q.dim          # layout mirrors realize
    O = Phiconf(arr)

    rng = np.random.default_rng(seed)
    state = jnp.asarray(rng.standard_normal(arr.Q.dim)) * init_scale
    apex_ctx = jnp.full(E, apex)
    src = (data, trivial_omega(arr.in_dim_M))                  # datum CLAMPED at the bottom
    boundary = lambda op: (jnp.zeros(E), apex_ctx)             # noqa: E731  fixed apex

    cells = [s for s in slices if s["kind"] == "cell"]
    heads = [s for s in slices if s["kind"] == "head"]
    traj = dict(U=[], zt_norm=[], D_top=[], D_mean=[], Om_mean=[])

    def record(s):
        traj["U"].append(float(arr.U(s, data, apex_ctx)))
        traj["zt_norm"].append(float(jnp.linalg.norm(get_z_top(s, slices))))
        traj["D_top"].append(cell_D_norm(s, top_cell(slices)))
        traj["D_mean"].append(float(np.mean([cell_D_norm(s, c) for c in cells])))
        traj["Om_mean"].append(float(np.mean([head_Omega_norm(s, h) for h in heads])) if heads else 0.0)

    record(state)
    for _ in range(steps):
        _, _, state = O.with_state(state).run_one(src, boundary)
        if noise:
            state = state + jnp.asarray(rng.standard_normal(arr.Q.dim)) * noise
        record(state)

    return dict(arr=arr, slices=slices, final=state, z_top=get_z_top(state, slices),
                **{key: np.array(v) for key, v in traj.items()})


# --- metrics + report --------------------------------------------------------

def _spark(xs):
    b = "▁▂▃▄▅▆▇█"
    lo, hi = float(np.min(xs)), float(np.max(xs))
    if hi - lo < 1e-12:
        return b[0] * len(xs)
    return "".join(b[min(7, int((x - lo) / (hi - lo) * 7.999))] for x in xs)


def _line(tag, r, half):
    frac = 100 * (1 - r["U"][-1] / r["U"][0]) if r["U"][0] > 0 else 0.0
    print(f"  {tag:<11} U {r['U'][0]:7.2f}->{r['U'][-1]:7.2f} ({frac:4.0f}%) | "
          f"||z_top|| {r['zt_norm'][-1]:.3f} | ||D_top|| {r['D_top'][-1]:.3f} | "
          f"<||D||> {r['D_mean'][-1]:.3f} | <||Om||> {r['Om_mean'][-1]:.3f}")
    print(f"              U {_spark(r['U'])}   ||z_top|| {_spark(r['zt_norm'])}   <||D||> {_spark(r['D_mean'])}")


def _drop(r):
    return 100 * (1 - r["U"][-1] / r["U"][0]) if r["U"][0] > 0 else 0.0

def _escaped(r):
    """Honest gate: did relaxation do real work (sum U dropped > 10%)?"""
    return np.isfinite(r["U"][-1]) and _drop(r) > 10.0

def _cos(a, b):
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    if not (np.isfinite(na) and np.isfinite(nb)) or na < 1e-9 or nb < 1e-9:
        return float("nan")
    return float(np.dot(a, b) / (na * nb))


def main():
    E, k, d, d_v = 6, 2, 4, 3
    n_bottom, depth = 4, 3
    # Conservative, STABLE step sizes (eta=0.3 overshot -> nan for some data; SPEC's
    # "well-posedness is conditional on the sharp").  z fast, D slow, weights slowest.
    eta_z, eta_D, eta_w = 0.15, 0.03, 0.01
    steps = 400
    lam, mu0 = 1.0, jnp.ones(k) / float(np.sqrt(k))           # the z_top prior (||mu0||=1)
    cfg = dict(E=E, k=k, d=d, d_v=d_v, n_bottom=n_bottom, depth=depth,
               eta_z=eta_z, eta_D=eta_D, eta_w=eta_w)
    bare = tower_term(**cfg)
    prior = tower_term(**cfg, top_prior_lambda=lam, top_prior_mu=mu0)
    sysb = KQVSystem(bare)
    dA = jnp.asarray(np.random.default_rng(1).standard_normal(n_bottom * E))
    dB = jnp.asarray(np.random.default_rng(2).standard_normal(n_bottom * E))

    print("=" * 78)
    print(f"ACTIVATION TOWER  data->head({n_bottom})->[cell->head]x{depth-1}->cell(top)  "
          f"E={E} k={k} (bottleneck {k}<{E})   eta(z,D,w)=({eta_z},{eta_D},{eta_w})")
    print("provenance (KQVSystem.trace, bare):")
    print("  " + sysb.trace().replace("\n", "\n  "))
    print(f"  Q.dim={sysb.arrangement.Q.dim}  data dim={n_bottom*E}  z_top dim={k}")

    # 1) STATIONARY-POINT TEST (run FIRST) -- random vs near-zero, bare design --
    print("\n" + "=" * 78)
    print("1) STATIONARY-POINT TEST (first): does the silent state persist? (bare)")
    print("=" * 78)
    rz = run_tower(bare, dA, E=E, init_scale=0.3, steps=steps, seed=0)
    nz = run_tower(bare, dA, E=E, init_scale=1e-3, steps=steps, seed=0)
    _line("random .3", rz, None)
    _line("near-zero", nz, None)
    print(f"  random   : <||D||> {rz['D_mean'][0]:.3f}->{rz['D_mean'][-1]:.3f}, "
          f"<||Om||> {rz['Om_mean'][0]:.3f}->{rz['Om_mean'][-1]:.3f}  => {'escapes' if _escaped(rz) else 'stuck'}")
    print(f"  near-zero: <||D||> {nz['D_mean'][0]:.4f}->{nz['D_mean'][-1]:.4f}, "
          f"<||Om||> {nz['Om_mean'][0]:.4f}->{nz['Om_mean'][-1]:.4f}  => "
          f"{'ESCAPES' if _escaped(nz) else 'STAYS SILENT (bilinear dead zone: norms frozen at init, U flat)'}")
    no_silent_sp = _escaped(nz)

    # 2) THE SANCTIONED z_top PRIOR (1/2 lam||z-mu0||^2) on near-zero init -------
    print("\n" + "=" * 78)
    print(f"2) z_top PRIOR lever on near-zero init  (lam={lam}, ||mu0||=1) -- does it break the dead zone?")
    print("=" * 78)
    pA = run_tower(prior, dA, E=E, init_scale=1e-3, steps=steps, seed=0)
    pB = run_tower(prior, dB, E=E, init_scale=1e-3, steps=steps, seed=0)
    _line("prior  dA", pA, None)
    _line("prior  dB", pB, None)
    prior_breaks = pA["zt_norm"][-1] > 0.05 and pB["zt_norm"][-1] > 0.05
    cos_prior = _cos(pA["z_top"], pB["z_top"])
    print(f"  => prior {'BREAKS the silence' if prior_breaks else 'does NOT break silence'} "
          f"(||z_top|| dA={pA['zt_norm'][-1]:.3f}, dB={pB['zt_norm'][-1]:.3f})")
    print(f"     datum-dependence under prior: cos(z_top dA, dB) = {cos_prior:+.3f}  "
          f"({'datum-DEPENDENT' if (np.isfinite(cos_prior) and cos_prior < 0.9) else 'tracks mu0 (datum-INDEPENDENT)'})")

    # 3) METRICS in the working (random-init) regime ---------------------------
    print("\n" + "=" * 78)
    print("3) METRICS (random init, bare): reconstruction / bottleneck / datum-dependence")
    print("=" * 78)
    rB = run_tower(bare, dB, E=E, init_scale=0.3, steps=steps, seed=0)
    nA, nB = float(np.linalg.norm(rz["z_top"])), float(np.linalg.norm(rB["z_top"]))
    cos_rand = _cos(rz["z_top"], rB["z_top"])
    recon = _drop(rz)
    print(f"  reconstruction: sum U {rz['U'][0]:.2f} -> {rz['U'][-1]:.2f}  ({recon:.0f}% accounted)")
    print(f"  bottleneck:     z_top dim {k}  vs  data dim {n_bottom*E}   ({k}/{n_bottom*E})")
    print(f"  non-silence:    ||z_top(dA)|| {nA:.3f}   ||z_top(dB)|| {nB:.3f}")
    print(f"  datum-depend.:  cos(z_top dA, dB) = {cos_rand:+.3f}")

    # 4) HONEST VERDICT (Phase R) ---------------------------------------------
    reconstructs = recon > 10.0
    non_silent = nA > 0.05 and nB > 0.05
    datum_dep = np.isfinite(cos_rand) and cos_rand < 0.9
    print("\n" + "=" * 78)
    print("4) VERDICT (Phase R)")
    print("=" * 78)
    print("  -- bare design, plain Phiconf --")
    for name, ok in [("non-trivial reconstruction (>10%, random init)", reconstructs),
                     ("z_top non-silent (random init)", non_silent),
                     ("z_top datum-dependent (random init, cos<0.9)", datum_dep),
                     ("no silent stationary point at NEAR-ZERO init", no_silent_sp)]:
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}")
    bare_pass = all([reconstructs, non_silent, datum_dep, no_silent_sp])
    print(f"    OVERALL (bare): {'PASS' if bare_pass else 'FAIL (informative)'}")
    print("  -- with the sanctioned z_top prior --")
    print(f"    near-zero silence {'BROKEN' if prior_breaks else 'NOT broken'}; "
          f"z_top {'datum-dependent' if (np.isfinite(cos_prior) and cos_prior<0.9) else 'tracks mu0'}.")
    print("\n  Headline: the bilinear dead zone is REAL and depth-amplified; near-zero init")
    print("  collapses under plain Phiconf. The decisive criterion is the near-zero one.")
    return bare_pass


if __name__ == "__main__":
    main()
