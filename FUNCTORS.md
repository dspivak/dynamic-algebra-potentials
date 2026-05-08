# Functors and natural transformations

This file lists the named functors and natural transformations the paper introduces. It is the companion to `TYPES_curated.md` (which lists categories and structured objects).

## Endofunctors on $\pvect$

- **$T\colon\pvect\to\pvect$** (introduced in \cref{prop.TT_endofunctors}) — sends $V$ to $V\oplus V$ and $\phi\colon V\to W$ to $\phi\oplus\phi$. Strong symmetric monoidal with respect to $(0,\oplus)$ by \cref{prop.TT_monoidal}.
- **$T^*\colon\pvect\to\pvect$** (introduced in \cref{prop.TT_endofunctors}) — sends $V$ to $V\oplus V^*$ and $\phi$ to $\phi\oplus(\phi^*)\inv$. Strong symmetric monoidal with respect to $(0,\oplus)$ by \cref{prop.TT_monoidal}.

## Functors between named categories

- **$\Fun{Store}\colon\smset_\cong\to\poly$** (introduced in \cref{def.store_action}) — sends $S$ to $S\yon^S$ and a bijection $f\colon S\To{\cong}T$ to $f\yon^{f\inv}$. Strong symmetric monoidal with respect to $(1,\times)\to(\yon,\otimes)$.
- **$\cot\colon\mfd\to\poly$** (introduced in \cref{def.cot}) — sends $M$ to $\sum_{m\in M}\yon^{T^*_mM}$ and a smooth $f\colon M\to N$ to the $\poly$ map with forward part $f$ and backward part $(T_mf)^\top$. Strong symmetric monoidal by \cref{prop.cot_monoidal}.

## Lifted functor

- **$\Lens\cot\colon\lmfd^\rr\to\Lens{\poly}^\rr$** (introduced in \cref{lem.cot_lifts_lens_potential}) — strong symmetric monoidal lift of $\cot$ to potentialized lens categories, via the monad-morphism $\cot{\rr\times\blank}\Rightarrow\cot{\rr}\otimes\cot{\blank}$.

## Internalization / dynamical realization chain

- **$\cint\colon\potlens\to\para{\cot}{\poly}$** (introduced in \cref{lem.potlens_to_para_poly}) — *cotangent internalization*. Lax symmetric monoidal; the composite $\para\pvect{\Lens\cot}\then\para\pvect{\Theta_{\potd}}$.
- **$\leg\colon\para{\cot}{\poly}\to\para{\cot{T^*}}{\poly}$** (introduced in \cref{lem.para_rho}) — *Legendre refinement*. Strong symmetric monoidal; induced from the natural transformation $\rho$.
- **$\dyn\colon\para{\cot{T^*}}{\poly}\to\org$** (introduced in \cref{lem.poly_to_org}) — *dynamical realization*. Identity-on-objects lax symmetric monoidal functor, obtained via the action square involving $T^*$ and $\Fun{Store}$.
- **$\Phi\colon\potlens\to\org$** (introduced in \cref{thm.functor}) — the paper's main functor; lax symmetric monoidal composite $\cint\then\leg\then\dyn$.

## Auxiliary functors / operations

- **$\Theta_{\potd}\colon\Lens{\poly}^\rr\to\poly$** (introduced in \cref{lem.Theta_poly_potential}) — lax monoidal functor sending $\lensob p$ to $\outp p\otimes\ihom{\inpt p,\yon}$; specialization of the $\Fun T$-monoid construction $\Theta_{T,\alpha}$ at $z=\yon$ and the constant covector field $\potd\colon\cot{\rr}\to\yon$ of \eqref{eqn.d_potential}.
- **$\Psi\colon\para{\pvect}{\mfd}\to\org$** (introduced in \cref{cor.cotangent_learners}) — *cotangent learners*. Strong symmetric monoidal; sends $M\mapsto\cot{M}$ and a parameterized smooth map to its cotangent-learner coalgebra. Restricts to the deep-learning operad functor of \cref{sec.deep_learning}.

## Natural transformations

- **$\theta\colon\Fun{Store}\circ|\blank|\Rightarrow\cot\circ\Fun{inc}$** (introduced in \cref{prop.pnla_polynomial}) — components $\theta_V\colon V\yon^V\To{\cong}\cot{V}$, identity on positions and given on directions at $v$ by $\xi\mapsto v+\sharp_V(\xi)$. Witnesses commutativity of the $\pvect$-to-$\poly$ square.
- **$\rho\colon\cot{T^*\blank}\Rightarrow\cot{\blank}$** (introduced in \cref{lem.rho_natural}) — monoidal natural transformation $\pvect\to\poly$ with components $\rho_V\colon\cot{T^*V}\to\cot{V}$ given by the *Legendre projection* of \cref{def.legendre_projection}: position $(v,\xi)\mapsto v$, and direction $\xi_V\mapsto(\xi_V,\sharp_V(\xi))$.
