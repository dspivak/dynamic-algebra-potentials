# Stage-2 vocabulary

Master vocabulary for the Stage-2 Python implementation of `dynamic-algebra-potentials`. Each entry carries a scope tag:

- `[in-scope]` — Stage 2 implements this directly.
- `[abstract]` — Used in proofs at high abstraction; Stage 2 implements only the specialization needed for the running examples.
- `[future-work]` — Acknowledged but not part of Stage 2.

Entries follow the form `- **\name** (introduced in \cref{label}) — [tag] one-line description.`

# TYPES

## Categories

- **`\smset`** (introduced in \cref{sec.poly}) — `[in-scope]` the cartesian category of sets and functions; we also use the core groupoid $\smset_\cong$ of sets and bijections.
- **`\finset`** (introduced in \cref{ex.lens_finsetop}) — `[abstract]` the category of finite sets and functions; $\finset\op$ is cartesian monoidal under disjoint union $(0,+)$.
- **`\vect`** (introduced in \cref{sec.manifolds_notation}) — `[in-scope]` the category of finite-dimensional real vector spaces and linear maps, with cartesian monoidal structure $(0,\oplus)$.
- **`\mfd`** (introduced in \cref{sec.manifolds_notation}) — `[in-scope]` the cartesian category $(\mfd,\rr^0,\times)$ of finite-dimensional smooth real manifolds and smooth maps; v1 restricts to $\rr^d$.
- **`\pvect`** (introduced in \cref{def.pnla}) — `[in-scope]` the symmetric monoidal groupoid of paired vector spaces and pairing-preserving linear isomorphisms, monoidal under direct sum.
- **`\pnla`** (introduced in \cref{rmk.pnla_generalization}) — `[future-work]` the symmetric monoidal groupoid of paired nilpotent Lie algebras, a generalization of $\pvect$ flagged in remarks.
- **`\poly`** (introduced in \cref{sec.poly}) — `[in-scope]` the symmetric monoidal closed category of polynomial functors $\smset\to\smset$ under the Dirichlet product $\otimes$.
- **`\smcat`** (introduced in \cref{sec.org}) — `[abstract]` the cartesian category of small categories, used as the codomain of the lax monoidal coalgebra functor.
- **`\org`** (introduced in \cref{sec.org}) — `[in-scope]` the monoidal bicategory of polynomials with $\org(p,q)\coloneqq\ihom{p,q}\coalg$, the dynamical-system semantics; represented in code via `OrgMorphism` (no class for the bicategory itself).
- **`\Lens{\cat{C}}`** (introduced in \cref{subsec.lenses}) — `[abstract]` the symmetric monoidal category of lenses in a symmetric monoidal $\cat C$, with objects $\lensob c$ and morphisms $(\outp f,\inpt f)$.
- **`\Lens{\cat{C}}^{\Fun T}`** (introduced in \cref{prop.backward_comonad}) — `[abstract]` the coKleisli category of the backward comonad $\Lens{\Fun T}$ for a strong monad $\Fun T$ on $\cat C$; Stage 2 only instantiates the cotangent monad case.
- **`\potlens`** (introduced in \cref{def.potlens}) — `[in-scope]` the symmetric monoidal category $\para{\pvect}{\lmfd^\rr}$ of potentialized lenses, the principal object of study.
- **`\Para`** (introduced in \cref{sec.para_general}) — `[abstract]` the bicategorical Para construction $\para{\cat A}{\cat D}$ for an action of a symmetric monoidal $\cat A$ on $\cat D$; Stage 2 builds only the specific Para instances needed.

## Objects / Structures

- **paired vector space** (introduced in \cref{def.pnla}) — `[in-scope]` a finite-dimensional real vector space $V$ equipped with a linear isomorphism $\sharp_V\colon V^*\To{\cong}V$ (equivalently a nondegenerate bilinear pairing).
- **lens object** (introduced in \cref{subsec.lenses}) — `[in-scope]` a pair $\lensob c=\binom{\inpt c}{\outp c}$ of objects of $\cat C$ with a chosen commutative comonoid structure on $\outp c$.
- **$(\otimes)$-comonoid** (introduced in \cref{sec.prelim}) — `[in-scope]` an object $c$ in a symmetric monoidal category equipped with coassociative, counital comultiplication $\delta_c\colon c\to c\otimes c$ and counit $\varepsilon_c\colon c\to I$; carried explicitly in code via `DirichletComonoid(poly, monoid)`.
- **supply of comonoids** (introduced in \cref{sec.prelim}) — `[abstract]` a $\otimes$-compatible choice of cocommutative comonoid structure on every object of $\cat C$, possibly homomorphic.
- **$\tri$-comonoid / polynomial comonad** (introduced in \cref{sec.comonads}) — `[in-scope]` a polynomial $c$ with counit $\epsilon\colon c\to\yon$ and comultiplication $\delta\colon c\to c\tri c$; equivalently a small category.
- **$p$-coalgebra** (introduced in \cref{sec.coalgebras}) — `[in-scope]` a pair $(S,\beta\colon S\to p(S))$ presenting a deterministic dynamical system whose interface is the polynomial $p$.
- **$\ihom{p,q}$-coalgebra** (introduced in \cref{def.pq_coalg}) — `[in-scope]` a pair $(S,\beta\colon S\to\ihom{p,q}\tri S)$, the data of a hom-object morphism in $\org$, decomposing as an action $\act^\beta\colon S\to\poly(p,q)$ and an update.
- **$\Fun{T}$-monoid** (introduced in \cref{def.T_monoid}) — `[abstract]` a $\otimes$-monoid $(z,e_z,m_z)$ with a $\Fun T$-algebra $\alpha\colon\Fun T z\to z$ that is a monoid homomorphism; Stage 2 uses only the cotangent specialization.
- **potentialized manifold lens** (introduced in \cref{subsec.potentialized_lenses}) — `[in-scope]` a morphism $(\outp f,\inpt f,U)\colon\lensob M\to\lensob N$ in $\lmfd^\rr$, comprising forward map, backward map, and potential $U\colon\outp M\times\inpt N\to\rr$.
- **potentialized polynomial lens** (introduced in \cref{subsec.potentialized_lenses}) — `[in-scope]` a morphism $\lensob p\to\lensob q$ in $\Lens{\poly}^\rr$, i.e.\ a pair $(\outp f\colon\outp p\to\outp q,\;\inpt f\colon\outp p\otimes\inpt q\to\cot{\rr}\otimes\inpt p)$.
- **parameterized map** (introduced in \cref{sec.para_general}) — `[in-scope]` a morphism in $\para{\cat A}{\cat D}$, a pair $(a,f\colon a\cdot x\to y)$ of parameter $a:\cat A$ and underlying $\cat D$-map.

## Operations / Maps

- **`\sharp`** (introduced in \cref{def.pnla}) — `[in-scope]` the sharp map $\sharp_V\colon V^*\To{\cong}V$ of a paired vector space.
- **`\flat`** (introduced in \cref{def.pnla}) — `[in-scope]` the flat map $\flat_V\coloneqq\sharp_V\inv\colon V\to V^*$, inverse of $\sharp$.
- **exponential** (introduced in \cref{sec.TT}) — `[in-scope]` the map $\exp_V\colon T^*V\to V$, $(v,\xi)\mapsto v+\sharp_V(\xi)$, the time-1 flow of the constant left-invariant vector field on a paired vector space.
- **Dirichlet product** (introduced in \cref{sec.poly}) — `[in-scope]` the symmetric monoidal product on $\poly$, $p\otimes q=\sum_{(i,j)}\yon^{p[i]\times q[j]}$, with unit $\yon$; constructor `DirichletProduct(*ps)`.
- **internal hom** (introduced in \cref{sec.poly}) — `[in-scope]` the right adjoint $\ihom{p,q}$ to $\blank\otimes p$ in $\poly$, satisfying $\ihom{p,q}(1)=\poly(p,q)$; never materialized — appears virtually inside `OrgMorphism` step functions.
- **substitution product** (introduced in \cref{sec.comonads}) — `[in-scope]` the composition product $p\tri q\coloneqq p\circ q$ on $\poly$, with unit $\yon$; comonoids for $\tri$ are small categories.
- **store action** (introduced in \cref{def.store_action}) — `[in-scope]` the strong monoidal action $S\cdot p\coloneqq S\yon^S\otimes p$ of $\smset_\cong$ on $\poly$.
- **Legendre projection** (introduced in \cref{def.legendre_projection}) — `[in-scope]` the per-component map $\rho_V\colon\cot{T^*V}\to\cot{V}$ with positions $(v,\xi)\mapsto v$ and directions $\xi_V\mapsto(\xi_V,\sharp_V(\xi))$; the natural transformation $\rho$ assembling these lives in FUNCTORS.

## Wiring / Operadic structures

- **wiring-diagram operad** (introduced in \cref{sec.wd_operads}) — `[abstract]` an operad $\cat W$ (e.g.\ $\cat W_{\tn{O-Cat}}$, $\cat W_{\tn{O-MnCat}}$, $\cat W_{\tn{O-Opd}}$) whose multimorphisms are legal arrangements of boxes-with-ports inside a box.
- **`\List`** (introduced in \cref{sec.wd_operads}) — `[abstract]` the list endofunctor on $\smset$, used to form object sets such as $\List(O)\times O$ for $\cat W_{\tn{O-Opd}}$.

# FUNCTORS

## Endofunctors on $\pvect$

- **$T\colon\pvect\to\pvect$** (introduced in \cref{prop.TT_endofunctors}) — `[in-scope]` sends $V$ to $V\oplus V$ and $\phi\colon V\to W$ to $\phi\oplus\phi$; strong symmetric monoidal w.r.t.\ $(0,\oplus)$ by \cref{prop.TT_monoidal}.
- **$T^*\colon\pvect\to\pvect$** (introduced in \cref{prop.TT_endofunctors}) — `[in-scope]` sends $V$ to $V\oplus V^*$ and $\phi$ to $\phi\oplus(\phi^*)\inv$; strong symmetric monoidal w.r.t.\ $(0,\oplus)$ by \cref{prop.TT_monoidal}.

## Functors between named categories

- **$\Fun{Store}\colon\smset_\cong\to\poly$** (introduced in \cref{def.store_action}) — `[in-scope]` sends $S$ to $S\yon^S$ and a bijection $f\colon S\To{\cong}T$ to $f\yon^{f\inv}$; strong symmetric monoidal $(1,\times)\to(\yon,\otimes)$.
- **$\cot\colon\mfd\to\poly$** (introduced in \cref{def.cot}) — `[in-scope]` sends $M$ to $\sum_{m\in M}\yon^{T^*_mM}$ and smooth $f\colon M\to N$ to the $\poly$ map with forward part $f$ and backward part $(T_mf)^\top$; strong symmetric monoidal by \cref{prop.cot_monoidal}.

## Lifted functor

- **$\Lens\cot\colon\lmfd^\rr\to\Lens{\poly}^\rr$** (introduced in \cref{lem.cot_lifts_lens_potential}) — `[in-scope]` strong symmetric monoidal lift of $\cot$ to potentialized lens categories, via the monad-morphism $\cot{\rr\times\blank}\Rightarrow\cot{\rr}\otimes\cot{\blank}$.

## Internalization / dynamical realization chain

- **$\cint\colon\potlens\to\para{\cot}{\poly}$** (introduced in \cref{lem.potlens_to_para_poly}) — `[in-scope]` *cotangent internalization*; lax symmetric monoidal composite $\para\pvect{\Lens\cot}\then\para\pvect{\Theta_{\potd}}$. Independently exposed and tested.
- **$\leg\colon\para{\cot}{\poly}\to\para{\cot{T^*}}{\poly}$** (introduced in \cref{lem.para_rho}) — `[in-scope]` *Legendre refinement*; strong symmetric monoidal, induced by $\rho$. Independently exposed and tested.
- **$\dyn\colon\para{\cot{T^*}}{\poly}\to\org$** (introduced in \cref{lem.poly_to_org}) — `[in-scope]` *dynamical realization*; identity-on-objects lax symmetric monoidal, via the action square involving $T^*$ and $\Fun{Store}$. Independently exposed and tested.
- **$\Phi\colon\potlens\to\org$** (introduced in \cref{thm.functor}) — `[in-scope]` the paper's main functor; lax symmetric monoidal composite $\cint\then\leg\then\dyn$.

## Auxiliary functors

- **$\Theta\colon\Lens{\cat C}\to\cat C$** (introduced in \cref{prop.Theta}) — `[future-work]` the normal lax monoidal functor $\lensob c\mapsto\outp c\otimes\ihom{\inpt c,I}$ internalizing lenses inside an arbitrary closed monoidal $\cat C$.
- **$\Theta_z$ / $\Theta_{T,\alpha}\colon\Lens{\cat C}^{\Fun T}\to\cat C$** (introduced in \cref{prop.Theta_T_alpha}) — `[abstract]` the lax monoidal functor $\lensob c\mapsto\outp c\otimes\ihom{\inpt c,z}$ depending on a $\Fun T$-monoid $(z,e,m,\alpha)$.
- **$\Theta_{\potd}\colon\Lens{\poly}^\rr\to\poly$** (introduced in \cref{lem.Theta_poly_potential}) — `[in-scope]` the cotangent-monad specialization of $\Theta_{T,\alpha}$ at $z=\yon$ and the constant covector field $\potd\colon\cot{\rr}\to\yon$ of \eqref{eqn.d_potential}; sends $\lensob p$ to $\outp p\otimes\ihom{\inpt p,\yon}$.
- **$\Psi\colon\para{\pvect}{\mfd}\to\org$** (introduced in \cref{cor.cotangent_learners}) — `[in-scope]` *cotangent learners*; strong symmetric monoidal, $M\mapsto\cot{M}$, restricting to the deep-learning operad functor of \cref{sec.deep_learning}.

## Natural transformations

- **$\theta\colon\Fun{Store}\circ|\blank|\Rightarrow\cot\circ\Fun{inc}$** (introduced in \cref{prop.pnla_polynomial}) — `[in-scope]` components $\theta_V\colon V\yon^V\To{\cong}\cot{V}$, identity on positions and given on directions at $v$ by $\xi\mapsto v+\sharp_V(\xi)$; witnesses commutativity of the $\pvect$-to-$\poly$ square.
- **$\rho\colon\cot{T^*\blank}\Rightarrow\cot{\blank}$** (introduced in \cref{lem.rho_natural}) — `[in-scope]` monoidal natural transformation $\pvect\to\poly$ with components the Legendre projection $\rho_V$ of \cref{def.legendre_projection}: position $(v,\xi)\mapsto v$, direction $\xi_V\mapsto(\xi_V,\sharp_V(\xi))$.

# Design decisions for Stage 2

1. **Polynomial representation: a small library of named constructors, not a generic `Polynomial` class.**
   - `Yon` — the unit polynomial $\yon$.
   - `Cot(dim)` — $\cot{\rr^{\text{dim}}}$; positions are points of $\rr^{\text{dim}}$, directions are cotangent vectors of the same shape.
   - `DirichletProduct(*ps)` — $p_1\otimes\cdots\otimes p_k$.
   - `PolyMap(src, tgt, position_action, direction_action)` — polynomial maps between any of the above.

2. **Internal hom $\ihom{p,q}$ is virtual.** It appears only inside $\org$-homsets, represented as `OrgMorphism = (state, step_function)`. The step function returns a `PolyMap` together with a state-update closure. We never materialize $\ihom{p,q}$ as a standalone polynomial.

3. **The bicategory $\org$ has no Python class.** Its homsets are represented via `OrgMorphism`, with a `compose` operator (series + parallel). 2-cells are not modeled.

4. **$\otimes$-comonoid structure on polynomials is explicit, not implicit.** A polynomial $p$ is a Dirichlet-comonoid iff each direction set carries a monoid; that monoid choice is carried in code. For our examples it is always the additive group structure on cotangent fibers, making $\cot\rr$ a Dirichlet-comonoid. Wrapper: `DirichletComonoid(poly, monoid)`.

5. **Manifolds = $\rr^d$ in v1.** All current examples (wave equation, Klein-Gordon, N-body, future heavy-ball-style fixed-loss) are Euclidean. Non-Euclidean manifolds ($S^1$ for the pendulum, etc.) deferred to v2.

6. **$\Theta_z$ implemented at the cotangent specialization only.** $T = \cot\rr\otimes\blank$, $z = \yon$, $\alpha = \potd$. The generic $\Theta_{T,\alpha}$ remains `[abstract]`.

7. **Expose all four functors in the chain ($\cint$, $\leg$, $\dyn$, $\Phi$).** Each is independently testable; per-stage tests make debugging tractable.

8. **Autodiff backend: JAX.** Cotangent pullbacks $T^\top f$, differentials $dU$, transposes $(\phi^*)^{-1}$ all use `jax.vjp` / `jax.linear_transpose`. Closures capturing state arrays use `jax.tree_util.Partial` for jit-friendliness.

9. **Affine covector fields.** All covector fields in the running examples are affine — $\omega(v_0) = a v_0 + b$ with state-dependent $a, b$. Represented as `(matrix, vector)` pairs by default; fall back to general closures only if needed. Saves serialization and JIT pain.
