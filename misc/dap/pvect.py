"""Paired vector spaces (def.pnla).

A paired vector space is a finite-dimensional real vector space ``V``
together with a linear isomorphism ``sharp_V: V^* -> V`` (def.pnla).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import jax.numpy as jnp
from jax import Array


@dataclass(frozen=True)
class PairedVectorSpace:
    """A paired vector space ``(V, sharp_V)`` per def.pnla."""

    V_dim: int
    sharp: Array  # ``sharp_V: V^* -> V``, encoded as a (V_dim, V_dim) matrix.

    @property
    def flat(self) -> Array:
        """The flat map ``flat_V := sharp_V^{-1}: V -> V^*``."""
        return jnp.linalg.inv(self.sharp)

    def pairing(self, v: Array, vp: Array) -> Array:
        """The nondegenerate pairing ``<v, vp> := flat(v) . vp``."""
        return jnp.dot(self.flat @ v, vp)

    def apply_sharp(self, xi: Array) -> Array:
        """Apply ``sharp_V`` to a covector ``xi in V^*``."""
        return self.sharp @ xi

    def direct_sum(self, other: "PairedVectorSpace") -> "PairedVectorSpace":
        """Monoidal product on pvect: block-diagonal sharp."""
        n, m = self.V_dim, other.V_dim
        S = jnp.zeros((n + m, n + m))
        S = S.at[:n, :n].set(self.sharp)
        S = S.at[n:, n:].set(other.sharp)
        return PairedVectorSpace(V_dim=n + m, sharp=S)


def trivial_pvect() -> PairedVectorSpace:
    """The monoidal unit of pvect: the zero vector space."""
    return PairedVectorSpace(V_dim=0, sharp=jnp.zeros((0, 0)))


# Convenience constructor used throughout the wave-equation example.
def diagonal_pvect(diag: Array) -> PairedVectorSpace:
    """A paired vector space whose sharp is diagonal with the given entries."""
    diag = jnp.asarray(diag)
    return PairedVectorSpace(V_dim=int(diag.shape[0]), sharp=jnp.diag(diag))


SmoothMap = Callable[..., Array]
