# Critical linearization integration plan

*Companion to `srw-lin-plan.md`, which closed out at step 11 with `\srw^{\lin}\subset\srw` graduated to a named regime. This plan brings the standalone draft `critical-linearization.tex` into the main paper, with two structural upgrades applied to the draft before insertion: a Para-decomposed presentation of $J^2$, and promotion from operad functor to symmetric monoidal functor.*

## Goal

Add an end-of-`ch.potential_driven_dynamics` section formalizing Taylor linearization at critical operating points. The construction delivers:

1. An operad $\srw_*$ of *pointed* smooth rewiring diagrams (operating-point data on each interface + parameter + external input, with lens-compatibility).
2. A sub-operad $\srw_{\crit}\subseteq\srw_*$ cut out by the criticality property $dU|_z=0$.
3. A symmetric monoidal functor $J^2\colon\srw_{\crit}\to\srw^{\lin}$ given by tangent-and-Hessian.
4. A retract $J^2\circ\iota=\id_{\srw^{\lin}}$ via zero-pointing.

This upgrades the role of $\srw^{\lin}$ in the design-space picture: it is not just "the regime in which the wave and heat examples happen to live," it is the canonical second-order Taylor target of any critically-pointed smooth system.

## Operating principle

**Same as the $\srw^{\lin}$ rewrite: clean, clarify, abstract, carve at joints.** The standalone draft `critical-linearization.tex` defines $\srw_*$, $\srw_{\crit}$, and $J^2$ by hand. Before inserting, refactor along the Para joint that already governs $\srw=\para{\rvect}{\plmfd}$. The pointed/critical/Taylor structure decomposes cleanly into pointed/critical/Taylor structure on each side, combined via `prop.para_square`. This:

- absorbs the file's awkward parenthetical ("if $\sharpR_V$ is not constant, take its value at $v$") into a clean side-functor $J^2_{\rvect}$;
- collapses the compatibility conditions of `def.srw_pointed` into ordinary basepoint preservation of lens maps;
- removes a hand-built composition argument (the file's `prop.srw_crit_suboperad` proof) in favor of Para closure;
- lets $J^2$ be stated and proved as a strong symmetric monoidal functor (not just an operad functor).

## The clean refactoring

The file's $\srw_*$ has objects pointed lens interfaces $(\lensob M, m)$ and morphisms pointed multimorphisms $(f,z)$ with compatibility $\outp f(v,\outp m)=\outp n$, $\inpt f(v,\outp m,\inpt n)=\inpt m$. These are *exactly* basepoint preservation when we pass to pointed versions of each Para factor:

> **Definition** (pointed reactive vector spaces). $\rvect_*$ has objects $(V,\sharpR_V,v_0)$ with $(V,\sharpR_V)\in\rvect$ and a chosen basepoint $v_0\in V$ (generally $\ne 0$). Morphisms $(V,v_0)\to(V',v'_0)$ are $\rvect$-isomorphisms $u$ with $u(v_0)=v'_0$. SMC structure: $(V,v_0)\oplus(W,w_0)=(V\oplus W,(v_0,w_0))$, unit $(0,0)$.

> **Definition** (pointed potentialized manifold lenses). $\plmfd_*$ has objects $\lensob M$ together with basepoints $(\outp m_0,\inpt m_0)\in\outp M\times\inpt M$, and morphisms $\plmfd$-morphisms $(\outp f,\inpt f,U)\colon\lensob M_*\to\lensob N_*$ satisfying $\outp f(\outp m_0)=\outp n_0$, $\inpt f(\outp m_0,\inpt n_0)=\inpt m_0$, and $U(\outp m_0,\inpt n_0)=0$. (The last is forced by reading $\rr$ as pointed at $0$; potentials only enter the dynamics via $dU$, so this is a free normalization.)

> **Definition** (critical pointed lenses). $\plmfd_*^{\crit}\subseteq\plmfd_*$ asks additionally $dU|_{(\outp m_0,\inpt n_0)}=0$.

> **Definition** (pointed smooth rewiring). $\srw_*$ is the underlying operad of $\para{\rvect_*}{\plmfd_*}$, where the action of `lem.parameter_lens_action` lifts: the action object $\binom{\inpt X}{V\times\outp X}$ inherits basepoint $(v_0,\outp x_0)$ on the output side; the compatibility of `def.srw_pointed` is then exactly basepoint preservation of the lens components after the action.

> **Definition** (critical smooth rewiring). $\srw_{\crit}\coloneqq$ underlying operad of $\para{\rvect_*}{\plmfd_*^{\crit}}$.

The file's `def.srw_pointed`, `prop.srw_pointed_operad`, `def.srw_crit`, `prop.srw_crit_suboperad` all collapse to: $\rvect_*$ and $\plmfd_*$ (resp. $\plmfd_*^{\crit}$) are SMCs, and the action restricts. Closure under operadic composition becomes automatic from Para's machinery (no hand-built composition argument).

### The Taylor functor as Para of side-functors

> **Definition** ($J^2_{\rvect}$). $J^2_{\rvect}\colon\rvect_*\to\rvect^{\cnst}$ sends $(V,\sharpR_V,v_0)\mapsto(V,\sharpR_{v_0})$ — evaluate the sharp section at the basepoint to obtain a constant sharp. Strong monoidal: $(\sharpR_V\oplus\sharpR_W)_{(v_0,w_0)}=\sharpR_{v_0}\oplus\sharpR_{w_0}$.

> **Definition** ($J^2_{\plmfd}$). $J^2_{\plmfd}\colon\plmfd_*^{\crit}\to\plmfd^{\lin}$ sends:
> - $\lensob{M_*}\mapsto\binom{T_{\inpt m_0}\inpt M}{T_{\outp m_0}\outp M}$.
> - $(\outp f,\inpt f,U)\mapsto(T\outp f,T\inpt f,\tfrac12 d^2U|_{(\outp m_0,\inpt n_0)})$.

Strong monoidal: $T$ preserves products on pointed manifolds; Hessian on a product is direct sum of Hessians. Composition preservation uses the criticality condition $dU|_{\text{base}}=0$, which kills the $d^2a\cdot dU$ contamination terms in the Hessian chain rule (this is the file's existing argument).

> **Definition / theorem** ($J^2$). The action square for $J^2_{\rvect}$ and $J^2_{\plmfd}$ commutes via the canonical isomorphism $T_{v_0}V\cong V$ (translation-invariance of $TV$). Applying `prop.para_square` with this canonical 2-cell yields a strong symmetric monoidal functor $J^2\colon\srw_{\crit}\to\srw^{\lin}$.

The parenthetical "if $\sharpR_V$ is not constant, take its value at $v$" in the file's `def.taylor_critical` disappears: it's exactly what $J^2_{\rvect}$ does.

### The retract

> **Corollary**. Zero-pointing $\iota\colon\srw^{\lin}\to\srw_{\crit}$ — point every $\srw^{\lin}$-multimorphism at $(0,0,0)$ — lands in $\srw_{\crit}$ (basepoint compatibility automatic from linearity; criticality automatic since $dU|_0=0$ for pure quadratic $U$). Then $J^2\circ\iota=\id_{\srw^{\lin}}$: $T_0L=L$ for linear $L$; $\tfrac12 d^2U|_0=U$ for pure quadratic $U$.

This corollary is the precise sense in which $\srw^{\lin}$ is "the" Taylor target — not just one possible target.

### What makes it clean

- **Two new joints, parallel to $\rvect^{\cnst}$/$\plmfd^{\lin}$.** "Pointing the parameter side" ($\rvect_*$) and "pointing-plus-critical on the lens-and-potential side" ($\plmfd_*^{\crit}$) are independent concepts; Para combines them. Same shape as the $\srw^{\lin}$ definition.
- **Para inherits all the structural goods.** Operad structure, SMC structure, identities, monoidal product, composition closure — all from Para once the side-SMCs are checked.
- **`prop.para_square` does the heavy lifting for $J^2$.** Same proposition that gave `thm.srw_lin_suboperad` (the embedding $\srw^{\lin}\hookrightarrow\srw$); here it gives the linearization functor $J^2\colon\srw_{\crit}\to\srw^{\lin}$.
- **The retract becomes a one-line corollary** rather than a separate construction.

## Categorical scope decisions (made deliberately)

1. **Promote to SMC, not just operad functor.** The file states $J^2$ as an operad functor. The Para decomposition lives at the SMC level, so the SMC statement is cleaner and matches the existing $\srw^{\lin}\hookrightarrow\srw$ framing.

2. **Do not abstract jet bundles as a category.** $J^2$ is named for "2-jet" but the paper does not develop jet bundles. The notation is suggestive only.

## Notational conventions

One new macro:

```latex
\newcommand{\crit}{\mathrm{crit}}    % critical-stratum marker
```

Add immediately after `\newcommand{\cnst}{\mathrm{cnst}}` (line 425).

Subscript-$*$ for pointed: $\rvect_*$, $\plmfd_*$, $\srw_*$. No macro — direct `_*` in source. Matches the precedent that `\lin` and `\cnst` are minor regime markers, not tracked terms.

$J^2$ written inline (no macro). The "2" is suggestive of the jet-bundle convention.

Variable conventions:
- $v_0\in V$, $\outp m_0\in\outp M$, $\inpt m_0\in\inpt M$ for basepoints. The file uses unsubscripted $v$, $\outp m$, $\inpt m$; switch to subscript-0 to disambiguate from generic elements (the basepoint is a distinguished choice, the generic element a variable).
- $z = (v_0, \outp m_0, \inpt n_0)$ for the composite operating point on the action's lens side. Match the file's $z$.
- $\delta z$ for tangent vector at $z$, matching the file.

`\defineTermAs` anchors for: **pointed smooth rewiring diagram**, **critical smooth rewiring diagram**.

## Section-by-section changes

### `sec.forming_potlens` — leave alone

No edits. The $\srw^{\lin}$ cluster stays where it is. The new $\rvect_*$, $\plmfd_*$, $\plmfd_*^{\crit}$ definitions live in the new section, not here. Rationale: the pointed/critical machinery is Taylor-section-specific and would bulk up `sec.forming_potlens` unnecessarily.

### New section `sec.critical_linearization` at end of `ch.potential_driven_dynamics`

Insert immediately after `sec.design_space` (which currently ends at line 2925, just before `\chapter{Applications}` at line 2928). Working title: **Critical operating points and Taylor linearization**.

Two subsections matching the file:

**Subsection 1: Pointed and critical smooth rewiring diagrams** (`sec.srw_pointed`). Content, in order:

1. Opening paragraph (one paragraph): in engineering practice, one starts with a smooth system, picks an operating point, linearizes. This section records that the linearization step is itself operad-functorial. Roadmap: pointed operad → critical sub-operad → Taylor functor → retract corollary.

2. `def.rvect_pointed`: $\rvect_*$ as objects-with-basepoint. One-line remark inlining the sub-SMC check (basepoints stay basepoints under $\oplus$).

3. `def.plmfd_pointed`: $\plmfd_*$ via basepoint-preserving morphisms. State as pointed manifolds in $\plmfd$'s coKleisli setup with $\rr$ pointed at $0$.

4. Short lemma (or inline): $\plmfd_*$ is a sub-SMC of $\plmfd$ (basepoint preservation closed under identity, composition, monoidal product — all transparent).

5. Short lemma (or inline): the action $\rvect\times\plmfd\to\plmfd$ of `lem.parameter_lens_action` restricts to $\rvect_*\times\plmfd_*\to\plmfd_*$. The output basepoint of the action object $\binom{\inpt X}{V\times\outp X}$ is $(v_0,\outp x_0)$; the lens components of the action morphism preserve basepoints by inspection.

6. `def.srw_pointed`: $\srw_*\coloneqq$ underlying operad of $\para{\rvect_*}{\plmfd_*}$. **One-paragraph unpacking** explicating that this means a multimorphism in $\srw_*$ is exactly the file's `def.srw_pointed` data — basepoint preservation gives the compatibility conditions $\outp f(v_0,\outp m_0)=\outp n_0$ and $\inpt f(v_0,\outp m_0,\inpt n_0)=\inpt m_0$. This unpacking is the bridge from the abstract Para definition to the concrete operating-point picture; do not skip it. Use `\defineTermAs{pointed_srw_diagram}{...}` here.

7. `def.plmfd_critical`: $\plmfd_*^{\crit}\subseteq\plmfd_*$ adds $dU|_{(\outp m_0,\inpt n_0)}=0$. Short lemma: this is closed under composition (use the coKleisli composition formula and the criticality vanishing argument as in `lem.plmfd_lin_smc`).

8. `def.srw_critical`: $\srw_{\crit}\coloneqq$ underlying operad of $\para{\rvect_*}{\plmfd_*^{\crit}}$. Use `\defineTermAs{critical_srw_diagram}{...}`.

9. `rmk.full_vs_storage_critical`: criticality is stronger than storage-dependent equilibrium. Direct port from the file (lines 82-84). Recast slightly: now framed against `prop.storage_pair` rather than the file's standalone framing.

**Subsection 2: The Taylor functor $J^2$** (`sec.taylor_critical`). Content, in order:

10. `def.J2_rvect`: $J^2_{\rvect}\colon\rvect_*\to\rvect^{\cnst}$. Short lemma `lem.J2_rvect_smc`: strong symmetric monoidal.

11. `def.J2_plmfd`: $J^2_{\plmfd}\colon\plmfd_*^{\crit}\to\plmfd^{\lin}$. Short lemma `lem.J2_plmfd_smc`: strong symmetric monoidal. The proof packages the file's existing argument (tangent on lens components, Hessian on potential, criticality kills the $d^2a\cdot dU$ contamination terms).

12. `lem.J2_action_compatible`: the action square of $J^2_{\rvect}$ and $J^2_{\plmfd}$ commutes via the canonical $T_{v_0}V\cong V$. One-paragraph proof: tangent of a vector space at any point is canonically the vector space itself (translation invariance); under this identification, $J^2_{\rvect}(V)\cdot J^2_{\plmfd}(\lensob{X_*}) = \binom{T\inpt X}{V\times T\outp X} = J^2_{\plmfd}(V\cdot\lensob{X_*})$.

13. `thm.taylor_critical_functor`: applying `prop.para_square` to $J^2_{\rvect}$, $J^2_{\plmfd}$, with 2-cell the canonical iso from `lem.J2_action_compatible`, yields a strong symmetric monoidal functor $J^2\colon\srw_{\crit}\to\srw^{\lin}$. **State as SMC functor**, not just operad functor.

14. `cor.taylor_retract`: zero-pointing $\iota\colon\srw^{\lin}\to\srw_{\crit}$ satisfies $J^2\circ\iota=\id$. Two-sentence proof: criticality at zero is automatic for pure quadratic $U$ (gradient vanishes at the origin) and linear lens (basepoints all zero); under $J^2$, linear maps are their own tangent maps, pure quadratics are their own Hessian/2.

15. `rmk.srw_lin_taylor_target`: $\srw^{\lin}$ as canonical second-order Taylor target. Direct port from the file (lines 138-144), light edits to mention the retract corollary.

16. **New example: Newton's method as a $\srw_{\crit}$-scalar.** Worth roughly half a page. State as a separate `\paragraph` or short `example` environment at the end of subsection 2. The Newton scalar of `sec.newton_warmup` has parameter sharp $\sharpR_v=-(d^2\ell|_v)^{-1}$ (non-constant!) and potential $\ell$ (non-quadratic), so sits in $\srw$ but not in $\srw^{\lin}$. Point it at a critical $v^*$ of $\ell$ to land in $\srw_{\crit}$. Then $J^2$ gives the scalar with parameter sharp $-(d^2\ell|_{v^*})^{-1}$ (constant — inverse Hessian at $v^*$) and potential $\tfrac12 d^2\ell|_{v^*}$ (pure quadratic). Under $\Phiconf{}$: $v\mapsto v+\sharpR(dU|_v)=v-(d^2\ell|_{v^*})^{-1}d^2\ell|_{v^*}(v-v^*)=v^*$. **One step to the fixed point** — the categorical articulation of "Newton's method is exact on the quadratic Taylor approximation."

### `sec.design_space` — add one cross-reference

Cross-reference the new section. Suggested placement: after the closing paragraph of `sec.design_space` (around line 2874), add one sentence: "The kinematical regime $\srw^{\lin}$ is more than the home of the wave and heat examples — it is the canonical second-order Taylor target of any critically-pointed smooth system in $\srw$; see \cref{sec.critical_linearization}."

### Intro paragraph (line 548) — light sharpening

Current closing sentence: "We name the syntactic regime where the superposition axis lives the *linear stratum* $\srw^{\lin}\subset\srw$ (\cref{def.srw_lin})."

Proposed update: "We name the syntactic regime where the superposition axis lives the *linear stratum* $\srw^{\lin}\subset\srw$ (\cref{def.srw_lin}); it is also the canonical second-order Taylor target of any critically-pointed smooth system (\cref{sec.critical_linearization})."

Single sentence add, maintains the existing rhetorical register.

### `sec.newton_warmup` — leave alone (or add one pointer sentence)

The Newton's method example lives in the new section. `sec.newton_warmup` itself stays in `ch.applications` unchanged. Optional: at the end of `sec.newton_warmup`, add one sentence: "The relation of this scalar to the linear stratum is taken up in \cref{sec.critical_linearization}." Decision: leave alone unless the editorial pass calls for it.

### `sec.wave_equation`, `sec.graph_laplacian` — leave alone

The examples there are in $\srw^{\lin}$ on the nose (via the existing tags from the $\srw^{\lin}$ rewrite). The Taylor framework would let one present a chain of *nonlinear* oscillators in the small-oscillation regime, but that example is out of scope here. No edits.

## Order of operations

1. **Add macro** (`\crit`) in the preamble.

2. **Build the pointed/critical cluster** in the new section: `def.rvect_pointed`, `def.plmfd_pointed`, action restriction, `def.srw_pointed` with the Para-to-compatibility unpacking paragraph, `def.plmfd_critical`, `def.srw_critical`, `rmk.full_vs_storage_critical`. Build, verify the cluster compiles, no undefined refs. Verify the `\defineTermAs` anchors land.

3. **Build the Taylor functor cluster**: `def.J2_rvect` + `lem.J2_rvect_smc`; `def.J2_plmfd` + `lem.J2_plmfd_smc`; `lem.J2_action_compatible`; `thm.taylor_critical_functor`; `cor.taylor_retract`; `rmk.srw_lin_taylor_target`. Build.

4. **Add the Newton's method example** at the end of subsection 2. Build.

5. **Cross-reference into `sec.design_space`**: one sentence at the closing paragraph.

6. **Intro paragraph update** at line 548.

7. **Build twice; cross-reference sweep.** All new labels resolve (`sec.critical_linearization`, `sec.srw_pointed`, `sec.taylor_critical`, `def.rvect_pointed`, `def.plmfd_pointed`, `def.plmfd_critical`, `def.srw_pointed`, `def.srw_critical`, `def.J2_rvect`, `def.J2_plmfd`, `lem.J2_rvect_smc`, `lem.J2_plmfd_smc`, `lem.J2_action_compatible`, `thm.taylor_critical_functor`, `cor.taylor_retract`, `rmk.full_vs_storage_critical`, `rmk.srw_lin_taylor_target`, and the `pointed_srw_diagram`, `critical_srw_diagram` term anchors).

## Risks and uncertainties

1. **Page count estimate: +2½ to +3.** The pointed/critical cluster is lighter than the $\srw^{\lin}$ cluster (no SMC closure proof for $\rvect_*$ — basepoints are trivially closed; less elaborate Para-square setup). The Taylor cluster is comparable. Newton's method example adds half a page. Total likely in the +2.5 range. If it stretches past +3, the Newton example is the place to compress.

2. **The Hessian chain rule.** The proof of `lem.J2_plmfd_smc`'s composition closure uses the Hessian chain rule, which is non-trivial calculus. The file's existing proof is fine but heavy. Consider whether to (a) include the full chain-rule computation, (b) cite a standard reference, or (c) sketch and refer to differential-geometry tradition. Probably (b) or (c) — the paper's calculus content is otherwise light. **Decision deferred to editorial pass.**

3. **Canonical iso $T_{v_0}V\cong V$.** Translation-invariance of the tangent bundle of a vector space. Standard but worth stating explicitly when invoked in `lem.J2_action_compatible`. One sentence; do not belabor.

4. **The "potential vanishes at basepoint" normalization.** $\plmfd_*$ asks $U(\outp m_0,\inpt n_0)=0$, automatic if $\rr$ is pointed at $0$. Worth a one-line remark in `def.plmfd_pointed`'s body: "Since the dynamics functor only sees $dU$, this normalization is free." This forestalls any reader confusion about why we can freely demand it.

5. **The pointed-manifold conventions.** $\mfd_*$ is the category of pointed manifolds and pointed smooth maps. The paper does not currently use this category; the new section introduces it implicitly when defining $\plmfd_*$. Decision: just use the conventions inline (basepoints preserved, $\rr_*=(\rr,0)$) without naming $\mfd_*$ as a category in its own right. **Minimal footprint.**

6. **Wording of `def.srw_pointed`'s unpacking paragraph.** This is the bridge from abstract Para definition to concrete operating-point picture; it has to read clearly for a reader who hasn't done the Para algebra themselves. Allocate care here. Draft and surface for review if it lands awkwardly.

7. **Newton's method example placement.** Currently planned at end of subsection 2. Alternative: as a standalone subsection. Decision: keep at end of subsection 2 as a `\paragraph` block or `example` environment — the example is short and reads as payoff, not as a standalone topic.

## Estimated effort

1 day. The cluster has fewer load-bearing lemmas than the $\srw^{\lin}$ rewrite (which took ~2 days). The Para infrastructure is already in place and tested; the new content is mostly the side-SMC definitions plus one application of `prop.para_square`. Newton's example is half a page of explicit calculation.

## What this rewrite is *not*

- **Not** introducing $\mfd_*$ as a category in its own right (used implicitly).
- **Not** abstracting "2-jet" to a category of jets.
- **Not** developing the dynamical consequences ($J^2$-then-$\Phi$ gives small-oscillation / linear-response dynamics) beyond a one-sentence mention in `rmk.srw_lin_taylor_target`.
- **Not** introducing examples beyond Newton's method. The chain of nonlinear oscillators near equilibrium is the natural physics example but is out of scope.
- **Not** revisiting `sec.newton_warmup`'s presentation. Newton's method stays as currently defined in `ch.applications`; the new section *references* it.

## Handoff notes (read before starting)

**Line numbers in this plan are approximate.** Grep for the label or term, don't trust the integer. Labels are stable.

**Label slugs to use** (kebab-case, matching paper conventions):

| Slug | What | Step |
|---|---|---|
| `sec.critical_linearization` | New section | 2 |
| `sec.srw_pointed` | Subsection 1 | 2 |
| `sec.taylor_critical` | Subsection 2 | 3 |
| `def.rvect_pointed` | $\rvect_*$ | 2 |
| `def.plmfd_pointed` | $\plmfd_*$ | 2 |
| `def.plmfd_critical` | $\plmfd_*^{\crit}$ | 2 |
| `def.srw_pointed` | $\srw_*$ | 2 |
| `def.srw_critical` | $\srw_{\crit}$ | 2 |
| `def.J2_rvect` | $J^2_{\rvect}$ | 3 |
| `def.J2_plmfd` | $J^2_{\plmfd}$ | 3 |
| `lem.J2_rvect_smc` | $J^2_{\rvect}$ strong monoidal | 3 |
| `lem.J2_plmfd_smc` | $J^2_{\plmfd}$ strong monoidal | 3 |
| `lem.J2_action_compatible` | Action square | 3 |
| `thm.taylor_critical_functor` | $J^2$ as SMC functor | 3 |
| `cor.taylor_retract` | $J^2\circ\iota=\id$ | 3 |
| `rmk.full_vs_storage_critical` | Criticality vs equilibrium | 2 |
| `rmk.srw_lin_taylor_target` | $\srw^{\lin}$ as Taylor target | 3 |
| `pointed_srw_diagram` | `\defineTermAs` anchor | 2 |
| `critical_srw_diagram` | `\defineTermAs` anchor | 2 |

**The standalone `critical-linearization.tex` is the source.** Read it first. It contains the existing presentation (`def.srw_pointed`, `prop.srw_pointed_operad`, `def.srw_crit`, `prop.srw_crit_suboperad`, `rmk.full_vs_storage_critical`, `def.taylor_critical`, `thm.taylor_critical_functor`, `rmk.srw_lin_taylor_target`). The plan refactors that content into the Para-decomposed form; do **not** copy the file verbatim. Use the file's prose where it survives the refactoring (the opening paragraph, `rmk.full_vs_storage_critical`, `rmk.srw_lin_taylor_target` — these stay close to as-written).

**The Para refactoring is the load-bearing change.** Before writing, read:
- `sec.forming_potlens` lines 2110–2208 (the $\srw^{\lin}$ cluster) — same pattern.
- `lem.parameter_lens_action` (line 1533) — defines the action being lifted.
- `prop.para_square` (line 1155) — the engine for $J^2$.

The proof of `thm.srw_lin_suboperad` (line 2190) is the closest existing template — `thm.taylor_critical_functor`'s proof will look similar in shape, but with non-identity 2-cell (the canonical $T_{v_0}V\cong V$) instead of $\theta=\id$.

**Build after every step**, not just the final one. Use the pdflatex+biber recipe in `reference_build.md` (auto-memory).

**Judgment calls to surface, not decide unilaterally:**

- **`rmk.full_vs_storage_critical`'s wording.** The file's version is good but was written against a standalone framing; the in-paper version should reference `prop.storage_pair` for the anchor/update language. Draft once; surface if it lands awkwardly.
- **Newton's example length.** Draft at ~half a page; if it bloats, cut the explicit one-step-convergence calculation and just state the result with one-sentence justification.
- **Whether to include a forward pointer from `sec.newton_warmup`.** Plan says leave alone unless editorial pass calls for it. If the Newton example in the new section reads as ungrounded without a backward link to `sec.newton_warmup`, propose adding the pointer.
- **Wording of the Para-to-compatibility unpacking paragraph in `def.srw_pointed`.** This is the critical reader-bridge. Draft and surface for review.

**Downstream-citation check at final step:** the intro paragraph update at line 548 adds a `\cref{sec.critical_linearization}`. Verify it resolves after the new section is in place. The `sec.design_space` cross-reference at line ~2874 similarly. No other downstream citations expected; the new section is end-of-chapter and not yet referenced elsewhere.

---

## Edit log (running memory)

Format: each entry covers one session-step. Lists files/locations touched, deviations from the plan, and editorial decisions worth flagging for the editorial pass.

### Step 1 — Macro
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** Preamble (after `\cnst` at line 425): added `\newcommand{\crit}{\mathrm{crit}}`.
- **Verified:** Build clean, 68 pages, unchanged from baseline (macro not yet used).

### Step 2 — Pointed/critical cluster
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** Inserted new `\section{Critical operating points and Taylor linearization}\label{sec.critical_linearization}` between the closing `\end{remark}` of `rmk.cotangent_learners` (around old line 2926) and `\chapter{Applications}`.
- **Content (subsection 1, `sec.srw_pointed`):**
  - Two opening paragraphs for the section (first frames the engineering rationale, second locates the Para decomposition and the consequence for the design-space picture).
  - One short opening sentence for the subsection.
  - `def.rvect_pointed` + companion paragraph noting closure under $\oplus$ and that the forgetful is strict symmetric monoidal.
  - `def.plmfd_pointed` with three compatibility conditions `\eqref{eqn.plmfd_pointed_compat}` + companion paragraph explaining $U(\outp m_0,\inpt n_0)=0$ as a free normalization (since the dynamics functor only sees $dU$ per `prop.storage_pair`).
  - `lem.plmfd_pointed_smc` (identity / composition / monoidal product), proof verifies basepoint preservation in each.
  - `lem.action_restricts_pointed` (action restricts $\rvect_*\times\plmfd_*\to\plmfd_*$).
  - `def.srw_pointed` ($\srw_*\coloneqq\para{\rvect_*}{\plmfd_*}$) with `\defineTermAs{pointed_srw_diagram}{...}` anchor.
  - **Unpacking paragraph** (the reader-bridge flagged in the plan): unfolds the Para definition against `lem.parameter_lens_action` to recover the file's `def.srw_pointed` compatibility conditions `\eqref{eqn.pointed_compatibility}`.
  - `def.plmfd_critical` (criticality `\eqref{eqn.plmfd_crit}`).
  - `lem.plmfd_critical_smc` (composition closure + action restriction folded into one lemma — see deviations).
  - `def.srw_critical` ($\srw_{\crit}\coloneqq\para{\rvect_*}{\plmfd_*^\crit}$) with `\defineTermAs{critical_srw_diagram}{...}` anchor.
  - `rmk.full_vs_storage_critical` (criticality stronger than storage-dependent equilibrium; reframed against `prop.storage_pair` and `\cref{sec.cotangent_storages}` per plan).
- **Decisions / deviations:**
  - **Three-component compatibility `\eqref{eqn.plmfd_pointed_compat}`.** Included the third condition $U(\outp m_0,\inpt n_0)=0$ as a baseline part of $\plmfd_*$ rather than as separate normalization step. Justified by the companion paragraph (dynamics only sees $dU$). Carries through to `def.srw_pointed`'s unpacking — the file's two compatibility conditions become three.
  - **Action restriction lemma kept separate from SMC closure for $\plmfd_*$, but folded into `lem.plmfd_critical_smc` for the critical case.** For the pointed case the closure proof is substantial and the action restriction is short; for the critical case both are very short, so combining saved an environment.
  - **No `def.plmfd_critical`-companion paragraph.** Reads cleanly without one given the closure lemma immediately follows.
  - **`pointed_srw_diagram` anchor placement.** Inside `def.srw_pointed`'s body sentence about multimorphisms, not in the unpacking paragraph. Matches existing `smooth_rewiring_diagram` precedent.
  - **Surfaced for review (per plan's handoff notes):**
    - *Wording of the unpacking paragraph after `def.srw_pointed`.* Drafted to bridge the abstract Para definition to the concrete operating-point picture via two bullet items and explicit equation; reads cleanly on first pass but is the load-bearing reader-bridge.
    - *`rmk.full_vs_storage_critical` wording.* Recast the file's standalone framing against `prop.storage_pair` for the equilibrium language ("the configuration-storage update of `prop.storage_pair` fixes a state $x\in V$ when..."). Close to the file's original prose otherwise.
- **Verified:** Build clean, 71 pages (+3 over baseline), no undefined references.

### Step 3 — Taylor functor cluster
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** Appended new `\subsection{The Taylor functor $J^2$}\label{sec.taylor_critical}` after `rmk.full_vs_storage_critical`, before `\chapter{Applications}`.
- **Content:** One opening sentence; `def.J2_rvect` + companion paragraph showing pairing-preservation of $u$ at the basepoint implies the constant-sharp pairing condition `\eqref{eqn.pairing_triangle}|_{x=v_0}`; `lem.J2_rvect_smc` (strong monoidal via `prop.rvect_monoidal`); `def.J2_plmfd` with tangent-and-Hessian formulas `\eqref{eqn.J2_lens}` and `\eqref{eqn.J2_pot}` + companion paragraph noting the four-condition check of `cor.srw_lin_four_conditions` lands on the lens side; `lem.J2_plmfd_smc` with identity/composition/monoidal-product structure, the composition case packaging the Hessian-chain-rule cancellation argument explicitly; `lem.J2_action_compatible`; `thm.taylor_critical_functor` (applying `prop.para_square`); `cor.taylor_retract` ($J^2\circ\iota=\id_{\srw^\lin}$ via zero-pointing); `rmk.srw_lin_taylor_target` (the design-space framing).
- **Decisions / deviations:**
  - **Build fix.** Initial draft of `rmk.srw_lin_taylor_target`'s displayed equation used `\Phi_\store{\bullet}`, which produced a double-subscript error (since `\store{X}` already carries a subscript on `\termref{store}{\termraw{store}}_{X}`). Replaced with `\Phi_{\store{\bullet}}` (extra braces).
  - **Hessian chain rule.** Per plan risk #2 ("decision deferred to editorial pass"), I included the chain-rule formula explicitly with the criticality cancellation, mirroring the file's argument. Compact but explicit. Editorial pass might prefer citing a standard reference instead — the calculus content elsewhere in the paper is light.
  - **Canonical iso $T_{v_0}V\cong V$.** Stated in `lem.J2_action_compatible` body and used in proof + corollary. One-sentence treatment per plan risk #3.
  - **`cor.taylor_retract`'s $\iota$.** Defined inline ("zero-pointing functor obtained by pointing every object at the origin..."), not as a separate definition. Could be promoted to a definition if cited downstream, but no current citations need it.
  - **No new SMC sub-categorical machinery.** $\iota$ in the corollary is described in prose; no separate `lem.iota_well_defined` or similar — the corollary's proof inlines the well-definedness check.
- **Verified:** Build clean, 73 pages (+2 over Step 2), no undefined references.

### Step 4 — Newton's example
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** Inserted `\begin{example}[Newton's method linearizes about a critical point]\label{ex.newton_critical}` immediately after `rmk.srw_lin_taylor_target`, before `\chapter{Applications}`.
- **Content:** Three paragraphs. (1) Newton scalar of `sec.newton_warmup` lies outside $\srw^\lin$ (non-constant sharp, non-quadratic potential); pointing at a critical $v^*$ and normalizing $\ell\to\tilde\ell\coloneqq\ell-\ell(v^*)$ produces an $\srw_{\crit}$-scalar. (2) $J^2$ replaces sharp by inverse Hessian at $v^*$ and potential by half-Hessian quadratic, landing in $\srw^\lin$. (3) $\Phiconf{}$ applied to the linearized scalar: one step takes any $\delta v$ to $0$, equivalently any $v$ to $v^*$.
- **Decisions / deviations:**
  - **Example environment, not `\paragraph`.** Matches the document's `ex.X` label convention and allows cross-reference if desired.
  - **Translation back from $\delta v$ to $v=v^*+\delta v$.** Spelled out as one sentence to clarify that the linearized world's state is a tangent vector at $v^*$; without this, the "$\delta v\mapsto 0$" calculation would read ambiguously.
  - **Kept the explicit one-step convergence calculation** (plan risk #2: if it bloats, cut this and just state the result). At ~half a page the example fits within the plan's budget; the calculation is short enough to keep and reads as payoff.
  - **No backward link from `sec.newton_warmup` added** (plan optional). The example reads on its own with the forward link `\cref{sec.newton_warmup}`; no urge to add a reciprocal pointer.
- **Verified:** Build clean, 74 pages (+1 over Step 3).

### Step 5 — Design-space cross-reference
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** Appended one sentence to the closing paragraph of `sec.design_space` (immediately after the "Mixed-symmetry $\sharp$..." sentence): "The kinematical regime $\srw^\lin$ is moreover more than the home of the wave and heat examples --- it is the canonical second-order Taylor target of any critically-pointed smooth system in $\srw$; see \cref{sec.critical_linearization}."
- **Verified:** Build clean.

### Step 6 — Intro paragraph update
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** Closing sentence of the intro paragraph at line 548: appended "; it is also the canonical second-order Taylor target of any critically-pointed smooth system (\cref{sec.critical_linearization})." to the existing $\srw^\lin$ definition pointer.
- **Verified:** Build clean.

### Step 7 — Rebuild and cross-reference sweep
- Ran `pdflatex` twice; both passes clean, 74 pages, no undefined references.
- **All new labels resolve in .aux:** `sec.critical_linearization`, `sec.srw_pointed`, `sec.taylor_critical`, `def.rvect_pointed`, `def.plmfd_pointed`, `def.plmfd_critical`, `def.srw_pointed`, `def.srw_critical`, `lem.plmfd_pointed_smc`, `lem.action_restricts_pointed`, `lem.plmfd_critical_smc`, `def.J2_rvect`, `def.J2_plmfd`, `lem.J2_rvect_smc`, `lem.J2_plmfd_smc`, `lem.J2_action_compatible`, `thm.taylor_critical_functor`, `cor.taylor_retract`, `rmk.full_vs_storage_critical`, `rmk.srw_lin_taylor_target`, `ex.newton_critical`.
- **`\defineTermAs` anchors added:** `pointed_srw_diagram`, `critical_srw_diagram`, `J2_rvect`, `J2_plmfd`.
- **Downstream-citation check:** intro sentence at line 548 now contains `\cref{sec.critical_linearization}` — resolves. Closing paragraph of `sec.design_space` contains the same — resolves. No other downstream citations expected; the new section is end-of-chapter and not yet referenced elsewhere.
- **No new build warnings.** The pre-existing `\qedhere` warning at line 810 (in `def.store_action`) is unrelated to this rewrite.

---

## Final state (after step 7)
- **Total page delta (this rewrite):** +6 (68 → 74). Over the plan's "+2.5 to +3" estimate. Sources of the overshoot: the pointed-side closure lemma `lem.plmfd_pointed_smc` runs longer than the plan's "short lemma or inline" because the coKleisli composition verification spans three components (`\outp`, `\inpt`, $U$); the Taylor cluster's `lem.J2_plmfd_smc` proof includes the explicit Hessian-chain-rule cancellation (plan risk #2's deferred editorial decision); the Newton example is at full ~half-page weight (kept the explicit one-step calculation). Editorial pass could trim by inlining `lem.action_restricts_pointed` and the action half of `lem.plmfd_critical_smc`, or by deferring the Hessian chain rule to a standard reference.
- **Labels added (this rewrite):** see Step 7 list above; 21 labels + 4 `\defineTermAs` anchors.
- **Labels relocated or removed:** none.
- **Preamble change:** one `\newcommand{\crit}{\mathrm{crit}}`.
- **Two pieces flagged for review (per plan handoff):**
  1. The unpacking paragraph in `def.srw_pointed` (the reader-bridge from Para to operating-point picture).
  2. The wording of `rmk.full_vs_storage_critical`, recast to reference `prop.storage_pair` and the storage of `\cref{sec.cotangent_storages}`.
