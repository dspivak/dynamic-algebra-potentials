# Codex brief — audit the activation cell + bet on the residual hierarchy

You are the **external, adversarial auditor** for the sense-making / KQV experiment. Default to
skepticism; audit **code and frozen specs only**, reproduce checks where you can. Two jobs this
round: (1) **audit** what was built; (2) **bet** on what is proposed.

## Read (frozen targets)
- `sensemaking/attention-suboperad/attention-suboperad.tex` — the paper-faithful head (`eq.attn`,
  `eq.pool`, `eq.Uattn`, `con.head`, `rmk.moore`, `rmk.circuits`, `obs.residual`).
- `sensemaking/kqv/SPEC.md` — Generator 3 (built), **Findings**, **Generator 4** (proposed).
- `sensemaking/AUDIT.md` — the charter: **A** (head), **A′** (Generator 3), **F** (verify findings),
  **A″** (Generator 4 design), **Bet**.
- `sensemaking/PLAN.md` — Phase R context.

## Code under audit
- `sensemaking/kqv/head.py` (head), `cell.py` (Generator 3), `operad.py` (`Act` + generalized
  `Sub` + `realize`/`trace`), `builders.py`.
- `sensemaking/experiments/activation_tower.py` (the experiment + metrics).
- `dap-core/dap/` (the framework: `arrangement.py`, `rvect.py`, `interpretation.py`,
  `integrator.py`, `functors.py`).

## Run it yourself
```
cd <repo root>
PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m pytest sensemaking/kqv -q
PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m pytest sensemaking/experiments/test_activation_tower.py -q
PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m sensemaking.experiments.activation_tower   # ~5 min, no jit
```

## Audit tasks
1. **A′ (Generator 3, G1–G5)** against `kqv/cell.py` + `kqv/operad.py`. Re-run the law tests.
   The bar: it must factor through `sarr` (R-vect carrier, block sharp = data of `Q`, no new
   operad op; `out_f=Dz` Moore; `U=½‖h−Dz‖²`).
2. **F (verify the findings)** — reproduce the broadcast ceiling (`pred = Wo@(Wv@n)` is one
   `R^E` vector), the ~⅓ ≈ predict-the-mean baseline, and the near-zero-collapse / `z_top→μ0`
   prior result. These are the implementer's *negative* results; confirm or refute.
3. **A″ (Generator 4, the residual head — DESIGN only, not built)** — judge whether the
   compressed-residual-up design *could* be a faithful generator. The load-bearing check is
   **H2 (Moore)**: `out_f` may use `(q,h)` but not the descending `n`, so the subtracted
   prediction must be the box's own state, not the top-down `Ω·n`.

## The bet (pre-register a number before any Generator-4 build)
Probability in [0,1], with reasoning and the single most likely failure mode, for the claim in
`AUDIT.md` **Bet**: that under `Phiconf` the residual hierarchy will *discover* multi-scale
residual-compressors so a distant correlated pair (box 3 / box 6, different medium boxes, same
grandparent) is predicted better *because* its residual climbed the tree — staying a faithful
suboperad. The prior in-house bet (near-zero activation inference, ~40%) **lost**; calibrate.

## Output
Per check: `PASS / FAIL / UNCLEAR` with `file:line` evidence and any command + result. Then:
(1) **most likely way this is fooling itself**; (2) **verdict** — does Generator 3 factor through
the KQV suboperad, yes/no; (3) **your bet** — the number, the failure mode, and the one change
that would most raise your confidence.
