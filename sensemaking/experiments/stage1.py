"""Stage 1: is the communication channel used? (Task 3)

Self-supervised next-observation prediction by N=48 short-memory sensor-boxes wired
into ONE KQV attention head (the experiment's box).  Each box predicts its next
observation as a residual plus the message it receives over the channel:

    pred_i(t) = o_i(t) + Delta_i,     Delta = arr.in_f(W, obs(t), 0)   (eq.attn, the CHANNEL)

The channel ``Delta`` is the audited KQV self-attention (``realize(KQVTerm).in_f`` --
provenance holds).  Learning is gradient descent of the total potential

    U_total(W) = mean_i || pred_i - o_i(t+1) ||^2  +  beta * mean ||Delta||^2

i.e. next-obs prediction error plus a capacity (rate) penalty.  With the Euclidean
sharp this descent IS Phiconf (eqn.learning_sharp); the gradient is exactly the one
dap's interpretation computes by functoriality of Phiconf, here taken with jax.grad.

Controls (explicitly NOT KQV -- they are alternative models):
* no-channel ablation: diagonal attention (each box uses only its own value; no
  cross-box mixing) -- "no communication".
* full-observability ceiling: each box is handed the global pool for free -- the best
  a box could do if it did not need to communicate.

PRE-REGISTERED (locked before any run):
  PASS = treatment next-obs R^2 > no-channel + 0.02  (mixing helps)
         AND treatment R^2 within reach of the full-obs ceiling
         AND I(Delta; s) > I(Delta_diag; s) + 0.05  (channel carries the season)
         AND rate > 0  (channel not collapsed),  across >= 5 seeds.
  FAIL = rate -> 0 (collapse), or treatment ~ no-channel (mixing useless),
         or I(Delta; s) ~ 0.
Numbers are reported raw either way; the world/gate are NOT retuned to make this pass.
"""

from __future__ import annotations

from functools import partial

import jax
jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp
import numpy as np

from sensemaking.kqv import Builder, KQVSystem, param_dim, unpack
from sensemaking.world import embed_views, standard_world
from sensemaking.world.diagnose import _decode_r2

E, D, DV, N = 8, 8, 8, 48  # residual width, head ranks, sensor count
_ARR = KQVSystem(Builder(E, D, DV).head(N)).arrangement  # the box (provenance: realize(KQVterm))


# ---- the three message models (Delta) ----

def msg_treatment(W, obs_t):
    """The KQV self-attention channel (eq.attn) -- this is the audited suboperad map."""
    return _ARR.in_f(W, obs_t, jnp.zeros(E))


def msg_diag(W, obs_t):
    """No-channel ablation: diagonal attention -- each box sees only its own value."""
    P = unpack(W, E, D, DV)
    omega = P["Wo"] @ P["Wv"]  # (E, E) OV circuit
    h = obs_t.reshape(N, E)
    return (h @ omega.T).reshape(N * E)


def msg_full(W, obs_t):
    """Full-observability ceiling: each box is handed the global pool for free."""
    P = unpack(W, E, D, DV)
    omega = P["Wo"] @ P["Wv"]
    gmean = obs_t.reshape(N, E).mean(0)  # the pool, handed to every box
    return jnp.broadcast_to(omega @ gmean, (N, E)).reshape(N * E)


def _loss(W, obs_t, target, beta, msg_fn):
    delta = msg_fn(W, obs_t)  # the pooled estimate IS the prediction (no residual)
    return jnp.mean((delta - target) ** 2) + beta * jnp.mean(delta ** 2)


# ---- the world stream ----

def _consensus(x):
    """Broadcast the per-time pooled observation: (T, N*E) -> (T, N*E) of the box-mean.

    The pooled next-observation is noise-robust (independent sensor noise averages
    over N=48) and ~ the season, and a single box cannot compute it -- so predicting
    it genuinely requires the channel.  (Predicting each sensor's RAW next obs is
    capped by that sensor's own irreducible noise.)
    """
    T = x.shape[0]
    xm = x.reshape(T, N, E).mean(1)  # (T, E) the pool
    return jnp.broadcast_to(xm[:, None, :], (T, N, E)).reshape(T, N * E)


def build_stream(seed, T=2400, embed_seed=777):
    roll, views = standard_world(seed, T=T)
    emb = embed_views(views, E, seed=embed_seed)  # list of N arrays (T, E)
    obs = jnp.asarray(np.concatenate([emb[i] for i in range(N)], axis=1))  # (T, N*E)
    # target = the POOLED next observation (self-supervised, noise-robust, pooling-required)
    return obs[:-1], _consensus(obs[1:]), np.asarray(roll.s)[:-1]


# ---- training (Phiconf = Euclidean-sharp gradient descent) ----

def train(msg_fn, obs_t, target, beta, *, eta=0.005, epochs=15, seed=0):
    rng = np.random.default_rng(1000 + seed)
    W = jnp.asarray(rng.standard_normal(param_dim(E, D, DV))) * 0.1

    @jax.jit
    def epoch(W):
        def step(W, batch):
            ot, tg = batch
            g = jax.grad(_loss)(W, ot, tg, beta, msg_fn)
            g = jnp.clip(g, -1.0, 1.0)  # mild gradient clip for symplectic-free stability
            return W - eta * g, None
        W, _ = jax.lax.scan(step, W, (obs_t, target))
        return W

    for _ in range(epochs):
        W = epoch(W)
    return W


def metrics(W, msg_fn, obs_ev, target_ev, s_ev):
    """Evaluate on a HELD-OUT split (obs_ev/target_ev/s_ev never seen in training)."""
    delta = jax.vmap(lambda x: msg_fn(W, x))(obs_ev)  # (n, N*E) the prediction = channel output
    ss_res = float(jnp.mean((delta - target_ev) ** 2))
    ss_tot = float(jnp.mean((target_ev - target_ev.mean(0)) ** 2))
    r2 = 1.0 - ss_res / ss_tot
    rate = float(jnp.mean(delta ** 2))
    # I(delta_i; s): does a SINGLE box's received message carry the season? (median box)
    dr = np.asarray(delta).reshape(delta.shape[0], N, E)
    per_box = sorted(_decode_r2(dr[:, i, :], s_ev, window=1) for i in range(N))
    return {"pooled_pred_r2": r2, "rate": rate, "I_delta_s": float(per_box[N // 2])}


def run(seed, beta, train_frac=0.6):
    obs_t, target, s = build_stream(seed)
    a = int(obs_t.shape[0] * train_frac)  # train on [:a], evaluate strictly on [a:]
    out = {}
    for name, fn in (("treatment", msg_treatment), ("no_channel", msg_diag), ("full_obs", msg_full)):
        W = train(fn, obs_t[:a], target[:a], beta, seed=seed)
        out[name] = metrics(W, fn, obs_t[a:], target[a:], s[a:])
    return out


def summary(beta, seeds=range(5)):
    rows = {"treatment": [], "no_channel": [], "full_obs": []}
    for seed in seeds:
        r = run(seed, beta)
        for k in rows:
            rows[k].append(r[k])
    print(f"\n=== beta={beta}, {len(list(seeds))} seeds (mean [min,max]) ===")
    for name, ms in rows.items():
        def stat(key):
            v = [m[key] for m in ms]
            return f"{np.mean(v):+.3f} [{min(v):+.3f},{max(v):+.3f}]"
        print(f"  {name:10s}  pooled_pred_R2={stat('pooled_pred_r2')}  "
              f"rate={np.mean([m['rate'] for m in ms]):.4f}  I(delta_i;s)={stat('I_delta_s')}")
    return rows


if __name__ == "__main__":
    for beta in (0.0, 0.02):
        summary(beta)
