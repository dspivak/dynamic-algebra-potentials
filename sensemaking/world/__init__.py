"""The experiment's world: a Phiphase-compiled oscillator environment (Task 2).

* ``oscillator`` -- the world as ``Phiphase(SmoothArrangement)`` (slow season + M fast
  weather modes tethered to it); ``world_arrangement``, ``roll_world``, ``WorldRoll``.
* ``observe`` -- distributed partial observability + sensor noise (``partition_modes``,
  ``sense``, ``embed_views``).
* ``diagnose`` -- the necessary-communication gate (``decode_gate``).
* ``standard`` -- the locked Stage-1 configuration (``standard_world``, ``WORLD``, ...).
* ``couple`` -- stream the world into an open ``KQVSystem`` (``run_in_world``).

This whole layer is the environment, OUTSIDE the KQV suboperad.
"""

from .couple import run_in_world
from .diagnose import decode_gate
from .observe import embed_views, partition_modes, sense
from .oscillator import WorldRoll, roll_world, world_arrangement
from .standard import GATE_WINDOW, SENSE, WORLD, standard_world

__all__ = [
    "world_arrangement",
    "roll_world",
    "WorldRoll",
    "partition_modes",
    "sense",
    "embed_views",
    "decode_gate",
    "standard_world",
    "WORLD",
    "SENSE",
    "GATE_WINDOW",
    "run_in_world",
]
