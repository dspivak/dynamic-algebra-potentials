# Plan: Reframe the second wave-equation pass as an audit

## Context

The paper currently derives the discrete wave equation in two ways in `dynamic-algebra-potentials.tex`.

- `sec.spring_first_pass`: compose the particles and wiring in `\srw`, then apply `\Phiphase{}`.
- `sec.spring_second_pass`: apply `\Phiphase{}` to the particle and wiring separately, then compose in `\org`.

The author's intent is that the second computation is a consistency check: the two routes agree by functoriality, and the explicit agreement helps audit signs, indices, covector-field evaluation, and the routing of inputs. It should not feel like a second mandatory derivation.

## Goal

Keep `sec.spring_second_pass`, but reframe it as an optional bookkeeping/functoriality audit. The section should say, in effect:

> We already derived the wave equation. This subsection checks the machinery by computing the same coalgebra after applying `\Phiphase{}` to the pieces and composing in `\org`. The agreement is a useful sanity check on the formulas.

## Proposed edits

1. Retitle the subsection.

   Current:

   ```latex
   \subsection{Second pass: composing in \texorpdfstring{$\org$}{Org}}\label{sec.spring_second_pass}
   ```

   Suggested:

   ```latex
   \subsection{Functoriality audit: composing in \texorpdfstring{$\org$}{Org}}\label{sec.spring_second_pass}
   ```

   Keep the label unchanged.

2. Revise the first paragraph of `sec.spring_second_pass`.

   It should explicitly say that the subsection is not needed to obtain the wave equation, but checks the bookkeeping and the functoriality claim. Suggested replacement:

   ```latex
   We have already recovered the wave equation by connecting $K$-many particles together in $\srw$, sending the result to $\org$, and reading off the resulting $(\cotof{\rr}\otimes[\cotof{\rr},\yon])$-coalgebra. This subsection is a bookkeeping audit: we instead apply $\Phiphase{}$ to the particle and to the static wiring separately, compose the resulting coalgebras in $\org$, and check that the same coalgebra is obtained. The equality is forced by operad-functoriality of $\Phiphase{}$,
   ```

   Then keep the displayed equality that follows, if it is still syntactically connected.

3. Keep the high-value technical pieces.

   Preserve:

   - the displayed functoriality equality;
   - the single-particle coalgebra formula;
   - `eqn.org_wiring_concise`;
   - the composition display
     ```latex
     T^*\rr^K\To{\Phiphase{}(\Part)^{\otimes K}}\cdots
     ```
   - the final threading paragraph explaining how `\omega_{i+1}(x_i)`, `x_{i-1}`, and `\xi_N` route through the composite.

4. Reduce repeated explanatory prose.

   The second pass should not re-explain the physical meaning at the same level as the first pass. In particular, consider tightening paragraphs whose main content is informal explanation after a formula. Good candidates:

   - the prose paragraph beginning `In other words, starting at position $x$ and momentum $p$...`;
   - the last sentence of the static-wiring paragraph beginning `The routing $\omega_{i+1}(x_i)$...`;
   - any sentence that repeats what was already derived in `sec.spring_first_pass`.

   Do not remove the actual formulas or the routing data.

5. Make the close read like a check, not a proof burden.

   The final sentence currently ends with:

   ```latex
   This is exactly the same as \eqref{eqn.potlens_composite_final}, verifying the functor and auditing the validity of the formulas in this case.
   ```

   Suggested revision:

   ```latex
   This is exactly the same as \eqref{eqn.potlens_composite_final}. Thus the two routes agree: composing first in $\srw$ and composing after applying $\Phiphase{}$ give the same coalgebra, as functoriality requires.
   ```

## Things to avoid

- Do not delete `sec.spring_second_pass`.
- Do not change the label `sec.spring_second_pass`; it is referenced elsewhere.
- Do not change mathematical formulas unless a genuine typo is found.
- Do not introduce new claims about formalization, LLMs, or mechanization into the paper text.
- Preserve the author's notation, tone, and local terminology.

## Verification

After editing, compile with:

```sh
env PATH=/Library/TeX/texbin:$PATH /Library/TeX/texbin/latexmk -pdf -interaction=nonstopmode dynamic-algebra-potentials.tex
```

Expected result: compilation succeeds. Existing overfull-box, font-substitution, and `\qedhere` warnings may remain.
