# Notation conventions for `dynamic-algebra-potentials.tex`

This file is **both** the notation table for the paper **and** the audit procedure
for verifying that the paper conforms to it. An LLM handed this file should read
this whole document, then execute the audit described in §"Audit procedure"
against `dynamic-algebra-potentials.tex` in the same directory.

The table below is a draft — assume it is incomplete and may contain errors.
Verify every claim against the `.tex` file. Do not propose fixes; only report
findings.

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

- Do NOT trust the convention table. Verify against the `.tex`.
- Do NOT stop at the first binding site for a sort. Sweep the whole paper.
- Distinguish *binding sites* (introduction) from *uses* (later reference).
  Both count; binding-site collisions are more serious.
- For overloads (one symbol, two sorts), check whether the paper ever
  disambiguates — and whether any single passage uses both senses without
  warning.
- Do NOT update this file. Output a separate report.
- Do NOT propose renames. The user decides.

---

## Convention table

### Manifolds & points

| Sort | Symbol(s) | Notes |
|---|---|---|
| Generic smooth manifold | `M`, `N` | `\mfd` for the category |
| Real vector space (object of `\rvect`) | `V`, `W` | also: domain for `T^*V` constructions |
| Point of a manifold | `m`, `n` | `m\colon\rr^0\to M` style |
| Point of a vector space | `x`, `y` | also: position in `(x,\xi)\in T^*V` |
| Tangent vector | `v`, `w` | at `T_xV`; avoid clashing with vector-space `V` |
| Covector | `\xi` | primed/indexed: `\xi'`, `\xi_V`, `\xi_M` |
| Phase point | `(x,\xi)\in T^*V` | position–momentum pair |
| State (underlying set) | `s\in S` | `S=|V|` when from a reactive vector space |

Search hints: "manifold", "vector space", "point", "covector", "tangent",
`(x,\\xi)`, `T^*_`, `T_xV`, `m\\colon\\rr^0`.

### Sections of `T^*` (covector fields / 1-forms)

A section of `T^*` is `\omega\colon M\to T^*M` for a generic manifold `M`,
specializing to the monoidal-1-form case `\omega\colon T^*V\to T^*T^*V` when
`M=T^*V`. Same sort, same symbol; the base just changes.

| Sort | Symbol(s) | Notes |
|---|---|---|
| Generic section of `T^*` | `\omega` | also names the induced nat. trans.; covers covector fields on any `M` |
| Kinetic 1-form | `\beta` | the `\sharpR`-packaging on `T^*V` |
| Dissipation 1-form | `\omega^\nu` | parameterized by friction `\nu` |
| **Forbidden for 1-forms** | `\gamma`, `\alpha` | `\gamma` used elsewhere as a generic nat. trans. |

Search hints: `"1-form"`, `"one[- ]form"`, `\\Rightarrow\\yon`,
`T^*V\\to T^*\\(T^*V\\)`, `\\colon T^*`.

### p-coalgebras and state-update maps

| Sort | Symbol(s) | Notes |
|---|---|---|
| `p`-coalgebra structure map | `f` | generic function name; `\beta`, `\phi`, `\delta` forbidden for this sort |
| State set | `S` | |
| State element | `s` | |

Search hints: `"coalgebra"`, `S\\to p\\(S\\)`, `S\\to p\\tri`, `S\\to`,
`\\to\\ihom`, every `\\colon S\\to` in the file.

### Scalars and parameters

| Sort | Symbol(s) | Notes |
|---|---|---|
| Friction / damping coefficient | `\nu \in [0,1]` | $\nu=0$ undamped, $\nu=1$ fully damped |
| Learning rate | `\eta_{\mathrm{LR}}` | never bare `\eta` (reserved, see below) |
| Generic real scalar | `\lambda`, `t` | `t` for time/index |
| Potential | `U\colon V\to\rr` | also `U\colon X\to\rr` for general state space |

Search hints: `"friction"`, `"decay"`, `"damping"`, `"dissipat"`,
`"learning rate"`, `"potential"`, `U\\colon`, `\\to\\rr`.

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
| Reactive sharp | `\sharpR_V`, `\sharpR_x` | section / fiber-evaluated |
| Symplectic (canonical) sharp | `\sharpS_{T^*V}` | always on `T^*V` |
| Euclidean sharp | `\sharpEuc{}` | constant case |
| Lens backward map | `\bk{\varphi}{i}` | **never** `\varphi^\sharp` (clashes with `\sharpR`, footnote line 750) |

### Polynomial functors

| Sort | Symbol(s) | Notes |
|---|---|---|
| Generic polynomial | `p`, `q` | |
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
