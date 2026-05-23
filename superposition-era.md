# Superposition era: work-package record and fork-point reference

This document consolidates the three work-package plans that drove the paper's expansion from 64 to 74 pages (May 20--22, 2026). It serves two purposes:

1. **Historical record** of what was added and why.
2. **Fork-point reference** for a potential sequel split: what to keep on revert, what goes with the new material.

The commit containing this file marks the safe divergence point.

---

## Timeline

| Date | Commits | What happened |
|------|---------|---------------|
| May 19 | `a531b10` | Last pre-superposition state (64 pp) |
| May 20 | `c0a2805`--`738f1e1` | Manual editing: symplectic sharp, pairing, rho/phase-lift rename, graph Laplacian drafted |
| May 21 | `299a210` | "Edits after Jake's visit" --- superposition seed commit. Abstract rewrite, `\srw`/`\potlens` naming, `rmk.linear_stratum`, `rmk.graph_heat`, graph Laplacian subsection |
| May 22 AM | `590827c`--`dc7f0a6` | **Work package 1** executed (storage design-space reframing) |
| May 22 midday | `d7c3632` | **Work package 2** executed (linear stratum promotion) |
| May 22 PM | `1a5215e` | **Work package 3** executed (critical linearization) + broad editorial pass |
| May 22 PM | `8502551` | Manual editorial pass through 3.4.2 --- structural relocations, terminology changes |

---

## Work package 1: Storage design-space reframing

**Source:** `rewrite-plan.md` (now deleted; full text in Appendix A).

**Goal.** Reframe `sec.cotangent_storages` around a design-space picture: three independent axes of the carrier sharp (constant/kinematical, antisymmetric/conservative, symmetric-pos-def/dissipative). `conf` and `phase` are two named points in this space.

**What it added (64 -> 65 pp):**
- Design-space paragraph in `sec.cotangent_storages` (later relocated to `sec.design_space` by WP2).
- Rewrote `lem.phase_storage` proof to derive from two ingredients: kinetic 1-form $\beta_V$ + canonical symplectic sharp $\sharp^S_{T^*V}$.
- Deleted `rmk.phase_lift` (content absorbed into proof).
- Graduated `rmk.linear_stratum` to `prop.linear_stratum`.
- Sharpened `rmk.constant_inverse_mass_hamiltonian` with design-space axis framing.
- Tightened `rmk.cotangent_learners` and `rmk.graph_heat` with design-space coordinates.
- Split `lem.phase_storage` into composite-form lemma + pair-form `prop.phase_storage_pair`.
- One intro sentence added.

**Labels added:** `prop.linear_stratum`, `eqn.hamiltonian`, `eqn.phase_storage_def`, `prop.phase_storage_pair`.
**Labels removed:** `rmk.linear_stratum`, `rmk.phase_lift`.

---

## Work package 2: Linear stratum promotion

**Source:** `srw-lin-plan.md` (now deleted; full text in Appendix B).

**Goal.** Promote $\srw^{\lin}$ from a single-use ad-hoc suboperad to a named syntactic regime. Decompose at the Para joint: $\srw^{\lin} = \mathrm{Para}(\rvect^{\cnst}, \plmfd^{\lin})$.

**What it added (65 -> 68 pp):**
- Definitions: `def.rvect_cnst`, `def.plmfd_lin`, `def.srw_lin`.
- Lemmas: `lem.quadratic_functorial` (pure quadratic forms), `lem.plmfd_lin_smc`, `lem.action_restricts`.
- Theorem: `thm.srw_lin_suboperad` (embedding via `prop.para_square`).
- Corollary: `cor.srw_lin_four_conditions`.
- New terminal section `sec.design_space` in `ch.dynamics_functor`, consolidating migrated remarks.
- Tagged worked examples ($\Part$, $\psi_G$, etc.) with $\srw^{\lin}$ membership.
- Migrated `prop.linear_stratum`, `rmk.constant_inverse_mass_hamiltonian`, `rmk.cotangent_learners` into `sec.design_space`.
- Macros: `\lin`, `\cnst`.

---

## Work package 3: Critical linearization

**Source:** `crit-lin-plan.md` (now deleted; full text in Appendix C).
**Standalone draft:** `critical-linearization.tex` (kept as source artifact).

**Goal.** Integrate `critical-linearization.tex` into the main paper. Taylor linearization at critical operating points as an operad functor $J^2 \colon \srw_{\crit} \to \srw^{\lin}$, decomposed via Para.

**What it added (68 -> 74 pp):**
- New section `sec.critical_linearization` at end of `ch.potential_driven_dynamics`.
- Subsection 1 (`sec.srw_pointed`): pointed and critical smooth rewiring diagrams via $\rvect_*$, $\plmfd_*$, $\plmfd_*^{\crit}$.
- Subsection 2 (`sec.taylor_critical`): Taylor functor $J^2$ as SMC functor, retract $J^2 \circ \iota = \id$.
- Newton's method example (`ex.newton_critical`): one-step convergence on the quadratic Taylor approximation.
- Macro: `\crit`.

**Labels added:** 21 labels + 4 `\defineTermAs` anchors (see Appendix C for full list).

---

## Incidental changes: what survives a revert

If the superposition-era material is factored out into a sequel and the paper reverted to `a531b10` (May 19), the following independent improvements should be cherry-picked back in.

### Concrete (apply mechanically)

1. **`\newcommand{\inj}{\hookrightarrow}`** + sweep at 6 sites. Pure notation shorthand.

2. **`\crefname{definitionx}{Definition}{Definitions}`** in preamble. Fixes a latent cleveref bug for multi-crefs to definitions.

3. **Citation precision** (5 upgrades):
   - `\cite{ahman2016directed}` -> `\cite[\S 3.2]{ahman2016directed}`
   - `\cite{spivak2019generalized}` -> `\cite[Def.~2.9]{spivak2019generalized}`
   - `\cite{Spivak2023lotteries}` -> `called $\mathrm{lott}$ in~\cite{Spivak2023lotteries}`
   - `\cite{leinster2021entropy}` -> `\cite[Ch.~12]{leinster2021entropy}`
   - `\cite{rumelhart1986learning}` added in DL section

### Style calls (re-evaluate on revert)

4. **Pos/dir notation** for storage pair-form: `\vartheta_{V,1}` -> `\vartheta_V^{\mathrm{pos}}`, `\bk{{\vartheta_V}}{\blank}` -> `\vartheta_V^{\mathrm{dir}}`.

5. **"pure quadratic" -> "quadratic"** throughout. The word "pure" was always redundant; the old paper uses the concept in the potential discussion.

6. **`\Cat{SRW}` -> `\mathbb{S}\Cat{RW}`** rendering for the operad symbol.

7. **`\defineTermAs` removal.** The old paper may not have many of these, but don't re-add them --- the experiment was abandoned.

### Goes with the sequel (do not cherry-pick)

Everything else: `\quadf`, `\srwlin`/`\srwcrit` tracked terms, `\tto`/`\src`/`\tgt`/`\bang` macros, `def.rvect_cnst` relocation, `lem.quadratic_functorial` rewrite, "kinematical" -> "uniform" rename, design-space prose, intro rewrite, acknowledgments (Jake/superposition credit), `critical_point`/`hessian` term anchors, bilinear-form background paragraph, graph Laplacian citation.

---

## Incidental changes: which commits carry them

The two "contaminated" commits where plan-execution and independent improvements are interleaved:

- **`1a5215e`** ("reference check"): carries `\inj` macro, citation precision, `\Cat{SRW}` -> `\mathbb{S}\Cat{RW}`, intro rewrite, acknowledgments, tracked-term additions.
- **`8502551`** ("edits through 3.4.2"): carries `\defineTermAs` removal, "pure quadratic" -> "quadratic", pos/dir notation, `\quadf`, `def.rvect_cnst` relocation, "kinematical" -> "uniform", design-space prose rewrite.

Cherry-picking from these commits is not practical (too interleaved). The concrete items (1--3 above) are small enough to re-apply by hand; the style calls (4--7) are decisions to make fresh.

---

---

# Appendix A: Storage design-space reframing (full plan + edit log)

*Originally `rewrite-plan.md`.*

## Goal

Reframe `sec.cotangent_storages` around a **design-space picture**: a cotangent storage is the data of (carrier, anchor, update), and properties of the carrier's reactive structure $\sharp$ determine the dynamical regime. The current paper presents `conf` and `phase` as two ad hoc storages with a downstream remark (`rmk.graph_heat`) noting they share syntax. The rewrite makes them named points in a small design space, exposes the three structural axes that are currently entangled, and clarifies that *superposition* and *energy conservation* are independent properties of $\sharp$ that physics tends to bundle together.

## Core reframing: three independent axes of carrier $\sharp$

| Axis | Constraint on $\sharp$ | Consequence | Currently lives in |
|---|---|---|---|
| Kinematical | constant linear | superposition (linear endomap on carrier) | `rmk.linear_stratum` |
| Conservative | antisymmetric | energy conservation (Hamiltonian-style) | `rmk.constant_inverse_mass_hamiltonian` |
| Dissipative | symmetric positive-definite | gradient descent on $H$ | `rmk.cotangent_learners`, `rmk.graph_heat` |

The two storages we work out sit at two corners:

- `conf` carrier $V$ with Euclidean $\sharp$: {constant, symmetric pos-def} --- linear + dissipative --- gradient flow.
- `phase` carrier $T^*V$ with canonical symplectic $\sharp_{T^*V}$: {constant, antisymmetric} --- linear + conservative --- Hamiltonian.

The two axes are *orthogonal*. `phase` gets superposition because its $\sharp$ is constant linear, *not* because it's antisymmetric. It gets energy conservation because it's antisymmetric, *not* because it's constant. Disentangling these is the conceptual win.

## Section-by-section changes

### `sec.cotangent_storages`

**Keep:** `def.cotangent_storage`, `prop.storage_pair` (anchor + update), `prop.storage_to_org`.

**Add (new subsection, ~1/2 page):** "Design space of cotangent storages." Lay out the three axes; flag that `conf` and `phase` are two named points; preview that the linear-stratum and energy-conservation results land on different axes.

**Rewrite `prop.rvect_polynomial` (conf storage):**
- Restate as: configuration storage with carrier $V$. Anchor $\id_V$, update $(x,\xi')\mapsto x+\sharp^R_x(\xi')$.
- Note the design-space coordinates: any $\sharp$ on $V$; constant symmetric pos-def is the Euclidean / gradient-descent special case.

**Rewrite `lem.phase_storage` (phase storage):**
- Statement unchanged in pair form: anchor $\pi_V$, update $((x,\xi),\xi')\mapsto(x+\sharp^R_x(\xi),\xi-\xi')$.
- **Proof now derives the formula** from two ingredients, both visibly load-bearing:
  - **Kinetic drift** $x+\sharp^R_x(\xi)$: from the kinetic 1-form $\beta_V$, which uses $\sharp^R_V$ (not symplectic).
  - **Momentum kick with sign** $\xi-\xi'$: from $\theta_{T^*V}^{\mathrm{dir}}$ applied to the lifted covector, which uses the canonical symplectic sharp $\sharp^S_{T^*V}$; that's what flips $(\xi',\sharp^R_x(\xi))$ to $(\sharp^R_x(\xi),-\xi')$.
- Note the design-space coordinates: carrier $T^*V$, $\sharp$ canonical antisymmetric.

**Delete `rmk.phase_lift`:** the construction is now in the proof.

### Two propositions (graduating from remarks)

**`prop.linear_stratum`** (graduates `rmk.linear_stratum`):
> For any cotangent storage whose carrier $\sharp$ is constant linear, the dynamics functor restricted to $\srw^{\lin}$ produces linear endomaps on the carrier. Symplecticity *not* invoked. Kinematical claim only.

**`prop.energy_conservation`** (distilled from `rmk.constant_inverse_mass_hamiltonian`):
> For any cotangent storage whose carrier $\sharp$ is antisymmetric, the (continuous-time) trajectory conserves energy. Linearity *not* required. Dynamical claim only.

*Decision at step 5: energy_conservation stayed as a sharpened remark, not graduated to proposition.*

### `rmk.graph_heat` and `rmk.cotangent_learners`

Tightened with design-space coordinates. No structural change.

### Notation

$\sharp^R$, $\sharp^S_{T^*V}$, $\sharp^{\mathrm{Euc}}$ kept distinct.

## What stayed untouched

- `ch.lenses_internalization` and everything before `sec.storage_semantics`
- Moore internalization, $\srw$ construction
- `thm.functor` (statement and proof unchanged)
- `sec.phase_dynamics`, `sec.configuration_dynamics` (framing-only edits)
- All four worked examples in `ch.applications`
- Bibliography, intro chapter (modulo one sentence)

## Final state

- **Total page delta:** +1 (64 -> 65).
- **Labels removed:** `rmk.linear_stratum`, `rmk.phase_lift`.
- **Labels added:** `prop.linear_stratum`, `eqn.hamiltonian`, `eqn.phase_storage_def`, `prop.phase_storage_pair`.

### Edit log

#### Step 1 --- Design-space subsection
- **Touched:** `sec.cotangent_storages`. Inserted `\paragraph{Design space of cotangent storages.}` after the proof of `prop.storage_pair`.
- **Deviations:** Used `\paragraph` instead of `\subsubsection` (no subsubsections elsewhere). Skipped inline table.

#### Steps 2+3 --- Rewrite `lem.phase_storage` proof; delete `rmk.phase_lift`
- **Touched:** `lem.phase_storage` proof (full replacement); `rmk.phase_lift` (deleted); two back-references updated.
- **Deviations:** Used `\lambda_V` for the phase-lift map (defined inline in proof only). Used description-list (Step 1/Step 2) for the two ingredients.

#### Step 4 --- Graduate `rmk.linear_stratum` to `prop.linear_stratum`
- **Touched:** End of `sec.graph_laplacian`.
- **Deviations:** Kept in place (didn't move to `sec.dynamics_functor`). Dropped the "iff" claim (conflates parameter-sharp and carrier-sharp for `phase`). Hit LaTeX double-subscript error, fixed with extra braces.
- **Page-budget decision:** +2 pages, accepted as cost of the reframing. Langevin sketch skipped.

#### Step 5 --- Sharpen `rmk.constant_inverse_mass_hamiltonian` (not graduate)
- Sharpened as remark, not graduated. Single-use proposition wouldn't amortize. ~0 page delta.

#### Step 6 --- Tighten `rmk.cotangent_learners` and `rmk.graph_heat`
- Design-space coordinate sentences appended. Title added to `rmk.graph_heat`.

#### Step 8 --- Intro sentence
- One sentence appended about the design space.

#### Step 10 --- Split `lem.phase_storage` (post-rewrite refactor)
- User-requested split: composite-form lemma + pair-form proposition with discussion paragraph between them. Saved a page (66 -> 65).

---

# Appendix B: Linear stratum promotion (full plan + edit log)

*Originally `srw-lin-plan.md`.*

## Goal

Promote $\srw^{\lin}$ from a single-use ad-hoc suboperad inside one proposition to a named syntactic regime. Three structural problems with the prior treatment: forward references, ad-hoc introduction, suboperad asserted without checking closure.

## The clean refactoring

Carve at the Para joint. Define each side's "linear part" separately:

- $\rvect^{\cnst} \subseteq \rvect$: full sub-SMC on objects with constant sharp.
- $\plmfd^{\lin} \subseteq \plmfd$: sub-SMC on vector-space interfaces, linear lens maps, pure quadratic potentials.
- $\srw^{\lin}$: underlying operad of $\mathrm{Para}(\rvect^{\cnst}, \plmfd^{\lin})$.

Four conditions recovered by unpacking. Closure under operadic composition automatic from Para once side-SMC closure and action restriction are verified.

## Full proofs

- **Lemma 1** ($\rvect^{\cnst}$ sub-SMC): direct sum of constants is constant.
- **Lemma 2** (pure quadratic functoriality): pullback along linear maps preserves pure quadratic; sums preserve pure quadratic.
- **Lemma 3** ($\plmfd^{\lin}$ sub-SMC): identity, composition (via coKleisli formula + Lemma 2), monoidal product.
- **Lemma 4** (action restricts): action formula of `lem.parameter_lens_action` preserves linearity and pure-quadratic on each component.
- **Theorem** ($\srw^{\lin} \hookrightarrow \srw$): apply `prop.para_square` with $\theta = \id$.
- **Corollary** (four-condition characterization): unpack the Para definition.

## Section-by-section changes

- `sec.W_choice`: definition cluster inserted after `def.potlens`.
- `sec.cotangent_storages`: design-space paragraph deleted (migrated to `sec.design_space`).
- New `sec.design_space` at end of `ch.dynamics_functor`: three-axes paragraph, migrated `prop.linear_stratum`, migrated `rmk.constant_inverse_mass_hamiltonian` (sharpened), migrated `rmk.cotangent_learners` (sharpened).
- `sec.phase_dynamics`: pointer left at old remark site.
- `sec.wave_equation`, `sec.graph_laplacian`: examples tagged with $\srw^{\lin}$ membership.
- Intro: one phrase added.

## Final state

- **Total page delta:** +3 (65 -> 68).
- **Labels added:** `def.rvect_cnst`, `def.plmfd_lin`, `def.srw_lin`, `thm.srw_lin_suboperad`, `cor.srw_lin_four_conditions`, `lem.quadratic_functorial`, `lem.plmfd_lin_smc`, `lem.action_restricts`, `sec.design_space`, `pure_quadratic_form` term anchor.
- **Labels relocated:** `prop.linear_stratum`, `rmk.constant_inverse_mass_hamiltonian`, `eqn.hamiltonian`, `rmk.cotangent_learners`, `eqn.learning_sharp`.
- **Preamble:** `\lin`, `\cnst` macros; `\crefname{definitionx}` declaration.

### Edit log

#### Step 1 --- Macros + linear-stratum cluster
- Inserted after the `closed_system` paragraph in `sec.forming_potlens` (not before the composition-diagram remark, as originally planned). Dropped $\Sym^2$ notation (no preamble macro). Inlined Lemma 1 as one-paragraph remark.

#### Step 2 --- Tag worked examples
- Five sites in `ch.applications` tagged. `\fun{wire}_K` tagged implicitly via the chain-composite sentence.

#### Step 3 --- New `sec.design_space`
- Inserted between `sec.configuration_dynamics` and `\chapter{Applications}`. Opening frames as consolidation. Content temporarily duplicated with `sec.cotangent_storages` block (resolved at step 7).

#### Step 4 --- Migrate `prop.linear_stratum`
- Statement compressed (four-condition recap dropped, now cited as `def.srw_lin`). "Pure-quadraticity of $U$ means..." replaced with "Since $U$ is pure quadratic..." (term now defined upstream).

#### Step 5 --- Migrate and sharpen Hamiltonian remark
- Kept unified (not split). Bold-hypothesis structure removed; collapsed to "$f$ is a $0$-ary closed system in $\srw^{\lin}$, applied through $\store{\phase}$" + "parameter sharp moreover symmetric."

#### Step 6 --- Migrate and sharpen learners remark
- Title changed to "Gradient descent as the dissipative-corner instance."

#### Step 7 --- Delete old design-space block
- Bifurcation paragraph extended with forward pointer to `sec.design_space`.

#### Steps 8--10 --- Sharpen `rmk.graph_heat`, phase-dynamics pointer, intro sentence
- Minimal-touch edits.

#### Step 11 --- Rebuild and sweep
- Fixed stray `\cref{sec.cotangent_storages}` at line 2500. Fixed `cleveref` `definitionx` format warning.

---

# Appendix C: Critical linearization (full plan + edit log)

*Originally `crit-lin-plan.md`. Standalone draft `critical-linearization.tex` kept as source artifact.*

## Goal

Add an end-of-`ch.potential_driven_dynamics` section formalizing Taylor linearization at critical operating points. Delivers:

1. Operad $\srw_*$ of pointed smooth rewiring diagrams.
2. Sub-operad $\srw_{\crit} \subseteq \srw_*$ cut out by criticality $dU|_z = 0$.
3. Symmetric monoidal functor $J^2 \colon \srw_{\crit} \to \srw^{\lin}$ (tangent-and-Hessian).
4. Retract $J^2 \circ \iota = \id_{\srw^{\lin}}$ via zero-pointing.

## The clean refactoring

Decompose via Para:

- $\rvect_*$: reactive vector spaces with basepoint.
- $\plmfd_*$: potentialized manifold lenses with basepoint.
- $\plmfd_*^{\crit} \subseteq \plmfd_*$: criticality condition.
- $J^2_{\rvect} \colon \rvect_* \to \rvect^{\cnst}$: evaluate sharp at basepoint.
- $J^2_{\plmfd} \colon \plmfd_*^{\crit} \to \plmfd^{\lin}$: tangent-and-Hessian.
- Action square commutes via canonical $T_{v_0}V \cong V$.
- `prop.para_square` delivers $J^2$ as strong symmetric monoidal functor.

## Section-by-section changes

- New `sec.critical_linearization` at end of `ch.potential_driven_dynamics`.
- Subsection 1 (`sec.srw_pointed`): `def.rvect_pointed`, `def.plmfd_pointed`, `lem.plmfd_pointed_smc`, `lem.action_restricts_pointed`, `def.srw_pointed` with unpacking paragraph, `def.plmfd_critical`, `lem.plmfd_critical_smc`, `def.srw_critical`, `rmk.full_vs_storage_critical`.
- Subsection 2 (`sec.taylor_critical`): `def.J2_rvect`, `lem.J2_rvect_smc`, `def.J2_plmfd`, `lem.J2_plmfd_smc`, `lem.J2_action_compatible`, `thm.taylor_critical_functor`, `cor.taylor_retract`, `rmk.srw_lin_taylor_target`.
- Newton's method example (`ex.newton_critical`).
- Cross-reference in `sec.design_space` + intro paragraph update.
- Macro: `\crit`.

## Final state

- **Total page delta:** +6 (68 -> 74).
- **Labels added:** `sec.critical_linearization`, `sec.srw_pointed`, `sec.taylor_critical`, `def.rvect_pointed`, `def.plmfd_pointed`, `def.plmfd_critical`, `def.srw_pointed`, `def.srw_critical`, `lem.plmfd_pointed_smc`, `lem.action_restricts_pointed`, `lem.plmfd_critical_smc`, `def.J2_rvect`, `def.J2_plmfd`, `lem.J2_rvect_smc`, `lem.J2_plmfd_smc`, `lem.J2_action_compatible`, `thm.taylor_critical_functor`, `cor.taylor_retract`, `rmk.full_vs_storage_critical`, `rmk.srw_lin_taylor_target`, `ex.newton_critical`.
- **`\defineTermAs` anchors:** `pointed_srw_diagram`, `critical_srw_diagram`, `J2_rvect`, `J2_plmfd`.

### Edit log

#### Step 1 --- Macro
- Added `\newcommand{\crit}{\mathrm{crit}}` after `\cnst`.

#### Step 2 --- Pointed/critical cluster
- Inserted `sec.critical_linearization` between `rmk.cotangent_learners` and `\chapter{Applications}`. Three-component compatibility for $\plmfd_*$ (including $U(\outp m_0, \inpt n_0) = 0$). Action restriction for pointed case kept separate; folded into `lem.plmfd_critical_smc` for critical case. Build: 71 pages (+3 over baseline).

#### Step 3 --- Taylor functor cluster
- Build fix: `\Phi_\store{\bullet}` double-subscript error, fixed with extra braces. Hessian chain rule included explicitly (editorial pass might prefer citing a standard reference). $\iota$ defined inline, not as separate definition. Build: 73 pages.

#### Step 4 --- Newton's example
- Used `example` environment (not `\paragraph`). Kept explicit one-step convergence calculation. No backward link from `sec.newton_warmup`. Build: 74 pages.

#### Steps 5--7 --- Cross-references and rebuild
- Design-space cross-reference, intro update, full sweep. All 21 labels + 4 term anchors resolve.
- Page delta over plan estimate (+6 vs. planned +2.5 to +3). Sources: `lem.plmfd_pointed_smc` longer than planned, Hessian chain rule explicit, Newton example at full weight.
