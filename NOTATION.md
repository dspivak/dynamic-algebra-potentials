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
| Reactive vector space (object of `\rvect`) | `\rv V`=`(V,\sharpR_V)` | bold `\rv` macro; emphasizes sharp-dependence (e.g. `\thetaV{\rv V}`) |
| Underlying / carrier vector space | `V`, `W` | also: domain for `T^*V` constructions; abused for the object `\rv V` when sharp is understood or canonical (`T^*V`) |
| Point of a manifold | `m`, `n` | `m\colon\rr^0\to M` style |
| Point of a vector space | `x`, `y` | also: position in `(x,\xi)\in T^*V` |
| Tangent vector | `v`, `w` | at `T_xV`; avoid clashing with vector-space `V` |
| Covector | `\xi` | primed/indexed: `\xi'`, `\xi_V`, `\xi_M` |
| Phase point | `(x,\xi)\in T^*V` | position–momentum pair |
| State (underlying set) | `s\in S` | `S=|V|` when from a reactive vector space |

Search hints: "manifold", "vector space", "point", "covector", "tangent",
`(x,\\xi)`, `T^*_`, `T_xV`, `m\\colon\\rr^0`.

### Sections of `T^*` (covector fields)

A section of `T^*` is `\omega\colon M\to T^*M` for a generic manifold `M`; on `T^*V` we use the kinetic datum `\beta`.

| Sort | Symbol(s) | Notes |
|---|---|---|
| Generic section of `T^*` | `\omega` | a covector field on a manifold `M`; also names an induced nat. trans. |
| Kinetic datum | `\beta` | the `\sharpR`-packaging `\beta_V(x,\xi)=(0,\sharpR_x\xi)` on `T^*V`; term-tracked (`\trackTermSymbol{beta_kin}`), anchor `\defineTerm{beta_kin}_V` at `eqn.kinetic_one_form` |

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
| Parameter interface | `p` | strong monoidal functor `\cat A\to\poly`; `p_a` (=`p(a)`) is a polynomial for each `a:\cat A`. Deliberately the generic-polynomial letter, since it is a poly-valued functor; generic polynomial *objects* in this section are `q` |
| State space | `\Fun S` | strong monoidal functor `\cat A\to\smsetiso`; `\Fun S(a)` is the state set |
| Integrator | `\intg` (renders `\mathfrak{i}`) | the pair `\intg=(\Fun S,\upd)` (`def.integrator`). Instances: `\intg_\theta` (configuration, `\Fun S=\absval\blank`) and `\intg_\beta` (phase, `\Fun S=\absval{T^*\blank}`) |
| Update | `\upd` (renders `u`) | the second component of an integrator: a monoidal nat. trans. `\Store\circ\Fun S\Rightarrow p`. Instances: `\theta` (configuration), `\upd_\beta` (phase). The `\Para_{\cat A}^\upd` functors in `prop.integrator_to_org` carry the update as superscript (the action-square datum) and the acting category `\cat A` as subscript (the identity `F`, per the suppression convention after `prop.para_square`) |
| Kinetic update | `\nu` | the monoidal nat. trans. `\cot\circ T^*\Rightarrow\cot` that reads out the position and injects `(\xi',\sharpR_x\xi)`; the phase update factors as `\upd_\beta=\nu\circ\thetaV{T^*\blank}` (`sec.phase_integrators`). Greek `\nu`, distinct from `\upd` (which renders `u`) |
| Integrator semantics | `\Psisem` (renders `\Psi`) | `\Psi_\intg\colon\para p\poly\to\org` (`prop.integrator_to_org`); indexed by the integrator pair |
| Dynamics functor | `\Phi_\intg`, `\Phi'` | `\Phi_\intg\colon\srw\to\org`; `\Phi'` the syntax→`\para\cot\poly` factor. Named: `\Phiconf=\Phi_{\intg_\theta}`, `\Phiphase=\Phi_{\intg_\beta}` |

Search hints: `"integrator"`, `\\intg`, `\\Store\\circ`, `\\Rightarrow p`, `\\upd`, `\\Fun S`, `\\Psisem`, `\\Phi_`.

### Scalars and parameters

| Sort | Symbol(s) | Notes |
|---|---|---|
| Learning rate | `\eta_{\mathrm{LR}}` | never bare `\eta` (reserved, see below) |
| Generic real scalar | `c`, `t` | `c\in\rr` for scalar multiplication; `t` for time/index. (`\lambda` is taken — dual-pairing element at `eqn.canonical_dual_sum`.) |
| Potential | `U\colon V\to\rr` | also `U\colon X\to\rr` for general state space |

Search hints: `"learning rate"`, `"potential"`, `U\\colon`, `\\to\\rr`.

### Categorical structure (reserved, line 671)

| Sort | Symbol | Notes |
|---|---|---|
| Unit (monad, group, monoid, …) | `\eta` | never use bare `\eta` for anything else; Lie-group identity is OK |
| Multiplication (monad, group, monoid, …) | `\mu` | Lie-group multiplication is OK |
| Comonoid counit | `\varepsilon` | |
| Comonoid comultiplication | `\delta` | never for a coalgebra structure map — use `f` (see below) |
| Strong-monad strength | `\sigma` | |
| Lax/colax structure map | `\theta` | |

### Reactive vector spaces & sharp maps

| Sort | Symbol(s) | Notes |
|---|---|---|
| Reactive sharp | `\sharpR_V`, `\sharpR_x` | section / fiber-evaluated; the data distinguishing the object `\rv V=(V,\sharpR_V)` |
| Symplectic (canonical) sharp | `\sharpS_{T^*V}` | always on `T^*V` |
| Euclidean sharp | `\sharpEuc{}` | constant case |
| Lens backward map | `\bk{\varphi}{i}` | **never** `\varphi^\sharp` (clashes with `\sharpR`, footnote line 750) |

### Polynomial functors

| Sort | Symbol(s) | Notes |
|---|---|---|
| Generic polynomial | `p`, `q` | the parameter-interface functor is *also* `p` (a poly-valued functor `\cat A\to\poly`, `p_a:\poly`); see §"Integrators & dynamics functors". Generic polynomial *objects* in the integrator section are `q`, to avoid clash |
| Position set | `p(1)` | |
| Directions at `i` | `p[i]` | |
| Cotangent polynomial | `\cotof{M}` | from `\cot\colon\mfd\to\poly` |
| Representable | `\yon^N`, just `\yon` | `\defineTerm{yon}\coloneqq\yon^1` |

### Lenses

| Sort | Symbol(s) | Notes |
|---|---|---|
| Lens object | `\lensob{c}` | binomial `\binom{\inpt c}{\outp c}` |
| Lens morphism | `f\colon\lensob c\to\lensob d` | components: `\inpt f`, `\outp f` |

### Priming convention (line 724)

- `f'` does **not** mean derivative.
- Priming indicates "analogous to `f`".
- Use this for `\xi'` (cotangent input vs. stored momentum).
