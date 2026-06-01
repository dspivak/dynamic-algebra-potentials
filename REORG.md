# Reorg blueprint — `abstract-reorg` branch

Goal: reorganize the paper around its **necessary ingredients**. Define an
abstract *rewiring setup*, prove that every setup (plus an integrator) yields a
functor to `Org`, and recover the current `(mfd, rvect, cot, ℝ)` development as
one instance.

## Organizing principle

- **Machine vs. instance.** Everything generic/categorical builds the machine;
  manifolds/cotangent/reactions are quarantined into ONE instance chapter that
  plugs in and recovers `Φconf, Φphase`.
- **The spine is the factorization** `rWD_D →[Φ'] Para_p(Poly) →[Ψ_𝔦] Org`.
- **Recalled vs. novel.** Background = purely recalled tools; the framework
  chapter = our abstract contributions; the instance chapter = the smooth model.
- **No new proof gaps.** The reorg *relocates existing complete proofs*. (Contrast
  the cut `archive/CC_framework` chapter, whose proofs were stubs — that was a
  different, orthogonal abstraction of Moore internalization via Day convolution.)

## Target structure (with provenance)

```
Ch 1  Introduction                                  [keep; rewrite §Plan only]
      Motivation / smooth→dynamics / CLS relation      sec.intro_*, sec.related_cls

Ch 2  Background — categorical tools                 [generic ONLY; manifolds removed]
      Notation                                         sec.prelim   [drop manifold rows]
      Poly, coalgebras, Org, store                     sec.poly_dynamic_bg  [minus cot subsec]
      Wiring-diagram operads                           sec.wd_operads  [minus "W:=SRWD" line]
      The Para construction                            sec.para_general
      Lenses and backward monads                       sec.lenses_general   ← moved up from Ch3

Ch 3  The abstract framework                         [lands the abstract main theorem]
      Rewiring setups                                ★NEW  def.rewiring_setup
      The syntax operad of a setup                   ★NEW  def.rwd  (from def.potlens)
      Moore internalization & the data functor        sec.abstract_representation
                                                     ★NEW  thm.data_functor (= lem.potlens_to_para_poly at p)
      Integrators & the dynamics functor rWD          sec.integrator_semantics
                                                     ★NEW  thm.dynamics_functor (= thm.functor, abstract)
                                                     ★NEW  rmk.rwd_functor (Tier-1/3), prop.integrator_variation (Tier-2)

Ch 4  The smooth instance                            [plug in; recover]
      Smooth manifolds                                 sec.manifolds_notation   ← moved from Ch2
      Cotangent functor & the potential 𝖉             sec.cot + sec.potential_algebra
      Reactive vector spaces & the exponential         sec.rvect
      Cotangent endofunctor & the two integrators      sec.TT + sec.phase_integrators
      Recovery                                       ★NEW  thm (setup + integrators ⇒ Φconf, Φphase)
      Configuration / phase dynamics, unpacked         sec.configuration_dynamics + sec.phase_dynamics

Ch 5  Applications                                   [unchanged]
      Newton / GD+backprop / wave / graph Laplacian
```

The abstract result lands at the **end of Ch 3**. (Lean Ch 2 of recalled tools
kept separate; fold into Ch 3 only if we want the result literally in Ch 2.)

## The "unzip" — abstract half (Ch 3) ↔ instantiation (Ch 4)

| concept | abstract half (Ch 3) | instantiation (Ch 4) |
|---|---|---|
| potential monad | `lemma.monoid_to_monad` (any comm. monoid `R`) | `R=ℝ` ⇒ `ℝ×−`, `cot(ℝ)⊗−` |
| potential algebra | `rmk.alpha_general` (folded into the setup) | `lem.alpha_constant`, `𝖉` at `r=+1` |
| data functor | **thm.data_functor**: `rWD_D → Para_p(Poly)` | recovery for `p = cot` |
| Moore internalization | `thm.Theta_T_alpha` — **stays whole, relocates** (already abstract) | — |

## The four new statements (status)

1. `def.rewiring_setup` — the ingredient bundle. **Drafted** (framework-new.tex).
2. `thm.data_functor` (Thm A) — `lem.potlens_to_para_poly` with `cot↦p`. **Stated**; proof = relocate.
3. `thm.dynamics_functor` (Thm B) — `thm.functor`, abstract. **Stated**; proof = compose.
4. Recovery (Thm C) — discharge table citing `prop.cot_monoidal`, `prop.cot_hopf`,
   `lem.alpha_constant`, `prop.rvect_polynomial`. **Not yet drafted** (lives in Ch 4).

Plus the framing layer:
- `rmk.rwd_functor` (Tier 1 + Tier 3) — output type / functoriality slogan. **Drafted.**
- `prop.integrator_variation` (Tier 2) — one syntax, many regimes. **Stated; proof TODO** (morphisms of integrators via the readout).

## Rename map (abstract halves only; instance keeps concrete symbols)

| current | abstract |
|---|---|
| `mfd` | `𝓒` (cartesian) |
| `rvect` | `𝓐` with `J: 𝓐→𝓒` |
| `cot` | `p` |
| `ℝ` | `R` (commutative **monoid**, not group) |
| `𝓢𝓡𝓦𝓓` / "smooth rewiring diagrams" | `rWD_D` / "rewiring-diagram operad of a setup" |
| `𝖉` / `lem.alpha_constant` | `(z,α)` potential algebra |

## Naming / notation decisions

- `\rwd` = `\Fun{rWD}` (sans-serif, matches the functor convention). `\rwd_D` =
  operad of a setup; bare `\rwd` = the functor `Data → SMC_{/Org}`.
- Reserve `\srwd` / "smooth rewiring diagrams" for the Ch 4 instance only.
- Domain `\Data` (echoes the intro's "smooth data"); alt `Setup`.
- Codomain is the **(normal-lax, pseudo) slice** `SMC_{/Org}`, not plain `Cat/Org`.

## rWD framing — three tiers

- **Tier 1 (free):** output type "an object of `SMC_{/Org}`." Adopt as the Ch-3 slogan.
- **Tier 2 (cheap, on-thesis):** fix setup, vary integrator → `Int_D → [rWD_D, Org]`.
  Needs morphisms of integrators (config/phase related by readout `T*V↠V`). = `prop.integrator_variation`.
- **Tier 3 (aspirational):** full `rWD: Data → SMC_{/Org}`. Needs morphisms of
  setups + naturality assembly; CLS overlap `𝓡` (`prop.euler_submersion_lenses`)
  is the worked example. = `rmk.rwd_functor`.

## Group vs. monoid (resolved)

`R` is a commutative **monoid**, not a group. The antipode of `p(R)` is never used:
composition adds potentials via `μ=(+)`, never subtracts; `lem.alpha_constant`'s
constancy argument uses only unit+multiplication and generalizes to any commutative
monoid (giving `T*_e R` potential choices). `prop.cot_hopf` (Lie groups) is where
"group" leaked in; it's not a hypothesis we need.

## Execution status / next steps

- [x] Branch `abstract-reorg`.
- [x] Parked, compiling scaffold: `framework-new.tex`, `\input` before the bib.
- [ ] Draft recovery theorem (Thm C) for Ch 4.
- [ ] Move blocks chapter-by-chapter (build after each): Ch 2 trim → Ch 3 assemble → Ch 4 instance.
- [ ] Rename in abstract halves (`cot→p`, `mfd→𝓒`, `ℝ→R`); fix `\cref` breakage.
- [ ] Update `NOTATION.md` (add `𝓒`, `R`; `p` already present) in the same commits.
- [ ] Relocate `framework-new.tex` content into Ch 3; delete the parked `\input`.
