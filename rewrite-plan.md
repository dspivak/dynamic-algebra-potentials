# Storage section rewrite plan

## Goal

Reframe `sec.cotangent_storages` around a **design-space picture**: a cotangent storage is the data of (carrier, anchor, update), and properties of the carrier's reactive structure $\sharp$ determine the dynamical regime. The current paper presents `conf` and `phase` as two ad hoc storages with a downstream remark (`rmk.graph_heat`) noting they share syntax. The rewrite makes them named points in a small design space, exposes the three structural axes that are currently entangled, and clarifies that *superposition* and *energy conservation* are independent properties of $\sharp$ that physics tends to bundle together.

## Core reframing: three independent axes of carrier $\sharp$

| Axis | Constraint on $\sharp$ | Consequence | Currently lives in |
|---|---|---|---|
| Kinematical | constant linear | superposition (linear endomap on carrier) | `rmk.linear_stratum` |
| Conservative | antisymmetric | energy conservation (Hamiltonian-style) | `rmk.constant_inverse_mass_hamiltonian` |
| Dissipative | symmetric positive-definite | gradient descent on $H$ | `rmk.cotangent_learners`, `rmk.graph_heat` |

The two storages we work out sit at two corners:

- `conf` carrier $V$ with Euclidean $\sharp$: {constant, symmetric pos-def} → linear + dissipative → gradient flow.
- `phase` carrier $T^*V$ with canonical symplectic $\sharp_{T^*V}$: {constant, antisymmetric} → linear + conservative → Hamiltonian.

The two axes are *orthogonal*. `phase` gets superposition because its $\sharp$ is constant linear, *not* because it's antisymmetric. It gets energy conservation because it's antisymmetric, *not* because it's constant. Disentangling these is the conceptual win.

Varying $\sharp$ (e.g. double pendulum) is preserved as a generality; the linear stratum is the constant-$\sharp$ sub-stratum where superposition holds. Both are real.

## Section-by-section changes

### `sec.cotangent_storages`

**Keep:** `def.cotangent_storage`, `prop.storage_pair` (anchor + update), `prop.storage_to_org`.

**Add (new subsection, ~½ page):** "Design space of cotangent storages." Lay out the three axes; flag that `conf` and `phase` are two named points; preview that the linear-stratum and energy-conservation results land on different axes.

**Rewrite `prop.rvect_polynomial` (conf storage):**
- Restate as: configuration storage with carrier $V$. Anchor $\id_V$, update $(x,\xi')\mapsto x+\sharpR_x(\xi')$.
- Note the design-space coordinates: any $\sharp$ on $V$; constant symmetric pos-def is the Euclidean / gradient-descent special case.

**Rewrite `lem.phase_storage` (phase storage):**
- Statement unchanged in pair form: anchor $\pi_V$, update $((x,\xi),\xi')\mapsto(x+\sharpR_x(\xi),\xi-\xi')$.
- **Proof now derives the formula** from two ingredients, both visibly load-bearing:
  - **Kinetic drift** $x+\sharpR_x(\xi)$: from the kinetic 1-form $\beta_V$ \eqref{eqn.kinetic_one_form}, which uses $\sharpR_V$ (not symplectic).
  - **Momentum kick with sign** $\xi-\xi'$: from $\theta_{T^*V}^{\dir}$ applied to the lifted covector, which uses the canonical symplectic sharp $\sharpS_{T^*V}$ \eqref{eqn.canonical_sharp}; that's what flips $(\xi',\sharpR_x(\xi))$ to $(\sharpR_x(\xi),-\xi')$.
- Note the design-space coordinates: carrier $T^*V$, $\sharp$ canonical antisymmetric.

**Delete `rmk.phase_lift`:** the construction is now in the proof; the remark was a vestige of treating the categorical construction as "alternative." Keep the term *phase lift* if a downstream reference needs it (verify: line ~2592 in `sec.phase_dynamics` references it; either keep a one-line term definition or rephrase the back-ref).

### Two new propositions (graduating from remarks)

**`prop.linear_stratum`** (graduates `rmk.linear_stratum`):
> For any cotangent storage whose carrier $\sharp$ is constant linear, the dynamics functor restricted to $\srw^{\mathrm{lin}}$ produces linear endomaps on the carrier. The hypotheses are: storage's anchor and update linear (which holds iff carrier $\sharp$ is constant linear), and $\srw$-side linear/quadratic.

Symplecticity *not* invoked. This is the kinematical claim only.

**`prop.energy_conservation`** (distilled from `rmk.constant_inverse_mass_hamiltonian`):
> For any cotangent storage whose carrier $\sharp$ is antisymmetric and where the $\srw$-side potential $U$ admits a Hamiltonian reading, the (continuous-time) trajectory conserves energy.

Linearity *not* required. This is the dynamical claim only.

These two propositions sit in different parts of the design space. `phase` lies in the intersection and inherits both. `conf` with Euclidean $\sharp$ lies in linear ∩ dissipative, inheriting linear-stratum but not conservation.

### `rmk.graph_heat`

Becomes a one-sentence **corollary** of the design-space picture: applying $\psi_G$ through `phase` (antisymmetric corner) gives the wave equation; through `conf` with Euclidean $\sharp$ (symmetric pos-def corner) gives the heat equation. No longer a surprise.

### `rmk.cotangent_learners`

Lightly rewritten to name its design-space coordinates: "conf with constant Euclidean $\sharp$ — symmetric corner — recovers gradient descent."

### Notation

Leave $\sharpR$, $\sharpS_{T^*V}$, $\sharpEuc$ as-is — the distinct names carry meaning. Optionally add a small inline table in the design-space subsection mapping each named sharp to its (carrier, symmetry) coordinates. Don't introduce a new unified $\sharp$ symbol.

## One short worked example (optional)

Add ~⅓ page in `ch.applications` (or in the new design-space subsection) sketching a **mixed-sharp / Langevin storage** as a third point in the design space:

> Take the carrier $T^*V$ with reactive structure $\sharp = \sharp_{T^*V} + \alpha\,\sharpRiem$ for small $\alpha>0$ — antisymmetric symplectic plus symmetric positive-definite. Both `prop.linear_stratum` and a damped analog of `prop.energy_conservation` apply: the trajectory is linear (when $\sharpR_V$ is constant and $U$ quadratic), but energy decays at rate proportional to $\alpha$. This is the storage-level shape of Langevin / GENERIC dynamics.

Two paragraphs max. **Verify first** that $\sharp_{T^*V} + \alpha\,\sharpRiem$ is genuinely a reactive structure (nondegenerate iso) on $T^*V$ for small $\alpha$ before committing. If not, drop the example or replace with another natural mixed/asymmetric instance.

## What stays untouched

- `ch.lenses_internalization` and everything before `sec.storage_semantics`
- Moore internalization, $\srw$ construction
- `thm.functor` (statement and proof unchanged)
- `sec.phase_dynamics`, `sec.configuration_dynamics` (consume the storages; framing-only edits)
- All four worked examples in `ch.applications` (Newton, DL, wave, graph Laplacian) — except potentially the one short addition above
- Bibliography, intro chapter (modulo a sentence updating the design-space framing)

## Sketch: the rewritten proof of `lem.phase_storage`

The lemma's *statement* keeps the pair form (anchor $\pi_V$, update $((x,\xi),\xi')\mapsto(x+\sharpR_x(\xi),\xi-\xi')$). The new proof derives this formula by composing two ingredients, with each one's role named.

**Construction.** Define $\rho_V$ as the composite
$$\Store(\absval{T^*V})\;\overset{\theta_{T^*V}}{\longrightarrow}\;\cotof{T^*V}\;\overset{\lambda_V}{\longrightarrow}\;\cotof V$$
where:

- $\theta_{T^*V}$ is the configuration storage of `prop.rvect_polynomial` applied at the carrier $T^*V$. Its update uses $T^*V$'s reactive structure, which by `prop.canonical_symplectic_pairing` *is* the canonical symplectic sharp $\sharpS_{T^*V}$ from \eqref{eqn.canonical_sharp}.
- $\lambda_V$ is the phase-lift composite $\cotof{T^*V}\to\cotof{T^*V}\otimes\cotof{T^*V}\to\cotof V\otimes\yon\cong\cotof V$ from \eqref{eqn.phase_lift_decomp}, built from the $\otimes$-comultiplication of `lem.cot_comonoid` and the kinetic 1-form $\beta_V$ from \eqref{eqn.kinetic_one_form}.

Each ingredient does one job:

- $\lambda_V$ contributes the **kinetic drift** $\sharpR_x(\xi)$ (via $\beta_V$, which uses $\sharpR_V$).
- $\theta_{T^*V}$ contributes the **position-momentum flip with sign** (via $\sharpS_{T^*V}$).

**Pair-form readout (using `prop.storage_pair`).**

*Anchor.* On positions: $\theta_{T^*V,1}=\id_{\absval{T^*V}}$ (conf storage is identity on positions) and $\lambda_{V,1}\colon(x,\xi)\mapsto x$ (from $\cotof{\pi_V}$ on positions). Composite: $\pi_V$.

*Update.* At state $(x,\xi)\in\absval{T^*V}$ and incoming $\xi'\in V^*$, trace through the composite (reading right-to-left as functions on directions, which run backward through poly maps):

- **Step 1 (apply $\lambda_V$ on directions at $(x,\xi)$).** The phase-lift map sends $\xi'\in T^*_xV\cong V^*$ to
$$(\xi',\,0)\;+\;\beta_V(x,\xi)\;=\;(\xi',\,\sharpR_x(\xi))\;\in\;V^*\oplus V\cong T^*_{(x,\xi)}T^*V,$$
where $(\xi',0)$ is the cotangent pullback along $\pi_V$, $\beta_V(x,\xi)=(0,\sharpR_x(\xi))$ is the kinetic 1-form, and the sum is fiberwise addition from $\cotof{\Delta_{T^*V}}$. This is the *kinetic-drift contribution* — it injects the velocity $\sharpR_x(\xi)$ into the second component.
- **Step 2 (apply $\theta_{T^*V}$ on directions at $(x,\xi)$).** The conf-storage update at carrier $T^*V$ sends a covector $\omega\in T^*_{(x,\xi)}T^*V$ to
$$\bk{{\theta_{T^*V}}}{(x,\xi)}(\omega)\;=\;(x,\xi)\;+\;\sharpS_{T^*V}(\omega).$$
For our $\omega=(\xi',\sharpR_x(\xi))$ from Step 1, \eqref{eqn.canonical_sharp} gives
$$\sharpS_{T^*V}(\xi',\sharpR_x(\xi))\;=\;(\sharpR_x(\xi),\,-\xi').$$
This is the *symplectic-flip contribution* — it swaps the two components and introduces the minus sign on momentum.

Adding to $(x,\xi)$:
$$(x,\xi)\;+\;(\sharpR_x(\xi),\,-\xi')\;=\;(x+\sharpR_x(\xi),\;\xi-\xi'),$$
which is the displayed update. The drift $x+\sharpR_x(\xi)$ is the kinetic contribution; the kick $\xi-\xi'$ — including its sign — is the symplectic contribution.

**Naturality** in $\rvect$-isomorphisms is inherited from the components: $\theta_{T^*V}$ is natural by `prop.rvect_polynomial` applied at $T^*V$ (using the pairing-preservation equation \eqref{eqn.pairing_triangle} for $\sharpS_{T^*V}$); $\lambda_V$ is natural in $\rvect$-isos because $\beta_V$ and $\cotof{\Delta_{T^*V}}$ both are.

**Monoidality** follows from the direct-sum convention $\sharpR_{V_1\oplus V_2}=\sharpR_{V_1}\oplus\sharpR_{V_2}$ (\cref{prop.rvect_monoidal}) and the monoidality of $\theta$ and $\lambda$.

### What this sketch reveals

1. The two ingredients are *structurally distinct*: $\beta_V$ (using $\sharpR_V$) ≠ $\sharpS_{T^*V}$ (using only the canonical structure on $T^*V$). They cannot be conflated; they enter at different steps and contribute different terms.
2. The minus sign on momentum has a *single* source: $\sharpS_{T^*V}$ via $\theta_{T^*V}$'s update. Removing or modifying $\sharpS_{T^*V}$ would change the sign and break Hamiltonicity.
3. The drift $\sharpR_x(\xi)$ has a *single* source: $\beta_V$ via $\lambda_V$. Removing or modifying $\beta_V$ would kill the kinetic motion entirely (you'd get pure momentum decay).
4. The pair-form lemma now reads honestly: "here's the formula; here are the two ingredients that produce each half of it; neither is auxiliary."
5. `rmk.phase_lift` is genuinely redundant after this rewrite — its content is the construction in the proof. Delete cleanly.

### Things to check while writing

- The naming $\lambda_V$ for the phase-lift map: pick a letter that doesn't collide. The current $\rho_V$ is being repurposed (in the pair-form `lem.phase_storage` it's the *whole* storage, not just the lift). Use $\lambda$ or another free letter for the lift map. Mention it once in the proof, don't add it to the global notation.
- Whether to make the construction $\rho_V\coloneqq\lambda_V\circ\theta_{T^*V}$ explicit in the lemma's statement or only in the proof. Recommendation: in the proof only, to keep the pair-form statement clean and front-facing.
- Cross-references: \eqref{eqn.kinetic_one_form}, \eqref{eqn.canonical_sharp}, `prop.canonical_symplectic_pairing`, `prop.rvect_polynomial`, \eqref{eqn.pairing_triangle}, `prop.rvect_monoidal`, `lem.cot_comonoid`, \eqref{eqn.phase_lift_decomp}.
- After deleting `rmk.phase_lift`, \eqref{eqn.phase_lift_decomp} loses its containing environment. Move the equation into the proof of `lem.phase_storage`.

## Order of operations

1. Add design-space subsection in `sec.cotangent_storages` (introduces axes, previews two propositions).
2. Rewrite proof of `lem.phase_storage` to derive update from $\beta_V$ + $\sharpS_{T^*V}$.
3. Delete `rmk.phase_lift`; update the back-reference in `sec.phase_dynamics`.
4. Graduate `rmk.linear_stratum` to `prop.linear_stratum` with kinematical-only framing.
5. Distill `rmk.constant_inverse_mass_hamiltonian` into `prop.energy_conservation` (or leave as remark with sharper framing — call this once we see how the proposition reads).
6. Tighten `rmk.graph_heat` and `rmk.cotangent_learners` to use design-space coordinates.
7. (Optional, last) Add Langevin sketch — only if it survives the nondegeneracy check.
8. Update intro chapter sentence about conf/phase to mention the design space.
9. Rebuild; sanity-check cross-references; spot-check that downstream citations of `rmk.linear_stratum` still resolve (they reference the new proposition).

## Risks and uncertainties

1. **Langevin fit.** Need to confirm $\sharp_{T^*V} + \alpha\,\sharpRiem$ is nondegenerate. Likely yes for small $\alpha$, but a real check before claiming.
2. **Axis independence on curved carriers.** The three axes are clean for vector-space carriers. If you ever generalize to nilpotent Lie algebras (`rmk.rnla_generalization`) or curved manifolds, "constant" requires a connection or group structure to make sense; "(anti)symmetric" requires a bundle metric. The design-space picture may need refinement there. Out of scope for this rewrite, but worth flagging.
3. **`prop.energy_conservation` continuous vs discrete.** The current `rmk.constant_inverse_mass_hamiltonian` is honest that the discrete (explicit-Euler) dynamics doesn't conserve energy — only the underlying continuous vector field does. The new proposition needs to be equally careful: state energy conservation for the *continuous* flow, note the discrete dynamics is its Euler step (which doesn't conserve), and cite `rmk.euler_energy` / `rmk.org_N` (multi-stage integrators) for the discrete remedy.
4. **Backward-compat citations.** `rmk.linear_stratum`, `rmk.phase_lift`, `def.phase_lift` are referenced; the rewrite changes labels. Need to update each citing site.
5. **Page count.** Net delta likely ~0 to +½ page (added design space subsection + propositions, balanced by deleted alt-construction remark and tightened existing remarks). Not a budget concern.

## Estimated effort

2–3 days of focused work. Concentrated in `sec.cotangent_storages` plus a half-dozen downstream remarks. Most of the proof-level work is in rewriting `lem.phase_storage`'s proof to construct from $\beta_V + \sharpS_{T^*V}$ — that's the technically delicate piece.

## What this rewrite is *not*

- Not a reorganization of the paper's chapter structure.
- Not a generalization to nilpotent Lie algebras or curved carriers (parked in `rmk.rnla_generalization`).
- Not adding multi-stage integrators (parked in `rmk.org_N`).
- Not a comprehensive treatment of Langevin / GENERIC / Lie-Poisson — only a sketch to demonstrate the design space has more than two corners.

---

## Edit log (running memory)

Format: each entry covers one session-step. Lists files/locations touched, deviations from the plan, and editorial decisions worth flagging for the editorial pass.

### Step 1 — Design-space subsection
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** `sec.cotangent_storages`. Inserted a new `\paragraph{Design space of cotangent storages.}` block immediately after the proof of `prop.storage_pair` and before the existing "bifurcation between learning and physics" paragraph (around line 2337).
- **Content:** Three-axis enumeration (kinematical / conservative / dissipative), each cross-referenced to the existing remark that carried the claim (`rmk.linear_stratum`, `rmk.constant_inverse_mass_hamiltonian`, `rmk.cotangent_learners`). Closes by locating `conf` and `phase` at two corners and asserting orthogonality of the kinematical and dynamical axes.
- **Decisions / deviations:**
  - The plan called this a "new subsection." There are no `\subsubsection`s elsewhere in the document, so I used `\paragraph{...}` instead. No structural break.
  - Per the citation-rules memory ("don't say symplectic in statements"), the body says "antisymmetric" plus `\eqref{eqn.canonical_form}` rather than "symplectic". `rmk.symplectic_perpendicular` is cited for the argument that antisymmetry yields tangent-to-level-set.
  - Skipped the optional `(carrier, symmetry)` inline table — the prose names each storage's coordinates already.
  - Kept the existing bifurcation paragraph in place rather than deleting/merging it (edit-scope discipline).
  - Forward-references `prop.rvect_polynomial` and `lem.phase_storage` (next two propositions in the same subsection — fine).

### Steps 2+3 — Rewrite `lem.phase_storage` proof; delete `rmk.phase_lift`
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:**
  - `lem.phase_storage` proof (around line 2408): full replacement.
  - `rmk.phase_lift` (was around line 2412): deleted; its equation `\eqref{eqn.phase_lift_decomp}` and `\defineTermAs{phase_lift}{...}` term-definition both migrated into the new proof.
  - Back-reference at the kinetic-1-form definition (around line 1917): "used later in `\cref{rmk.phase_lift}`" → "used later in the proof of `\cref{lem.phase_storage}`."
  - Back-reference in `sec.phase_dynamics` (around line 2601, in the discussion following `eqn.state_update`): "phase lift at $(x,\xi)$, `\cref{rmk.phase_lift}`" → "phase lift at $(x,\xi)$ (the proof of `\cref{lem.phase_storage}`)."
- **Content:** Lemma statement unchanged. New proof constructs $\rho_V = \lambda_V \circ \theta_{T^*V}$ where $\lambda_V$ is the phase-lift composite (uses $\beta_V$) and $\theta_{T^*V}$ is configuration storage at the carrier $T^*V$ (uses $\sharpS_{T^*V}$). Pair-form readout is broken into Step 1 (apply $\lambda_V$ on directions, giving $(\xi', \sharpR_x(\xi))$ via $\beta_V$ — kinetic-drift contribution) and Step 2 (apply $\theta_{T^*V}$ on directions, giving the flip + minus sign via $\sharpS_{T^*V}$ — symplectic contribution). Naturality and monoidality argued at the end.
- **Decisions / deviations:**
  - Used `\lambda_V` for the phase-lift map per the plan's recommendation; defined inline in the proof, not added to global notation.
  - Construction is in the proof only, not in the lemma statement (matches plan's recommendation).
  - Used a `description`-list (`Step 1 / Step 2`) rather than inline prose; this makes the two ingredients' separate roles legible. Flatten if you'd rather.
  - The "monoidality follows from..." closing sentence is condensed — one sentence, not a step-by-step argument. If the editorial pass wants this expanded (e.g. explicit $\beta_{V_1 \oplus V_2} = \beta_{V_1} \oplus \beta_{V_2}$), easy to do.
  - Kept the `\defineTermAs{phase_lift}{...}` term-tracking entry inside the proof. The term is still referenced downstream by the prose at line ~2601.

### Step 4 — Graduate `rmk.linear_stratum` to `prop.linear_stratum`
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:**
  - `rmk.linear_stratum` (was around line 3274, end of `sec.graph_laplacian` in `ch.applications`): replaced with a short motivation paragraph, the new `prop.linear_stratum`, its proof, and a follow-up paragraph applying the result to `conf`/`phase` and naming the wave and heat equations as instances.
  - Cross-reference in the design-space subsection: `\cref{rmk.linear_stratum}` → `\cref{prop.linear_stratum}`.
- **Content:** Proposition statement is kinematical-only — for any cotangent storage with linear anchor and update, the dynamics functor sends every $0$-ary closed system in $\srw^{\mathrm{lin}}$ to a linear endomap on the carrier $F(V)$. Symplecticity is not invoked. Proof unpacks `\eqref{eqn.bigtheta}` in the closed case to $\xi_V = Qx$, then shows the state-update is the composite of three linear maps via `prop.storage_pair`. Follow-up paragraph specializes to `conf` and `phase`, and identifies the wave equation as the `\Phiphase{}` instance and the heat equation (`rmk.graph_heat`) as the `\Phiconf{}` instance — both share superposition for the same kinematical reason.
- **Decisions / deviations:**
  - **Location.** Plan didn't specify. Considered moving to `sec.dynamics_functor`, but that would require introducing the suboperad `\srw^{\mathrm{lin}}` earlier, which is out of edit scope. Graduated in place (end of `sec.graph_laplacian`) — the wave-equation motivation stays adjacent.
  - **Plan's "iff" claim.** The plan asserts that "storage's anchor and update linear iff carrier $\sharp$ is constant linear." This is true for `conf` (carrier $\sharp = \sharpR_V$), but for `phase` the carrier is $T^*V$ with carrier $\sharp = \sharpS_{T^*V}$ (always constant linear), while what makes the update linear is constancy of the *parameter* $\sharpR_V$. The iff conflates parameter-sharp and carrier-sharp for `phase`. Resolved by stating the proposition with the cleaner direct hypothesis ("anchor and update linear") and verifying both storages satisfy it when $\sharpR_V$ is constant. No iff in the headline.
  - **Scope of the closed-system restriction.** Kept "$0$-ary closed system" per the original remark. Non-closed morphisms in $\srw^{\mathrm{lin}}$ would need a different formulation of "linear" and aren't covered.
  - **Proposition headline.** Per `feedback_short_statements`, compressed to: $\srw^{\mathrm{lin}}$ definition + the linear-endomap claim, in two sentences. Could compress further if desired.
  - **Hit a LaTeX compile error first try.** `\bk{...}{...}` macro double-subscripts unless the first argument is wrapped in extra braces. Fixed by switching `\bk{\vartheta_V}{...}` → `\bk{{\vartheta_V}}{...}` (matches existing usage on lines 2328, 2330, 2334).
- **Verified:** Build clean, 66 pages, no undefined references.

### Page-budget decision (after step 4)
- Net delta is +2 pages, exceeding the plan's "~0 to +½ page" budget. Two structural sources: (i) the new proofs verify what the old remarks waved at — separation of concerns is *shown* on the page rather than implicit; (ii) the new propositions are each invoked exactly once, so the proposition-format setup cost doesn't amortize.
- Discussed two levers: (a) collapse the Step 1 / Step 2 scaffolding in `lem.phase_storage`'s proof to a tight 4-line computation, saving ~½ page; (b) commit to the Langevin sketch in step 7 to get genuine reuse of the new propositions.
- **Decision:** keep the scaffolding (user prefers visible separation of concerns); skip Langevin (user not confident enough in the material to write it). Accept the +2 page delta as the cost of the reframing.

### Step 5 — Sharpen `rmk.constant_inverse_mass_hamiltonian` (not graduate)
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** the body of `rmk.constant_inverse_mass_hamiltonian` (around line 2628, in `sec.phase_dynamics`).
- **Content:** Opening reframed to say "the closing paragraph locates each hypothesis on its proper design-space axis." Bold-hypothesis structure preserved. Added `\label{eqn.hamiltonian}` to the $H(x,\xi)$ display so the closing paragraph can refer back to "kinetic-plus-potential" form. Closing paragraph rewritten to disentangle two roles:
  - Conservation of $H$ along the continuous flow comes from antisymmetry of the carrier sharp $\sharpS_{T^*V}$ (via `rmk.symplectic_perpendicular`) — the conservative-axis property of the design space.
  - The closed/constant/symmetric hypotheses on the $\srw$ side play a *separate* role: they supply the explicit kinetic-plus-potential form of $H$, not the conservation itself.
  - Discrete update is Euler step → does not conserve $H$ in general (cites `rmk.euler_energy`).
- **Decisions / deviations:**
  - **Sharpen, don't graduate.** Plan allowed either ("call this once we see how the proposition reads"). Chose to sharpen because:
    (a) the proposition would apply only to `phase` storage in this paper (no other antisymmetric-$\sharp$ storage), so it would be single-use like `prop.linear_stratum` with no amortization;
    (b) a clean abstract statement is hard — the "Hamiltonian reading" hypothesis essentially says "the state-update is the Euler step of a Hamiltonian vector field," which collapses the proposition into a restatement of `rmk.symplectic_perpendicular` plus the construction work that the existing remark already does;
    (c) sharpening keeps the page budget flat for this step (~26 lines in, ~26 lines out), while graduating would have added ½ page on top of the current +2.
  - Kept the remark's label `rmk.constant_inverse_mass_hamiltonian` so the four existing citations (introduction line 545; kinetic 1-form definition line 1922; design-space subsection line 2341; `rmk.euler_energy` line 2657) continue to resolve.
  - Kept the title "Hamilton's equations in the constant symmetric case" — accurate; the axis-framing lives in the body.
  - Renamed "the sharp" → "the parameter sharp" in the bold-hypothesis labels to disambiguate from the carrier sharp once the design-space framing is in scope.
- **Verified:** Build clean, 66 pages, no undefined references. Net page delta unchanged (still +2). _(Updated by step 6.)_

### Step 6 — Tighten `rmk.cotangent_learners` and `rmk.graph_heat` with design-space coordinates
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:**
  - `rmk.cotangent_learners` (around line 2384, in `sec.cotangent_storages`): appended one sentence — "This places gradient descent at the *dissipative* corner of the design space (\cref{sec.cotangent_storages}): $\store{\conf}$ with constant symmetric $\sharpR_V$."
  - `rmk.graph_heat` (around line 3266, end of `sec.graph_laplacian`): added a title "[Heat equation as the dissipative-corner instance]" and rewrote the closing sentence as a design-space corollary that explicitly names the heat equation as the dissipative-corner instance vs the wave equation as the conservative-corner instance. Kept the explicit heat-equation computation (concrete value to the reader).
- **Decisions / deviations:**
  - Plan suggested `rmk.graph_heat` could "become a one-sentence corollary." Chose to keep the explicit computation — readers benefit from seeing the heat equation on the page, and the page-budget conversation already settled. Only reframed the closing sentence as a corner-naming corollary.
  - Slight imprecision (carried over from step 1): the design-space subsection says "symmetric positive-definite ⇒ gradient descent," which is loose — descent comes from negative-definite (or pos-def with the conventional minus sign). The `rmk.cotangent_learners` body already discusses the minus sign, so the new sentence just says "symmetric" without re-litigating signs. Editorial pass could tighten step 1's bullet if you want strict signs.
  - Added a title to `rmk.graph_heat`, which previously had only a label. Matches conventions of other remarks in this section.
- **Verified:** Build clean, 66 pages, no undefined references. Net page delta unchanged (still +2).

### Step 7 — Langevin sketch
- **Skipped per user direction** (not confident enough in the material). Page-budget conversation made this an explicit call; logged earlier in "Page-budget decision."

### Step 8 — Update intro chapter sentence
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** intro paragraph around line 545 (just before the "self-contained" paragraph).
- **Content:** Appended one sentence after the existing "changing the storage takes us from energy conservation semantics to energy dissipation semantics" closing: "Configuration and phase are two named points in a small design space of cotangent storages (\cref{sec.cotangent_storages}), whose axes --- constancy, antisymmetry, and symmetric positive-definiteness of the carrier's reactive structure --- are independently responsible for superposition, energy conservation, and gradient descent."
- **Decisions / deviations:**
  - Minimal-touch interpretation of the plan's "sentence updating the design-space framing." Did not rewrite the surrounding paragraph; just added a single forward-pointing sentence.
  - Did not touch the abstract or other intro-level prose.

### Step 9 — Rebuild and cross-reference sweep
- Ran `pdflatex` twice to settle cross-refs. Both passes clean, 66 pages, no undefined references.
- Verified no stale labels remain: `rmk.linear_stratum` and `rmk.phase_lift` are both absent from the file (as intended).
- Verified the four labels created in the rewrite all resolve: `prop.linear_stratum`, `eqn.hamiltonian`, `eqn.phase_lift_decomp` (relocated into `lem.phase_storage`'s proof), and the `\defineTermAs{phase_lift}` term-tracking entry.
- Verified all `\cref{...}` and `\eqref{...}` calls in the document resolve to some `\label{...}`, `\defineTerm{...}`, `\defineTermAs{...}`, or `\trackTerm{...}` definition.

## Final state

- **Total page delta:** +2 (64 → 66).
- **Labels removed:** `rmk.linear_stratum`, `rmk.phase_lift`.
- **Labels added:** `prop.linear_stratum`, `eqn.hamiltonian`.
- **Labels kept (with content rewritten):** `lem.phase_storage` (proof), `rmk.constant_inverse_mass_hamiltonian` (body), `rmk.graph_heat` (closing + title), `rmk.cotangent_learners` (closing).
- **Labels kept unchanged:** `eqn.phase_lift_decomp` (moved into the lemma's proof; equation label preserved), `phase_lift` term-definition (now inside the proof).
- **Sections touched:** `sec.cotangent_storages` (design-space subsection, lemma proof, conf-learners remark), `sec.phase_dynamics` (one back-reference, the Hamiltonian remark body), `sec.graph_laplacian` (linear-stratum proposition, heat-equation remark), `ch.background` (kinetic-1-form back-reference), intro chapter (one sentence).
- **Choices that asymmetrically split the design-space picture:** `prop.linear_stratum` (kinematical axis) was graduated to a proposition; `rmk.constant_inverse_mass_hamiltonian` (conservative axis) was sharpened as a remark, not graduated. The asymmetry was deliberate (single-use propositions don't amortize, the Hamiltonian-reading hypothesis is hard to abstract cleanly) and is logged at step 5. Easy to flip either direction on the editorial pass.
- **Known minor imprecision flagged for the editorial pass:** design-space subsection's "symmetric positive-definite ⇒ gradient descent" elides the sign convention (descent really needs negative-definite, or pos-def with a conventional minus sign).

### Step 10 — Split `lem.phase_storage` (post-rewrite refactor)
- **Files:** `dynamic-algebra-potentials.tex`.
- **Trigger:** user noted the verbose `lem.phase_storage` proof was awkward; suggested splitting into composite-form lemma + pair-form proposition with a discussion paragraph between them.
- **Touched:**
  - Replaced the verbose `lem.phase_storage` + proof (~46 lines) with:
    - A paragraph defining $\lambda_V$ (the phase lift) above the lemma, with `\eqref{eqn.phase_lift_decomp}` retained.
    - A new compact `lem.phase_storage` that defines $\rho_V \coloneqq \lambda_V \circ \theta_{T^*V}$ in `\eqref{eqn.phase_storage_def}` (new label) and asserts it is a storage. Proof is now just the naturality + monoidality argument (~3 lines).
    - A short discussion paragraph between the lemma and proposition, naming each factor's role: $\theta_{T^*V}$ uses the antisymmetric carrier sharp $\sharpS_{T^*V}$ (conservative-axis); $\lambda_V$ uses the parameter sharp $\sharpR_V$ via $\beta_V$ (kinetic drift).
    - A new `prop.phase_storage_pair` stating the pair-form anchor and update in `\eqref{eqn.phase_storage_update}` (label preserved).
    - A 4-line proof that gestures at the chase through $\lambda_V$ then $\theta_{T^*V}$, citing the four key equations (`eqn.kinetic_one_form`, `eqn.phase_lift_decomp`, `eqn.directions_sharp`, `eqn.canonical_sharp`) and relying on the reader to verify.
  - Updated two back-references: line 1917 (kinetic-1-form's "second packaging") now points at `\eqref{eqn.phase_lift_decomp}` directly; line 2606 (the three-pieces breakdown after `eqn.state_update`) likewise.
- **Decisions / deviations:**
  - This step wasn't in the original plan — it came from the user noticing the verbose proof was a problem after the page-budget conversation. The split is the user's suggested structure.
  - Kept `eqn.phase_storage_update`'s label even though it moved from the lemma to the new proposition — all four downstream citations (lines 2530, 2604, 3273) resolve unchanged.
  - Kept `lem.phase_storage`'s label even though its content is now narrower (storage existence only, no pair-form) — two downstream citations (lines 2344, 2346) read sensibly with the narrower content.
  - The new proposition's proof is deliberately terse: it states the chase, names the key equations, and stops. Per user direction: "calls a few lines and relies on readers to do the rest of the calculation."
  - Term-tracking entries (`\defineTermAs{phase_lift}`, `\defineTermAs{phase_space_storage}`, `\defineTerm{rho}`) all preserved.
- **Verified:** Build clean (two passes), 65 pages (was 66 — split saved a page). No undefined references.

## Updated final state (after step 10)
- **Total page delta:** +1 (64 → 65).
- **Labels added (cumulative):** `prop.linear_stratum`, `eqn.hamiltonian`, `eqn.phase_storage_def`, `prop.phase_storage_pair`.
- **Labels removed (cumulative):** `rmk.linear_stratum`, `rmk.phase_lift`.
