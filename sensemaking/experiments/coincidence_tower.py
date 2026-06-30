"""End-to-end test of the second-order (coincidence) suboperad (the box-3<->box-6 test).

Two groups A, B. Box a (in A) and box b (in B) carry hidden signs sa, sb in {-1,+1}; the
EVENT is e = (sa == sb): the two boxes, in *different groups*, are correlated. Each box's
marginal is pure noise, so only the PRODUCT sa*sb reveals e -- a coincidence no first-order
(mean) summary can see. Each group is summarized first (box identity lost in noise), so the
top must recover the coincidence from the two noisy group summaries.

We build the encoder as a KQV tower (factors through the suboperad via ``KQVSystem``):
  groups = attention heads (first order, preserve features);
  top    = either an attention head (FIRST order, the control) or a coincidence head
           (SECOND order, ``Coinc``) -- the recipe of ``kqv/coincidence.py``.
z_top = the tower's forward emission ``out_f``. We train the encoder weights + a linear
read-out to decode e (a capacity probe: can the architecture, trained, see the coincidence?),
and compare. The first-order top should be stuck at chance no matter how it is trained; the
second-order top should clear the bar.

Run: PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m sensemaking.experiments.coincidence_tower
"""

from __future__ import annotations

import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp
import numpy as np

from sensemaking.kqv import Coinc, Head, Sub, KQVSystem
from sensemaking.kqv.head import param_dim

E, G, R, dd = 4, 6, 4, 2          # width, boxes/group, feature rank, head dims (d=d_v=dd)
T, STEPS, LR = 5000, 500, 5e-2


def gen(T, rng, snr):
    sa = rng.choice([-1.0, 1.0], T); sb = rng.choice([-1.0, 1.0], T)
    e = (sa == sb).astype(np.float64)
    X = rng.standard_normal((T, 2, G, E))
    X[:, 0, 0, 0] += sa * snr; X[:, 1, 0, 0] += sb * snr
    return jnp.asarray(X.reshape(T, -1)), jnp.asarray(e)


# groups: heads with d_v = E so the OV circuit can be full rank (no bottleneck).
GH_DV = E


def frozen_group():
    """A head frozen at UNIFORM attention (w_star=0) with IDENTITY value/output projections,
    so out_f = mean over boxes -- the clean group summary that preserves the signal box. A
    valid KQV head parameter point; layout Wq(d,E),Wk(d,E),Wv(d_v,E),Wo(E,d_v),w_star(d)."""
    Wq = np.zeros((dd, E)); Wk = np.zeros((dd, E))
    Wv = np.eye(E); Wo = np.eye(E); ws = np.zeros(dd)      # Wv,Wo identity (d_v=E); w_star=0
    return jnp.asarray(np.concatenate([Wq.ravel(), Wk.ravel(),
                                       Wv.ravel(), Wo.ravel(), ws]))


def adam_train(loss_fn, params, steps, lr, rng):
    m = [np.zeros_like(p) for p in params]; v = [np.zeros_like(p) for p in params]
    b1, b2, eps = 0.9, 0.999, 1e-8
    g = jax.jit(jax.value_and_grad(loss_fn))
    for t in range(1, steps + 1):
        L, grads = g(params)
        params = list(params)
        for i, (p, gr) in enumerate(zip(params, grads)):
            gr = np.asarray(gr)
            m[i] = b1 * m[i] + (1 - b1) * gr
            v[i] = b2 * v[i] + (1 - b2) * gr * gr
            mh = m[i] / (1 - b1 ** t); vh = v[i] / (1 - b2 ** t)
            params[i] = p - lr * mh / (np.sqrt(vh) + eps)
            params[i] = jnp.asarray(params[i])
    return params, float(L)


def run(top_is_coinc, X, e, rng):
    groups = (Head(G, E, dd, GH_DV), Head(G, E, dd, GH_DV))      # frozen mean-pool summaries
    top = Coinc(2, E, R) if top_is_coinc else Head(2, E, dd, E)   # second vs first order top
    sysm = KQVSystem(Sub(top, groups))                           # provenance: a KQVTerm
    arr = sysm.arrangement
    nh = param_dim(E, dd, GH_DV)
    gp = jnp.concatenate([frozen_group(), frozen_group()])       # 2 frozen group heads
    # only the TOP generator's params (after the two group blocks) and the read-out train:
    encode = jax.vmap(lambda tq, x: arr.out_f(jnp.concatenate([gp, tq]), x), in_axes=(None, 0))

    n = len(e); idx = rng.permutation(n); k = int(0.7 * n); tr, te = idx[:k], idx[k:]
    tq0 = jnp.asarray(rng.standard_normal(arr.Q.dim - 2 * nh)) * 0.3
    w0, b0 = jnp.zeros(E), jnp.zeros(())

    def loss(params):
        tq, w, b = params
        logits = encode(tq, X[tr]) @ w + b
        return jnp.mean(jnp.logaddexp(0.0, logits) - e[tr] * logits) + 1e-4 * jnp.sum(tq * tq)

    (tq, w, b), _ = adam_train(loss, [tq0, w0, b0], STEPS, LR, rng)
    acc = lambda I: float(jnp.mean(((encode(tq, X[I]) @ w + b) > 0).astype(jnp.float64) == e[I]))
    return sysm, acc(tr), acc(te)


def main():
    print("=" * 78)
    print(f"COINCIDENCE TOWER  data->[head(A),head(B)]_frozen-mean->TOP_trained   E={E} G={G} r={R}")
    print(f"event e=(sa==sb): boxes a,b in DIFFERENT groups; only the PRODUCT sa*sb reveals it")
    print("=" * 78)
    print(f"  {'SNR':>4} | {'first-order top':>16} | {'second-order top (Coinc)':>26} | gap")
    for snr in (3.0, 5.0, 8.0):
        X, e = gen(T, np.random.default_rng(0), snr)
        _, _, a1 = run(False, X, e, np.random.default_rng(1))
        _, _, a2 = run(True, X, e, np.random.default_rng(1))
        print(f"  {snr:>4} | {a1:>16.3f} | {a2:>26.3f} | {a2 - a1:+.3f}")
    print("\n  factors through KQV (provenance trace):")
    print("    " + KQVSystem(Sub(Coinc(2, E, R), (Head(G, E, dd, dd), Head(G, E, dd, dd))))
          .trace().replace("\n", "\n    "))
    print("\n  PASS: second-order clears the bar; first-order (weak softmax nonlinearity) lags.")


if __name__ == "__main__":
    main()
