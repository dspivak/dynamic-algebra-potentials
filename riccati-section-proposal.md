# Proposal: add a "matrix Riccati recursion" section to `dynamic-algebra-potentials`

**For the executing Claude.** This spec adds a ~1.5-page section to the applications
chapter. It is self-contained, but you MUST open the live `.tex` file first and match
its actual macros, theorem-environment names, and `\label`s. Re-derive the one
computation yourself before committing it. Read the "claim discipline" section twice.

---

## 0. One-paragraph summary

Show that the phase integrator `\Phiphase`, applied to a *frame* of harmonic
oscillators (a closed quadratic system on a matrix-valued parameter) and read out
through its Lagrangian subspace `P = Y X^{-1}`, realizes a discrete **matrix Riccati
recursion**, whose measurement-update half is the **exact information-form Bayesian
precision update** `Π ↦ Π + G`. No new datum, interpretation, or integrator is
introduced — it reuses the existing smooth datum, smooth interpretation, and phase
integrator. The full Kalman/LQR filter (the drift term) is explicitly left as future
work.

---

## 1. CLAIM DISCIPLINE — non-negotiable

The author's standing rule: **never state as fact anything not internally verified.**

1. **Do NOT write "the Kalman filter" as the achieved result.** The achieved, provable
   claims are exactly two:
   - (a) the readout evolves by the matrix Riccati map `Ric_S` — which we **define in
     the paper**, so the claim is self-contained and needs no hedge;
   - (b) the measurement-update factor is exactly `Π ↦ Π + G` (precision addition).
2. **The full Kalman/LQR recursion is scoped out as future work**, with the honest
   reason stated: the system drift `A` requires a position–momentum cross term
   `ξᵀ A q` in the Hamiltonian, which is not the differential of a position-only
   potential `U: Q → ℝ`. Do not paper over this.
3. **Because we define `Ric_S` ourselves, the main proposition is a 2-line computation.**
   Re-derive it independently before writing. Do not assert it from this document alone.
4. **Citations: do NOT fabricate a definition/equation number.** See §5.

If at any step the computation does not check out as written here, STOP and report the
discrepancy rather than adjusting claims to fit.

---

## 2. Placement

Insert a new `\section{...}\label{sec.riccati}` in the applications chapter
**immediately before** `\section{Graph Laplacian on a directed graph}` (label
`sec.graph_laplacian`) — i.e. directly after the wave-equation section. It is the
sibling of the wave equation: that section runs `\Phiphase` on a *chain* of harmonic
particles; this one runs it on a *frame* of them.

Acceptable alternative (author's choice): place it **last** in the chapter, immediately
before `\section*{Conclusion}`, as a closing "and control/estimation too" reading.
Recommend the first option; mention the alternative to the author.

---

## 3. Notation / macros / environments — CONFIRM AGAINST LIVE FILE

Use the paper's existing macros (confirm names in the live file before using):
`\Phiphase`, `\phase`, `\cot`, `\sharpR`, `\rvect`, `\sarr`, `\pc`, `\rr`, `\bang`,
`\absval{...}`, `\cref`.

Confirm/needed, do NOT assume:
- **Theorem environments.** The body uses `\begin{definition}`, `\begin{proposition}`,
  `\begin{remark}` (with cleveref names). Use whatever the paper actually uses; do not
  use `definitionx`/etc. directly unless that is the body convention.
- **`\tr`** (trace) and **`\Ric`** may not exist. If not, add
  `\DeclareMathOperator{\tr}{tr}` and `\DeclareMathOperator{\Ric}{Ric}` near the other
  `\DeclareMathOperator`s, or use `\operatorname{...}`.
- Verify these `\label`s exist and are the right targets before `\cref`-ing them:
  `sec.wave_equation`, `sec.phase_integrators`, `eqn.phase_update`,
  `eqn.presented_position`, `prop.closed_conservation`, `def.rvect`,
  `ex.euclidean_sharp`, `def.arrangement_terminology`, `rmk.rmfdc_generalization`,
  `rmk.multistage`. If a label differs, fix the `\cref`, do not invent.

---

## 4. Ready-to-adapt LaTeX draft (~1.5 pp)

Adapt environment names/macros to the live file. The math is verified; transcribe it
faithfully and re-check the proof.

```latex
\section{A matrix Riccati recursion}\label{sec.riccati}

The wave equation (\cref{sec.wave_equation}) ran the phase integrator $\Phiphase$ on a
chain of harmonic particles. Here we run it on a \emph{frame} of $n$ such particles and
read out the Lagrangian subspace they span; in those coordinates the same phase
dynamics is a discrete matrix Riccati recursion. We introduce no new datum,
interpretation, or integrator: the arrangement is a closed quadratic system in $\sarr$
and the dynamics is $\Phiphase$.

\paragraph{The arrangement.}
Fix $n\geq 1$ and set $Q\coloneqq\rr^{n\times n}$, regarded as a frame of $n$ column
vectors in $\rr^n$. Let $G,\Lambda\in\rr^{n\times n}$ be symmetric. Equip $Q$ with the
constant reaction $\sharpR(\Xi)\coloneqq G\Xi$ (\cref{def.rvect}; the Euclidean sharp of
\cref{ex.euclidean_sharp} applied columnwise) and the quadratic potential
\[
  U\colon Q\to\rr,\qquad U(X)\coloneqq\tfrac12\tr(X^\top\Lambda X),
  \qquad dU|_X=\Lambda X .
\]
This is a closed system $f=\bigl((Q,\sharpR),\bang,\bang,U\bigr)\colon I\to I$ in $\sarr$
(\cref{def.arrangement_terminology}).

\paragraph{The dynamics.}
By \cref{eqn.phase_update}, $\Phiphase(f)$ carries state $(X,Y)\in\absval{T^*Q}\cong
\rr^{n\times n}\times\rr^{n\times n}$ and, being closed, updates by the presented
position $\tilde X=X+GY$ (\cref{eqn.presented_position}) and the restoring covector
$dU|_{\tilde X}=\Lambda\tilde X$:
\[
  X^+=X+GY,\qquad Y^+=Y-\Lambda X^+ .
\]
Equivalently $\binom{X^+}{Y^+}=S\binom{X}{Y}$ with
\[
  S=\begin{pmatrix}I&G\\-\Lambda&I-\Lambda G\end{pmatrix}
   =\begin{pmatrix}I&0\\-\Lambda&I\end{pmatrix}
    \begin{pmatrix}I&G\\0&I\end{pmatrix}.
\]
As a product of two symmetric shears $S$ is symplectic; this is the conservation of the
canonical pairing recorded in \cref{prop.closed_conservation}.

\paragraph{The Riccati readout.}

\begin{definition}\label{def.riccati_map}
For a symplectic block matrix
$S=\bigl(\begin{smallmatrix}S_{11}&S_{12}\\S_{21}&S_{22}\end{smallmatrix}\bigr)$, the
\emph{matrix Riccati map} is the partial map on symmetric matrices
\[
  \Ric_S(P)\coloneqq(S_{21}+S_{22}P)(S_{11}+S_{12}P)^{-1},
\]
defined wherever $S_{11}+S_{12}P$ is invertible. It is the action of $S$ on the
Lagrangian Grassmannian in the chart $P\mapsto\operatorname{span}\binom{I}{P}$
\cite{REF}.
\end{definition}

\begin{proposition}\label{prop.riccati}
On the locus where $X$ is invertible, the readout $P\coloneqq YX^{-1}$ of the closed
system above evolves by the matrix Riccati map of its symplectic $S$:
\[
  P^+=\Ric_S(P)=P(I+GP)^{-1}-\Lambda .
\]
\end{proposition}
\begin{proof}
Write $Y=PX$. From $X^+=X+GY=(I+GP)X$ we get
$Y(X^+)^{-1}=PX\bigl((I+GP)X\bigr)^{-1}=P(I+GP)^{-1}$, hence
\[
  P^+=Y^+(X^+)^{-1}=\bigl(Y-\Lambda X^+\bigr)(X^+)^{-1}
     =P(I+GP)^{-1}-\Lambda .
\]
Substituting the blocks of $S$ into \cref{def.riccati_map} gives the same map:
$(-\Lambda+(I-\Lambda G)P)(I+GP)^{-1}=\bigl(P-\Lambda(I+GP)\bigr)(I+GP)^{-1}
=P(I+GP)^{-1}-\Lambda$.
\end{proof}

\begin{remark}[Measurement update]\label{rmk.precision_addition}
The first factor is the information-form Bayesian update. Writing $\Pi\coloneqq P^{-1}$
for the precision and using $P(I+GP)^{-1}=(P^{-1}+G)^{-1}$,
\[
  P\longmapsto P(I+GP)^{-1}\quad\text{is}\quad \Pi\longmapsto\Pi+G,
\]
the additive accumulation of measurement precision $G$ --- the same additive law by
which potentials combine in $\sarr$, here read on the covariance. The trailing
$-\Lambda$ is the prediction step set by the potential's curvature; the signature of
$\Lambda$ selects oscillatory (elliptic) versus hyperbolic dynamics.
\end{remark}

\begin{remark}[Toward the Kalman filter]\label{rmk.kalman_outlook}
\Cref{prop.riccati} realizes the precision/measurement part of filtering and the
autonomous Riccati flow, but not the full Kalman or LQR recursion. Those carry a system
drift $A$, i.e.\ a Hamiltonian with diagonal blocks
$\bigl(\begin{smallmatrix}A&\ast\\\ast&-A^\top\end{smallmatrix}\bigr)$ and hence a
position--momentum cross term $\xi^\top A q$. Such a term is not the differential of a
position-only potential $U\colon Q\to\rr$, so it lies outside the present syntax.
Realizing it would extend the adaptive-arrangement datum to admit generating-function
potentials $T^*Q\to\rr$ (cf.\ \cref{rmk.rmfdc_generalization}), or compose a linear
drift arrangement by operator splitting (cf.\ \cref{rmk.multistage}); we leave this to
future work.
\end{remark}
```

---

## 5. Citation handling (`\cite{REF}` in `def.riccati_map`)

The fractional-linear / Lagrangian-Grassmannian form of the matrix Riccati equation is
classical, but **do not invent a definition or equation number.** Options, in order of
preference:

1. Find an **open-access** source (arXiv, freely available lecture notes, or a
   diamond/OA journal) that states the symplectic action / fractional-linear form, add
   it to the `.bib`, and cite it. Verify the exact statement before citing.
2. If only a standard book fits, cite one of: Bittanti–Laub–Willems (eds.), *The Riccati
   Equation*, Springer 1991; or Lancaster–Rodman, *Algebraic Riccati Equations*, Oxford
   1995 — **without a specific theorem number unless you have verified it.**
3. If neither can be verified now, replace `\cite{REF}` with a visible
   `% TODO(citation): symplectic/Lagrangian-Grassmannian form of matrix Riccati` and
   tell the author. Do not leave a fabricated citation.

The correctness of `\cref{prop.riccati}` does **not** depend on this citation — `Ric_S`
is defined in-paper — so the citation is for context/credit only.

---

## 6. Checklist before you finish

- [ ] You re-derived `P^+ = P(I+GP)^{-1} - Λ` and confirmed it equals `Ric_S(P)`.
- [ ] You confirmed `S` is symplectic (product of two symmetric shears) and that this is
      what `prop.closed_conservation` says.
- [ ] Environment names, `\tr`, `\Ric`, `\bang`, `\absval` all match / are declared.
- [ ] Every `\cref` target exists in the live file.
- [ ] No occurrence of "Kalman filter" as an achieved result; the drift limitation is
      stated plainly in `rmk.kalman_outlook`.
- [ ] No fabricated citation; `\cite{REF}` resolved or replaced with a visible TODO.
- [ ] The section compiles and is ~1.5 pages.
