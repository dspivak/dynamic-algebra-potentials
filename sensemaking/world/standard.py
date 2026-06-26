"""The locked Stage-1 world configuration (Task 2).

A single place for the world parameters tuned to pass the necessary-communication
gate, so Task 3 (the experiment) and the tests use exactly the same environment.

Tuned regime (robust across weather seeds, strong every-box gate): even the *best*
single box decodes the season at R^2 <= 0.42 (no single sensor can track it), while
pooling all N=48 sensors gives R^2 ~ 0.76 and beats every single box by >= 0.34.
This is a high-noise distributed-sensing regime: many 1-mode sensors, each too noisy
alone, that together recover the season.
"""

from __future__ import annotations

from typing import List, Tuple

import numpy as np

from .observe import sense
from .oscillator import WorldRoll, roll_world

# The world (Phiphase oscillator) and sensing parameters.
WORLD = dict(M=48, c=2.0, m_s=2500.0, k_s=1.0, season_amp=0.5, fast_ic_scale=1.0)
SENSE = dict(N=48, noise=4.0)  # one mode per sensor, high independent sensor noise
GATE_WINDOW = 10


def standard_world(seed: int, *, T: int = 2000) -> Tuple[WorldRoll, List[np.ndarray]]:
    """Roll the locked Stage-1 world and produce the ``N`` noisy per-box observations.

    Returns ``(roll, sensed_views)`` where ``roll.s`` is the hidden season (ground
    truth, for diagnostics) and ``sensed_views`` is a list of ``N`` arrays ``(T, k_i)``
    -- the noisy mode-slices each box senses.  Weather (fast modes) and sensor noise
    are seeded from ``seed``; the season cycle is fixed.
    """
    roll = roll_world(WORLD["M"], T=T, seed=seed, c=WORLD["c"], m_s=WORLD["m_s"],
                      k_s=WORLD["k_s"], season_amp=WORLD["season_amp"],
                      fast_ic_scale=WORLD["fast_ic_scale"])
    views = sense(roll.obs, SENSE["N"], noise=SENSE["noise"], seed=10_000 + seed)
    return roll, views
