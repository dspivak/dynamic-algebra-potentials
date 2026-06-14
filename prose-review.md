# Prose review — Claude-authored passages in `dynamic-algebra-potentials.tex`

## Instructions (read first)

This file lists every passage in `dynamic-algebra-potentials.tex` that **Claude (Fable) authored or substantially reworded** during the symplectic/conservation/terminology work on the `sympl-phase` branch. The mathematics, structure, and equations are settled — this pass is about *voice and phrasing only*. **David does the rewriting.**

**The LLM's only job is to locate, not to rewrite.** The division of labor:
1. Work top to bottom (entries are in document order).
2. For the next undeleted entry, grep its **anchor phrase** to find the current line(s): `grep -n '<anchor>' dynamic-algebra-potentials.tex`. Report only: `next spot: lines X–Y` (plus the anchor, so David can find it). Do **not** propose rewrites, draft prose, or comment on voice unless David asks.
3. David rewrites the passage himself in his own voice.
4. When David says an entry is done, **delete that entry** from this file, then point to the next spot.
5. Line numbers below are stale and **drift as the file is edited** — always re-grep the anchor; never trust the stored number.

**Tags:** `[new]` = whole block written from scratch · `[rewrite]` = Claude's words replacing David's · `[gloss]` = a connective phrase inserted into David's existing derivation.

**NOT in scope (do not review — these are *not* Claude's prose):**
- The single-stage framework block ≈ L1968–2085: `lem.poly_to_org`, `def.integrator`, `prop.integrator_to_org`, `thm.dynamics_functor` — restored verbatim from commit `d0a5c92` (David's own text).
- The wave/graph **derivations** themselves (§"The wave equation", §"Graph Laplacian") — David's text with a mechanical `q → q̃` symbol substitution. Only the connective glosses listed below are Claude's.

---

## Entries

### Phase integrator (§"Integrator semantics")
- `[new]` ≈L2726 — `is the instance of \cref{lem.combined_update} built from the exponential readout` (phase-integrator opening: now framed as the instance ν=ν_{σ¹,β}, presented position)
- `[new]` ≈L2757 — `The readout and the 1-form are independent dials` (the whole `rmk.phase_design_space`: damped/lookahead variants)
- note: the *Readouts and one-forms* subsection (`def.monoidal_one_form`…`lem.combined_update`) is restored from your pre-cut text, not Claude prose — out of scope, except the reworded sentence `Fed through the symplectic sharp, a monoidal 1-form contributes to the phase integrator`

### Phase dynamics (§"Phase-space dynamics")
- `[new]` ≈L2882 — subsection title `\subsection{The phase coalgebra}`
- `[rewrite]` ≈L2880 — `but the phase integrator evaluates them at the presented position`
- `[rewrite]` ≈L2906 — `The remaining difference is in the state update`
- `[new]` ≈L2931 — subsection title `\subsection{Closed systems and conservation}`
- `[new]` ≈L2933 — `When $f$ is a closed system---both interfaces trivial` (closed-systems lead paragraph)
- `[new]` ≈L2937 — `The construction imposes nothing further` (the bold scope declaration)
- `[rewrite]` ≈L2940 — `This remark justifies the Hamiltonian terminology` (`rmk.constant_inverse_mass_hamiltonian` opening)
- `[rewrite]` ≈L2944 — `This is the \emph{semi-implicit} Euler step`
- `[new]` ≈L2963 — `What it conserves is the canonical symplectic pairing` (conservation lead-in)
- `[new]` ≈L2969 — `a \emph{drift} advancing the position and a \emph{kick}`
- `[new]` ≈L2971–2989 — `Closed quadratic dynamics conserve the symplectic pairing` (`prop.closed_conservation` statement + proof)
- `[new]` ≈L2991 — `This is the structural signature of a conservative integrator` (the motivating closer)
- `[new]` ≈L2994 — `The integrators built here are \emph{single-stage}` (the whole `rmk.multistage`)

### Applications chapter
- `[rewrite]` ≈L3003 — `up to the phase integrator's readout` (dap footnote parenthetical)
- `[rewrite]` ≈L3009 — `Newton's method is a \emph{closed system}` (Newton opening)
- `[gloss]` ≈L3117 — `a $2$-ary closed morphism` (DL loss term)
- `[gloss]` ≈L3256 — `is the presented position \eqref{eqn.presented_position}, computed with the sharp` (wave, first pass)
- `[gloss]` ≈L3289 — `the second being the environment's response` (wave boundary condition)
- `[gloss]` ≈L3302 — `the presented position is the next position` (wave recurrence)
- `[gloss]` ≈L3306 — `which is exactly where the right-hand side is evaluated` (centered recurrence)
- `[gloss]` (wave second pass, §"Functoriality audit") — `where $\tilde q=q+\xi/m$ is the presented position` (grep `presented position`)
- `[gloss]` ≈L3523 — `is constant and symmetric, and the potential \eqref{eqn.graph_potential} is quadratic` (graph-Laplacian symplectic cross-ref sentence)
