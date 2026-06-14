# Prose review — Claude-authored passages in `dynamic-algebra-potentials.tex`

## Instructions (read first)

This file lists every passage in `dynamic-algebra-potentials.tex` that **Claude (Fable) authored or substantially reworded** during the symplectic/conservation/terminology work on the `sympl-phase` branch. The goal of the review is to **rewrite this prose in David's voice**. The mathematics, structure, and equations are settled — this pass is about *voice and phrasing only*.

**How to use this file with the LLM reviewer:**
1. Work top to bottom (entries are in document order).
2. Line numbers are approximate and **drift as you edit**. Locate each entry by its **anchor phrase**, not its line number: `grep -n '<anchor>' dynamic-algebra-potentials.tex`.
3. For each entry, rewrite the passage in David's voice, then **delete the entry** from this file.
4. Periodically refresh the remaining line numbers by re-grepping the anchors (a helper grep loop over the anchors works).
5. Consult the voice conventions in `~/.claude/.../memory/feedback_voice.md` (variable conventions, let-binding cadence, univocity, definition-companion paragraph, remark closers) and `feedback_proof_style.md` (slow, explicit proofs).

**Tags:** `[new]` = whole block written from scratch · `[rewrite]` = Claude's words replacing David's · `[gloss]` = a connective phrase inserted into David's existing derivation.

**NOT in scope (do not review — these are *not* Claude's prose):**
- The single-stage framework block ≈ L1968–2085: `lem.poly_to_org`, `def.integrator`, `prop.integrator_to_org`, `thm.dynamics_functor` — restored verbatim from commit `d0a5c92` (David's own text).
- The wave/graph **derivations** themselves (§"The wave equation", §"Graph Laplacian") — David's text with a mechanical `q → q̃` symbol substitution. Only the connective glosses listed below are Claude's.

---

## Entries

### Introduction
- `[rewrite]` ≈L610 — `a momentum, which carries the position forward`
- `[rewrite]` ≈L614 — `We make the conservative side precise` (the closed-systems / symplectic-pairing sentence)

### Syntax chapter — terminology
- `[rewrite]` ≈L2287 — `As for the interfaces, we call a morphism` (the closed / system / closed system definition, incl. the "sometimes called a scalar" aside)

### Cotangent section
- `[new]` ≈L2395 — `Covectors add along fan-out` (the whole `rmk.fanout_addition`: net force = autodiff gradient accumulation)

### Phase integrator (§"Integrator semantics")
- `[rewrite]` ≈L2587 — `and steps it by the symplectic sharp on` (phase-integrator opening) and the readout/ν sentence at `On positions, the map $\nu`
- `[new]` ≈L2598 — `assemble into a monoidal natural transformation` (`lem.nu_monoidal` statement **and** proof)
- `[rewrite]` ≈L2604 — `and $\nu$ is by \cref{lem.nu_monoidal}` (the "This is a $\cot$-integrator" sentence)
- `[rewrite]` ≈L2614 — `The two legs divide the labor`
- `[rewrite]` ≈L2622 — `This is one step of Hamilton's equations: the position moves by the velocity`

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
