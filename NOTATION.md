# Notation conventions for `dynamic-algebra-potentials.tex`

This file is **both** the notation table for the paper **and** the audit procedure
for verifying that the paper conforms to it. There are two distinct operations on
it, and they must never blur together:

- **Maintain** — the convention table is the canonical spec. When you deliberately
  change a convention, update the table *in the same commit* as the `.tex` change.
  Updating the table is an intentional, attributed edit — never a side effect of
  another task.
- **Audit** — verify the paper conforms to the table. Read-only on both files;
  emit a separate report; change nothing. See §"Audit procedure". Run it against a
  committed snapshot (compare working-tree `.tex` against `git show HEAD:NOTATION.md`),
  so the spec under test is frozen by git rather than by trust.

Triage — deciding, per audit finding, whether the *paper* is wrong (fix the paper)
or the *table* is stale (a maintain edit) — is a separate, user-owned step. Neither
side effect happens inside an audit.

An LLM handed this file *to audit* should read this whole document, then execute the
audit described in §"Audit procedure" against `dynamic-algebra-potentials.tex` in the
same directory. When auditing, treat the table as a draft under test: assume it is
incomplete and may contain errors, verify every claim against the `.tex`, and report
findings only — do not propose fixes.

---

## Audit procedure — instructions for LLMs

Your job is a **sortal notation audit**: every mathematical sort (1-form,
covector, coalgebra structure map, etc.) should have a designated symbol or
symbol family, and every binding site in the paper should match. Sortal
collisions — one sort named by two different symbols, or one symbol naming two
sorts — are what you are hunting for.

### The failure mode to avoid (historical worked example)

An earlier draft of this file recorded a row like

> coalgebra structure map | `\beta\colon S\to\ihom{p,q}\tri S` | …

citing the use of `\beta` for a coalgebra structure map in `sec.org`. That was
*one* binding site, but `sec.coalgebras` already defined a `p`-coalgebra as a
pair `(S,f)` with `f\colon S\to p(S)`. A later sweep then found `\phi` (in the
proof of `prop.coalg_as_poly_map`, as a polynomial map *in bijection with*
a coalgebra) and `\delta_{\mathrm{gen}}` (in `sec.dl_warmup`, for the
training-data coalgebra). Four symbols, one sort. The original table hid this
because it was built by looking *at* `\beta`, not *for* "every symbol naming a
coalgebra anywhere." (The paper has since been normalized to `f` everywhere;
this entry is preserved as a cautionary tale.)

This is the precise failure you must avoid: **looking at symbols instead of
sweeping for sorts**. A symbol-first sweep cannot find a sort with two symbols.

### Pass 1 — SORT → SYMBOL (do this first; this is the hard direction)

For each sort listed in §"Convention table" below — and any additional sort
you discover — grep the **full paper** for binding sites of that sort. A
*binding site* is any place an object of that sort is introduced, named, or
quantified over, regardless of which symbol is used. List every distinct
symbol you find binding to that sort.

If a sort uses more than one symbol across the paper, flag it as a **sortal
collision** and report all symbols with `file:line` citations.

Search hints are deliberately broad. Treat them as starting points, not
complete queries. Enumerate every `\begin{definition}`, `\begin{example}`,
`\begin{notation}`, and `\begin{proposition}` block too — they bind sorts.

### Pass 2 — SYMBOL → SORT

For each symbol the convention table designates for a sort, grep every
occurrence in the paper and confirm sort agreement. Flag any binding whose
sort disagrees. Also flag any symbol the table marks "forbidden for sort X"
that does in fact bind to sort X anywhere.

### Output format

A single report with three sections. No prose summary. No fix recommendations.

**§1. Pass-1 findings** (sort → symbols). One block per sort:
```
SORT: <name>
SYMBOLS FOUND: <each distinct symbol, with first ~3 binding-site citations>
COLLISION: yes/no
NOTES: <e.g. "f in sec.coalgebras (790) but \beta in lines 553, 1208">
```

**§2. Pass-2 findings** (symbol → sorts). Violations of the convention table.

**§3. New sorts** you discovered that aren't in the table but should be. One
row per: sort, symbol(s) found, citations.

### Discipline checklist

These rules govern an **audit run** (read-only). They do not apply to a *maintain*
edit, where updating the table is the whole point.

- Do NOT trust the convention table. Verify against the `.tex`.
- Do NOT stop at the first binding site for a sort. Sweep the whole paper.
- Distinguish *binding sites* (introduction) from *uses* (later reference).
  Both count; binding-site collisions are more serious.
- For overloads (one symbol, two sorts), check whether the paper ever
  disambiguates — and whether any single passage uses both senses without
  warning.
- During an audit, do NOT edit this file or the `.tex`. Output a separate report;
  report table/paper drift as findings rather than fixing it.
- Do NOT propose renames during an audit. The user decides at triage.

---

## Convention table

### Manifolds & points

| Sort | Symbol(s) | Notes |
|---|---|---|
| Generic smooth manifold | `M`, `N` | `\mfd` for the category |
| Reactive vector space (object of `\rvect`) | `\rv Q`=`(Q,\sharpR_Q)` | bold `\rv` macro; emphasizes sharp-dependence (e.g. `\chiQ{\rv Q}`) |
| Underlying / carrier vector space | `Q`, `W` | also: domain for `T^*Q` constructions; abused for the object `\rv Q` when sharp is understood or canonical (`T^*Q`) |
| Point of a manifold | `m`, `n` | `m\colon\rr^0\to M` style |
| Point of a vector space | `q` | element tracks the carrier `Q`; position in `(q,\xi)\in T^*Q`; second point `q'`, indexed `q_1,\ldots,q_K` (physics generalized coordinates). `x` is retired as a point, and `q` is never a polynomial |
| Tangent vector | `v`, `w` | at `T_qQ`; avoid clashing with vector-space `Q` |
| Covector | `\xi` | primed/indexed: `\xi'`, `\xi_Q`, `\xi_M`; a covector on a doubled space is written as the pair `(\xi,q)`, never named `\alpha` (`rmk.symplectic_perpendicular`) |
| Phase point | `(q,\xi)\in T^*Q` | position–momentum pair |
| State (underlying set) | `s\in S` | `S=|Q|` when from a reactive vector space |

Search hints: "manifold", "vector space", "point", "covector", "tangent",
`(x,\\xi)`, `T^*_`, `T_xQ`, `m\\colon\\rr^0`.

### Sections of `T^*` (covector fields)

A section of `T^*` is `\omega\colon M\to T^*M` for a generic manifold `M`; on `T^*Q` we use the kinetic datum `\beta`.

| Sort | Symbol(s) | Notes |
|---|---|---|
| Generic section of `T^*` | `\omega` | a covector field on a manifold `M`; also names an induced nat. trans. |
| Kinetic datum | `\beta` | the `\sharpR`-packaging `\beta_Q(x,\xi)=(0,\sharpR_x\xi)` on `T^*Q`; term-tracked (`\trackTermSymbol{beta_kin}`), anchor `\defineTerm{beta_kin}_Q` at `eqn.kinetic_one_form` |

Search hints: `"kinetic"`, `\\beta`, `\\colon T^*`.

### p-coalgebras and state-update maps

| Sort | Symbol(s) | Notes |
|---|---|---|
| `p`-coalgebra structure map | `f` | generic function name; `\beta`, `\phi`, `\delta` forbidden for this sort |
| State set | `S` | |
| State element | `s` | |

Search hints: `"coalgebra"`, `S\\to p\\(S\\)`, `S\\to p\\tri`, `S\\to`,
`\\to\\ihom`, every `\\colon S\\to` in the file.

### Integrators & dynamics functors

| Sort | Symbol(s) | Notes |
|---|---|---|
| Parameter interface | `p` | strong monoidal functor `\cat Q\to\poly`; `p_a` (=`p(a)`) is a polynomial for each `a:\cat Q`. Deliberately the generic-polynomial letter, since it is a poly-valued functor; generic polynomial *objects* are primed (`p'`, `p''`), with a probe/variable object `a` |
| State space | `\Fun S` | strong monoidal functor `\cat Q\to\smsetiso`; `\Fun S(a)` is the state set |
| Integrator | `\intg` (renders `\mathfrak{i}`) | the pair `\intg=(\Fun S,\upd)` (`def.integrator`). Instances: `\intg_{\mathrm{conf}}` (configuration, `\Fun S=\absval\blank`) and `\intg_{\mathrm{phase}}` (phase, `\Fun S=\absval{T^*\blank}`) |
| Update | `\upd` (renders `u`) | the second component of an integrator: a monoidal nat. trans. `\Store\circ\Fun S\Rightarrow p`. Instances: `\chi` (configuration; `\chiQ` for its `\rv Q`-component, distinct from the lax/colax `\theta` of line 213), `\upd_\beta` (phase). The `\Para_{\cat Q}^\upd` functors in `prop.integrator_to_org` carry the update as superscript (the action-square datum) and the acting category `\cat Q` as subscript (the identity `F`, per the suppression convention after `prop.para_square`) |
| Kinetic update | `\nu` | the monoidal nat. trans. `\cot\circ T^*\Rightarrow\cot` that reads out the position and injects `(\xi',\sharpR_x\xi)`; the phase update factors as `\upd_\beta=\nu\circ\chiQ{T^*\blank}` (`sec.phase_integrators`). Greek `\nu`, distinct from `\upd` (which renders `u`) |
| Integrator semantics | `\Psisem` (renders `\Psi`) | `\Psi_\intg\colon\para p\poly\to\org` (`prop.integrator_to_org`); indexed by the integrator pair |
| Dynamics functor | `\Phi_{\interp,\intg}`, `\Phip{\interp}` | `\Phi_{\interp,\intg}\colon\rwd_D\to\org` (`thm.dynamics_functor`), smooth instance `\Phi_\intg\colon\srwd\to\org` (`cor.functor`); `\Phip{\interp}` (the macro `\Phip[1]{\Phi'_{#1}}`, renders `\Phi'_\mathfrak{p}`) is the polynomial-interpretation factor into `\para{\Fun c\circ J}\poly` (`thm.poly_interpretation`). **Always write `\Phip{...}`, never a bare `\Phi'`** — the subscript is the in-scope interpretation `\interp` (`\mathfrak p`); the one definitional unfolding `\Phip{\interp}=\Phi'_{\cot,(\yon,\potd)}` is at `prop.smooth_setup`. Named: `\Phiconf=\Phi_{\intg_{\mathrm{conf}}}`, `\Phiphase=\Phi_{\intg_{\mathrm{phase}}}`. See §"Abstract framework" |

Search hints: `"integrator"`, `\\intg`, `\\Store\\circ`, `\\Rightarrow p`, `\\upd`, `\\Fun S`, `\\Psisem`, `\\Phi_`, `\\Phip`.

### Abstract framework (rewiring data)

A *rewiring datum* is `D = (\cat M, \cat Q, J, \Fun R)` (`def.rewiring_datum`), introduced in
`ch.framework`; the syntax operad `\rwd_D` depends only on it. Interpreting that syntax
adds an interface functor `\Fun c` into `\poly` and a potential algebra `(z,\alpha)` (the
polynomial interpretation, `sec.poly_interpretation`); an integrator then gives the dynamics functor into
`\org`. The smooth instance plugs in the rewiring datum `\Sm = (\mfd, \rvect, \inc, \rr)`
(`def.potlens`) with interface functor `\Fun c = \cot` and potential algebra
`(z,\alpha) = (\yon, \potd)` (`prop.smooth_setup`); the rightmost column gives it.

| Sort | Symbol | Notes | Smooth instance |
|---|---|---|---|
| Rewiring datum (whole tuple) | `D = (\cat M, \cat Q, J, \Fun R)` | `def.rewiring_datum`; determines the syntax operad `\rwd_D` | `\Sm` (`def.potlens`, renders `\mathrm{Sm}`) |
| Spaces (cartesian category) | `\cat M` | source of lens syntax | `\mfd` |
| Parameters (sym. monoidal category) | `\cat Q` | acts on `\cat M` via `J`; font-distinct from the carrier `Q` | `\rvect` |
| Parameter inclusion | `J\colon\cat Q\to\cat M` | strong monoidal | `\inc` |
| Potentials monad | `\Fun R` | monoidal monad on `\cat M` (`def.rewiring_datum`); the writer monad `R\otimes\blank` of a commutative **monoid** `R` (not a group — no antipode used) is the canonical instance | `\rr` (writer monad `\rr\otimes\blank`) |
| Interface functor | `\Fun c` | strong monoidal `\cat M\to\poly`; sans-serif like `\cot`; the `p` of `def.integrator` is `\Fun c\circ J`. **Forbidden clash:** the lens component `c` and the friction `c` | `\cot` |
| Potential algebra | `(z,\alpha)` | `\otimes`-monoid `z` with a `\Fun R'`-monoid structure `\alpha` (`def.T_monoid`; `\Fun R'=\Fun c(R)\otimes\blank` in the writer instance). `\alpha` is reserved for this map: **not** covectors (write the pair) nor `\Para` 2-cells (use `g`, `prop.para`). The submersion-lens backward map in `prop.euler_submersion_lenses` reuses `\alpha` locally—sanctioned, since that proof never co-occurs with the potential algebra | `(\yon,\potd)` |
| Set of modes | `\md` (`\mathsf{Md}`) | finite set decorating a monad via the power `(\blank)^{\md}` (`prop.moding`, `prop.moded_algebra`); a mode is an element `i\in\md`. Sans-serif to stay clear of the space `M` and the category `\cat M`; element indexed by `i` to stay clear of the manifold point `m` | single-mode `z=\yon` |
| Rewiring-diagram operad | `\rwd_D` (renders `\mathbb{R}\Cat{WD}_D`; blackboard `\mathbb{R}` marks it as a (2,1)-operad, in-family with `\org`) | underlying operad of `\para{\cat Q}{\Lcokl{\cat M}{\Fun R}}` (`def.rewiring_datum`) | `\srwd \coloneqq \rwd_{\Sm}` by definition (`def.potlens`); `\srwd` expands to `\rwd_{\Sm}` (renders `\mathbb{R}\Cat{WD}_{\mathrm{Sm}}`) |

Search hints: `"rewiring datum"`, `\\rwd`, `\\Sm`, `\\cat M`, `\\cat Q`, `\\Fun c`,
`def.rewiring_datum`, `def.potlens`, `thm.dynamics_functor`, `cor.functor`.

Named (smooth) rewiring diagrams use the wiring family: `\Part` (particle), `\boxob` (box), `\fun{wire}_K` (K-ary wiring), `\fun{wire}_G` (graph `G`'s wiring, `eqn.psi_graph_lap`). `\psi` is **not** used for these—it is only a local proof variable and the second of a composable `(\varphi,\psi)` pair.

### Scalars and parameters

| Sort | Symbol(s) | Notes |
|---|---|---|
| Learning rate | `\eta_{\mathrm{LR}}` | never bare `\eta` (reserved, see below) |
| Generic real scalar | `c`, `t` | `c\in\rr` for scalar multiplication; `t` for time/index. (`\lambda` is taken — dual-pairing element at `eqn.canonical_dual_sum`.) |
| Potential | `U\colon Q\to\rr` | `V` for a second potential in a composite (`g\circ f`); also `U\colon X\to\rr` for general state space |

Search hints: `"learning rate"`, `"potential"`, `U\\colon`, `\\to\\rr`.

### Categorical structure (reserved, line 696)

| Sort | Symbol | Notes |
|---|---|---|
| Unit (monad, group, monoid, …) | `\eta` | never use bare `\eta` for anything else; Lie-group identity is OK |
| Multiplication (monad, group, monoid, …) | `\mu` | Lie-group multiplication is OK |
| Comonoid counit | `\varepsilon` | |
| Comonoid comultiplication | `\delta` | never for a coalgebra structure map — use `f` (see below) |
| Strong-monad strength | `\sigma` | the Kock strength. The *product comparison* of a strong monoidal functor is its **productor** `F_2`, e.g. `(T^*)_2` (`prop.TT_monoidal`)—**not** `\sigma` |
| Lax/colax structure map | `\theta` | |

### Reactive vector spaces & sharp maps

| Sort | Symbol(s) | Notes |
|---|---|---|
| Reactive sharp | `\sharpR_Q`, `\sharpR_q` | section / fiber-evaluated; the data distinguishing the object `\rv Q=(Q,\sharpR_Q)` |
| Symplectic (canonical) sharp | `\sharpS_{T^*Q}` | always on `T^*Q` |
| Euclidean sharp | `\sharpEuc{}` | constant case |
| Lens backward map | `\bk{\varphi}{i}` | **never** `\varphi^\sharp` (clashes with `\sharpR`, footnote line 750) |

### Polynomial functors

| Sort | Symbol(s) | Notes |
|---|---|---|
| Generic polynomial | `p`, `p'`, `p''` | the parameter-interface functor is *also* `p` (a poly-valued functor `\cat Q\to\poly`, `p_a:\poly`); see §"Integrators & dynamics functors". Second and third polynomials are **primed** (e.g. composition `[p,p']\otimes[p',p'']\to[p,p'']`); a probe/variable object (tensor--hom, internal hom) is `a`. **`q` is never a polynomial**---it denotes a point of `Q` (full-consistency rename, 2026-06-05) |
| Position set | `p(1)` | |
| Directions at `i` | `p[i]` | |
| Cotangent polynomial | `\cotof{M}` | from `\cot\colon\mfd\to\poly` |
| Representable | `\yon^N`, just `\yon` | `\defineTerm{yon}\coloneqq\yon^1` |

### Lenses

| Sort | Symbol(s) | Notes |
|---|---|---|
| Lens object | `\lensob{c}` | binomial `\binom{\inpt c}{\outp c}` |
| Lens morphism | `f\colon\lensob c\to\lensob d` | components: `\inpt f`, `\outp f` |

#### `\Cat{Lens}` decoration rule

One rule governs all four gadgets: **subscript = base/functor direction, superscript = monad/monad-map direction.**

| Gadget | Symbol | Macro | Defined at |
|---|---|---|---|
| Lens category | `\Cat{Lens}_{\cat C}` | `\Lens{\cat C}` | `def.Lens` |
| Lens functoriality (on a functor `F`) | `\Cat{Lens}_F` | `\Lens F` | `prop.lens_functoriality` |
| Backward comonad (from a monad `\Fun T`) | `\Cat{Lens}^{\Fun T}` | `\LensFun{\Fun T}` | `prop.backward_comonad` |
| Induced coKleisli functor (from `(F,\theta)`) | `\Cat{Lens}_F^\theta` | `\LensMor{F}{\theta}` | `lem.lens_T_functoriality` |

- The comonad is the `F=\id` (empty subscript) special case of the induced functor.
- In `rem.filtration` the induced functor appears as `\LensMor{\cat M}{\eta}` = `\Cat{Lens}_{\cat M}^\eta` (the `F=\id_{\cat M}`, `\theta=\eta` case; `\cat M` is `\id_{\cat M}` by the "category name = its identity functor" convention stated in `sec.prelim`).
- On objects the induced functor agrees with `\Cat{Lens}_F`, so its object-action is written `F\lensob c` (not `\LensMor{F}{\theta}\lensob c`).

### Priming convention (line 2152)

- `f'` does **not** mean derivative.
- Priming indicates "analogous to `f`".
- Use this for `\xi'` (cotangent input vs. stored momentum) and `q'` (a second point of `Q`).
