"""Ergonomic builders for nested KQV systems (Task 1).

Every *term* builder (``leaf``/``head``/``node``/``nest``/``par``) returns a
``KQVTerm``, and ``system`` wraps one as a ``KQVSystem``; so provenance holds --
anything built here is ``realize``-able and ``KQVSystem``-wrappable, and its generator
tree is exposable via ``trace`` / ``KQVSystem.trace()``.  A ``Builder`` fixes ``E`` and
the internal ranks ``d, d_v`` so every head composes (uniform ``R^E`` interface,
``obs.residual``).

The headline builder is

    Builder(E, d, d_v).nest([N, N', N'', ...])

a *balanced* tree whose branching factors at successive levels are ``N, N', N'', ...``
(the "``N`` boxes, ``N'`` inside each, ``N''`` inside each of those, ... to any depth"
of the design).  The empty tail bottoms out in 0-ary prior leaves (``ex.zeroary``);
``nest([N])`` is the flat ``N``-box system (the ``N' = 0`` case).  ``node`` and ``par``
build ragged trees and width (lens-tensor / multi-head) respectively.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .operad import Head, KQVSystem, KQVTerm, Par, Sub, leaf


@dataclass(frozen=True)
class Builder:
    """Fixes ``(E, d, d_v)`` so every head built here shares the residual interface."""

    E: int
    d: int = 1
    d_v: int = 1

    def leaf(self) -> Head:
        """A 0-ary prior leaf (``ex.zeroary``)."""
        return leaf(self.E)

    def head(self, N: int) -> Head:
        """A bare arity-``N`` head generator (open at the bottom)."""
        return Head(N, self.E, self.d, self.d_v)

    def node(self, *children: KQVTerm) -> Sub:
        """A head substituted over the given child terms (ragged nesting)."""
        return Sub(self.head(len(children)), tuple(children))

    def nest(self, arities: Sequence[int]) -> KQVTerm:
        """A balanced closed tree with branching factors ``arities`` from the root down.

        ``nest([])`` is a leaf; ``nest([N])`` is the flat ``N``-box system; each extra
        entry adds a nesting level.  Every arity must be ``>= 1`` (use a shorter list
        for fewer levels rather than a ``0``).
        """
        if len(arities) == 0:
            return self.leaf()
        N, rest = arities[0], list(arities[1:])
        if N < 1:
            raise ValueError("each arity must be >= 1 (use a shorter list for fewer levels)")
        return self.node(*[self.nest(rest) for _ in range(N)])

    def par(self, *parts: KQVTerm) -> Par:
        """The lens tensor (width / multi-head) of independent subsystems."""
        return Par(tuple(parts))

    def system(self, term: KQVTerm) -> KQVSystem:
        """Wrap a term as an experiment-ready, provenance-carrying ``KQVSystem``."""
        return KQVSystem(term)
