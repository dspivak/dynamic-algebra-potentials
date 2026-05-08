# Types module (curated)

This file is the hand-curated complement to `TYPES.md`. It records the named mathematical structures the paper introduces that a Python implementation will instantiate as a class, dataclass, or distinguished structure. Concept-words, property-adjectives, and physical-process names have been dropped; descriptions are rewritten from the LaTeX source.

Each bullet has the form `- **\name** (introduced in \cref{label}) -- one-line description.`

## Categories

- **`\smset`** (introduced in \cref{sec.poly}) -- the cartesian category of sets and functions; we also use the core groupoid $\smset_\cong$ of sets and bijections.
- **`\finset`** (introduced in \cref{ex.lens_finsetop}) -- the category of finite sets and functions; $\finset\op$ is cartesian monoidal under disjoint union $(0,+)$.
- **`\vect`** (introduced in \cref{sec.manifolds_notation}) -- the category of finite-dimensional real vector spaces and linear maps, with cartesian monoidal structure $(0,\oplus)$.
- **`\mfd`** (introduced in \cref{sec.manifolds_notation}) -- the cartesian category $(\mfd,\rr^0,\times)$ of finite-dimensional smooth real manifolds and smooth maps.
- **`\pvect`** (introduced in \cref{def.pnla}) -- the symmetric monoidal groupoid of paired vector spaces and pairing-preserving linear isomorphisms, monoidal under direct sum.
- **`\pnla`** (introduced in \cref{rmk.pnla_generalization}) -- the symmetric monoidal groupoid of paired nilpotent Lie algebras (a generalization of $\pvect$ used in remarks).
- **`\poly`** (introduced in \cref{sec.poly}) -- the symmetric monoidal closed category of polynomial functors $\smset\to\smset$ under the Dirichlet product $\otimes$.
- **`\smcat`** (introduced in \cref{sec.org}) -- the cartesian category of small categories, used as the codomain of the lax monoidal coalgebra functor.
- **`\org`** (introduced in \cref{sec.org}) -- the monoidal bicategory of polynomials with $\org(p,q)\coloneqq\ihom{p,q}\coalg$, the dynamical-system semantics.
- **`\Lens{\cat{C}}`** (introduced in \cref{subsec.lenses}) -- the symmetric monoidal category of lenses in a symmetric monoidal category $\cat C$, with objects $\lensob c$ and morphisms $(\outp f,\inpt f)$.
- **`\Lens{\cat{C}}^{\Fun T}`** (introduced in \cref{prop.backward_comonad}) -- the coKleisli category of the backward comonad $\Lens{\Fun T}$ associated to a strong monad $\Fun T$ on $\cat C$.
- **`\potlens`** (introduced in \cref{def.potlens}) -- the symmetric monoidal category $\para{\pvect}{\lmfd^\rr}$ of potentialized lenses, the principal object of study.
- **`\Para`** (introduced in \cref{sec.para_general}) -- the bicategorical Para construction $\para{\cat A}{\cat D}$ associated to an action of a symmetric monoidal $\cat A$ on $\cat D$.

## Objects / Structures

- **paired vector space** (introduced in \cref{def.pnla}) -- a finite-dimensional real vector space $V$ equipped with a linear isomorphism $\sharp_V\colon V^*\To{\cong}V$ (equivalently a nondegenerate bilinear pairing on $V$).
- **lens object** (introduced in \cref{subsec.lenses}) -- a pair $\lensob c=\binom{\inpt c}{\outp c}$ of objects of $\cat C$ with a chosen commutative comonoid structure on $\outp c$.
- **$(\otimes)$-comonoid** (introduced in \cref{sec.prelim}) -- an object $c$ in a symmetric monoidal category equipped with a coassociative, counital comultiplication $\delta_c\colon c\to c\otimes c$ and counit $\varepsilon_c\colon c\to I$.
- **supply of comonoids** (introduced in \cref{sec.prelim}) -- a $\otimes$-compatible choice of cocommutative comonoid structure on every object of $\cat C$, possibly homomorphic.
- **$\tri$-comonoid / polynomial comonad** (introduced in \cref{sec.comonads}) -- a polynomial $c$ with counit $\epsilon\colon c\to\yon$ and comultiplication $\delta\colon c\to c\tri c$ for the substitution product; equivalently a small category.
- **$p$-coalgebra** (introduced in \cref{sec.coalgebras}) -- a pair $(S,\beta\colon S\to p(S))$ presenting a deterministic dynamical system whose interface is the polynomial $p$.
- **$\ihom{p,q}$-coalgebra** (introduced in \cref{def.pq_coalg}) -- a pair $(S,\beta\colon S\to\ihom{p,q}\tri S)$, the data of a hom-object morphism in $\org$, decomposing as an action $\act^\beta\colon S\to\poly(p,q)$ and an update.
- **$\Fun{T}$-monoid** (introduced in \cref{def.T_monoid}) -- a $\otimes$-monoid $(z,e_z,m_z)$ in $\cat C$ together with a $\Fun T$-algebra structure $\alpha\colon\Fun T z\to z$ that is a monoid homomorphism; the value object for $\Theta_z$.
- **potentialized manifold lens** (introduced in \cref{subsec.potentialized_lenses}) -- a morphism $(\outp f,\inpt f,U)\colon\lensob M\to\lensob N$ in $\lmfd^\rr$, comprising a forward map, a backward map, and a real-valued potential $U\colon\outp M\times\inpt N\to\rr$.
- **potentialized polynomial lens** (introduced in \cref{subsec.potentialized_lenses}) -- a morphism $\lensob p\to\lensob q$ in $\Lens{\poly}^\rr$, i.e.\ a pair $(\outp f\colon\outp p\to\outp q,\;\inpt f\colon\outp p\otimes\inpt q\to\cot{\rr}\otimes\inpt p)$.
- **parameterized map** (introduced in \cref{sec.para_general}) -- a morphism in $\para{\cat A}{\cat D}$, a pair $(a,f\colon a\cdot x\to y)$ consisting of a parameter $a:\cat A$ and an underlying $\cat D$-map.

## Operations / Maps

- **`\sharp`** (introduced in \cref{def.pnla}) -- the sharp map $\sharp_V\colon V^*\To{\cong}V$ of a paired vector space, raising a covector to a vector.
- **`\flat`** (introduced in \cref{def.pnla}) -- the flat map $\flat_V\coloneqq\sharp_V\inv\colon V\to V^*$, the inverse of $\sharp$.
- **exponential** (introduced in \cref{sec.TT}) -- the map $\exp_V\colon T^*V\to V$, $(v,\xi)\mapsto v+\sharp_V(\xi)$, the time-1 flow of the constant left-invariant vector field on a paired vector space.
- **Dirichlet product** (introduced in \cref{sec.poly}) -- the symmetric monoidal product on $\poly$, $p\otimes q=\sum_{(i,j)}\yon^{p[i]\times q[j]}$, with unit $\yon$.
- **internal hom** (introduced in \cref{sec.poly}) -- the right adjoint $\ihom{p,q}$ to $\blank\otimes p$ in $\poly$, satisfying $\ihom{p,q}(1)=\poly(p,q)$.
- **substitution product** (introduced in \cref{sec.comonads}) -- the composition product $p\tri q\coloneqq p\circ q$ on $\poly$, with unit $\yon$; comonoids for $\tri$ are small categories.
- **store action** (introduced in \cref{def.store_action}) -- the strong monoidal action $S\cdot p\coloneqq S\yon^S\otimes p$ of $\smset_\cong$ on $\poly$, packaging the store-comonad assignment $S\mapsto S\yon^S$.
- **Legendre projection** (introduced in \cref{def.legendre_projection}) -- the natural transformation $\rho_V\colon\cot{T^*V}\to\cot{V}$ with positions $(v,\xi)\mapsto v$ and directions $\xi_V\mapsto(\xi_V,\sharp_V(\xi))$.
- **cotangent internalization $\cint$** (introduced in \cref{lem.potlens_to_para_poly}) -- the lax symmetric monoidal functor $\potlens\to\para{\cot}{\poly}$ obtained by composing $\Lens\cot$ with the parameterized $\Theta_{\potd}$.
- **Legendre refinement $\leg$** (introduced in \cref{lem.para_rho}) -- the strong symmetric monoidal functor $\para{\cot}{\poly}\to\para{\cot{T^*}}{\poly}$ induced by $\rho$.
- **dynamical realization $\dyn$** (introduced in \cref{lem.poly_to_org}) -- the identity-on-objects lax symmetric monoidal functor $\para{\cot{T^*}}{\poly}\to\org$ produced via $\cot{T^*V}\cong F(V)\yon^{F(V)}$.
- **`\Theta`** (introduced in \cref{prop.Theta}) -- the normal lax monoidal functor $\Theta\colon\Lens{\cat C}\to\cat C$, $\lensob c\mapsto\outp c\otimes\ihom{\inpt c,I}$, internalizing lenses inside a closed base.
- **$\Theta_z$ / $\Theta_{\potd}$** (introduced in \cref{prop.Theta_T_alpha}) -- the lax monoidal functor $\Lens{\cat C}^\Fun{T}\to\cat C$, $\lensob c\mapsto\outp c\otimes\ihom{\inpt c,z}$, depending on a $\Fun T$-monoid $(z,e,m,\alpha)$; the special case $\Theta_{\potd}$ uses $z=\yon$ with $\potd\colon\cot{\rr}\to\yon$ encoding the constant covector field $+1$.

## Wiring / Operadic structures

- **wiring-diagram operad** (introduced in \cref{sec.wd_operads}) -- an operad $\cat W$ (e.g.\ $\cat W_{\tn{O-Cat}}$, $\cat W_{\tn{O-MnCat}}$, $\cat W_{\tn{O-Opd}}$) whose multimorphisms are legal arrangements of boxes-with-ports inside a box.
- **`\List`** (introduced in \cref{sec.wd_operads}) -- the list endofunctor on $\smset$, used to form object sets such as $\List(O)\times O$ for the operad $\cat W_{\tn{O-Opd}}$.
