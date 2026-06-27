# sensemaking

Speculative companion work to the manuscript *Dynamic algebra of potentials* (DAP):
an experiment testing whether **addressed, discrete, reusable communication — "a
language", or "a sense" — emerges** as the low-rate, stable structure of nested
predictive arrangements under a capacity bound, entirely inside the DAP formalism.

Everything here factors through the **KQV attention suboperad of `sarr`**
([`kqv/SPEC.md`](kqv/SPEC.md)), which is faithful to
[`attention-suboperad/attention-suboperad.tex`](attention-suboperad/attention-suboperad.tex).

## Relationship to `dap`

This package depends on the executable DAP core, vendored as a git submodule at
[`../dap-core`](../dap-core) — the public repository
**<https://github.com/dspivak/dap>**. This `sensemaking/` code is deliberately kept
*outside* that submodule: it is exploratory and should not couple the public `dap`
repo to speculative work.

## Governance (read these first)

- [`PLAN.md`](PLAN.md) — the staged plan and the anti-Goodhart stance.
- [`AUDIT.md`](AUDIT.md) — the adversarial auditor charter (run before every
  milestone; an independent external audit is the real gate).
- [`kqv/SPEC.md`](kqv/SPEC.md) — the KQV suboperad that all work factors through.

## Running

The `dap` submodule ships a virtualenv with `jax`, `numpy`, `pytest`, and `dap`
installed editable. Run from the **repo root** with this package on `PYTHONPATH`:

```sh
PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m pytest sensemaking/kqv/test_operad_laws.py -q
```

(Equivalently, make your own venv with `jax>=0.4 numpy pytest` and
`pip install -e dap-core`, then `PYTHONPATH=$(pwd) python -m pytest sensemaking`.)

## Layout

```
sensemaking/
  PLAN.md, AUDIT.md           governance
  attention-suboperad/        the standalone companion note (the spec this code realizes)
  kqv/                        the KQV attention suboperad (Tasks 0-1)
    SPEC.md                   the math spec, faithful to attention-suboperad/attention-suboperad.tex
    head.py                   the head + prior-box generators (con.head, ex.zeroary)
    operad.py                 KQVTerm algebra (Head/Sub/Par) + F = realize + KQVSystem
    builders.py               Builder(E,d,d_v).nest([N,N',...]) and ragged/width builders
    test_operad_laws.py       operad-law + faithfulness tests
    test_property_composition.py  random-tree composition auditor
    test_nesting.py           nesting / lens-tensor / generalization tests
  world/                      partial-observability drive            (Task 2, TBD)
  experiments/                the sense-making climb                 (Task 3+, TBD)
```

## Status

- Task 0 (the KQV suboperad) — **complete; audited by both in-house and external
  (codex)**, both verdicts "factors through the KQV suboperad as specified."
- Task 1 (arbitrary-depth nesting API: `Builder.nest([N, N', ...])`, ragged trees,
  the `Par` lens tensor; provenance via `KQVSystem`) — **complete; in-house +
  external (codex) audited**. Codex round 1 found three real issues (a missing
  `trace(Par)` provenance branch, a non-total `Head` admitting negative arity, and a
  docstring overclaim) — all fixed; the term algebra is now total (validated at
  construction). **Codex re-audit: passed** ("Yes for Task 1 as scoped"); two minor
  follow-ups (`KQVSystem` validates its term at construction; module docstring
  includes `Par`) also addressed.
- Task 2 (the partial-observability world: `world/`) — **complete; in-house audited**.
  The locked world is the *periodic* oscillator `Phiphase(world_arrangement)` (slow season
  + 48 fast weather modes), proven genuinely phase-flow (matched to 2e-14 vs an independent
  symplectic integrator), outside the suboperad. The **strong** necessary-communication gate
  holds across 8 weather seeds: no single sensor decodes the season (best R^2 <= 0.42), the
  pool does (>= 0.71). The audit caught an earlier gate relaxation; fixed by retuning the
  world to pass the strong every-box bar (not by loosening the threshold). This is the world
  the experiments below run on.
- Task 2, decoder-window-robust variant (`world/chaotic.py`, a *standalone probe* — imported
  by no experiment) — **explored; does NOT pass its strong gate. Kept as a finding, not routed
  around.** The intent was an aperiodic (chaotic phi^4-chain) season so even a *long-window*
  single decoder cannot extrapolate it. As committed it fails (best single R^2 ~ 0.79, and
  *climbing* with window). Diagnosis: (i) the tether `c*s` (c=2) is ~2.6x the confounder, (ii)
  the ring coupling that makes the season chaotic also leaks it into the confounder coordinates
  (nearest-neighbour corr 0.88), and (iii) what suppression remains is sensor-noise-driven,
  hence window-*fragile*. A decoupled per-mode confounder restores window-robustness for the
  *typical* (median) sensor, but the *strong every-box* bar (best of 48 < 0.45) is an
  extreme-value statistic the centred-confounder mechanism can meet only fragilely (it needs a
  3x+ confounder, which over-confounds the median and erodes pool recovery). Open decision:
  reclassify this variant's gate to the median sensor (an honestly weaker claim) or record it
  as a negative result. The periodic Task-2 world above is unaffected.
- Task 3 (the sense-making climb, `experiments/`) — **Stages 1–3 implemented; in-house
  audited.** Stage 1 (`stage1.py`): under a capacity bound the channel is *used* — it learns to
  **pool** (structureless averaging) when the task is "estimate one shared latent." Stage 2
  (`stage2_routing.py`): when the task *requires* routing (content-addressed fetch), the
  emergent communication is correspondingly **addressed** — the KQV QK-circuit recovers the
  hidden matching and averaging fails. Stage 3 (`stage3_selfmaintenance.py`): a beta-mediated
  attention circuit **self-maintains and is bistable** under a soft fetch reward (maintains /
  self-repairs / dissolves); irreversibility is **margin-conditioned, not intrinsic** (the
  original intrinsic claim was walked back after audit). All three channels carry the audited
  `realize(KQVTerm)` provenance.
- 40 tests pass, 2 fail; the 2 failures are exactly the chaotic strong-gate finding above
  (`world/test_chaotic.py`). Run: `PYTHONPATH=$(pwd) dap-core/.venv/bin/python -m pytest
  sensemaking/ -q`.
