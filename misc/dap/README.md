# dap — dynamic-algebra-potentials

A Python implementation of the principal constructions of the paper
*Dynamic Algebra Potentials* (David Spivak). The package builds, in
order, the categories and functors used in the paper, culminating in
the composite functor

    Phi : potlens --[cint]--> Para(poly) --[leg]--> Para(poly,T) --[dyn]--> dyn

(`thm.functor` in the paper). Two end-to-end tests exercise Phi on the
harmonic chain (`sec.spring`) and Klein–Gordon chain
(`sec.klein_gordon`) and check the resulting trajectories against the
closed-form eigenmode solutions.

## What's in the box

| Module          | Paper reference                                              |
|-----------------|--------------------------------------------------------------|
| `pvect.py`      | `def.pnla` — paired vector spaces `(V, sharp_V)`             |
| `polynomial.py` | `sec.poly` — named constructors `Yon`, `Cot`, `DirichletProduct`, `PolyMap` |
| `lens.py`       | `def.potlens` — potentialized lens maps in `Para(pvect, lmfd^R)` |
| `wiring.py`     | `sec.wd_operads`, `sec.spring` — chain-wire and parallel composition |
| `functors.py`   | `thm.functor` — `cint`, `leg`, `dyn`, and `Phi`              |
| `org.py`        | `def.pq_coalg` — Moore-style `OrgMorphism` (state + step)    |

The `tests/` directory has unit tests for each module plus the two
golden tests above.

## Requirements

- Python 3.10+
- [JAX](https://github.com/jax-ml/jax) (we use `jax.numpy` throughout; `conftest.py` enables `x64`)
- NumPy
- pytest

```
pip install jax numpy pytest
```

## Running the tests

From the directory that *contains* `dap/` (one level up from this file):

```
pytest dap/tests -v
```

The two physics tests are the most fun:

```
pytest dap/tests/test_wave_equation.py -v
pytest dap/tests/test_klein_gordon.py -v
```

Each constructs a chain of K coupled particles as a wiring composite of
single-particle `PotLensMap`s, pushes the composite through `Phi` to get
an `OrgMorphism`, runs the resulting discrete dynamics, and checks the
trajectory against the analytic eigenmode solution.

## Design notes

A few non-obvious conventions, all from `VOCAB.md` in the paper repo:

1. There is no generic `Polynomial` class; polynomials are built only
   from `Yon`, `Cot`, `DirichletProduct`, `PolyMap`.
2. The internal hom `[p, q]` is never materialized; `OrgMorphism`
   stores `state` and a `step` closure that exposes both the action
   `act^beta(s)` as a `PolyMap` and a curried position/direction
   update.
3. Manifolds are specialized to `R^d` throughout this implementation.

## Provenance

Written with Claude Code as a companion to
`dynamic-algebra-potentials.tex`. Module/function docstrings reference
the specific theorems, lemmas, and equations of the paper they
implement.
