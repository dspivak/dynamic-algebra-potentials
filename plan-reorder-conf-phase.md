# Plan: Reorder sec.configuration_dynamics before sec.phase_dynamics

**Base commit:** `d808ffa` ("good state: notation cleanup before conf/phase reorder")

**Reversibility test:** This plan specifies the exact replacement text for
lines 2560–2844 of `dynamic-algebra-potentials.tex`, plus four exact
cross-reference substitutions elsewhere. Applying it produces the "after"
state. To reverse, restore the file to commit `d808ffa`.

**Guiding principle:** Every claim cites a numbered equation or result.
Nothing says "by the work above" or "as before" without a label.

---

## Why this reorder

1. Configuration lift is $(\id,\id)$; phase lift requires kinetic 1-form,
   cotangent endofunctor, multi-step composite. Simpler case first.
2. Applications chapter already puts configuration first (Newton, gradient
   descent before wave equation).
3. The intro foreshadows configuration first (rmk.cotangent_learners).
4. All shared formulas depend on $x$ alone; $\xi$ enters only through the
   phase state update.

---

## Part 1: Replace lines 2560–2844

Delete everything from line 2560 (the `%---` rule above the current phase
section header) through line 2844 (the blank line after the bridging
sentence). Replace with the exact text in **Section A** below (new
configuration section) followed by **Section B** (new phase section).

### Source tracking

Every block below is tagged with its origin. Tags:

- **VERBATIM phase 2561–2575** = copied character-for-character from the
  current phase section at those lines.
- **MODIFIED phase 2577–2584 [Φ_phase→Φ_conf ×3]** = copied from those
  lines with exactly the listed substitutions.
- **VERBATIM conf 2738–2752** = copied from the current configuration
  section.
- **NEW** = text that does not exist in the current file.

These tags appear as comments in the text below for the implementer's
reference. **Do not include the tags in the .tex file.**

---

### Section A: New configuration section (goes first)

```latex
%--------------------------------------------------------------------
\section{Configuration dynamics \texorpdfstring{$\Phiconf{}$}{Phi conf}}\label{sec.configuration_dynamics}
%--------------------------------------------------------------------
```
> MODIFIED conf 2704–2705. Only change: section now appears first; header
> and label are identical.

```latex

The dynamics functor $\Phiconf{}\colon\srw\to\org$ is the simpler of the two dynamics functors: its state space is the position manifold $V$ (no momentum component), and each step updates $x\mapsto x+\sharpR_x(\xi_V)$, where $\xi_V\in V^*$ is the parameter-direction covector assembled from $f$'s backward pass and the differential of its potential. This is the functor we apply to recover Newton's method (\cref{sec.newton_warmup}) and gradient descent (\cref{sec.dl_warmup}).
```
> MODIFIED conf 2707. Change: "is the configuration-lift analog of
> $\Phiphase{}$: its" → "is the simpler of the two dynamics functors: its".
> Rationale: conf now comes first, so "analog of phase" is a forward
> reference to something not yet unpacked.

```latex

For the configuration lift, the functor $\Psi_{\lift_{\conf}}$ presents a $\cotof{V}$-parameter by the store polynomial on $S\coloneqq\absval{V}$:
\[
S\yon^S\To{\theta_V}\cotof{V}.
\]
A state consists of a position $x\in V$, and an incoming covector $\xi'\in T^*_xV$ updates that state to $x+\sharpR_x(\xi')$ by \eqref{eqn.directions_sharp}. Note that in this case $\sharpR$ can depend on $x\in V$. But the majority of what takes place under $\Phi_\lift$ is still compressed within the $\Phi'$ factor from \cref{lem.potlens_to_para_poly}. So we now unpack $\Phiconf{}$ in total, tracing each term and sign in the resulting formulas back to the definitions that produced it.
```
> MODIFIED conf 2709–2713. Changes:
> - Deleted "So as in \cref{sec.phase_dynamics} we now carefully unpack
>   $\Phiconf{}$."
> - Replaced with "So we now unpack $\Phiconf{}$ in total, tracing each
>   term and sign in the resulting formulas back to the definitions that
>   produced it."
>   (Phrasing taken from phase 2569, adapted: $\Phiphase{}$ → $\Phiconf{}$.)

```latex

Let $\inpt M,\outp M:\mfd$ be manifolds, and write
\[\Omega(M)\coloneqq\{\omega\colon M\to T^*M\mid\pi\circ\omega=\id\}\]
for the set of (not-necessarily continuous) \emph{covector fields} on $M$.%
\footnote{We take all set-theoretic sections because the category $\poly$ remembers only the underlying sets of positions and directions, not their topology.} 
A smooth map $f\colon M\to N$ induces a \emph{pullback} $f^*\colon\Omega(N)\to\Omega(M)$ defined by $(f^*\omega)(m)\coloneqq(T_m f)^\top\omega(f(m))$.
```
> VERBATIM phase 2571–2575. No changes.

```latex

\paragraph{The action of $\Phiconf{}$ on objects.}
The functor $\Phiconf{}$ acts on objects as follows:
\begin{equation}\label{eqn.Phi_on_obs}
\Phiconf{}\lensob M=
\cotof{\outp M}\otimes\ihom{\cotof{\inpt M},\yon}\cong
\sum_{(\outp m,\omega):\outp M\times\Omega(\inpt M)}\yon^{\left(T^*_{\outp{m}}\outp M\right)\times\inpt M}.
\end{equation}
A position in $\Phiconf{}\lensob M$ is a pair $(\outp m,\omega)$ where $\outp m\in\outp{M}$ is a point and $\omega\in\Omega(\inpt M)$ is a covector field. A direction at $(\outp m,\omega)$ is a pair $(\xi,\inpt m)$ where $\xi:T^*_{\outp{m}}\outp M$ is a covector and $\inpt m\in\inpt M$ is a point.
```
> MODIFIED phase 2577–2584 [$\Phiphase{}$ → $\Phiconf{}$ ×3].
> The three occurrences are: paragraph header, "The functor $\Phiconf{}$
> acts", the LHS of eqn.Phi_on_obs, and "A position in $\Phiconf{}$".
> Wait — that's actually 4 occurrences. Let me list them:
> 1. `\paragraph{The action of $\Phiconf{}$` (was $\Phiphase{}$)
> 2. `The functor $\Phiconf{}$ acts` (was $\Phiphase{}$)
> 3. `\Phiconf{}\lensob M=` in eqn.Phi_on_obs (was $\Phiphase{}$)
> 4. `A position in $\Phiconf{}\lensob M$` (was $\Phiphase{}$)
>
> All other text, the equation, and the prose are character-for-character
> identical.

```latex

\paragraph{The action of $\Phiconf{}$ on morphisms.}
Describing the action of $\Phiconf{}$ on morphisms will extend to the end of this section, \cref{sec.configuration_dynamics}. Let $(V,\sharpR_V):\rvect$ and let
$f\colon V\cdot\lensob M\to\lensob N$
be a morphism in $\srw$, i.e.\ a tuple $\left(\binom{\inpt f}{\outp f},U\right)$ as in \eqref{eqn.para_potential_lens_maps}:
\begin{equation}\label{eqn.para_potential_lens_maps}
\outp f\colon V\times\outp M\to\outp N,\qquad
\inpt f\colon V\times\outp M\times\inpt N\to\inpt M,\qquad
U\colon V\times\outp M\times\inpt N\to\rr.
\end{equation}
It is sent by $\Phiconf{}$ to a $[\Phiconf{}\lensob M,\Phiconf{}\lensob N]$-coalgebra whose carrier is the underlying set of $V$,
\begin{equation}\label{eqn.state_space_conf}
S\coloneqq\absval{V};
\end{equation}
we write $x\in S=|V|$. The state update below uses the (possibly basepoint-varying) sharp $\sharpR_x$ on $V$ from \cref{def.rvect}.
```
> This block is a hybrid of phase 2586–2603 and conf 2718–2725.
> Specifically:
>
> Lines "Describing...as in \eqref{eqn.para_potential_lens_maps}:" and the
> display equation eqn.para_potential_lens_maps: from phase 2586–2593, with
> $\Phiphase{}$ → $\Phiconf{}$ ×1, \cref{sec.phase_dynamics} →
> \cref{sec.configuration_dynamics}.
>
> "It is sent by...carrier is the underlying set of $V$,": from phase
> 2595, with $\Phiphase{}$ → $\Phiconf{}$ ×2, "$T^*V$" → "$V$".
>
> eqn.state_space_conf display, "we write..." sentence, and sharp
> sentence: VERBATIM conf 2722–2725.
>
> DELETED from phase: eqn.state_space ($S:=|T^*V|$), the $s=(x,\xi)$
> notation, the "Although the coalgebra..." sentence, eqn.sharp_S, and
> "specializing \eqref{eqn.canonical_sharp}." These are phase-only.

```latex

We now unpack the coalgebra function itself,
\[
S\To{\Phiconf{}(V,\sharpR_V,f)}
\left[\Phiconf{}\lensob M,\Phiconf{}\lensob N\right]\tri S.
\]
Given a state $x\in S$ and a position $a\coloneqq(\outp m,\omega_M):\outp M\times\Omega(\inpt M)$, define the output point using $\outp{f}$ from \eqref{eqn.para_potential_lens_maps}:
\begin{equation}\label{eqn.outpn}
\outp n\coloneqq\outp f(x,\outp m)
\end{equation}
and the output covector field $\omega_N\colon\inpt N\to T^*\inpt N$ using the rest of \eqref{eqn.para_potential_lens_maps}:
\begin{equation}\label{eqn.omegaprime}
\omega_N(\inpt n)\coloneqq(\inpt f(x,\outp m,\blank))^*\omega_M\big|_{\inpt n}\;+\;d(U(x,\outp m,\blank))\big|_{\inpt n}.
\end{equation}
The first term is the pullback of $\omega_M$ along the partial map $\inpt f(x,\outp m,\blank)\colon\inpt N\to\inpt M$; the second is the differential of the potential $U(x,\outp m,\blank)\colon\inpt N\to\rr$ at $\inpt n$, in the sense of \eqref{eqn.differential}.%
\footnote{The $+1$ that turns the second summand into $dU$ comes from \eqref{eqn.d_potential}; the $+$ between summands is the cotangent splitting $T^*(\rr\times\inpt M)\cong T^*\rr\oplus T^*\inpt M$ (\cref{sec.manifolds_notation}).} Thus the readout position is the pair,
\[
b\coloneqq\bigl(\outp n,\,\omega_N\bigr)\;\in\;\outp N\times\Omega(\inpt N).
\]
```
> MODIFIED phase 2605–2622. Changes:
> - $\Phiphase{}$ → $\Phiconf{}$ ×2 (in the coalgebra-function display)
> - "$s\coloneqq(x,\xi)\in S$" → "$x\in S$"
>
> Everything else — eqn.outpn, eqn.omegaprime, the prose, the footnote,
> the readout $b$ — is character-for-character identical. These formulas
> depend on $x$ alone.

```latex


Now given a direction $(\xi_N,\inpt n):T^*_{\outp n}\outp N\times\inpt N=\Phiconf{}\lensob N[b]$, the coalgebra function $\Phiconf{}(V,\sharpR_V,f)$ at $(x,a)$ produces a direction in $T^*_{\outp m}\outp M\times\inpt M$ as follows. Let
\begin{equation}\label{eqn.inptm}
\inpt m\coloneqq\inpt f(x,\outp m,\inpt n)
\end{equation}
and define
\begin{equation}\label{eqn.bigtheta}
(\xi_V,\,\xi_M,\,\xi_{\inpt N})\coloneqq (T_{(x,\outp m)}\outp f)^\top\xi_N \;+\; (T_{(x,\outp m,\inpt n)}\inpt f)^\top\omega_M(\inpt m) \;+\; dU\big|_{(x,\outp m,\inpt n)}\;
\end{equation}
where $(\xi_V,\,\xi_M,\,\xi_{\inpt N}):V^*\oplus T^*_{\outp m}\outp M\oplus T^*_{\inpt n}\inpt N$.%
\footnote{Each summand is a cotangent pullback: $\xi_N$ along $\outp f$, $\omega_M(\inpt m)$ along $\inpt f$, and $+1$ along $U$ (via $\potd$, \eqref{eqn.d_potential}); the $+$'s are the cotangent splitting of $V\times\outp M\times\inpt N$ (\cref{sec.manifolds_notation}), morally the domain of the maps in \eqref{eqn.para_potential_lens_maps}. Throughout, we silently use the canonical chart identification \eqref{eqn.tangent_vec} to treat covectors at points of vector spaces as elements of the dual.}
Note that the first summand naturally lands in $V^*\oplus T^*_{\outp m}\outp M$ and has been extended by $0$ in the remaining $\inpt N$-factor, so by \eqref{eqn.omegaprime} we have $\omega_N(\inpt n)=\xi_{\inpt N}$.
```
> MODIFIED phase 2625–2635. Changes:
> - $\Phiphase{}$ → $\Phiconf{}$ ×2
> - "$(s,a)$" → "$(x,a)$"
>
> Everything else — eqn.inptm, eqn.bigtheta, the types, the footnote, the
> $\xi_{\inpt N}=\omega_N(\inpt n)$ note — is character-for-character
> identical.

```latex

All of the work has now been done: the coalgebra at $(x,a)$ on $(\xi_N,\inpt n)$ returns the direction
\[
(\xi_M,\,\inpt m):T^*_{\outp m}\outp M\times\inpt M=\Phiconf{}\lensob M[a]
\]
and updates the state (from its original $x$) to
\begin{equation}\label{eqn.state_update_gradient}
x+\sharpR_x(\xi_V),
\end{equation}
which is the on-directions component of $\theta_V$ \eqref{eqn.directions_sharp} applied to the covector $\xi_V\in V^*$ of \eqref{eqn.bigtheta}. In other words, the state is updated by summing three covectors pulled back along the maps in \eqref{eqn.para_potential_lens_maps}---$\xi_N$ along $\outp f$, $\omega_M(\inpt m)$ along $\inpt f$, and $+1$ along $U$ (yielding $dU$)---projecting to the $V^*$-component, sharpening to a vector via $\sharpR_x$, and adding to the original state.
```
> This block is a hybrid of phase 2637–2641 and conf 2733–2736.
>
> "All of the work...returns the direction": from phase 2637, with
> "$(s,a)$" → "$(x,a)$".
>
> Direction display: from phase 2638–2639, with $\Phiphase{}$ →
> $\Phiconf{}$.
>
> "and updates the state (from its original $x$) to": from phase 2641,
> with "$s=(x,\xi)$" → "$x$".
>
> eqn.state_update_gradient display and the two-sentence explanation:
> VERBATIM conf 2733–2736.
>
> DELETED: the phase-specific material at 2643–2685 (LHS/RHS breakdown,
> rmk.constant_inverse_mass_hamiltonian, rmk.euler_energy). These belong
> in the phase section only.

```latex

All in all, one could tersely denote the coalgebra map as follows:
\begin{multline*}
\Phiconf{}(V,\sharpR_V,f)\colon
x\mapsto
(\outp m,\omega_M)\mapsto
\Big(
	(\outp n,\omega_N),
	(\xi_N,\inpt n)\mapsto\\
	\big(
		(\xi_M,\inpt m),
		x+\sharpR_x(\xi_V)
	\big)
\Big),
\end{multline*}
where $\outp n$, $\omega_N$, $\xi_M$, $\xi_V$, and $\inpt m$ are as in \eqref{eqn.outpn}, \eqref{eqn.omegaprime}, \eqref{eqn.bigtheta}, and \eqref{eqn.inptm}.

We can now fulfill the promise from \cref{sec.related_cls}.
```
> VERBATIM conf 2738–2754. No changes.

```latex

\begin{proposition}[Eulerized submersion lenses]\label{prop.euler_submersion_lenses}
```
> From here through the end of the proof (current conf 2756–2841):
> VERBATIM. No changes. (This is ~85 lines; not reproduced here to
> save space, but every character is identical.)

```latex
\end{proof}

Applications of $\Phiconf{}$ appear in \cref{sec.newton_warmup} (Newton's method) and \cref{sec.dl_warmup} (gradient descent and backpropagation), and applications of $\Phiphase{}$ to harmonic-oscillator particles---recovering the discrete wave equation on a chain (\cref{sec.wave_equation}) and the graph Laplacian on an arbitrary finite directed graph (\cref{sec.graph_laplacian})---follow.
```
> VERBATIM conf 2843. No changes.

---

### Section B: New phase section (goes second)

```latex

%--------------------------------------------------------------------
\section{Phase-space dynamics \texorpdfstring{$\Phiphase{}$}{Phi phase}}\label{sec.phase_dynamics}
%--------------------------------------------------------------------

For the phase lift, the functor $\Psi_{\lift_{\phase}}$ presents a $\cotof{V}$-parameter by the store polynomial on $S\coloneqq\absval{T^*V}$:
\[
S\yon^S\To{\theta_{T^*V}}\cotof{T^*V}\To{\rho_V}\cotof{V}.
\]
A state consists of a position and a momentum $(x,\xi)\in T^*V$, and an incoming covector $\xi'\in T^*_xV$ updates that state to $(x+\sharpR_x(\xi),\,\xi-\xi')$
 by \eqref{eqn.phase_lift_update}. The readout and backward pass of the coalgebra $\Phiphase{}(V,\sharpR_V,f)$ are identical to the configuration case---their formulas \eqref{eqn.outpn}, \eqref{eqn.omegaprime}, \eqref{eqn.inptm}, \eqref{eqn.bigtheta} depend only on the parameter position $x$, and the phase lift maps $(x,\xi)\mapsto x$ on positions by \eqref{eqn.phase_lift_decomp}. What changes is the state space and the state update; we unpack these below.
```
> MODIFIED phase 2561–2569. The first four lines through "by
> \eqref{eqn.phase_lift_update}." are VERBATIM. Then:
>
> DELETED: "But the majority of what takes place under $\Phi_\lift$ is
> still compressed within the $\Phi'$ factor from
> \cref{lem.potlens_to_para_poly}. So we now unpack $\Phiphase{}$ in
> total, tracing each term and sign in the resulting formulas back to the
> definitions that produced it."
>
> INSERTED (NEW): "The readout and backward pass of the coalgebra
> $\Phiphase{}(V,\sharpR_V,f)$ are identical to the configuration
> case---their formulas \eqref{eqn.outpn}, \eqref{eqn.omegaprime},
> \eqref{eqn.inptm}, \eqref{eqn.bigtheta} depend only on the parameter
> position $x$, and the phase lift maps $(x,\xi)\mapsto x$ on positions
> by \eqref{eqn.phase_lift_decomp}. What changes is the state space and
> the state update; we unpack these below."

```latex

\paragraph{The action of $\Phiphase{}$ on objects.}
The functor $\Phiphase{}$ acts on objects exactly as $\Phiconf{}$ in \eqref{eqn.Phi_on_obs}: a position in $\Phiphase{}\lensob M$ is a pair $(\outp m,\omega)$ and a direction at $(\outp m,\omega)$ is a pair $(\xi,\inpt m)$, with the same types as in the configuration case.
```
> MODIFIED conf 2715–2716. Changes (4 swaps + 1 phrase):
> - $\Phiconf{}$ → $\Phiphase{}$ ×3 (paragraph header, "The functor",
>   "A position in")
> - $\Phiphase{}$ → $\Phiconf{}$ ×1 ("exactly as $\Phiconf{}$")
> - "the phase-space case" → "the configuration case"

```latex

\paragraph{The action of $\Phiphase{}$ on morphisms.}
Describing the action of $\Phiphase{}$ on morphisms will extend to the end of this section, \cref{sec.phase_dynamics}. Let $(V,\sharpR_V):\rvect$ and let
$f\colon V\cdot\lensob M\to\lensob N$
be a morphism in $\srw$, i.e.\ a tuple $\left(\binom{\inpt f}{\outp f},U\right)$ as in \eqref{eqn.para_potential_lens_maps}. It is sent by $\Phiphase{}$ to a $[\Phiphase{}\lensob M,\Phiphase{}\lensob N]$-coalgebra whose carrier is the underlying set of $T^*V$,
\begin{equation}\label{eqn.state_space}
S\coloneqq\absval{T^*V}\cong V\oplus V^*;
\end{equation}
we write $s=(x,\xi)\in S$ for position $x\in V$ and momentum $\xi\in V^*$. Although the coalgebra remembers only the set $S$, the state update below uses the canonical symplectic pairing on $T^*V$. Its sharp map is
\begin{equation}\label{eqn.sharp_S}
\sharpS_S\colon S^*\to S,\qquad (\xi',x')\mapsto(x',-\xi'),
\end{equation}
specializing \eqref{eqn.canonical_sharp}.
```
> MODIFIED phase 2586–2603. Changes:
> - "as in \eqref{eqn.para_potential_lens_maps}**:**" → "as in
>   \eqref{eqn.para_potential_lens_maps}**.**" (colon → period)
> - DELETED: the 5-line display equation for eqn.para_potential_lens_maps
>   (it is now defined in the configuration section).
>
> Everything else — $\Phiphase{}$ ×3, \cref{sec.phase_dynamics},
> eqn.state_space, the $s=(x,\xi)$ notation, the "Although the
> coalgebra..." sentence, eqn.sharp_S — is VERBATIM from phase.

```latex

We now unpack the coalgebra function itself,
\[
S\To{\Phiphase{}(V,\sharpR_V,f)}
\left[\Phiphase{}\lensob M,\Phiphase{}\lensob N\right]\tri S.
\]
Given a state $s\coloneqq(x,\xi)\in S$ and a position $a\coloneqq(\outp m,\omega_M):\outp M\times\Omega(\inpt M)$, the output point $\outp n$, output covector field $\omega_N$, and readout position $b=(\outp n,\omega_N)\in\outp N\times\Omega(\inpt N)$ are defined by \eqref{eqn.outpn} and \eqref{eqn.omegaprime}. Given a direction $(\xi_N,\inpt n):T^*_{\outp n}\outp N\times\inpt N=\Phiphase{}\lensob N[b]$, the coalgebra function $\Phiphase{}(V,\sharpR_V,f)$ at $(s,a)$ produces the direction $(\xi_M,\inpt m):T^*_{\outp m}\outp M\times\inpt M=\Phiphase{}\lensob M[a]$ via \eqref{eqn.inptm} and \eqref{eqn.bigtheta}, exactly as in \cref{sec.configuration_dynamics}---the formulas depend on $x$ alone, and the phase lift maps $(x,\xi)\mapsto x$ on positions by \eqref{eqn.phase_lift_decomp}. The only difference is in the state update: starting from $s=(x,\xi)$, the state is updated to
\begin{equation}\label{eqn.state_update}
s+\sharpS_S(\xi_V,\sharpR_x(\xi))=\bigl(x+\sharpR_x(\xi),\,\xi-\xi_V\bigr).
\end{equation}
```
> This block replaces the explicit readout+backward at phase 2605–2643.
>
> "We now unpack...itself," + coalgebra-function display: VERBATIM phase
> 2605–2608.
>
> "Given a state $s\coloneqq(x,\xi)\in S$...": NEW deferral paragraph.
> Modeled on current conf 2732 but with roles reversed. All equation
> references are by label: \eqref{eqn.outpn}, \eqref{eqn.omegaprime},
> \eqref{eqn.inptm}, \eqref{eqn.bigtheta}, \eqref{eqn.phase_lift_decomp}.
> The section reference \cref{sec.configuration_dynamics} is for the
> reader's convenience; the equation labels carry the rigor.
> The justification "the formulas depend on $x$ alone, and the phase lift
> maps $(x,\xi)\mapsto x$ on positions by \eqref{eqn.phase_lift_decomp}"
> is NEW; it explains WHY the deferral is valid.
>
> eqn.state_update: VERBATIM phase 2642–2643.
>
> DELETED from phase: the explicit definitions of eqn.outpn (2611–2612),
> eqn.omegaprime (2615–2616), the prose+footnote for omegaprime
> (2618–2619), the readout $b$ display (2620–2622), the eqn.inptm
> definition (2626–2627), the eqn.bigtheta definition (2630–2631), the
> types+footnote for bigtheta (2633–2634), and the $\xi_{\inpt N}$ note
> (2635). All of these are now in the configuration section.

```latex
We will now break down \cref{eqn.state_update}, which is the phase lift \eqref{eqn.phase_lift_update} with the substitution $\xi'=\xi_V$.

Its left-hand side records where the three pieces of this update come from. The sum $s+\sharpS_S(\blank)$ is the exponential of the reactive vector space $T^*V$ on the underlying set $S$, \eqref{eqn.flow_cot}; the use of $\sharpS_S$ comes from the canonical symplectic pairing on $T^*V$, \eqref{eqn.canonical_sharp}, which is constant in $s$ regardless of variation in $\sharpR_V$ (\cref{rmk.constant_canonical_sharp}); and the pair $(\xi_V,\sharpR_x(\xi))\in T^*_sS$ comes from the phase lift \eqref{eqn.phase_lift_decomp} at $(x,\xi)$. 

The right-hand side of \cref{eqn.state_update} is the computation: \eqref{eqn.canonical_sharp} gives $\sharpS_S(\xi_V,\sharpR_x(\xi))=(\sharpR_x(\xi),-\xi_V)$, then componentwise addition with $s=(x,\xi)$ produces $(x+\sharpR_x(\xi),\,\xi-\xi_V)$.

\begin{remark}[Hamilton's equations in the constant symmetric case]\label{rmk.constant_inverse_mass_hamiltonian}
In this remark we aim to justify the Hamiltonian terminology that we allude to elsewhere in the paper. The assumptions that make the dynamics Hamiltonian are written in bold.

Suppose \textbf{the domain and codomain interfaces are closed}, i.e.\ $\inpt M=\outp M=\inpt N=\outp N=\rr^0$, so that in particular $\xi_N=0$ and $\omega_M=0$ and $U\colon V\to\rr$ depends only on $x$. Then \eqref{eqn.bigtheta} gives $\xi_V=dU|_x$. If moreover \textbf{the sharp is constant}, $\sharpR_x=\sharpR_0$, then \eqref{eqn.state_update} becomes
\[
s+\sharpS_S(dU|_x,\sharpR_0(\xi))
=
(x+\sharpR_0(\xi),\,\xi-dU|_x),
\]
which is the explicit Euler step for the vector field
\[
\dot x=\sharpR_0(\xi),
\qquad
\dot\xi=-dU|_x.
\]
In the one-dimensional mass=$m$ case this reads $\dot x=\xi/m$ and $\dot\xi=-dU|_x$, the familiar (velocity, force) form of Newton's second law, with $\xi=m\dot x$ the usual momentum.

Finally, when \textbf{the sharp is symmetric}, in the sense that $\xi'(\sharpR_0(\xi))=\xi(\sharpR_0(\xi'))$ for all $\xi,\xi'\in V^*$, this vector field is \emph{Hamiltonian} meaning that it is the symplectic sharp applied to the derivative of some function, namely
\[
H(x,\xi)\coloneqq \tfrac12\xi(\sharpR_0(\xi))+U(x).
\]
Indeed, the symmetry condition and the linearity of $\sharpR$ give $dH|_{(x,\xi)}=(dU|_x,\sharpR_0(\xi))\in V^*\oplus V$, and applying the canonical symplectic sharp \eqref{eqn.sharp_S} recovers the vector field:
\[
\sharpS_S(dH|_{(x,\xi)})=(\sharpR_0(\xi),-dU|_x)=(\dot{x},\dot{\xi}).
\]
In particular the flow conserves $H$, by \cref{rmk.symplectic_perpendicular}.\qedhere
\end{remark}

\begin{remark}[Euler step and energy non-conservation]\label{rmk.euler_energy}
\Cref{eqn.state_update} can be read two ways. As the defining equation of a discrete dynamical system, it is exact: that's the perspective of \cref{sec.wave_equation}, where the recurrence \eqref{eqn.recurrence} \emph{is} the discrete wave equation we want. But as a numerical time-stepper for the corresponding continuous phase-space dynamics---Hamiltonian in the standard closed, constant inverse-mass case (\cref{rmk.constant_inverse_mass_hamiltonian})---it is not adequate over many timesteps: explicit Euler integration is not symplectic, so the simulated trajectory accumulates energy drift and diverges from the true flow. For example, on the harmonic oscillator of \cref{sec.wave_equation}, the simulated energy grows without bound for any positive step size \cite[Ch.~I]{hairer2006geometric}.

The configuration analog \eqref{eqn.state_update_gradient} (\cref{sec.configuration_dynamics}) is also explicit Euler, but on a gradient flow rather than a Hamiltonian one; on Euclidean parameter spaces the constant case \eqref{eqn.learning_sharp} is vanilla gradient descent with learning rate $\eta_{\mathrm{LR}}$, which is a standard, well-behaved update for sufficiently small $\eta_{\mathrm{LR}}$. 

If the conjecture of \cref{rmk.org_N} works out---that multi-stage integrators can be built into the bicategories $\org^{(K)}$---then the above energy issue would be remedied by a velocity-Verlet refinement at $K=2$.\qedhere
\end{remark}
```
> VERBATIM phase 2645–2685. No changes. (The reference to
> \cref{sec.configuration_dynamics} in rmk.euler_energy was already
> present in the original and remains correct — it is now a backward
> reference instead of a forward one.)

```latex

All in all, one could tersely denote the coalgebra map as follows:
\begin{multline*}
\Phiphase{}(V,\sharpR_V,f)\colon
(x,\xi)\mapsto
(\outp m,\omega_M)\mapsto
\Big(
	(\outp n,\omega_N),
	(\xi_N,\inpt n)\mapsto\\
	\big(
		(\xi_M,\inpt m),
		(x+\sharpR_x(\xi),\,\xi-\xi_V)
	\big)
\Big),
\end{multline*}
where $\outp n$ is defined in \eqref{eqn.outpn}, $\omega_N$ in \eqref{eqn.omegaprime}, $\xi_M$ and $\xi_V$ in \eqref{eqn.bigtheta}, and $\inpt m$ in \eqref{eqn.inptm}.
```
> VERBATIM phase 2687–2701. No changes.

---

## Part 2: Cross-reference edits elsewhere in the file

There are exactly four lines outside the replaced range that need editing.
Each is specified as an exact old→new substitution.

### Edit 1: Line 631

**Old (VERBATIM):**
```
unpacked in full detail in \cref{sec.phase_dynamics,sec.configuration_dynamics}.
```

**New:**
```
unpacked in full detail in \cref{sec.configuration_dynamics,sec.phase_dynamics}.
```

> Change: reorder the two arguments to \cref so the first-listed section
> comes first in the document. The surrounding sentence already says
> "configuration and phase" in that order, so no other change is needed.

### Edit 2: Line 2306

**Old (VERBATIM):**
```
\Cref{sec.phase_dynamics,sec.configuration_dynamics} unpack the differential geometry underlying $\Phiphase{}$ and $\Phiconf{}$ in full detail.
```

**New:**
```
\Cref{sec.configuration_dynamics,sec.phase_dynamics} unpack the differential geometry underlying $\Phiconf{}$ and $\Phiphase{}$ in full detail.
```

> Changes: (1) reorder \cref arguments, (2) swap $\Phiphase{}$ and
> $\Phiconf{}$ so the order matches the sections.

### Edit 3: not needed

Line 2425 (\cref{sec.configuration_dynamics} in rmk.cotangent_learners):
no change. It was a forward reference before and remains a forward
reference after (the remark is in sec.lift_semantics, which precedes both
dynamics sections).

### Edit 4: not needed

Lines 3069 and 3248 (\cref{sec.phase_dynamics} in sec.wave_equation and
sec.graph_laplacian): no change. The phase section still exists with the
same label, just in a later position.

---

## Rigour checklist

Before declaring the task complete, verify each item:

- [ ] Every displayed equation in both sections has a `\label`.
- [ ] Every "as in" or "exactly as" phrase cites a specific `\eqref`
      or `\cref`, not just a vague reference.
- [ ] The two footnotes from eqn.omegaprime and eqn.bigtheta appear
      in the configuration section (where they are now defined).
- [ ] The note "$\omega_N(\inpt n)=\xi_{\inpt N}$" (by
      \eqref{eqn.omegaprime}) appears in the configuration section.
- [ ] The new phase section's deferral paragraph cites all four
      shared equations by label: \eqref{eqn.outpn},
      \eqref{eqn.omegaprime}, \eqref{eqn.inptm}, \eqref{eqn.bigtheta}.
- [ ] The new phase section's deferral paragraph explains WHY the
      shared formulas carry over: cites \eqref{eqn.phase_lift_decomp}
      and states "the formulas depend on $x$ alone."
- [ ] rmk.euler_energy's reference to \cref{sec.configuration_dynamics}
      is now a backward reference (conf precedes phase). Verify no
      wording implies it is forward.
- [ ] No equation label is defined in two places.
- [ ] No equation label is referenced before it is defined, unless
      it is a deliberate forward reference via \cref that will resolve.
- [ ] The terse summary in each section indexes every equation label
      it uses.
- [ ] prop.euler_submersion_lenses remains in the configuration
      section and all its internal \eqref and \cref references resolve.
- [ ] pdflatex compiles without "undefined reference" warnings for any
      label in the replaced range.

---

## Changelog

*To be filled in by whoever performs the changes. For each edit, record:*

| # | What | Old location | New location | Wording change? | Rationale |
|---|------|-------------|-------------|-----------------|-----------|
| | | | | | |
