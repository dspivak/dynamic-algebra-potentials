"""Stage 3 (revised after adversarial audit): beta-mediated self-maintenance & bistability.

HONEST FRAMING -- the result, stated plainly so the caveats can't be missed:

  This demonstrates beta-mediated SELF-MAINTENANCE and BISTABILITY of a KQV-STYLE attention
  circuit under a soft fetch reward. A bound state maintains itself while it keeps being
  right; a perturbation above the basin threshold self-repairs; prolonged impossible-world
  dynamics drive beta into the dead basin. **IRREVERSIBILITY IS NOT INTRINSIC** -- restoring
  the world revives beta at margin 0, 0.05, 0.1 (and, for some seeds, even at the null+eps
  maintenance margin). Death sticks reliably only under a STRICTER reward cutoff (~0.2). See
  `margin_sweep`.

  PROVENANCE -- **Stage 3 is an EXTENSION of the audited KQV circuit, NOT an element of the
  original KQV suboperad.** `fetch_beta` hand-codes the QK-match + OV-copy with an explicit
  temperature, softmax(beta * QK^T / sqrt(d)) -- mathematically the audited circuit plus a
  beta knob, but it BYPASSES the formal `KQVSystem(...).arrangement` provenance path. The
  beta-dynamics is new structure; it is NOT hidden inside the suboperad.

  REWARD -- the reward is soft fetch R^2 (`_r2`). It is beta-dependent because it scores the
  COPIED PAYLOAD (the soft-attention-weighted value), which genuinely degrades as beta
  flattens. It is NOT argmax routing: argmax(softmax(beta*s)) is beta-INVARIANT for beta>0
  (beta does not reorder logits), so `routing_acc` is kept ONLY as an interpretability
  diagnostic -- never as reward or as evidence of aliveness.

  TWO MARGINS -- reward is paid only for performance ABOVE a margin, and the two roles need
  DIFFERENT margins. Do not conflate them:
    * MAINTENANCE margin = null+eps (`maintenance_margin`). Flat (beta=0) attention scores
      fetch R^2 ~ 0.16-0.17 (`null_r2`); null+eps zeroes chance-level credit PER TRAINED MODEL,
      giving a genuine dead attractor at beta=0. This is LOAD-BEARING for SELF-MAINTENANCE and
      BISTABILITY (R2) and holds across seeds 0,1,2.
    * IRREVERSIBILITY margin = ~0.2 (`IRREVERSIBILITY_MARGIN`). MARGIN-CONDITIONED
      irreversibility (R3) needs a STRICTER cutoff. The per-seed irreversibility knee sits in
      [0.18, 0.20], and null+eps (~0.19) STRADDLES it: seeds 0,1 revive under null+eps, seed 2
      dies. So **null+eps does NOT reliably earn irreversibility** -- only margin >= ~0.2 kills
      all seeds. The maintenance margin is not an irreversibility margin.

REVISED CRITERIA (after the audit; the original commit overstated irreversibility as intrinsic):
  R1  sharpness load-bearing: fetch R^2 ~ null at beta=0, > 0.85 by beta>=1, rises then plateaus.
  R2  self-maintenance (MAINTENANCE margin = null+eps), seeds 0,1,2: MAINTAIN / DISSOLVE /
      SELF-REPAIR / CONTROL (no-reward-coupling dies).
  R3  irreversibility is MARGIN-CONDITIONED, not intrinsic: margin=0 revives (intrinsic FAIL),
      seeds 0,1,2; margin >= ~0.2 stays dead (conditioned PASS), seeds 0,1,2. The null+eps
      maintenance margin is NOT sufficient across seeds -- it straddles the knee (seeds 0,1
      revive, seed 2 dies), so it is not claimed as an irreversibility margin.
  Numbers reported raw; nothing retuned to force a result.
"""

from __future__ import annotations

import jax
jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp
import numpy as np

from sensemaking.experiments.stage2_routing import D, DV, D_ID, E, E_VAL, N, VAL, gen_episodes
from sensemaking.kqv import param_dim, unpack

_CHANCE = 1.0 / N

# Stricter reward cutoff that margin-conditioned irreversibility (R3) needs. The per-seed
# irreversibility knee sits in [0.18, 0.20]; the null+eps maintenance margin (~0.19) straddles
# it, so it is NOT a reliable irreversibility margin. margin >= ~0.2 kills all seeds.
IRREVERSIBILITY_MARGIN = 0.2


def fetch_beta(W, h, beta):
    """KQV QK-match + OV-copy with an explicit inverse-temperature beta on the softmax.

    EXTENSION of the audited KQV circuit (not the formal suboperad path): the QK match and OV
    copy are the audited circuits; beta scales the logits (beta=0 -> uniform/flat; large ->
    sharp). Pure self-attention, no star column.
    """
    P = unpack(W, E, D, DV)
    hr = h.reshape(N, E)
    scores = (hr @ P["Wq"].T) @ (hr @ P["Wk"].T).T / jnp.sqrt(D)
    A = jax.nn.softmax(beta * scores, axis=1)
    return ((A @ (hr @ P["Wv"].T)) @ P["Wo"].T)[:, VAL]


def routing_acc(W, h_batch, t_batch, beta):
    """DIAGNOSTIC ONLY (never a reward). Fraction of boxes whose argmax attention hits target.

    NOTE: argmax(softmax(beta * scores)) is beta-INVARIANT for beta>0 -- it cannot distinguish
    a sharp self from a nearly-flat one, so it is NOT an aliveness measure. Use soft fetch R^2.
    """
    P = unpack(W, E, D, DV)

    def one(h):
        hr = h.reshape(N, E)
        s = (hr @ P["Wq"].T) @ (hr @ P["Wk"].T).T / jnp.sqrt(D)
        return jnp.argmax(jax.nn.softmax(beta * s, axis=1), axis=1)

    return float(jnp.mean(jax.vmap(one)(h_batch) == jnp.asarray(t_batch)))


def _r2(W, h, tgt, beta):
    """Soft fetch R^2 -- the reward. beta-dependent because it scores the copied payload."""
    out = jax.vmap(lambda x: fetch_beta(W, x, beta))(h)
    return float(1.0 - jnp.mean((out - tgt) ** 2) / jnp.mean((tgt - tgt.mean()) ** 2))


def null_r2(W, *, seed=0, n=200):
    """Flat-attention (beta=0) fetch R^2 -- the null baseline; reward is paid only above this."""
    h, tgt, _ = gen_episodes(n, np.random.default_rng(9000 + seed))
    return _r2(W, h, tgt, 0.0)


def maintenance_margin(W, *, seed=0, epsilon=0.03):
    """null+eps: the per-model no-credit-below-chance margin.

    LOAD-BEARING for the dead attractor / self-maintenance / bistability (R2); holds across
    seeds. It is NOT a reliable irreversibility margin (R3) -- it straddles the per-seed knee
    in [0.18, 0.20] (seeds 0,1 revive, seed 2 dies). Use `IRREVERSIBILITY_MARGIN` for R3.
    """
    return null_r2(W, seed=seed) + epsilon


def train(seed, *, lr=3e-3, steps=2500):
    """Train the fetch weights at beta=1 (Adam = a diagonal reactive sharp, rmk.optimizer)."""
    rng = np.random.default_rng(seed)
    h, tgt, _ = gen_episodes(400, rng)
    W0 = jnp.asarray(np.random.default_rng(1000 + seed).standard_normal(param_dim(E, D, DV))) * 0.1
    b1, b2, eps = 0.9, 0.999, 1e-8

    def loss(W):
        out = jax.vmap(lambda x: fetch_beta(W, x, 1.0))(h)
        return jnp.mean((out - tgt) ** 2)

    def step(carry, _):
        W, m, v, i = carry
        g = jax.grad(loss)(W)
        m, v, i = b1 * m + (1 - b1) * g, b2 * v + (1 - b2) * g * g, i + 1.0
        W = W - lr * (m / (1 - b1 ** i)) / (jnp.sqrt(v / (1 - b2 ** i)) + eps)
        return (W, m, v, i), None

    z = jnp.zeros_like(W0)
    (W, *_), _ = jax.lax.scan(step, (W0, z, z, 0.0), None, length=steps)
    return W


# ---- R1: sharpness sweep (fetch R^2 is the measure; routing_acc is a diagnostic) ----

def r1_curve(seed=0, betas=(0.0, 0.1, 0.25, 0.5, 0.75, 1.0, 2.0, 4.0, 8.0)):
    W = train(seed)
    h, tgt, t = gen_episodes(200, np.random.default_rng(9000 + seed))
    return W, [(b, _r2(W, h, tgt, b), routing_acc(W, h, t, b)) for b in betas]


# ---- R2: beta-dynamics (beta sustained by being right) ----

def _scramble(h, rng):
    """Make being-right impossible: randomize the query (address) so no box can locate its target."""
    h = np.asarray(h).copy()
    h[:, :, D_ID + E_VAL:] = rng.standard_normal(h[:, :, D_ID + E_VAL:].shape) / np.sqrt(D_ID)
    return jnp.asarray(h)


def run_dynamics(W, beta0, *, steps=160, world="predict", decay=0.1, gain=0.3,
                 margin=None, epsilon=0.03, knock=None, seed=0):
    """beta_{t+1} = (1-decay) beta + gain * reward, reward = max(0, soft fetch R^2 - margin).

    margin=None -> the MAINTENANCE margin null+eps (`maintenance_margin`); for R3
    irreversibility pass an explicit stricter margin (`IRREVERSIBILITY_MARGIN`).
    world: 'predict' / 'scramble' / 'switch' (predict then scramble @half) / 'revive' (scramble
    then world restored in the last third). knock=(step, value) externally sets beta once.
    """
    if margin is None:
        margin = maintenance_margin(W, seed=seed, epsilon=epsilon)
    rng = np.random.default_rng(7000 + seed)
    beta, traj = beta0, []
    for s in range(steps):
        h, tgt, _ = gen_episodes(48, rng)
        scrambled = (
            world == "scramble"
            or (world == "switch" and s >= steps // 2)
            or (world == "revive" and s < 2 * steps // 3)
        )
        if scrambled:
            h = _scramble(h, rng)
        reward = max(0.0, _r2(W, h, tgt, beta) - margin)  # soft, beta-dependent; null-rectified
        beta = (1 - decay) * beta + gain * reward
        if knock and s == knock[0]:
            beta = knock[1]
        traj.append((beta, reward))
    return traj


def margin_sweep(W, *, margins=(0.0, 0.05, 0.1, 0.2, 0.4), seed=0, steps=240):
    """Is irreversibility intrinsic or margin-induced? revive-world final beta per margin.

    Returns (label, margin, final_beta) rows for the fixed margins, then one extra row for the
    null+eps MAINTENANCE margin -- shown explicitly so it is visible that it straddles the knee
    (NOT a reliable irreversibility margin). margin=0/0.05/0.1 revive; margin>=~0.2 dies.
    """
    rows = [(f"{m:.2f}", m, run_dynamics(W, 2.8, world="revive", steps=steps, margin=m, seed=seed)[-1][0])
            for m in margins]
    nem = maintenance_margin(W, seed=seed)
    rows.append((f"null+eps={nem:.2f}", nem,
                 run_dynamics(W, 2.8, world="revive", steps=steps, margin=nem, seed=seed)[-1][0]))
    return rows


def initial_beta_sweep(W, *, beta0s=(0.0, 0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.8), margin=None, seed=0, steps=150):
    """Basin map: from each initial beta in a predictable world, climb alive or decay dead?"""
    if margin is None:
        margin = maintenance_margin(W, seed=seed)
    return [(b0, run_dynamics(W, b0, world="predict", steps=steps, margin=margin, seed=seed)[-1][0]) for b0 in beta0s]


def _show(tag, traj, every=20):
    pts = " ".join(f"{traj[i][0]:.2f}" for i in range(0, len(traj), every))
    print(f"  {tag:34s} beta: {pts}   (final reward {traj[-1][1]:.2f})")


if __name__ == "__main__":
    W, curve = r1_curve(0)
    print("=== R1: fetch quality vs sharpness beta (seed 0) -- fetch_R2 is the measure ===")
    print("  beta   fetch_R2   routing_acc [diagnostic only: argmax, beta-invariant for beta>0]")
    for b, r2, acc in curve:
        print(f"  {b:4.2f}   {r2:+.3f}     {acc:.3f}   " + "#" * int(max(0, r2) * 30))

    null = null_r2(W, seed=0)
    margin = maintenance_margin(W, seed=0)
    print(f"\nnull baseline (flat-attention fetch R^2) = {null:.3f}  ->  maintenance margin = null+eps = {margin:.3f}")
    print(f"irreversibility margin (R3, stricter)    = {IRREVERSIBILITY_MARGIN:.3f}  (null+eps straddles the knee -- not reliable for R3)")

    print(f"\n=== R2: self-maintenance (MAINTENANCE margin={margin:.2f} = null+eps; alive ~2.x, dead 0) ===")
    _show("(i)  MAINTAIN  predictable", run_dynamics(W, 2.8, world="predict"))
    _show("(ii) SELF-REPAIR knock 0.5 @80", run_dynamics(W, 2.8, world="predict", knock=(80, 0.5)))
    _show("(iii)DISSOLVE  scramble @half", run_dynamics(W, 2.8, world="switch"))
    _show("(iv) CONTROL   no reward (gain=0)", run_dynamics(W, 2.8, world="predict", gain=0.0))

    print("\n=== R3: irreversibility is MARGIN-CONDITIONED, not intrinsic (revive-world final beta, seed 0) ===")
    for label, m, fb in margin_sweep(W):
        verdict = "DEAD (irreversible)" if fb < 0.2 else "REVIVED (reversible -> NOT intrinsic)"
        print(f"  margin={label:14s} final beta={fb:.2f}   {verdict}")

    print("\n  null+eps is NOT a reliable irreversibility margin -- per seed (revive-world final beta):")
    for sd in range(3):
        Ws = train(sd)
        nem = maintenance_margin(Ws, seed=sd)
        fb = run_dynamics(Ws, 2.8, world="revive", steps=240, margin=nem, seed=sd)[-1][0]
        print(f"    seed {sd}: null+eps={nem:.2f}  final beta={fb:.2f}   {'REVIVED' if fb >= 0.2 else 'DEAD'}")
    print(f"  => margin>=~{IRREVERSIBILITY_MARGIN:.1f} kills all 3 seeds; null+eps straddles the knee (seed 2 dies, seeds 0,1 revive).")

    print("\n=== basin: initial beta in predictable world (maintenance margin=null+eps) ===")
    for b0, fb in initial_beta_sweep(W):
        print(f"  beta0={b0:.2f}  ->  final {fb:.2f}   ({'alive' if fb > 1.0 else 'dead'})")

    print("\n=== robustness across 3 seeds (maintain alive; scramble dead; maintenance margin=null+eps) ===")
    for sd in range(3):
        Ws = train(sd)
        m_ = maintenance_margin(Ws, seed=sd)
        mt = run_dynamics(Ws, 2.8, world="predict", margin=m_, seed=sd)[-1][0]
        dd = run_dynamics(Ws, 2.8, world="scramble", margin=m_, seed=sd)[-1][0]
        print(f"  seed {sd}: margin={m_:.2f}  maintain beta={mt:.2f}   scramble beta={dd:.2f}")
