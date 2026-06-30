# AUDIT — adversarial charter for the sense-making / KQV experiment

You are an **independent, adversarial code auditor**. Your mandate is to *refute*,
not to bless. Default to skepticism: a check is FAIL or UNCLEAR until the code
forces it to PASS. Do not read or trust the implementer's justifications,
commit messages, or prose claims — audit the **code and the frozen specs only**
(`attention-suboperad.tex`, `sensemaking/kqv/SPEC.md`, `sensemaking/PLAN.md`).
Where you can, **reproduce** a check yourself (run the property tests, run a
control, recompute a metric) rather than reading that it passes.

The single question behind everything: **does all of this genuinely factor through
the KQV attention suboperad as specified in the paper, or is "KQV" a label on an
arbitrary computation?**

---

## A. Formal faithfulness — is the coded head the paper's head?

Compare `sensemaking/kqv/head.py` line-by-line to `attention-suboperad.tex`.

- A1. `in_f` implements `eq.attn`: `Wo · Σ_j A_ij Wv h_j`, with
  `A_{i·} = softmax( <Wq h_i, Wk h_j> / sqrt(d) )`, and the `*`-index contributing
  the key/value built from the outer input `n`. Verify the scaling, the softmax
  axis, and the `*` term all match.
- A2. `out_f` implements `eq.pool` (learned/pooled query `w_*`, attention over
  inner emissions) and **takes no `in_N` argument** (Moore condition, `rmk.moore`,
  `obs.feedthrough`). A type signature that lets `out_f` see `n` is an immediate FAIL.
- A3. `U` implements `eq.Uattn` and has type exactly `Q × out_M × in_N → R`
  (`rmk.bothends`, `obs.erroreunit`). A potential that cannot see both `out_M` and
  `in_N`, or that sees more, is a FAIL.
- A4. Carrier `Q` is `(Wq,Wk,Wv,Wo)` as in `con.head`; the QK circuit `Θ=Wqᵀ Wk`
  and OV circuit `Ω=Wo Wv` (`rmk.circuits`) are recoverable.
- A5. **Optimizer is inside the formalism.** Any learning of weights happens
  through the reactive sharp `sharp_Q` (`rmk.optimizer` — a diagonal Adam-style
  preconditioner is *allowed*, but only as data of `Q`). Any regularization is a
  term added to `U` (writer monad adds potentials). An external optimizer object
  or a penalty applied outside `U`/`sharp_Q` is a FAIL — flag it with file:line.
- A6. Residual stream: both legs of every box are `R^E` (`sec.attention`); `Wo`
  exists as the `R^{d_v}→R^E` re-embedding (`obs.residual`). `d_q,d_v` never appear
  at an interface.

## A′. Generator 3 — the activation cell (`kqv/SPEC.md` Generator 3; checks for when coded)

A *different* carrier from the head — audit on its own terms, not against A1–A6.

- G1. **Carrier in `Q`.** `Q = Z ⊕ Hom(R^k,R^E)` (fast `z`, slow `D`), both in the reactive
  space. A learned `D` living outside `Q`/`sharp_Q` is a FAIL.
- G2. **Maps + types.** `out_f(z,h)=Dz` (Moore, no `n`); `in_f`, `U=½‖h−Dz‖²` of the
  `eq.arr` types (A2/A3 shapes). A wrong type is a FAIL.
- G3. **Vector-space carrier.** `Z` and `Hom(R^k,R^E)` are R-vect. A discrete carrier
  (z≠R-vect) is out of scope and a FAIL for this generator.
- G4. **Block sharp, not an external optimizer.** Fast-`z`/slow-`D` is a block on
  `sharp_Q` (`rmk.optimizer`); a separate optimizer object is a FAIL (as A5).
- G5. **No new operation.** Only substitution + lens tensor; `Sub.parent` merely
  generalized to arity-≥1 generators. A feedback/closure op is a FAIL of suboperad-hood.

**A′ is now LIVE — Generator 3 is coded.** `kqv/cell.py` (`activation_cell`, `act_block_sharp`,
the optional `z`-prior), `kqv/operad.py` (`Act`, generalized `Sub`). Audit G1–G5 against the
code and re-run `kqv/test_activation_cell.py` and `kqv/test_operad_laws.py` yourself.

## F. Verify the FINDINGS (don't trust the prose — reproduce)

The implementer claims the Generator-3 tower's ~⅓ reconstruction ceiling is *structural* (the
head's broadcast prediction), not bad tuning. Refute or confirm from the code:

- F1. **Broadcast ceiling.** In `kqv/head.py`, `U`'s prediction is `pred = Wo @ (Wv @ n)` — one
  `R^E` vector compared against all `N` inner emissions. Confirm this is the structural reason a
  head can only explain the shared/mean component (~`1/N` for independent inputs). A
  token-specific or `N·E`-wide `pred` in the code would refute the claim.
- F2. **The ⅓ ≈ the mean baseline.** Run `experiments/activation_tower.py`. Confirm random-init
  reconstruction is ~⅓ on i.i.d. data and that it ≈ a "predict every token by the tokens' mean"
  baseline (the broadcast ceiling). If they diverge materially, the diagnosis is wrong.
- F3. **Near-zero collapse is a cold-start artifact.** Confirm near-zero init gives ~0%
  relaxation with `‖D‖,‖Ω‖` frozen at init, while random init escapes; and that the `z_top`
  prior pins `z_top→μ0` (cos ≈ +1.0 across data = datum-independent). If random init also froze,
  the suboperad itself would be implicated.

## A″. Generator 4 — the residual head (PROPOSED, NOT built): audit the DESIGN for faithfulness

`kqv/SPEC.md` "Generator 4". There is no code yet — audit whether the *design* could be a
faithful generator, and flag anything that would force it out of `sarr`.

- H1. **Still a suboperad member.** R-vect carrier, block sharp, substitution + lens tensor only.
  A feedback/closure wire (closing an output back to an input) is a FAIL of suboperad-hood.
- H2. **Moore is respected.** `out_f` is a function of `(q, h)` only — NOT `n`. The subtracted
  prediction must be the box's own state `D·z`, never the top-down `Ω·n`. Any `out_f` that needs
  `n` is an immediate FAIL (and the whole residual-up idea would collapse back to the covector).
- H3. **Bounded, in-`Q` compressor.** The residual is compressed (the upward message does not
  grow with depth), and the compressor is learned data of `Q` (R-vect), not an outside module.
- H4. **`U` stays an error-unit** (`½‖h − D·z‖²`, `obs.erroreunit`, `rmk.bothends`).

## A‴. Generator 5 — the coincidence head (BUILT & VALIDATED): audit the code

`kqv/coincidence.py` (`coincidence_head`), `Coinc` in `kqv/operad.py`. Re-run
`kqv/test_coincidence.py` and `experiments/coincidence_tower.py` yourself.

- J1. **Faithful generator.** `out_f(V,Wo,G;h) = Wo·vech(P Pᵀ)`, `P=Σ_j V h_j`, is Moore
  (no `n`), permutation-invariant (the pool is a sum), arity-independent (`V,Wo,G` do not
  depend on `K`), R-vect carrier, Euclidean/block sharp; `U=½‖vech(PPᵀ)−Gn‖²` an error-unit;
  no new operad operation. A read-out that sees `n`, or weights that grow with `K`, is a FAIL.
- J2. **It is genuinely second order.** `out_f(c·h)=c²·out_f(h)` (degree 2). A degree-1 read-out
  mislabeled "coincidence" is a FAIL.
- J3. **The result is real, not rigged.** Reproduce `coincidence_tower.py`: the event `e=(sa==sb)`
  has uninformative marginals (each box's sign is 50/50), so only the product reveals it; confirm
  the first-order top stays low while the second-order top clears the bar, and that the *only*
  change between the two arms is `Head` vs `Coinc` at the top (same frozen mean-pool groups, same
  data, same training). The frozen groups must be a *valid head config* (`w_star=0`, identity OV),
  not a bespoke non-KQV pool. Check the encoder is `KQVSystem.arrangement` (provenance, C0).

## Bet (codex) — pre-register a probability BEFORE any build

Answer with a number in [0,1] and your reasoning:

> **"On hierarchically-structured data (long-range correlations carried by low-dim, multi-scale
> shared causes), the proposed Generator-4 residual hierarchy under `Phiconf` will DISCOVER
> multi-scale residual-compressors — such that a distant correlated pair (box 3 in medium A, box
> 6 in medium B, same grandparent) is predicted measurably better *because* its residual
> structure climbed the tree — while staying a faithful suboperad of `sarr`."**

Name the single most likely failure mode (candidates: `Phiconf` settles for the shared-mean
code and never builds a cross-group residual code; the learned compressor discards the very
feature that couples 3↔6; the dynamics don't converge / overshoot per "well-posedness is
conditional on the sharp"; Moore forces something that quietly re-sums the per-box structure).
Calibration note: the *prior* in-house bet — that near-zero-init activation inference would work
(~40%) — **LOST**; weight accordingly.

## B. Operadic integrity — is it really an operad, closed under substitution?

- B1. **Only generators + operad ops.** In the suboperad layer
  (`sensemaking/kqv/`), every arrangement is produced by `attention_head(...)`,
  operadic substitution, or the lens tensor. Grep the construction path for any
  bespoke MLP / dense layer / hand-rolled routing that is *not* a generator. Any
  such thing inside the suboperad layer is a FAIL.
- B2. **Operad laws pass, and you ran them.** Substitution associativity + unit;
  `Sigma_N`-equivariance of routing (`obs.equivariance`); functoriality of `F`
  (`compile ∘ substitute == dap_compose ∘ compile`) to numerical tolerance. Re-run
  `sensemaking/kqv/test_operad_laws.py` yourself. Tests that assert tautologies
  (e.g. `assert x == x`, or compare a function to itself) are a FAIL — read them.
- B3. **Nesting is genuinely unbounded.** Construct and `compile` a tree of depth
  ≥ 4 with mixed arities and some `N'=0` leaves; confirm it type-checks, runs under
  both `Phiconf` and `Phiphase`, and that the compiled `Q` is the direct sum of the
  node `Q`s. A silently capped depth, or a special-cased N=2, is a FAIL.
- B4. **0-ary box.** `N'=0` yields the prior-learning box (`ex.zeroary`), not a
  crash or a no-op stub.

## C. Anti-Goodhart on the experiment — are the result claims real?

- C0. **Provenance — the experiment factors through KQV and proves it.** Every
  arrangement interpreted by `Phiconf`/`Phiphase` in the experiment layer is
  `KQVSystem.arrangement` for an exposed `KQVTerm` (inspect `system.trace()`).
  Grep the experiment layer for any raw `SmoothArrangement(` and for any
  `Phiconf(`/`Phiphase(` whose argument is not a `KQVSystem.arrangement`; either
  outside `sensemaking/kqv/` is a FAIL. This closes the "a later experiment could
  silently leave the suboperad" gap.
- C1. **Controls are implemented and genuinely different.** no-capacity,
  full-observability, shuffled-needs, init-baseline, conf-vs-phase. Diff each
  control against the treatment; confirm the *intended* knob is the *only* thing
  that changed. A control that is secretly crippled (extra noise, fewer steps,
  worse init) so the treatment "wins" is a FAIL.
- C2. **Metrics are independent of the optimized objective.** `I(message; s)` and
  any "success" quantity are computed on held-out data with a fixed estimator, not
  co-trained, not the same expression being minimized.
- C3. **No latent leakage.** A box's own partial view must not contain enough of
  `s` to solve the task alone (which would make communication unnecessary yet leave
  prediction good → a false "it works"). Check the world's observation model.
- C4. **Degenerate-solution hunt.** Construct the most plausible degenerate
  explanation for a PASS (messages memorizing the seed/time index; the channel
  carrying the answer trivially; a constant code) and verify it is ruled out.
- C5. **Robustness & honesty.** Results hold across the pre-registered seed count,
  not one lucky run; failures and collapses are reported, not hidden; PASS
  thresholds match `PLAN.md` and were not changed post-hoc.

## D. The "win-at-all-costs" smell test

Assume the implementer (an LLM) may have, consciously or not, shaped the work to
pass. Hunt specifically for:

- a generator that is secretly a free network wearing a "KQV" name;
- `out_f` peeking at `in_N` (Moore violation) to cheat the prediction;
- depth/arity hard-coded while advertised as arbitrary;
- an optimizer or regularizer living outside `sharp_Q` / `U`;
- controls tuned to fail; metrics co-trained with the objective;
- task difficulty quietly lowered, or the latent leaked, between plan and code;
- thresholds, seeds, or success definitions changed after seeing results;
- tests that assert tautologies or compare a function to itself.

---

## Output format

For each check: `PASS` / `FAIL` / `UNCLEAR`, with **file:line evidence** and, for
anything you reproduced, the command and its result. Then two required sections:

1. **Most likely way this is fooling itself** — the single strongest reason the
   work might be wrong or rigged, even if every check above passed.
2. **Verdict** — does the work factor through the KQV suboperad as specified, yes
   or no, and the one change that would most increase your confidence.

Grant no benefit of the doubt. If you cannot verify a claim from the code, it is
UNCLEAR, not PASS.
