# sensemaking

Speculative companion work to the manuscript *Dynamic algebra of potentials* (DAP):
an experiment testing whether **addressed, discrete, reusable communication — "a
language", or "a sense" — emerges** as the low-rate, stable structure of nested
predictive arrangements under a capacity bound, entirely inside the DAP formalism.

Everything here factors through the **KQV attention suboperad of `sarr`**
([`kqv/SPEC.md`](kqv/SPEC.md)), which is faithful to
[`../attention-suboperad.tex`](../attention-suboperad.tex).

## Relationship to `dap`

This package depends on the executable DAP core, vendored as a git submodule at
[`../misc/dap`](../misc/dap) — the public repository
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
PYTHONPATH=$(pwd) misc/dap/.venv/bin/python -m pytest sensemaking/kqv/test_operad_laws.py -q
```

(Equivalently, make your own venv with `jax>=0.4 numpy pytest` and
`pip install -e misc/dap`, then `PYTHONPATH=$(pwd) python -m pytest sensemaking`.)

## Layout

```
sensemaking/
  PLAN.md, AUDIT.md           governance
  kqv/                        the KQV attention suboperad (Tasks 0-1)
    SPEC.md                   the math spec, faithful to attention-suboperad.tex
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
- 25 tests pass (`PYTHONPATH=$(pwd) misc/dap/.venv/bin/python -m pytest sensemaking/kqv/ -q`).
- Task 2 (the partial-observability world) — next.
