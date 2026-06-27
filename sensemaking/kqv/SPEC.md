# The KQV attention suboperad — specification

Faithful to `../attention-suboperad/attention-suboperad.tex`; the `sec.`/`eq.`/`rmk.`/`obs.`/`ex.`
labels below refer to it. This is the object every experiment must factor through
(`../PLAN.md`); the laws asserted here are tested in `test_operad_laws.py`.

## Interfaces

A **box** is a lens object `(R^E | R^E)`, the residual stream of width `E`
(`sec.attention`, `obs.residual`). Both legs are `R^E`, so the interface is uniform
and any term substitutes into any box (arbitrary nesting type-checks).

## Generator 1 — the attention head (`con.head`), arity `N ≥ 1`

A `SmoothArrangement` `(R^E|R^E)^{⊠N} → (R^E|R^E)`. Parameter `Q` carries
`(Wq:d×E, Wk:d×E, Wv:d_v×E, Wo:E×d_v, w_star:d)` with `d = d_q = d_k`; the optimizer
is the reactive sharp on `Q` (`rmk.optimizer`, default Euclidean = plain GD; any
preconditioner is allowed *as data of `Q`*). The three maps:

- `out_f(W,h) = Wo Σ_j softmax_j(⟨w_star, Wk h_j⟩/√d) Wv h_j`  — `eq.pool`; Moore: no `n` (`rmk.moore`).
- `in_f(W,h,n)_i = Wo Σ_{j∈1..N,*} A_ij Wv h_j`, `A_i = softmax(⟨Wq h_i, [Wk h_j ; Wk n]⟩/√d)` — `eq.attn`; the `*` column is the key/value built from the outer input `n`.
- `U(W,h,n) = ½‖h − Ω n‖²`, `Ω = Wo Wv` — `eq.Uattn`; error unit (`obs.erroreunit`).

The weight count is **independent of `N`** (`rmk.supertoken`): one head applies to
any number of tokens, so a single learned head composes into trees of every shape.

**Canonical choices** (stated as such, not forced — `feedback_no_false_inevitability`):
`w_star` is a learned vector in `Q` (`eq.pool`'s learned-query option; the pooled
alternative `w_star = mean_j Wq h_j` exists); the schematic `pred` of `eq.Uattn` is
made concrete as the OV-circuit image `Ω n` of the descending context (`rmk.circuits`).

## Generator 2 — the prior box (`ex.zeroary`), arity `N = 0`

`(R^0|R^0) → (R^E|R^E)`. `out_f(q) = q` (a learned constant), `in_f` vacuous,
`U = 0`: the prior is learned from whatever environment the box is wired into,
exactly as `dap.learning.parameterized_map` (the data-marginal of `ex.zeroary`). The
uniform interface forces `in_dim_N = E` (it receives a descending message but, being
a bottom box, ignores it). Predictive-coding variant `U = ½‖q − n‖²` is deferred to
the experiment layer.

## Operad operations

- **Substitution (depth).** For a parent head of arity `N` and terms `t_1,…,t_N`
  (each targeting one width-`E` box),
  `F(Sub(parent, t)) = compose_seq( tensor_arrangements(F t_i), F(parent) )`.
  dap's `compose_seq` direct-sums the `Q`s and *adds* the potentials (the writer
  monad), so this is exactly the operadic substitution of `sarr` — nothing is
  written by hand.
- **Lens tensor (width).** `tensor_arrangements` bundles a head's `N` children;
  user-facing parallel/multi-head width is deferred to Task 1.
- **`Σ_N` action.** Permuting inner boxes; the head is equivariant (no positional
  information, `obs.equivariance`), so order requires explicit encoding.

## The generated suboperad (`obs.generate`)

Heads *generate*, they do not *close*: a composite of heads is a finite attention
network, not a single head. The suboperad is the closure of the two generators
under substitution. **Membership is by construction**: a `KQVTerm` is a generator
(`Head`) or a substitution (`Sub`); `realize = F` maps it into `sarr` using *only*
`attention_head`, `compose_seq`, `tensor_arrangements`. Hence "factors through KQV"
≡ "is `realize(t)` for some `KQVTerm t`", checkable by tracing `t`.

## Realization and interpretation

A **closed tree** (all leaves prior boxes) realizes to `(R^0|R^0) → (R^E|R^E)`:
closed at the bottom, open to the world at the root (`in_N` = descending context,
`out_N` = upward emission). It is interpreted by `Phiconf` (relaxational) or
`Phiphase` (oscillatory) into `pc` (`sec.semantics`): predictions flow down `in_f`,
errors flow up, the state relaxes to minimize `Σ U` (`slo.pc`).

**Well-posedness is conditional on the sharp (the `rmk.optimizer` knob).** The
configuration integrator is *explicit* gradient descent, so a deep tree from a
non-trivial initial state diverges if the step size is too large — exactly as
standard GD — and the conservative phase step has its own, smaller, stability
threshold. There is no universally safe step: a sensible small-`η` sharp gives
finite, non-degenerate relaxation (tested in
`test_deep_relaxation_is_well_posed_from_random_init`), while the default `η = 1`
overshoots at depth. This is a property of the chosen optimizer, not of the
suboperad; the experiment layer selects `η`/init per integrator.

## Laws tested (`test_operad_laws.py`)

shapes + arity-independent weights; uniform residual interface; Moore (`out_f` has
no `n`); error-unit `U`; `Σ_N`-equivariance; substitution type-checks and runs under
`Phiconf`/`Phiphase`; arbitrary depth + mixed arity (no cap); **functoriality of
`F`** (`Phiconf(g∘f) = Phiconf(f).then(Phiconf(g))`, forward and backward, at random
parameters); `realize` rejects non-terms; `Sub` validates arity/width.

## Modeling choices deferred to the experiment layer (NOT part of the suboperad)

- What flows under `Φ` (weights only; weights + activations; per-box free state).
- The predictive-coding leaf potential `U = ½‖q − n‖²`.
- Heterogeneous per-box predictions (needed for addressing, Task 4).
- Positional encoding, if order matters.

Keeping these out of the suboperad is deliberate: the auditor must be able to see
that the generator is the paper's head and nothing more.
