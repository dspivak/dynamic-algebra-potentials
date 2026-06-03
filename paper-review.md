# Paper Review: Compositional Dynamics for Learning and Physics

This review covers the TeX source, build behavior, bibliography, and the rendered PDF. It also incorporates three delegated reads: a PDF-only pass, a mathematical/source-consistency pass, and a references/bibliography pass.

No source edits were made as part of this review.

## Bottom Line

The paper is strong and the main narrative works, but it is not yet a perfect incarnation of what it is trying to be. The largest issues are not ordinary typos: there are a few type/proof mismatches in the abstract framework, a real compile/PDF-health problem, and a handful of places where the paper promises more than it actually proves.

## Highest Priority

1. `dynamic-algebra-potentials.tex:1913`: `\Phi'_{\interp}\colon\rwd_D\to\para{\Fun c}{\poly}` is ill-typed as written. `\Fun c` has domain `\cat M`, while the Para parameter category is `\cat V`; the action is explicitly `V\cdot q=\Fun c(JV)\otimes q`. This should likely be `\para{\Fun c\circ J}{\poly}` or a notation that makes the induced action unambiguous. The same issue recurs at lines 1924 and 2048.

2. `dynamic-algebra-potentials.tex:1933`: the moded interpretation proof appears wrong or incomplete. For `(\Fun R')^\md=\prod_\md\circ\Fun R'`, the algebra on `z^\md` should have domain roughly `(\Fun R'(z^\md))^\md`, but the proof constructs only `\Fun R'(z^\md)\to z^\md`. Also line 1930 omits `J` from the rewiring datum and has an unclosed displayed tuple.

3. `dynamic-algebra-potentials.tex:2797`: in the Eulerized submersion-lens comparison, the displayed `\cat S` morphism loses the tangent component. Since the action uses `(TV\surj V)\otimes p`, the total space should involve `TV\times E`, not just `V\times E`; the later update `x+u(...)` depends on exactly that missing vector.

4. `dynamic-algebra-potentials.tex:2549`: the phase integrator is called “symplectic Euler,” but the formula at line 2572 is explicit Euler using old `x` and old momentum. This conflicts with the later correct remark at line 2935 that explicit Euler is not symplectic.

5. Build/PDF health: running the prescribed `latexmk` command produced a PDF on one pass but failed on a later pass with a biblatex/backref aux error around `chung1997spectral`. It also emits `pdfTeX warning (dest): name{term.interp} has been referenced but does not exist`. The current PDF also triggers Poppler/PDF syntax warnings during text extraction. This should be fixed before distribution.

## Proof and Self-Containedness

- `dynamic-algebra-potentials.tex:1522`: the Moore internalization theorem is advertised as the main technical result, but the proof leaves identity preservation to the reader and compresses lax monoidal coherence into “amount to” prose. Given the paper’s self-containedness claim, this is the main proof that deserves more detail.

- `dynamic-algebra-potentials.tex:1883`: the power-monad/distributive-law proof leaves the distributive-law and monoidality axioms to the reader. That may be acceptable if this is demoted, but it currently supports the moded interpretation proposition.

## Promises and Scope

- `dynamic-algebra-potentials.tex:2016`: the paper promises “configuration, phase, and dissipative” integrators, but only configuration and phase are built. Remove “and dissipative” unless the dissipative integrator is added.

- `dynamic-algebra-potentials.tex:3252`: the adaptive spring remark is interesting but underdeveloped relative to its length. It introduces a multiplicative stiffness update and invokes natural gradient descent without unpacking the coupled dynamics. It should either be shortened or expanded into a real example.

- `dynamic-algebra-potentials.tex:3317`: “Hopefully this serves...” is less crisp than the surrounding prose.

## Notation, Hyperlinks, and PDF Rendering

- `dynamic-algebra-potentials.tex:458`: `\interp` is tracked but never defined with `\defineTerm{interp}`, so semantic links to it point nowhere.

- `dynamic-algebra-potentials.tex:738`: typo: “substition” should be “substitution.”

- PDF page 65: the opposite-sign heat reaction formula is cramped inline; it would read better as a display.

- PDF pages 61-62: the functoriality audit is correct-looking but very dense. It is near the readability limit.

- PDF page 52, footnote 19: the footnote is long and includes a compact categorical construction in very small type.

- PDF page 2: the running head says “1. Introduction” while the top of the page is still the continuation of the table of contents. Since the Introduction starts later on the same page, this is understandable but mildly confusing.

## Bibliography

- `Library20260419.bib:3876`: `niu2025polynomial` is stale: it says `year={2024}` and “to appear.” Cambridge lists it as published in 2025, LMS Lecture Note Series 498, DOI `10.1017/9781009576734`. Source checked: Cambridge Core, <https://www.cambridge.org/core/books/polynomial-functors/contents/99E864BD83CFB75B950851B9CE3A8520>.

- `Library20260419.bib:1159`: “Actegories for the Working Amthematician” looks like a typo in the PDF, but the arXiv title itself currently uses “Amthematician,” so this is visually odd rather than clearly bibliographically wrong. Source checked: arXiv, <https://arxiv.org/abs/2203.16351>.

- PDF references: arXiv numbers and URLs render with spaces around punctuation, making them hard to copy. Examples seen in the PDF include `2105 . 06332` and URLs rendered like `https : / / topos . institute / ...`.

## Checks With No Finding

- No ordinary missing labels were found in the source-level label/reference scan.

- No duplicate labels were found.

- Biber found all 34 cited keys; the apparent missing keys `Lee:1997a` and `fox1976coalgebras` in a simple parser scan were artifacts of entries written as `@book { ... }` / `@article { ... }` with a space before `{`.

- No unresolved `??` references or missing citation markers were visible in the rendered PDF.

- The wave-equation derivation appears internally consistent on signs: the left boundary comes from the external point input and the right boundary from the external covector input.

## Verification

I ran the prescribed TeX command:

```sh
env PATH=/Library/TeX/texbin:$PATH /Library/TeX/texbin/latexmk -pdf -interaction=nonstopmode dynamic-algebra-potentials.tex
```

It did not complete cleanly. The many undefined-reference warnings in the failed run appear downstream of the aux/backref failure, not ordinary missing labels.

---

# Addendum: second-pass multi-agent review

A second review pass fanned out six independent readers (three deep math passes by
chapter cluster, a cross-reference/label audit, a bibliography-precision audit, and a
PDF-rendering pass), then reconciled them against this file. Below: (1) corroborations
and refinements of the items above; (2) new findings this file had missed; (3) a build/PDF
update; (4) one correction to a "no finding" claim. No source edits were made.

## 1. Corroborations and refinements of existing items

- **Highest Priority #1 (`:1913` ill-typed `\para{\Fun c}{\poly}`) — confirmed.** `\Fun c\colon\cat M\to\poly`, but the acting category is `\cat V` and the action is `V\cdot q=\Fun c(JV)\otimes q`; the smooth analog at `:2451`/`:2594` correctly writes `\para{\cot}{\poly}` where `\cot=\Fun c\circ J`. So the abstract subscript should be `\Fun c\circ J`. Recurs at `:1922`, `:1924`, `:2048`. (The action is spelled out, so this is a notation/typing abuse rather than a math error — but it should be fixed for the `\para{p}{\poly}` convention to hold.)
- **Highest Priority #3 (`:2797` submersion-lens loses the tangent component) — confirmed by independent recomputation.** The action is `V\cdot p=(TV\twoheadrightarrow V)\otimes p`, whose total space is `TV\times E`. The displayed `\cat S`-morphism writes the left column as `V\times E\twoheadrightarrow V\times B` (map "`V\times p`") and lands `(u,\alpha)` in `V\times E`, dropping the `TV` (i.e. the `\dot x=u(\dots)` factor used at `:2823`, `:2833`). Fix: left column `TV\times E\twoheadrightarrow V\times B` (≅ `V\times V\times E` under `TV\cong V\times V`), with `(u,\alpha)` targeting `TV\times E`. Note: the *final* coalgebra and the square's commutativity are nonetheless correct — only the displayed intermediate diagram mistypes the total space.
- **Highest Priority #4 (`:2549` "symplectic Euler") — confirmed.** The update `((x,\xi),\xi')\mapsto(x+\sharpR_x\xi,\ \xi-\xi')` (`:2572`) advances both position and momentum from *old* values, i.e. explicit (forward) Euler — exactly what `rmk.euler_energy` (`:2935`) says is *not* symplectic. Change "the symplectic Euler step" to "the (explicit) Euler step" or "the Euler step built from the symplectic sharp", reserving "symplectic" for the sharp, not the integrator.
- **Highest Priority #5 / `:458` (build health and the `\interp` link) — confirmed and sharpened.** `\interp` (`\mathfrak p`) is registered with `\trackTerm` (`:458`) but **`\defineTerm{interp}` is never placed anywhere in the source** (verified by grep; contrast `\defineTerm{intg}` at `:2001`). So *every* rendered `\interp` is a live `\hyperlink{term.interp}{...}` to a non-existent target — this is the source of the `pdfTeX warning (dest): name{term.interp} ... does not exist` and means the semantic links on the central symbol `\interp` are all dead. Fix: add `\defineTerm{interp}` at its definition site (`def.polynomial_interpretation`, `:1897`).
- **Promises / `:3252` (adaptive spring) — refined.** Beyond being underdeveloped, the natural-gradient citation is an **overclaim** (see new item B-3 below).
- **Bibliography / niu2025 — confirmed**, with the published metadata you already give (LMS LNS 498, DOI `10.1017/9781009576734`); also note the citation *key* says 2025 while the entry's `year={2024}` — reconcile both.

## 2. New findings (missed by the first pass)

### Should-fix — math/notation defects

- **`:1920`, `:1922` — wrong lens functor.** The proof of `thm.poly_interpretation` writes `\Lens{\Fun c}\colon\Lcokl{\cat M}{\Fun R}\to\Lcokl{\poly}{\Fun R'}` (and `\para{\cat V}{\Lens{\Fun c}}`). But `\Lens{\Fun c}=\Cat{Lens}_{\Fun c}` is the *plain*-lens functor (maps `\Lens{\cat M}\to\Lens{\poly}`); the functor between the *coKleisli* categories that uses `\theta` is `\LensMor{\Fun c}{\theta}=\Cat{Lens}_{\Fun c}^{\theta}` from `lem.lens_T_functoriality` — the very lemma cited one clause earlier. Fix: replace both `\Lens{\Fun c}` with `\LensMor{\Fun c}{\theta}`.
- **`:1920` — misattributed action square.** "The action square for `\Lens{\Fun c}` and the action square for `\Theta_z` recorded in `\cref{cor.parameterized_representation}`…": `cor.parameterized_representation` records only the `\Theta_z`-equivariance square. The lens-functor's action square is a separate fact (from strong monoidality of `\Fun c`). Attribute it separately.
- **`:1933`–`:1944` — moded-interpretation algebra has the wrong domain.** Corroborating Highest-Priority #2: an `(\Fun R')^\md=\prod_\md\circ\Fun R'`-algebra on `z^\md` is a map `\prod_\md\Fun R'(z^\md)\to z^\md`, but the displayed map starts from `\Fun R'(z^\md)` (one `\prod_\md` short, no projections). The result is true; the displayed structure map needs the outer `\prod_\md` and the per-mode projections. *Also* (separate): `:1936` cites `prop.moding` — stated and proved for **cartesian** `\cat M` — to conclude `(\Fun R')^\md` is a monoidal monad on `(\poly,\yon,\otimes)`, whose `\otimes` is **not** cartesian. True, but `prop.moding` as written doesn't cover it; either broaden `prop.moding` to "monoidal with `\md`-fold products" or justify the `\otimes`-case inline.
- **`:1930` — wrong tuple slot + unbalanced delimiter.** `D\coloneqq(\cat M,\Fun R,\cat V)` should have `J` (not `\cat V`) in slot 3 to match `def.rewiring_datum`/the proof; and `\cat{V}$)` closes the paren outside math. Fix: `(\cat M,\Fun R,J)` / `(\cat M,\Fun R^\md,J)`.
- **Tuple-order inconsistency across the framework.** Abstract datum is `(\cat M,\Fun R,J)` (3-tuple, monad in slot 2); smooth instance `def.potlens` (`:2411`) is `\Sm=(\mfd,\rvect,\inc,\rr)` (4-tuple, different order, **monoid** `\rr` where the abstract has the **monad** `\Fun R`). Pick one shape; e.g. present the abstract datum as `(\cat M,\cat V,J,\Fun R)` to parallel `\Sm`, noting `\Sm`'s `\rr` abbreviates the writer monad.
- **`:1296` — stray `M` for the monoid `R`.** `lem.monoid_to_monad` ends "Functoriality in `(\cat C,M)`"; the lemma statement (`:1288`) says `(\cat C,R)` and the monoid is `R`. Change `M`→`R`.
- **`:1115`, `:1141` — `\epsilon` for the comonoid counit, breaking the `\varepsilon` convention** (NOTATION.md; every other site uses `\varepsilon`). Relatedly, `:2996` writes the gradient-descent sharp as `-\epsilon\,\id`, inconsistent with the `-\eta_{\mathrm{LR}}\sharpEuc` of `eqn.learning_sharp`; prefer `\eta_{\mathrm{LR}}`.
- **`:2016` — unfulfilled promise "configuration, phase, and dissipative".** Only configuration and phase integrators are built; "dissipative"/"a dissipative variant" appears nowhere else (sole hit at `:2016`). Remove the two "dissipative" clauses unless the integrator is added. (This is the integrator-side analog of the existing "promises" findings.)

### Should-fix — grammar that breaks parse

- **`:2587` — "we use `\cot\colon\ldots` is strong symmetric monoidal".** No valid parse; insert "that": "we use that `\cot…` is…".
- **`:2782`–`:2786` — "given by [display] sends a submersion lens…".** Object- and morphism-actions of the functor `P` run together with no connective. Split: "…given on objects by `P(E\twoheadrightarrow B)\coloneqq\sum_{b}\yon^{E_b}`. It sends a submersion lens `(r,\alpha)` to…".

### Polish — typos, micro-clarity, weight

- `:738` "substition"→"substitution" (already noted above); `:2251` "denote **to** the underlying set" (delete "to").
- `:1974` `\poly(S,[p,q]\tri S)` should be `\smset(S,[p,q]\tri S)` (the post-`prop.coalg_as_poly_map` term is a set-function; `\org_\cong` is defined via `\smset`).
- `:2388` `\cotof{R}` should be `\cotof{\rr}` (no `R` in scope in `rmk.alpha_general`).
- `:1301`, `:2591` double spaces; `:1323` "correspond *precisely*" overstates (composition-preservation also uses `\sigma`-naturality, not a strength axiom alone — the commented `:1324` says it honestly).
- `:802` footnote reuses the lens-bracket macro `\lens{p}{q}` for the `\tri`-left-division, a glyph collision with lens objects right next to `\Store(S)=S\yon^S`.
- `:2831`, `:2837` write the cotangent pullback as `(T_\bullet w)^*` whereas the chapter (and `eqn.differential`) use `^\top`; unify.
- `:3189`/`:3195` call the external covector field `\omega_\boxob`, but the second pass (`:3297`, `:3313`) calls the same object `\omega_1`; unify.
- `:3434` (Conclusion) "two integrators of the same graph wiring" understates `rmk.graph_heat`, which *also* flips the sharp's sign; add "(with the reaction's sign flipped)".
- `:3317` "Hopefully this serves as a sanity check…" is softer than the surrounding prose (already noted in the first pass).

### Bibliography (new)

- **B-1 `:1354` — wrong Kock locator.** `\cite[(1.6)]{kock1972strong}` for "the associator axiom of strength": the paper uses Kock's *tensorial* strength `\sigma`, whose associativity coherence is Kock's **(1.8)** (his (1.6) is the enriched-strength composition axiom). Change `(1.6)`→`(1.8)`. The commented `\cite[(1.5)]` at `:1324`, if ever restored, should be **(1.7)** (unit coherence for `\sigma`). (Checked against Kock's "Strong functors and monoidal monads.")
- **B-2 `:3399` — Chung cites the wrong Laplacian.** The matrix at `:3393` is the *combinatorial/weighted* Laplacian `L=D-A`; Chung's *Spectral Graph Theory* reserves "the Laplacian of `G`" for the *normalized* `\mathcal L=T^{-1/2}(T-A)T^{-1/2}`. Either cite a combinatorial-Laplacian source (Godsil–Royle; or Spielman's notes) or narrow to Chung §1.2 noting it is the un-normalized `L=T-A` there.
- **B-3 `:3257` — natural-gradient overclaim.** The multiplicative stiffness update `\kappa_j\mapsto\kappa_j(1-\eta\tfrac12(x_{j+1}-x_j)^2)` is exponentiated-gradient / mirror descent, not Amari's natural gradient (which is `G^{-1}\nabla L` with `G` the *Fisher* metric on a statistical manifold — absent here). Soften to "a mirror-descent / preconditioned update" (or state the non-Fisher metric explicitly), or cite Kivinen–Warmuth instead of `amari1998natural`.
- **B-4 bib metadata.** `capucci2024actegories` title reads "Actegories for the Working **Amthematician**" — note the *arXiv title itself* carries this typo (so matching the source vs. silently correcting it is a judgment call; the first pass already flagged the visual oddness). `niu2025polynomial` `year={2024}` vs key-year 2025 and a `series={… {\em to appear}}` field that italicizes oddly — move "to appear" to `note`.

## 3. Build / PDF update

- The on-disk `dynamic-algebra-potentials.pdf` reviewed in this pass was **corrupt**: a broken xref table left ~53 of 68 page objects unreadable to Ghostscript and poppler (consistent with a watcher/clean truncating the file mid-write, and with the Highest-Priority #5 Poppler warnings). It was recompiled from the intact source via the documented chain (`pdflatex` → clean-env `biber` → `pdflatex`×2) into a valid 68-page PDF that renders cleanly: **0 overfull/underfull boxes, 0 `??`/`[?]`, all tikz/tikzcd diagrams within the text block** (including the Moore-internalization chase, the `rem.huge_wiring_diagram` composite, the particle chains, and the submersion-pullback squares). Keep the freshly built PDF; the prior one would fail to open/print in many viewers. The first pass's `latexmk` failure vs. this pass's successful manual chain suggests a `latexmk`/stale-`.bbl` interaction worth a clean `latexmk -C` before the next build.

## 4. Correction to a "Checks With No Finding"

- A cross-reference sweep in this pass initially reported "all `\termref` hyperlinks resolve" — that is **wrong**, and this file's `:458`/`term.interp` finding is the correct one (see item 1 above): `term.interp` has no anchor. Two further cosmetic label/environment mismatches surfaced (cleveref still prints correctly, but the label prefixes mislead): `ex.store` (`:746`) labels a `definition`, and `thm.functor` (`:2624`) labels a `corollary`. NOTATION.md also shows minor drift against the post-generalization source (phantom `rem.modes`; `\Lcokl{\cat M}{R}` vs the monad `\Fun R`; `\mathsf{Md}` vs table's `\mathsf{md}`; `\Phi_{\interp,\intg}` vs table's `\Phi_\intg`) — table-maintenance, for triage.
