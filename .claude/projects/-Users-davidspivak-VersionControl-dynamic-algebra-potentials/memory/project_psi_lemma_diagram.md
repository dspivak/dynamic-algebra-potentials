---
name: psi-lemma-diagram
description: Status and plan for the psi-composition lemma proof diagram in psi-lemma.tex
metadata:
  type: project
---

The file `psi-lemma.tex` proves the lemma $\psi_{g \circ f} = \psi_g \circ (\outp{f} \otimes \psi_f) \circ (\delta \otimes \id)$ for the monad case.

**What's done:**
- Section 1: Setup (T-algebra, coKleisli lenses, definition of $\psi_f$ as a composite of C-morphisms using $\coev'$ then $[\inpt{d}, -]$ applied to $\inpt{f}, \sigma, T\ev, \alpha$)
- Section 2: Lemma statement
- Section 3.1: LHS ($\psi_{g \circ f}$) spelled out as a tikzcd diagram — $\coev'_e$ then 9 arrows inside $[\inpt{e}, -]$
- Section 3.2: RHS ($\psi_g \circ (\outp{f} \otimes \psi_f) \circ (\delta \otimes \id)$) spelled out as three tikzcd diagrams composed

**What's needed:**
- Section 3.3: The proof diagram — a landscape tikzcd showing both paths as opposite sides of a rectangle, interior filled with tiles. This IS the monad diagram from the main paper (dynamic-algebra-potentials.tex, lines 3700-3780), with the boundary relabeled using $\psi$ notation. Each tile commutes by one word: functoriality, naturality of $\sigma$/$\coev'$/$\ev$, $T$-algebra axiom, or comonoid axiom.

**Key user preferences (critical):**
- Every arrow is one C-morphism, one difference from the previous node
- NO prose arguments, NO "absorbing" or "simplifying" — just tiles
- Work at the $\psi$ level throughout — never switch to $\phi$ without justification
- Use $[\inpt{d}, -]$ and $[\inpt{e}, -]$ notation (applying internal hom functor), matching the main paper's style
- The interior has double internal homs $[\inpt{e}, \ldots [\inpt{d}, \ldots]]$
- The user wants proofs that look like the main paper's big diagram: trustworthy because every tile is slam-dunk obvious

**Why:** [[feedback_proof_style]], [[feedback_edit_scope]]
