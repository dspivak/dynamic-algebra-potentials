# Proposal: a Riemann-gradient parallel to the symplectic-Hamiltonian functor $\Phi$

## 1. Where the symplectic choice is actually made

The structural pivot is **`lem.para_rho` / `lem.poly_to_org`**, jointly. Concretely, the symplectic content of $\Phi=\cint\then\leg\then\dyn$ enters in two coupled places, both downstream of $\cint$:

1. **`lem.para_rho` (the Legendre refinement $\leg$).** The natural transformation $\rho\colon\cot{T^*\blank}\Rightarrow\cot$ of `lem.rho_natural`, with components $\xi_V\mapsto(\xi_V,\sharp_V(\xi))$ given by `def.legendre_projection`, *introduces the momentum factor*: it replaces the parameter object $V$ by its phase space $T^*V$, and threads $\sharp_V$ into the direction action.
2. **`lem.poly_to_org` (the dynamical realization $\dyn$).** The action square uses $\cot{T^*V}\cong\Fun{Store}(F(V))\otimes\blank$, where $F(V)$ is the *underlying set of $T^*V$* equipped with the **canonical symplectic pairing** of `prop.canonical_symplectic_pairing`. The store action then turns directions into state updates via the `\eqn.flow_cot` exponential, and the sharp on $T^*V$ is the canonical symplectic sharp $\sharp_X\colon(\xi',x')\mapsto(x',-\xi')$ of `\eqn.canonical_sharp`. This is precisely what produces `\eqn.state_update`:
   $$ s+\sharp_X(\xi_V,\sharp_V(\xi)) = (x+\sharp_V(\xi),\,\xi-\xi_V).$$

The single symbolic locus where "Hamiltonian" is locked in is the antisymmetric sign in `\eqn.canonical_sharp`/`\eqn.sharp_X`. Replacing the composite $\leg\then\dyn$ by a "do-nothing-then-flow" composite using the *original* pairing $\sharp_V$ on $V$ (rather than the symplectic pairing on $T^*V$) drops the momentum coordinate entirely and turns the update into
$$ x \mapsto x - \sharp_V(\xi_V),$$
which is gradient flow when $\sharp_V$ is positive-definite and $\xi_V = dU$. Note: $\cint$ is symplectic-agnostic; `lem.alpha_constant` is also symplectic-agnostic (it just fixes the constant covector field $+1$).

So the cleanest pivot is: **replace the $\leg\then\dyn$ tail by a direct $\dyn^{\rm grad}\colon\para{\cot}{\poly}\to\org$ using the store action $\Fun{Store}(|V|)$ instead of $\Fun{Store}(|T^*V|)$.** This is essentially what $\Psi$ does in `cor.cotangent_learners`.

## 2. Recommended structure: option C (with modification)

I recommend **option C with a sign change**: a short subsection in `ch.potentials` defining $\Phi^{\rm grad}$, plus a heat-equation subsection in `\section{Other examples}` (`sec.other_examples`) of `ch.spring`. With one important addition: $\Phi^{\rm grad}$ should be presented as a *literal factoring through $\Psi$*, not as an independent construction. This minimizes new machinery and makes the symplectic-vs-gradient parallel sharp.

Rationale against B (full parallel chapter): the gradient story is mathematically a *truncation* of the symplectic story — drop the Legendre lift, keep everything else. A parallel chapter would duplicate the wiring/composition narrative of `ch.spring` to no real benefit; the reader has already absorbed that machinery. A worked subsection inside `sec.other_examples` is enough to exhibit the heat equation and let the reader transfer the wave-equation derivation.

Rationale against A (subsection only): without the heat-equation example actually written out, the symmetry stays abstract. The reader currently sees $\Psi$ (deep learning) and $\Phi$ (physics); they should see one more concrete physics example using the gradient-flow side.

### 2.1. Sub-subsection structure inside `ch.potentials`

Insert a new subsection at the end of `\section{The dynamics of potentialized lenses}` (`sec.potential_lenses_to_dynamics`), after `sec.dynamics_functor`:

**`\subsection{Gradient flow as an alternative dynamics functor}\label{sec.gradient_dynamics}`** (~1 page)

- *Paragraph 1: the pivot.* State that the symplectic content of $\Phi$ enters via the Legendre refinement $\leg$ and the use of the canonical symplectic sharp on $T^*V$ in $\dyn$. Removing the Legendre step produces a different functor.
- *Paragraph 2: the construction.* Define
  $$\dyn^{\rm grad}\colon\para{\cot}{\poly}\to\org$$
  by the same recipe as `lem.poly_to_org` but using the action square for $V\cdot p = \cot{V}\otimes p$ and $F^{\rm grad}\colon\pvect\to\smset_\cong$, $V\mapsto |V|$ (no $T^*$). Note the relevant isomorphism is $\cot V\cong\Fun{Store}(|V|)$ from `prop.pnla_polynomial`, which already exists in the paper. Then
  $$\Phi^{\rm grad}\coloneqq\cint\then\dyn^{\rm grad}\colon\potlens\to\org.$$
- *Paragraph 3: the update formula.* On a morphism $f=(\outp f,\inpt f,U)\colon V\cdot\lensob M\to\lensob N$, the resulting coalgebra has state space $X^{\rm grad}\coloneqq V$ (no momentum coordinate), and the state update at $s=x\in V$ is
  $$ x \mapsto x + \sharp_V(\xi_V),$$
  where $\xi_V$ is exactly as in `\eqn.bigtheta`. When $\sharp_V$ is *negative*-definite (e.g.\ $\sharp_V = -\eta\cdot\id$), this is a gradient *descent* step on the contributing potentials; when $\sharp_V$ is positive-definite (e.g.\ $\sharp_V = \eta\cdot\id$), it is gradient *ascent*. Choose one convention and stick with it; below I use $\sharp_V=-\eta\cdot\id$ for descent, matching `sec.deep_learning`.
- *Paragraph 4: relation to $\Phi$.* Phrased categorically: there is a natural transformation $\Phi^{\rm grad}\Rightarrow\Phi\circ(\text{section of forgetful})$ — or, more usefully, $\Phi$ is what you get if you precompose with the Legendre lift and use the canonical symplectic pairing on $T^*V$ in place of the original pairing on $V$. The two functors have the same source $\potlens$ but produce coalgebras with different state spaces ($T^*V$ vs.\ $V$).
- *Paragraph 5: relation to $\Psi$.* See section 3 below; one or two sentences acknowledging that $\Phi^{\rm grad}$ is the potential-aware extension of $\Psi$ along the inclusion $\para\pvect\mfd\hookrightarrow\potlens$ that takes the trivial potential.

**New labels needed:**
- `lem.poly_to_org_gradient` — definition of $\dyn^{\rm grad}$ (parallel to `lem.poly_to_org`).
- `thm.functor_gradient` — the resulting $\Phi^{\rm grad}$ (parallel to `thm.functor`).
- `eqn.state_update_gradient` — the update $x\mapsto x+\sharp_V(\xi_V)$ (parallel to `eqn.state_update`).
- `eqn.sharp_X_gradient` — for cosmetic parallelism, optional.

**No new types or operations** in `VOCAB.md` are strictly required: the construction reuses $\sharp_V$, the cotangent monad on lenses, $\cint$, `prop.pnla_polynomial`. One new functor entry: `\Phi^{\rm grad}\colon\potlens\to\org` (introduced in `thm.functor_gradient`). One could optionally add a remark that $\sharp_V$ is being used as a *Riemannian metric* (positive-definite) rather than a generic pairing, but the paper's `\pvect` already permits indefinite pairings; the positive-definite restriction is a *choice the user makes per example*, not a structural change.

### 2.2. Heat equation subsection inside `sec.other_examples`

Insert as a new subsection after `sec.nbody`:

**`\subsection{The heat equation as gradient flow}\label{sec.heat_equation}`** (~3/4 page)

- *Setup.* Same chain wiring as `sec.spring_first_pass`; same harmonic potential $U(x,y)=(\kappa/2)(x-y)^2$. The single change is at the level of the parameter pairing: use $\sharp_V = -\eta\cdot\id$ on $V=\rr^K$ (positive learning rate $\eta>0$, descent sign), and apply $\Phi^{\rm grad}$ rather than $\Phi$.
- *Calculation.* Tracing through `eqn.state_update_gradient`, the chain coalgebra produces
  $$ x_i' = x_i - \eta\,(\xi_V)_i = x_i - \eta\,\partial_{x_i}U(\vec x,x_0).$$
  The pinned chain (same boundary conditions as `\eqn.wave_bc`) gives
  $$ x_i' = x_i + \eta\kappa(x_{i-1}+x_{i+1}-2x_i).$$
  This is exactly the discrete heat equation $\partial_t x = \eta\kappa\,\Delta x$ (negative-Laplacian convention of `sec.nd_wave`).
- *Stability remark.* Stable for $\eta\kappa<1/2$ — the standard explicit-Euler stability bound for parabolic equations. Worth noting *because* the wave-equation footnote (`\eqref{eqn.state_update}` footnote) explicitly flags that the symplectic Euler step is unconditionally unstable. The contrast is illuminating: gradient flow on a positive potential dissipates energy and is conditionally stable; Hamiltonian flow conserves energy and is unconditionally unstable in explicit Euler. This contrast is a free pedagogical bonus.
- *Generalizations.* One paragraph: replacing $U$ by Klein-Gordon-style on-site terms gives reaction-diffusion equations (Fisher-KPP, Allen-Cahn). Replacing the wiring by the cubic lattice gives the $d$-dimensional heat equation. This parallels `sec.klein_gordon` and `sec.nd_wave` and emphasizes that the *same* lens-and-potential infrastructure now produces parabolic equations once we swap the dynamics functor.

## 3. Relationship with $\Psi$

$\Phi^{\rm grad}$ **strictly subsumes** $\Psi$, but not by a lot. Precisely:

There is a faithful embedding $\iota\colon\para{\pvect}{\mfd}\hookrightarrow\potlens$ sending a parameterized map $f\colon V\times M\to N$ to the potentialized lens with the same forward map, *vacuous* backward map $\inpt f$, and *trivial* potential $U=0$. Under this embedding,
$$ \Phi^{\rm grad}\circ\iota \;\cong\; \Psi.$$
Trivial backward map and zero potential mean $\xi_V$ in `\eqn.bigtheta` reduces to its first summand $(T_{(x,m)}\outp f)^\top\xi_N$, and the gradient update becomes $s\mapsto s+\sharp_V((\partial_Vf)^\top\xi)$, which is `\eqn.cotangent_learner_update`.

So the relationship is: $\Phi^{\rm grad}$ is what $\Psi$ becomes once you allow potentials and a backward map. Equivalently, $\Psi$ is the trivial-potential, vacuous-backward restriction of $\Phi^{\rm grad}$.

The deep-learning example of `sec.deep_learning` should still live where it is (inside the $\Psi$ chapter), but the proposed `sec.gradient_dynamics` should add a sentence: "When restricted along $\iota$, $\Phi^{\rm grad}$ recovers the cotangent-learner functor $\Psi$ of `cor.cotangent_learners`; in particular it strictly extends the deep-learning example of `sec.deep_learning` by allowing potentials." This is the first time the paper actually *links* its two functors. Right now $\Psi$ is presented and then $\Phi$ is presented and the reader is left to wonder. Worth doing for that reason alone.

## 4. Does the wave-equation chapter need rebranding?

**Mild rebranding only.** The chapter title `Example: the wave equation` and the section structure are fine as is. I would suggest two small edits:

1. Add one sentence to `sec.spring_intro`: "We illustrate $\Phi$ by deriving the wave equation; in `sec.heat_equation` (or wherever) we illustrate the parallel functor $\Phi^{\rm grad}$ by deriving the heat equation."
2. The phrase "the wave equation" is already framed as a *symplectic* example by the footnote at `\eqn.state_update` (which calls out explicit Euler of the Hamiltonian vector field). So no chapter retitling. If you wanted a sharper handle, retitling `\section{Other examples}` to `\section{Other Hamiltonian examples}` and giving the heat equation its own peer section `\section{Gradient-flow examples}` would emphasize the parallel — but I think that overstates the structural difference at the level of $\potlens$, which is the paper's main object. The two functors share *all* of $\potlens$; only the post-composition differs.

## 5. One subtlety worth flagging

The paper's `\pvect` is *paired*, not *Riemannian*. A paired vector space allows indefinite pairings: nondegenerate but not necessarily positive-definite. The wave-equation example uses $\sharp_V(p)=p/m$ which happens to be positive-definite, but this is incidental — symplectic flow doesn't care about the sign of $\sharp_V$, only that it's invertible. Gradient flow *does* care: positive-definite $\sharp_V$ gives descent (heat equation, dissipation, conditional stability); indefinite $\sharp_V$ gives a flow that descends in some directions and ascends in others (saddle-flow, useful for adversarial dynamics like GANs but not what one usually means by "gradient flow").

Practically this means: nothing in the *categorical machinery* changes between $\Phi$ and $\Phi^{\rm grad}$, but the *interpretation* of $\sharp_V$ does. For $\Phi$ it is "inverse mass" (or symplectic structure on the parameter space); for $\Phi^{\rm grad}$ it is "Riemannian metric" or "negative learning-rate operator". The proposal should acknowledge this in `sec.gradient_dynamics`, possibly via a remark, so that readers don't conclude that $\pvect$ is somehow "Riemannian by default" when it isn't.

One concrete choice for the paper: in the heat-equation example, write $\sharp_V = -\eta\cdot\id$ (matching the $\Psi$ deep-learning example's sign). This gives genuine descent and matches `sec.deep_learning`'s convention exactly. This is *not* the same as `sec.spring_intro`'s $\sharp_V=p/m$ (which is positive). Worth being explicit about this sign so readers don't get confused.
