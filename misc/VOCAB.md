# dap vocabulary and design

Reference for the `dap` package (`misc/dap/`), the executable core of
`dynamic-algebra-potentials.tex`. Updated 2026-06-08 to match the current paper
(reactive vector spaces, the interpretation + integrator architecture, and the
two functors `Phiconf`/`Phiphase`).

Scope tags:

- `[in-scope]` — implemented in `dap`.
- `[paper-only]` — in the paper at higher generality; `dap` implements only the
  specialization needed for the running examples.
- `[future]` — acknowledged, not implemented.

## Module map

| module | implements | paper |
|---|---|---|
| `rvect.py` | `ReactiveVectorSpace` (position-dependent sharp) | def.rvect |
| `polynomial.py` | `Yon`, `Cot`, `DirichletProduct`, `PolyMap` | sec.poly_dynamic_bg, def.cot |
| `arrangement.py` | `SmoothArrangement` (a morphism of `sarr`) | def.potlens, eqn.srw_morphism |
| `interpretation.py` | `smooth_interpretation` = `Φ'_interpsm` (integrator-free) | sec.smooth_interpretation |
| `integrator.py` | `Integrator`, `configuration_integrator`, `phase_integrator` | sec.integrator_semantics |
| `functors.py` | `cot`, `Phi`, `Phiconf`, `Phiphase` | def.cot, cor.functor |
| `org.py` | `OrgMorphism` (a coalgebra / hom in `org`) | sec.poly_dynamic_bg |
| `wiring.py` | `chain_wire`, `compose_chain`, `parallel_arrangements` | sec.wave_equation |
| `learning.py` | `parameterized_map`, `train`, `forward_backward` | sec.dl_warmup |
| `demo.py` | runnable worked examples | ch.applications |

## Types

- **reactive vector space** (def.rvect) — `[in-scope]` a vector space `Q` with a
  smooth sharp `sharpR_Q : Q -> vect(Q*, Q)`, value `sharpR_q : Q* -> Q` at `q`.
  The reaction may be **position-dependent**; `constant`/`diagonal`/`euclidean`
  build the constant case, `inverse_hessian` the Newton case. Class
  `ReactiveVectorSpace`.
- **smooth adaptive arrangement** (def.potlens, eqn.srw_morphism) — `[in-scope]`
  a morphism in `sarr`: a tuple `(Q, (in_f / out_f), U)` with smooth
  `out_f : Q x out_M -> out_N`, `in_f : Q x out_M x in_N -> in_M`,
  `U : Q x out_M x in_N -> R`. Class `SmoothArrangement` (manifolds = `R^d`,
  recorded by dimension). Was `PotLensMap` with parameter `V`.
- **polynomial** (sec.poly) — `[in-scope]` built from `Yon`, `Cot(d)` = `cot(R^d)`,
  and `DirichletProduct`; maps are `PolyMap`. No generic `Polynomial` class.
- **org / coalgebra** (sec.poly_dynamic_bg) — `[in-scope]` a hom in the bicategory
  `org` is a `[p,q]`-coalgebra, represented as `OrgMorphism = (state, step)` in
  Moore form. The internal hom `[p,q]` is never materialized.
- **`poly`, `mfd`, `vect`, `Lens(C)`, `Para(A,D)`** — `[paper-only]` present
  implicitly; `dap` builds only the specific instances it needs.

## Functors

- **cot : mfd -> poly** (def.cot) — `[in-scope]` `cot_object`, `cot_map`;
  backward part `(T_x f)^T` via `jax.vjp`.
- **Φ'_interpsm : sarr -> Para(cot, poly)** (sec.smooth_interpretation) —
  `[in-scope]` the integrator-free interpretation; `smooth_interpretation(arr)`
  returns `q |-> (position_action, direction_action)` producing
  `(out_n, ω_N, in_m, ξ_Q, ξ_M)` (eqn.outpn/omegaprime/inptm/bigtheta).
- **integrator** (def.integrator) — `[in-scope]` a state space + update rule.
  `configuration_integrator`: `S = |Q|`, `q -> q - sharpR_q(ξ_Q)`
  (eqn.conf_integrator). `phase_integrator`: `S = |T*Q|`,
  `(q,ξ) -> (q + sharpR_q(ξ), ξ - ξ_Q)` (eqn.phase_update).
- **Φ_intg = Ψ_intg ∘ Φ'_interpsm : sarr -> org** (cor.functor) — `[in-scope]`
  `Phi(arr, integrator)`; `Phiconf` and `Phiphase` are the two instances.
- **lrn : Para(rvect, mfd) -> org** (eqn.lrn) — `[in-scope]` gradient-descent
  learner; `parameterized_map` + `Phiconf`, backprop = the lens backward pass.
- **Newton reaction** `sharpR^U_q = (T_q dU)^{-1}` (sec.newton_warmup) —
  `[in-scope]` `rvect.inverse_hessian`; the prototypical position-dependent sharp.
- **multi-stage `org^(K)` / leapfrog** (rmk.org_N) — `[future]` would make the
  wave dynamics a stable symplectic integrator; not implemented (the paper only
  conjectures it).

## Design decisions

1. **Named polynomial constructors**, not a generic `Polynomial` class.
2. **Internal hom is virtual** — it appears only inside `OrgMorphism.step`.
3. **One shared interpretation, swappable integrator.** `Phiconf` and `Phiphase`
   differ only in `integrator.py`; the readout/backward pass is identical
   (paper line 2894). This mirrors the paper's interpretation + integrator split.
4. **Position-dependent sharp.** `sharp_fn(q)` is a callable; the constant case
   is a constructor. Newton needs the non-constant case.
5. **Manifolds = `R^d`.** All examples are Euclidean.
6. **Affine covector fields.** `ω` is carried as an `(A, b)` pair; exact for the
   affine/quadratic examples.
7. **Autodiff backend: JAX.** Cotangent pullbacks and `dU` use `jax.vjp`/`jax.grad`;
   `tests/conftest.py` enables float64.
8. **What is "runnable for real".** `Phiconf` (gradient descent, Newton, heat) is
   explicit Euler on a *gradient* flow: stable for small steps, a genuine
   algorithm. `Phiphase` (wave) is explicit Euler on a *Hamiltonian* flow: the
   recurrence is an exact identity but unstable as a time-stepper (rmk.euler_energy).
