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
| data functor | **thm.data_functor**: `rWD_D → Para_𝖼(Poly)` | recovery for `𝖼 = cot` |
| Moore internalization | `thm.Theta_T_alpha` — **stays whole, relocates** (already abstract) | — |

## The four new statements (status)

1. `def.rewiring_setup` — the ingredient bundle. **Drafted** (framework-new.tex).
2. `thm.data_functor` (Thm A) — `lem.potlens_to_para_poly` with `cot↦p`. **Stated**; proof = relocate.
3. `thm.dynamics_functor` (Thm B) — `thm.functor`, abstract. **Stated**; proof = compose.
4. Recovery (Thm C) — `prop.smooth_setup` (the tuple is a setup: 5-clause discharge)
   + `thm.recovery` (`rWD_Dsm = 𝓢𝓡𝓦𝓓`; `Φ_𝔦θ=Φconf`, `Φ_𝔦β=Φphase`). **Drafted**
   (framework-new.tex §Recovery); relocates to Ch 4.

Plus the framing layer:
- `rmk.rwd_functor` (Tier 1 + Tier 3) — output type / functoriality-in-setup slogan. **Drafted.**
- `rmk.integrator_design` (Tier 2) — integrator functoriality **not pursued** (config/phase
  and the friction family are not maps of integrators in any evident sense). **Drafted.**

## Rename map (abstract halves only; instance keeps concrete symbols)

| current | abstract | reminiscent of |
|---|---|---|
| `mfd` | `𝓜` (`\cat M`, cartesian) | manifolds |
| `rvect` | `𝓥` (`\cat V`) with `J: 𝓥→𝓜` | vector spaces |
| `cot` | `𝖼` (`\Fun c`, sans-serif like `\cot`) | cotangent |
| `ℝ` | `R` (commutative **monoid**, not group) | |
| `𝓢𝓡𝓦𝓓` / "smooth rewiring diagrams" | `rWD_D` / "rewiring-diagram operad of a setup" | |
| `𝖉` / `lem.alpha_constant` | `(z,α)` potential algebra | |

## Naming / notation decisions

- `\rwd` = `\Fun{rWD}` (sans-serif, matches the functor convention). `\rwd_D` =
  operad of a setup; bare `\rwd` = the functor `Data → SMC_{/Org}`.
- Reserve `\srwd` / "smooth rewiring diagrams" for the Ch 4 instance only.
- Domain `\Data` (echoes the intro's "smooth data"); alt `Setup`.
- Codomain is the **(normal-lax, pseudo) slice** `SMC_{/Org}`, not plain `Cat/Org`.
- Abstract symbols `𝓜 / 𝓥 / 𝖼` are reminiscent of `mfd / rvect / cot`. Caveats:
  `𝓥` (`\cat V`) is font-distinct from the carrier `V`; `𝖼` (`\Fun c`) is sans-serif
  like `\cot`, distinct from the italic lens component `c` and roman friction `c`.
- "Coupled" dropped from `def.rewiring_setup`: it is needed only to *classify* the `α`'s
  (`rmk.alpha_general`), not to *posit* one.
- `def.T_monoid` must precede `def.rewiring_setup` in the final ordering (clause 5 cites it).

## rWD framing — three tiers

- **Tier 1 (free):** output type "an object of `SMC_{/Org}`." Adopt as the Ch-3 slogan.
- **Tier 2 (NOT pursued):** fix setup, vary integrator → `Int_D → [rWD_D, Org]`. Dropped —
  the actual integrators are not related by maps of integrators: config vs phase differ on
  stored-vs-incoming momentum (the projection `T*V↠V` does not intertwine the updates), and
  friction isn't natural. No current result consumes it. Recorded as `rmk.integrator_design`.
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
- [x] Draft recovery theorem (Thm C): `prop.smooth_setup` + `thm.recovery`.
- Move blocks one at a time (build after each):
  - [x] **1.** Lenses + backward monads → Background (after Para).
  - [ ] **2.** Manifolds + cot → new instance-chapter shell (out of Background). *(deferred to last, after the instance chapter exists)*
  - [x] **3.** Relocate framework draft into position as Ch 3; retire the parked `\input`. *(done before #2, per agreed reorder)*
  - **4.** Fill data-functor/integrator stubs:
    - [x] prep: inline the framework chapter into the main file.
    - [x] **4a.** Moore internalization machinery → Ch 3 data-functor section (label preserved).
    - [x] **4b.** abstract integrators (`sec.org_as_para`, `def.integrator`, `prop.integrator_to_org`) → Ch 3 dynamics-functor section; `sec.TT`/`sec.phase_integrators`/`prop.rvect_polynomial`/config integrator left for the instance.
  - **5.** Dedup (concrete = corollary of abstract) + assemble instance chapter:
    - [x] part 1: word-for-word abstract proofs (thm.data_functor ← lem.potlens_to_para_poly, thm.dynamics_functor ← thm.functor); add `lem.c_lifts_lens`.
    - [x] part 2a: dedup `thm.recovery`'s proof (drop the four doomed full-proof citations).
    - [x] part 2b: delete `lem.potlens_to_para_poly` (folded into recovery); `thm.functor` → headline **corollary** of `thm.dynamics_functor`.
    - [x] part 2c: redirect stale `thm.functor` references (Ch 5 intro, `rmk.rmfdc`, the Φconf/Φphase unpacking) → `thm.dynamics_functor`. (Plan 647 deferred to step 6's holistic plan rewrite.)
    - [x] part 2d: delete the other two subsumed concretes `lem.cot_lifts_lens_potential`, `lem.Theta_poly_potential`.
    - [x] part 2e-i: relocate Recovery (prop.smooth_setup + thm.recovery + handoff) into `sec.dynamics_functor` (Ch 5), after the integrators — fixes its forward-refs; drop the empty Recovery section header.
    - [ ] part 2e-ii (optional): move #2 — manifolds + `sec.cot` from Background into the instance (Ch 4 start), so the instance is self-contained with its ingredients. Surgical (`sec.cot` is nested in `sec.poly_dynamic_bg`). Reframe Ch 4/Ch 5 intros + titles as "the smooth instance".
  - **6.** Trims:
    - [x] drop "[DRAFT scaffold]" title; rename `ch.framework_DRAFT` → `ch.framework`.
    - [ ] move `lemma.monoid_to_monad` earlier (kills the `lem.c_lifts_lens` forward-ref).
    - [ ] rewrite the **Plan** (`sec.plan`) for the 5-chapter shape (it still describes the old 4-chapter structure, missing the framework chapter).
    - [ ] NOTATION pass (add `𝓜`/`𝓥`/`𝖼`/`R`/`rWD`; reconcile with the new structure).
- [x] **Math gap closed:** `lem.c_lifts_lens` stated (= `lem.cot_lifts_lens_potential` at `𝖼`).
- [ ] Rename in abstract halves (`cot→𝖼`, `mfd→𝓜`, `ℝ→R`); fix `\cref` breakage.
- [ ] Update `NOTATION.md` (add `𝓒`, `R`; `p` already present) in the same commits.
- [ ] Relocate `framework-new.tex` content into Ch 3; delete the parked `\input`.
