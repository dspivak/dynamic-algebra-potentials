"""Property-based composition auditor for the KQV suboperad (codex audit follow-up).

The single-head maps are verified elsewhere (test_operad_laws.py A1).  Here we audit
the *composition*: over many random closed KQV trees, an INDEPENDENT recursive oracle
re-derives the root emission and the summed per-node potential -- propagating
emissions UP and routing descending contexts DOWN by hand, using each node's own
generator map -- and compares to ``realize`` (which builds the same thing via dap's
``compose_seq``/``tensor_arrangements``).  A routing, packing, or potential-summation
bug in the operadic substitution would show up as a mismatch on some random tree.

The oracle reuses each node's *own* head map (``attention_head``), which is the
audited atom; it does NOT use ``compose_seq`` -- the tree traversal is hand-written,
so it is genuinely independent of the composition path under test.

Run from the repo root:
    PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m pytest \
        sensemaking/kqv/test_property_composition.py -q
"""

import jax
jax.config.update("jax_enable_x64", True)  # exact comparisons need float64

import jax.numpy as jnp
import numpy as np

from sensemaking.kqv import Head, Sub, attention_head, leaf, param_dim, realize


def random_tree(rng, depth, E, d, d_v, p_leaf=0.35, max_arity=3):
    """A random closed KQV term: leaves are 0-ary prior boxes (ex.zeroary)."""
    if depth <= 0 or rng.random() < p_leaf:
        return leaf(E)
    N = int(rng.integers(1, max_arity + 1))
    kids = tuple(random_tree(rng, depth - 1, E, d, d_v, p_leaf, max_arity) for _ in range(N))
    return Sub(Head(N, E, d, d_v), kids)


def node_dim(node, E, d, d_v):
    """Dimension of a node's OWN head parameters (leaf prior = E; head = param_dim)."""
    if isinstance(node, Head):  # a leaf (N == 0)
        return E
    return param_dim(E, d, d_v)  # a Sub: its parent head's params


def layout(node):
    """Nodes in dap's direct-sum packing order: children subtrees first, then the node.

    Mirrors realize(Sub) = compose_seq(tensor(children), parent): Q = child_1 (+) ...
    (+) child_K (+) parent (wiring.compose_seq + tensor_arrangements).
    """
    if isinstance(node, Head):
        return [node]
    out = []
    for c in node.children:
        out += layout(c)
    out.append(node)  # the parent head's own params come last
    return out


def _parent_head(node, E, d, d_v):
    return attention_head(node.parent.N, E, d, d_v)


def forward(node, qmap, E, d, d_v):
    """Root-ward emission: leaves emit their prior; each Sub pools its children (eq.pool)."""
    if isinstance(node, Head):  # leaf prior box emits its constant q
        return qmap[id(node)]
    child_em = jnp.concatenate([forward(c, qmap, E, d, d_v) for c in node.children])
    return _parent_head(node, E, d, d_v).out_f(qmap[id(node)], child_em)


def potential_sum(node, ctx, qmap, E, d, d_v):
    """Total potential: each Sub adds its U at its routed context, then routes down (in_f)."""
    if isinstance(node, Head):  # leaf: U = 0
        return 0.0
    ph = _parent_head(node, E, d, d_v)
    child_em = jnp.concatenate([forward(c, qmap, E, d, d_v) for c in node.children])
    here = float(ph.U(qmap[id(node)], child_em, ctx))
    child_ctx = ph.in_f(qmap[id(node)], child_em, ctx).reshape(node.parent.N, E)
    return here + sum(
        potential_sum(c, child_ctx[i], qmap, E, d, d_v)
        for i, c in enumerate(node.children)
    )


def test_property_based_composition():
    rng = np.random.default_rng(20260625)
    E, d, d_v = 3, 2, 2
    for trial in range(20):
        depth = int(rng.integers(1, 4))
        N = int(rng.integers(1, 4))
        root = Sub(
            Head(N, E, d, d_v),
            tuple(random_tree(rng, depth, E, d, d_v) for _ in range(N)),
        )
        arr = realize(root)

        nodes = layout(root)
        dims = [node_dim(n, E, d, d_v) for n in nodes]
        assert arr.Q.dim == sum(dims)  # direct-sum packing has the expected size

        q = jnp.asarray(rng.standard_normal(arr.Q.dim)) * 0.3
        qmap, off = {}, 0
        for n, dm in zip(nodes, dims):
            qmap[id(n)] = q[off : off + dm]
            off += dm
        n_world = jnp.asarray(rng.standard_normal(E))

        # forward emission: independent oracle vs realize (eq.pool composed up the tree)
        assert jnp.allclose(
            forward(root, qmap, E, d, d_v),
            arr.out_f(q, jnp.zeros(0)),
            atol=1e-8,
        ), f"forward mismatch on trial {trial}"

        # summed potential: independent oracle vs realize (potentials add; in_f routes down)
        assert jnp.allclose(
            potential_sum(root, n_world, qmap, E, d, d_v),
            arr.U(q, jnp.zeros(0), n_world),
            atol=1e-8,
        ), f"potential mismatch on trial {trial}"
