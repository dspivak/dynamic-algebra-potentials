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

## Generator 3 — the activation cell (route 2; IMPLEMENTED & AUDITED 2026-06-29)

Built in `kqv/cell.py` (`activation_cell`, `act_block_sharp`, plus the optional `z`-prior),
wired into the grammar in `kqv/operad.py` (`Act`; `Sub.parent` generalized to arity-≥1
generators), tested in `kqv/test_activation_cell.py` (G1–G5 + the atom saddle), exercised in
`experiments/activation_tower.py`. G1–G5 and the operad laws pass. See **Findings** and
**Generator 4** below for what running it taught us.

A relaxable **state** carrier, so *inference* (relaxing activations, not just weights)
factors through KQV instead of living in the environment. It is a `SmoothArrangement`, so
adding it keeps us a **suboperad of `sarr`** (the closure of more sarr-generators under
the *same* ops). Two constraints make that true: (i) the carrier `Z` is a **vector
space** (R-vect) — a discrete state machine would leave `sarr` and is out of scope; (ii)
no new operad *operation* — substitution + lens tensor only (a feedback/closure wire is
not operadic).

**Type.** Arity-1 cell `(R^E|R^E) → (R^E|R^E)` — a state box on a wire, so activations
can sit at *interior* levels. *(Open choice A: this cell vs an arity-0 leaf = the
`ex.zeroary` PC-variant. The cell lets `z` live between heads.)*

**Carrier.** `Q = Z ⊕ Hom(R^k, R^E)` — a fast **activation** `z ∈ Z = R^k` (the cause) and a slow **decode** `D : R^k → R^E`, under a **block sharp** (`z` fast, `D` slow); `k ≤ E` gives the
**bottleneck**, and like `d_v` the rank `k` never reaches the interface. Audit fix: `D` is *learned*, so it lives in `Q` — not a constant smuggled outside (take `D`
fixed ⇒ `Q = Z`, but learned `D` is the design).

**Maps.**
- `out_f(z,h) = D z` — emit the cause upward; Moore (no `n`). The forward output is the
  cell's *own state*, which is what makes `z` the thing read above.
- `in_f(z,h,n) = n` — transparent backward leg: the descending prediction passes through
  to the child. *(Open: identity vs a learned map.)*
- `U(z,h,n) = ½‖h − D z‖²` — bottom-up reconstruction: the activity below should match the
  cause's prediction. This is `ex.zeroary`'s deferred PC-potential, promoted and given a
  child. *(Open: add a top-down term `½‖D z − n‖²` for a symmetric Rao–Ballard cell.)*

**Input = projection by inference.** There is no explicit encoder `R^E → R^k`: the child
`h` enters *only* through `U`, and relaxing `z` to minimize `½‖h − D z‖²` *is* the
projection `z* = D⁺h` of `h` into the code (add an explicit `P` only for a feedforward
encode).

**Role.** Cells are the **level states** `z_ℓ`; heads are the **maps between levels**.
They alternate up the tower (`z, head, z, head, …`); a cell is neither higher nor lower
than a head — it is the state a head reads and writes. Relaxing `z` causes **lossy
compression**: `z` becomes the `k`-dim projection of the activity below; stacked, this is
the abstraction tower and `z_top` (most compressed) is the sense.

**Bare cell (the atom).** In isolation — no head inside or outside — a cell is a linear
autoencoder with an inferred code: clamp `x` below, relax to `z* = D⁺x`, emit `D z` (`n`
unused). Well-posed (unique minimizer at full column rank), so the atom does not collapse.
But bare cells *alone* are linear and **stack to a single projection**; the heads supply
the softmax nonlinearity, multi-input mixing, and top-down prediction. Cells compress;
heads transform and predict.

**Sharp.** A **fast** reactive sharp (large `η`), block-structured so activations relax
faster than the weights — data of `Q` (`rmk.optimizer`), **not** an external optimizer;
the fast/block structure must be written into the sharp (the auditor's caution).

**Substitution.** Arity-1, single-box target — a legal `Sub` child, and a head
substitutes into it; realized by `compose_seq` like any arrangement. Verified: the interleaved
tower `… → g → cell(z) → g → …` runs under one `Phiconf` and, from random init, relaxes each
`z` to a datum-dependent code (see **Findings**; from near-zero init it freezes — the dead
zone, now understood as a cold-start artifact rather than the decisive test).

**Term grammar (audit fix).** `Sub.parent` generalizes from `Head` to *any arity-≥1
generator* (now incl. `Act`) — a more general grammar, **not** a new operation. So this is
an *enlarged* suboperad, not the original heads-plus-priors one.

**Top-closure caveat.** A learned prior `½‖z_top − μ‖²` (free `μ`) is a route-2
*potential*, not feedback; only closing the top *output* back into its own *input* is
route 3.

**Bilinear dead zone (FINDING, not just a risk).** `(z,D)=(0,0)` is a *saddle* for a single
clamped cell — it escapes from random init (`test_atom_escapes_from_random_init`). But in a
*tower* the dead zone is **pervasive and depth-amplified**: every bilinear box (each cell's
`(z,D)` and each head's `Ω=Wo Wv`) has its own near-zero stationary point, and they compound,
so from near-zero init the whole tower stays frozen (0% relaxation, `‖D‖,‖Ω‖` at init —
`experiments/activation_tower.py`). The sanctioned levers (small noise, `init≤0.1`) do **not**
escape; the `z_top` prior breaks the top's silence only to pin `z_top→μ0` (datum-*independent*),
because the frozen tower below starves it of signal. **Resolution (per the user): near-zero
init is the wrong bar — use random init.** From random init the tower escapes; the dead zone
is a cold-start artifact of bilinear/PC systems, not a property of the suboperad. (So the
earlier "near-zero test is decisive" framing is retired.)

**Trace.** `act(k=…, E=…)`.

## Findings from the Generator-3 tower (2026-06-29; `experiments/activation_tower.py`)

The interleaved tower `data → head → cell → … → cell(top)`, data clamped at the bottom,
relaxed under one `Phiconf`, read at `z_top`, was built and run. From **random init** it
half-works: `z_top` is genuinely datum-dependent (cos ≈ −0.99 across two data) but tiny, and
only ~⅓ of the clamped data is reconstructed. The ⅓ is **structural**, and naming it is the
result:

1. **The head is a shared-structure extractor.** `eq.Uattn`'s prediction `pred = Ω·n` is a
   *single* `R^E` vector compared against all `N` inner emissions (broadcast). The best single
   prediction is the inputs' mean, so a head can only explain what its `N` boxes *share* —
   ~`1/N` of the energy for independent inputs (4 i.i.d. tokens → ~25–33%, the measured ⅓).
   This is `eq.Uattn` doing exactly what it says, not bad tuning or a stalled `sharp`.

2. **i.i.d. data is the wrong test.** Independent tokens have nothing to compress, so "⅓ = the
   mean" is correct, not a failure. Sense-making needs a low-dim shared cause — hierarchically
   structured data: locality up close, coarse shared causes at a distance.

3. **Capacity is not the wall.** The reactive state is unlimited; the cap is (a) the broadcast
   prediction (one vector) and (b) the descending interface width `E` (one `R^E` per box,
   `obs.residual`). A wide state does not lift the cap while `pred` is one vector; you also
   need a token-specific prediction *and* a wide per-datum source — at which point the box
   predicting each child from its own wide state *is a cell*. So: **heads summarize shared
   structure; cells reconstruct**; compress only where you intend a bottleneck (`z_top`), not
   at every interface.

## Generator 4 — the residual head (PROPOSED; reasoned 2026-06-29, NOT yet built)

The design the findings point to: a hierarchy that sends **compressed residuals** up, so each
level works on what the level below could not explain (Rao–Ballard, `rmk.corners`). This
generator is the *forward* (`out_f`) residual channel, distinct from the lens's existing
*backward* error covector.

- **Idea.** A box predicts its `N` children from its **own state** (cell-like `D·z`), forms
  the residual `r = h − D·z`, **compresses** it (a learned encoder = the bottleneck, so the
  upward message stays bounded and does not grow up the tree), and emits the code via `out_f`.
  The boss reads residual-codes from several children and models *their* shared structure —
  finding longer-range / coarser causes level by level.
- **Why `out_f` (forward), not the covector.** The lens already sends an error up the backward
  channel (`dU/dn = Ωᵀ·Σ residuals`), but it is *summed* over boxes (loses which-box-is-off)
  and *projected through the broadcast `Ω`*. An **appended-then-learned-compressed** residual
  in `out_f` preserves cross-box structure ("boxes 3 and 6 are jointly off") — exactly what a
  higher level needs to couple a distant correlated pair.
- **Moore is load-bearing.** `out_f` cannot see the descending context `n` (`rmk.moore`), so
  it *cannot* subtract the top-down prediction `Ω·n` — which is precisely why the framework
  parks the top-down error in the backward covector. The fix that stays Moore-legal: subtract
  the box's **own state** `D·z` (a function of `(h, q)` only), not `n`. This is iterative PC —
  each level's residual is relative to its own running explanation.
- **Faithfulness target (audit A″).** Still a `SmoothArrangement`: R-vect carrier, block sharp,
  no new operad op; `out_f` a smooth function of `(q, h)` only (Moore); `U` an error-unit
  (`½‖h − D·z‖²`). The novelty is *what `out_f` emits* — a compressed residual, not `eq.pool`'s
  pooled activity — so it is a **different generator**, audited on its own terms.
- **The hope, reasoned (the bet).** The hierarchy helps a distant pair (box 3 in medium A,
  box 6 in medium B, same grandparent) **iff** their correlation is carried by a low-dim cause
  shared at the grandparent scale that survives each level's compression. `ΣU`-descent has the
  right *pressure* (preserving the 3↔6 feature lowers total error), but whether `Phiconf`
  actually *discovers* the multi-scale residual-compressors — vs. settling for the shared-mean
  code — is the open question, and what codex should bet on (`../AUDIT.md`, **Bet**).

## Generator 5 — the coincidence head (second order; IMPLEMENTED & VALIDATED 2026-06-30)

Built in `kqv/coincidence.py` (`coincidence_head`), wired into the grammar as `Coinc` in
`kqv/operad.py`, tested in `kqv/test_coincidence.py`, demonstrated in
`experiments/coincidence_tower.py`. The **first degree-2 generator** — the moment hierarchy.

**Why.** The attention head's read-out (`eq.pool`) is a *first-order* statistic (a weighted
mean), so it is blind to **coincidences**: "child i and child j fired together" is a product
`h_i ⊗ h_j`, which no mean can see. The coincidence head sends up a **second moment** instead.

**Maps** (`r` = feature rank; carrier `(V, Wo, G)` — see the `.tex` catalog `sec.catalog`):
- `out_f(V,Wo,G ; h) = Wo·vech(P Pᵀ)`, `P = Σ_j V h_j` — degree-2 read-out; Moore, no `n`.
  Squaring the pool exposes the cross terms `(V h_i)(V h_j)ᵀ`, the coincidences.
- `in_f(. ; h, n)_i = n` — transparent backward leg.
- `U(V,G ; h, n) = ½‖vech(P Pᵀ) − G n‖²` — *second-order predictive coding*: predict the
  coincidence structure from above; the residual is the **unexpected coincidence**.

**Faithful** (a clean enlarged suboperad): arity-independent weights (the pool `Σ_j` is the
only `K`-dependence, `rmk.supertoken`), permutation-invariant (`obs.equivariance`), Moore
(`rmk.moore`), R-vect carrier, block/Euclidean sharp, substitution + lens tensor only. `Coinc`
is a sibling of `Head`/`Act` in the generating set; `Sub.parent` already accepts it.

**Validated end-to-end** (`experiments/coincidence_tower.py`). Two groups A, B; box `a∈A` and
box `b∈B` carry signs `sa,sb`; the event `e=(sa==sb)` is a *cross-group coincidence* that only
the product `sa·sb` reveals (each marginal is noise). Encoder `data → [head(A),head(B)] →
top`, factoring through KQV (`KQVSystem`); train the top + a read-out to decode `e`:

| SNR | first-order top (`Head`) | second-order top (`Coinc`) |
|---|---|---|
| 3 | 0.60 | **0.72** |
| 5 | 0.66 | **0.90** |
| 8 | 0.70 | **0.99** |

The coincidence head clears the bar (up to 0.99) where the first-order head cannot; the gap
widens with signal. **Design lesson (in the code/tests):** do *not* make every level second
order — squaring destroys signs (`(±1)²=1`), erasing the features higher levels must correlate.
First-order summaries climb to *preserve* features; the coincidence head sits where two
features must be correlated. (The group heads above are frozen at uniform attention `w_star=0`
= mean pool, a valid head config, so they preserve the signal box instead of washing it out.)

**Relation to Generator 4 (residual head).** Both enrich the *upward* `out_f` beyond the
first-order pool; the residual head sends up *what was not explained*, the coincidence head
sends up *what co-varies*. The coincidence head is the one built and validated.

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
network, not a single head. The suboperad is the closure of the generators (head, prior box, and — proposed,
pending audit — the activation cell) under substitution. **Membership is by construction**: a `KQVTerm` is a generator
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

- What flows under `Φ`: weights only is the current suboperad; **weights + activations**
  is proposed *as* Generator 3 (the activation cell), pending audit; arbitrary per-box
  free state stays out. (The timescale split / how the cell is wired is experiment-layer.)
- The predictive-coding leaf potential `U = ½‖q − n‖²`.
- Heterogeneous per-box predictions (needed for addressing, Task 4).
- Positional encoding, if order matters.

Keeping these out of the suboperad is deliberate: the auditor must be able to see
that the generator is the paper's head and nothing more.
