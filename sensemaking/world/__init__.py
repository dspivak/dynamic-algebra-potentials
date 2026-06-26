"""The experiment's world: a Phiphase-compiled oscillator environment (Task 2).

* ``oscillator`` -- the world as ``Phiphase(SmoothArrangement)`` (slow season + M fast
  weather modes tethered to it); ``world_arrangement``, ``roll_world``, ``WorldRoll``.
* ``observe`` -- distributed partial observability (``partition_modes``, ``embed_views``).
* ``diagnose`` -- the necessary-communication gate (``decode_gate``).

This whole layer is the environment, OUTSIDE the KQV suboperad.
"""

from .diagnose import decode_gate
from .observe import embed_views, partition_modes
from .oscillator import WorldRoll, roll_world, world_arrangement

__all__ = [
    "world_arrangement",
    "roll_world",
    "WorldRoll",
    "partition_modes",
    "embed_views",
    "decode_gate",
]
