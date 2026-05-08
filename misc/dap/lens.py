"""Potentialized lens maps in ``potlens = Para(pvect, lmfd^R)`` (def.potlens).

A morphism ``f: V . <M_in / M_out> -> <N_in / N_out>`` in potlens is a
tuple ``(V, sharp_V, out_f, in_f, U)`` per eqn.para_potential_lens_maps:

    out_f : V x M_out          -> N_out
    in_f  : V x M_out x N_in   -> M_in
    U     : V x M_out x N_in   -> R

In the running wave-equation example the manifolds are all ``R^d``;
that is the only case Stage 2 covers (VOCAB design (5)).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from jax import Array

from .pvect import PairedVectorSpace


SmoothMap = Callable[..., Array]


@dataclass(frozen=True)
class PotLensMap:
    """A potentialized lens map (def.potlens, eqn.para_potential_lens_maps).

    Source has output dimension ``out_dim_M`` and input dimension
    ``in_dim_M``; target has ``out_dim_N`` and ``in_dim_N``. The
    parameter is the paired vector space ``V``.
    """

    V: PairedVectorSpace
    out_dim_M: int
    in_dim_M: int
    out_dim_N: int
    in_dim_N: int
    out_f: SmoothMap  # (v, m_out)              -> n_out
    in_f: SmoothMap   # (v, m_out, n_in)        -> m_in
    U: SmoothMap      # (v, m_out, n_in)        -> R
    label: str = ""

    @property
    def sharp_V(self) -> Array:
        return self.V.sharp
