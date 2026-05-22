# $\srw^{\lin}$ promotion plan

*Companion to `rewrite-plan.md`, which closed out at step 10. This plan supersedes the design-space subsection produced in step 1 of that file and the location of `prop.linear_stratum` produced in step 4.*

## Goal

Promote $\srw^{\lin}$ from a single-use ad-hoc suboperad inside one proposition to a named syntactic regime that threads through the document. Three structural problems with the current treatment:

1. **Forward references.** The design-space subsection in `sec.cotangent_storages` (line 2337) cites `prop.linear_stratum`, which lives at the end of `sec.graph_laplacian` (line 3259) — a chapter and ~900 lines downstream.
2. **Ad-hoc introduction.** $\srw^{\lin}$ is introduced inside its only use. A reader meets the four conditions for the first time mid-proposition, with nothing to anchor them to.
3. **Suboperad asserted, not earned.** Calling $\srw^{\lin}$ a *suboperad* requires its conditions to survive operadic composition. The paper currently asserts this without checking.

## Operating principle

**Clean, clarify, abstract, carve at joints.** Graduate only when there is a real joint. Sharpen vocabulary where there is no joint but the prose can be tightened. The suboperad is now driving — what makes it clean is letting it.

---

## The clean refactoring

The current definition is four conditions joined together: (i) interfaces $\outp M,\inpt M\in\vect$, (ii) lens maps $\inpt f,\outp f$ linear, (iii) parameter $\sharpR_V$ constant, (iv) potential $U$ pure quadratic. Conditions (i), (ii), (iv) all live on the lens-and-potential side; condition (iii) lives on the parameter side. The Para structure of $\srw$ already separates those two sides:
\[
\srw \;=\; \para{\rvect}{\plmfd}.
\]
So the natural carving is to define each side's "linear part" separately and combine via the same Para construction:

> **Definition** (constant-sharp reactive vector spaces). $\rvect^{\cnst}\subseteq\rvect$ is the full sub-SMC on objects $(V,\sharpR_V)$ whose section $\sharpR_V\colon V\to(V\otimes V)^{\cong}$ is constant in $x:V$.

> **Definition** (linear potentialized manifold lenses). $\plmfd^{\lin}\subseteq\plmfd$ is the sub-SMC on objects $\lensob M$ with $\outp M,\inpt M\in\vect$ and morphisms $(\outp f,\inpt f,U)$ with $\outp f,\inpt f$ linear and $U\colon\outp M\times\inpt N\to\rr$ a pure quadratic form.

> **Definition** (linear smooth rewiring). $\srw^{\lin}$ is the underlying operad of $\para{\rvect^{\cnst}}{\plmfd^{\lin}}$, where the action of `lem.parameter_lens_action` restricts to one of $\rvect^{\cnst}$ on $\plmfd^{\lin}$.

The four conditions of the current `prop.linear_stratum` are recovered by unpacking. Closure under operadic composition becomes automatic from Para's machinery once we verify (1) $\rvect^{\cnst}$ is a sub-SMC of $\rvect$, (2) $\plmfd^{\lin}$ is a sub-SMC of $\plmfd$, and (3) the action restricts. Each of these is short.

### What makes it clean

- **Decomposed at the right joint.** "Linear on the parameter side" ($\rvect^{\cnst}$) and "linear on the lens-and-potential side" ($\plmfd^{\lin}$) are independent concepts; the Para construction combines them. Two separate joints, not a four-clause compound.
- **Inherits structure.** SMC structure, identity, composition, monoidal unit, and operadic composition all pass through Para without separate verification.
- **Same shape as $\srw$.** $\srw=\para{\rvect}{\plmfd}$, $\srw^{\lin}=\para{\rvect^{\cnst}}{\plmfd^{\lin}}$. A reader who has digested $\srw$ already understands the shape of $\srw^{\lin}$.
- **Closure shrinks to one observation.** The only nontrivial closure fact is that pure quadratic forms are closed under linear pullback and sum — packaged as one functoriality statement.

---

## Full proofs

### Lemma 1 ($\rvect^{\cnst}$ is a sub-SMC of $\rvect$).

The constant-$\sharpR$ condition is closed under the monoidal structure of `prop.rvect_monoidal`: the direct sum $\sharpR_{V\oplus W}=\sharpR_V\oplus\sharpR_W$ is constant in $(x,y):V\oplus W$ whenever $\sharpR_V$ and $\sharpR_W$ are constant in their respective points. The monoidal unit $0\in\rvect$ has unique (vacuously constant) sharp. Morphisms in $\rvect$ are $\rvect$-isomorphisms, which are inherited; fullness on objects gives the sub-SMC structure with no further checks.

### Lemma 2 (pure quadratic forms are functorial).

For a vector space $V$, write $\Sym^2(V^*)$ for the vector space of \defineTermAs{pure_quadratic_form}{\emph{pure quadratic forms}} on $V$: smooth functions $U\colon V\to\rr$ of the form $U(v)=q(v,v)$ for a symmetric bilinear $q\colon V\times V\to\rr$.

> $\Sym^2(\blank^*)\colon\vect\op\to\vect$ is a functor: a linear map $L\colon W\to V$ acts by pullback $U\mapsto U\circ L$, and the assignment is linear in $U$.

*Proof.* For $U(v)=q(v,v)$, the pullback is $(U\circ L)(w)=q(Lw,Lw)=q'(w,w)$ where $q'(w_1,w_2)\coloneqq q(Lw_1,Lw_2)$ is symmetric bilinear; this depends linearly on $U$ (i.e.\ on $q$) and contravariantly on $L$. For $U_1,U_2$ pure quadratic with bilinear data $q_1,q_2$, the sum is $(U_1+U_2)(v)=(q_1+q_2)(v,v)$ with $q_1+q_2$ symmetric bilinear, so $\Sym^2(V^*)$ is closed under sums. $\qed$

This packages both "pullback preserves pure-quadratic" and "sum preserves pure-quadratic" into one statement; both will be invoked in Lemma 3.

### Lemma 3 ($\plmfd^{\lin}$ is a sub-SMC of $\plmfd$).

We verify the three closure conditions: identity, composition, monoidal structure.

*Identity.* The identity at $\lensob M$ in $\plmfd$ is $\bigl(\id_{\outp M},\id_{\inpt M},0\bigr)$. The lens components are linear; the zero potential is pure quadratic ($q\equiv 0$).

*Composition.* Let $f\colon\lensob M\to\lensob N$ and $g\colon\lensob N\to\lensob P$ both satisfy the $\plmfd^{\lin}$ conditions. By the coKleisli composition formula in $\plmfd$ (\cref{sec.potentialized_cokleisli}), the composite $g\circ f$ has lens part
\[
\outp{g\circ f}=\outp g\circ\outp f,\qquad
\inpt{g\circ f}\colon\outp M\times\inpt P\to\inpt M,\;\;(m,p)\mapsto\inpt f\bigl(m,\,\inpt g(\outp f(m),p)\bigr),
\]
and potential
\[
U_{g\circ f}(m,p)\;=\;U_g\bigl(\outp f(m),p\bigr)+U_f\bigl(m,\,\inpt g(\outp f(m),p)\bigr),
\]
where the sum comes from the $\potd$-monoid multiplication $\mu=(+)$ on the backward $\rr$-channel.

Linearity of $\outp{g\circ f}$ and $\inpt{g\circ f}$: composites of linear maps. The first argument of $U_g$ is $(\outp f(m),p)$, linear in $(m,p)$; the second argument of $U_f$ is $\bigl(m,\inpt g(\outp f(m),p)\bigr)$, also linear in $(m,p)$. By Lemma 2, pullback of pure quadratic by linear is pure quadratic and sums of pure quadratics are pure quadratic, so $U_{g\circ f}$ is pure quadratic.

*Monoidal structure.* The symmetric monoidal structure on $\plmfd$ is induced from $(\mfd,\times)$ by `lem.cot_lifts_lens_potential` and `lem.parameter_lens_action`; on objects, it acts by $\lensob{M_1}\otimes\lensob{M_2}=\lensob{M_1\times M_2}=\binom{\inpt{M_1}\times\inpt{M_2}}{\outp{M_1}\times\outp{M_2}}$, which preserves vector-space interfaces. On morphisms, the monoidal product of $(\outp f_1,\inpt f_1,U_1)$ and $(\outp f_2,\inpt f_2,U_2)$ has lens components $\outp{f_1}\times\outp{f_2}$ and $\inpt{f_1}\times\inpt{f_2}$ (linear-on-linear) and potential $U_1\oplus U_2\colon\outp{M_1}\times\outp{M_2}\times\inpt{N_1}\times\inpt{N_2}\to\rr$, given by the sum $U_1\bigl(\outp m_1,\inpt n_1\bigr)+U_2\bigl(\outp m_2,\inpt n_2\bigr)$. Each summand is a pure quadratic pulled back along a linear projection; by Lemma 2 the sum is pure quadratic. The monoidal unit is $\lensob{\rr^0}$ with $\outp{\rr^0}=\inpt{\rr^0}=\rr^0\in\vect$, all data trivially linear and pure quadratic.

So $\plmfd^{\lin}$ is closed under identities, composition, and the monoidal product, hence a sub-SMC. $\qed$

### Lemma 4 (the action restricts).

The action of `lem.parameter_lens_action` sends $\bigl((V,\sharpR_V),\lensob X\bigr)\mapsto\binom{\inpt X}{V\times\outp X}$. We verify that this restricts to an action $\rvect^{\cnst}\times\plmfd^{\lin}\to\plmfd^{\lin}$.

*On objects.* For $V\in\rvect^{\cnst}$ (so $V\in\vect$) and $\lensob X\in\plmfd^{\lin}$ (so $\outp X,\inpt X\in\vect$), the action $\binom{\inpt X}{V\times\outp X}$ has $\inpt X\in\vect$ and $V\times\outp X\in\vect$. ✓

*On morphisms.* For $u\colon V\to V'$ in $\rvect^{\cnst}$ (a $\rvect$-iso between constant-sharp objects, hence a linear map of vector spaces) and $f=(\outp f,\inpt f,U)\colon\lensob c\to\lensob d$ in $\plmfd^{\lin}$, the action formula of `lem.parameter_lens_action` gives
\[
u\cdot f \;=\; \binom{(\varepsilon_{\inc(V)}\otimes\outp c\otimes\inpt d)\then\inpt f}{\inc(u)\otimes\outp f}.
\]
Here $\varepsilon_{\inc(V)}\colon V\to 1$ is the comonoid counit; concretely on vector-space objects this is the unique map (projection that discards $V$). So the lens components of $u\cdot f$ are
\[
\outp{u\cdot f}\colon V\times\outp c\to V'\times\outp d,\quad(v,c)\mapsto(u(v),\outp f(c)),
\]
\[
\inpt{u\cdot f}\colon V\times\outp c\times\inpt d\to\inpt c,\quad(v,c,d)\mapsto\inpt f(c,d).
\]
Both are linear. The potential of $u\cdot f$ pulls $U\colon\outp c\times\inpt d\to\rr$ back along the projection $V\times\outp c\times\inpt d\to\outp c\times\inpt d$, a linear map; by Lemma 2 the pullback is pure quadratic. ✓

So the action restricts. $\qed$

### Theorem ($\srw^{\lin}$ is a sub-operad of $\srw$).

By Lemmas 1, 3, 4, the action $\rvect\times\plmfd\to\plmfd$ restricts to an action $\rvect^{\cnst}\times\plmfd^{\lin}\to\plmfd^{\lin}$ between sub-SMCs. Apply `prop.para_square` with $F$ the inclusion $\rvect^{\cnst}\hookrightarrow\rvect$ (strict monoidal, since the sub-SMC structure is inherited on the nose), $G$ the inclusion $\plmfd^{\lin}\hookrightarrow\plmfd$ (strict monoidal, similarly), and natural transformation $\theta = \id$ (both sides of $F(a)\cdot' G(x)\to G(a\cdot x)$ are literally equal because $F, G$ are inclusions and the actions agree on sub-objects, so all coherence diagrams are tautological). The proposition delivers a strong symmetric monoidal functor
\[
\para{\rvect^{\cnst}}{\plmfd^{\lin}}\;\longrightarrow\;\para{\rvect}{\plmfd}\;=\;\potlens.
\]
It is injective on objects and faithful because $F$ and $G$ both are (sub-SMC inclusions); hence an embedding. Taking underlying operads gives $\srw^{\lin}\hookrightarrow\srw$. $\qed$

### Corollary (the four-condition characterization).

A multimorphism $f=\bigl((V,\sharpR_V),\binom{\inpt f}{\outp f},U\bigr)$ in $\srw$ lies in $\srw^{\lin}$ iff (i) all interfaces are vector spaces, (ii) $\outp f$ and $\inpt f$ are linear, (iii) $\sharpR_V$ is constant in $x:V$, and (iv) $U$ is a pure quadratic form. Unpack the Para definition.

---

## Notational conventions

Two new $\mathrm{xxx}$-label macros, matching the existing $\conf,\phase,\lrn,\euc$ pattern (lines 419–422):

```latex
\newcommand{\lin}{\mathrm{lin}}    % linear-stratum suboperad/subcategory marker
\newcommand{\cnst}{\mathrm{cnst}}  % constant-sharp marker for rvect
```

Call sites: $\srw^{\lin}$, $\rvect^{\cnst}$, $\plmfd^{\lin}$. Tracks the existing precedent ($\srw^{\mathrm{lin}}$ rendered the same way, just compiled via macro now). No new tracked term needed — these inherit the `\trackTerm` machinery of $\srw$, $\rvect$, etc.

One new `\defineTermAs` for **pure quadratic form**, anchored in Lemma 2's introductory sentence so the term has a single canonical source.

Variable conventions for the new propositions/lemmas: $f,g$ for srw-morphisms (not $h,k$); $V,W$ for parameter spaces; $\lensob M,\lensob N,\lensob P$ for interfaces; $\outp f,\inpt f$ for lens components; $U$ for potential; $\sharpR_V$ for parameter sharp; $\sharpS_{T^*V}$ for canonical symplectic sharp. (Mirrors `prop.linear_stratum` and `rmk.constant_inverse_mass_hamiltonian`.)

---

## Section-by-section changes

### `sec.W_choice` — add the definitions and lemmas

Insert immediately after `def.potlens` (line 2097, where `\srw` is named) and before the composition-diagram remark at line 2107. New content:

1. `def.rvect_cnst`: $\rvect^{\cnst}$.
2. Lemma 1 inline as a one-line remark or folded into the definition body ("closed under direct sum by `prop.rvect_monoidal`").
3. `def.plmfd_lin`: $\plmfd^{\lin}$.
4. Lemma 2: pure-quadratic-form functoriality (also defines the term **pure quadratic form**).
5. Lemma 3: $\plmfd^{\lin}$ is closed under composition, monoidal product, identity.
6. Lemma 4 inline in the next definition's lemma slot.
7. `def.srw_lin` (and `thm.srw_lin_suboperad`): $\srw^{\lin}\coloneqq$ underlying operad of $\para{\rvect^{\cnst}}{\plmfd^{\lin}}$; the embedding into $\srw$ from the Theorem above.

Net: one definition cluster, four short lemmas, one theorem-corollary pair. ~½ page.

### `sec.cotangent_storages` — strip the design-space subsection

Delete lines 2337–2344 (the `\paragraph{Design space of cotangent storages.}` block and its closing paragraph). The bifurcation paragraph at line 2346 ("we now get to our bifurcation between learning and physics") stays in place.

`rmk.cotangent_learners` at line 2384 moves to `sec.design_space` (next change).

### New section `sec.design_space` at end of `ch.dynamics_functor`

Insert after `sec.configuration_dynamics` ends (around line 2810), before `ch.applications` begins at line 2812. Working title: **Design space of cotangent storages.**

Content, in order:
1. Three-axes paragraph (migrated from `sec.cotangent_storages`, rewritten as consolidation rather than preview; opening sentence: "Having unpacked $\Phiconf{}$ and $\Phiphase{}$ in detail, we step back and locate them in a small design space.").
2. `prop.linear_stratum` (relocated from `sec.graph_laplacian`), with its inline four-condition recap removed (now cited as `def.srw_lin` upstream). Statement compresses to ~3 lines; proof unchanged modulo references.
3. `rmk.constant_inverse_mass_hamiltonian` (migrated from `sec.phase_dynamics`, line 2610), sharpened with $\srw^{\lin}$ vocabulary: "Suppose $f\in\srw^{\lin}$ with parameter sharp symmetric, applied through $\store{\phase}$" replaces the three boldface hypotheses. Closing paragraph already separates "Hamiltonian-form" from "conservation"; vocabulary substitution sharpens the split. **Decision deferred:** split into two short remarks vs.\ keep unified.
4. `rmk.cotangent_learners` (migrated from `sec.cotangent_storages`), sharpened: "for $f\in\srw^{\lin}$ with parameter sharp symmetric positive-definite, $\Phiconf{}$ recovers gradient descent on $U$."
5. Closing paragraph naming the design-space corners visually (kinematical / conservative / dissipative) and the mixed-symmetry possibilities (Langevin / variable-$\sharp$) as out-of-scope.

### `sec.phase_dynamics` — leave a pointer

After deletion of `rmk.constant_inverse_mass_hamiltonian` from its current location at line 2610, leave a one-sentence pointer: "The Hamiltonian reading of \eqref{eqn.state_update} is given in \cref{sec.design_space}." `rmk.euler_energy` at line 2639 stays in place — it's a separate point about the Euler step, not Hamiltonian content.

### `sec.wave_equation` — tag and clean

Add to $\Part$'s definition: "$\Part\in\srw^{\lin}$." After the chain composite, note that the closure of Lemma 3 makes the composite again in $\srw^{\lin}$. The derivation is unchanged.

### `sec.graph_laplacian` — tag and tighten

Add to $\rr^{\varphi_G},\Part_v,\psi_G$: all in $\srw^{\lin}$. The wave/heat paragraph at line 3273 (currently following the in-place `prop.linear_stratum`) is reworked: since `prop.linear_stratum` has moved upstream to `sec.design_space`, this paragraph now reads as application-side commentary citing the upstream proposition. The "for the same kinematical reason" sentence becomes one line: "Both wave and heat dynamics on $\psi_G$ are instances of \cref{prop.linear_stratum} applied through $\store{\phase}$ and $\store{\conf}$ respectively."

`rmk.graph_heat` at line 3248 stays in `sec.graph_laplacian`; its closing sentence updates to cite `sec.design_space`'s design-space framing.

### Intro chapter — one phrase

Update the sentence at line 545 ending "...constancy, antisymmetry, and symmetric positive-definiteness of the carrier's reactive structure --- are independently responsible for superposition, energy conservation, and gradient descent." Add: "We name the syntactic regime where the superposition axis lives, the linear stratum $\srw^{\lin}\subset\srw$ (\cref{def.srw_lin})."

---

## Order of operations

1. **Add macros and definitions** in preamble (`\lin`, `\cnst`) and in `sec.W_choice` (`def.rvect_cnst`, `def.plmfd_lin`, Lemmas 1–4, `def.srw_lin`, `thm.srw_lin_suboperad`, Corollary). Build, verify the lemma cluster compiles.
2. **Tag worked examples**: $\Part$, $\rr^{\varphi_G}$, $\Part_v$, $\psi_G$, the chain composite. Available now without forward references.
3. **Create `sec.design_space`** at the end of `ch.dynamics_functor`. Start with the three-axes paragraph migrated from `sec.cotangent_storages`, framed as consolidation.
4. **Migrate `prop.linear_stratum`** from `sec.graph_laplacian` into `sec.design_space`. Compress its statement (drop the four-condition recap, now cited as `def.srw_lin`). Update the citing prose at line 3273.
5. **Migrate `rmk.constant_inverse_mass_hamiltonian`** from `sec.phase_dynamics` into `sec.design_space`, sharpened with $\srw^{\lin}$ vocabulary. Decide split-or-not.
6. **Migrate `rmk.cotangent_learners`** from `sec.cotangent_storages` into `sec.design_space`, sharpened. Leave the dissipative-corner stub.
7. **Delete the design-space `\paragraph` block** in `sec.cotangent_storages` (lines 2337–2344). Its content has now migrated.
8. **Sharpen `rmk.graph_heat`** (stays in `sec.graph_laplacian`) to cite `sec.design_space` cleanly.
9. **Insert phase-dynamics pointer** at the old `rmk.constant_inverse_mass_hamiltonian` site.
10. **Update intro sentence** at line 545.
11. **Build twice; cross-reference sweep.** No stale `\cref{rmk.linear_stratum}`; no stale forward references; new labels (`def.rvect_cnst`, `def.plmfd_lin`, `def.srw_lin`, `thm.srw_lin_suboperad`, lemma labels, `pure_quadratic_form` term) all resolve.

---

## Risks and uncertainties

1. **Anticlimactic reading.** The current design-space placement in `sec.cotangent_storages` lets `conf`/`phase` be motivated as design-space points before their definitions. Moving the section to the end of `ch.dynamics_functor` reverses this: storages defined first, then categorized retrospectively. **Mitigation:** opening paragraph of `sec.design_space` needs to frame as consolidation-and-payoff, not recap. Write deliberately.
2. **Conservative-remark migration.** Moving `rmk.constant_inverse_mass_hamiltonian` out of `sec.phase_dynamics` distances the Hamiltonian reading from the phase-space update equation. Mitigated by leaving an in-place pointer.
3. **Citation rot.** Three labels currently exist that get moved: `rmk.constant_inverse_mass_hamiltonian`, `rmk.cotangent_learners`. Citations exist at the intro (line 545), kinetic-1-form definition (line 1922), `rmk.euler_energy` (line 2657), `sec.cotangent_storages` design-space subsection. Labels follow the remarks; `\cref` resolves to the new location, prose stays correct.
4. ~~**The Para-restriction theorem.** Used `prop.para_square` for the embedding $\para{\rvect^{\cnst}}{\plmfd^{\lin}}\hookrightarrow\srw$.~~ *Verified.* The hypotheses fit cleanly with $\theta=\id$ because both $F$ and $G$ are sub-SMC inclusions and the actions agree on sub-objects (so all coherence diagrams are tautological). The invocation is in fact tighter than the previous uses in the paper (lines 2253, 2279–2289), which combine `prop.para_square` with `prop.para_strong_induced` to *produce* the action square; we have the action square in hand from Lemma 4. Injectivity-on-objects and faithfulness of the resulting embedding come from $F,G$ being inclusions — not from `prop.para_square` directly; flagged in the Theorem proof as one extra sentence.
5. **Page count.** Net delta probably +½ to +1 page: definitions and lemmas in `sec.W_choice` add weight; the new `sec.design_space` consolidates content already in the document (relocations). The previous rewrite ended at +1; this one shouldn't add more than ½–1 more.

## Estimated effort

1–2 days of focused work. Definitions and lemmas in `sec.W_choice` are the load-bearing piece; everything else is relocation and vocabulary substitution.

## What this rewrite is *not*

- **Not** graduating the conservative or dissipative axes — they don't carve joints worth graduating beyond what sharpening does.
- **Not** changing the chapter structure beyond adding one terminal section in `ch.dynamics_functor`.
- **Not** introducing continuous-time machinery to formalize energy conservation as a proposition.
- **Not** revisiting `prop.linear_stratum`'s proof — statement compresses; proof unchanged.

---

## Handoff notes (read before starting)

**Line numbers in this plan are approximate.** Grep for the label or term, don't trust the integer. The plan was written against the post-step-10 state of `rewrite-plan.md`; the file may have drifted slightly. Labels are stable; line numbers aren't.

**Label slugs to use** (consistent kebab-case, matching paper conventions):

| Slug | What | Step |
|---|---|---|
| `def.rvect_cnst` | $\rvect^{\cnst}$ | 1 |
| `def.plmfd_lin` | $\plmfd^{\lin}$ | 1 |
| `def.srw_lin` | $\srw^{\lin}$ | 1 |
| `lem.rvect_cnst_smc` | Lemma 1 (could be inline) | 1 |
| `lem.quadratic_functorial` | Lemma 2 (pure quadratic forms) | 1 |
| `lem.plmfd_lin_smc` | Lemma 3 ($\plmfd^{\lin}$ closed) | 1 |
| `lem.action_restricts` | Lemma 4 (action restriction) | 1 |
| `thm.srw_lin_suboperad` | Theorem (embedding) | 1 |
| `cor.srw_lin_four_conditions` | Corollary (four-condition characterization) | 1 |
| `pure_quadratic_form` | `\defineTermAs` term anchor in Lemma 2 | 1 |
| `sec.design_space` | New terminal section of `ch.dynamics_functor` | 3 |

**The "pure quadratic form" term currently lives inline in `prop.linear_stratum`'s proof** (around line 3264: "Pure-quadraticity of $U$ means $dU|_x=Qx$ for some linear $Q$"). After Step 1, that sentence becomes redundant — Lemma 2 defines the term with a $\defineTermAs{pure_quadratic_form}$ anchor. Delete the inline definition in the proof; the term is now resolved upstream.

**Step 1 also includes an inline-macro sweep.** The current `prop.linear_stratum` writes $\srw^{\mathrm{lin}}$ inline (line 3260, 3264, 3273). After adding `\newcommand{\lin}{\mathrm{lin}}` to the preamble, sweep these to $\srw^\lin$ so all sites use the macro. (Same render, uniform source.)

**Build after every step**, not just Step 1. The previous rewrite's edit log records build-clean checkpoints at each step; do the same. See `reference_build.md` in auto-memory for the pdflatex+biber recipe in this repo.

**Judgment calls to surface, not decide unilaterally:**

- **Step 5 (Hamiltonian remark): split into two short remarks vs.\ keep unified.** The closing paragraph of `rmk.constant_inverse_mass_hamiltonian` already separates "Hamiltonian-form" (uses symmetric parameter sharp) from "conservation" (uses antisymmetric carrier sharp). With $\srw^{\lin}$ vocabulary the split reads sharper; whether to formalize as two remarks depends on how the migrated prose lands. Write it once unified first; if it reads cleanly, leave it. If it muddies, propose the split.
- **Step 3 (opening paragraph of `sec.design_space`): tone.** The plan's #1 risk is "anticlimactic reading" — moving the design-space exposition from upstream-of-storage-definitions to downstream changes the rhetorical posture from "preview" to "consolidation." The opening sentence sets that tone. Draft and surface for review.
- **Lemma 1 inline or as its own labeled lemma.** Lemma 1's content ($\oplus$ of constants is constant) is one line. Could fold into `def.rvect_cnst`'s body as a parenthetical, or call it out as a numbered lemma. Either works; pick whichever reads better in context.

**Downstream-citation check at Step 11:** `eqn.hamiltonian` (defined at line 2628 inside `rmk.constant_inverse_mass_hamiltonian`) gets pulled with the remark when it migrates to `sec.design_space`. Citations to it (line 2636) still resolve since the label stays. Verify in the sweep.

**Don't graduate the conservative or dissipative axes.** The user explicitly directed: graduate only when there's a real joint. The verification turned up exactly three graduations: the two new definitions ($\rvect^{\cnst}$, $\plmfd^{\lin}$), and `def.srw_lin`. The remarks get sharpened, not promoted. Anything more is scope creep — surface to the user first if you find yourself wanting more.

---

## Edit log (running memory)

Format: each entry covers one session-step. Lists files/locations touched, deviations from the plan, and editorial decisions worth flagging for the editorial pass.

### Step 1 — Macros + linear-stratum cluster in `sec.forming_potlens`
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:**
  - Preamble (after line 422): added `\newcommand{\lin}{\mathrm{lin}}` and `\newcommand{\cnst}{\mathrm{cnst}}`.
  - `sec.forming_potlens` (between `def.potlens` and the composition-diagram remark, after the `smooth_rewiring_diagram`/`closed_system` naming paragraph): inserted the cluster.
  - Existing `\srw^{\mathrm{lin}}` sites in (a) the design-space `\paragraph` block in `sec.cotangent_storages` and (b) the in-place `prop.linear_stratum` in `sec.graph_laplacian` swept to `\srw^{\lin}`.
- **Content:** Definition cluster, in order: `def.rvect_cnst` + one-paragraph remark on its sub-SMC closure (Lemma 1 inlined); `def.plmfd_lin`; `lem.quadratic_functorial` (which introduces `\defineTermAs{pure_quadratic_form}{...}` as the canonical term anchor); `lem.plmfd_lin_smc` (identity / composition / monoidal-product closure); `lem.action_restricts`; `def.srw_lin` ($\para{\rvect^\cnst}{\plmfd^\lin}$); `thm.srw_lin_suboperad` (embedding via `prop.para_square` with $\theta=\id$); `cor.srw_lin_four_conditions` (four-condition characterization).
- **Decisions / deviations:**
  - **`\Sym^2` notation dropped.** Plan's draft for Lemma 2 used $\Sym^2(V^*)$; the operator isn't declared in the preamble. Rephrased the lemma to plain prose ("the pure quadratic forms on $V$ make a real vector space; pullback along a linear map is linear in $U$") — same content, no new preamble macros. The $\Sym^2$ notation isn't reused anywhere.
  - **Insertion location.** Plan said "after `def.potlens`, before the composition-diagram remark." Placed the cluster after the closed_system paragraph (line 2105) rather than before it — keeps the "$\srw$ named → its morphisms named → its sub-operad introduced → composition visualized" reading order.
  - **No new subsection header.** The cluster reads as a continuation of `sec.forming_potlens`; adding a subsubsection here would be the only subsubsection in the document.
  - **Lemma 1 inlined** as a one-paragraph remark after `def.rvect_cnst` (per plan's option). It's a single observation, doesn't warrant a numbered lemma slot.
  - **Tracked terms:** no new `\defineTerm{...}` macros — $\rvect^\cnst$, $\plmfd^\lin$, $\srw^\lin$ render as compositions of existing macros, and the plan explicitly notes "no new tracked term needed." Only `pure_quadratic_form` is added (as a `\defineTermAs` anchor in Lemma 2).
  - **Trailing remark removed before commit.** Drafted a closing "the composition formula reads off closure of $\srw^\lin$" remark; removed as redundant with `thm.srw_lin_suboperad` (edit-scope discipline).
- **Verified:** Build clean, 68 pages (was 65), no undefined references.

### Step 2 — Tag worked examples
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** five sites in `ch.applications`:
  - `sec.wave_equation`, particle $\Part$ (line 3081, end of harmonic-potential paragraph): "Thus $\Part\in\srw^\lin$ (\cref{cor.srw_lin_four_conditions})."
  - `sec.wave_equation`, chain composite (line 3115, end of "with $\inpt f$ vacuous…" paragraph): "Both $\Part$ and $\fun{wire}_K$ lie in $\srw^\lin$, so by closure under operadic composition (\cref{lem.plmfd_lin_smc}) so does $\fun{wire}_K(\Part,\ldots,\Part)$."
  - `sec.graph_laplacian`, $\rr^{\varphi_G}$ (line 3276): "; hence $\rr^{\varphi_G}\in\srw^\lin$."
  - `sec.graph_laplacian`, $\Part_v$ (line 3294, end of the "single $\kappa,m>0$" sentence): "As for $\Part$, the same four-condition check gives $\Part_v\in\srw^\lin$."
  - `sec.graph_laplacian`, $\psi_G$ (line 3305, end of partition-of-$E$ sentence): "Since $\rr^{\varphi_G}$ and each $\Part_v$ lie in $\srw^\lin$, closure under operadic composition (\cref{lem.plmfd_lin_smc}) gives $\psi_G\in\srw^\lin$."
- **Decisions / deviations:**
  - Tagged $\fun{wire}_K$ implicitly via the chain-composite sentence ("Both $\Part$ and $\fun{wire}_K$ lie in $\srw^\lin$") rather than as a separate standalone tag — saves a sentence and reads cleanly.
  - Did not tag the static-wiring-diagram framing line for $\fun{wire}_K$ at line 3098–3103 separately; the chain-composite sentence carries it.
- **Verified:** Build clean, 68 pages, no undefined references.

### Step 3 — New `sec.design_space` section
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** `ch.dynamics_functor`, end (between the closing sentence of `sec.configuration_dynamics` and `\chapter{Applications}`): inserted `\section{Design space of cotangent storages}\label{sec.design_space}` with opening consolidation paragraph + three-axes bullet list + "two storages at two corners" closing paragraph.
- **Decisions / deviations:**
  - Left the existing forward-pointing sentence at end of `sec.configuration_dynamics` ("Applications of $\Phiconf{}$ appear in…") in place rather than moving it — minimal-touch.
  - Opening sentence frames as consolidation, not preview: "Having unpacked $\Phiphase{}$ and $\Phiconf{}$ in detail (\cref{sec.phase_dynamics,sec.configuration_dynamics}), we step back and locate them in a small design space."
  - The bullet list and closing paragraph are migrated verbatim from the still-extant `\paragraph{Design space…}` block in `sec.cotangent_storages` (which gets deleted in Step 7). Between Steps 3 and 7, the prose is duplicated — accepted as the intermediate state.
- **Verified:** Build clean, 68 pages, no undefined references.

### Step 4 — Migrate `prop.linear_stratum`
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:**
  - `sec.design_space` (after the closing paragraph of Step 3): inserted compressed `prop.linear_stratum` + its proof + the "Both worked-out storages satisfy the hypothesis…" verification paragraph.
  - `sec.graph_laplacian` (around old line 3371–3387): deleted the lead-in paragraph ("The wave equation exhibits superposition…"), the in-place `prop.linear_stratum` + proof, and the trailing "Both worked-out storages…" paragraph. Replaced the whole block with one sentence: "Both wave and heat dynamics on $\psi_G$ are instances of \cref{prop.linear_stratum}, applied through $\store{\phase}$ and $\store{\conf}$ respectively: the shared kinematical hypothesis — $\psi_G\in\srw^\lin$ together with linear anchor and update at constant $\sharpR$ — accounts for the superposition both exhibit, independent of the conservative/dissipative split."
- **Decisions / deviations:**
  - **Statement compressed.** Dropped the "Write $\srw^\lin\subset\srw$ for the suboperad whose interfaces…" four-condition recap — that content is now `def.srw_lin` + `cor.srw_lin_four_conditions`. The statement now reads as one sentence: "For any cotangent storage … whose anchor and update are linear maps of vector spaces, the dynamics functor $\Phi_\mathfrak{s}$ sends every $0$-ary closed system $I\to I$ in $\srw^\lin$ to a linear endomap on the carrier $F(V)$."
  - **Pure-quadraticity sentence in the proof:** changed "Pure-quadraticity of $U$ means $dU|_x=Qx$ for some linear $Q$" → "Since $U$ is pure quadratic, $dU|_x=Qx$ for some linear $Q$." Per handoff note: the original sentence was the inline definition of the term; now superseded by `lem.quadratic_functorial`.
  - **Verification paragraph kept with prop, application paragraph collapsed.** The original trailing paragraph had two functions: (a) verifying both worked-out storages satisfy the linear-anchor/update hypothesis, (b) citing the wave and heat equations as instances. Migrated (a) with the prop into `sec.design_space`; (b) collapsed to the one-line citation in `sec.graph_laplacian`. The "superposition is kinematical, not from antisymmetry" insight from the original lead-in is now folded into the collapsed sentence and into `sec.design_space`'s third paragraph.
  - Wave-equation forward-reference avoided: the migrated verification paragraph in `sec.design_space` does not cite `\eqref{eqn.discrete_wave}` or `\cref{rmk.graph_heat}` (those references are application-side and stay in `sec.graph_laplacian`).
- **Verified:** Build clean, 68 pages, no undefined references.

### Step 5 — Migrate and sharpen `rmk.constant_inverse_mass_hamiltonian`
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:**
  - `sec.design_space`: inserted the sharpened remark immediately after the Step 4 verification paragraph.
  - `sec.phase_dynamics`: deleted the original remark in full (lines 2712–2739 pre-edit). The phase-dynamics pointer that replaces it lives in Step 9.
- **Decisions / deviations:**
  - **Kept the remark unified** (not split into two short remarks) per handoff direction ("write it once unified first; if it reads cleanly, leave it"). The closing paragraph's split between Hamiltonian-form (parameter-symmetric) and conservation (carrier-antisymmetric) already reads sharply with $\srw^\lin$ vocabulary; no need to formalize the split as separate remarks.
  - **Bold-hypothesis structure removed.** The three bold-hypothesis labels ("closed", "constant", "symmetric") collapsed to two prose conditions: (a) "$f$ is a $0$-ary closed system in $\srw^\lin$, applied through $\store{\phase}$" — captures closed + constant + linear-data + pure-quadratic in one phrase via `cor.srw_lin_four_conditions`; (b) "when the parameter sharp is moreover *symmetric*…" — the additional Hamiltonian condition.
  - **Intro line dropped.** The original opened with "This remark justifies the Hamiltonian terminology used elsewhere in the paper. The hypotheses are written in bold; the closing paragraph locates each on its proper design-space axis." — both halves now obvious in the new context (we're in `sec.design_space`, the bold-hypothesis structure is gone), so the opening goes straight to the math.
  - Closing paragraph's `\cref{sec.cotangent_storages}` → "this design space" (we're inside it).
  - Label `rmk.constant_inverse_mass_hamiltonian` and `eqn.hamiltonian` both preserved — all five downstream citations (intro line 547, kinetic 1-form line 1924, design-space bullet at line 2914, `rmk.euler_energy` at line 2742, and Step 9's pointer) resolve unchanged.
- **Verified:** Build clean, 68 pages, no undefined references.

### Step 6 — Migrate and sharpen `rmk.cotangent_learners`
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:**
  - `sec.design_space`: inserted the sharpened remark immediately after `rmk.constant_inverse_mass_hamiltonian` (preserving the kinematical / conservative / dissipative bullet order).
  - `sec.cotangent_storages`: deleted the original remark in full.
- **Decisions / deviations:**
  - **Title changed:** "Gradient-based learning" → "Gradient descent as the dissipative-corner instance" — matches `rmk.graph_heat`'s "dissipative-corner instance" title pattern and locates the remark on the design-space axis directly.
  - **Opening sharpened per plan:** "For $f\in\srw^\lin$ with parameter sharp $\sharpR_V$ symmetric positive-definite, applied through $\store{\conf}$, the dynamics functor $\Phiconf{}$ recovers gradient descent on $U$."
  - **Sign-convention nuance carried over.** The Euclidean example $\sharpR_x = -\eta_{\mathrm{LR}}\sharpEuc{}$ absorbs the descent direction into the sharp; the body explains this. Statement says "symmetric positive-definite" (matching the design-space bullet's wording) and the example shows the concrete sign convention. Editorial pass could tighten the bullet's wording if strict signs matter.
  - Label `rmk.cotangent_learners` and `eqn.learning_sharp` both preserved — three downstream citations (`ex.euclidean_sharp` at line 1909, `rmk.euler_energy` at line 2715, `sec.dl_warmup` at line 3033) resolve unchanged.
- **Verified:** Build clean, 68 pages, no undefined references.

### Step 7 — Delete old design-space block in `sec.cotangent_storages`
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** `sec.cotangent_storages`, the `\paragraph{Design space of cotangent storages.}` block (lines 2439–2446 pre-edit): deleted in full. The bifurcation paragraph at line 2448 stays in place.
- **Decisions / deviations:**
  - **Bifurcation paragraph extended with a forward pointer.** Original closing: "These are formalized in \cref{prop.rvect_polynomial} and \cref{lem.phase_storage}." Updated: "These are formalized in \cref{prop.rvect_polynomial} and \cref{lem.phase_storage}; both are located in a small design space of cotangent storages in \cref{sec.design_space}." — preserves the upstream-of-storages reader's signpost to the consolidation section.
- **Verified:** Build clean, 68 pages, no undefined references.

### Step 8 — Sharpen `rmk.graph_heat`
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** `rmk.graph_heat` (in `sec.graph_laplacian`): updated the closing sentence's design-space cite from `\cref{sec.cotangent_storages}` to `\cref{sec.design_space}`. The body of the remark (heat-equation derivation, dissipative-corner-vs-conservative-corner sentence) stays in place.
- **Decisions / deviations:**
  - **Minimal touch.** Per Step 8's narrow scope ("closing sentence updates to cite sec.design_space's design-space framing"), changed only the cref target — no rewording of the surrounding prose.

### Step 9 — Phase-dynamics pointer
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** `sec.phase_dynamics` (after the breakdown paragraphs following `eqn.state_update`, where `rmk.constant_inverse_mass_hamiltonian` used to live): inserted "The Hamiltonian reading of \eqref{eqn.state_update} is given in \cref{rmk.constant_inverse_mass_hamiltonian} (\cref{sec.design_space})."
- **Decisions / deviations:**
  - One-sentence pointer as planned. Did not move surrounding content.

### Step 10 — Intro sentence
- **File:** `dynamic-algebra-potentials.tex`.
- **Touched:** intro paragraph at line 547 (the closing sentence that lists the three design-space axes).
- **Content:** Two changes in one edit: (a) `\cref{sec.cotangent_storages}` → `\cref{sec.design_space}`; (b) appended "We name the syntactic regime where the superposition axis lives the *linear stratum* $\srw^\lin\subset\srw$ (\cref{def.srw_lin})."
- **Decisions / deviations:**
  - Phrased as "We name the syntactic regime where the superposition axis lives the *linear stratum*…" with the emphatic comma and italics, matching the existing rhetorical register of this paragraph.

### Step 11 — Rebuild and cross-reference sweep
- Ran `pdflatex` twice; both passes clean, 68 pages, no undefined references.
- **Stale-reference sweep:**
  - One stray `\cref{sec.cotangent_storages}` at line 2500 (in the discussion of phase storage's antisymmetric ingredient, between `lem.phase_storage` and `prop.phase_storage_pair`) — not called out in the plan. Updated to `\cref{sec.design_space}`.
  - No stale `\cref{rmk.linear_stratum}` (already gone from the previous rewrite).
  - All new labels (`def.rvect_cnst`, `def.plmfd_lin`, `def.srw_lin`, `thm.srw_lin_suboperad`, `cor.srw_lin_four_conditions`, `lem.quadratic_functorial`, `lem.plmfd_lin_smc`, `lem.action_restricts`, `pure_quadratic_form` term anchor) resolve.
- **`cleveref` `definitionx` format warning fixed.** The proof of `cor.srw_lin_four_conditions` uses `\cref{def.rvect_cnst,def.plmfd_lin}` — a comma-separated multi-cref to definition labels. This triggered "cref reference format for label type `definitionx' undefined" because the preamble declares `\crefname{...}{...}{...}` for `examplex`/`remarkx`/`theorem`/etc. but is missing the parallel declaration for `definitionx`. (Latent oversight — the existing document never used a multi-cref to definitions.) Added `\crefname{definitionx}{Definition}{Definitions}` at line 161 of the preamble, immediately after `\newtheorem{definitionx}{Definition}[section]`. Warning gone.

## Final state (after step 11)
- **Total page delta (this rewrite):** +3 (65 → 68). Slightly over the plan's "+½ to +1 page" estimate; the lemma cluster (3 definitions + 3 lemmas + 1 theorem + 1 corollary + tracked-term anchor) is the load-bearing source, as anticipated.
- **Labels added (this rewrite):** `def.rvect_cnst`, `def.plmfd_lin`, `def.srw_lin`, `thm.srw_lin_suboperad`, `cor.srw_lin_four_conditions`, `lem.quadratic_functorial`, `lem.plmfd_lin_smc`, `lem.action_restricts`, `sec.design_space`, and the `pure_quadratic_form` `\defineTermAs` anchor.
- **Labels relocated (label preserved, location moved):** `prop.linear_stratum`, `rmk.constant_inverse_mass_hamiltonian`, `eqn.hamiltonian`, `rmk.cotangent_learners`, `eqn.learning_sharp`.
- **Labels removed:** none.
- **Preamble change:** two `\newcommand`s (`\lin`, `\cnst`) and one `\crefname{definitionx}{...}` declaration.
