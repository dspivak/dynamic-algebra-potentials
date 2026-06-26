"""Regression test of the Stage-1 result: the communication channel is used (Task 3).

Pre-registered headline: with the KQV attention channel the boxes predict the pooled
consensus ~ as well as the full-observability ceiling, while the no-channel ablation
(diagonal attention, no cross-box mixing) cannot.  2 seeds for test speed; the
reported result is over 5 (run `python -m sensemaking.experiments.stage1`).

Run: PYTHONPATH=$(pwd) misc/dap/.venv/bin/python -m pytest sensemaking/experiments/test_stage1.py -q
"""

from sensemaking.experiments.stage1 import run


def test_channel_is_used_and_necessary():
    for seed in (0, 1):
        r = run(seed, beta=0.0)
        t, nc, fo = r["treatment"], r["no_channel"], r["full_obs"]
        assert t["pooled_pred_r2"] > nc["pooled_pred_r2"] + 0.02  # channel helps the prediction
        assert t["pooled_pred_r2"] > 0.7 * fo["pooled_pred_r2"]  # ~ recovers the full-obs ceiling
        assert t["rate"] > 10 * nc["rate"]  # channel is used, not collapsed to silence
        assert t["I_delta_s"] > nc["I_delta_s"] + 0.05  # a box's received message carries the season
