"""Test ``PairedVectorSpace`` (def.pnla)."""

import jax.numpy as jnp
import numpy as np

from dap.pvect import PairedVectorSpace, diagonal_pvect, trivial_pvect


def test_sharp_flat_inverse():
    V = diagonal_pvect(jnp.array([0.5, 2.0, 1.0]))
    flat = V.flat
    sharp = V.sharp
    np.testing.assert_allclose(sharp @ flat, jnp.eye(3), atol=1e-10)
    np.testing.assert_allclose(flat @ sharp, jnp.eye(3), atol=1e-10)


def test_pairing_nondegenerate():
    V = diagonal_pvect(jnp.array([3.0, 0.5]))
    v = jnp.array([1.0, -2.0])
    vp = jnp.array([4.0, 0.5])
    # <v, vp> = flat(v) . vp = (v1/3)*vp1 + (v2/0.5)*vp2 = 1/3*4 + (-4)*0.5
    expected = (1.0 / 3.0) * 4.0 + (-2.0 / 0.5) * 0.5
    np.testing.assert_allclose(V.pairing(v, vp), expected, atol=1e-10)


def test_direct_sum_block_diagonal():
    V = diagonal_pvect(jnp.array([2.0]))
    W = diagonal_pvect(jnp.array([5.0, 7.0]))
    VW = V.direct_sum(W)
    assert VW.V_dim == 3
    expected = jnp.diag(jnp.array([2.0, 5.0, 7.0]))
    np.testing.assert_allclose(VW.sharp, expected, atol=1e-10)


def test_trivial_pvect():
    V0 = trivial_pvect()
    assert V0.V_dim == 0
