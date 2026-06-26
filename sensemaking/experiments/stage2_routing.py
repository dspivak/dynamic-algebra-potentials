"""Stage 2: does ADDRESSED routing emerge? (the atom of language)

Stage 1 showed the channel learns to *pool* (average) when the task is "estimate one
shared latent" -- structureless communication.  Here the task *requires routing*, and
we ask whether the emergent communication is correspondingly *addressed*.

The task (content-addressed fetch), random every episode so nothing can be memorized:
N boxes; box j holds a random identity ``id_j`` (a key) and a random ``value_j`` (a
payload).  Each box i is given a query ``id_{t_i}`` -- the address of the box it must
fetch from, for a random matching ``t`` (a derangement, so ``t_i != i``).  Box i must
output ``value_{t_i}``.  Its emission packs ``h_i = [id_i, value_i, query_i]``, so the
KQV head's QK circuit can match query->key (the ADDRESS) and the OV circuit can copy
the value (the PAYLOAD).  Averaging is useless; the only solution is to send the right
payload to the right address.

Channel = the audited KQV self-attention ``realize(KQVTerm).in_f`` (provenance holds).
Controls (non-KQV baselines): no-channel (diagonal -- a box sees only its own value)
and shuffled-query (the address is randomized at eval -- if the model ignores the
address its score is unchanged; if it uses it, the score collapses).

PRE-REGISTERED (locked before any run):
  PASS = treatment fetch-R^2 > 0.8  AND  routing accuracy (argmax attention == t_i) > 0.9
         AND no-channel fetch-R^2 < 0.2  AND  shuffled-query fetch-R^2 < 0.2,
         across >= 5 seeds, on held-out episodes (fresh ids/values/matching).
  INTERPRETABILITY (the point): the learned attention matrix == the matching t.
Numbers reported raw either way.
"""

from __future__ import annotations

import jax
jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp
import numpy as np

from sensemaking.kqv import Builder, KQVSystem, param_dim, unpack

N, D_ID, E_VAL = 6, 12, 8        # boxes; identity dim (address); value dim (payload)
E = 2 * D_ID + E_VAL             # residual = [id | value | query]
D, DV = 16, 16                   # head ranks
VAL = slice(D_ID, D_ID + E_VAL)  # where the value lives in the residual
_ARR = KQVSystem(Builder(E, D, DV).head(N)).arrangement  # provenance: realize(KQVterm)


# ---- episodes ----------------------------------------------------------------

def _derangement(rng, n):
    while True:
        p = rng.permutation(n)
        if np.all(p != np.arange(n)):
            return p


def gen_episodes(n_ep, rng):
    """Returns h (n_ep, N, E), target (n_ep, N, E_VAL), t (n_ep, N)."""
    H, T, TT = [], [], []
    for _ in range(n_ep):
        ids = rng.standard_normal((N, D_ID)) / np.sqrt(D_ID)
        vals = rng.standard_normal((N, E_VAL))
        t = _derangement(rng, N)
        h = np.concatenate([ids, vals, ids[t]], axis=1)  # [id_i, value_i, query=id_{t_i}]
        H.append(h)
        T.append(vals[t])  # box i must output value_{t_i}
        TT.append(t)
    return jnp.asarray(np.stack(H)), jnp.asarray(np.stack(T)), np.stack(TT)


# ---- the channel (treatment) and controls -----------------------------------

def msg_treatment(W, h_flat):
    return _ARR.in_f(W, h_flat, jnp.zeros(E))  # audited KQV self-attention


def msg_diag(W, h_flat):  # no-channel: each box sees only its own value (OV circuit)
    P = unpack(W, E, D, DV)
    omega = P["Wo"] @ P["Wv"]
    return (h_flat.reshape(N, E) @ omega.T).reshape(N * E)


def _fetch(W, h, msg_fn):
    delta = msg_fn(W, h.reshape(-1)).reshape(N, E)
    return delta[:, VAL]  # the fetched payload per box


def _loss(W, h_batch, tgt_batch, msg_fn):
    out = jax.vmap(lambda h: _fetch(W, h, msg_fn))(h_batch)
    return jnp.mean((out - tgt_batch) ** 2)


def train(msg_fn, h, tgt, *, lr=3e-3, steps=2500, seed=0):
    """Adam = a diagonal state-dependent reactive sharp (rmk.optimizer); faithful, and it
    reliably escapes the uniform-attention saddle that plain GD gets stuck at."""
    W0 = jnp.asarray(np.random.default_rng(1000 + seed).standard_normal(param_dim(E, D, DV))) * 0.1
    b1, b2, eps = 0.9, 0.999, 1e-8

    def step(carry, _):
        W, m, v, i = carry
        g = jax.grad(_loss)(W, h, tgt, msg_fn)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        i = i + 1.0
        W = W - lr * (m / (1 - b1 ** i)) / (jnp.sqrt(v / (1 - b2 ** i)) + eps)
        return (W, m, v, i), None

    z = jnp.zeros_like(W0)
    (W, *_), _ = jax.lax.scan(step, (W0, z, z, 0.0), None, length=steps)
    return W


# ---- metrics + interpretability ---------------------------------------------

def attn_matrix(W, h):
    """Recompute the KQV attention A (over the N boxes) for inspection == the routing graph."""
    P = unpack(W, E, D, DV)
    hr = h.reshape(N, E)
    scores = (hr @ P["Wq"].T) @ (hr @ P["Wk"].T).T / jnp.sqrt(D)
    return jax.nn.softmax(scores, axis=1)  # (N, N): row i = where box i reads from


def metrics(W, msg_fn, h_ev, tgt_ev, t_ev):
    out = jax.vmap(lambda h: _fetch(W, h, msg_fn))(h_ev)
    r2 = float(1.0 - jnp.mean((out - tgt_ev) ** 2) / jnp.mean((tgt_ev - tgt_ev.mean()) ** 2))
    A = jax.vmap(lambda h: attn_matrix(W, h))(h_ev)  # (n_ev, N, N)
    routing_acc = float(jnp.mean(jnp.argmax(A, axis=2) == jnp.asarray(t_ev)))
    return {"fetch_r2": r2, "routing_acc": routing_acc}


def run(seed):
    rng = np.random.default_rng(seed)
    h_tr, t_tr, _ = gen_episodes(400, rng)
    h_ev, tgt_ev, tt_ev = gen_episodes(200, rng)  # held-out: fresh ids/values/matchings
    out = {}

    W = train(msg_treatment, h_tr, t_tr, seed=seed)
    out["treatment"] = metrics(W, msg_treatment, h_ev, tgt_ev, tt_ev)
    # shuffled-query control: randomize the address block at eval; if it uses addresses, this collapses
    hq = np.asarray(h_ev).copy()
    hq[:, :, D_ID + E_VAL:] = np.asarray(gen_episodes(h_ev.shape[0], rng)[0])[:, :, D_ID + E_VAL:]
    out["shuffled_query"] = metrics(W, msg_treatment, jnp.asarray(hq), tgt_ev, tt_ev)

    Wd = train(msg_diag, h_tr, t_tr, seed=seed)
    out["no_channel"] = metrics(Wd, msg_diag, h_ev, tgt_ev, tt_ev)
    out["_sampleA"] = np.asarray(attn_matrix(W, h_ev[0]))
    out["_t0"] = tt_ev[0]
    return out


if __name__ == "__main__":
    rows = {"treatment": [], "shuffled_query": [], "no_channel": []}
    sample = None
    for seed in range(5):
        r = run(seed)
        for k in rows:
            rows[k].append(r[k])
        if sample is None:
            sample = (r["_sampleA"], r["_t0"])
    print("=== Stage 2: addressed routing (5 seeds, mean [min,max]) ===")
    for name, ms in rows.items():
        def st(key):
            v = [m[key] for m in ms]
            return f"{np.mean(v):.3f} [{min(v):.3f},{max(v):.3f}]"
        print(f"  {name:14s}  fetch_R2={st('fetch_r2')}   routing_acc={st('routing_acc')}")
    A, t0 = sample
    print(f"\nlearned attention (seed 0, episode 0) -- row i should peak at t_i={list(t0)}:")
    for i, row in enumerate(A):
        print(f"  box {i} -> " + " ".join(f"{x:.2f}" for x in row) + f"   argmax={int(np.argmax(row))} (t={t0[i]})")
