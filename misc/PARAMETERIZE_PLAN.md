# Plan: parameterize the dynamics functor and add the gradient-flow case

## Context

`/Users/davidspivak/VersionControl/dynamic-algebra-potentials/dynamic-algebra-potentials.tex` currently develops one main functor $\Phi\colon\potlens\to\org$ via the chain $\cint\then\leg\then\dyn$, with `lem.poly_to_org` (the dynamical realization) and `thm.functor` (the composite) stating the symplectic-Hamiltonian case. The author has decided to:

- Promote both `lem.poly_to_org` and `thm.functor` to a *parameterized* form indexed by strong monoidal functors $F\colon\pvect\to\smset_\cong$ together with a compatible natural transformation $\eta_F$.
- Exhibit two natural members: $\Phi^{\mathrm{symp}}$ (Hamilton flow) and $\Phi^{\mathrm{grad}}$ (gradient flow).
- Rename the existing $\Phi$ to $\Phi^{\mathrm{symp}}$ throughout — no bare $\Phi$ as default.
- Add a new subsection `sec.gradient_dynamics` defining the gradient-flow case explicitly and walking through its specifics.
- Add a one-sentence forward pointer to `ch.deep_learning` (chapter not yet written; cref will be intentionally undefined for now).

The implementing LLM should execute the changes below in order, build, and report.

## Inputs to read

Before editing, read these to understand the current state:

1. The paper itself: `/Users/davidspivak/VersionControl/dynamic-algebra-potentials/dynamic-algebra-potentials.tex` (~2540 lines). Focus on:
   - `\section{Dynamic compositional structures}` (`sec.dynamic_structures`) and its subsections, especially `sec.org`, `sec.para_general`, `sec.org_as_para`, and `sec.deep_learning` (the forward pointer; line ~1361).
   - `\chapter{Potentialized lenses}` (`ch.potentials`) starts ~line 1370.
   - `\section{The dynamics of potentialized lenses}` (`sec.potential_lenses_to_dynamics`, line ~2030) — this is the main editing site.
     - `lem.potlens_to_para_poly` (defines $\cint$, line ~2070).
     - `lem.para_rho` (defines $\leg$, line ~2189).
     - `lem.poly_to_org` (defines $\dyn$, line ~2200) — **PRIMARY EDIT TARGET**.
     - `thm.functor` (defines $\Phi$, line ~2220) — **PRIMARY EDIT TARGET**.
     - The unpacking of $\Phi$ on objects/morphisms (lines ~2240–2335).
     - `eqn.state_update` and its footnote (line ~2196 and its footnote).
   - `\chapter{Example: the wave equation}` (`ch.spring`, line ~2335).
     - `sec.spring_intro` (line ~2335) — needs a one-sentence framing edit.
     - `eqn.potlens_composite_final` (line ~2455) — the wave-equation update formula, references $\Phi$.

2. `/Users/davidspivak/VersionControl/dynamic-algebra-potentials/VOCAB.md` — types and functors that are in scope.

3. `/Users/davidspivak/VersionControl/dynamic-algebra-potentials/RIEMANN_GRADIENT_PROPOSAL.md` — earlier proposal that this plan supersedes (some content may be reused, but the plan below is binding).

4. Style memory:
   - `/Users/davidspivak/.claude/projects/-Users-davidspivak-VersionControl-dynamic-algebra-potentials/memory/feedback_voice.md` — variable conventions, proof style, $\emph$ discipline, etc.
   - `/Users/davidspivak/.claude/projects/-Users-davidspivak-VersionControl-dynamic-algebra-potentials/memory/feedback_short_statements.md` — keep theorem statements punchy.
   - `/Users/davidspivak/.claude/projects/-Users-davidspivak-VersionControl-dynamic-algebra-potentials/memory/feedback_proof_style.md` — annotated `align*` for multi-step calculations.
   - `/Users/davidspivak/.claude/projects/-Users-davidspivak-VersionControl-dynamic-algebra-potentials/memory/feedback_notation.md` — vectors are $v$, covectors are $\xi$/$\alpha$; use `\ad` not `[-,-]`.

## Decisions made (binding)

1. **Parameterization**: indexed by strong monoidal $F\colon\pvect\to\smset_\cong$ together with a monoidal natural transformation $\eta_F\colon\Fun{Store}\circ F\Rightarrow\cot$ in $\poly$. Two natural members:
   - $F = \lvert\blank\rvert$ (underlying set), $\eta = \id_{\cot}$ (using $\cot V \cong V\yon^V = \Fun{Store}(\lvert V\rvert)$ from `prop.pnla_polynomial`). Defines $\Phi^{\mathrm{grad}}$.
   - $F = \lvert T^*\blank\rvert$, $\eta = \rho$ (Legendre projection from `lem.rho_natural`). Defines $\Phi^{\mathrm{symp}}$.

2. **Rename**: replace every `\Phi` (referring to the existing functor $\potlens\to\org$) with `\Phi^{\mathrm{symp}}`. Use `\mathrm{symp}` not `\rm symp` (memoir-class quirk: `\rm` is rejected). No bare $\Phi$ remains as the default name.

3. **Theorem form**: generic. `thm.functor` states the parameterized theorem; two named instances ($\Phi^{\mathrm{symp}}$, $\Phi^{\mathrm{grad}}$) are immediate.

4. **$\leg$**: stays in the chain, but reframed as "the lift induced by the natural transformation $\eta_F$" — for $F = \lvert T^*\blank\rvert$ and $\eta_F = \rho$, $\leg^{\eta_F} = \leg$ (existing). For $F = \lvert\blank\rvert$ and $\eta_F = \id$, $\leg^{\eta_F}$ is the identity functor.

5. **`sec.gradient_dynamics`**: new subsection at the end of `sec.potential_lenses_to_dynamics`, after the unpacking of $\Phi$ on objects and morphisms. Short — half a page. Walks through the gradient case specifically.

6. **$\Psi$ forward pointer**: one-sentence pointer in `sec.gradient_dynamics`. Do NOT state $\Phi^{\mathrm{grad}}\circ\iota \cong \Psi$ as a labeled corollary here. (The deep-learning chapter will develop it.)

7. **No editorializing**: just state facts. Do NOT add commentary like "this is genuinely structural" or "the reader should walk away with...". Match the paper's terse declarative voice.

8. **Don't change the wave-equation chapter's structure**: `ch.spring` remains, examples remain. Only the framing sentence in `sec.spring_intro` is edited (one sentence) plus the renamed $\Phi^{\mathrm{symp}}$ throughout `ch.spring`.

9. **The footnote at `eqn.state_update`**: update only minimally — replace "$\Phi$" with "$\Phi^{\mathrm{symp}}$" if it appears, otherwise leave as-is. Add a parallel footnote at the new `eqn.state_update_gradient` for stability contrast (see Task 4 below).

## Tasks (in order)

### Task 1: Modify `lem.poly_to_org`

Around line 2200, the lemma currently reads (verify exact wording before editing):

> \begin{lemma}\label{lem.poly_to_org}
> With the action $V\cdot p=\cot{T^*V}\otimes p$ of $\pvect$ on $\poly$, there is an identity-on-objects lax symmetric monoidal functor
> \[\dyn\colon\para{\cot{T^*}}{\poly}\to\org.\]
> We call it the \emph{dynamical realization} functor.
> \end{lemma}

Replace with the parameterized form:

> \begin{lemma}\label{lem.poly_to_org}
> Let $F\colon\pvect\to\smset_\cong$ be strong symmetric monoidal. With the action $V\cdot p=\Fun{Store}(F(V))\otimes p$ of $\pvect$ on $\poly$, there is an identity-on-objects lax symmetric monoidal functor
> \[\dyn^F\colon\para{\Fun{Store}\circ F}{\poly}\to\org.\]
> \end{lemma}

The proof is the same construction; modify it to abstract over $F$. The existing proof relies on `prop.pnla_polynomial` (giving $\cot V \cong V\yon^V$) and the action-square / `prop.org_as_para` argument. Keep the proof body essentially intact, with notational substitution $|T^*\blank| \leadsto F$.

Remove the colloquial "dynamical realization" naming from the lemma statement; introduce that name in the theorem (Task 2) or omit it. The author's `feedback_short_statements.md` says theorem statements should be punchy headlines, not have epithets in them.

### Task 2: Modify `thm.functor`

Around line 2220, the theorem currently reads:

> \begin{theorem}\label{thm.functor}
> We have a lax symmetric monoidal functor
> \[\Phi\colon\potlens\to\org.\]
> \end{theorem}

Replace with the parameterized form:

> \begin{theorem}\label{thm.functor}
> Let $F\colon\pvect\to\smset_\cong$ be strong symmetric monoidal and $\eta_F\colon\Fun{Store}\circ F\Rightarrow\cot$ a monoidal natural transformation in $\poly$. There is a lax symmetric monoidal functor
> \[\Phi^F\colon\potlens\to\org\]
> defined as the composite $\cint\then\leg^{\eta_F}\then\dyn^F$, where $\leg^{\eta_F}\colon\para{\cot}{\poly}\to\para{\Fun{Store}\circ F}{\poly}$ is the Para-functor induced by $\eta_F$ via \cref{prop.para_strong_induced,prop.para_square}.
> \end{theorem}

Adjust the proof accordingly: it just notes the composite, with each piece justified by `lem.potlens_to_para_poly`, `lem.para_rho` (now generalized — see below), and `lem.poly_to_org` (Task 1).

Add immediately after the theorem (in prose, not as a labeled environment):

> Two natural members: writing $|\blank|\colon\pvect\to\smset_\cong$ for the underlying-set functor and using $\cot V\cong V\yon^V$ from \cref{prop.pnla_polynomial},
> \begin{itemize}
> \item $\Phi^{\mathrm{grad}}\coloneqq\Phi^{(|\blank|,\,\id_{\cot})}$, the \emph{gradient-flow} functor.
> \item $\Phi^{\mathrm{symp}}\coloneqq\Phi^{(|T^*\blank|,\,\rho)}$, the \emph{symplectic} functor of \cref{rmk.legendre_choice}.
> \end{itemize}

(Adapt cref labels as needed; `rmk.legendre_choice` doesn't exist yet — see Task 4. If the cref doesn't resolve cleanly, use `\cref{lem.rho_natural}` instead, which definitely exists.)

### Task 3: Generalize `lem.para_rho`

`lem.para_rho` (around line 2189) currently produces $\leg\colon\para{\cot}{\poly}\to\para{\cot{T^*}}{\poly}$ from $\rho$. This is already a generic-Para-functoriality construction; just refresh the statement to reflect that it's the special case of a more general construction:

> \begin{lemma}\label{lem.para_rho}
> Any monoidal natural transformation $\eta\colon\Fun{Store}\circ F\Rightarrow\cot$ in $\poly$ induces a strong symmetric monoidal functor
> \[\leg^\eta\colon\para{\cot}{\poly}\to\para{\Fun{Store}\circ F}{\poly}.\]
> \end{lemma}

Proof: same — applies `prop.para_strong_induced,prop.para_square` to $\eta$.

After the lemma, in prose, name the existing case:

> The \emph{Legendre refinement} is the case $\eta = \rho\colon\cot{T^*\blank}\Rightarrow\cot$ of \cref{lem.rho_natural}; we write $\leg\coloneqq\leg^\rho$.

### Task 4: Update unpacking and add `eqn.state_update_symp` (rename or add)

The unpacking around lines 2240–2335 develops $\Phi$ in detail. With the rename, this is now developing $\Phi^{\mathrm{symp}}$. Update accordingly:

- Find every occurrence of `$\Phi$` (the bare functor name, not `$\Phi(...)$` invocations) in the unpacking and replace with `$\Phi^{\mathrm{symp}}$`.
- The labeled equation `eqn.state_update` at line ~2196 stays labeled the same way (`eqn.state_update`) but now describes the symplectic case. The footnote attached to it (the explicit-Euler-instability footnote) stays — it correctly describes the Hamilton flow case.

### Task 5: Write `sec.gradient_dynamics`

Insert a new subsection at the END of `sec.potential_lenses_to_dynamics` (after the unpacking of `eqn.state_update` for the symplectic case finishes — i.e., after the terse coalgebra-map summary around line 2330).

Subsection content (~half page; match the paper's voice: declarative, present tense, tight):

> \subsection{The gradient-flow case}\label{sec.gradient_dynamics}
>
> [Paragraph 1: identify the case.] The gradient-flow functor $\Phi^{\mathrm{grad}}\colon\potlens\to\org$ is the case $F = \lvert\blank\rvert$ of \cref{thm.functor}. The natural transformation $\eta_F$ is the canonical iso $\cot V\cong V\yon^V$ of \cref{prop.pnla_polynomial}, so the induced $\leg^{\eta_F}$ is the identity (up to that iso); the composite simplifies to $\Phi^{\mathrm{grad}}=\cint\then\dyn^{\lvert\blank\rvert}$.
>
> [Paragraph 2: state space and update.] On a morphism $f=(\outp f,\inpt f,U)\colon V\cdot\lensob M\to\lensob N$, the resulting coalgebra has state space $X^{\mathrm{grad}}\coloneqq V$ and update at $s=v\in V$ given by
> \begin{equation}\label{eqn.state_update_gradient}
> v\mapsto v+\sharp_V(\xi_V),
> \end{equation}
> with $\xi_V$ as in \eqref{eqn.bigtheta}. There is no momentum coordinate.
>
> [Paragraph 3: stability footnote — attached to eqn.state_update_gradient.] Add the footnote:
> %
> \footnote{
> \Cref{eqn.state_update_gradient} is explicit Euler of gradient flow. For positive-definite $\sharp_V$ and convex potential $U$, it is conditionally stable: the standard explicit-Euler bound for parabolic flow applies. Contrast \cref{eqn.state_update}, which is unconditionally unstable for harmonic systems.
> }
>
> [Paragraph 4: forward pointer to deep learning.] Restricting along the embedding $\iota\colon\para{\pvect}{\mfd}\hookrightarrow\potlens$ that takes vacuous backward map and zero potential, $\Phi^{\mathrm{grad}}$ recovers the cotangent-learners functor of \cref{cor.cotangent_learners}; we develop this in \cref{ch.deep_learning}.

The cref `\cref{ch.deep_learning}` will produce an undefined-reference warning. This is intentional and will be resolved when the chapter is written.

If `cor.cotangent_learners` doesn't exist as a label, use the closest existing label (probably the relevant lemma in `sec.deep_learning`, line ~1361) or omit the specific cite and just say "the cotangent-learners construction of \cite{shapiro2022dynamic}."

### Task 6: Update `sec.spring_intro`

Around line 2335, the wave-equation chapter intro currently says:

> We illustrate $\Phi\colon\potlens\to\org$ by deriving the wave equation.

Change to:

> We illustrate $\Phi^{\mathrm{symp}}\colon\potlens\to\org$ by deriving the wave equation; \cref{ch.deep_learning} illustrates the parallel functor $\Phi^{\mathrm{grad}}$ via deep learning.

The cref to `ch.deep_learning` will warn; intentional.

### Task 7: Global rename $\Phi \to \Phi^{\mathrm{symp}}$

Sweep the whole `dynamic-algebra-potentials.tex` for occurrences of bare `\Phi` referring to the functor $\potlens\to\org$. Replace with `\Phi^{\mathrm{symp}}`.

Care:
- DO NOT rename `\Phi(plm)` invocations where `\Phi` is being applied to something — those are notational and continue to be the bare symbol since we're now writing `\Phi^{\mathrm{symp}}(plm)` and that should look right.
- Wait, actually: the bare `\Phi` is the functor name. In invocations like `\Phi(\Part)` or `\Phi(\fun{wire}_K)`, the same renaming applies — replace with `\Phi^{\mathrm{symp}}(\Part)` etc.
- DO NOT touch any unrelated `\Phi` — but in this paper, `\Phi` is exclusively the main functor name. There are no unrelated uses.
- The renaming will affect: `sec.potential_lenses_to_dynamics`, `ch.spring` (especially the spring derivation), `sec.deep_learning` forward pointer (already mentions $\Phi^{\mathrm{grad}}$; should also mention $\Phi^{\mathrm{symp}}$).
- In TikZ figures, `\Phi` may also appear; rename consistently.

Use a careful grep + replace strategy. After replacement, do a final grep for `\Phi` (bare) to confirm no stragglers — only `\Phi^{\mathrm{symp}}`, `\Phi^{\mathrm{grad}}`, or `\Phi^F`/`\Phi^{(F,\eta_F)}` should remain.

### Task 8: Update `sec.deep_learning` forward pointer

Around line 1361 in `sec.deep_learning` (currently a forward pointer), update to mention both functors with their new names. Current text (verify):

> The cotangent-learners construction of \cite{shapiro2022dynamic} sits inside our framework as a strong monoidal functor $\Psi\colon\para{\pvect}{\mfd}\to\org$, sending $\rr^n\mapsto\cot{\rr^n}$ and a parameterized smooth map $f\colon V\times\rr^m\to\rr^n$ to the coalgebra whose update at $s\in V$ is one step of stochastic gradient descent. We develop deep learning fully in \cref{ch.deep_learning}, where it appears as a special case of the gradient-flow functor $\Phi^{\mathrm{grad}}$ defined in \cref{sec.gradient_dynamics}; the cotangent-learners restriction is the Euclidean, learning-rate-$\eta$ specialization. For now, take this as a forward pointer.

This is mostly fine — verify it references $\Phi^{\mathrm{grad}}$ and `sec.gradient_dynamics` correctly. (`sec.gradient_dynamics` will exist after Task 5, so the cref will resolve.)

### Task 9: Build and verify

```bash
cd /Users/davidspivak/VersionControl/dynamic-algebra-potentials
/usr/local/texlive/2024/bin/universal-darwin/pdflatex -interaction=nonstopmode -halt-on-error dynamic-algebra-potentials.tex 2>&1 | tail -15
```

Expected:
- Build succeeds.
- One intentional undefined-reference warning: `ch.deep_learning` (chapter not yet written).
- All other crefs resolve.
- Page count: probably ~38 pages (was 38; might be ~39 with the new subsection).

If `cor.cotangent_learners` was referenced and doesn't resolve, fix to a working label.

Run a second pass of pdflatex (cross-references) and confirm.

## Style constraints

1. Match the paper's voice: declarative, present tense, tight. See `feedback_voice.md`.
2. Theorem statements should be short; details go in proofs and surrounding prose. See `feedback_short_statements.md`.
3. Use `\coloneqq` for definitional equality; `\eqref{...}` for equations; `\cref{...}` for results; `\qqand` for "and" between formulas.
4. `\emph{...}` only for first introduction of a technical term. Don't use it for emphasis.
5. **Don't editorialize.** No commentary like "this is structural" or "the reader should walk away with...". State facts.
6. Use `\mathrm{symp}` and `\mathrm{grad}` for the superscripts; `\rm` does not work (memoir-class quirk).
7. Footnote markers go AFTER punctuation (period, comma, colon).

## Reporting

When done, report (under 400 words):

1. Build status; intentional warnings only (`ch.deep_learning` cref, possibly one or two others if cleanup of forward references is needed).
2. Final page count.
3. Final state of the parameterized `thm.functor`: paste its statement.
4. Final state of `sec.gradient_dynamics`: paste the section, including the footnote.
5. Confirmation that bare `\Phi` no longer appears (grep result).
6. Confirmation that `eqn.state_update` is unchanged structurally; `eqn.state_update_gradient` is added.
7. Any judgment calls made (e.g., wording variations, places where the planned wording didn't fit and was adjusted, references that needed substitution).
8. A final summary of what changed, by section/line range, useful as a "diff at a glance" for the author.
